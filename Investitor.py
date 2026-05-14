# Un investitor dorește să investească 100.000 lei în trei titluri de valoare: T1, T2, T3.
#
# T1: dividend 4%, factor risc 1
# T2: dividend 9%, factor risc 3
# T3: dividend 6%, factor risc 2
#
# Condiții:
# 1. factorul mediu de risc este sub 2.5
# 2. suma investită în T2 este de maxim 30.000 lei
#
# Se cer sumele investite în T1, T2 și T3 astfel încât profitul obținut să fie maxim.
#
# Dacă sumele investite sunt x, y, z, factorul mediu de risc este:
# (x + 3y + 2z) / (x + y + z)

#1.fenotip = investirea in cele 3 titluri de valoare T1,T2,T3

#2.genotip = vector real de sume unde x= suma invest in t1 .....

#3.forma individului = vectorul de sume [x,y,z]

#4.spatiul solutiilor = infinit / finit daca sunt bani intregi

#5.restrictii = da, trebuie riscul mediu sa fie < 2.5 si suma investita in T2 maxim 30000
# x + y + z = 100000
#
# x, y, z >= 0
#
# y <= 30000
#
# (x + 3y + 2z) / (x + y + z) < 2.5

#6.fitness/functia obiectiv = profitul (suma profitului din investitia in T1,T2 respectiv T3)

#7.mutatie = fulaj (nu stiu ce e) sau am vazut modificare aleatoare a unei sume + reparare(ce o fi insemnand
# si asta ;D)

#8.recombinare => aritmetica(nu stiu ce e)

#9.selectie parinti => cu turneu ca altu nu stiu :))))

#10.selectie generatie => elitism adica alegem indivizii cu fitnessul cel mai mare

#11.conditie de terminare => cand se ajunge la nr max de generatii bagat sau cand se atinge obiectivul
#(profitul maxim)


import random
from logging import exception

info_titluri_de_valoare = [
    [4,1],
    [9,3],
    [6,2]
]

n = len(info_titluri_de_valoare)
B = 100000
def risc_mediu(individ):
    x, y, z = individ
    return (x + 3*y + 2*z) / (x + y + z)

def este_fezabil(individ):
    x, y, z = individ

    if x < 0 or y < 0 or z < 0:
        return False

    if abs(x + y + z - B) > 0.0001:
        return False

    if y > 30000:
        return False

    if risc_mediu(individ) >= 2.5:
        return False

    return True

def generare_individ():
    while True:
        y = random.uniform(0, 30000)
        x = random.uniform(0, B - y)
        z = random.uniform(0, B - y)

        individ = [x, y, z]

        if este_fezabil(individ):
            return individ

def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        populatie.append(generare_individ())

    return populatie

def fitness(individ):
    x, y, z = individ

    profit_din_suma_investita_T1 = info_titluri_de_valoare[0][0] / 100 * x
    profit_din_suma_investita_T2 = info_titluri_de_valoare[1][0] / 100 * y
    profit_din_suma_investita_T3 = info_titluri_de_valoare[2][0] / 100 * z

    return profit_din_suma_investita_T1 + profit_din_suma_investita_T2 + profit_din_suma_investita_T3

# def mutatie_fulaj(individ):
#     copil = individ.copy()
#
#     #vrem sa mutam o suma de bani dintr un titlu in alt titlu fara sa incalcam restrictiile
#
#     titluri_de_interschimbat_bani = random.sample([0,1,2], 2)
#
#     suma = random.uniform(0, min(individ[titluri_de_interschimbat_bani[0]], individ[titluri_de_interschimbat_bani[1]]))
#
#     if individ[titluri_de_interschimbat_bani[0]] > individ[titluri_de_interschimbat_bani[1]]:
#         # ca sa facem mai destept verificam care e mai mare si transferam din suma mai mare in cea mica
#         copil[titluri_de_interschimbat_bani[0]] -= suma
#         copil[titluri_de_interschimbat_bani[1]] += suma
#     else:
#         copil[titluri_de_interschimbat_bani[0]] += suma
#         copil[titluri_de_interschimbat_bani[1]] -= suma
#
#     return copil

def mutatie_fluaj(individ):
    copil = individ.copy()

    # alegem doua titluri diferite
    sursa, destinatie = random.sample([0, 1, 2], 2)

    # mutam o suma mica din sursa in destinatie
    suma = random.uniform(0, min(5000, copil[sursa]))

    copil[sursa] -= suma
    copil[destinatie] += suma

    # daca mutatia respecta restrictiile, o pastram
    if este_fezabil(copil):
        return copil
    else:
        return individ.copy()

def schema_generala_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ = mutatie_fluaj(individ)
        populatie_noua.append(individ)

    return populatie_noua

def recombinare_aritmetica(p1,p2):
    copil1 = []
    copil2 = []
    alpha = random.random()

    for i in range(p1):
        copil1.append(alpha * p1[i] + (1 - alpha) * p2[i])
        copil2.append(alpha * p2[i] + (1 - alpha) * p1[i])

    return copil1, copil2

def recombinare_aritmetica_cu_fezabilitate(p1, p2):
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

def selectie_parinte_turneu(populatie, dim_turneu):
    if dim_turneu <= len(populatie):
        candidati = random.sample(populatie, dim_turneu)
    else:
        raise Exception("Trebuie dim_turneu sa fie mai mic decat dim_populatie")

    cel_mai_bun = candidati[0]

    for candidat in candidati:
        if fitness(candidat) > fitness(cel_mai_bun):
            cel_mai_bun = candidat

    return cel_mai_bun.copy()

def GA(dim_pop, nr_generatii, probab_mutatie, dim_turneu):
    populatie = generare_populatie(dim_pop)

    for _ in range(nr_generatii):
        copii = []
        while len(copii) < dim_pop:
            parinte = selectie_parinte_turneu(populatie, dim_turneu)

            if random.random() < probab_mutatie:
                copil = mutatie_fluaj(parinte)
            else:
                copil = parinte.copy()
            copii.append(copil)
        total = copii + populatie
        total.sort(key=fitness, reverse=True)

        populatie = total[:dim_pop]

    return max(populatie, key=fitness)






