"""
This python file stores all the interface stuff for
DCViewer. We are using tkinter as our default interface
package.

Copyright (C) 2020  Jim Acosta, Sebastián Carrazco
For conditions of distribution and use, see copyright notice in "notice"
"""
#===========================
#     LIBRARIES
#===========================
import os
# Changing the Python working directory to the core file
absolute_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(absolute_directory) 

import tkinter as tk

# Our necessary Python files
#import displaying
#import variables
import menu


#================================================
#                CLASSES
#================================================
class Application():
    """
    Class to instance the application
    """
    def __init__(self):
        """
        Constructor for principal app window
        """
        # Creating the window and giving to it a title
        self.root = tk.Tk()
        self.root.title('DCViewer')

        # Creating and adding a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.create_menu_bar()

        # Configurations of root window
        self.root.config(
            menu=self.menu_bar, bg='lightblue', 
            relief='sunken', bd='10'
        )
        self.root.geometry('620x680')

        # Add an icon to the window
        initial_image = tk.PhotoImage(file='../LogoDC_Viewer_600.gif')
        self.root.call('wm', 'iconphoto', self.root._w, initial_image)

        # Configuring first column and row of root window to allow frame resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
        # Instance the frame to put things on window app
        self.first_frame = WindowFrame(self.root)
        self.first_frame.do_startup(initial_image)

        # Create a loop for executing the program
        self.root.mainloop()

    def create_menu_bar(self):
        """
        Function to construct the menu bar for app
        """
        #================================================
        #                FILE MENU
        #================================================
        #File options on the menu bar
        file = tk.Menu(self.menu_bar, tearoff=0)
        file.add_command(
            label='Open FITS file', 
            command=lambda:menu.File().open_file(self.first_frame.frame)
        )
        file.add_command(
            label='Display Header', 
            command=lambda:menu.File().display_header('Header', self.root)
        )
        file.add_separator()
        file.add_command(
            label='Exit', 
            command=lambda:menu.File().exit_program(self.root)
        )

        #================================================
        #                TOOLS MENU
        #================================================
        # Tools options on the menubar
        tools = tk.Menu(self.menu_bar, tearoff=0)

        #=================== SCALE OPTION ===================
        # Scale and sub-options in Tools
        scale = tk.Menu(tools, tearoff=0)
        scale.add_command(
            label="Linear scale", 
            command=lambda:menu.Tools(self.first_frame.frame).change_scale('Linear')
        )
        scale.add_command(
            label="Log scale", 
            command=lambda:menu.Tools(self.first_frame.frame).change_scale('Log')
        )
        scale.add_command(
            label="Sqrt scale", 
            command=lambda:menu.Tools(self.first_frame.frame).change_scale('Sqrt')
        )

        # Add Scale option to Tools
        tools.add_cascade(label='Scale', menu=scale)

        #=================== COLORMAP OPTION ===================
        # Colormaps and sub-options in Tools
        colormap = tk.Menu(tools, tearoff=0)
        
        # Adding perceptually uniform sequential colormaps
        colormap.add_command(
            label='viridis', 
            command=lambda:menu.Tools(self.first_frame.frame).change_colormap('viridis')
        )
        colormap.add_command(
            label='plasma', 
            command=lambda:menu.Tools(self.first_frame.frame).change_colormap('plasma')
        )
        colormap.add_command(
            label='inferno', 
            command=lambda:menu.Tools(self.first_frame.frame).change_colormap('inferno')
        )
        colormap.add_command(
            label='magma', 
            command=lambda:menu.Tools(self.first_frame.frame).change_colormap('magma')
        )
        colormap.add_separator()
        
        # Adding sequential colormaps
        colormap.add_command(
            label='Greys', 
            command=lambda:menu.Tools(self.first_frame.frame).change_colormap('Greys')
        )
        colormap.add_command(
            label='Blues', 
            command=lambda:menu.Tools(self.first_frame.frame).change_colormap('Blues')
        )
        colormap.add_command(
            label='Reds', 
            command=lambda:menu.Tools(self.first_frame.frame).change_colormap('Reds')
        )

        # Add Colormap option to Tools 
        tools.add_cascade(label='Colormap', menu=colormap)

        #================================================
        #                   HELP MENU
        #================================================
        #Help options on menu bar
        help = tk.Menu(self.menu_bar, tearoff=0)
        help.add_command(
            label='License', 
            command=lambda:menu.Help().text_license(
                'License', open('../notice.md', 'r').read(), self.root)
        )
        help.add_command(
            label='About',
            command=lambda:menu.Help().text_about(
                'About', 'DCViewer version 0.2: Ordovician period')
        )

        #================================================
        #           ADDING OPTIONS TO MENU BAR
        #================================================
        self.menu_bar.add_cascade(label='File', menu=file)
        self.menu_bar.add_cascade(label='Tools', menu=tools)
        self.menu_bar.add_cascade(label='Help', menu=help)


class WindowFrame():
    """
    Class to instace a frame, where will be shown,
    for example, the FITS data figures when opened.
    """
    def __init__(self, root):
        """
        Constructor to attach a frame to the app
        window to display things using grid method.
        """
        # Creating the principal frame for images
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=0, sticky='nswe')
        self.frame.config(bg='pink')

        # Configuring first column and row of frame to allow widget resizing
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def do_startup(self, initial_image):
        """
        The first thing to do when running
        the principal frame
        """
        # Adding an image to initial frame
        tk.Label(
            self.frame, 
            image=initial_image, 
            bg='light steel blue').grid(row=0, column=0, sticky='nswe'
        )
        
        # Adding a text label with the program name
        tk.Label(
            self.frame, 
            text='DCViewer', 
            bg='RoyalBlue2', 
            font=('Ubuntu', 24)).grid(row=1, column=0, sticky='nswe'
        )     


#===========================
#     ASSEMBLE THINGS UP
#===========================
if __name__ == "__main__":
    app = Application()