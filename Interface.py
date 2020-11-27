"""
This python file stores all the interface stuff for
DCViewer. We are using tkinter as our default interface
package.

Iconos diseñados por <a href="https://www.flaticon.es/autores/dinosoftlabs" title="DinosoftLabs">DinosoftLabs</a> from <a href="https://www.flaticon.es/" title="Flaticon"> www.flaticon.es</a>
"""

#===========================
#     LIBRARIES
#===========================
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#from matplotlib.backend_bases import key_press_handler # Implement the default Matplotlib key bindings.
#from matplotlib import pyplot as plt

from astropy.visualization import LogStretch, LinearStretch, SqrtStretch
import traceback

#Our methods for displaying data cubes
from Displaying import * 

#===========================
#     GLOBAL VARIABLES
#===========================
data = None
header = None
scale_type = LogStretch()
add_figure = None

#===========================================================================
#                            METHODS
#===========================================================================


def open_file():
    """
    Function to allow program to open FITS files
    """
    #Input global variables
    global data
    global header

    #Defining filetypes to appear on window asking to open files
    filetypes = [('FITS files', ('*.fits', '*.gz')), ('All files', '*.*')]
    
    #Here we're trying to open a FITS file
    file = filedialog.askopenfilename(title='Open', initialdir='', filetypes=filetypes)
    
    #Selecting the data cube wavelenght to display
    wavelenght = simpledialog.askinteger('Wavelenght', 'Type the wavelenght you want')
    data, header = read_cube(file, wavelenght)
    show_fits(data)

    return file


def show_info(title, info):
    """
    Function to display a windows with info
    """
    #Show a window with some info
    messagebox.showinfo(title, info)


def show_error(error):
    """
    Function to show the errors on emergent windows
    """
    #Show a window with the specific error
    messagebox.showerror('Error', error)


def exit_program():
    """
    Function to ask to user if really want to close
    """
    value = messagebox.askquestion('Exit', 'Are you really sure to exit?')
    
    if value == 'yes':
        #Close the root, so program close too.
        root.destroy()
    else:
        pass


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
        fig = plot_fits(data, scale_type)

        #Display figure with data in window
        add_figure = FigureCanvasTkAgg(fig, frame)
        #add_figure.draw()

        #Toolbar from matplotlib to interact with figure
        toolbar = NavigationToolbar2Tk(add_figure, frame)
        #toolbar.update()

        #Add the figure as a widget to the window
        add_figure.get_tk_widget().pack()
        
    
    except:
        #Show an error windows with the complete problem
        show_error(traceback.format_exc())


def show_header():
    """
    Function to show a window with the data header
    """
    #Input global variable
    global header

    #Showing header
    messagebox.showinfo('Header', header)


def change_scale(scale):
    """
    Function that change the scale for data
    and re-display the image
    """
    #Input global variables
    global data
    global scale_type

    #Get the scale variable
    scale = scale

    #Conditional to change the type of scale
    if scale == 'Linear':
        scale_type = LinearStretch()
    elif scale == 'Log':
        scale_type = LogStretch()
    else:
        scale_type = SqrtStretch() 

    #Re-display data
    show_fits(data)


#===========================================================================
#                            PUTTING TOGETHER
#===========================================================================

if __name__ == "__main__":

    #Creating the window and giving to it a title
    root = Tk()
    root.title('DCViewer')

    #Create a menu bar
    menu_bar = Menu(root)
    root.config(menu=menu_bar, bg='lightblue', relief='sunken', bd='10')

    #Creating the principal frame for images
    frame = Frame(root)
    frame.pack()
    #frame.config(bg='pink')

    #Adding an image to initial frame (the image isn't showing up, I don't know why)
    initial_image = PhotoImage(file='radar.gif')
    Label(frame, image=initial_image).pack()
    Label(frame, text='DCViewer', font=('Times New Roman', 24)).pack()

    #Add an icon to the window
    #root.call('wm', 'iconphoto', root._w, PhotoImage(file='galaxy.gif'))

    #================================================
    #                DEFINING ITEMS FOR MENU BAR
    #================================================

    #File options on the menu bar
    file = Menu(menu_bar, tearoff=0)
    file.add_command(label='Open FITS file', command=open_file)
    file.add_command(label='Display Header', command=show_header)
    file.add_separator()
    file.add_command(label='Exit', command=exit_program)

    #Tools options on the menubar
    tools = Menu(menu_bar, tearoff=0)

    #Sub options in Tools
    scale = Menu(tools, tearoff=0)
    scale.add_command(label="Linear scale", command=lambda:change_scale('Linear'))
    scale.add_command(label="Log scale", command=lambda:change_scale('Log'))
    scale.add_command(label="Sqrt scale", command=lambda:change_scale('Sqrt'))
    tools.add_cascade(label='Scale', menu=scale)

    #Help options on menu bar
    help = Menu(menu_bar, tearoff=0)
    help.add_command(label='Licency', command=lambda:show_info('Licency', 'This program has no licency yet'))
    help.add_command(label='About',command=lambda:show_info('About', 'DCViewer version: Cambriad period 0.1'))

    #Adding the options to menu bar
    menu_bar.add_cascade(label='File', menu=file)
    menu_bar.add_cascade(label='Tools', menu=tools)
    menu_bar.add_cascade(label='Help', menu=help)

    #=================== SEPARATOR ===================
    
    #Create a loop for executing the program
    root.mainloop()