from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class FITSView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualisation d'images FITS")
        self.setGeometry(100, 100, 800, 600)

        # Créer les widgets
        self.objet_label = QLabel("Nom de l'objet céleste:")
        self.objet_input = QLineEdit()

        self.telescope_label = QLabel("Nom du télescope:")
        self.telescope_input = QLineEdit()

        self.radius_label = QLabel("Rayon de recherche:")
        self.radius_input = QLineEdit()

        self.filters_label = QLabel("Filtres (séparés par des virgules):")
        self.filters_input = QLineEdit()

        self.image_label = QLabel("Aucune image à afficher.")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.load_button = QPushButton("Télécharger et afficher")

        # Agencement des widgets
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.objet_label)
        form_layout.addWidget(self.objet_input)
        form_layout.addWidget(self.telescope_label)
        form_layout.addWidget(self.telescope_input)
        form_layout.addWidget(self.radius_label)
        form_layout.addWidget(self.radius_input)
        form_layout.addWidget(self.filters_label)
        form_layout.addWidget(self.filters_input)
        form_layout.addWidget(self.load_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.image_label)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def afficher_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.width(), self.image_label.height(), Qt.AspectRatioMode.KeepAspectRatio
        ))

    def afficher_message(self, message):
        self.image_label.setText(message)