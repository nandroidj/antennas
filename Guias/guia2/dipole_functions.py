'''
Created on Jun 6, 2020

@author: nandroid
'''


import math
import numpy as np
import matplotlib.pyplot as plt
import os

from scipy import integrate
from sympy import Symbol, cos, sin
from Crypto.Util.number import size
from cmath import polar
from pathlib import Path ## Manejo de directorios

from dictionaries import *

pi = math.pi
c = 3e8

# Datos del dipolo
length = 1 # m
radio = 1 # mm
sigma = 5.8e7 # S/m
mu = 4*pi*1e-7

# Datos del monopolo
# radio y conductividad idem dipolo
heigth = 1/2 #m
length_monopole = 2*length


'''
    Resistencia de Radiacion - Dipolo Delgado
    
    Balanis - pags. 173 a 176.
        A partir de P_rad = I0^2 * R_rad 
    
    Electronic Engineer Reference Book - pag. 646+647 (49/15)

    input : termino L/lambda
    output : resistencia de radiacion
'''


def dipole_radiation_resistance_integrand(l,x):
    
    num = (np.cos(pi*l*np.cos(x)) - np.cos(pi*l))**2
    den = np.sin(x)
    
    return num/den


def dipole_radiation_resistance_equation(l):
    
    r_radiation = integrate.quad(lambda x: dipole_radiation_resistance_integrand(l,x), 0, pi)

    return 60 * r_radiation[0]


'''
    Resistencia de Perdida - Dipolo Delgado

    input : termino L/lambda
    output : resistencia de perdida
'''

def dipole_loss_resistance(l):
    
    termino_1 = length**1/2 / (2*pi*radio)
    termino_2 = (pi*c*mu/sigma)**1/2
    termino_3 = l**1/2
    termino_4 = 1- (sin(2*pi*l)/ (2*pi*l))

    return termino_1 * termino_2 * termino_3 * termino_4

'''
    Rendimiento del Dipolo - Balanis pag. 86
    
    rendimiento = resistencia_radiacion / (resistencia_perdidas + resistencia_radiacion)
'''

def dipole_efficiency(l):
    
    return dipole_radiation_resistance_equation(l) / (dipole_radiation_resistance_equation(l) + dipole_loss_resistance(l))
    

'''
    Directivity - Balanis pag. 191 pdf  [eq 473]
    
    input : length factor, theta_dipole
    ouput : directivity value
'''
        
def dipole_radiation_function(l,theta_dipole):

    num = (cos(pi*l*cos(theta_dipole)/2) - cos(pi*l))
    den = sin(theta_dipole)
    
    # F(theta) = f(theta)^2
    return (num/den)**2

def dipole_max_directivity_inTimes(l):
    
    # max when theta = 90 deg
    theta_dipole = 90 # deg
    
    return 120 * dipole_radiation_function(l,theta_dipole) / dipole_radiation_resistance_equation(l)
    

def dipole_directivity_indBi(l):
    
    in_times = dipole_max_directivity_inTimes(l)
    
    return 10 * math.log10(in_times)


'''
    Ganancia
    
    input : directivity_value , efficiency_value
    ouput : gain_value
'''    

def dipole_gain_inTimes(l):

#    return directivity_value * efficiency_value;

    return float(dipole_max_directivity_inTimes(l) * dipole_efficiency(l))

def dipole_gain_indBi(l):
    
    in_times = dipole_gain_inTimes(l)
    
    return 10 * math.log10(in_times)


'''
    Directivity expression
    
    Balanis eq. 4.74 - pag 191 pdf
    
    Input: dipole_radiation_function
    Output: directivity_value
'''
 
def dipole_expression(l,theta_dipole):
        
    num = 2 * dipole_radiation_function(l,theta_dipole)
    
    den = integrate.quad(lambda x: dipole_radiation_function(l,x)*sin(x),0,pi)

    return num /(den[0])


