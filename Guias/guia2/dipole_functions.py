'''
Created on Jun 6, 2020

@author: nandroid
'''


import math
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path ## Manejo de directorios

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
        
def dipole_radiation_function(l, theta_dipole):

    num = (np.cos(pi*l*np.cos(theta_dipole)) - np.cos(pi*l))
    den = np.sin(theta_dipole)
    
    return (num/den)**2

def dipole_max_directivity_inTimes(l):
    
    dipole_max = max((dipole_radiation_function(l, x) for x in range(1,180)))
  
    func = lambda x, l: dipole_radiation_function(l, x)*np.sin(x)
    r_radiation = integrate.quad(func, 0, pi, args=(l,))[0]
      
    return 2 * dipole_max / r_radiation
    

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

def polar_plot_dB(l, mindB, wd):
    #####Parametros
    avoid0 = 0.001
    dtheta = np.linspace(avoid0, 2*pi, 1000)
    
    ## R radation and R loss
    R_rad = dipole_radiation_resistance_equation(l)
    R_loss = dipole_loss_resistance(l)
    
    ## D and eff
    directivity = dipole_max_directivity_inTimes(l)
    efficiency = dipole_efficiency(R_rad, R_loss)
        
    #### Caluclo de la ganancia
    # Hay que castear a float para usar np.log10()
    gain = float(directivity * efficiency)
    
    # lambda fucntion G*F() 
    # List comprehension gF fot all theta in dtheta
    gF = lambda x: abs(gain*dipole_radiation_function(l, x))
    F = [gF(theta) for theta in dtheta]
    
    # filtered 0 values in F
    filteredF = [x if x != 0 else x+avoid0 for x in F]
     # values to dB, check if is grather that mindB
    todB = lambda x: 10*np.log10(x)
    F_g_db = [todB(x) if todB(x) > mindB else mindB
              for x in filteredF ] 
    
    ##### Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    
    ax.plot(dtheta, F_g_db,
            label=fr'$L/\lambda$ = {l}',
            color='m', linewidth=2)
    ax.legend(loc='upper right')
    
    fig.savefig(wd/f"polarplotL_{l}.png", bbox_inches='tight', dpi=150)
    

def plot_parameter(param, wd):
    
    #### All lengths
    dl = np.arange(0.01,1,0.01)
    
    
    if param == 'Radiation Resistance':
        parameter = [dipole_radiation_resistance_equation(l) 
                            for l in dl]
    elif param == 'Loss Resistance': 
        parameter = [dipole_loss_resistance(l) 
                  for l in dl]
    elif param == 'Efficiency':
        parameter = [dipole_efficiency(dipole_radiation_resistance_equation(l),
                                 dipole_loss_resistance(l)) for l in dl]
    elif param == 'Directivity':
        parameter = [dipole_max_directivity_inTimes(l) 
                       for l in dl]
    else:
        print(f"Error {param} param not found!")
        return 
    
    fig = plt.figure()
    
    plt.plot(dl, parameter,
             linewidth=2, color='b',
             label=fr'{param}')
    
    plt.legend(loc='upper left')
    plt.grid('minor')
    
    fig.savefig(wd/f"{param}.png", bbox_inches='tight', dpi=150)
    


def main():
    
    ### Manage paths
    WORKING_DIR = Path.cwd()
    IMG_DIR = WORKING_DIR/"Img"
    ### Check if Img dir exist
    if not IMG_DIR.is_dir():
        ### if not exist then create the dir
        Path.mkdir(IMG_DIR)
    
    ### All posible parameters
    plotParameters = [
        'Radiation Resistance', 
        'Loss Resistance',
        'Efficiency',
        'Directivity',
        'Random To Test Errors'
    ]
    
    ### Plot
    for param in plotParameters:
        print(f"Ploting {param}....")
        plot_parameter(param, IMG_DIR)
        
    ### All posible length       
    lengths = [
        0.1,
        0.5,
        1,
        1.25,
        1.5
    ]
    
    ### Min dB ploted
    mindB = -30
    
    ### Plot
    for l in lengths:
        print(f"Ploting polar plor for L/lam = {l}")
        polar_plot_dB(l ,mindB, IMG_DIR)
        
                       
if __name__ == '__main__':
    main()    
