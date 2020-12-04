# DCViewer (Data Cube Viewer)

## An introduction

### What is DCViewer?
DCViewer is a Python 3 graphical interface GPLv3 licensed. This program it's intented to display and analysis with different tools, the more distinct data cubes formats of IFU telescopes.

### Why DCViewer?
We want to create a program that actually could be used to display and work with some distint data cubes. This due the lack of compatibility among the way that IFS telescope manage their data.

### What DCViewer can do?
As the name says, it can display data cubes from differentes IFS telescopes. Also, we want to add some functions for the sake of data analysis.

## Running DCViewer

### Before running DCViewer!
Like a lot Python programs out there, we implement distint packages to get done our program. In this case, if you haven't anaconda installed, maybe you would like to check Makefile out, it will install the required dependencies with pip install. Just open the shell, get to the root directory of DCViewer and type

```console
$ make
```

Also, in Python distributions that some Linux distros got, tkinter isn't installed (even though it's installed by default when you install Python manually). To handle this, ina debian-based Linux distro type this on the terminal

```console
$ sudo apt-get install python3-tk
```

### How to run DCViewer?
If you have linux (or bash installed on your PC) and ipython (or python3) installed, just get into the DCViewer root directory and run the shell file 'RUN' as

```console
$ ./RUN.sh
```



