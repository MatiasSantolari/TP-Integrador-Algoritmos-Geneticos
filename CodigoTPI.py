import random
from math import log

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# definicion de variables globales
probabilidadCrossover = 0.75
probabilidadMutacion = 0.05
#la direccion del viento la voy a considerar constante y que recorra de OESTE a ESTE
viento = 7 #en metros/segundos
potencia = 164 #en Kw

#variables globales necesarias para el efecto estela
const_proporcionalidad = 1 #(TIENE QUE SER UN VALOR MAYOR E IGUAL A 1 Y MENOR A 4)
radio_turbina = 25 #en metros
radio_estela = radio_turbina * const_proporcionalidad

#variables globales necesarias para la potencia afectada por la estela
coef_induccion_axial = 1/3 # este seria el ideal
z= 46 # Altura mínima de la góndola : 46 metros
z_inicial = 0.0024 # la rugosidad del terreno. El cual corresponde al factor de rugosidad del tipo de terreno “campo abierto con superficie lisa”
coef_arrastre = 1/(2 * log(z/z_inicial))
dist_entre_turbinas = 4 * radio_turbina

"""el parque es una matriz de 10x10 donde cada elemento de la matriz es un espacio de 100 metros cuadrados.
entonces como la distancia entre turbinas es de 100 metros verá que en la funcObj la estela solamente es aplicadas
a un aerogenerador si tiene a una casilla de distancia a otro aerogenerador o obstaculo."""


def crearCromosoma(): #crea la matriz bidimensional binaria pero solo se asigna 0 (se piensa que es el terreno sin ningun aerogenerador)
    matrizCromo=[]
    cromosoma = []
    for t in range(10): #cantidad de columnas
        cromosoma.append(0)
    for g in range(10):
        matrizCromo.append(cromosoma)
    return matrizCromo

def asignarObstaculos(matriz, i): #maximo de 20 espacios de terreno ocupado
                                    #el numero 2 signifca que hay un obstaculo
    fila = []    
    fila = list(matriz[i])
    for t in range(len(fila)):
        fila[t] = 2
    fila = tuple(fila)
    matriz[i] = fila
    return matriz    


def asginarAerogeneardor(matrizCromo):
    matrizA = []
    cont = 0
    i = 0
    j = 0
    for i in range(len(matrizCromo)):
        for j in range(len(matrizCromo[i])):
            if (matrizCromo[i][j] == 2): 
                pass
            else:
                binario = random.randint(0, 1)
                if binario == 1:
                    cont += 1

                    if cont < 26:
                        matrizCromo[i][j] = binario
                    else:
                        matrizCromo[i][j] = 0
                else: matrizCromo[i][j] = binario
        a=tuple(matrizCromo[i])
        matrizA.append(a)
    return matrizA


# funcion objetivo f(cromosoma) donde cromosoma es el cromosoma que se pasa como parámetro
def CalcularfuncObj(cromosoma):
    #el calculo es el siguiente:
    """El cromosoma representa al parque eolico, cada gen representa un espacio de dicho parque
       que puede contener o no un aerogenerador.
       Se procede a hacer una sumatoria de potencias por cada sector del parque (osea cada gen del
       cromosoma)
            -si el gen es 0 o 2, entonces la potencia es nula
            -si el gen es 1 pero no lo afecta la estela, entonces la potencia se saca con la formular
             de la potencia (por el momento solo usaremos la constante potencia)
            -si el gen es 1 pero lo afecta la estela, entonces le aplicaremos otra formula"""
    total=0
    i=0
    j=0
    for i in range(len(cromosoma)):
        for j in range(len(cromosoma[i])):
            if (cromosoma[i][j] == 2) or (cromosoma[i][j] == 0):
                pass
            else:
                if (cromosoma[i][j] == 1) and ((cromosoma[i][j-1] == 1) or (cromosoma[i][j-1] == 2)):
                    #significa que se aplica la estela
                    p = viento * (1 - ((2 * coef_induccion_axial)/(1 + coef_arrastre * (dist_entre_turbinas/radio_estela)) ** 2))
                else:
                    p = potencia
                total = total + p
    return total

