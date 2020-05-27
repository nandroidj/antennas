'''
Created on May 27, 2020

@author: nandroid

• Punto 4:
A partir de las dimensiones de los conductores de la lınea de transmisión coaxial y del valor de la
permitividad relativa epsilon_r del dieléctrico, obtenidos de las hojas de datos del fabricante, determinar la
impedancia caracterıstica Z0 analıticamente.

Para muy altas frecuencias el modelo cuasi-estático deja de ser bpalido y se debe usar el
modelo de campos de las guı́as de ondas. De acá se deriva la siguiente expresión:
'''
import numpy as np
import math
from P2 import *

epsilon_0 = 8.85e-12    # F/m    Permitividad en el vacio
mu_0 = 1.25e-6          # H/m    Permeabilidad en el vacio
pi = math.pi

epsilon_r = 2.25        # permitividad del polotietileno

z_0_rg213 = np.sqrt(mu_0)/(2*pi*np.sqrt(epsilon_0*epsilon_r)) * math.log(rg213_outer_conductor/rg213_inner_conductor )
print(z_0_rg213)

z_0_rg58 = np.sqrt(mu_0)/(2*pi*np.sqrt(epsilon_0*epsilon_r)) * math.log(rg58_outer_conductor/rg58_inner_conductor )
print(z_0_rg58)


'''
De las hojas de datos se obtuvieron los diámetros internos y externos de ambas clases de
coaxiales y el material dieléctrico con el que están constituidos. Con la información sobre el
material dieléctrico, se puede encontrar la constante dieléctrica y de esta manera volcar los
datos en la fórmula de arriba para obtener el Zo de cada tipo de lınea.
'''

