from astropy.io import fits
from astroquery.mast import Observations
import numpy as np
import os, sys, shutil

class FITSModel:
    def __init__(self):
        self.download_dir = os.path.join(sys.path[0], "Donnees")
        os.makedirs(self.download_dir, exist_ok=True)

    @staticmethod
    def normaliser(data):
        vmin, vmax = np.percentile(data, (1, 99))
        return np.clip((data - vmin) / (vmax - vmin), 0, 1)

    @staticmethod
    def extraire_image(fichier_fits):
        with fits.open(fichier_fits) as hdul:
            if len(hdul) == 1:
                return fits.getdata(fichier_fits)
            for hdu in hdul[1:]:
                if isinstance(hdu, fits.ImageHDU) and hdu.data is not None:
                    return hdu.data
        return None

    def verif_files_dl(self, objet, telescope, radius):
        dossier_nom = f"{telescope.replace(' ', '_')}_{objet.replace(' ', '_')}_{radius.replace(' ', '_')}"
        dossier_path = os.path.join(self.download_dir, dossier_nom)
        if os.path.exists(dossier_path) and len(os.listdir(dossier_path)) == 3:
            return dossier_path
        return None

    def download(self, objet, telescope, radius, filtres):
        dossier_path = self.verif_files_dl(objet, telescope, radius)
        if dossier_path:
            return [os.path.join(dossier_path, f) for f in ["red.fits", "green.fits", "blue.fits"]], []

        errors = []
        fichiers_fits = []

        try:
            result_filtered = Observations.query_criteria(
                objectname=objet, radius=radius, obs_collection=telescope, dataRights="PUBLIC"
            )
            for filtre in filtres:
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
                            fits_files[int(len(fits_files) / 2)], download_dir=sys.path[0], mrp_only=False
                        )
                        fichiers_fits.append(downloaded["Local Path"][0])
                    else:
                        errors.append(f"Aucun fichier FITS disponible pour le filtre {filtre}")
                else:
                    errors.append(f"Pas d'observation trouvée pour le filtre {filtre}")

            self.rename_and_replace(objet, telescope, radius, fichiers_fits)
        except Exception as e:
            errors.append(f"Erreur lors de la requête : {e}")

        return fichiers_fits, errors

    def rename_and_replace(self, objet, telescope, radius, fichiers_fits):
        dossier_nom = f"{telescope.replace(' ', '_')}_{objet.replace(' ', '_')}_{radius.replace(' ', '_')}"
        dossier_path = os.path.join(self.download_dir, dossier_nom)
        os.makedirs(dossier_path, exist_ok=True)

        if len(fichiers_fits) == 3:
            for i, name in enumerate(["red.fits", "green.fits", "blue.fits"]):
                os.rename(fichiers_fits[i], os.path.join(dossier_path, name))
            shutil.rmtree(os.path.join(sys.path[0], "mastDownload"), ignore_errors=True)