def calcularfuncObjFila(fila):
    total = 0
    i = 0
    for i in range(len(fila)):
        if (fila[i] == 2) or (fila[i] == 0):
            pass
        else:
            if (fila[i] == 1) and ((fila[i-1] == 1) or (fila[i-1] == 2)):
                # significa que se aplica la estela
                p = viento * (1 - ((2 * coef_induccion_axial) / (1 + coef_arrastre * (dist_entre_turbinas / radio_estela)) ** 2))
            else:
                p = potencia
            total = total + p
    return total

def fitness(x, subLista) -> float: #x es el valor de la funcion objetivo de un solo cromosoma
    return x / sum(subLista)

def aplicarFitness(subLista): #Aca sublista es listaFunObj que es la lista que contiene los valores en formato entero de la funcion objetivo de cada cromosoma
    listaFit = []
    for m in subLista:
        f = fitness(m, subLista) #m contiene el valor entero en la posicion de subLista
        listaFit.append(f) #listaFit es una lista con los valores de la fitness de cada cromosoma en forma flotante(ya que lo que retorna a funcion fitness es el valor en flotante)
    return listaFit  # retorna una lista de los valores de la funcion Fitness aplicadas a los cromosomas en formato flotante


# -----------------------------------------------------------------------------------------------------------
# a Aca se desarrolla el elitismo

def elitismo(poblacion, listaFitness):
    listaFit = listaFitness.copy()
    cromosomasSeleccionados = []
    for d in range(2):
        fitMax = max(listaFit)

        indice = listaFit.index(
            fitMax)  # Los otros elementos con el mismo valor se ignoran porque ya ha encontrado una coincidencia dentro de la lista
        cromosomasSeleccionados.append(poblacion[indice])
        listaFit[indice] = 0
    return cromosomasSeleccionados


# -------------------------------------------------------------------------------------------------

def partRuleta(listaFitness):  # se calcula el porcentaje de cada cromosoma y se le asigna
# un arco de circunferencia proporcional a su fitness. porc
# El parametro es la listaFitness que es uan lista con los valores en formatO FLOTANTE de la funcion fitness aplicada a cada cromosoma
    i = 0
    listaPorcentajeFitness = []
    for b in range(len(listaFitness)):
        den = sum(listaFitness)
        nu = round((listaFitness[i] / den) * 100, 2)
        listaPorcentajeFitness.append(nu)
        i += 1
    return listaPorcentajeFitness  # listaProcentajeFitness es una lista que va a tener los porcentajes en formato FLOTANTE de cada cromosoma segun su valor de la funcion fitness


def seleccionRuleta(ruleta, posiciones,poblacion):  # ruleta es la lista de valores ENTEROS de los porcentajes de los cromosomas segun su funcion fitness


    # posiciones es int(sum(ruleta)) que seria el valor ENTERO de la suma de los valores de la lista ruleta.
    # poblacion es listaPoblacionInicialCadena que es la lista de los cromosomas en digitos binarios en formato STRING

    ruletaDefinitiva = []  # es la lista de 100 posiciones en donde a cada posicion de esta lista se le asigna el cromosoma en formato STRING en la posicion i de la lista poblacion
    padres = []  # es la lista con los cromosomas en formato STRING que fueron seleccionados en la lista ruletaDefinitiva, que serian los padres
    for i in range(50):
        for j in range(ruleta[i]):
            ruletaDefinitiva.append(poblacion[i])  # el tamaño de ruletaDefinitiva es posiciones->int(suma(ruleta))
    for k in range(50):
        a = random.randint(0,
                           posiciones - 1)  # genera un numero entero entre 0 y posiciones (que seria 100 aprox). Seria la "Tirada de la bolita en la ruleta"
        padres.append(ruletaDefinitiva[
                          a])  # se agrega en padres el cromosoma en formato STRING en la lista ruletaDefinitiva en la posicion elegida aleatoriamente. Seria "El lugar donde cayo la bola al girar la ruleta"
    return padres  # es la lista con los cromosomas en formato STRING que fueron seleccionados en la lista ruletaDefinitiva al girarla 10 veces, ya que los padres deben ser 10


