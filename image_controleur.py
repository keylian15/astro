from PyQt6.QtWidgets import QFileDialog

class FITSController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._connect_signals()

    def _connect_signals(self):
        for i in range(3):
            self.view.bind_file_button(i, lambda checked, idx=i: self.choose_file(idx))
            self.view.bind_slider(i, lambda value, idx=i: self.update_coefficient(idx, value))
        self.view.slider_changed.connect(self.update_image)
        self.view.download_button.clicked.connect(self.download_data)  # Connecter le bouton de téléchargement

    def choose_file(self, idx):
        fichier, _ = QFileDialog.getOpenFileName(self.view, "Choisir un fichier FITS", "", "FITS Files (*.fits *.fit)")
        if fichier:
            self.model.set_file(idx, fichier)
            couleurs = ["Rouge", "Vert", "Bleu"]
            self.view.update_file_label(idx, f"Fichier FITS {couleurs[idx]}: {fichier}")
            self.update_image()

    def update_coefficient(self, idx, value):
        coef = value / 100
        self.model.set_coefficient(idx, coef)
        self.view.update_slider_label(idx, coef)

    def update_image(self):
        if not self.model.is_ready():
            self.view.show_status_message("Veuillez choisir trois fichiers FITS pour RGB.")
            return
        image = self.model.load_combined_image()
        if image is not None:
            self.view.display_image(image)
        else:
            self.view.show_status_message("Erreur lors du chargement de l'image.")

    def download_data(self):
        """
        Gère le téléchargement des données en fonction des informations saisies dans la vue.
        """
        objet = self.view.objet_input.text()
        telescope = self.view.telescope_input.text()
        radius = self.view.radius_input.text()
        filters = self.view.filter_input.text().split(',')
        
        fichiers, erreurs = self.model.download(objet, telescope, radius, filters)
        
        if erreurs:
            self.view.show_status_message("\n".join(erreurs))
        else:
            self.view.show_status_message("Téléchargement terminé!")
            # Afficher les fichiers téléchargés ou actualiser la vue en conséquence
