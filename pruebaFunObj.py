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
print(hijo)







