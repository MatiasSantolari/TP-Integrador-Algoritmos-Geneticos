#tpi 
#Dudas
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
potencia = 164 #en Kw, no me acuerdo la formula que uso eric, cuando me la pase la coloco aca, pero por ahora le pongo una constante para seguir programando

#variables globales necesarias para el efecto estelar
const_proporcionalidad = 1 #NO SE QUE ES, LE PUSE 1 PARA QUE HICIERA EL CALCULO (TIENE QUE SER UN VALOR MAYOR E IGUAL A 1 Y MENOR A 4)
radio_turbina = 25 #en metros
radio_estela = radio_turbina * const_proporcionalidad

#variables globales necesarias para la potencia afectada por la estela
coef_induccion_axial = 1/3 # este seria el ideal
z= 46 # Altura mínima de la góndola : 46 metros
z_inicial = 0.0024 # la rugosidad del terreno. El cual corresponde al factor de rugosidad del tipo de terreno “campo abierto con superficie lisa”
coef_arrastre = 1/(2 * log(z/z_inicial))
dist_entre_turbinas = 4 * radio_turbina



def crearCromosoma(): #crea la matriz bidimensional binaria pero solo se asigna 0 (se piensa que es el terreno sin ningun aerogenerador)
    matrizCromo=[]
    cromosoma = []
    for t in range(10): #cantidad de columnas
        #for j in range(4): # cantidad de filas
        cromosoma.append(0)
        print(cromosoma)
    for g in range(10):
        matrizCromo.append(cromosoma)
        print(matrizCromo)

    #Matriz vacia
    print("matriz:")
    for m in matrizCromo:
        print(m)
    return matrizCromo

def asignarObstaculos(matriz, i): #maximo de 20 espacios de terreno ocupado
                                    #el numero 2 signifca que hay un obstaculo
    fila = []    
    fila = list(matriz[i])
    print("fila", fila)
    for t in range(len(fila)):
        print(t)
        fila[t] = 2;
    fila = tuple(fila)
    matriz[i] = fila
    return matriz    


def asginarAerogeneardor(matrizCromo):
    matrizA = []
    cont = 0
    for i in range(len(matrizCromo)):
        for j in range(len(matrizCromo[i])):
            if (matrizCromo[i][j] == 2): 
                pass
            else:
                binario = random.randint(0, 1)
                if binario == 1:
                    cont += 1
                    print("contador actual: ", cont)

                    #contador va a regular que se de manera equitativa 1s a todas las filas mas o menos
                    #(para resolver el problema de que las ultimas 3 filas aprox no queden todas con 0s)
                    """contador = 0
                    for n in range(len(matrizCromo[i])):
                        if matrizCromo[i][n] == 1:
                            contador += 1"""
                    # fin de la logica del contador

                    print("contador actual: ", cont)
                    if cont < 26 and """contador < 4""":
                        matrizCromo[i][j] = binario
                    else:
                        matrizCromo[i][j] = 0
                else: matrizCromo[i][j] = binario
        print(matrizCromo[i])
        a=tuple(matrizCromo[i])
        print(a)
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
    print("ruleta ", ruleta)
    print("la cantidad de posiciones en la ruleta son, posiciones:", posiciones)
    print("la lista poblacion inicial cadena es: ", poblacion)
    print("el largo de lista poblacion inicial cadena es: ", len(poblacion))

    ruletaDefinitiva = []  # es la lista de 100 posiciones en donde a cada posicion de esta lista se le asigna el cromosoma en formato STRING en la posicion i de la lista poblacion
    padres = []  # es la lista con los cromosomas en formato STRING que fueron seleccionados en la lista ruletaDefinitiva, que serian los padres
    for i in range(10):
        for j in range(ruleta[i]):
            ruletaDefinitiva.append(poblacion[i])  # el tamaño de ruletaDefinitiva es posiciones->int(suma(ruleta))
    for k in range(10):
        a = random.randint(0,
                           posiciones - 1)  # genera un numero entero entre 0 y posiciones (que seria 100 aprox). Seria la "Tirada de la bolita en la ruleta"
        padres.append(ruletaDefinitiva[
                          a])  # se agrega en padres el cromosoma en formato STRING en la lista ruletaDefinitiva en la posicion elegida aleatoriamente. Seria "El lugar donde cayo la bola al girar la ruleta"
    return padres  # es la lista con los cromosomas en formato STRING que fueron seleccionados en la lista ruletaDefinitiva al girarla 10 veces, ya que los padres deben ser 10