def seleccionCrossover(cromo1,cromo2):  # cromo 1 y cromo 2 van a tener c/u el cromosoma en formato ENTERO donde cada posicion es un gen binario ENTERO y cromosoma es un padre (ya convertido a ENTERO) de la listaPadres

    a = random.uniform(0, 1)  # La función random.uniform devuelve un número real entre 0 y 1
    if (a <= probabilidadCrossover):
        #En hijo1 se aplicara crosover por fila
        hijo1 = []
        i=0
        for i in range(len(cromo1)):
            cromo1[i] = list(cromo1[i])
            cromo2[i] = list(cromo2[i])

            potenciaFila1 = calcularfuncObjFila(cromo1[i])
            potenciaFila2 = calcularfuncObjFila(cromo2[i])
            if (potenciaFila1 == potenciaFila2):
                hijo1.append(cromo1[i])
            if (potenciaFila2 < potenciaFila1):
                hijo1.append(cromo1[i])
            if (potenciaFila1 < potenciaFila2):
                hijo1.append(cromo2[i])
        #En hijo2 se aplicara crosover por columna
        """primero voy a realizar la transpuesta de ambos padres, para asi usar la misma logica de las filas
        pero con las columnas, que ahora por ser una matriz compuesta, seran filas"""
        cromo1_Transpuesta = (np.transpose(cromo1)).tolist()
        cromo2_Transpuesta = (np.transpose(cromo2)).tolist()
        hijo2 = []
        i=0
        for i in range(len(cromo1)):
            potenciaFila1 = calcularfuncObjFila(cromo1_Transpuesta[i])
            potenciaFila2 = calcularfuncObjFila(cromo2_Transpuesta[i])
            if potenciaFila1 == potenciaFila2:
                hijo2.append(cromo1_Transpuesta[i])
            if potenciaFila2 < potenciaFila1:
                hijo2.append(cromo1_Transpuesta[i])
            if potenciaFila1 < potenciaFila2:
                hijo2.append(cromo2_Transpuesta[i])
        hijo2 = (np.transpose(hijo2)).tolist()

        if verificarCantAerogeneradores(hijo1):
            hijo1 = cromo1.copy()
        if verificarCantAerogeneradores(hijo2):
            hijo2 = cromo2.copy()
    else:
        hijo1 = cromo1.copy()
        hijo2 = cromo2.copy()
    return hijo1, hijo2


def verificarCantAerogeneradores(cromosoma):
    cont = 0
    for m in cromosoma:
        aerogeneradoresPorFila = m.count(1)
        cont += aerogeneradoresPorFila
    if cont > 25:
        return True
    else:
        return False

def mutacion(cromo1): #le paso el cromosoma despues de haber con el croosover (puede que no se haya aplicado) y cromo es una cromosoma que a la vez es una lista de genes donde c/gen es un ENTERO binario
    cromoLista = []
    i = 0
    for i in cromo1:
        c = list(i)
        cromoLista.append(c)
    d = random.uniform(0, 1)
    if d <= probabilidadMutacion:
        k = random.randint(0, 9)
        j = random.randint(0, 9)
        if cromoLista[k][j] == 0:
            cromoLista[k][j] = 1
        if cromoLista[k][j] == 1:
            cromoLista[k][j] = 0
    cromito = tuple(cromoLista)
    return cromito #cromo1 es un cromosoma, que a la vez es una lista de genes donde c/gen es un ENTERO binario

# se tiene que simular un sector fijo para poner establecimiento necesario para que funcione los aerogeneradores


"""#####################################
   #####################################
   #####################################
   Funciones que utilizare exclusivamente para generar datos que utilizare para mostrar en tablas y graficos
   usando pandas y matplotlib, para obtener y visualizar mayor cantidad de informacion de los resultados 
   obtenidos
   #####################################
   #####################################
   #####################################"""

def suma(lista):  # suma todos los valores de la funcion objetivo de cada cromosoma
    cont = 0
    for u in range(len(lista)):
        cont += lista[u]
    return cont


def promedio(lista):  # me devuelve el promedio de la listaFunjObj que es la lista que contiene los valores en formato ENTERO de la funcion objetivo de cada cromosoma
                        # ( mas adelante tambien se trabaja con la lista de la funcion fitness que es uan lista con los valores FLOTANTES de la funcion fitness de cada cromosoma)
    suma = 0
    for u in range(len(lista)):
        suma += lista[u] #suma tiene el valor a sumar todos los valores
    promedio = suma / len(lista)
    return promedio #promedio vuelve como un dato en formato FLOTANTE (ya sea que se trabajo con listaFunObj como listaFitness)


def maximo(lista):  # devuelve el valor maximo de la lista funcion objetivo (y mas adelante tambien se trabaja con la lista de la funcion fitness) en formato FLOTANTE
                    # ( mas adelante tambien se trabaja con la lista de la funcion fitness y lo que retorna tambien es un valor FLOTANTE)
    return max(lista)

