"""
Anntena parametres
"""

import numpy as np


def impedance(reflexion_coef, caracteristic_impedance):
    """@brief funcion para calcular la impedancia de la antena
    dado gamma o la reflexión en la antena y la impedancia 
    caracterisitca
    """
    zo = caracteristic_impedance
    gamma = reflexion_coef

    return [zo * (1+x)/(1-x) for x in gamma]

def get_real_imag_parts(arr):

    real = [x.real for x in arr]
    imag = [x.imag for x in arr]

    return real, imag

def reflexion_coef(s_parameter):
    s11 = s_parameter
    return [abs(x) for x in s11]

def reflexion_coef_db(s_parameter):
    s11 = s_parameter
    return [10*np.log10(abs(x)) for x in s11] 

def roe(s_parameter):
    s11 = s_parameter
    reflex = reflexion_coef(s11)

    return [(1 + x) / (1 - x) for x in reflex]
