# IFA

## Teoría


### Consideraciones Básicas

- **Antena IFA**,

  * el **brazo superior** de la antena IFA tiene la longitud de una **guia de cuarto de onda** (lambda / 4)

  * la **altura** (H) de la antena IFA debe ser una pequeña fracción de la guia de onda.


- El **feed**,

  * esta posicionado desde el plano de tierra hasta el **brazo superior**

  * se encuentra mas proximo al **shorting pin** que a la posicion *L* del **brazo superior** 


- **Ground Plane**,

  * el **ancho** de el plano de tierra debe ser al menos la longitud del brazo superior, *W_ground_plane* > L

  * la **altura** del plano de masa debe ser como minimo *lambda/4*. En caso de ser menor, el BW y la eficiencia van a **bajar**.


- La polarización de la antena es vertical y el patrón de radiación tiene forma de una dona con su eje en la dirección vertical.

- Las propiedades de radiación y la impedancia no tienen una fuerte dependencia del parámetro *H*, altura de la antena IFA.


### Análisis

El modo en el que se propaga la radiación de la antena IFA es a partir del circuito abierto que se encuentra en el extremo derecho. En el punto *l = L*, la corriente es cero y la tensión es máxima (*V = V_supply* ?). Por ello, la IFA puede ser analizada como una *half-slot antenna*.








## Modelo

![IFA](https://github.com/nandroidj/antennas/blob/master/Inverted%20F%20antenna/imgs/IFA_model.png)

|   index  |  longitud   |
|:-:|:-:|
| a  | 18.2   |
| b  |  5.4 |
| e  |  50 |
| g  |  35 |
| h  |  4.4 |
| w  |  1 |
| T  |  3 |
| *Sub_H*  | 5 |


## Consideraciones Tecnicas

1. **Brazo del alimentador**:

  - Debe estar conectado a una *guía de ondas coplanar* (CPWG) de 50 Ohm.

  - El largo del **brazo**, parámetro *h*, debe ser lo más corta posible.

  - Es recomendable que se encuentre cubierto por máscara antisoldante.

2. **Brazo corto**, debe estar conectado al plano de tierra con al menos 2 vias.

3. **Plano de Tierra**,

  - La zona debajo de la antena debe ser removido.

  - Deberia agregarse una máscara antisoldante en el plano de tierra.

  - El tamaño del plano de tierra es tan importante como las dimensiones de la antena misma.


4. **Adaptador de Impedancia**

  - El layout del adaptador (matching net?) no debería alterar la impedancia de la linea de transmisión.

  - La **T** o **pie matching net** es suficiente para todo tipo de antenas. Debe ser lo más simple posible.

 
5. **IFA**  

  - **Si cambian las dimensiones del sustrato => deben modificarse las dimensiones de la antena**

  - La **posición** de la antena es muy importante para su diseño. Ver que en el diseño se encuentra en una posición **T**.

  - La impedancia característica de la **CPWG** debe ser igual a la impedancia de entrada de la antena, `Z* = Z_0`, con la intención de mejorar las **pérdidas por retorno** en el puerto de entrada de la antena (50 Ohm).

  - No es recomendable utilizar la linea microstrip como alimentador porque puede alterar la longitud de la **efectividad electrica**.

  - Alrededor del plano de tierra deberian conectarse pequeñas vias a tierra con un diametro de 8~10 mils.

  
## Performance 

Ver páginas 18 a 21 del documento **BLE Antenna Design Guide** [ST Electronics]

  











