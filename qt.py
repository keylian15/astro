from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox

class FenetrePrincipale(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Exemple avec un bouton Ouvrir")
        self.setGeometry(100, 100, 300, 200)  # Position et taille de la fenêtre

        # Création du bouton
        self.bouton_ouvrir = QPushButton("Ouvrir", self)
        self.bouton_ouvrir.clicked.connect(self.ouvrir_fichier)  # Connecte le clic à la méthode

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.bouton_ouvrir)
        self.setLayout(layout)

    def ouvrir_fichier(self):
        # Boîte de dialogue pour ouvrir un fichier
        fichier, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Tous les fichiers (*)")
        
        if fichier:
            # Affiche une boîte de message avec le chemin du fichier sélectionné
            QMessageBox.information(self, "Fichier sélectionné", f"Vous avez sélectionné :\n{fichier}")

# Création de l'application
app = QApplication([])
fenetre = FenetrePrincipale()
fenetre.show()
app.exec()