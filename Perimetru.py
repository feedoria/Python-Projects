# se considera n puncte in plan  si fiecare punct A are coord (xA,yA)
# oricare 3 puncte sunt necoliniare
# utilizati un algo genetic care sa determine 4 puncte cu perimetrul cel
# mai mare
# lungimea unui segment

#1.fenotip = cele 4 puncte alese care formeaza patrulaterul

#2.genotip = codificarea solutiei => vector de 4 indici distincti (de numere intregi)
# adica indici ai punctelor nu coordonatele directe

#3.solutie fezabila = un vector cu 4 elem intregi distincte intre 0 si n-1

#4.spatiul solutiilor = finit pentru ca alegem 4 din cele n
# daca tratam si ordinea avem permutari partiale: n*(n-1)*(n-2)*(n-3)
# daca tratam doar cele 4 puncte avem C(n,4) fara ordine sunt combinari

#5.restrictii: enuntul zice ca oricare 3 sunt necoliniare
# e bine ca oricare 3 puncte as alege ele pot forma un patrulater si nu mi pun problema de
# coliniaritate
# => deci restrictia principala: cele 4 puncte sa fie distincte
# pot fenta asta cu random.sample(range(n),4) si le iau direct distincte asa

#6.fitness/fct obiectiv => perimetrul maxim adica suma lungimilor segmentelor
# e deja problema de maximizare

#7.recombinare => discreta/uniforma , dar asta produce si duplicate deci trebuie si REPARARE

#8.mutatie =>inlocuire aleatoare fare duplicate
# am de ex individul [2,5,0,7] astia sunt indicii punctelor
# iau de exemplu pozitia 1 deci indicele 5 si il inlocuiesc cu un indice care NU ESTE IN INDIVID DEJA

import math
import random

puncte = [
    [0,0],
    [1,2],
    [3,1],
    [4,5],
    [2,3],
    [6,1],
    [5,4]
]

n = len(puncte)

def genereaza_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = random.sample(range(n), 4)
        populatie.append(individ)

    return populatie

def distanta(indice1,indice2):
    x1,y1 = puncte[indice1]
    x2,y2 = puncte[indice2]

    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def fitness(individ):
    return distanta(individ[0],individ[1]) + distanta(individ[1],individ[2]) + distanta(individ[2],individ[3])  + distanta(individ[3],individ[0])

def selectie_turneu(populatie, dim_turneu):
    candidati = random.sample(populatie, dim_turneu)

    cel_mai_bun = candidati[0]

    for individ in candidati:
        if fitness(individ) > fitness(cel_mai_bun):
            cel_mai_bun = individ

    return cel_mai_bun.copy()

def mutatie_inlocuire(individ):
    copil = individ.copy()

    pozitie = random.randint(0,3)

    variante = []

    for indice in range(n):
        if indice not in copil:
            variante.append(indice)

    copil[pozitie] = random.choice(variante)

    return copil

def schema_generala_de_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ = mutatie_inlocuire(individ)
        populatie_noua.append(individ)

    return populatie_noua

def GA(dimensiune_populatie, numar_generatii, probabilitate_mutatie, dimensiune_turneu):
    populatie = genereaza_populatie(dimensiune_populatie)

    for _ in range(numar_generatii):
        copii = []

        while len(copii) < dimensiune_populatie:
            parinte = selectie_turneu(populatie, dimensiune_turneu)
            copil = mutatie_inlocuire(parinte)

            copii.append(copil)

        total = populatie + copii
        total.sort(key=fitness, reverse=True)

        populatie = total[:dimensiune_populatie]

    return max(populatie, key=fitness)

solutie = GA(
    dimensiune_populatie=20,
    numar_generatii=100,
    probabilitate_mutatie=0.1,
    dimensiune_turneu=3,
)

print("Solutie:", solutie)
print("Fitness:", fitness(solutie))
print("Puncte alese:", [puncte[i] for i in solutie])