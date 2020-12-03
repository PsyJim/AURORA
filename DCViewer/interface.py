"""
This python file stores all the interface stuff for
DCViewer. We are using tkinter as our default interface
package.

Copyright (C) 2020  Jim Acosta
For conditions of distribution and use, see copyright notice in "notice"
"""

#===========================
#     LIBRARIES
#===========================
from itertools import groupby
import tkinter as tk
import numpy as np

import os
import sys

#Something that will help
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import RectangleSelector
# Implement the default Matplotlib key bindings.
#from matplotlib.backend_bases import key_press_handler

from astropy.visualization import LogStretch, LinearStretch, SqrtStretch
import traceback #For tracing the errors

#Our methods for displaying data cubes
os.chdir(os.path.dirname(sys.argv[0])) #Changing the Python working directory
from displaying import *

#===========================
#     GLOBAL VARIABLES
#===========================
data = None
header = ''
scale_type = LogStretch()

#FITS coords
x1 = 0
x2 = 0
y1 = 0
y2 = 0


#===========================================================================
#                            METHODS
#===========================================================================


def open_file():
    """
    Function to allow program to open FITS files
    """
    #Input global variables
    global data, header

    #Defining filetypes to appear on window asking to open files
    filetypes = [('FITS files', ('*.fits', '*.gz')), ('All files', '*.*')]
    
    #Here we're trying to open a FITS file
    file = tk.filedialog.askopenfilename(title='Open', initialdir='../', filetypes=filetypes)
    
    #Selecting the data cube wavelenght to display
    wavelenght = tk.simpledialog.askinteger('Wavelenght', 'Type the wavelenght you want')
    data, header = read_cube(file, wavelenght)
    show_fits(data)

    return file


#def show_info(title, info):
#    """
#    Function to display a windows with info
#    """
#    #Show a window with some info
#    tk.messagebox.showinfo(title, info)


def show_error(error):
    """
    Function to show the errors on emergent windows
    """
    #Show a window with the specific error
    tk.messagebox.showerror('Error', error)


def exit_program():
    """
    Function to ask to user if really want to close
    """
    value = tk.messagebox.askquestion('Exit', 'Are you really sure to exit?')
    
    if value == 'yes':
        #Close the root, so program close too.
        root.destroy()
    else:
        pass


#=================== THIS FUNCTIONS I GUESS WILL BE MOVED ===================

