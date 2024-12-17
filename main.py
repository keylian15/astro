from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

# ====== Recupération ======
image1 = "Tarantula_Nebula-halpha.fit"
image2 = "Tarantula_Nebula-oiii.fit"
image3 = "Tarantula_Nebula-sii.fit"

img4 = "./test/red.fits"
img5 = "./test/green.fits"
img6 = "./test/blue.fits"
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

    data1 = fits.getdata(image1)
    data2 = fits.getdata(image2)
    data3 = fits.getdata(image3)

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


# # Normal
# afficher([image1, image2, image3], 1, 1, 1)
# # + de rouge
# afficher([image1, image2, image3], 1.5, 1, 1, "Image Combinée avec + de Red")
# # + de vert
# afficher([image1, image2, image3], 1, 1.5, 1, "Image Combinée avec + de Green")
# # + de bleu
# afficher([image1, image2, image3], 1, 1, 1.5, "Image Combinée avec + de Blue")

# afficher([img4, img5, img6], 1, 1, 1, "test dl")
# Il va me dire qu'il y a un probleme de taille sauf que ca renvoie que des nan :
# print(f"Affichage premiere matrice : \n{fits.getdata(img4)}")
# print(f"Affichage deuxieme matrice : \n{fits.getdata(img5)}")
# print(f"Affichage troisieme matrice : \n{fits.getdata(img6)}")
# Ca ne change rien toujours des nan.
# img4 = np.nan_to_num(img4)