def minimo(lista): # devuelve el valor minimo de la lista funcion objetivo en formato FLOTANTE
                    # ( mas adelante tambien se trabaja con la lista de la funcion fitness y lo que retorna en un valor FLOTANTE)
    return min(lista)

def cromoMaximo(listaPoblacion, maxobj, listaPotencias):
    
    nroIteracion = 0

    for j in listaPotencias:        #buscamos la posición de la potencia máxima, para así poder acceder al cromosoma más exitoso
        if j == maxobj:
            pos = nroIteracion
        nroIteracion = nroIteracion + 1
    
    valor = listaPoblacion[pos] 
    return valor #valor contiene el cromosoma en formato ENTERO con mayor valor de la funcion objetivo

#Funciones para graficar:
def graficarFitness(min, max, prom):
    plt.style.use('default')
    plt.plot(min, label='Minimo Fitness')
    plt.plot(max, label='Maximo Fitness')
    plt.plot(prom, label='Promedio Fitness')
    plt.legend()
    plt.title('Fitness')
    plt.xlabel('Generaciones')
    plt.grid(True)
    plt.show()


def graficarObj(min, max, prom):
    plt.style.use('default')
    plt.plot(min, label='Minima Funcion Objetivo')
    plt.plot(max, label='Maxima Funcion Objetivo')
    plt.plot(prom, label='Promedio Funcion Objetivo')
    plt.legend()
    plt.title('Funcion Objetivo')
    plt.xlabel('Generaciones')
    plt.grid(True)
    plt.show()

def graficarTodo(minF, maxF, promF, minO, maxO, promO):
    plt.style.use('default')
    plt.plot(minF, label='Minimo Fitness')
    plt.plot(maxF, label='Maximo Fitness')
    plt.plot(promF, label='Promedio Fitness')
    plt.plot(minO, label='Minima Funcion Objetivo')
    plt.plot(maxO, label='Maxima Funcion Objetivo')
    plt.plot(promO, label='Promedio Funcion Objetivo')
    plt.legend()
    plt.title('Fitness + Funcion Objetivo')
    plt.xlabel('Generaciones')
    plt.grid(True)
    plt.show()

"""#####################################
   #####################################
   #####################################
   Fin seccion de funciones para pandas y matplotlib
   #####################################
   #####################################
   #####################################"""