def show_fits(data):
    """
    Function to display data FITS with matplotlib
    """
    #Input global variable
    global scale_type

    #Erasing all the stuff for the principal frame
    for widget in frame.winfo_children():
        widget.destroy()

    #Handling errors with try sentence
    try:
        #Creating the data cube figure
        fig, ax = plot_fits(data, scale_type)

        #Display figure with data in window
        add_figure = FigureCanvasTkAgg(fig, frame)
        #add_figure.draw()

        #Toolbar from matplotlib to interact with figure
        toolbar = NavigationToolbar2Tk(add_figure, frame)
        toolbar.update()

        #To draw a rectangle on the data cube image
        toggle_selector.RS = RectangleSelector(ax, line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
        add_figure.mpl_connect('key_press_event', toggle_selector) #Connect 

        #Add the figure as a widget to the window
        add_figure.get_tk_widget().pack(expand=tk.YES, fill=tk.BOTH)
        
    except:
        #Show an error windows with the complete problem
        show_error(traceback.format_exc())


"""def show_header(header):
    
    #Function to show a window with the data header
    
    #Input global variable
    #global header

    window = tk.Tk()
    window.title('Header')

    #Adding a scrollbar to window
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #Allocate text in the window
    text = tk.Text(window, text=header) #,font=('Courier New', 12, BOLD))
    text.pack()

    #Allocate button to the bottom of window
    ok_button = tk.Button(window, text='Ok', command=window.destroy)
    ok_button.pack()

    #Window loop
    window.mainloop()"""


def change_scale(scale):
    """
    Function that change the scale for data
    and re-display the image
    """
    #Input global variables
    global data, scale_type

    #Conditional to change the type of scale
    if scale == 'Linear':
        scale_type = LinearStretch()
    elif scale == 'Log':
        scale_type = LogStretch()
    else:
        scale_type = SqrtStretch() 

    #Re-display data
    show_fits(data)


"""def change_wavelenght():
    
    #Function to display a scrollbar that will
    #change the wavelenght of the data cube
    
    scrollbar = Scrollbar(frame)"""


def text_window(title, info, type):
    """
    Function to display another tkinter window.
    """
    #Initilizing another tkinter window and grouping to main program
    window = tk.Toplevel(root)
    window.group(root)
    window.title(title)

    #Enable widgets resizing for new window
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    #Checking the type of window you like
    if type == 'header':
        
        #Creating Text widget and insert text to it
        text = tk.Text(window, padx=5, pady=5) #,font=('Courier New', 12, BOLD))
        text.insert(tk.INSERT, info)
        text.configure(state="disabled", relief="flat", wrap='word')
        text.grid(row=0, column=0, sticky='nswe')

        #Adding a scrollbar o the text
        scrollbar = tk.Scrollbar(window)
        scrollbar.grid(row=0, column=1, sticky='nswe')
        scrollbar.config(command = text.yview)
        text.config(yscrollcommand=scrollbar.set)

    else:

        #Allocate text in the window
        text = tk.Label(window, text=info, padx=5, pady=5) #,font=('Courier New', 12, BOLD))
        text.grid(row=0, column=0, sticky='nswe')


    #Allocate button to the bottom of window
    ok_button = tk.Button(window, text='Ok', command=window.destroy)
    ok_button.grid(row=1, column=0)

    #Window loop
    window.mainloop()


def integrate_flux(data, x1, x2, y1, y2):
    """
    Short function to calculate an approximate
    flux inside a rectangle due to integer coords.
    """
    #Simply integrating region with sum from numpy
    integrated_flux = np.sum(data[int(x1):int(x2),int(y1):int(y2)])
    print('Flux: %.2f' % integrated_flux)

    return integrated_flux



#================================= FUNCTIONS TO REVIEW ================================

def line_select_callback(eclick, erelease):
    """
    eclick and erelease are the press and release events
    """
    global x1, x2, y1, y2

    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    print("Coords: (%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    #print(" The button you used were: %s %s" % (eclick.button, erelease.button))

    #Print the integrated flux within coordinates
    integrate_flux(data, x1, x2, y1, y2)

    return x1, x2, y1, y2


def toggle_selector(event):
    """
    If you press q key on keyboard, you deactivated this
    function and pressing a key activated again. 
    Apparently, pressing esc key will remove the box.
    """
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)


#===========================================================================
#                            PUTTING TOGETHER
#===========================================================================

if __name__ == "__main__":

    #Creating the window and giving to it a title
    root = tk.Tk()
    root.title('DCViewer')

    #Create a menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar, bg='lightblue', relief='sunken', bd='10')
    root.geometry('600x600')

    #Creating the principal frame for images
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky='nswe')
    frame.config(bg='pink')
    

    #Adding an image to initial frame (the image isn't showing up, I don't know why)
    initial_image = tk.PhotoImage(file='../Logo_DCViewer.gif')
    tk.Label(frame, image=initial_image, bg='pink').grid(row=0, column=0, sticky='nswe')
    tk.Label(frame, text='DCViewer', bg='pink', font=('Times New Roman', 24)).grid(row=1, column=0, sticky='nswe')

    #Configuring columns and rows to enable widgets resizing
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    #Add an icon to the window
    #root.call('wm', 'iconphoto', root._w, PhotoImage(file='galaxy.gif'))

    #================================================
    #                DEFINING ITEMS FOR MENU BAR
    #================================================

    #File options on the menu bar
    file = tk.Menu(menu_bar, tearoff=0)
    file.add_command(label='Open FITS file', command=open_file)
    file.add_command(label='Display Header', command=lambda:text_window('Header', header, type='header'))
    file.add_separator()
    file.add_command(label='Exit', command=exit_program)

    #Tools options on the menubar
    tools = tk.Menu(menu_bar, tearoff=0)

    #Scale and sub-options in Tools
    scale = tk.Menu(tools, tearoff=0)
    scale.add_command(label="Linear scale", command=lambda:change_scale('Linear'))
    scale.add_command(label="Log scale", command=lambda:change_scale('Log'))
    scale.add_command(label="Sqrt scale", command=lambda:change_scale('Sqrt'))
    tools.add_cascade(label='Scale', menu=scale)

    #Help options on menu bar
    help = tk.Menu(menu_bar, tearoff=0)
    help.add_command(label='License', command=lambda:text_window('License', open('../LICENSE', 'r').read(), type='text'))
    help.add_command(label='About',command=lambda:text_window('About', 'DCViewer version 0.2: Ordovician period', type='text'))

    #Adding the options to menu bar
    menu_bar.add_cascade(label='File', menu=file)
    menu_bar.add_cascade(label='Tools', menu=tools)
    menu_bar.add_cascade(label='Help', menu=help)

    #=================== INIT MAINLOOP ===================
    
    #Create a loop for executing the program
    root.mainloop()