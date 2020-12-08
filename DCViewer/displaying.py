"""
This python file containg all the necessary methods
and libraries to display data cubes of IFS telescopes.

Copyright (C) 2020  Jim Acosta, Sebastián Carrazco
For conditions of distribution and use, see copyright notice in "notice"
"""

#===========================
#     LIBRARIES
#===========================
from astropy.io import fits
from astropy.visualization import ImageNormalize, MinMaxInterval
import numpy as np

#FOR COORDINATES PLOTING
from astropy.wcs import WCS
from astropy.utils.data import get_pkg_data_filename

import matplotlib
matplotlib.use('Agg') #This is the default non-interactive backend to render plots
from matplotlib import pyplot as plt
plt.style.use('dark_background')

#===========================================================================
#                            METHODS
#===========================================================================

def read_cube(file, wavelenght):
    #For MaNGa
    hdu = fits.open(file)
    data_flux = hdu[1].data
    data_flux_header = hdu[1].header
    return data_flux[wavelenght,:,:], data_flux_header


def plot_fits(data, scale_type, fitsheader):
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
    image = ax.imshow(data, norm=norm, origin='lower', cmap ='gist_rainbow')
    #--> Labels section
    fig.suptitle('MaNGA ID: '+str(fitsheader['MANGAID'])) 
    #fig.set_ylabel()
    #ax.set_ylabel(str(fitsheader['BUNIT']), rotation=270)
    ax.set_xlabel("pixels")
    ax.set_ylabel("pixels")    
    #ax.title()  
    bar = fig.colorbar(image) #Defining colorbar as bar  
    bar.set_label(str(fitsheader['BUNIT'])) #Label of colorbar
    """
    #--> Coordinates grid: https://docs.astropy.org/en/stable/visualization/wcsaxes/
    #hdu = fits.open(filename)[0]
    #wcs = WCS(hdu.header)

    wcs = WCS(fitsheader)
    ax2 = plt.subplot(projection=wcs)

    overlay = ax2.get_coords_overlay('fk5')
    overlay.grid(color='white', ls='dotted')
    overlay[0].set_axislabel('Right Ascension (J2000)')
    overlay[1].set_axislabel('Declination (J2000)')
    """
    return fig, ax


def integrate_flux(data, x1, x2, y1, y2):
    """
    Short function to calculate an approximate
    flux inside a rectangle due to integer coords.
    """
    #Simply integrating region with sum from numpy
    integrated_flux = np.sum(data[int(x1):int(x2),int(y1):int(y2)])
    print('Flux: %.2f' % integrated_flux)

    return integrated_flux


#===========================
#     PROVING METHODS
#===========================

if __name__ == "__main__":
    pass