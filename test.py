from astroquery.mast import Observations

# Rechercher des observations pour un objet céleste
# result = Observations.query_object("Orion Nebula", radius="0.1 deg")
result = Observations.query_object("NGC 6362", radius="0.05 deg")

# Filtrer pour des observations avec un filtre spécifique
# filtres = ["F656N", "F502N", "F673N"]  # Exemple : H-alpha, OIII, SII
filtres = ["F625W", "F555W", "F438W"]  # Exemple de filtres à utiliser

fichiers_fits = []

for filtre in filtres:
    # Filtrer les résultats pour chaque filtre
    filtered_result = result[result['filters'] == filtre]
    
    if len(filtered_result) > 0:
        obs_id = filtered_result[0]['obsid']  # Première observation
        products = Observations.get_product_list(obs_id)  # Produits associés
        fits_files = Observations.filter_products(products, productSubGroupDescription="FITS")
        
        # Télécharger les fichiers FITS
        downloaded = Observations.download_products(fits_files)
        fichiers_fits.append(downloaded['Local Path'][0])  # Chemin local du fichier téléchargé
    else:
        print(f"Pas d'observation trouvée pour le filtre {filtre}")

print("Fichiers téléchargés :", fichiers_fits)

