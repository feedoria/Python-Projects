# Se consideră k puncte in plan, fiecare punct A are coordonatele (xA, yA),
# ambele coordonate fiind in mulțimea (0, 1, 2, -., n).
# Utilizați un algoritm genetic pentru a determina (dacă există)
# un punct R in plan cu coordonate (xR, yR), ambele numere din intervalul [a, b]
# cu proprietatea că este egal depărtat de cele k puncte.
# Lungimea unui segment AR este sqrt((xA-xR)2+ (yA-yRJ3, k. n. a, b sint parametri dați.

#1.Fenotipul = solutia reala: punctul R din plan cu coord (xR, yR)

#2.Genotipul = codificarea punctului R
#alegem vector de 2 numere intregi
# forma individului: [XR,YR], unde XR,YR apartin [a,b]

#3.Spatiul solutiilor: finit, in intervalul a,b
#numarul de variante: (b-a+1)^2
#pt XR am b-a+1 valori pos, la fel si pt YR

#4.Restrictii => sunt restrictii din problema sa se afle in interval, dar nu suplimentare daca generam direct

#6.Functia obiectiv/fitness
#pentru un individ R =[XR,YR] calculam distantele la fiecare punct Ai
# d(R,Ai) = sqrt((xAi - XR)^2 + (yAi - YR)^2) => toate dist trb sa fie egale
# eroare = distMax - distMin
#finess(R) = 1/(1+max(distante) - min(distante)) ; distante = distantele de la R la fiecare punct

#7.Operatorii genetici
#Reprezentare => vector intreg cu 2 componente
#Recombinare => discreta/uniforma
    #exemplu
    # pentru p1=[2,8] si p2=[5,3] => [2,3]
#Mutatie => resetare aleatoare
    #alegem o coordonata si ii dam o valoare noua din [a,b]
    #exemplu
    # avem [4,7] si mutam xr [9,7] sau mutam yr [4,2]
#Spatiu => finit
#Restrictii => fara suplimentare, daca generam direct in a,b

#8.Selectare parinti prin SUS/FPS/sigma sau turneu

#9.Generatie urmatoare => elitism

#10.Terminare => nr max de generatii sau fitness maxim 1

import random
import math

puncte = [(0,1), (2,3), (4,1), (3,5)]
a = 0
b = 10
k = len(puncte)

def genereaza_populatie(dim):
    populatie = []

    for _ in range(dim):
        XR = random.randint(a,b)
        YR = random.randint(a,b)
        individ = [XR,YR]
        populatie.append(individ)

    return populatie

def distanta(R,A):
    XR, YR = R
    xA, yA = A

    return math.sqrt((xA - XR) ** 2 + (yA - YR) ** 2)

def fitness(individ):
    distante = []

    for punct in puncte:
        distante.append(distanta(punct, individ))

    eroare = max(distante) - min(distante)

    return 1/(1+eroare)

def selectie_turneu(populatie, dim_turneu):
    candidati = random.sample(populatie, dim_turneu)

    cel_mai_bun = candidati[0]

    for individ in candidati:
        if fitness(individ) > fitness(cel_mai_bun):
            cel_mai_bun = individ

    return cel_mai_bun.copy()

def mutatie_resetare_aleatoare(individ):
    copil = individ.copy()

    poz = random.randint(0,1)
    copil[poz] = random.randint(a, b)

    return copil

def schema_generala_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ = mutatie_resetare_aleatoare(individ)

        populatie_noua.append(individ)

    return populatie_noua


def recombinare_uniforma(p1, p2):
    copil1 = []
    copil2 = []

    for i in range(2):
        if random.random() < 0.5:
            copil1.append(p1[i])
            copil2.append(p2[i])
        else:
            copil1.append(p2[i])
            copil2.append(p1[i])

    return copil1, copil2


def GA(dim, nr_gen, pc, pm, dim_turneu):
    populatie = genereaza_populatie(dim)

    for _ in range(nr_gen):

        copii = []

        while len(copii) < dim:

            p1 = selectie_turneu(populatie, dim_turneu)

            p2 = selectie_turneu(populatie, dim_turneu)

            if random.random() < pc:

                c1, c2 = recombinare_uniforma(p1, p2)

            else:

                c1 = p1.copy()

                c2 = p2.copy()

            if random.random() < pm:
                c1 = mutatie_resetare_aleatoare(c1)

            if random.random() < pm:
                c2 = mutatie_resetare_aleatoare(c2)

            copii.append(c1)

            if len(copii) < dim:
                copii.append(c2)

        total = populatie + copii

        total.sort(key=fitness, reverse=True)

        populatie = total[:dim]

        if fitness(populatie[0]) == 1:
            break

    return max(populatie, key=fitness)


solutie = GA(dim=20, nr_gen=100, pc=0.8, pm=0.1, dim_turneu=3)

print("Solutie:", solutie)

print("Fitness:", fitness(solutie))


