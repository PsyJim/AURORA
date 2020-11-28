"""
This python file containg all the necessary methods
and libraries to display data cubes of IFS telescopes.
"""

#===========================
#     LIBRARIES
#===========================
from astropy.io import fits
from astropy.visualization import ImageNormalize, MinMaxInterval
from matplotlib import pyplot as plt


#===========================================================================
#                            METHODS
#===========================================================================

def read_cube(file, wavelenght):
    #For MaNGa
    hdu = fits.open(file)
    data_flux = hdu[1].data
    data_flux_header = hdu[1].header
    return data_flux[wavelenght,:,:], data_flux_header

def plot_fits(data, scale_type):
    """
    Function to display data FITS with matplotlib
    """
    #Clear actual figure if exist one
    #clf()

    #Creating a figure to display data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    #Data display settings
    norm = ImageNormalize(data, interval=MinMaxInterval(), stretch=scale_type)
    image = ax.imshow(data, norm=norm, origin='lower', cmap ='gray')
    fig.colorbar(image)
    fig.suptitle('FITS data cube')

    return fig, ax


#===========================
#     PROVING METHODS
#===========================

if __name__ == "__main__":
    read_cube('StarFieldForever.fits')