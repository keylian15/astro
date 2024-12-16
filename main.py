from astropy.io import fits 
import matplotlib.pyplot as plt 

# ====== Variables Globales ======
Halpha = './Tarantula_Nebula-halpha.fit'
Oiii = './Tarantula_Nebula-oiii.fit'
Sii = './Tarantula_Nebula-sii.fit'
# ====== Fin Variables Globales ======

def afficher(chemin : str ) : 
    """"""
    
    data = fits.getdata(chemin)

    plt.imshow(data, cmap= 'gray')
    plt.colorbar()
    plt.show()
    
# Choix user.
choix = input("Choissisez l'image :\n1 -> Halpha.\n2 -> Oiii.\n3 -> Sii.\n")
if choix == '1' : 
    afficher(Halpha)
if choix == '2' : 
    afficher(Oiii)
if choix == '3' : 
    afficher(Sii)