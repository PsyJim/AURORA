#!/bin/bash
###
### A shell script to run DCViewer with ipython before python3
###

if [ -f DCViewer/interface.py ]; then
    
    ipython DCViewer/interface.py || python3 DCViewer/interface.py

else

    echo "There is no python interpreter installed or file interface.py doesn't exist!"
    exit    

fi
