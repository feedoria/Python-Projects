# Problema 2 — Aranjarea circulară a numerelor naturale
#
# Într-un fișier text sunt păstrate n numere naturale, unde n > 15.
#
# Se cere determinarea unei aranjări circulare a acestor numere astfel încât suma produselor
# oricăror două numere alăturate să fie maximă.
#
# Fiind o aranjare circulară, ultimul număr este considerat vecin cu primul.
#
# Pentru o aranjare:
# p = [p0, p1, p2, ..., p(n-1)]
import random

from fontTools.varLib.models import nonNone

numere = [16, 90, 76, 89, 100, 67, 20, 35, 46]

n = len()
def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = list(range(n))
        random.shuffle(individ)
        populatie.append(individ)
    return populatie

def fitness(individ):
    produs_nr_alaturate = 1
    suma = 0

    for indice in range(len(individ)):
        produs_nr_alaturate = numere[individ[indice]] * numere[individ[(indice + 1)%n]]
        suma += produs_nr_alaturate

    return suma

def mutatie_interschimbare(individ):
    copil = individ.copy()

    i, j = random.sample(range(n), 2)

    copil[i], copil[j] = copil[j], copil[i]

    return copil

def schema_generala_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ = mutatie_interschimbare(individ)

        populatie_noua.append(individ)

    return populatie_noua

def recombinare_ocx(p1, p2):
    copil1 = [None] * n
    copil2 = [None] * n

    start, end = sorted(random.sample(range(n), 2))

    copil1[start:end + 1] = p1[start:end + 1]
    copil2[start:end + 1] = p2[start:end + 1]

    pozitie = 0
    for gena in p2:
        if gena not in copil1:
            while copil1[pozitie] is not None:
                pozitie +=1
            copil1[pozitie] = gena

    pozitie = 0
    for gena in p1:
        if gena not in copil2:
            while copil2[pozitie] is not None:
                pozitie += 1
            copil2[pozitie] = gena

    return copil1, copil2


