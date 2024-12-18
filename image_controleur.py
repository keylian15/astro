import sys
from PyQt6.QtWidgets import QApplication
from image_model import FITSModel
from image_view import FITSView
import os

class FITSController:
    def __init__(self):
        self.model = FITSModel()
        self.view = FITSView()

        # Connecter les signaux et les slots
        self.view.load_button.clicked.connect(self.handle_load_button)

        self.view.show()

    def handle_load_button(self):
        # Récupérer les données de la vue
        objet = self.view.objet_input.text()
        telescope = self.view.telescope_input.text()
        radius = self.view.radius_input.text()
        filtres = [f.strip() for f in self.view.filters_input.text().split(',')]

        if not (objet and telescope and radius and filtres):
            self.view.afficher_message("Tous les champs doivent être remplis.")
            return

        self.view.afficher_message("Téléchargement en cours...")
        fichiers_fits, errors = self.model.download(objet, telescope, radius, filtres)

        if errors:
            self.view.afficher_message("\n".join(errors))
        elif fichiers_fits:
            self.view.afficher_message("Affichage de l'image combinée...")
            try:
                image_path = self.creer_image_combinee(fichiers_fits)
                self.view.afficher_image(image_path)
            except Exception as e:
                self.view.afficher_message(f"Erreur lors de la création de l'image : {e}")

    def creer_image_combinee(self, fichiers):
        import matplotlib.pyplot as plt
        import numpy as np

        data_r = self.model.extraire_image(fichiers[0])
        data_g = self.model.extraire_image(fichiers[1])
        data_b = self.model.extraire_image(fichiers[2])

        min_height = min(data_r.shape[0], data_g.shape[0], data_b.shape[0])
        min_width = min(data_r.shape[1], data_g.shape[1], data_b.shape[1])

        data_r = self.model.normaliser(data_r[:min_height, :min_width])
        data_g = self.model.normaliser(data_g[:min_height, :min_width])
        data_b = self.model.normaliser(data_b[:min_height, :min_width])

        image = np.stack([data_r, data_g, data_b], axis=-1)

        output_path = os.path.join(self.model.download_dir, "image_combined.png")
        plt.imsave(output_path, image)
        return output_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = FITSController()
    sys.exit(app.exec())