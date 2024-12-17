"""
Fichier de test n°2 : Pour les téléchargements.
Résultat : Il renvoie la listes d'un fichier parmis tous ceux trouvés pour certaines filtres RGB (correct)
Probleme : Spésification dans le HST donc problemes futurs !
"""

from astroquery.mast import Observations

# Paramètres de recherche
objet = "NGC 6362"
radius = "0.01 deg"  # Réduire le rayon de recherche
filtres = ["F814W", "F658N", "F336W"]  # Filtres à tester
fichiers_fits = []

try:
    # Requête initiale
    result = Observations.query_object(objet, radius=radius)
    print(f"Nombre d'observations trouvées : {len(result)}")
    
    for filtre in filtres:
        # Filtrage des observations contenant le filtre
        filtered_result = result[[filtre in f for f in result['filters']]]
        # # On test autrement ici :=
        # filtered_result = result[result['filters'] == filtre]

        if len(filtered_result) > 0:
            # # Trier pour choisir l'observation avec le plus haut calib_level
            # filtered_result.sort('calib_level', reverse=True)
            obs_id = filtered_result[0]['obsid']
            
            # Obtenir la liste des produits FITS
            products = Observations.get_product_list(obs_id)
            fits_files = Observations.filter_products(
                products,
                extension=["fits", "fit", "fz"],
                description="HAP fits science image"  # Optionnel pour filtrer des fichiers précis
            )
            
            if len(fits_files) > 0:
                # Télécharger le premier fichier FITS trouvé

                downloaded = Observations.download_products(fits_files[:1])
                fichiers_fits.append(downloaded['Local Path'][0])
                print(f"Fichier téléchargé pour {filtre} : {downloaded['Local Path'][0]} ") #{downloaded['Local Path'][0]}
            else:
                print(f"Aucun fichier FITS disponible pour le filtre {filtre}")
        else:
            print(f"Pas d'observation trouvée pour le filtre {filtre}")

except Exception as e:
    print("Erreur lors de la requête :", e)

print("Fichiers téléchargés :", fichiers_fits)
