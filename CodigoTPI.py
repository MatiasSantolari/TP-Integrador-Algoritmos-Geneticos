#tpi 
#Dudas
#¿Cuantos aerogeneradores hay que poner?
import random 

def crearCromosoma(): #crea la matriz bidimensional binaria pero solo se asigna 0 (se piensa que es el terreno sin ningun aerogenerador)
    matrizCromo=[]
    cromosoma = []
    for t in range(5): #cantidad de columnas
        #for j in range(4): # cantidad de filas
        cromosoma.append(0)
        print(cromosoma)
    for g in range(5):
        matrizCromo.append(cromosoma)
        print(matrizCromo)
    return matrizCromo            

def asginarAerogeneardor(matrizCromo):
    for i in range(len(matrizCromo)):
      for j in range(len(matrizCromo[i])):
          binario = random.randint(0,1)
          print(binario)
          matrizCromo[i][j] = binario
      print(matrizCromo[i])
    return matrizCromo
 
matriz=[]
matrizAerogeneradores =[]    
matriz.extend(crearCromosoma())
matrizAerogeneradores.extend(asginarAerogeneardor(matriz))
print(matrizAerogeneradores) #¿PORQUE ME MUESTRA REPETIDA 5 VECES LA ULTIMA LISTA?


#for i in range(50):
    
