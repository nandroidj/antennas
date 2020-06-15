"""
Plots functions
"""

import numpy as np
from pathlib import Path
from smithplot import SmithAxes
from matplotlib import pyplot as pp 


def plot_smith_chart(s_params, save_dir):
    """@brief funcion para plotear los parametros s en la carta de smith
    @param s_params lista de parametros s complejos
    @param save_dir directorio para guardar el gráfico
    """
    ## Plot
    SmithAxes.update_scParams(axes_impedance=50)
    fig = pp.figure(figsize=(6, 6))
    ax = pp.subplot(1, 1, 1, projection='smith', grid_major_enable=True)
    pp.plot(s_params, datatype=SmithAxes.S_PARAMETER)

    fig.savefig(save_dir / 'smithChart.png',
                bbox_inches='tight', dpi=150)


def plot_roe(roe, freq, save_dir):

    fig = pp.figure()
    pp.plot(freq, roe, linewidth=2, color='r')
    pp.ylim((0, 9))
    pp.grid()
    pp.xlabel(r'f[Hz]')
    fig.savefig(save_dir / 'roe.png',
            bbox_inches='tight', dpi=150)

def plot_coef_reflexion(coef, freq, save_dir):
    fig = pp.figure()
    pp.plot(freq, coef, linewidth=2, color='m')
    pp.grid()
    pp.xlabel(r'f[Hz]')
    fig.savefig(save_dir / 'ceofReflexion.png', 
            bbox_inches='tight', dpi=150)
    
def plot_real_imag(realPart, imagPart, freq, save_dir):
    fig = pp.figure()
    pp.plot(freq, realPart, linewidth=2, color='b')
    pp.plot(freq, imagPart, linewidth=2, color='m')
    pp.xlabel(r'f[Hz]')
    pp.grid()
    fig.savefig(save_dir / 'realImag.png',
            bbox_inches='tight', dpi=150)
