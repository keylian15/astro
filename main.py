from astropy.io import fits 
import matplotlib.pyplot as plt 

data = fits.getdata('./Tarantula_Nebula-halpha.fit')

plt.imshow(data, cmap= 'gray')
plt.colorbar()
plt.show()