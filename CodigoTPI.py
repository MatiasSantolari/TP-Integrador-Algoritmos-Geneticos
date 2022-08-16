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




def asginarAerogeneardor(matrizCromo):
    matrizA=[]
    for i in range(len(matrizCromo)):
        for j in range(len(matrizCromo[i])):
            binario = random.randint(0,1)
            print(binario)
            matrizCromo[i][j] = binario
        print(matrizCromo[i])
        a=tuple(matrizCromo[i])
        print(a)
        matrizA.append(a)
    return matrizA
 
matriz=[]
matrizAerogeneradores =[]    
matriz.extend(crearCromosoma())
matrizAerogeneradores.extend(asginarAerogeneardor(matriz))
print(matrizAerogeneradores)

#matriz llena
print("matriz llena:")
for m in matrizAerogeneradores:
    print(m)


#for i in range(50):
    
