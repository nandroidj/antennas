"""
Process data
"""
import numpy as np
from pathlib import Path

from plots import plot_smith_chart,\
                  plot_roe, plot_coef_reflexion,\
                  plot_real_imag

from files import read_data

from anntena import impedance,\
                    get_real_imag_parts,\
                    reflexion_coef_db,\
                    reflexion_coef, \
                    roe 

def process_data(data):
    
    # offset on the s1p files
    OFFSET = 8

    freq = [float(x[0]) for x in data[OFFSET:]]
    # If the data set is in dB, then we have info about
    # magnitude in dB and phase in deg
    if data[OFFSET-1][0].split(' ')[3] == 'DB':
        arrToComplex = lambda x: \
                np.sqrt((10**(float(x[1])/10.0))) * \
                (np.cos(np.deg2rad(float(x[2]))) + 1j*np.sin(np.deg2rad(float(x[2]))))
    else:
        arrToComplex = lambda x: float(x[1]) + 1j*float(x[2])

    s11 = [arrToComplex(x) for x in data[OFFSET:]]

    return freq, s11

def process_s1p_files(anntenas_t, files_sp1, IMAGES):
    """
    #TODO: Doc
    """
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
        
        ###################PLOTS#######################
        print("---------------------------")
        print(f"{ANNTENA_DIR.stem.upper()} anntena")
        print("---------------------------")
        print("Ploting Smith Chart")
        plot_smith_chart(s11, ANNTENA_DIR)
        print("ploting ROE ") 
        plot_roe(onda_estacionaria,freq, ANNTENA_DIR)
        print("ploting Reflexion Coef ") 
        plot_coef_reflexion(refelxion_coef_mod_db, freq, ANNTENA_DIR)
        print("ploting Real Imag Parts ") 
        plot_real_imag(realPart, imagPart, freq, ANNTENA_DIR)




