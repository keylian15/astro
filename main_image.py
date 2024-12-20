import sys
from PyQt6.QtWidgets import QApplication
from image_model import ImageModel
from image_view import FITSView
from image_controleur import FITSController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = ImageModel()
    view = FITSView()
    controller = FITSController(model, view)
    view.show()
    sys.exit(app.exec())
