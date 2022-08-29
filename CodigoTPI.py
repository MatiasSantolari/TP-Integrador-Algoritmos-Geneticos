#tpi 
#Dudas
import random 

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
                    if cont < 26:
                        matrizCromo[i][j] = binario
                    else:
                        matrizCromo[i][j] = 0
                else: matrizCromo[i][j] = binario
        print(matrizCromo[i])
        a=tuple(matrizCromo[i])
        print(a)
        matrizA.append(a)
    return matrizA


def CalcularfuncObj():

 




# se tiene que simular un sector fijo para poner establecimiento necesario para que funcione los aerogeneradores


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



for i in poblacionInicial:
    for j in i:
        print(j)
    print("---------------------------")
