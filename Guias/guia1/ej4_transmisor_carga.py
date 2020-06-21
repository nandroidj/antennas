'''
Created on May 20, 2020

@author: nandroid

4. Considere que un transmisor se encuentra conectado a una impedancia de carga ZL = 50 Ω y la
potencia sobre dicha carga es de 25 W. Se pide calcular:

        https://www.rfmentor.com/content/dbm-dbw-dbuv-calculators
'''
import math
import numpy as np

z_L = 50 # ohm 
p_L = 25 # W

'''
a) La potencia en dBW.
'''

p_dBW = 10*np.log10(p_L)
print(p_dBW) # 32,19 dBW

'''
b) La potencia en dBm.
'''
p_dBm = 10*np.log10(p_L*10e2)
print(p_dBm)  # 125.29 dBm

# check  dBm to dBW,  simply subtract 30 from the dBm value. 0 dBW = 30 dBm

p_dBW2 = p_dBm - 30
print(p_dBW2)
