"""
Fichier de test n°3 : Pour les téléchargements.
Résultat : Il telecharge le 1er fichier trouvé pour certaines filtres RGB (correct)
"""

from astroquery.mast import Observations
import sys, os, shutil


def download(objet: str, telescope: str, radius: str, filter) -> tuple:
    """_summary_

    Args:
        objet (str): Le nom de l'objet celeste.
        telescope (str): Le telescope.
        radius (str): Le rayon d'observation.
        filter (_type_): Les filtres utilisés par les fichiers fits.

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

    if verif_files_dl(objet, telescope, radius):
        pass
    else:
        pass

    try:
        errors = []

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
                        fits_files[:1], download_dir=sys.path[0], mrp_only=False
                    )

                    # Ajouter les chemins locaux des fichiers téléchargés à la liste
                    fichiers_fits.extend(downloaded["Local Path"])

                else:
                    errors.append(
                        "Aucun fichier FITS disponible pour le filtre {}".format(filtre)
                    )
                    # print(f"Aucun fichier FITS disponible pour le filtre {filtre}")
            else:
                errors.append(
                    "Pas d'observation trouvée pour le filtre {}".format(filtre)
                )
                # print(f"Pas d'observation trouvée pour le filtre {filtre}")

        # On replace correctement les images
        rename_and_replace(objet, telescope, radius, fichiers_fits)
        return fichiers_fits, errors

    except Exception as e:
        errors.append(f"Erreur lors de la requête :{e}")

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

        shutil.rmtree(chemin + "/mastDownload/")


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

    if (
        os.path.exists(dossier_nom)
        and os.path.isdir(dossier_nom)
        and len(os.listdir(dossier_nom)) == 3
    ):
        return True
    return False


# Paramètres de recherche
objet = "NGC 6362"
telescope = "HST"
radius = "0.01 deg"  # Réduire le rayon de recherche
filtres = ["F814W", "F658N", "F336W"]  # Filtres RGB à tester
fichiers_fits = []
errors = []

# fichier_fits, errors = download(objet, telescope, radius, filtres)
# download(objet, telescope, radius, filtres)
print(verif_files_dl(objet, telescope, radius))
