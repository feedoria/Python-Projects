# Scrieți câte o funcție Python pentru rezolvarea următoarelor probleme:
# 1. Calculați numărul liniilor unei matrice cu proprietatea că au elementele în ordine
# crescătoare.
from numpy.ma.core import concatenate

print("Ex 1: ")
import numpy as np
arr = np.arange(6).reshape(2,3)

def nrLiniiMatrice(matrice) -> int:
    nrLinii = 0
    suntCrescLinie = True
    for i in range(0,2):
        minimLinie = matrice[i][0]
        for j in range(0,2):
            if matrice[i][j+1] < matrice[i][j]:
                minimLinie = matrice[i][j+1]
                suntCrescLinie = False
        if suntCrescLinie == True:
            nrLinii += 1
    return nrLinii

print(nrLiniiMatrice(arr))

#2. Determinați coloanele unei matrice cu proprietatea că au cel mai mic element egal cu 5.
print("Ex 2: ")
mat2 = np.array([[9,0,3],[7,5,6],[5,8,9]])
for j in range(0,3):
    minimCol = mat2[0][j]
    for i in range(0,3):
        if mat2[i][j] < minimCol:
            minimCol = mat2[i][j]
    if minimCol == 5:
        print(f"Coloana {j} are cel mai mic element 5\n")


# 3. Implementați algoritmul de sortare prin metoda bulelor pentru a ordona fiecare linie a unei
# matrice
print("Ex 3: ")
def bubble_sort(matriceData):
    ok = True
    while ok:
        ok = False
        for i in range(0,len(matriceData)-1):
            for j in range(0,len(matriceData[i])-1):
                if matriceData[i][j] > matriceData[i][j+1]:
                    aux = matriceData[i][j]
                    matriceData[i][j] = matriceData[i][j+1]
                    matriceData[i][j+1] = aux
                    ok = True
bubble_sort(mat2)
print(mat2)

# 4. Implementați algoritmul de sortare prin inserție pentru a ordona fiecare coloană a unei
# matrice
print("Ex 4: ")
def insertion_sort_column(matrice, col):
    n = len(matrice)

    for i in range(1, n):
        key = matrice[i][col]
        j = i - 1

        while j >= 0 and matrice[j][col] > key:
            matrice[j + 1][col] = matrice[j][col]
            j -= 1

        matrice[j + 1][col] = key

    return matrice


# Test
mat = [
    [5, 2, 9],
    [1, 7, 3],
    [4, 6, 8]
]

print(f"sortare prin insetie a lui \"mat\" {insertion_sort_column(mat, 1)}")

# 5. Scrieți o funcție recursivă pentru calculul cmmdc dintre două numere naturale nenule
print("Ex 5: ")
def cmmdc(a,b) -> int:
    maxDiv = 0
    if a > b:
        c = b
    else:
        c = a
    for i in range(1, c+1):
        if a % i == 0 and b % i == 0 and i > maxDiv:
            maxDiv = i
    return maxDiv
print(cmmdc(3,4))
print(cmmdc(2,6))

def cmmdcRecursiv(a,b) -> int:
    if b == 0:
        return a
    return cmmdcRecursiv(b, a % b)
print(cmmdcRecursiv(3,6))

print("Ex 6: ")

# 6. Fie A și B două matrice pătratice și n un număr natural nenul. Calculați 𝐴
# 𝑇
# , A+B, A*B și
# 𝐴
# 𝑛
# . -> A transpus DA A+B DA A*B DA A^n

A = np.array([[1,0],[0,1]])
B = np.array([[1,2],[0,1]])
C = np.array([[1,2,3],[0,9,0]])
produs = np.dot(A,B)
print(f"Produsul matricei A*B: {produs}")

print(f"A transpus: {A.T}\n")
print(C.T) # verific mai vizibil ca merge .T