def ejecutarPrograma(poblacion, iteracion):
    # lista de valores de potencias de cada parque eolico generado
    listaPotencias = []
    for i in poblacion:
        potencia_parque = CalcularfuncObj(i)
        listaPotencias.append(potencia_parque)


    # aplico fitness a dichas potencias
    listaFitness = aplicarFitness(listaPotencias)

    maxiObj = maximo(
        listaPotencias)  # retorna el valor maximo de la lista que tiene los valores de la funcion objetivo de cada cromosoma en formato FLOTANTE
    cromosomaMaximo = cromoMaximo(poblacion, maxiObj, listaPotencias)
    miniObj = minimo(
        listaPotencias)  # retorna el valor minimo de la lista que tiene los valores de la funcion objetivo de cada cromosoma en formato FLOTANTE
    promeObj = promedio(
        listaPotencias)  # retorna el promedio de la lista que tiene los valores de la funcion objetivo de cada cromosoma en formato FLOTANTE
    maxiFit = maximo(
        listaFitness)  # retorna el valor maximo de la lista que tiene los valores de la funcion fitness de cada cromosoma en formato FLOTANTE
    miniFit = minimo(listaFitness)
    promeFit = promedio(listaFitness)
    #

    # Guardamos maxiObj, miniObj, promeObj, maxiFit, miniFit, promeFit sus respectivas listas
    listaMinimosFit.append(miniFit)
    listaMaximosFit.append(maxiFit)
    listaPromFit.append(promeFit)
    listaMinimosObj.append(miniObj)
    listaMaximosObj.append(maxiObj)
    listaPromObj.append(promeObj)
    listaMaxCromo.append(cromosomaMaximo)

    print('Datos de la Generacion nro: ', iteracion)
    tabla = pd.DataFrame(
        {'pobl': poblacion, 'F obj': listaPotencias, 'Fitness': listaFitness})
    print(tabla)
    print(cromosomaMaximo, ' ', maxiObj, ' ', miniObj, ' ', promeObj, ' ', maxiFit, '', miniFit, ' ', promeFit)

    # calcular porcentajes que van a tener cada parque en la ruleta de 100 pocisiones
    listaPorcentajesRuleta = partRuleta(listaFitness)

    ruleta = []  # lista de los valores en formato ENTERO de los porcentajes redondeados de la funcion fitness
    for i in partRuleta(
            listaFitness):  # esta funcion trae una lista que va a tener los porcentajes en formato FLOTANTE de cada cromosoma segun su valor de la funcion fitness
        if i > 1:
            n = round(i,
                      0)  # n va a tener el valor en formato ENTERO redondeado del porcentaje relacionado a la funcion fitness
            ruleta.append(int(n))
        else:
            ruleta.append(1)

    listaPadres = []

    cromosomasElitismo = elitismo(poblacion, listaFitness)
    listaPadres.extend(cromosomasElitismo)

    listaPadres.extend(seleccionRuleta(ruleta, int(sum(ruleta)), poblacionInicial))

    z = 0
    i = 0
    hijo1 = 0
    hijo2 = 0
    listaSiguienteGeneracion = []
    for i in range(25):  # se repite 25 veces xq hay 25 pares de cromosomas padres para aplicar el crossover
        c1 = [x for x in listaPadres[
            z]]  # c1 es una lista en formato ENTERO donde cada posicion contiene un gen, es decir c1 es un cromosoma padre
        c2 = [x for x in listaPadres[
            z + 1]]  # c2 es una lista en formato ENTERO donde cada posicion contiene un gen, es decir c2 es un cromosoma padre
        hijo1, hijo2 = seleccionCrossover(c1, c2)  # hijo1 y hijo2 son listas de Enteros donde cada posicion es un gen entero. hijo1 y hijo2 son cromosoma
        hijo1 = mutacion(hijo1)
        hijo2 = mutacion(hijo2)
        z += 2  # con la variable z me ubico a cada par de posicion en el arreglo padre
        listaSiguienteGeneracion.append(hijo1)
        listaSiguienteGeneracion.append(hijo2)

    return listaSiguienteGeneracion



#Programa Principal

listaMinimosFit = []
listaMaximosFit = []
listaPromFit = []
listaMinimosObj = []
listaMaximosObj = []
listaPromObj = []
listaMaxCromo = []


#poblacion incial
poblacionInicial = []
matriz = []

matriz.extend(crearCromosoma())
matriz = asignarObstaculos(matriz, 0)
matriz = asignarObstaculos(matriz, 9)
for i in range(50):
    matrizAerogeneradores = []
    matrizAerogeneradores.extend(asginarAerogeneardor(matriz))

    poblacionInicial.append(matrizAerogeneradores)

i = 0
listaSiguienteGeneracion = []
listaSiguienteGeneracion.extend(ejecutarPrograma(poblacionInicial, i))
for l in range(1, 200):
    listaSiguienteGeneracion = ejecutarPrograma(listaSiguienteGeneracion, l)

tablaMinFit = pd.DataFrame({'Min Fitness': listaMinimosFit})
tablaMaxFit = pd.DataFrame({'Max Fitness': listaMaximosFit})
tablaProbFit = pd.DataFrame({'Prom Fitness': listaPromFit})

tablaMinObj = pd.DataFrame({'Min Obj': listaMinimosObj})
tablaMaxObj = pd.DataFrame({'Max Obj': listaMaximosObj})
tablaProbObj = pd.DataFrame({'Prom Obj': listaPromObj})

max = 0
nroIteracion = 0
for k in listaMaximosObj:
    if k > max:
        max = k
        nroGeneracion = nroIteracion
    nroIteracion = nroIteracion + 1

print('\nPoblacion inicial FO MAX: ', listaMaximosObj[0])
print('Máximo F. objetivo: ', max)
print('Generacion con máximo objetivo: ', nroGeneracion)
print('Cromosoma más óptimo: ', listaMaxCromo[nroGeneracion])

print('\nParque eólico más óptimo:\n')
for m in listaMaxCromo[nroGeneracion]:
        print(m)


graficarFitness(tablaMinFit, tablaMaxFit, tablaProbFit)
graficarObj(tablaMinObj, tablaMaxObj, tablaProbObj)
graficarTodo(tablaMinFit, tablaMaxFit, tablaProbFit, tablaMinObj, tablaMaxObj, tablaProbObj)