def seleccionCrossover(cromo1,cromo2):  # cromo 1 y cromo 2 van a tener c/u el cromosoma en formato ENTERO donde cada posicion es un gen binario ENTERO y cromosoma es un padre (ya convertido a ENTERO) de la listaPadres

    """a = random.uniform(0, 1)  # La función random.uniform devuelve un número real entre 0 y 1
    if (a <= probabilidadCrossover):
        fila = random.randint(0,9)  # random.randint devuelve número entero aleatorio en el intervalo cerrado (tambien toma los limites) entre 0 y 29
        #columna = random.randint(0,9)
        aux1 = cromo1[:fila] + cromo2[fila:]  # con el [:rango] selecciona los valores de rango
        aux2 = cromo2[:fila] + cromo1[fila:]  # aca se generan los hijos es decir los padres aplicando crossover
        cromo1 = aux1  # esos hijos se guardan donde anteriormente estaban los padres
        cromo2 = aux2
    return cromo1, cromo2  # cromo 1 y cromo2 son listas que contienen valores ENTEROS donde cada valor es un gen, es decir c1 y c2 son un Cromosoma
    """
    a = random.uniform(0, 1)  # La función random.uniform devuelve un número real entre 0 y 1
    if (a <= probabilidadCrossover):
        hijo = []
        for i in range(len(cromo1)):
            potenciaFila1 = calcularfuncObjFila(cromo1[i])
            potenciaFila2 = calcularfuncObjFila(cromo2[i])
            if (potenciaFila1 == potenciaFila2):
                hijo.append(cromo1[i])
            if (potenciaFila2 <= potenciaFila1):
                hijo.append(cromo1[i])
            if (potenciaFila1 <= potenciaFila2):
                hijo.append(cromo2[i])
        return hijo

def mutacion(cromo1): #le paso el cromosoma despues de haber con el croosover (puede que no se haya aplicado) y cromo es una cromosoma que a la vez es una lista de genes donde c/gen es un ENTERO binario
    cromoLista = []
    for i in cromo1:
        c = list(i)
        cromoLista.append(c)
    print("Lista de listas del cromosoma", cromoLista)
    d = random.uniform(0, 1)
    if (d <= probabilidadMutacion):
        i = random.randint(0, 9) #determinar una posicion al azar del cromosoma entre 0 a 29 (incluyendo 0 y 29)
        j = random.randint(0, 9) #determinar una pos
        if(cromoLista[i][j] == 0):
            cromoLista[i][j]=1
        else:
            cromoLista[i][j]=0
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

def cromoMaximo(listaPoblacionInicial):
    valor = listaPoblacionInicial[9] #como esta ordenada de menor a mayor, siempre vamos a queres el cromosoma en la ultima posicion(que en esta caso es 9) que seria
                                     #el cromosoma con el valor de la funcion objetivo mas alto
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

"""
for i in poblacionInicial:
    for j in i:
        print(j)
    print("---------------------------")
"""



"""
cont = 0
for i in listaSiguienteGeneracion:
    cont = cont + 1
    print ("hijo nro ", cont, " :", i, "\n")
"""
print("#############################################################################"
      "#############################################################################"
      "#############################################################################"
      "#############################################################################"
      "#############################################################################"
      "#############################################################################"
      "#############################################################################"
      "#############################################################################")