'''
    Current Distribution
    
    Balanis - pag. 194 pdf
    
    Input : length_factor
    Output : current_distribution_value
    
    VER COMO EVALUAR I entre [-L/2 ; 0] y [0 ; L/2]  
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

###################################################################
######################## MONOPOLE    ##############################
###################################################################

'''
    r_rad_monopole = r_radiation_dipole / 2

    r_perd_monopole = r_perd_dipole / 2
    
    Rendimiento del Monopolo
    
    rendimiento_monopolo = 1/2 * rendimiento_dipolo

    Directividad Monopolo
    
    directivida_monopolo = 2 * directividad_monopolo
    
    Ganancia Monopolo
    
    ganancia_monopolo = 2 * ganancia_dipolo
    
    
'''


 
'''
    recibir func y el diccionario pertinente a plotear en la llamada de
    cada funcion tipo r_radiation, directivity
'''    
def evaluate_parameters():
    
    theta_dipole = np.arange(0.01,pi, 0.5)
    
    for key, value in dipole_dictionary.items():
        for v in value:
            r_radiation_dictionary[key].append(dipole_radiation_resistance_equation(v))
            loss_resistance_dictionary[key].append(dipole_loss_resistance(v))
            efficiency_dictionary[key].append(dipole_efficiency(v))
            directivity_dictionary[key].append(dipole_max_directivity_inTimes(v))
            directivity_dbi_dictionary[key].append(dipole_directivity_indBi(v))
            gain_dictionary[key].append(dipole_gain_inTimes(v))
            gain_dbi_dictionary[key].append(dipole_gain_indBi(v))
            
            # Radiation Patterns in Mati's script.

def plot_dipole_parameters(wd):               

    save_dir = wd/"dipole/"
    if not save_dir.is_dir():
        print(f"{save_dir}: Directory not found! Creating one")
        Path.mkdir(save_dir)


    for key_dipole in dipole_dictionary.keys():

        save_dir_r_resistance= wd/"dipole/radiation_resistance/"
        if not save_dir_r_resistance.is_dir():
            print(f"{key_dipole}_r_radiation_dipole: Directory not found! Creating one")
            Path.mkdir(save_dir_r_resistance)


        for key_r_radiation in r_radiation_dictionary.keys():

            if key_dipole == key_r_radiation:       
                plt.figure()
                plt.ion()
                plt.xlabel('L/lambda')
                plt.ylabel(key_r_radiation + ' ' + '[Ohm]')
                plt.plot(dipole_dictionary[key_dipole], r_radiation_dictionary[key_r_radiation], color='g')
                plt.grid()
                plt.ioff()
                
                plt.savefig(save_dir_r_resistance/f"{key_dipole}_r_radiation_dipole.png", bbox_inches='tight', dpi=150)

        save_dir_loss_resistance= wd/"dipole/loss_resistance/"
        if not save_dir_loss_resistance.is_dir():
            print(f"{key_dipole}_r_loss_dipole: Directory not found! Creating one")
            Path.mkdir(save_dir_loss_resistance)

        for key_loss in loss_resistance_dictionary.keys():

            if key_dipole == key_loss:       
                plt.figure()
                plt.ion()
                plt.xlabel('L/lambda')
                plt.ylabel(key_loss + ' ' + '[Ohm]')
                plt.plot(dipole_dictionary[key_dipole], loss_resistance_dictionary[key_loss], color='g')
                plt.grid()
                plt.ioff()
                plt.savefig(save_dir_loss_resistance/f"{key_dipole}_r_loss_dipole.png", bbox_inches='tight', dpi=150)


        save_dir_efficiency= wd/"dipole/efficiency/"
        if not save_dir_efficiency.is_dir():
            print(f"{key_dipole}_r_efficiency: Directory not found! Creating one")
            Path.mkdir(save_dir_efficiency)

        for key_efficiency in efficiency_dictionary.keys():

            if key_dipole == key_efficiency:       
                plt.figure()
                plt.ion()
                plt.xlabel('L/lambda')
                plt.ylabel('Rendimiento' + ' ' + '[%]')
                plt.plot(dipole_dictionary[key_dipole], efficiency_dictionary[key_efficiency], color='g')
                plt.grid()
                plt.ioff()
                plt.savefig(save_dir_efficiency/f"{key_dipole}_efficiency_dipole.png", bbox_inches='tight', dpi=150)

        save_dir_directivity= wd/"dipole/directivity/"
        if not save_dir_directivity.is_dir():
            print(f"{key_dipole}_directivity: Directory not found! Creating one")
            Path.mkdir(save_dir_directivity)


        for key_directivity in directivity_dictionary.keys():

            if key_dipole == key_directivity:       
                plt.figure()
                plt.ion()
                plt.xlabel('L/lambda')
                plt.ylabel('Directividad' + ' ' + '[veces]')
                plt.plot(dipole_dictionary[key_dipole], directivity_dictionary[key_directivity], color='g')
                plt.grid()
                plt.ioff()
                plt.savefig(save_dir_directivity/f"{key_dipole}_directivity_dipole.png", bbox_inches='tight', dpi=150)


        save_dir_directivity_dbi = wd/"dipole/directivity/dbi/"
        if not  save_dir_directivity_dbi.is_dir():
            print(f"{key_dipole}_directivity_dbi: Directory not found! Creating one")
            Path.mkdir(save_dir_directivity_dbi)

        for key_directivity_dbi in directivity_dbi_dictionary.keys():

            if key_dipole == key_directivity_dbi:       
                plt.figure()
                plt.ion()
                plt.xlabel('L/lambda')
                plt.ylabel('Directividad' + ' ' + '[dBi]')
                plt.plot(dipole_dictionary[key_dipole], directivity_dbi_dictionary[key_directivity_dbi], color='g')
                plt.grid()
                plt.ioff()
                plt.savefig(save_dir_directivity_dbi/f"{key_dipole}_directivity_dbi_dipole.png", bbox_inches='tight', dpi=150)

        save_dir_gain_times = wd/"dipole/gain/"
        if not save_dir_gain_times.is_dir():
            print(f"{key_dipole}_gain_times: Directory not found! Creating one")
            Path.mkdir(save_dir_gain_times)

        for key_gain in gain_dictionary.keys():

            if key_dipole == key_gain:       
                plt.figure()
                plt.ion()
                plt.xlabel('L/lambda')
                plt.ylabel('Ganancia' + ' ' + '[veces]')
                plt.plot(dipole_dictionary[key_dipole], gain_dictionary[key_gain], color='g')
                plt.grid()
                plt.ioff()
                plt.savefig(save_dir_gain_times/f"{key_dipole}_gain_dipole.png", bbox_inches='tight', dpi=150)

        save_dir_gain_dbi = wd/"dipole/gain/dbi/"
        if not save_dir_gain_dbi.is_dir():
            print(f"{key_dipole}_gain_times: Directory not found! Creating one")
            Path.mkdir(save_dir_gain_dbi)


        for key_gain_dbi in gain_dbi_dictionary.keys():

            if key_dipole == key_gain_dbi:       
                plt.figure()
                plt.ion()
                plt.xlabel('L/lambda')
                plt.ylabel('Directividad' + ' ' + '[dBi]')
                plt.plot(dipole_dictionary[key_dipole], gain_dbi_dictionary[key_gain_dbi], color='g')
                plt.grid()
                plt.ioff()
                plt.savefig(save_dir_gain_dbi/f"{key_dipole}_gain_dbi_dipole.png", bbox_inches='tight', dpi=150)
                

def plot_monopole_parameters(wd):

    plt.figure()
    plt.ion()
    plt.xlabel('L/lambda')
    plt.ylabel('dipole_pure' + ' ' + '[Ohm]')
    plt.plot(dipole_dictionary['dipole_pure'], [x / 2 for x in r_radiation_dictionary['dipole_pure']], color='g')
    plt.grid()
    plt.ioff()

    save_dir= wd/"monopole/"
    if not save_dir.is_dir():
        print(f"{save_dir}: Directory not found! Creating one")
        Path.mkdir(save_dir)
    
    plt.savefig(save_dir/f"monopole_r_radiation.png", bbox_inches='tight', dpi=150)

    plt.figure()
    plt.ion()
    plt.xlabel('L/lambda')
    plt.ylabel('dipole_pure' + ' ' + '[Ohm]')
    plt.plot(dipole_dictionary['dipole_pure'], [x / 2 for x in loss_resistance_dictionary['dipole_pure']], color='g')
    plt.grid()
    plt.ioff()
    
    plt.savefig(save_dir/f"monopole_r_loss.png", bbox_inches='tight', dpi=150)

    plt.figure()
    plt.ion()
    plt.xlabel('L/lambda')
    plt.ylabel('Rendimiento' + ' ' + '[%]')
    plt.plot(dipole_dictionary['dipole_pure'], [x / 2 for x in efficiency_dictionary['dipole_pure']], color='g')
    plt.grid()
    plt.ioff()

    plt.savefig(save_dir/f"monopole_efficiency.png", bbox_inches='tight', dpi=150)

    plt.figure()
    plt.ion()
    plt.xlabel('L/lambda')
    plt.ylabel('Directividad' + ' ' + '[veces]')
    plt.plot(dipole_dictionary['dipole_pure'], [x * 2 for x in directivity_dictionary['dipole_pure']], color='g')
    plt.grid()
    plt.ioff()

    plt.savefig(save_dir/f"monopole_directivity.png", bbox_inches='tight', dpi=150)

    plt.figure()
    plt.ion()
    plt.xlabel('L/lambda')
    plt.ylabel('Directividad' + ' ' + '[dBi]')
    plt.plot(dipole_dictionary['dipole_pure'], [x * 2 for x in directivity_dbi_dictionary['dipole_pure']], color='g')
    plt.grid()
    plt.ioff()
    
    plt.savefig(save_dir/f"monopole_directivity_dbi.png", bbox_inches='tight', dpi=150)

    plt.figure()
    plt.ion()
    plt.xlabel('L/lambda')
    plt.ylabel('Ganancia' + ' ' + '[veces]')
    plt.plot(dipole_dictionary['dipole_pure'], [x * 2 for x in gain_dictionary['dipole_pure']], color='g')
    plt.grid()
    plt.ioff()

    plt.savefig(save_dir/f"monopole_gain_times.png", bbox_inches='tight', dpi=150)    
    
    plt.figure()
    plt.ion()
    plt.xlabel('L/lambda')
    plt.ylabel('Ganancia' + ' ' + '[veces]')
    plt.plot(dipole_dictionary['dipole_pure'], [x * 2 for x in gain_dbi_dictionary['dipole_pure']], color='g')
    plt.grid()
    plt.ioff()

    plt.savefig(save_dir/f"monopole_gain_dbi.png", bbox_inches='tight', dpi=150)    


def plot_current_distribution(l, wd):

    z = np.linspace(-0.5, 0.5, 1000)
    distribution = [dipole_current_distribution(l ,x) for x in z]

    fig = plt.figure()
    plt.plot(distribution, z, 
            linewidth=2, color='g', label=fr'L/\lambda = {l}')
    
    plt.legend(loc='upper right')
    plt.grid()

    save_dir = wd/"dipole/current_distribution/"
    if not save_dir.is_dir():
        print(save_dir/f"{save_dir}: Directory not found! Creating one")
        Path.mkdir(save_dir)

    fig.savefig(save_dir/f"currentDist_{l}.png", bbox_inches='tight', dpi=150)
    

def main():

    WORKING_DIR = Path.cwd()
    IMG_DIR = WORKING_DIR/"imgs"
    
    evaluate_parameters()
    plot_dipole_parameters(IMG_DIR)
    plot_monopole_parameters(IMG_DIR)

    lengths_c = [
            0.01,
            0.1,
            0.5,
            1
    ]

    for l in lengths_c:
        plot_current_distribution(l,IMG_DIR)    

    
if __name__ == '__main__':
    main()    
    
