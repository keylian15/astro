from astropy.io import fits
from astroquery.mast import Observations
import matplotlib.pyplot as plt
import numpy as np
import sys, os, shutil
from reproject import reproject_interp


def normaliser(data):
    """Fonction permettant de normaliser les données."""

    # Percentile -> renvoi le 1er percentile et le 99e percentile des valeurs dans data.
    # Pour les supprimer.
    vmin, vmax = np.percentile(data, (1, 99))
    data_norm = np.clip((data - vmin) / (vmax - vmin), 0, 1)

    return data_norm


def extraire_image(fichier_fits: str):
    """Fonction qui parcourt un fichier FITS et retourne les données de la première extension ImageHDU
    contenant des données (si plusieurs extensions sont présentes).

    Args:
        fichier_fits (str): Le chemin de fichier

    Returns:
        Tuple: L'equivalant d'un fits.getData
    """
    with fits.open(fichier_fits) as hdul:
        if len(hdul) == 1:
            return fits.getdata(fichier_fits)

        # Parcours des extensions à partir de l'index 1 (ignorer le Primary HDU à l'index 0)
        for i in range(1, len(hdul)):
            hdu = hdul[i]
            if isinstance(hdu, fits.ImageHDU) and hdu.data is not None:
                return (
                    hdu.data
                )  # Retourne les données de la première extension valide trouvée

    return None


def reproduct(image1, image2, image3, data2, data3):
    """Gère la reprojection des données si nécessaire.

    Args:
        image1 (str): Chemin vers le fichier FITS de référence.
        image2 (str): Chemin vers le deuxième fichier FITS.
        image3 (str): Chemin vers le troisième fichier FITS.
        data2 (ndarray): Données extraites du fichier 2.
        data3 (ndarray): Données extraites du fichier 3.

    Returns:
        tuple: Les données reprojetées (ou originales si aucune reprojection n'est nécessaire).
    """
    with fits.open(image1) as hdul1, fits.open(image2) as hdul2, fits.open(
        image3
    ) as hdul3:
        header_ref = hdul1[1].header if len(hdul1) > 1 else hdul1[0].header
        header2 = hdul2[1].header if len(hdul2) > 1 else hdul2[0].header
        header3 = hdul3[1].header if len(hdul3) > 1 else hdul3[0].header

        # Vérifier la présence de 'NAXIS1' et 'NAXIS2' avant d'y accéder
        if "NAXIS1" not in header_ref or "NAXIS2" not in header_ref:
            raise KeyError(
                "Keyword 'NAXIS1' or 'NAXIS2' not found in the reference header."
            )

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

    return data2, data3


def verifier_objet_celeste_multiple(fichiers: list) -> bool:
    """
    Vérifie que les trois fichiers FITS pointent vers le même objet céleste.

    Args:
        fichiers (list): Liste de chemins vers les fichiers FITS.

    Returns:
        bool: True si tous les fichiers pointent vers le même objet céleste, False sinon.
    """
    # Extraire l'objet céleste du premier fichier
    with fits.open(fichiers[0]) as hdul1:
        if len(hdul1) == 1:
            header1 = hdul1[0].header
        else:
            header1 = hdul1[1].header
        objet1 = header1.get("OBJECT", None)

    # Vérifier les autres fichiers
    for fichier in fichiers[1:]:
        with fits.open(fichier) as hdul:
            if len(hdul) == 1:
                header = hdul[0].header
            else:
                header = hdul[1].header
            objet = header.get("OBJECT", None)

            # Si l'objet n'est pas trouvé ou est différent, retourner False
            if objet != objet1 or objet is None:
                return False

    return True


def afficher(
    fichiers: list,
    multi_r: float = 1.0,
    multi_g: float = 1.0,
    multi_b: float = 1.0,
    titre: str = "Image Combinée",
):
    """Fonction qui affiche une image combinée de 3 fichiers avec un coef de RGB possible.

    Args:
        fichiers (list): La liste des fichiers à combiner.
        multi_r (float, optional): Le multiplicateur de rouge. Defaults to 1.0.
        multi_g (float, optional): Le multiplicateur de vert. Defaults to 1.0.
        multi_b (float, optional): Le multiplicateur de bleu. Defaults to 1.0.
        titre (str, optional): Le titre du graphique. Defaults to "Image Combinée".
    """

    if not verifier_objet_celeste_multiple(fichiers):
        print(
            "Les fichiers ne proviennent pas du même objet céleste ou les coordonnées ne sont pas renseigné."
        )

    image1, image2, image3 = fichiers

    data1 = extraire_image(image1)
    data2 = extraire_image(image2)
    data3 = extraire_image(image3)

    data2, data3 = reproduct(image1, image2, image3, data2, data3)

    # Normalisation des données
    red = normaliser(data1) * multi_r
    green = normaliser(data2) * multi_g
    blue = normaliser(data3) * multi_b

    # Limiter les valeurs à l'intervalle [0, 1]
    red = np.clip(red, 0, 1)
    green = np.clip(green, 0, 1)
    blue = np.clip(blue, 0, 1)

    # Combinaison des canaux
    image = np.stack([red, green, blue], axis=-1)

    # Affichage
    plt.imshow(image, origin="lower")
    plt.colorbar()
    plt.title(titre)
    plt.show()