def ejecutarPrograma(poblacion, iteracion):
    # lista de valores de potencias de cada parque eolico generado
    listaPotencias = []
    for i in poblacion:
        potencia_parque = CalcularfuncObj(i)
        listaPotencias.append(potencia_parque)

    # muestro las potencias que obtuve de cada uno de los 10 parques
    for i in listaPotencias:
        print(i)

    # aplico fitness a dichas potencias
    listaFitness = aplicarFitness(listaPotencias)

    """##############################################################
       ##############################################################
       ##############################################################"""
    maxiObj = maximo(
        listaPotencias)  # retorna el valor maximo de la lista que tiene los valores de la funcion objetivo de cada cromosoma en formato FLOTANTE
    cromosomaMaximo = cromoMaximo(poblacion)
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

    print('Datos de la Generacion nro: ', iteracion)
    tabla = pd.DataFrame(
        {'pobl': poblacion, 'F obj': listaPotencias, 'Fitness': listaFitness})
    print(tabla)
    print(cromosomaMaximo, ' ', maxiObj, ' ', miniObj, ' ', promeObj, ' ', maxiFit, '', miniFit, ' ', promeFit)

    """##############################################################
       ##############################################################
       ##############################################################"""
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
    listaPadres.extend(seleccionRuleta(ruleta, int(sum(ruleta)), poblacionInicial))
    print(listaPadres)

    z = 0
    i = 0
    hijo1 = 0
    hijo2 = 0
    listaSiguienteGeneracion = []
    for i in range(5):  # se repite 5 veces xq hay 5 pares de cromosomas padres para aplicar el crossover
        c1 = [x for x in listaPadres[
            z]]  # c1 es una lista en formato ENTERO donde cada posicion contiene un gen, es decir c1 es un cromosoma padre
        c2 = [x for x in listaPadres[
            z + 1]]  # c2 es una lista en formato ENTERO donde cada posicion contiene un gen, es decir c2 es un cromosoma padre
        hijo1, hijo2 = seleccionCrossover(c1,
                                          c2)  # hijo1 y hijo son listas de Enteros donde cada posicion es un gen entero. hijo1 y hijo2 son cromosoma
        hijo1 = mutacion(hijo1)
        hijo2 = mutacion(hijo2)
        z += 2  # con la variable z me ubico a cada par de posicion en el arreglo padre
        listaSiguienteGeneracion.append(hijo1)
        listaSiguienteGeneracion.append(hijo2)

    """
    cont = 0
    for i in listaSiguienteGeneracion:
        cont = cont + 1
        print ("hijo nro ", cont, " :", i, "\n")
    """
    print("#############################################################################"
          "#############################################################################"
          "#############################################################################"
          "#############################################################################"
          "#############################################################################"
          "#############################################################################"
          "#############################################################################"
          "#############################################################################")
    return listaSiguienteGeneracion



#Programa Principal

listaMinimosFit = []
listaMaximosFit = []
listaPromFit = []
listaMinimosObj = []
listaMaximosObj = []
listaPromObj = []


#poblacion incial
poblacionInicial = []
matriz = []

matriz.extend(crearCromosoma())
matriz = asignarObstaculos(matriz, 0)
matriz = asignarObstaculos(matriz, 9)
for i in range(10):
    matrizAerogeneradores = []
    matrizAerogeneradores.extend(asginarAerogeneardor(matriz))
    print(matrizAerogeneradores)

    # matriz llena
    print("matriz llena:")
    for m in matrizAerogeneradores:
        print(m)

    poblacionInicial.append(matrizAerogeneradores)


listaSiguienteGeneracion = []
listaSiguienteGeneracion.extend(ejecutarPrograma(poblacionInicial, i))
for i in range(9):
    listaSiguienteGeneracion = ejecutarPrograma(listaSiguienteGeneracion, i)

tablaMinFit = pd.DataFrame({'Min Fitness': listaMinimosFit})
tablaMaxFit = pd.DataFrame({'Max Fitness': listaMaximosFit})
tablaProbFit = pd.DataFrame({'Prom Fitness': listaPromFit})

tablaMinObj = pd.DataFrame({'Min Obj': listaMinimosObj})
tablaMaxObj = pd.DataFrame({'Max Obj': listaMaximosObj})
tablaProbObj = pd.DataFrame({'Prom Obj': listaPromObj})

graficarFitness(tablaMinFit, tablaMaxFit, tablaProbFit)
graficarObj(tablaMinObj, tablaMaxObj, tablaProbObj)
graficarTodo(tablaMinFit, tablaMaxFit, tablaProbFit, tablaMinObj, tablaMaxObj, tablaProbObj)




