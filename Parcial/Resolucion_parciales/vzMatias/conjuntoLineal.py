from numpy import cos, sin, pi, linspace, amax, gradient
from matplotlib import pyplot as plt
import random

def main():
    
    COLORS = ['m', 'r', 'b', 'g']
    ANGULOS = [0, pi/4, pi/2, pi, pi*3/2]

    alfa = random.choice(ANGULOS)
    d = 1/2
    N = 4
    beta = 2*pi
    alfa = pi/2

    if alfa == 0:
        print("Broad side")
        ## El máximo esta en phi = 90Grados
        ## psi = 0 -> Máximo del diagrama -> cos(phi) = -alfa / (beta*d) 
        ## Si quiero el máximo en phi = 90Grados -> alfa = 0
    elif alfa ==  beta*d:
        print("Endfire")
        ## El máximo va a estar en phi = 0Grados
        ## Si quiero el máximo en phi = 0Grados -> alfa = +- beta * d

    phi = linspace(0, 2*pi, 10000);
    psi = beta*d* cos(phi) + alfa 

    ######## Array factor del conjunto ###########
    fun = lambda x: 1/N * sin(N*x/2) / sin(x/2)
    array_factor = [abs(fun(x)) if x != 0 else 1 for x in psi]
    ## Esta es una función simétrica periódica 

    ## Ancho lóbulo principal = 4*pi / N
    ## Ancho lóbulo secundarios = 2*pi / N

    ####### SLL Side Lobe Level ##################
    ## SLL = maxLobulo secundario / maxLobuloPrincipal
    
    #TODO: buscar el máximo principal y moverse 3pi/N 
    # Luego hacer 20*log10(SLL)

    ####### Calcular defasaje #################
    # En el máximo psi = 0
    # cos(phi) = -alfa / (beta * d)
    # phi = lo que quieras -> obtengo alfa
    # alfa = cos(phi) * beta * d    
    
    #### Campo lejano ##########################
    # D -> Dimensión de la antena
    # Un dipolo es corto cuanado -> L < lambda  / 10 
    # D \approx lambda/2
    # R \approx (2D^{2}/\label)
    
    ###### Potencia recibida Wr mediante ecuación de friss
    
    ################ POLARES ################################ 
    fig = plt.figure()
    plt.polar(phi, array_factor)
    ######################### PLOTS #########################
    fig = plt.figure()
    plt.plot(psi/pi, array_factor, linewidth=2,
            color=random.choice(COLORS), label=fr'$\alpha=${alfa/pi}$\pi$')
    plt.xlabel(r'[x$\pi$]')
    plt.grid('minor')
    plt.legend()
    ###### SHOW PLOTS ###### 
    plt.show()

    """
    Cambiar alpha te mueve el diagrama de lugar
    Aumentar N te aumentan los lóbulos secundarios
    Bajar N te baja los lóbulos
    """

if __name__ == '__main__':
    main()
