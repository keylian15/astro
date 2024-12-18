from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import sys
# ====== Recupération ======
image1 = "Tarantula_Nebula-halpha.fit"
image2 = "Tarantula_Nebula-oiii.fit"
image3 = "Tarantula_Nebula-sii.fit"
# ====== Fin Recupération ======


def normaliser(data):
    """Fonction permettant de normaliser les données."""

    # Percentile -> renvoi le 1er percentile et le 99e percentile des valeurs dans data.
    # Pour les supprimer.
    vmin, vmax = np.percentile(data, (1, 99))
    data_norm = np.clip((data - vmin) / (vmax - vmin), 0, 1)

    return data_norm

def afficher(
    fichiers, multi_r=1.0, multi_g=1.0, multi_b=1.0, titre: str = "Image Combinée"
):
    """Fonction qui affiche une image combiné de 3 fichiers avec un coef de RGB possible."""
    image1 = fichiers[0]
    image2 = fichiers[1]
    image3 = fichiers[2]

    # data1 = fits.getdata(image1)
    # data2 = fits.getdata(image2)
    # data3 = fits.getdata(image3)

    data1 = extraire_image(image1)
    data2 = extraire_image(image2)
    data3 = extraire_image(image3)
    
    red = normaliser(data1) * multi_r
    green = normaliser(data2) * multi_g
    blue = normaliser(data3) * multi_b

    red = np.clip(red, 0, 1)
    green = np.clip(green, 0, 1)
    blue = np.clip(blue, 0, 1)

    image = np.stack([red, green, blue], axis=-1)

    plt.imshow(image, origin="lower")
    plt.colorbar()
    plt.title(titre)
    plt.show()

def extraire_image(fichier_fits):
    """
    Fonction qui parcourt un fichier FITS et retourne les données de la première extension ImageHDU
    contenant des données (si plusieurs extensions sont présentes).
    """
    with fits.open(fichier_fits) as hdul:
        if len(hdul) == 1 : 
            return fits.getdata(fichier_fits)
        
        # Parcours des extensions à partir de l'index 1 (ignorer le Primary HDU à l'index 0)
        for i in range(1, len(hdul)):
            hdu = hdul[i]
            if isinstance(hdu, fits.ImageHDU) and hdu.data is not None:
                return hdu.data  # Retourne les données de la première extension valide trouvée
    
    return None


# # Normal
# afficher([image1, image2, image3], 1, 1, 1)
# # + de rouge
# afficher([image1, image2, image3], 1.5, 1, 1, "Image Combinée avec + de Red")
# # + de vert
# afficher([image1, image2, image3], 1, 1.5, 1, "Image Combinée avec + de Green")
# # + de bleu
# afficher([image1, image2, image3], 1, 1, 1.5, "Image Combinée avec + de Blue")

dossier_test = sys.path[0] + "/Donnees/HST_NGC_6362_0.01_deg/"
t1 = dossier_test + "red.fits" 
t2 = dossier_test + "green.fits" 
t3 = dossier_test + "blue.fits" 
afficher([t1,t2,t3])
