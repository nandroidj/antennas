import matplotlib.pyplot as pp

from pathlib import Path
from numpy import pi, arange

from plots import polar_plot
from importlib_metadata.tests import data
from files import read_data

def process_trc(save_dir):

    WORKING_DIR = Path.cwd()
    MEDICIONES = WORKING_DIR.parent/"Mediciones"
    
    files_name = [
        "plano_phi_0_medicion.TRC",
        "plano_phi_90_medicion.TRC"
    ]
    
    for fname in files_name:

        data = read_data(MEDICIONES/fname, ',')

        OFFSET = 216
        gain = [float(x[0]) for x in data[OFFSET:]]
    
        maxG = max(gain)
        gain = [x - maxG for x in gain]
    
        step = 2*pi / len(gain)
        theta = arange(0, 2*pi, step)
    
        polar_plot(theta, gain, "nop")

if __name__ == '__main__':
    process_trc("nop")
