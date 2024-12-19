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
        data1 = fits.getdata(self.files[0])
        data2 = fits.getdata(self.files[1])
        data3 = fits.getdata(self.files[2])

        red = self._normalize(data1) * self.coefficients[0]
        green = self._normalize(data2) * self.coefficients[1]
        blue = self._normalize(data3) * self.coefficients[2]

        image = np.stack([np.clip(red, 0, 1), np.clip(green, 0, 1), np.clip(blue, 0, 1)], axis=-1)
        return image

    @staticmethod
    def _normalize(data):
        vmin, vmax = np.percentile(data, (1, 99))
        return np.clip((data - vmin) / (vmax - vmin), 0, 1)