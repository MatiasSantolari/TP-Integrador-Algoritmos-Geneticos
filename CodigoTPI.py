#tpi 
#Dudas
import random
from math import log

# definicion de variables globales
probabilidadCrossover = 0.75
probabilidadMutacion = 0.05
#la direccion del viento la voy a considerar constante y que recorra de OESTE a ESTE
viento = 7 #en metros/segundos
potencia = 164 #en Kw, no me acuerdo la formula que uso eric, cuando me la pase la coloco aca, pero por ahora le pongo una constante para seguir programando

#variables globales necesarias para el efecto estelar
const_proporcionalidad = 0.5 #NO SE QUE ES, LE PUSE 0.5 PARA QUE HICIERA EL CALCULO
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
