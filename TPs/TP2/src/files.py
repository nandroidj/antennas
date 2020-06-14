"""
Module for files manage
"""


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
            data += [line.split(delimiter)]
        except:
            pass

    return data





####### TESTING ###########
if __name__ == "__main__":
    pass
###########################
