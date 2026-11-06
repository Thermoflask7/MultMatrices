import time
import numpy
import random

def BruteForce (matrizA, matrizB):
    size = len(matrizA[0])
    c = [[0 for _ in range(size)] for _ in range(size)]

    start = time.perf_counter()

    for i in range(size):
        for j in range(size):
            c[i][j] = sum([matrizA[i][k] * matrizB[k][j] for k in range(size)])

    end = time.perf_counter()
    tiempo = end - start
    return (c, tiempo)



def Recursivo (matrizA, matrizB):
    start = time.perf_counter()

    def sumar_matrices(A, B):
        n = len(A)
        return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

    def pasoRecursivo (A, B):
        n = len(A)
        if n == 1:
            return [[A[0][0] * B[0][0]]]
        h = n//2

        A1 = [row[:h] for row in A[:h]]
        A2 = [row[h:] for row in A[:h]]
        A3 = [row[:h] for row in A[h:]]
        A4 = [row[h:] for row in A[h:]]

        B1 = [row[:h] for row in B[:h]]
        B2 = [row[h:] for row in B[:h]]
        B3 = [row[:h] for row in B[h:]]
        B4 = [row[h:] for row in B[h:]]

        C1 = sumar_matrices(pasoRecursivo(A1,B1), pasoRecursivo(A2,B3))
        C2 = sumar_matrices(pasoRecursivo(A1,B2), pasoRecursivo(A2,B4))
        C3 = sumar_matrices(pasoRecursivo(A3,B1), pasoRecursivo(A4,B3))
        C4 = sumar_matrices(pasoRecursivo(A3,B2), pasoRecursivo(A4,B4))

        C = [[0.0] * n for _ in range(n)]
        for i in range(h):
            for j in range(h):
                C[i][j] = C1[i][j]
                C[i][j+h] = C2[i][j]
                C[i+h][j] = C3[i][j]
                C[i+h][j+h] = C4[i][j]
        return C

    c = pasoRecursivo( matrizA, matrizB)
    tiempo = time.perf_counter() - start
    return (c, tiempo)




def Strassen (matrizA, matrizB):
    start = time.perf_counter()

    def suma(A, B):
        n = len(A)
        return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
    
    def resta(A,B):
        n = len(A)
        return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

    
    def pasoRecursivo ( A, B):
        n = len(A)

        if n == 1:
            return([[A[0][0] * B[0][0]]])
        
        h = n//2

        A1 = [row[:h] for row in A[:h]]
        A2 = [row[h:] for row in A[:h]]
        A3 = [row[:h] for row in A[h:]]
        A4 = [row[h:] for row in A[h:]]

        B1 = [row[:h] for row in B[:h]]
        B2 = [row[h:] for row in B[:h]]
        B3 = [row[:h] for row in B[h:]]
        B4 = [row[h:] for row in B[h:]]

        M1 = pasoRecursivo(suma(A1, A4), suma(B1, B4))
        M2 = pasoRecursivo(suma(A3, A4), B1)
        M3 = pasoRecursivo(A1, resta(B2, B4))
        M4 = pasoRecursivo(A4, resta(B3, B1))
        M5 = pasoRecursivo(suma(A1, A2), B4)
        M6 = pasoRecursivo(resta(A3, A1), suma(B1, B2))
        M7 = pasoRecursivo(resta(A2, A4), suma(B3, B4))

        C1 = suma(resta(suma(M1, M4), M5), M7)
        C2 = suma(M3, M5)
        C3 = suma(M2, M4)
        C4 = suma(resta(suma(M1, M3), M2), M6)

        C = [[0.0] * n for _ in range(n)]
        for i in range(h):
            for j in range(h):
                C[i][j] = C1[i][j]
                C[i][j+h] = C2[i][j]
                C[i+h][j] = C3[i][j]
                C[i+h][j+h] = C4[i][j]
        return C

    c = pasoRecursivo(matrizA, matrizB)
    tiempo = time.perf_counter() - start
    return (c, tiempo)  

def Numpy (matrizA, matrizB):
    start = time.perf_counter()
    c = numpy.matmul(matrizA, matrizB)
    tiempo = time.perf_counter() - start
    return(c, tiempo)


#Generacion de matrices

def generar_random(n, low=0, high=10):
    A = [[random.uniform(low, high) for _ in range(n)] for _ in range(n)]
    B = [[random.uniform(low, high) for _ in range(n)] for _ in range(n)]
    return A, B

def generar_identidad(n):
    A = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    B = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    return A, B

def generar_cero(n):
    A = [[0 for _ in range(n)] for _ in range(n)]
    B = [[0 for _ in range(n)] for _ in range(n)]
    return A, B

def Pruebas():
    sizes = [2,4,8,16,32,64,128,256,512,1024]

    for i in range(len(sizes)):
        randA, randB = generar_random(sizes[i])
        idA , idB= generar_identidad(sizes[i])
        ceroA, ceroB = generar_cero(sizes[i])

        print(f"## size = {sizes[i]}")
        print(BruteForce(randA, randB)[1])
        print(BruteForce(idA, idB)[1])
        print(BruteForce(ceroA, ceroB)[1])
        print(Recursivo(randA, randB)[1])
        print(Recursivo(idA, idB)[1])
        print(Recursivo(ceroA, ceroB)[1])
        print(Strassen(randA, randB)[1])
        print(Strassen(idA, idB)[1])
        print(Strassen(ceroA, ceroB)[1])
        print(Numpy(randA, randB)[1])
        print(Numpy(idA, idB)[1])
        print(Numpy(ceroA, ceroB)[1])

Pruebas()