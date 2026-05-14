import random
from codeop import compile_command

n = 10

#permutare

def mutatie_interschimbare(individ):
    copil = individ.copy()

    i, j = random.sample(range(len(copil)), 2)

    copil[i], copil[j] = copil[j], copil[i]

    return copil

def recomb_ocx(p1, p2):
    copil1 = [None] * n
    copil2 = [None] * n

    start, end = sorted(random.sample(range(n),2))

    copil1[start:end + 1] = p1[start:end + 1]
    copil2[start:end + 1] = p2[start:end + 1]

    pozitie = 0
    for gena in p1:
        if gena not in copil2:
            while copil2[pozitie] is not None:
                pozitie += 1
            copil2[pozitie] = gena

    pozitie = 0
    for gena in p2:
        if gena not in copil1:
            while copil1[pozitie] is not None:
                pozitie += 1
            copil1[pozitie] = gena

    return copil1, copil2

#vector binar
def mutatie_bitflip(individ):
    copil = individ.copy()

    pozitie = random.randint(0, range(len(copil)))

    copil[pozitie] = 1 - copil[pozitie]
    return copil

def mutatie_swap(individ):
    copil = individ.copy()

    #i, j = random.sample(range(len(copil)), 2)

    pozitii_0 = []
    pozitii_1 = []
    for i in copil:
        if copil[i] == 1:
            pozitii_1.append(i)
        else:
            pozitii_0.append(i)

    pozitie_0 = random.choice(pozitii_0)
    pozitie_1 = random.choice(pozitii_1)
    copil[pozitie_0], copil[pozitie_1] = copil[pozitie_1], copil[pozitie_0]
    return copil

def recombinare_unipunct(p1, p2):
    n = len(p1)
    punct = random.randint(0, n - 1)
    copil1 = p1[:punct] + p2[punct:]
    copil2 = p2[:punct] + p1[punct:]
    return copil1, copil2


# vector real
def mutatie_fluaj(individ, pas):
    copil = individ.copy()

    suma = random.uniform(-pas, pas)
    pozitie = random.randint(0, len(copil))

    copil[pozitie] += suma
    return copil

def recombinare_aritmetica(p1,p2):
    alpha = random.random()

    copil1 = []
    copil2 = []
    for i in range(len(p1)):
        copil1.append(alpha * p1[i] + (1-alpha) * p2[i])
        copil2.append(alpha * p2[i] + (1-alpha) * p1[i])

    return copil1, copil2

# vector intreg
def mutatie_resetare_aleatoare(individ, a, b):
    copil = individ.copy()
    # a si b sunt din datele problemei ma gandesc ca mi spune de exemplu sa fie intre 0 si 100 valorile
    valoare = random.randint(a,b)
    pozitie = random.randint(0, len(copil))
    copil[pozitie] = valoare
    return copil

def recomnbinare_uniforma(p1, p2):
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

def schema_generala_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ = mutatie_interschimbare(individ)
        populatie_noua.append(individ)

    return populatie_noua
