'''
Created on May 25, 2020

@author: nandroid

• Punto 2:
Investigar el modelo y las especificaciones del fabricante de las lı́neas de transmisión: impedancia 
caracterıstica, factor de velocidad, atenuación, etc.
'''

#import numpy as np

'''
    Coaxial Cable RG-213 - Electrical Properties
'''

rg213_z_0 = 50 # +-2 ohm    Charasteristic Impedance
rg213_vp = 66 # %    Relative Propagation Velocity
rg213_C = 101e-9 # F/m    Capacitance
rg213_L = 0.253e-6 # H/m  Inductance
rg213_f_max = 2.4e6 # Hz
rg213_inner_R = 5.8 # ohm/km
rg213_outer_R = 4.1 # ohm/km

rg213_inner_conductor = 2.26 # mm
rg213_dielectric = 7.25 # mm
rg213_outer_conductor = 8.11 # mm
rg213_jacket = 10.31 # mm

'''
    Coaxial Cable RG-58 - Electrical Properties
'''

rg58_z_0 = 50 # +-2 ohm    Charasteristic Impedance
rg58_vp = 66 # %    Relative Propagation Velocity
rg58_C = 100e-9 #+-5 F/m    Capacitance
rg58_L = 0.253e-6 # H/m  Inductance
rg58_f_max = 2.4e6 # Hz
rg58_inner_R = 39 # ohm/km
rg58_outer_R = 15 # ohm/km

rg58_inner_conductor = 0.90 # mm
rg58_dielectric = 2.90 # mm
rg58_outer_conductor = 3.55 # mm
rg58_jacket = 5 # mm

