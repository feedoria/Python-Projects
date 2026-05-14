# Problema 1 — Repartizarea legionarilor în centurii
#
# Lux Brumalis, comandantul legiunii romane XXL - Utopica, vrea să echilibreze forța de luptă
# a cohortei întâi din legiune, după înlocuirea pierderilor cu recruți noi.
#
# Pentru fiecare legionar din cohortă se cunoaște nivelul de vitejie în luptă, evaluat pe o
# scară de la 1 la 100, unde 100 reprezintă valoarea maximă.
#
# Utilizați un algoritm genetic pentru a repartiza cei n = 480 legionari ai cohortei în
# m = 6 centurii de dimensiuni egale, astfel încât valorile centuriilor să fie cât mai apropiate.
#
# Valoarea unei centurii este calculată ca suma valorilor individuale ale membrilor.
import random

def genereaza_lista_vitejie():
    vitejie = []

    for _ in range(480):
        vitejie.append(random.randint(1,100))

    return vitejie

vitejie = genereaza_lista_vitejie()

n = len(vitejie)

m = 6

def genereaza_populatie(dimensiune_populatie):
    populatie = []

    for _ in range(dimensiune_populatie):
        individ = list(range(n))
        random.shuffle(individ)
        populatie.append(individ)

    return populatie

def fitness(individ):
    dim_centurie = n // m
    sume_centurii = []

    # calculez suma vitejiei pentru fiecare centurie
    for c in range(m):
        inceput = c * dim_centurie
        sfarsit = inceput + dim_centurie

        suma = 0
        for pozitie in range(inceput, sfarsit):
            legionar = individ[pozitie]
            suma += vitejie[legionar]

        sume_centurii.append(suma)

    # calculez media sumelor centuriilor
    media = sum(sume_centurii) / len(sume_centurii)

    # calculez varianta sumelor
    varianta = 0
    for suma in sume_centurii:
        varianta += (suma - media) ** 2

    varianta = varianta / len(sume_centurii)

    # vrem varianta mica, deci fitness mare
    return 1 / (1 + varianta)

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

def recombinare_OCX(p1,p2):
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
                pozitie+=1
            copil2[pozitie] = gena

    return copil1, copil2