def adunareMatrice(matrice1, matrice2):
    if len(matrice1) != len(matrice2):
        return None
    else:
        for i in range(0,len(matrice1)):
            for j in range(0,len(matrice1[i])):
                matriceRez = matrice2[i][j] + matrice1[i][j]
        return matriceRez

print(f"Adunare A si B: {adunareMatrice(A, B)}")

print("A^n :")
# deci stiu ca pot sa fac x ** 2 de ex si imi da x la patrat
# mai stiu si ca produsul lui A si B se face cu .dot
# deci daca as face .dot(A,A) prima oara si retin asta in C si apoi .dot(C,A) de ex de fiecare data pana la n
# pe care il scad pas cu pas
# ar trebui sa obtin A^n

def produsADeNOri(a,n):
    if n==1:
        return a
    elif n==2:
        c = np.dot(a,a)
        return c
    else:
        c = np.dot(a, a)
        for i in range(0,n-2):
            d = np.dot(c,a)
            n -= 1
            c = d
        return d
A = [[1,2],[2,0]]
print(f" produs A de 2 ori : {produsADeNOri(A,2)}")
print(f" produs A de 3 ori : {produsADeNOri(A,3)}")


#EXERCITIU SEMINAR1
# fibonacci -> facut cu profu la seminar1
def Fib(n):
    if n==0:
        return 0
    if n==1:
        return 1
    return Fib(n-1) + Fib(n-2)

def Fib2(n):
    rez = [0,1]
    for i in range(2,n):
        rez.append(rez[i-1] + rez[i-2])
    return rez

if __name__ == "__main__":
    n = int(input("Da nr pt n: "))
    #print(Fib(n))
    rez = Fib2(n)
    print(f"Rezultat functie Fib2[{n}] : {rez}")

# 7. Implementați algoritmul de sortare prin inserție în liste/vectori
def insertion_sort(v):
    n = len(v)

    for i in range(1, n):
        key = v[i]        # elementul care trebuie inserat
        j = i - 1

        # mutăm elementele mai mari la dreapta
        while j >= 0 and v[j] > key:
            v[j + 1] = v[j]
            j -= 1

        # inserăm elementul pe poziția corectă
        v[j + 1] = key

    return v


# Test
lista = [5, 2, 9, 1, 3]
print(insertion_sort(lista))


# 8. Verificați proprietatea unei permutări de a fi permutarea identică.
# deci permutarea identica vizualizata ca matrice pozitia 1 are val 1 poz 2 are val 2 si tot asa

def verificarePermutareIdentica(mat):
    if len(mat) != 2:
        print("Nu e matrice 2 x n")
        return False

    if len(mat[0]) != len(mat[1]):
        print("Randurile nu au aceeasi lungime")
        return False

    n = len(mat[0])  # numarul de coloane
    ok = True
    for i in range(0, n):
        if mat[0][i] == mat[1][i] and mat[0][i] == i+1:
            ok = True
        else:
            ok = False
            break
    if ok:
        return print("Matriceaa data este permutarea identica")
    else:
        return print("Matriceaa data NU este permutarea identica")
matricePermutare = [
    [1,2,3],
    [1,2,3]
]

verificarePermutareIdentica(matricePermutare)

matricePermutare2 = [
    [1,2,5],
    [1,2,5]
]

verificarePermutareIdentica(matricePermutare2)

matricePermutare3 = [
    [0,7,8],
    [9,0,3]
]

verificarePermutareIdentica(matricePermutare3)

# 9. Fie S mulțimea vectorilor binari de lungime 7. Calculați, prin generare aleatoare, o matrice
# A cu 20 de linii, vectori din S și un vector V cu 20 de elemente, fiecare 𝑉[𝑖] reprezentând
# calitatea liniei i din A, definită prin suma biților vectorului linie i.

# matrice9 = np.zeros((20,7))
# print(f"matrice 9 declarare/init: {matrice9}")
# for i in range(7):
#     for j in range(20):
#         matrice9 = np.random.rand(0,1)
#
# print("matrice 9: (dupa completare)")
# print(matrice9)
# for linie in matrice9:     # DE INTREBAT!!!!
#     print(linie)

