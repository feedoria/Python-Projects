# Problema — Planificarea bugetului pentru reclame
#
# O firmă are un buget total de 100000 lei pe care vrea să îl împartă între 3 canale
# de promovare:
# reclame online, reclame TV și reclame outdoor.
#
# Pentru fiecare canal se cunoaște randamentul estimat:
# randament = [0.08, 0.12, 0.06]
#
# și factorul de risc:
# risc = [1, 3, 2]
#
# Condițiile sunt:
# 1. Suma totală investită trebuie să fie 100000 lei.
# 2. Suma investită în al doilea canal trebuie să fie de cel mult 30000 lei.
# 3. Factorul mediu de risc trebuie să fie cel mult 2.
#
# Dacă sumele investite sunt [x, y, z], atunci profitul este:
# profit = 0.08*x + 0.12*y + 0.06*z
#
# iar factorul mediu de risc este:
# risc_mediu = (1*x + 3*y + 2*z) / (x + y + z)
#
# Trebuie determinată împărțirea bugetului astfel încât profitul să fie maxim.

import random

TOTAL = 100000

randament = [0.08, 0.12, 0.06]
risc = [1, 3, 2]

limita_C2 = 30000
limita_risc = 2


def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        y = random.uniform(0, limita_C2)
        x = random.uniform(0, TOTAL - y)
        z = TOTAL - x - y

        individ = [x, y, z]

        if este_fezabil(individ):
            populatie.append(individ)
        else:
            # daca nu e fezabil, mai incerc o data printr-o metoda simpla
            while not este_fezabil(individ):
                y = random.uniform(0, limita_C2)
                x = random.uniform(0, TOTAL - y)
                z = TOTAL - x - y
                individ = [x, y, z]

            populatie.append(individ)

    return populatie


def risc_mediu(individ):
    x, y, z = individ

    return (x + 3 * y + 2 * z) / (x + y + z)


def este_fezabil(individ):
    x, y, z = individ

    if x < 0 or y < 0 or z < 0:
        return False

    if abs(x + y + z - TOTAL) > 0.000001:
        return False

    if y > limita_C2:
        return False

    if risc_mediu(individ) > limita_risc:
        return False

    return True


def fitness(individ):
    if not este_fezabil(individ):
        return 0

    x, y, z = individ

    return 0.08 * x + 0.12 * y + 0.06 * z


def mutatie_fluaj(individ):
    copil = individ.copy()

    din_care, in_care = random.sample(range(3), 2)

    suma_de_mutat = random.uniform(0, copil[din_care])

    copil[din_care] -= suma_de_mutat
    copil[in_care] += suma_de_mutat

    if este_fezabil(copil):
        return copil
    else:
        return individ.copy()


def schema_generala_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ_nou = mutatie_fluaj(individ)
        else:
            individ_nou = individ.copy()

        populatie_noua.append(individ_nou)

    return populatie_noua


def recombinare_aritmetica(p1, p2):
    alpha = random.random()

    copil1 = []
    copil2 = []

    for i in range(len(p1)):
        copil1.append(alpha * p1[i] + (1 - alpha) * p2[i])
        copil2.append(alpha * p2[i] + (1 - alpha) * p1[i])

    if not este_fezabil(copil1):
        copil1 = p1.copy()

    if not este_fezabil(copil2):
        copil2 = p2.copy()

    return copil1, copil2