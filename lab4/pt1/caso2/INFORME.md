
***
# RED
### Redes y Sistemas Distribuídos 2024
**Autores:** Nahuel Fernandez, Ignacio Gomez, Luciano Rojo.

#### Introducción

#### PARTE 1: Análisis
Esta parte se divide en dos casos de testeo, que difieren en la cantidad de nodos que generarán tráfico hacia el nodo 5.
En ambos casos obtendremos y compararemos las métricas: **paquetes generados, tamaños de buffer, paquetes entregados, delay y paquetes perdidos.**

**CASO 1:** 
Se ejecuta el modelo con las fuentes de tráfico configuradas como node[0] y node [2] transmitiendo datos a node[5]. Notar que node[0] envia paquetes en sentido horario en el anillo, mientras que node[2] lo hace en sentido antihorario.
Una vez completada la simulación, obtenemos instancias de las métricas anteriormente mencionadas.

(Fotos de las métricas en órden)

Luego de analizar los gráficos, no es muy difícil notar que se produce una congestión de aproximadamente el 50%, ya que tanto node[0] como node[2] están generando alrededor de 200 paquetes cada uno, y node[5] solo envió 200, dejando una pérdida de aprox. 200 paquetes.
La demora (delay) desde que un paquete es generado hasta que es enviado presenta una curva casi lineal con irregularidades generadas por el distinto tiempo que le insume a cada paquete ser enviado según la congestion presente.
La congestión es principalmente producida por una sobrepoblación de paquetes en el búffer del node[0] que no pueden avanzar a node[1] porque el enlace está saturado.

**CASO 2:** 
Se ejecuta el modelo con las fuentes de tráfico configuradas como todos los nodos excepto node[5] transmitiendo datos a node[5]. Todos los nodos generadores transmiten los paquetes en sentido horario hasta node[5], lo que inevitablemente producirá una mayor demora en el envío de los paquetes generados en los nodos 1, 2, 3, y 4.
Una vez completada la simulación, obtenemos instancias de las métricas anteriormente mencionadas.

(Fotos de las métricas en órden)

Tenemos que ahora hay 7 nodos generando, en promedio, 170 paquetes cada uno. Todos estos paquetes circulan por el anillo en sentido horario hasta node[5] donde son enviados a la capa de aplicación.
En esta última etapa, notamos que la cantidad enviada sigue siendo la máxima soportada por node[5], que es de 200 paquetes. Vemos que la pérdida de paquetes se ha incrementado notablemente y alcanza un valor aproximado del 83%.
Otra métrica que resalta a la vista es el delay, que ahora presenta una amplitud bastante errática a lo largo de la misma cantidad de tiempo.
Esto último se dá debido a la llegada intercalada de paquetes generados en los nodos 0, 6 y 7 con aquellos generados en los nodos 1, 2, 3 y 4. Esta llegada intercalada produce que se registren delays que difieren mucho entre si, ya que los del primer grupo llegan considerablemente antes que los generados por el segundo, que deben atravesar todo el anillo para llegar a node[5].
Este caso presenta además una nueva "métrica" a considerar, que es el valor mínimo de interArrivalTime tal que la pérdida de paquetes cae dentro de un margen razonable al que llamaremos "umbral de estabilidad", y conoceremos al concepto de "estabilidad" como la ausencia o ínfima presencia de paquetes perdidos en los resultados.
Tenemos que el intervalo según el cual se generarán paquetes nuevos de manera pararela en cada nodo generador está determinado por la línea: 
Network.node[{generadores}].app.interArrivalTime = exponential(x)
Esta linea configura a los nodos del conjunto "Generadores" para que simulen la llegada de paquetes cada un intervalo de tiempo promedio determinado por la distribución exponencial de parámetro x a la cual está asignada.
Como la capacidad de envío de node[5] no cambia, la única forma que tenemos hasta ahora de reducir la pérdida es reducir la tasa de generación de paquetes. Retomando los datos calculados antes, tenemos que reducir la tasa de generación aproximadamente en un 80%, lo que nos deja con un valor de x igual a 4.5 en la línea de código anterior.
 