'''
Created on May 17, 2020

@author: nandroid


A una linea de transmisión de bajas pérdidas se le ha medido, a una frecuencia de 500 MHz, las
siguientes caracterı́sticas.

Determinar R, L, C y G.

Dato: 1 Np = 10*log(e) dB approx. 4.343 dB
'''
import sympy
from sympy.abc import R,L,G,C
import math

pi = math.pi
f = 500e6 # Hz       |    Frecuencia
w = 2*pi*f # rad/s   |    Frecuencia Angular

z_0_real = 50 # ohm       |    Impedancia Caracteristica
z_0_imaginaria = 0 # ohm

alpha = 0.02 # dB/m  |    Constante de Atenuacion
beta = 15.7 # rad/m  |    Constante de Fase

'''
De pag. 7 - lineas de transimision. Apunte 6 de catedra electromagnetismo.

    Se trata de una linea de BAJAS PERDIDAS cuando,
                                                        R << w*L
                                                        G << w*C
'''
f1 = beta/w - sympy.sqrt(L*C)
f2 = alpha - (beta/2) * (R/(w*L) + G/(w*C)) # << beta
f3 = z_0_real - sympy.sqrt(L/C)
f4 = z_0_imaginaria - z_0_real/2 * (G/(w*C) - R/(w*L))

def solve_equation():
    
    sol = sympy.solve([f1,f2,f3,f4], dict=True)                    
    print(sol)
    
if __name__ == '__main__':
    solve_equation()



