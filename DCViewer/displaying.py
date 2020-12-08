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
from astropy.visualization.stretch import LogStretch, SqrtStretch, LinearStretch
import numpy as np
import tkinter as tk

# FOR COORDINATES PLOTING
from astropy.wcs import WCS
from astropy.utils.data import get_pkg_data_filename

import matplotlib
matplotlib.use('Agg') #This is the default non-interactive backend to render plots
from matplotlib import pyplot as plt
plt.style.use('dark_background')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import RectangleSelector, EllipseSelector

import variables as var


#===========================================================================
#                            METHODS
#===========================================================================

def read_cube(file, wavelenght):
    """
    Read a data cube and header with astropy
    """
    
    # For MaNGa
    hdu = fits.open(file)
    data = hdu[1].data
    header = hdu[1].header

    return data[wavelenght,:,:], header


def plot_fits(data, header, scale, colormap):
    """
    Function to display data FITS with matplotlib
    """
    # Clear actual figure if exist one
    #clf()

    # Creating a figure to display data
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Data display settings
    norm = ImageNormalize(data, interval=MinMaxInterval(), stretch=scale)
    image = ax.imshow(data, norm=norm, origin='lower', cmap=colormap)
    #--> Labels section
    fig.suptitle('MaNGA ID: '+str(header['MANGAID'])) 
    #fig.set_ylabel()
    #ax.set_ylabel(str(fitsheader['BUNIT']), rotation=270)
    ax.set_xlabel("pixels")
    ax.set_ylabel("pixels")    
    #ax.title()  
    bar = fig.colorbar(image) #Defining colorbar as bar  
    bar.set_label(str(header['BUNIT'])) #Label of colorbar
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


def show_fits(data, header, frame, scale=LogStretch(), colormap='viridis'):
    """
    Function to display data FITS with matplotlib
    """
    # Erasing all the stuff for the principal frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Handling errors with try sentence
    try:
        # Creating the data cube figure
        fig, ax = plot_fits(data, header, scale, colormap)

        # Display figure with data in window
        add_figure = FigureCanvasTkAgg(fig, frame)
        #add_figure.draw()

        # Toolbar from matplotlib to interact with figure
        toolbar = NavigationToolbar2Tk(add_figure, frame)
        toolbar.update()

        # To draw a rectangle on the data cube image
        toggle_selector.RS = RectangleSelector(
            ax, line_select_callback,
            drawtype='box', useblit=True,
            button=[1, 3],  # don't use middle button
            minspanx=5, minspany=5,
            spancoords='pixels',
            interactive=True
        )
        add_figure.mpl_connect('key_press_event', toggle_selector) #Connect 

        # Add the figure as a widget to the window
        add_figure.get_tk_widget().pack(expand=tk.YES, fill=tk.BOTH)
        
    except:
        # Show an error windows with the complete problem
        #show_error(traceback.format_exc())
        pass


def integrate_flux(x1, x2, y1, y2):
    """
    Short function to calculate an approximate
    flux inside a rectangle due to integer coords.
    """

    # Simply integrating region with sum from numpy
    integrated_flux = np.sum(var.data[int(x1):int(x2),int(y1):int(y2)])
    print('Flux: %.2f' % integrated_flux)

    return integrated_flux


#===========================================================================
#          METHODS FOR DRAW RECTANGLES AND ELLIPSES IN DISPLAYED FITS
#===========================================================================
def line_select_callback(eclick, erelease):
    """
    eclick and erelease are the press and release events
    """

    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print("Coords: (%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    #print(" The button you used were: %s %s" % (eclick.button, erelease.button))

    # Print the integrated flux within coordinates
    integrate_flux(x1, x2, y1, y2)

    return x1, x2, y1, y2


def toggle_selector(event):
    """
    If you press q key on keyboard, you deactivated this
    function and pressing a key activated again. 
    Pressing esc key will remove the box.
    """
    print(' Key pressed.')
   
    # Conditionals for Rectangle selector
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)

    # Conditionals for Ellipse selector
    if event.key in ['Q', 'q'] and toggle_selector.ES.active:
        print('EllipseSelector deactivated.')
        toggle_selector.RS.set_active(False)
    
    if event.key in ['A', 'a'] and not toggle_selector.ES.active:
        print('EllipseSelector activated.')
        toggle_selector.ES.set_active(True)


def onselect(eclick, erelease):
    """
    eclick and erelease are matplotlib 
    events at press and release.
    """
    print('startposition: (%f, %f)' % (eclick.xdata, eclick.ydata))
    print('endposition  : (%f, %f)' % (erelease.xdata, erelease.ydata))
    print('used button  : ', eclick.button)


#===========================
#     END OF FILE
#===========================
if __name__ == "__main__":
    pass