def download(objet: str, telescope: str, radius: str, filter: list) -> tuple:
    """_summary_

    Args:
        objet (str): Le nom de l'objet celeste.
        telescope (str): Le telescope.
        radius (str): Le rayon d'observation.
        filter (list): Les filtres utilisés par les fichiers fits.

    Returns:
        tuple: La liste des chemins dl et les erreurs possibles.
    """

    # ====== Verification Données ======
    if not objet:
        return "Le nom doit être valide."

    if not telescope:
        return "Le nom de telescope doit être valide."

    if not radius:
        return "Le rayon doit être valide."

    if not filter:
        return "Les filtres doivent être valide."
    # ====== Fin Verification Données ======

    errors = []
    if not verif_files_dl(objet, telescope, radius):

        try:

            # Filtrer les observations par des critères spécifiques si nécessaire
            result_filtered = Observations.query_criteria(
                objectname=objet,
                radius=radius,
                obs_collection=telescope,
                dataRights="PUBLIC",
            )

            for filtre in filtres:
                filtered_result = result_filtered[result_filtered["filters"] == filtre]

                if len(filtered_result) > 0:
                    obs_id = filtered_result[0]["obsid"]

                    # Récupérer les produits associés à l'observation
                    products = Observations.get_product_list(obs_id)

                    # Filtrer pour ne garder que les fichiers FITS
                    fits_files = Observations.filter_products(
                        products, extension=["fits", "fit", "fz"], mrp_only=False
                    )

                    if len(fits_files) > 0:

                        fits_files.sort("size", reverse=True)

                        # Télécharger les fichiers FITS
                        downloaded = Observations.download_products(
                            fits_files[int(len(fits_files) / 2)],
                            download_dir=sys.path[0],
                            mrp_only=False,
                        )

                        # Ajouter les chemins locaux des fichiers téléchargés à la liste
                        fichiers_fits.extend(downloaded["Local Path"])

                    else:
                        errors.append(
                            "Aucun fichier FITS disponible pour le filtre {}".format(
                                filtre
                            )
                        )
                else:
                    errors.append(
                        "Pas d'observation trouvée pour le filtre {}".format(filtre)
                    )

            # On replace correctement les images
            rename_and_replace(objet, telescope, radius, fichiers_fits)

        except Exception as e:
            errors.append(f"Erreur lors de la requête :{e}")
    else:
        errors.append(f"Les 3 fichiers sont déjà dans le répertoire.")
    return fichiers_fits, errors


def rename_and_replace(objet: str, telescope: str, radius: str, fichiers_fits: list):
    """Fonction permettant de remplacer le nom des fichiers par red/green/blue.fits
    et de les mettres dans un répertoire sous la forme NOM TELESCOPE _ NOM OBJET _ RAYON

    Args:
        objet (str): Le nom de l'objet celeste.
        telescope (str): Le telescope.
        radius (str): Le rayon d'observation.
        fichiers_fits (list): Les 3 chemins de fichiers télécharger.

    Returns:
        None: Effet de bord : Replacement et renamage des fichiers, suppressions de fichiers tempos.
    """
    # ====== Verification Données ======
    if not telescope:
        return "Le nom de telescope doit être valide."
    # ====== Fin Verification Données ======
    chemin = sys.path[0]

    liste = ["red.fits", "green.fits", "blue.fits"]

    # Création du dossier de type NOM TELESCOPE _ NOM OBJET _ RAYON
    dossier_nom = (
        telescope.replace(" ", "_")
        + "_"
        + objet.replace(" ", "_")
        + "_"
        + radius.replace(" ", "_")
    )
    dossier_nom = chemin + "/Donnees/" + dossier_nom
    os.makedirs(dossier_nom)

    # Cas correct : On renomme et deplace
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


def verif_files_dl(objet: str, telescope: str, radius: str) -> bool:
    """Fonction permettant de verifier si des fichiers ont déja été telecharger et qu'ils sont tous la.

    Args:
        objet (str): Le nom de l'objet celeste.
        telescope (str): Le telescope.
        radius (str): Le rayon d'observation.

    Returns:
        Bool: Presence ou non.
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


if __name__ == "__main__":

    # ====== Test Affichage Normal  ======
    # image1 = sys.path[0] + "/Donnees/Exemple/Tarantula_Nebula-halpha.fit"
    # image2 = sys.path[0] + "/Donnees/Exemple/Tarantula_Nebula-oiii.fit"
    # image3 = sys.path[0] + "/Donnees/Exemple/Tarantula_Nebula-sii.fit"
    # afficher([image1, image2, image3], 1, 1, 1)
    # ====== Fin Test Affichage ======

    # ====== Test Telechargement Hubble ======
    objet = "NGC 6362"
    telescope = "HST"
    radius = "0.005 deg"
    filtres = ["F814W", "F658N", "F336W"]
    fichiers_fits = []
    errors = []
    fichiers_fits, errors = download(objet, telescope, radius, filtres)
    if errors:
        print(errors)
    dossier_test = f"{sys.path[0]}/Donnees/{telescope}_{objet.replace(" ","_")}_{radius.replace(" ","_")}/"
    t1 = dossier_test + "red.fits"
    t2 = dossier_test + "green.fits"
    t3 = dossier_test + "blue.fits"
    afficher([t1, t2, t3])
    # ====== Fin Test Telechargement Hubble ======

    # ====== Test Données USB ======
    # c = sys.path[0]
    # afficher(
    #     [
    #         c + "/Donnees/data_jw01783/jw01783-o001_t001_nircam_clear-f115w/jw01783-o001_t001_nircam_clear-f115w_i2d.fits",
    #         c + "/Donnees/data_jw01783/jw01783-o001_t001_nircam_clear-f115w/jw01783-o001_t001_nircam_clear-f115w_i2d.fits",
    #         c + "/Donnees/data_jw01783/jw01783-o001_t001_nircam_clear-f115w/jw01783-o001_t001_nircam_clear-f115w_segm.fits",
    #     ]
    # )
    # ====== Fin Test Données USB ======
    print("")