"""
"""
#===========================
#     GLOBAL VARIABLES
#===========================
from astropy.visualization.stretch import LinearStretch, LogStretch, SqrtStretch


data = None
header = ''

# Matplotlib display values
scale_type = {'Linear':LinearStretch(), 'Log':LogStretch(), 'Sqrt':SqrtStretch()}
cmap = None

# FITS coords
x1 = 0
x2 = 0
y1 = 0
y2 = 0