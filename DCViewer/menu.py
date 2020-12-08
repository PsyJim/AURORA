"""
File with the methods related to items from
app menu bar
"""
#===========================
#        LIBRARIES
#===========================
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, scrolledtext


# Our necessary Python files
import variables as var
import displaying


#================================================
#                   CLASSES
#================================================
class File():
    """
    Class to define the methods for the
    options on file menu
    """
    def __init__(self):
        """
        """
        pass

    def open_file(self, frame):
        """
        Function to allow program to open FITS files
        """
        # Defining filetypes to appear on window asking to open files
        filetypes = [('FITS files', ('*.fits', '*.gz')), ('All files', '*.*')]
        
        # Here we're trying to open a FITS file
        file = filedialog.askopenfilename(
            title='Open', 
            initialdir='../', 
            filetypes=filetypes
        )
        
        # Selecting wavelenght to display data cube
        wavelenght = simpledialog.askinteger(
            'Wavelenght', 
            'Type the wavelenght you want'
        )
        
        # Show the data cube
        var.data, var.header = displaying.read_cube(file, wavelenght)
        displaying.show_fits(var.data, var.header, frame)

        return file

    def display_header(self, title, root):
        """
        Function to display a tkinter window with text.
        Useful to display FITS data header.
        """

        # Initilizing another tkinter window and grouping to main program
        window = tk.Toplevel(root)
        window.group(root)
        window.title(title)

        # Enable widgets resizing for new window
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
      
        # Creating Text widget and insert text to it
        text = scrolledtext.ScrolledText(window,  wrap = tk.WORD) 

        text.insert(tk.INSERT, var.header)
        text.configure(state="disabled", relief="flat", wrap='word')
        text.grid(row=0, column=0, sticky='nswe')

        # Allocate button to the bottom of window
        ok_button = tk.Button(window, text='Ok', command=window.destroy)
        ok_button.grid(row=1, column=0)

        # Window loop
        window.mainloop()

    def exit_program(self, root):
        """
        Function to ask to user if really want to close
        """
        value = messagebox.askquestion(
            'Exit', 
            'Are you sure you want to exit?'
        )
    
        # Close the root, so program close too
        if value == 'yes':
            root.destroy()
        else:
            pass


class Tools():
    """
    Class to define the methods for the
    options on tools menu
    """
    def __init__(self, frame):
        """
        """
        self.frame = frame

    def change_scale(self, name):
        """
        Function that change the scale for data
        and re-display the image
        """

        # Change the type of scale
        self.scale = var.scale_type[name]

        # Re-display data
        displaying.show_fits(
            var.data, var.header, 
            self.frame, scale=self.scale
        )

    def change_colormap(self, cmap):
        """
        """
        # Getting the matplotlib colormap
        self.colormap = cmap

        # Re-display data
        displaying.show_fits(
            var.data, var.header, 
            self.frame, colormap=self.colormap
        )


class Help():
    """
    Class to define the methods for the
    options on help menu
    """
    def __init__(self):
        """
        """
        pass

    def text_license(self, title, info, root):
        """
        Function to display a tkinter window with text.
        Useful to display FITS data header.
        """
        # Initilizing another tkinter window and grouping to main program
        window = tk.Toplevel(root)
        window.group(root)
        window.title(title)

        # Enable widgets resizing for new window
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
      
        # Creating Text widget and insert text to it
        text = tk.Text(window, padx=5, pady=5)
        text.insert(tk.INSERT, info)
        text.configure(state="disabled", relief="flat", wrap='word')
        text.grid(row=0, column=0, sticky='nswe')

        # Allocate button to the bottom of window
        ok_button = tk.Button(window, text='Ok', command=window.destroy)
        ok_button.grid(row=1, column=0)

        # Window loop
        window.mainloop()

    def text_about(self, title, info):
        """
        Display a messabox with program info
        """
        messagebox.showinfo(title, info)


#===========================
#     END OF FILE
#===========================
if __name__ == "__main__":
    pass