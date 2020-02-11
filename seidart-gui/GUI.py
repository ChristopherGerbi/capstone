import numpy as np
from materials.material_functions import isotropic_materials as var

import gui.SeidarTGUI as gui


gui.MATERIALS = var
gui.startGui()



