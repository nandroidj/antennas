'''
Created on May 30, 2020

@author: nandroid

• Punto 5:
Medición de la impedancia caracterı́stica Z0 utilizando el analizador vectorial de redes (VNA):

a) Calibrar el VNA y explicar en qué consiste y por qué se realiza este procedimiento.

    https://www.electronics-notes.com/articles/test-methods/rf-vector-network-analyzer-vna/how-to-calibrate-vna.php
'''

'''
b) Conectar un cortocircuito en el extremo de la lı́nea, medir el coeficiente de reflexión y representar
gráficamente en el diagrama de Smith. Repetir la medición y la representación gráfica conectando
al extremo de la lı́nea un circuito abierto. Realizar las mediciones para un rango de frecuencias
comprendido entre 200 MHz y 1,5 GHz.
'''

from pathlib import Path #TODO: ver
from smithplot import SmithAxes
import numpy as np
import matplotlib.pyplot as plt

#Algunas constantes
IMG_DIR = "imgs"
SRC_DIR = "src/"
IMG_TYPE = "png"
S1P_DATA_DIR = "mediciones/archivos_extension_s1p/"
S2P_DATA_DIR = "mediciones/archivos_extension_s2p/"

def read_data(location, cols, delim):
    """@brief funcion para leer data de un archivo
    @param location es la ubicacion del archivo
    @param cols tupla que indica las columnas que se quieren leer
    @param delim es el delimitador
    @return s los datos leidos
    file = open(location,'r')
    for line in file:
        try:
            data += [line.split(delim)]
        except:
            pass
    """
    data = np.genfromtxt(location,
                         delimiter=delim, skip_header=8, usecols=cols)
    
    return data

def array_to_complex(arr, real, imag):
    """@brief transformar un array de dos dimensiones a un numero complejo \
        input = [Re,Im]
    @return lista de numeros complejos
    """
    return [x[real] + x[imag]*1j for x in arr]

def reflection_coefficient_to_impedance(arr, caracteristic_impedance):
    """@brief transformar los coeficiente de reflexion en impedancia para poder \
        plotear en la carta de smith
    """
    return [caracteristic_impedance * (1+x)/(1-x) for x in arr]
    
def plot_smith_chart(input_impedance, caracteristic_impedance, wd, file_name):
    """@brief plot smith chart function
    """
    directory = wd.parent / IMG_DIR
    if directory.is_dir() is not True:
        directory.mkdir() 
    fig = plt.figure(figsize=(10, 8))
    SmithAxes.update_scParams(axes_impedance=caracteristic_impedance)
    plt.subplot(1, 1, 1, projection='smith', grid_major_enable=True)
    plt.plot(input_impedance, datatype=SmithAxes.Z_PARAMETER)
    plt.show()
    fig.savefig(directory / f'{file_name}.{IMG_TYPE}',
                bbox_inches='tight', dpi=150)

def main():
    """@brief funcion principal
    """
    WORKING_DIR = Path.cwd() # cwd() = current work directory
    caracteristic_impedance: int = 50
    s1p_file_dir = WORKING_DIR.parent / S1P_DATA_DIR
    
    # https://realpython.com/list-comprehension-python/
    s1p_files = (s1p_file_dir / f'AutoSave{n}.s1p' for n in range(1, 3)) # vector using list comprehension
    
    #Ploteo la carta de smith para todos los archivos
    for file in s1p_files:
        print('Ploteando', file.stem)
        data = read_data(file,
                         (0, 1, 2), '\t')
        s_11_parameter = array_to_complex(data, 1, 2)
        input_impedance = reflection_coefficient_to_impedance(s_11_parameter,
                                                             caracteristic_impedance)
        plot_smith_chart(input_impedance, caracteristic_impedance,
                         WORKING_DIR, file.name)
        
    
    print(input_impedance)
    print(np.size(input_impedance))
        
if __name__ == '__main__':
    main()    
    