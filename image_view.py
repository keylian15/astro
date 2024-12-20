from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QSlider, QFileDialog, 
    QHBoxLayout, QGroupBox, QGridLayout, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FITSView(QMainWindow):
    slider_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualisation d'images FITS")
        self.resize(800, 600)

        self.file_labels = [QLabel("Fichier FITS Rouge: Non sélectionné"),
                            QLabel("Fichier FITS Vert: Non sélectionné"),
                            QLabel("Fichier FITS Bleu: Non sélectionné")]
        self.sliders = []
        self.slider_labels = []
        self.canvas = None
        self.figure = None
        self.ax = None
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout()

        # Fichier selection
        self.file_buttons = [QPushButton("Choisir Rouge"), QPushButton("Choisir Vert"), QPushButton("Choisir Bleu")]
        file_layout = QVBoxLayout()
        for i in range(3):
            row = QHBoxLayout()
            row.addWidget(self.file_labels[i])
            row.addWidget(self.file_buttons[i])
            file_layout.addLayout(row)
        main_layout.addLayout(file_layout)

        # Sliders
        sliders_layout = QGroupBox("Ajustement des coefficients RGB")
        sliders_layout.setLayout(QGridLayout())
        colors = ["Red", "Green", "Blue"]

        for i, color in enumerate(colors):
            label = QLabel(f"{color}: 1.0")
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(1)
            slider.setMaximum(300)
            slider.setValue(100)
            slider.valueChanged.connect(self.slider_changed.emit)
            self.sliders.append(slider)
            self.slider_labels.append(label)
            sliders_layout.layout().addWidget(QLabel(f"{color}"), i, 0)
            sliders_layout.layout().addWidget(slider, i, 1)
            sliders_layout.layout().addWidget(label, i, 2)

        main_layout.addWidget(sliders_layout)

        # Canvas Matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Champs de saisie pour les informations supplémentaires
        self.objet_input = QLineEdit(self)
        self.objet_input.setText("NGC 6362")  # Valeur par défaut pour l'objet

        self.telescope_input = QLineEdit(self)
        self.telescope_input.setText("HST")  # Valeur par défaut pour le télescope

        self.radius_input = QLineEdit(self)
        self.radius_input.setText("0.005 deg")  # Valeur par défaut pour le rayon

        self.filter_input = QLineEdit(self)
        self.filter_input.setText("F814W,F658N,F336W")  # Valeurs par défaut des filtres

        self.download_button = QPushButton("Télécharger les Images FITS")
        self.download_button.clicked.connect(self.download_data)

        # Layout pour télécharger les données
        download_layout = QVBoxLayout()
        download_layout.addWidget(QLabel("Objet:"))
        download_layout.addWidget(self.objet_input)
        download_layout.addWidget(QLabel("Télescope:"))
        download_layout.addWidget(self.telescope_input)
        download_layout.addWidget(QLabel("Rayon:"))
        download_layout.addWidget(self.radius_input)
        download_layout.addWidget(QLabel("Filtres (séparés par des virgules):"))
        download_layout.addWidget(self.filter_input)
        download_layout.addWidget(self.download_button)
        main_layout.addLayout(download_layout)

        # Layout central
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def bind_file_button(self, idx, callback):
        self.file_buttons[idx].clicked.connect(callback)

    def bind_slider(self, idx, callback):
        self.sliders[idx].valueChanged.connect(callback)

    def update_file_label(self, idx, text):
        self.file_labels[idx].setText(text)

    def update_slider_label(self, idx, value):
        self.slider_labels[idx].setText(f"{['Red', 'Green', 'Blue'][idx]}: {value:.2f}")

    def display_image(self, image):
        self.ax.clear()
        self.ax.imshow(image, origin='lower')
        self.ax.set_title("Image Combinée FITS")
        self.canvas.draw()

    def show_status_message(self, message):
        self.statusBar().showMessage(message)

    def download_data(self):
        """
        Récupère les informations saisies par l'utilisateur et lance le téléchargement des images.
        """
        objet = self.objet_input.text()
        telescope = self.telescope_input.text()
        radius = self.radius_input.text()
        filters = self.filter_input.text().split(',')
        
        if objet and telescope and radius and filters:
            self.download_button.setEnabled(False)  # Désactiver le bouton pendant le téléchargement
            self.slider_changed.emit()  # Indiquer un changement de données (optionnel)
            self.download_button.setEnabled(True)  # Réactiver le bouton après le téléchargement
        else:
            self.show_status_message("Veuillez remplir tous les champs.")
