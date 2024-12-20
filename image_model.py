import os
import sys
import shutil
from astroquery.mast import Observations
from astropy.io import fits
import numpy as np
from reproject import reproject_interp
class ImageModel:
    def __init__(self):
        self.files = [None, None, None]
        self.coefficients = [1.0, 1.0, 1.0]

    def set_file(self, idx, filepath):
        self.files[idx] = filepath

    def set_coefficient(self, idx, value):
        self.coefficients[idx] = value

    def is_ready(self):
        return None not in self.files
    
    
    def reproduct(self, image1, image2, image3, data1, data2, data3):
        """Gère la reprojection des données si nécessaire.

        Args:
            image1 (str): Chemin vers le fichier FITS de référence.
            image2 (str): Chemin vers le deuxième fichier FITS.
            image3 (str): Chemin vers le troisième fichier FITS.
            data1 (ndarray): Données extraites du fichier 1 (rouge).
            data2 (ndarray): Données extraites du fichier 2 (vert).
            data3 (ndarray): Données extraites du fichier 3 (bleu).

        Returns:
            tuple: Les données reprojetées (ou originales si aucune reprojection n'est nécessaire).
        """
        with fits.open(image1) as hdul1, fits.open(image2) as hdul2, fits.open(image3) as hdul3:
            header_ref = hdul1[1].header if len(hdul1) > 1 else hdul1[0].header
            header2 = hdul2[1].header if len(hdul2) > 1 else hdul2[0].header
            header3 = hdul3[1].header if len(hdul3) > 1 else hdul3[0].header

            # Vérification de la présence de 'NAXIS1' et 'NAXIS2' avant d'y accéder
            if "NAXIS1" not in header_ref or "NAXIS2" not in header_ref:
                raise KeyError("Keyword 'NAXIS1' or 'NAXIS2' not found in the reference header.")

            # Reprojection pour le fichier 2
            if (
                "NAXIS1" not in header2
                or "NAXIS2" not in header2
                or header2["NAXIS1"] != header_ref["NAXIS1"]
                or header2["NAXIS2"] != header_ref["NAXIS2"]
            ):
                data2, _ = reproject_interp((data2, header2), header_ref)

            # Reprojection pour le fichier 3
            if (
                "NAXIS1" not in header3
                or "NAXIS2" not in header3
                or header3["NAXIS1"] != header_ref["NAXIS1"]
                or header3["NAXIS2"] != header_ref["NAXIS2"]
            ):
                data3, _ = reproject_interp((data3, header3), header_ref)

        return data1, data2, data3

    def load_combined_image(self):
        if not self.is_ready():
            return None

        # Chargement des données des fichiers FITS
        red_data = fits.getdata(self.files[0])
        green_data = fits.getdata(self.files[1])
        blue_data = fits.getdata(self.files[2])

        # Vérification et reprojection des données si nécessaire
        red_data, green_data, blue_data = self.reproduct(self.files[0], self.files[1], self.files[2], red_data, green_data, blue_data)

        # Normalisation des données
        red = self._normalize(red_data) * self.coefficients[0]
        green = self._normalize(green_data) * self.coefficients[1]
        blue = self._normalize(blue_data) * self.coefficients[2]

        # Vérification de la forme des données après reprojection
        if red.shape != green.shape or green.shape != blue.shape:
            raise ValueError("Les dimensions des images RGB ne sont pas identiques après reprojection.")

        # Empilage des canaux RGB
        image = np.stack([np.clip(red, 0, 1), np.clip(green, 0, 1), np.clip(blue, 0, 1)], axis=-1)
        return image


    @staticmethod
    def _normalize(data):
        vmin, vmax = np.percentile(data, (1, 99))
        return np.clip((data - vmin) / (vmax - vmin), 0, 1)

    def download(self, objet: str, telescope: str, radius: str, filters: list) -> tuple:
        """
        Télécharge les fichiers FITS correspondant à un objet céleste.
        """
        if not objet:
            return "Le nom doit être valide."

        if not telescope:
            return "Le nom de telescope doit être valide."

        if not radius:
            return "Le rayon doit être valide."

        if not filters:
            return "Les filtres doivent être valides."

        errors = []
        fichiers_fits = []
        if not self.verif_files_dl(objet, telescope, radius):
            try:
                result_filtered = Observations.query_criteria(
                    objectname=objet,
                    radius=radius,
                    obs_collection=telescope,
                    dataRights="PUBLIC",
                )

                for filtre in filters:
                    filtered_result = result_filtered[result_filtered["filters"] == filtre]

                    if len(filtered_result) > 0:
                        obs_id = filtered_result[0]["obsid"]
                        products = Observations.get_product_list(obs_id)

                        fits_files = Observations.filter_products(
                            products, extension=["fits", "fit", "fz"], mrp_only=False
                        )

                        if len(fits_files) > 0:
                            fits_files.sort("size", reverse=True)
                            downloaded = Observations.download_products(
                                fits_files[int(len(fits_files) / 2)],
                                download_dir=sys.path[0],
                                mrp_only=False,
                            )
                            fichiers_fits.extend(downloaded["Local Path"])
                        else:
                            errors.append(f"Aucun fichier FITS disponible pour le filtre {filtre}")
                    else:
                        errors.append(f"Pas d'observation trouvée pour le filtre {filtre}")

                self.rename_and_replace(objet, telescope, radius, fichiers_fits)
            except Exception as e:
                errors.append(f"Erreur lors de la requête : {e}")
        else:
            errors.append(f"Les 3 fichiers sont déjà dans le répertoire.")

        return fichiers_fits, errors

    def rename_and_replace(self, objet: str, telescope: str, radius: str, fichiers_fits: list):
        """
        Renomme et déplace les fichiers téléchargés dans un dossier structuré.
        """
        if not telescope:
            return "Le nom de telescope doit être valide."

        chemin = sys.path[0]
        liste = ["red.fits", "green.fits", "blue.fits"]

        dossier_nom = (
            telescope.replace(" ", "_")
            + "_"
            + objet.replace(" ", "_")
            + "_"
            + radius.replace(" ", "_")
        )
        dossier_nom = chemin + "/Donnees/" + dossier_nom
        os.makedirs(dossier_nom)

        if len(fichiers_fits) == 3:
            for id_fichier in range(len(fichiers_fits)):
                os.rename(fichiers_fits[id_fichier], dossier_nom + "/" + liste[id_fichier])
            os.chmod(chemin + "/mastDownload/", 0o777)
            shutil.rmtree(chemin + "/mastDownload/")
        else:
            os.chmod(dossier_nom, 0o777)
            shutil.rmtree(dossier_nom)
            dossier_nom = chemin + "/mastDownload/"
            os.chmod(dossier_nom, 0o777)
            shutil.rmtree(dossier_nom)

    def verif_files_dl(self, objet: str, telescope: str, radius: str) -> bool:
        """
        Vérifie si les fichiers nécessaires ont déjà été téléchargés.
        """
        dossier_nom = (
            telescope.replace(" ", "_")
            + "_"
            + objet.replace(" ", "_")
            + "_"
            + radius.replace(" ", "_")
        )
        dossier_nom = sys.path[0] + "/Donnees/" + dossier_nom

        if os.path.exists(dossier_nom) and os.path.isdir(dossier_nom):
            if len(os.listdir(dossier_nom)) == 3:
                return True
            else:
                os.chmod(dossier_nom, 0o777)
                shutil.rmtree(dossier_nom)
        return False

