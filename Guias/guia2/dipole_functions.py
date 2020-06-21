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
    
    dipole_max = max((dipole_radiation_function(l, x) for x in np.deg2rad(range(1,180))))
  
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
    
    if z >= 0:
        I = I_M * sin(k * (length/2 - z))
    else: 
        I = I_M * sin(k * (length/2 + z))

    return I


##############################################################################################################################
##################################################################PLOTS#######################################################
##############################################################################################################################

def plot_current_distribution(l, wd):

    z = np.linspace(-0.5, 0.5, 1000)
    distribution = [dipole_current_distribution(l ,x) for x in z]

    fig = plt.figure()  
    plt.plot(z, distribution,
            linewidth=2, color='r', label=fr'L/\lambda = {l}')
    
    plt.legend(loc='upper right')
    plt.grid('minor')

    save_dir = wd/"Dipolo"
    if not save_dir.is_dir():
        print(f"{save_dir}: Directory not found! Creating one")
        Path.mkdir(save_dir)
    plt.xlabel(r"$z\:[m]$")
    plt.ylabel(r"$I/:[A]$")
    fig.savefig(save_dir/f"currentDist_{l}.png", bbox_inches='tight', dpi=150)
    


def polar_plot_dB(l, mindB, wd, key):
    #####Parametros
    
    avoid0 = 0.001

    if key == "Dipolo":
        dtheta = np.linspace(avoid0, 2*pi, 1000)
    if key == "Monopolo":
        dtheta = np.linspace(-pi/2, pi/2, 1000)

    ## R radation and R loss
    R_rad = dipole_radiation_resistance_equation(l)
    R_loss = dipole_loss_resistance(l)
    
    if key == "Monopolo":
        R_rad = np.divide(R_rad, 2)
        R_loss = np.divide(R_loss, 2)

    ## D and eff
    directivity = dipole_max_directivity_inTimes(l)

    if key == "Monopolo":
        directivity = np.multiply(directivity, 2)

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
              for x in filteredF] 
    
    ##### Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    
    ax.plot(dtheta, F_g_db,
            label=fr'$L/\lambda$ = {l}',
            color='m', linewidth=2)
    ax.legend(loc='upper right')
    
    save_dir = wd/f"{key}"
    if not save_dir.is_dir():
        print(f"{save_dir}: Directory not found! Creating one")
        Path.mkdir(save_dir)

    fig.savefig(save_dir/f"polarplotL_{l}.png", bbox_inches='tight', dpi=150)
    


def min_max_val(parameter, param, key):
    minVal = min(parameter)
    maxVal = max(parameter)

    print(f"| {key} {param} minima | {minVal} |", file=open("README.md","a"))
    print(f"| {key} {param} maxima | {maxVal} |", file=open("README.md","a"))

