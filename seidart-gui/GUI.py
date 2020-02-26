import numpy as np
from materials.material_functions import isotropic_materials as var

import gui.SeidarTGUI as gui
import os


#command = "f2py -c -m seismicFDTD2D fdtd/seismicFDTD2D.f95"
#os.system(command)
#command = "f2py -c -m emFDTD2D fdtd/emFDTD2D.f95"
#os.system(command)

gui.MATERIALS = var
gui.startGui()



