# Import des bibliothèques nécessaires
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------
# Lecture et affichage d'une image FITS
# ------------------------------
def load_and_display_fits(file_path, title=None, cmap="inferno"):
    """
    Charge et affiche une image FITS avec une colormap spécifique.

    :param file_path: Chemin du fichier FITS.
    :param title: Titre à afficher sur l'image (facultatif).
    :param cmap: Colormap à utiliser pour l'affichage.
    """
    # Chargement des données FITS
    print(f"Chargement du fichier FITS : {file_path}")
    with fits.open(file_path) as hdul:
        data = hdul[0].data  # Extraction des données de l'image
        header = hdul[0].header  # Extraction des métadonnées

    # Affichage des données
    plt.figure(figsize=(8, 8))
    plt.imshow(data, cmap=cmap, origin="lower")
    plt.colorbar(label="Intensité")
    plt.title(title if title else f"Image : {header.get('OBJECT', 'Inconnue')}")
    plt.show()

# ------------------------------
# Combinaison multispectrale (sans écriture de fichier)
# ------------------------------
def combine_multispectral_images(image_files, weights=None):
    """
    Combine plusieurs images FITS en une image composite, et l'affiche sans enregistrer de fichier.

    :param image_files: Liste des chemins des fichiers FITS.
    :param weights: Liste des poids à attribuer à chaque canal (facultatif).
    """
    print("Combinaison des images multispectrales...")
    data_list = []
    
    # Chargement des données de chaque image
    for i, file in enumerate(image_files):
        with fits.open(file) as hdul:
            data = hdul[0].data
            data_list.append(data)
    
    # Application des poids si spécifiés
    if weights is None:
        weights = [1] * len(data_list)  # Poids égaux si non spécifiés

    combined_data = np.zeros_like(data_list[0], dtype=np.float32)
    for i, data in enumerate(data_list):
        combined_data += weights[i] * data

    # Normalisation de l'image finale
    combined_data = (combined_data - combined_data.min()) / (combined_data.max() - combined_data.min())

    # Affichage de l'image combinée
    plt.figure(figsize=(8, 8))
    plt.imshow(combined_data, cmap="viridis", origin="lower")  # Colormap finale "viridis"
    plt.colorbar(label="Intensité combinée")
    plt.title("Image Multispectrale Combinée")
    plt.show()

# ------------------------------
# Exemple d'utilisation
# ------------------------------
if __name__ == "__main__":
    # Liste des fichiers FITS (format .fit)
    fits_files = [
        "Tarantula_Nebula-halpha.fit",
        "Tarantula_Nebula-oiii.fit",
        "Tarantula_Nebula-sii.fit"
    ]

    # Colormaps spécifiques pour chaque canal
    colormaps = ["inferno", "cividis", "plasma"]  # Trois colormaps bien distinctes

    # Étape 1 : Affichage des images individuelles
    for file, cmap in zip(fits_files, colormaps):
        title = f"Image : {file.split('-')[-1].replace('.fit', '').upper()}"
        load_and_display_fits(file, title=title, cmap=cmap)

    # Étape 2 : Combinaison multispectrale (sans écriture de fichier)
    weights = [0.4, 0.3, 0.3]  # Poids pour les canaux Halpha, OIII et SII
    combine_multispectral_images(fits_files, weights=weights)
