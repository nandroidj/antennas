'''
Created on Jun 6, 2020

@author: nandroid
'''


import math
import numpy as np
import matplotlib.pyplot as plt

from scipy import integrate
from sympy import Symbol, cos, sin
from Crypto.Util.number import size

pi = math.pi
c = 3e8

# Datos del dipolo
length = 1 # m
radio = 1e-3 # mm
sigma = 5.8e7 # S/m
mu = 4*pi*1e-7

# Datos del monopolo
# radio y conductividad idem dipolo
heigth = 1/2 #
length_monopole = 2*length


'''
    Resistencia de Radiacion - Dipolo Delgado
    
    Balanis - pags. 173 a 176.
        A partir de P_rad = I0^2 * R_rad 
    
    Electronic Engineer Reference Book - pag. 646+647 (49/15)

    input : termino L/lambda
    output : resistencia de radiacion
'''

def dipole_radiation_resistance_integrand(x,l):

    num = ((np.cos(pi*l*np.cos(x)) - np.cos(pi*l))**2)
    den = np.sin(x)
    
    return num/den

def dipole_radiation_resistance_equation(l):
    
    r_radiation = integrate.quad(lambda x, l: dipole_radiation_resistance_integrand(x,l),
                                      0, 3.14, args=(l,))

    return 60 * r_radiation[0]


'''
    Resistencia de Perdida - Dipolo Delgado

    input : termino L/lambda
    output : resistencia de perdida
'''

def dipole_loss_resistance(l):
    
    termino_1 = ((length)**(1/2) / (2*pi*radio))
    termino_2 = ((pi*c*mu)/sigma)**(1/2)
    termino_3 = l**(1/2)
    termino_4 = (1 - (sin(2*pi*l) / (2*pi*l)))

    return termino_1 * termino_2 * termino_3 * termino_4

'''
    Rendimiento del Dipolo - Balanis pag. 86
    
    rendimiento = resistencia_radiacion / (resistencia_perdidas + resistencia_radiacion)
'''

def dipole_efficiency(r_radiation_value, r_loss_value):
    
    return r_radiation_value / (r_radiation_value + r_loss_value)
    

'''
    Directivity - Balanis pag. 191 pdf  [eq 473]
    
    input : length factor, theta_dipole
    ouput : directivity value
'''
        
def dipole_radiation_function(l,theta_dipole):

    num = cos(pi*l*cos(theta_dipole)/2) - cos(pi*l)
    den = sin(theta_dipole)
    
    # F(theta) = f(theta)^2
    return (num/den)**2

def dipole_max_directivity_inTimes(l, r_radiation):
    
    # max when theta = 90 deg
    theta_dipole = 90 # deg
    
    return 120 * dipole_radiation_function(l,theta_dipole) / r_radiation
    

def dipole_directivity_indBi(directivity_value):
    
    return 10*np.log10(directivity_value)


'''
    Ganancia
    
    input : directivity_value , efficiency_value
    ouput : gain_value
'''    

def dipole_gain(directivity_value, efficiency_value):

    return directivity_value * efficiency_value;


'''
    Directivity expression
    
    Balanis eq. 4.74 - pag 191 pdf
    
    Input: dipole_radiation_function
    Output: directivity_value
'''

def dipole_expression(l, theta_dipole):
    
    num = 2*dipole_radiation_function
    den = integrate.quad(lambda theta_dipole: dipole_radiation_function*sin(theta_dipole),0,pi)
    
    return num/den


'''
    Current Distribution
    
    Balanis - pag. 194 pdf
    
    Input : length_factor
    Output : current_distribution_value
    
    
    VER COMO EVALUAR I entre 0 y L/2 y -L/2 y 0
'''

def dipole_current_distribution(l,z):
    
    I_M = 1
    lambda_dipole = length / l
    k = 2*pi / lambda_dipole
    
    I_positive = I_M * sin(k * (length/2 - z))
    I_negative = I_M * sin(k * (length/2 + z))

    return I_positive, I_negative


###################################################################
######################## MONOPOLE    ##############################
###################################################################

'''
    Resistencia de Radiacion - Monopolo
    
    Input : r_radiacion_dipolo
    Output : r_radiacion_monopolo
'''

def monopole_radiation_resistance(r_radiation_dipole):

    return r_radiation_dipole / 2

'''
    Resistencia de Perdida - Monopolo
    
    Input : r_perdida_monopolo
    Output : r_perdida_monopolo
'''

def monopole_loss_resistance(r_loss_dipole):

    return r_loss_dipole / 2


'''
    Rendimiento del Monopolo
    
    rendimiento_monopolo = 1/2 * rendimiento_dipolo

    Directividad Monopolo
    
    directivida_monopolo = 2 * directividad_monopolo
    
    Ganancia Monopolo
    
    ganancia_monopolo = 2 * ganancia_dipolo
    
    
'''



def plot_parameter():
    
    dl = np.arange(0.01,1,0.01)
    r_radiation_list = [dipole_radiation_resistance_equation(l) for l in dl]
    
    r_loss = [dipole_loss_resistance(l) for l in dl]

    plt.plot(dl, r_loss)
    
    plt.plot(dl, r_radiation_list)


def main():
    
    plot_parameter()

    
if __name__ == '__main__':
    main()    