def plot_parameter(param, dictionary, wd):
    
    #### All lengths

    for key, value in dictionary.items():    
        #dl = np.arange(0.01,1,0.01) 
        dl = value
    
        if param == 'Radiation Resistance':
            parameter = [dipole_radiation_resistance_equation(l) 
                            for l in dl]
            if(key == 'Monopolo'):
               parameter = np.divide(parameter, 2)
            
            min_max_val(parameter, param, key)
            _ylabel = r"$R_{RAD} [\Omega]$"

        elif param == 'Loss Resistance': 
            parameter = [dipole_loss_resistance(l) 
                  for l in dl]

            if(key == 'Monopolo'):
                parameter = np.divide(parameter, 2)

            min_max_val(parameter, param, key)
            _ylabel = r"$R_{Loss} [\Omega]$"

        elif param == 'Efficiency':
            parameter = [dipole_efficiency(dipole_radiation_resistance_equation(l),
                                 dipole_loss_resistance(l)) for l in dl]
            min_max_val(parameter, param, key)

            _ylabel = r"$\eta $"
        elif param == 'Directivity':
            parameter = [dipole_max_directivity_inTimes(l) 
                       for l in dl]
                        
            if(key == 'Monopolo'):
                parameter = np.multiply(parameter, 2)

            min_max_val(parameter, param, key)
            _ylabel = r"D"

        elif param == 'Gain':
            
            directivity = [dipole_max_directivity_inTimes(l) 
                       for l in dl]
            
            if(key == 'Monopolo'):
                directivity = np.multiply(directivity, 2)

            eff = [dipole_efficiency(dipole_radiation_resistance_equation(l),
                    dipole_loss_resistance(l)) for l in dl]
            
            parameter = np.multiply(directivity, eff)

            min_max_val(parameter, param, key)
            _ylabel = r"Ganancia"

        else:
            print(f"Error {param} param not found!")
            return 
       
       ## Only plot dipolo or monopolo
        if(key == "Dipolo" or key == "Monopolo"):

            fig = plt.figure()
    
            plt.plot(dl, parameter,
                    linewidth=2, color='b',
                    label=fr'{param}')
            plt.legend(loc='upper left')
            plt.grid('minor')

            save_dir = wd/f"{key}"
            if not save_dir.is_dir():
                print(f"{save_dir}: Directory not found! Creating one")
                Path.mkdir(save_dir)

            plt.xlabel(r"$\frac{L}{\lambda}\:[Hz/m]$")
            plt.ylabel(fr"{_ylabel}")
            fig.savefig(save_dir/f"{param}.png", bbox_inches='tight', dpi=150)
            ## dB Plot
            if param == 'Gain': 
                fig = plt.figure()

                todB = lambda x: 10*np.log10(x)
                parameter = [todB(float(x)) for x in parameter]

                plt.plot(dl, parameter,
                    linewidth=2, color='b',
                    label=fr'{param}')
                plt.legend(loc='upper left')
                plt.grid('minor')
                plt.xlabel(r"$\frac{L}{\lambda}\:[Hz/m]$")
                plt.ylabel("Ganancia [dB]")
                fig.savefig(save_dir/f"{param}db.png", bbox_inches='tight', dpi=150)


def main():
    
    ################################# Manage paths #############################
    WORKING_DIR = Path.cwd()
    IMG_DIR = WORKING_DIR/"Img"
    ### Check if Img dir exist
    if not IMG_DIR.is_dir():
        ### if not exist then create the dir
        print(IMG_DIR, ": Directory not found. Making it for you")
        Path.mkdir(IMG_DIR)
    #############################PARAMETERS#####################################
    
    antennas_t = {
            "Dipolo": np.arange(0.01,1,0.01), 
            "Monopolo": np.arange(0.01,1,0.01), 
            "Dipolo hertz": np.linspace(0.00001, 0.001, 1000),
            "Dipolo corto": np.linspace(0.01, 0.1, 1000),
            "Dipolo media": np.linspace(0.001, 0.5, 1000)
            }

    plotParameters = [
        'Radiation Resistance', 
        'Loss Resistance',
        'Efficiency',
        'Directivity',
        'Gain'
    ]
   
    ## Create table markdown file to generate a table wth the values

    print("## Archivo creado por dipole_functions.py ", file=open("README.md","a"))

    print("| Dato | Valor |", file=open("README.md","a"))
    print("| ---- | ----- |", file=open("README.md","a"))

    ### Plot
    for param in plotParameters:
        print(f"Ploting {param}....")
        plot_parameter(param, antennas_t, IMG_DIR)

    #################################POLAR PLOT##################################       
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

    for key, vals in antennas_t.items():
        if key == "Dipolo" or key == "Monopolo":
            for l in lengths:
                print(f"{key}: Ploting polar plor for L/lam = {l}")
                polar_plot_dB(l ,mindB, IMG_DIR, key)

    #################################CUrrent Distribution#########################
    lengths_c = [
            0.01,
            0.1,
            0.5,
            1
    ]

    for l in lengths_c:
        print(f"Ploting current distribution for L/lam = {l}")
        plot_current_distribution(l,IMG_DIR)

if __name__ == '__main__':
   main()

