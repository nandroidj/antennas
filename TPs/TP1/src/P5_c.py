'''
Created on May 31, 2020

@author: nandroid

A partir de la siguiente ecuación que corresponde a la impedancia de entrada que se ve
desde el plano de referencia hacia la derecha (es decir, incluye la lı́nea y la carga):

        Z (z) = Zo * (ZL + jZotg (βL))/(Zo + jZLtg (βL))

Podemos decir que si la carga es el cortocircuito del kit con el que trabajamos (cabe resaltar
que el kit se utiliza para lograr un cortocircuito y un circuito abierto precisos) entonces ZL es 0 y:

    Z (incc) = Zo * (jZo tg (βL))/Zo

Siendo entonces:

    Z (incc) = jZo tg (βL)

Por otro lado, si hacemos lo mismo teniendo la carga en circuito abierto, entonces:

    Z (inca) = Zo / jtg (βL)

Y ası multiplicando Z (incc) * Z (inca) da Zo^2 , por lo cual:

    sqrt( Z (incc) .Z (inca) ) = Zo

Este método de obtención de la impedancia caracterı́stica va a dejar de valer cuando las
frecuencias en las que se está midiendo se acercan a los valores extremos de la carta de Smith
iguales a Z=0 y Z=∞, ya que en esos puntos se tienen indeterminaciones.
De esta manera se obtuvo lo siguiente, donde se pueden ver claramente las indeterminacio-
nes en los tramos que se sale del valor promedio y se escapaba hacia infinito:
'''

