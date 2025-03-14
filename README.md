## Documentation des fichiers Python

### Fichier : `main_image.py`

#### Fonction principale
- **Rôle** :
  - Initialiser et lancer l'application PyQt6.
  - Charger les modules pour le modèle (à partir de `ImageModel`), la vue (à partir de `FITSView`), et le contrôleur (à partir de `FITSController`).

#### Composants principaux :
- **`ImageModel`** : Gestion des fichiers et données FITS.
- **`FITSView`** : Interface utilisateur pour afficher et interagir avec les images FITS.
- **`FITSController`** : Contrôle les interactions entre la vue et le modèle.

---

### Fichier : `image_controleur.py`

#### Classe : `FITSController`
- **Rôle** :
  - Gérer les interactions utilisateur.
  - Contrôler les actions liées aux fichiers FITS et à leur affichage.

#### Méthodes principales :
- **`__init__`** :
  - Initialise le contrôleur avec le modèle et la vue.
  - Connecte les signaux entre les widgets de la vue et les méthodes du contrôleur.

- **`_connect_signals`** :
  - Lie les boutons de fichier, les curseurs et le bouton de téléchargement aux méthodes correspondantes.

- **`choose_file(idx)`** :
  - Ouvre une boîte de dialogue pour choisir un fichier FITS.
  - Met à jour l'étiquette de la vue et recharge l'image.

- **`update_coefficient(idx, value)`** :
  - Met à jour les coefficients RGB en fonction de la position du curseur.

- **`update_image`** :
  - Charge et affiche l'image combinée RGB si tous les fichiers sont prêts.

- **`download_data`** :
  - Gère le téléchargement des données FITS selon les entrées utilisateur.

---

### Fichier : `image_model.py`

#### Classe : `ImageModel`
- **Rôle** :
  - Gérer les fichiers FITS et leurs coefficients.
  - Fournir les données prêtes pour l'affichage.

#### Méthodes principales :

- **`__init__`** :
  - Initialise les chemins des fichiers et les coefficients RGB.

- **`set_file(idx, filepath)`** :
  - Enregistre le chemin d'un fichier FITS pour un canal RGB donné.

- **`set_coefficient(idx, value)`** :
  - Modifie le coefficient associé à un canal RGB.

- **`is_ready()`** :
  - Vérifie si les trois fichiers RGB sont prêts.

- **`reproduct(image1, image2, image3, data1, data2, data3)`** :
  - Gère la reprojection des données FITS si nécessaire.

- **`load_combined_image()`** :
  - Charge, normalise et combine les données des fichiers FITS pour créer une image RGB.

- **`_normalize(data)`** :
  - Normalise les données FITS en utilisant les percentiles 1 et 99.

- **`download(objet, telescope, radius, filters)`** :
  - Télécharge les fichiers FITS pour un objet et des filtres donnés.
  - Vérifie si les fichiers existent déjà avant de lancer un nouveau téléchargement.

- **`rename_and_replace(objet, telescope, radius, fichiers_fits)`** :
  - Renomme et déplace les fichiers téléchargés dans un répertoire structuré.

- **`verif_files_dl(objet, telescope, radius)`** :
  - Vérifie si les fichiers nécessaires ont déjà été téléchargés.

---

### Fichier : `Image_view.py`

#### Classe : `FITSView`
- **Rôle** :
  - Gérer l'interface utilisateur pour sélectionner les fichiers, ajuster les coefficients RGB et afficher les images FITS combinées.

#### Méthodes principales :
- **`__init__`** :
  - Initialise l'interface utilisateur avec des boutons, curseurs, et un canvas pour afficher les images.

- **`_setup_ui()`** :
  - Configure les éléments de l'interface :
    - Boutons pour sélectionner les fichiers FITS (rouge, vert, bleu).
    - Curseurs pour ajuster les coefficients RGB.
    - Canvas Matplotlib pour afficher les images.
    - Champs de saisie pour les informations d'objet, télescope, rayon et filtres.

- **`bind_file_button(idx, callback)`** :
  - Associe un bouton de sélection de fichier à une fonction de rappel.

- **`bind_slider(idx, callback)`** :
  - Associe un curseur à une fonction de rappel.

- **`update_file_label(idx, text)`** :
  - Met à jour l'étiquette affichant le chemin du fichier FITS sélectionné.

- **`update_slider_label(idx, value)`** :
  - Met à jour l'étiquette affichant la valeur du coefficient RGB correspondant.

- **`display_image(image)`** :
  - Affiche une image RGB combinée dans le canvas Matplotlib.

- **`show_status_message(message)`** :
  - Affiche un message d'état dans la barre de statut.

- **`download_data()`** :
  - Récupère les informations saisies par l'utilisateur et lance le téléchargement des fichiers FITS.
