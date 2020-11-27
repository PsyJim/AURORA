"""
This python file containg all the necessary methods
and libraries to display data cubes of IFS telescopes.
"""

#===========================
#     LIBRARIES
#===========================
from astropy.io import fits
from matplotlib import pyplot as plt



#===========================================================================
#                            METHODS
#===========================================================================

def read_cube(file):
    hdu = fits.open(file)
    data = hdu[0].data
    return data


#===========================
#     PROVING METHODS
#===========================

if __name__ == "__main__":
    read_cube('StarFieldForever.fits')