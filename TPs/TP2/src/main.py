"""
Trabajo práctico numero 2:
    Medición en antenas de WiFi
"""
from pathlib import Path
from process_data import process_s1p_files   

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
    ### Process de s1p files
    # Get parameters and plots 
    process_s1p_files(anntenas_t, files_sp1, IMAGES)

###########################
if __name__ == "__main__":
    main()
###########################


