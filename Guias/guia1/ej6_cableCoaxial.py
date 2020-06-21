'''
Created on May 20, 2020

@author: nandroid

6. Considere una linea de transmisión coaxial del tipo RG 58, que posee las siguientes caracteristicas:

        epsilon_r = 2,26
        a = 0,406 mm
        b = 1,48 mm
        μ = μ0
'''
import math
import numpy as np

epsilon_0 = 8.85e-12    # F/m    Permitividad en el vacio
mu_0 = 1.25e-6          # H/m    Permeabilidad en el vacio

epsilon_r = 2.26 
a = 0.406 #mm
b = 1.48 #mm
mu_r = mu_0 

'''
a) La impedancia caracteristica Z0.
    https://www.everythingrf.com/rf-calculators/coaxial-cable-calculator
    Referencia: http://www.idc-online.com/technical_references/pdfs/data_communications/RG_58.pdf
'''

z_0 = 138*np.log10(b/a) / np.sqrt(epsilon_r)
print(z_0)

'''
b) La velocidad de propagación respecto a la velocidad de la luz, en valor porcentual.

    https://www.everythingrf.com/community/what-is-propagation-velocity-in-a-cable
'''
c = 1/(np.sqrt(mu_0*epsilon_0))
print('Velocidad de la luz',c)

vop = 1/np.sqrt(epsilon_r)
print('Factor de velocidad =', vop) 

relacion_porcentual = vop * 100
print('Relacion porcentual respecto a la velocidad de la luz,', relacion_porcentual,'%')





