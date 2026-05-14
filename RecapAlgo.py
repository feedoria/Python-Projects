import random


# MUTATIE PERMUTARE
def mutatie_interschimbare(individ):
    copil = individ.copy()
    i, j = random.sample(range(len(copil)), 2)
    copil[i], copil[j] = copil[j], copil[i]
    return copil


# RECOMBINARE PERMUTARE
def recombinare_OCX(p1, p2):
    n = len(p1)

    copil1 = [None] * n
    copil2 = [None] * n

    start, end = sorted(random.sample(range(n), 2))

    copil1[start:end + 1] = p1[start:end + 1]
    copil2[start:end + 1] = p2[start:end + 1]

    pozitie = 0
    for gena in p2:
        if gena not in copil1:
            while copil1[pozitie] is not None:
                pozitie += 1
            copil1[pozitie] = gena

    pozitie = 0
    for gena in p1:
        if gena not in copil2:
            while copil2[pozitie] is not None:
                pozitie += 1
            copil2[pozitie] = gena

    return copil1, copil2


# MUTATIE BINAR
def mutatie_bitflip(individ):
    copil = individ.copy()
    pozitie = random.randint(0, len(copil) - 1)
    copil[pozitie] = 1 - copil[pozitie]
    return copil


# MUTATIE BINAR CU NUMAR FIX DE 1
def mutatie_binar_numar_fix(individ):
    copil = individ.copy()

    pozitii_1 = []
    pozitii_0 = []

    for i in range(len(copil)):
        if copil[i] == 1:
            pozitii_1.append(i)
        else:
            pozitii_0.append(i)

    i = random.choice(pozitii_1)
    j = random.choice(pozitii_0)

    copil[i], copil[j] = copil[j], copil[i]

    return copil


# RECOMBINARE BINAR
def recombinare_unipunct(p1, p2):
    n = len(p1)
    punct = random.randint(1, n - 1)
    copil1 = p1[:punct] + p2[punct:]
    copil2 = p2[:punct] + p1[punct:]
    return copil1, copil2


# MUTATIE VECTOR REAL
def mutatie_fluaj(individ, pas):
    copil = individ.copy()
    pozitie = random.randint(0, len(copil) - 1)
    copil[pozitie] += random.uniform(-pas, pas)
    return copil


# MUTATIE VECTOR REAL CU SUMA FIXA
def mutatie_fluaj_suma_fixa(individ):
    copil = individ.copy()
    din_care, in_care = random.sample(range(len(copil)), 2)
    suma_de_mutat = random.uniform(0, copil[din_care])
    copil[din_care] -= suma_de_mutat
    copil[in_care] += suma_de_mutat
    return copil


# RECOMBINARE VECTOR REAL
def recombinare_aritmetica(p1, p2):
    alpha = random.random()
    copil1 = []
    copil2 = []

    for i in range(len(p1)):
        copil1.append(alpha * p1[i] + (1 - alpha) * p2[i])
        copil2.append(alpha * p2[i] + (1 - alpha) * p1[i])

    return copil1, copil2


# MUTATIE VECTOR INTREG
def mutatie_resetare_aleatoare(individ, a, b):
    copil = individ.copy()
    pozitie = random.randint(0, len(copil) - 1)
    copil[pozitie] = random.randint(a, b)
    return copil


# MUTATIE INDICI DISTINCTI
def mutatie_inlocuire_indice(individ, n_total):
    copil = individ.copy()
    pozitie = random.randint(0, len(copil) - 1)

    variante = []
    for i in range(n_total):
        if i not in copil:
            variante.append(i)

    copil[pozitie] = random.choice(variante)

    return copil


# RECOMBINARE UNIFORMA
def recombinare_uniforma(p1, p2):
    copil1 = []
    copil2 = []

    for i in range(len(p1)):
        if random.random() < 0.5:
            copil1.append(p1[i])
            copil2.append(p2[i])
        else:
            copil1.append(p2[i])
            copil2.append(p1[i])

    return copil1, copil2