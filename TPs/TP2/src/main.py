"""
Trabajo práctico numero 2:
    Medición en antenas de WiFi
"""
import numpy as np
from pathlib import Path
from smithplot import SmithAxes
from matplotlib import pyplot as pp 

# TODO: Lectura de los archivos de medición con los distintos parámetors

def read_data(location, delimiter):
    """@brief funcion para leer data de un archivo
    @param location es la ubicacion del archivo
    @param cols tupla que indica las columnas que se quieren leer
    @param delim es el delimitador
    @return s los datos leidos
    """
    data = []

    file = open(location, 'r')

    for line in file:
        try:
            data += [line.split('\t')]
        except:
            pass

    return data

def plot_smith_chart(s_params, save_dir):
    """@brief funcion para plotear los parametros s en la carta de smith
    @param s_params lista de parametros s complejos
    @param save_dir directorio para guardar el gráfico
    """
    ## Plot
    SmithAxes.update_scParams(axes_impedance=50)
    pp.figure(figsize=(6, 6))
    ax = pp.subplot(1, 1, 1, projection='smith', grid_major_enable=True)
    pp.plot(s_params, datatype=SmithAxes.S_PARAMETER)

    # TODO: Save plot
    pp.show()    


def process_data(data):
    
    # offset on the s1p files
    OFFSET = 8

    freq = [float(x[0]) for x in data[OFFSET:]]
    # TODO: If the params are in dB transform them ?  
    if data[OFFSET-1][0].split(' ')[3] == 'DB':
        arrToComplex = lambda x: 10**(float(x[1])/10) + 1j*10**(float(x[2])/10)
    else:
        arrToComplex = lambda x: float(x[1]) + 1j*float(x[2])
    s11 = [arrToComplex(x) for x in data[OFFSET:]]

    return freq, s11


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

################################## MAIN PROGRAM ##########################################
def main():
    ####### Dictrionary
    # Map file stem to anntena 
    anntenas_t = {
        'AutoSave1': 'Biquad',
        'AutoSave2': 'Parche',
        'AutoSave3': 'Clindrica'
    }

    # Directories
    WORKING_DIR = Path.cwd()
    IMAGES = WORKING_DIR.parent/"Img"
    MEDICIONES = WORKING_DIR.parent/"Mediciones" 

    # Generator of all the AutoSaveN.s1p file
    # A generator is a lazy iterable object
    files_sp1 = (MEDICIONES/f"AutoSave{x}.s1p" for x in range(1,4))
    
    ## For every file get the data and plot it
    for location in files_sp1:
        ## Process data get s11 and freq
        data = read_data(location, '\t')
        freq, s11 =  process_data(data)
        ## Calculo de la impedancia
        zl = impedance(s11, 50)
        realPart, imagPart = get_real_imag_parts(zl)
        ## Coeficiente de reflexion
        refelxion_coef_mod_db = reflexion_coef_db(s11)
        ## Calculo de ROE
        onda_estacionaria = roe(s11)
        
        ######################dirs####################
        if not IMAGES.is_dir():
            IMAGES.mkdir()

        ANNTENA_DIR = IMAGES/f"{anntenas_t[location.stem]}"
    
        if not ANNTENA_DIR.is_dir():
            ANNTENA_DIR.mkdir()
        ###############################################

        ## TODO: Hay que hacer las funciones de los Plot 
        pp.plot(freq[500:], onda_estacionaria[500:])
        pp.show()
        #plot_smith_chart(s11, "nd")


###########################
if __name__ == "__main__":
    main()
###########################


