"""
Fichier de test n°1 : Pour les téléchargements.
Résultat : Il renvoie la listes de tous les fichiers trouvés pour certaines filtres RGB (correct)
"""


from astroquery.mast import Observations

# Paramètres de recherche
objet = "NGC 6362"
# objet = "NGC 7000"
radius = "0.01 deg"  # Réduire le rayon de recherche
filtres = ["F814W", "F658N", "F336W"]  # Nouveaux filtres à tester
# filtres = ['F606W', 'F555W', 'F658N;F625W', 'IRAC2', 'F439W', 'F336W', 'F658N', 'UVM2', 'F814W;F606W', 'F814W;F625W;F606W', 'F336W;F275W', 'F625W', 'F814W', 'detection', 'F275W', 'TESS', 'DETECTION', 'IRAC1', 'F438W', 'UVW2', 'G430M', 'MIRVIS', 'F785LP', 'F555W;F439W', 'UVW1']
fichiers_fits = []

try:
    result = Observations.query_object(objet, radius=radius)
    print(f"Nombre d'observations trouvées : {len(result)}")

    # filtres_disponibles = set(result['filters'])
    # print("Filtres disponibles :", filtres_disponibles)
    
    # # for element in filtres : 
    # #     if element in filtres_disponibles : 
    # #         print(f"Filre {element} possible.")
    
    for filtre in filtres:
        # Filtrer les observations pour un filtre donné
        filtered_result = result[result['filters'] == filtre]
        
        # print(filtered_result)
        
        if len(filtered_result) > 0:
            obs_id = filtered_result[0]['obsid'] 
            
            # Lister et filtrer les produits FITS
            products = Observations.get_product_list(obs_id)
            
            fits_files = Observations.filter_products(
                products,
                # description = "HAP fits science image",
                extension=["fits", "fit", "fz"]
            )

            # fits_files = [product for product in fits_files if product['calib_level'] == 2]
            
            # Télécharger les fichiers FITS si disponibles
            print(f"len de fits_files : {len(fits_files)}")
            
            if len(fits_files) > 0:
                # downloaded = Observations.download_products(fits_files)
                # fichiers_fits.append(downloaded['Local Path'][0])
                print(f"Fichier a télécharger !\n{fits_files}") #{fits_files}
            else:
                print(f"Aucun fichier FITS disponible pour le filtre {filtre}")
        else:
            print(f"Pas d'observation trouvée pour le filtre {filtre}")

except Exception as e:
    print("Erreur lors de la requête :", e)

print("Fichiers téléchargés :", fichiers_fits)
