'''
Created on May 17, 2020

@author: nandroid

Se desea adaptar una antena con impedancia de entrada ZL = 200 Ω a una lı́nea de transmisión
con Z0 = 75 Ω utilizada en TV, con un transformador de cuarto de onda, a la frecuencia central de
operación para el canal 11 de TV (f0 = 199 MHz). Se pide:

Canal    Frecuencia
2            55 MHz
7            175 MHz
9            187 MHz
11           199 MHz
13           211 MHz
'''
import math
import numpy as np
import matplotlib.pyplot as plt


def main():

    pi = math.pi
    
    z_L = 200 # Ohm  Z_L circuit = Z_in_ant
    z_0_tl = 75 # Ohm
    f_0 = 199e6 # Hz
    c = 3e8
    wave_length = c/f_0
        
    
    f_max = 600e6
    
    '''
        a) Calcular la Z0 del transformador de cuarto de onda.
    
    De pag. 1 - lineas de transimision. Apunte 6-Lineas2 de catedra electromagnetismo.
    
    Se trata de un trozo de línea de longitud L_a y de impedancia característica Z_a. 
    Para la adaptación, se requiere que la impedancia de entrada del conjunto carga + adaptador 
    sea igual a la impedancia característica de la línea original Z0.
    '''
    
    z_a = math.sqrt(z_L*z_0_tl)
    
    
    '''
        b) Graficar el módulo y la fase del coeficiente de reflexión en función de f entre 1 y 600 MHz.
    
        si beta = 2*pi/lambda y l = lambda/4 => beta*l = pi*f / 2*f_0 siendo lambda_0
    '''

    z_L_freq = []
    
    reflection_coeff = []
    reflection_coeff_abs = []
    reflection_coeff_angle = []
    
    d_frequency = np.arange(1e6,f_max,1e6)
    
    for freq in d_frequency: 
        
        beta_l = (math.pi/2)*(freq/f_0)
        
        z_L_freq_i = z_a * complex(z_L, z_a*math.tan(beta_l))/complex(z_a, z_L*math.tan(beta_l))
        
        reflection_coeff_i = (z_L_freq_i - z_0_tl)/(z_L_freq_i + z_0_tl)
        reflection_coeff_i_abs = abs(reflection_coeff_i)
        reflection_coeff_i_angle = np.angle(reflection_coeff_i, deg=True)
        
        z_L_freq.append(z_L_freq_i)
        
        reflection_coeff.append(reflection_coeff_i)
        reflection_coeff_abs.append(reflection_coeff_i_abs)
        reflection_coeff_angle.append(reflection_coeff_i_angle)
        

    '''
    c) Graficar la relación de onda estacionaria (ROE) en función de f entre 1 y 600 MHz y calcular el
    ancho de banda considerando que es aceptable una ROE ≤ 2.
    '''
    max_f = np.size(reflection_coeff_abs)
    print(max_f)
    d_ref_abs = np.arange(0,max_f,1)
    ROE = []
    
    for i in d_ref_abs:
        ROE_i = (1 + reflection_coeff_abs[i])/(1 - reflection_coeff_abs[i])
        ROE.append(ROE_i)
    


    # Ancho de banda entre 120 MHz y 300 MHz. Los graficos estan normalizados.
    
    '''
    d) Investigar que sucede con esta adaptación para los otros canales de aire.
    
        En base a la tabla del enunciado, con esta adaptacion y un ROE <= 2 unicamente el canal 2
        no podra ser adaptado.

    e) Diseñar la misma adaptación pero utilizando una linea de transmisión en derivación (stub) en
    cortocircuito, y repetir los puntos b), c) y d).
    
            VER ~/optativas/antenas/guias/ee350-10 + pag 2 - Electro 6-lineas2
    '''
    
    y_0 = 1/z_0_tl
    y_L = 1/z_L
    
    d_s = wave_length/(2*pi) * np.arctan(np.sqrt(z_L/z_0_tl))
#    l_s = wave_length/(2*pi) * np.arctan(2*np.sqrt(z_L*z_0_tl)/(z_L-z_0_tl))
    
    reflection_coeff_stub = []
    reflection_coeff_stub_abs = []
    reflection_coeff_stub_angle = []

    # d_frequency = np.arange(1e6,f_max,1e6)
    
    for freq in d_frequency: 
        
        y_sin = np.sin(2*pi*freq*d_s/c)
        y_cos = np.cos(2*pi*freq*d_s/c)
        
        y_in_num = complex(y_L*y_cos, y_0*y_sin)
        y_in_den = complex(y_0*y_cos, y_L*y_sin)
        y_in = y_0*(y_in_num/y_in_den)
        z_in = 1/y_in
    
        reflection_coeff_stub_i = (z_in - z_0_tl)/(z_in + z_0_tl) 
        reflection_coeff_i_abs = abs(reflection_coeff_i)
        reflection_coeff_stub_angle_i = np.angle(reflection_coeff_i, deg=True)

        reflection_coeff_stub.append(reflection_coeff_stub_i)
        reflection_coeff_stub_abs.append(reflection_coeff_i_abs)
        reflection_coeff_stub_angle.append(reflection_coeff_stub_angle_i)
    
    ##################################################################################
    ROE_stub = []
    
    for i in d_ref_abs:
        ROE_i = (1 + reflection_coeff_stub_abs[i])/(1 - reflection_coeff_stub_abs[i])
        ROE_stub.append(ROE_i)
    
    plt.ion()
    
     # magnitud del coef. de relfexion vs frecuencia
    plt.figure(1)
    plt.plot(d_frequency/f_max, reflection_coeff_abs, label='Magnitud Coeficiente Reflexion')
    plt.xlabel('Frecuencia')
    plt.ylabel('Magnitud')
    plt.grid()
    
    # fase del coef. de relfexion vs frecuencia
    plt.figure(2)
    plt.plot(d_frequency/f_max, np.rad2deg(reflection_coeff_angle), label='Fase Coeficiente Reflexion')
    plt.xlabel('Frecuencia')
    plt.ylabel('Fase')
    plt.grid()
    
    # ROE 
    plt.figure(3)
    plt.plot(d_frequency/f_max, ROE, label='ROE')
    plt.xlabel('Frecuencia')
    plt.ylabel('ROE')
    plt.grid()
    
    # magnitud del coef. de relfexion vs frecuencia
    plt.figure(4)
    plt.plot(d_frequency/f_max, reflection_coeff_stub_abs, label='Magnitud Coeficiente Reflexion')
    plt.xlabel('Frecuencia')
    plt.ylabel('Magnitud')
    plt.grid()
    
    # fase del coef. de relfexion vs frecuencia
    plt.figure(5)
    plt.plot(d_frequency/f_max, np.rad2deg(reflection_coeff_stub_angle), label='Fase Coeficiente Reflexion')
    plt.xlabel('Frecuencia')
    plt.ylabel('Fase')
    plt.grid()
    
    # ROE 
    plt.figure(6)
    plt.plot(d_frequency/f_max, ROE_stub, label='ROE')
    plt.xlabel('Frecuencia')
    plt.ylabel('ROE')
    plt.grid()
    
    plt.ioff()
    plt.show()
    
    
if __name__ == '__main__':
    main()


