lista1 = [["n0","n0","n0","n0","n0"], ["n1","n1","n1","n1","n1"], ["n2","n2","n2","n2","n2"], ["n3","n3","n3","n3","n3"], ["n4","n4","n4","n4","n4"]
]
lista2 = [["m0","m0","m0","m0","m0"], ["m1","m1","m1","m1","m1"], ["m2","m2","m2","m2","m2"], ["m3","m3","m3","m3","m3"], ["m4","m4","m4","m4","m4"]
]

fila = 3
columna = 2

print("lista1[:fila][:columna]: ",lista1[:columna])
print("lista2[fila:][columna:]: ",lista2[fila:][columna:])
print("lista2[:fila][:columna]: ",lista2[:fila][:columna])
print("lista1[fila:][columna:]: ",lista1[fila:][columna:])



aux1 = lista1[:fila][:columna] + lista2[fila:][columna:]
aux2 = lista2[:fila][:columna] + lista1[fila:][columna:]

print("aux 1", aux1)
print("aux 2", aux2)







