lista1 = [["n0","n0","n0","n0","n0"], ["n1","n1","n1","n1","n1"], ["n2","n2","n2","n2","n2"], ["n3","n3","n3","n3","n3"], ["n4","n4","n4","n4","n4"]
]
lista2 = [["m0","m0","m0","m0","m0"], ["m1","m1","m1","m1","m1"], ["m2","m2","m2","m2","m2"], ["m3","m3","m3","m3","m3"], ["m4","m4","m4","m4","m4"]
]

fila = 3
"""columna = 2

print("lista1[:fila][:columna]: ",lista1[:columna])
print("lista2[fila:][columna:]: ",lista2[fila:][columna:])
print("lista2[:fila][:columna]: ",lista2[:fila][:columna])
print("lista1[fila:][columna:]: ",lista1[fila:][columna:])



aux1 = lista1[:fila][:columna] + lista2[fila:][columna:]
aux2 = lista2[:fila][:columna] + lista1[fila:][columna:]

print("aux 1", aux1)
print("aux 2", aux2)"""



def calcularfuncObjFila(fila):
    total = 0
    i = 0
    for i in range(len(fila)):
        if (fila[i] == 2) or (fila[i] == 0):
            pass
        else:
            if (fila[i] == 1) and ((fila[i-1] == 1) or (fila[i-1] == 2)):
                # significa que se aplica la estela
                p = 0.5
            else:
                p = 1
            total = total + p
    return total


cromo1 = [[1,0,0,0],[0,0,1,1],[1,0,0,1],[0,0,0,0]]
cromo2 = [[0,0,0,0],[1,0,1,1],[0,0,0,1],[1,1,0,0]]

"""
hijo1 = []
for i in range(len(cromo1)):
    potenciaFila1 = calcularfuncObjFila(cromo1[i])
    potenciaFila2 = calcularfuncObjFila(cromo2[i])
    if (potenciaFila1 == potenciaFila2):
        hijo1.append(cromo1[i])
    if (potenciaFila2 <= potenciaFila1):
        hijo1.append(cromo1[i])
    if (potenciaFila1 <= potenciaFila2):
        hijo1.append(cromo2[i])
print(hijo1)

"""

import numpy as np
import random
"""
# hago la transpuesta del cromo 1 y del cromo 2
cromo1_Transpuesta = (np.transpose(cromo1)).tolist()
cromo2_Transpuesta = (np.transpose(cromo2)).tolist()

print(cromo1_Transpuesta)
print("----------------------------------")
print(cromo2_Transpuesta)
print("----------------------------------")
hijo2=[]
for i in range(len(cromo1)):
    potenciaFila1 = calcularfuncObjFila(cromo1_Transpuesta[i])
    potenciaFila2 = calcularfuncObjFila(cromo2_Transpuesta[i])
    if (potenciaFila1 == potenciaFila2):
        hijo2.append(cromo1_Transpuesta[i])
    if (potenciaFila2 < potenciaFila1):
        hijo2.append(cromo1_Transpuesta[i])
    if (potenciaFila1 < potenciaFila2):
        hijo2.append(cromo2_Transpuesta[i])
print("hijo2 = ",hijo2)

"""






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
    if (a <= 0.75):
        #En hijo1 se aplicara crosover por fila
        hijo1 = []
        for i in range(len(cromo1)):
            potenciaFila1 = calcularfuncObjFila(cromo1[i])
            potenciaFila2 = calcularfuncObjFila(cromo2[i])
            if (potenciaFila1 == potenciaFila2):
                hijo1.append(cromo1[i])
            if (potenciaFila2 <= potenciaFila1):
                hijo1.append(cromo1[i])
            if (potenciaFila1 <= potenciaFila2):
                hijo1.append(cromo2[i])
        #En hijo2 se aplicara crosover por columna
        """primero voy a realizar la transpuesta de ambos padres, para asi usar la misma logica de las filas
        pero con las columnas, que ahora por ser una matriz compuesta, seran filas"""
        cromo1_Transpuesta = (np.transpose(cromo1)).tolist()
        cromo2_Transpuesta = (np.transpose(cromo2)).tolist()
        hijo2 = []
        for i in range(len(cromo1)):
            potenciaFila1 = calcularfuncObjFila(cromo1_Transpuesta[i])
            potenciaFila2 = calcularfuncObjFila(cromo2_Transpuesta[i])
            if (potenciaFila1 == potenciaFila2):
                hijo2.append(cromo1_Transpuesta[i])
            if (potenciaFila2 < potenciaFila1):
                hijo2.append(cromo1_Transpuesta[i])
            if (potenciaFila1 < potenciaFila2):
                hijo2.append(cromo2_Transpuesta[i])

        return hijo1, hijo2


hijo1, hijo2 = seleccionCrossover(cromo1,cromo2)

print('hijo1: ',hijo1)
print('hijo2: ',hijo2)







