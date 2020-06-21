'''
Created on May 20, 2020

@author: nandroid
'''
import math
import numpy as np
import sympy

'''
3. Considere una linea de transmisión de Z_0 = 50 Ω que posee una ROE = 3 a la cual se le ha medido
el patrón de ondas estacionarias, y entre dos minimos sucesivos se midió una distancia de 40 cm. 
Se pide determinar:

a) La longitud de onda dentro de la lınea.

    Longitud de ondaλ: Es la distancia entre dosmáximos (o mínimos ) sucesivos de la onda. 
    Es unaseparación  espacial,  no  temporal.  La  unidad  demedida en MKS es el metro.
    
    
    https://www.allaboutcircuits.com/textbook/alternating-current/chpt-14/long-and-short-transmission-lines/
'''

z_0 = 50 # ohm
ROE = 3
wave_length = 40 # cm     ES LA LONGITUD DE ONDA DENTRO DE LA LINEA?
c = 3e8

f_0 = c / wave_length

'''
b) El módulo del coeficiente de reflexión.
'''

rho = sympy.Symbol('rho', rational=True)
f1 = ROE*(1 - rho)/(1 + rho) - 1 

# The first argument for solve() is an equation (equaled to zero) 
# and the second argument is the symbol that we want to solve the equation for.

reflection_coefficient = sympy.solve(f1,rho)

'''
c) La constante de fase β [rad/m].

    https://en.wikipedia.org/wiki/Propagation_constant#Phase_constant
'''

beta = 2*math.pi / wave_length