matrice9 = np.random.randint(0,2,size=(20,7))

V = np.sum(matrice9, axis=1)
print(matrice9)
print(V)

# 11. Implementați algoritmul hill-climbing pentru a calcula maximul funcției
# 𝑓:{1,2, … ,2500} → ℝ, 𝑓(𝑥) = (𝑠𝑖𝑛(𝑥 − 2)) ^ 2 − 𝑥 ∗ 𝑐𝑜𝑠(𝑥).

#solutia mea
import math as m
def f(x):
    return (m.sin(x-2)) ** 2 - x * m.cos(x)

def algHillClimbing():
    maxLocal = f(0)
    for x in range(2,2500):
        if f(x-1) < f(x) and f(x) > f(x+1) and maxLocal < f(x):
            maxLocal = f(x)
    return maxLocal

print(f"Implementare algoritmul Hill-Climbing pentru functia f : {algHillClimbing()}")


# solutie 2
def maxim_global():
    best_x = 1
    best_val = f(1)
    for x in range(2, 2501):
        val = f(x)
        if val > best_val:
            best_val = val
            best_x = x
    return best_x, best_val

x, val = maxim_global()
print("Maxim global la x =", x, "valoare =", val)


# 12. Fie 𝑓:{1,2, … ,2500} → ℝ, 𝑓(𝑥) = (𝑠𝑖𝑛(𝑥 − 2)) ^ 2 − 𝑥 ∗ 𝑐𝑜𝑠(𝑥) funcţia obiectiv a unei
# probleme de maxim. Fiecărui fenotip 𝑥 ∈ {1,2, … ,2500} îi corespunde un genotip şir binar
# obţinut prin reprezentarea standard în bază 2 a lui x. Rezolvați problema de maxim utilizând
# un algoritm de tip hill climbing.
# Indicație
# 1.x ∈ {1,2, … ,2500}→b(x): reprezentarea binară standard
# 2. vecinii unui sir binar b(x) → vectori binari cu distanta Hamming 1 fata de b(x), dar ale
# caror reprezentari in baza 10 sunt in {1,2, … ,2500}
# 3. valoarea unui sir binar b(x)
# - obtine reprezentarea in baza 10 a lui b(x) → x
# - evalueaza f(x) → val
# - calitatea lui b(x) este val

# DE INTREBAT!!!!!!

def reprezentareBaza2(x : int) -> str:
    # pentru reprez in baza 2 trebuie sa impartim la 2 pana nu mai merge si sa luam
    # resturile de la ultimul la primul si aceea e reprezentarea numarului in baza 2, iar valorile
    # pot fi 0 sau 1
    n = int(x/2)
    xBaza2 = ""
    for nrImpartiri in range(0,n-1):
        x_pt_rest = int((x/2)%2)
        xBaza2 += str(x_pt_rest)
        x /= 2
    return xBaza2
# print(reprezentareBaza2(10))
print(int(reprezentareBaza2(10)))

#Test pas cu pas
# x = 10
# x_pt_rest = int((x/2)%2)
# rez = str(x_pt_rest) + "0"
# xBaza2 = ""
# xBaza2 += str(x_pt_rest)
# print(xBaza2)
# #x_pt_rest = int(((x/2)/2)%2)
# print(rez)
# print(x_pt_rest)



def problema12():
    x = np.random.randint(1,2500)
    while True:
        curent = f(x)

        stanga = f(x-1) if x > 1 else float('inf')  # fortam alg sa nu iasa din intervalul 1-2500
        dreapta = f(x+1) if x<2500 else float('inf')

        if stanga > curent and stanga >= dreapta:
            x = x - 1
        elif dreapta > curent and dreapta > stanga:
            x = x + 1
        else:
            break

def f(x):
    return sin(x-2) ** 2 - x*cos(x)


