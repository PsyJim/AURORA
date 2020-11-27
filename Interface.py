"""
This python file stores all the interface stuff for
DCViewer. We are using tkinter as our default interface
package.
"""

#===========================
#     LIBRARIES
#===========================
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #To add charts to tkinter window
from astropy.visualization import ImageNormalize, MinMaxInterval, LogStretch
import numpy as np

#Our methods for displaying data cubes
from Displaying import * 

#===========================
#     GLOBAL VARIABLES
#===========================
data = None

#===========================================================================
#                            METHODS
#===========================================================================


def open_file():
    """
    Function to allow program to open FITS files
    """
    #Input global variable
    global data

    filetypes = [('FITS files', '*.fits'), ('All files', '*.*')]
    
    #Here we're trying to open a FITS file
    file = filedialog.askopenfilename(title='Open', initialdir='', filetypes=filetypes)
    data = read_cube(file)
    show_fits(data)


def show_info(title, info):
    """
    Function to display a windows with info
    """
    messagebox.showinfo(title, info)


def show_error(error):
    """
    Function to show the errors on emergent windows
    """
    messagebox.showerror('Error', error)


def exit_program():
    """
    Function to ask to user if really want to close
    """
    valor = messagebox.askquestion('Exit', 'Are you really sure to exit?')
    
    if valor == 'yes':
        root.destroy()

    else:
        pass


#=================== THIS FUNCTION I GUESS WILL BE MOVED ===================
def show_fits(data):
    """
    Function to display data FITS with matplotlib
    """
    #Getting global variable

    try:
        #Creating a figure to display data
        fig = plt.figure(dpi=100)
        ax = fig.add_subplot(111)

        #Data display settings
        norm = ImageNormalize(data, interval=MinMaxInterval(), stretch=LogStretch())
        image = ax.imshow(data, norm=norm, origin='lower', cmap ='gray')
        fig.colorbar(image)
        fig.suptitle('FITS data')

        #Display figure with data in window
        add_figure = FigureCanvasTkAgg(fig, root)
        add_figure.get_tk_widget().pack(side=LEFT, fill=BOTH)
    
    except Exception as error:
        show_error(error)


#===========================================================================
#                            PUTTING TOGETHER
#===========================================================================

if __name__ == "__main__":

    #Creating the window and giving to it a title
    root = Tk()
    root.title('DCViewer')

    #Create a menu bar
    menu_bar = Menu(root)
    root.config(menu=menu_bar, width=300, height=300)

    #================================================
    #                DEFINING ITEMS FOR MENU BAR
    #================================================

    file = Menu(menu_bar, tearoff=0)
    file.add_command(label='Open', command=open_file)
    file.add_separator()
    file.add_command(label='Exit', command=exit_program)

    help = Menu(menu_bar, tearoff=0)
    help.add_command(label='Licency', command=lambda:show_info('Licency', 'This program has no licency yet'))
    help.add_command(label='About',command=lambda:show_info('About', 'DCViewer version: Cambriad period 0.1'))

    #Adding the times to menu bar
    menu_bar.add_cascade(label='File', menu=file)
    menu_bar.add_cascade(label='Help', menu=help)

    #=================== SEPARATOR ===================
    
    #Create a loop for executing the program
    root.mainloop()