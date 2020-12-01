#!/bin/bash
###
### A shell script to run DCViewer with ipython before python3
###

if [ -f DCViewer/Interface.py ]; then
    
    ipython DCViewer/Interface.py || python3 DCViewer/Interface.py

else

    echo "There is no python interpreter installed!"
    exit    

fi
