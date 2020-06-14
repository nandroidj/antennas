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
