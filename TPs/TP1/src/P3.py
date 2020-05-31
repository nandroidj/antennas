'''
Created on May 27, 2020

@author: nandroid

Punto 3:

Utilizar el medidor RLC para medir la capacidad C y la inductancia L por unidad de longitud de la
linea, y con estos parámetros calcular la impedancia caracterıstica Z_0 , la velocidad de propagación v y
la permitividad relativa epsilon_r . 

Explicar el modelo empleado en este método de medición y presentar los resultados en un cuadro comparativo.
    
    RLC Calculator
    https://www.everythingrf.com/rf-calculators/coaxial-cable-calculator
    
    Capacitance of Coaxial Cable
    https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Book%3A_Electromagnetics_I_(Ellingson)/05%3A_Electrostatics/5.24%3A_Capacitance_of_a_Coaxial_Structure
    
    Inductance of Coaxial Cable
    https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Book%3A_Electromagnetics_I_(Ellingson)/07%3A_Magnetostatics/7.14%3A_Inductance_of_a_Coaxial_Structure

    -------------------------------------------------------------------------------------------------------------
    HABLAR DE COMO FUNCIONA EL MEDIDOR RLC!
    
    https://www.hioki.com/en/products/listUse/?category=10
    
    https://www.electronics-tutorials.ws/accircuits/ac-inductance.html

    Dado que las lı́neas de transmisión que están siendo estudiadas son de tipo coaxial, enton-
    ces responden a una geometrı́a que consiste en un conductor cilı́ndrico de cobre, rodeado por
    un cilindro de material dieléctrico (con un r ) y luego una capa de cobre que rodea toda la
    estructura. De esta forma, usando el modelo cuasi-estático de cuadripolo para cada tramo dz
    de la linea, se pueden calcular los parámetros circuitales del modelo, teniéndose:

        Ecuaciones de C y L
        
    Para medir la capacitancia se conectó la lı́nea al RLC dejando en circuito abierto la misma,
    mientras que para medir la inductancia se cortocircuitó el extremo de la lı́nea. Los datos ob-
    tenidos están relacionados con las longitudes de las lı́neas que se midieron, por lo cual se debe
    ajustar estas mediciones a las unidades de [Hy/m] o [F/m] para poder encontrar los parámetros
    que siguen:

    Vale resaltar que para el calculo de epsilon_r se consideró μr = 1
'''

