from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QSlider,
    QLabel,
)
from PyQt6.QtCore import Qt

class FenetrePrincipale(QWidget):
    
    typeCmap = [
    "Accent",
    "Accent_r",
    "Blues",
    "Blues_r",
    "BrBG",
    "BrBG_r",
    "BuGn",
    "BuGn_r",
    "BuPu",
    "BuPu_r",
    "CMRmap",
    "CMRmap_r",
    "Dark2",
    "Dark2_r",
    "GnBu",
    "GnBu_r",
    "Grays",
    "Greens",
    "Greens_r",
    "Greys",
    "Greys_r",
    "OrRd",
    "OrRd_r",
    "Oranges",
    "Oranges_r",
    "PRGn",
    "PRGn_r",
    "Paired",
    "Paired_r",
    "Pastel1",
    "Pastel1_r",
    "Pastel2",
    "Pastel2_r",
    "PiYG",
    "PiYG_r",
    "PuBu",
    "PuBuGn",
    "PuBuGn_r",
    "PuBu_r",
    "PuOr",
    "PuOr_r",
    "PuRd",
    "PuRd_r",
    "Purples",
    "Purples_r",
    "RdBu",
    "RdBu_r",
    "RdGy",
    "RdGy_r",
    "RdPu",
    "RdPu_r",
    "RdYlBu",
    "RdYlBu_r",
    "RdYlGn",
    "RdYlGn_r",
    "Reds",
    "Reds_r",
    "Set1",
    "Set1_r",
    "Set2",
    "Set2_r",
    "Set3",
    "Set3_r",
    "Spectral",
    "Spectral_r",
    "Wistia",
    "Wistia_r",
    "YlGn",
    "YlGnBu",
    "YlGnBu_r",
    "YlGn_r",
    "YlOrBr",
    "YlOrBr_r",
    "YlOrRd",
    "YlOrRd_r",
    "afmhot",
    "afmhot_r",
    "autumn",
    "autumn_r",
    "binary",
    "binary_r",
    "bone",
    "bone_r",
    "brg",
    "brg_r",
    "bwr",
    "bwr_r",
    "cividis",
    "cividis_r",
    "cool",
    "cool_r",
    "coolwarm",
    "coolwarm_r",
    "copper",
    "copper_r",
    "cubehelix",
    "cubehelix_r",
    "flag",
    "flag_r",
    "gist_earth",
    "gist_earth_r",
    "gist_gray",
    "gist_gray_r",
    "gist_grey",
    "gist_heat",
    "gist_heat_r",
    "gist_ncar",
    "gist_ncar_r",
    "gist_rainbow",
    "gist_rainbow_r",
    "gist_stern",
    "gist_stern_r",
    "gist_yarg",
    "gist_yarg_r",
    "gist_yerg",
    "gnuplot",
    "gnuplot2",
    "gnuplot2_r",
    "gnuplot_r",
    "gray",
    "gray_r",
    "grey",
    "hot",
    "hot_r",
    "hsv",
    "hsv_r",
    "inferno",
    "inferno_r",
    "jet",
    "jet_r",
    "magma",
    "magma_r",
    "nipy_spectral",
    "nipy_spectral_r",
    "ocean",
    "ocean_r",
    "pink",
    "pink_r",
    "plasma",
    "plasma_r",
    "prism",
    "prism_r",
    "rainbow",
    "rainbow_r",
    "seismic",
    "seismic_r",
    "spring",
    "spring_r",
    "summer",
    "summer_r",
    "tab10",
    "tab10_r",
    "tab20",
    "tab20_r",
    "tab20b",
    "tab20b_r",
    "tab20c",
    "tab20c_r",
    "terrain",
    "terrain_r",
    "turbo",
    "turbo_r",
    "twilight",
    "twilight_r",
    "twilight_shifted",
    "twilight_shifted_r",
    "viridis",
    "viridis_r",
    "winter",
    "winter_r",
]

    def __init__(self):
        super().__init__()

        # ====== Fenetre Principale ======
        self.setWindowTitle("Sae")
        self.setGeometry(100, 100, 300, 200)  
        # ====== Fin Fenetre Principale ======
        
        # ====== Layout ======
        self.layoutPrincipal = QVBoxLayout()
        self.layoutFiltre = QVBoxLayout()
        
        self.setLayout(self.layoutPrincipal)
        self.layoutPrincipal.addLayout(self.layoutFiltre)
        # ====== Fin Layout ======
        
        # ====== Label Filtre ======
        self.labelFiltre = QLabel("Le type de filtre")
        self.labelFiltre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutFiltre.addWidget(self.labelFiltre)
        # ====== Fin Label Filtre ======
        
        # ====== Slider Type ======
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(0,169)
        self.layoutFiltre.addWidget(self.slider)
        # ====== Fin Slider Type ======

        # ====== Bouton Ouvrir ======
        self.bouton_ouvrir = QPushButton("Ouvrir", self)
        self.bouton_ouvrir.clicked.connect(
            self.ouvrir_fichier
        )  
        
        self.layoutPrincipal.addWidget(self.bouton_ouvrir)
        # ====== Fin Bouton Ouvrir ======
        
        
        
        # ====== Signeaux ======
        self.slider.valueChanged.connect(self.updateFilterValue)
        # ====== Fin Signeaux ======
        
        
    def ouvrir_fichier(self):
        fichier, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier", "", "Tous les fichiers (*)"
        )

        if fichier:
            return True

    def updateFilterValue(self):
        self.labelFiltre.setText(f"Le filtre : {self.typeCmap[self.slider.value()]}")

# Création de l'application
app = QApplication([])
fenetre = FenetrePrincipale()
fenetre.show()
app.exec()
