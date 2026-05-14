import random

timp = [4, 7, 3, 6, 2, 5, 8, 1]
memorie = [80, 120, 60, 150, 40, 100, 180, 30]
valoare = [10, 18, 7, 16, 5, 13, 20, 4]

T = 15
M = 300
n = len(timp)


def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = []

        for i in range(n):
            individ.append(random.randint(0, 1))

        populatie.append(individ)

    return populatie


def este_fezabil(individ):
    total_timp = 0
    total_memorie = 0

    for i in range(len(individ)):
        if individ[i] == 1:
            total_timp += timp[i]
            total_memorie += memorie[i]

    return total_timp <= T and total_memorie <= M


def fitness(individ):
    if not este_fezabil(individ):
        return 0

    val_functionala = 0

    for i in range(len(individ)):
        if individ[i] == 1:
            val_functionala += valoare[i]

    return val_functionala


def mutatie_bitflip(individ):
    copil = individ.copy()

    pozitie = random.randint(0, len(copil) - 1)

    copil[pozitie] = 1 - copil[pozitie]

    return copil


def schema_generala_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ_nou = mutatie_bitflip(individ)
        else:
            individ_nou = individ.copy()

        populatie_noua.append(individ_nou)

    return populatie_noua


def recomb_unipunct(p1,p2):
    pass










def recombinare_unipunct(p1, p2):
    n = len(p1)

    punct = random.randint(1, n - 1)

    copil1 = p1[:punct] + p2[punct:]
    copil2 = p2[:punct] + p1[punct:]

    return copil1, copil2