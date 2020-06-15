import matplotlib.pyplot as pp

from pathlib import Path
from importlib_metadata.tests import data

def main():
    
    OFFSET = 216

    WORKING_DIR = Path.cwd()
    MEDICIONES = WORKING_DIR.parent/"Mediciones"
    
    data = []
    file = open(MEDICIONES/"plano_phi_0_medicion.TRC", 'r')
    
    for line in file:
        try:
            data += [line.split(',')]
        except:
            pass
    
    parameter = [float(x[0]) for x in data[OFFSET:]]

    pp.plot(parameter)
    pp.show()

    print(parameter)


if __name__ == '__main__':
    main()