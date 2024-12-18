from astropy.io import fits
import numpy as np

class ImageModel:
    def __init__(self):
        self.files = [None, None, None]
        self.coefficients = [1.0, 1.0, 1.0]

    def set_file(self, idx, filepath):
        self.files[idx] = filepath

    def set_coefficient(self, idx, value):
        self.coefficients[idx] = value

    def is_ready(self):
        return None not in self.files

    def load_combined_image(self):
        if not self.is_ready():
            return None
        data1 = self.extraire_image(self.files[0])
        data2 = self.extraire_image(self.files[1])
        data3 = self.extraire_image(self.files[2])

        red = self._normalize(data1) * self.coefficients[0]
        green = self._normalize(data2) * self.coefficients[1]
        blue = self._normalize(data3) * self.coefficients[2]

        image = np.stack([np.clip(red, 0, 1), np.clip(green, 0, 1), np.clip(blue, 0, 1)], axis=-1)
        return image
    
    def extraire_image(self,fichier_fits):
        """
        Fonction qui parcourt un fichier FITS et retourne les données de la première extension ImageHDU
        contenant des données (si plusieurs extensions sont présentes).
        """
        with fits.open(fichier_fits) as hdul:
            if len(hdul) == 1 : 
                return fits.getdata(fichier_fits)
            
            # Parcours des extensions à partir de l'index 1 (ignorer le Primary HDU à l'index 0)
            for i in range(1, len(hdul)):
                hdu = hdul[i]
                if isinstance(hdu, fits.ImageHDU) and hdu.data is not None:
                    return hdu.data  # Retourne les données de la première extension valide trouvée
        
        return None

    @staticmethod
    def _normalize(data):
        vmin, vmax = np.percentile(data, (1, 99))
        return np.clip((data - vmin) / (vmax - vmin), 0, 1)
