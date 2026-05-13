# Problema 1 — tip „indici fără repetiții”
# Enunț
#
# Se dau n locații turistice într-un oraș, fiecare locație având coordonate în plan:
# L1 = (x1, y1), L2 = (x2, y2), ..., Ln = (xn, yn)
#
# Trebuie să alegem 3 locații distincte pentru amplasarea unor puncte de informare turistică,
# astfel încât suma distanțelor dintre cele 3 locații alese să fie maximă.
#
# Pentru trei locații alese A, B, C, calitatea soluției este:
# d(A,B) + d(B,C) + d(C,A)
# unde distanța dintre două locații se calculează cu formula euclidiană:
# d(A,B) = sqrt((xA - xB)^2 + (yA - yB)^2)

#1.fenotip = 3 locatii pentru informare turistica

#2.genotip = codificarea celor 3 locatii in vector cu 2 componente fiecare pentru x si y

#3.forma individului => exemplu de individ: i = [2,5,0] si reprezinta indicii din lista de puncte

#4.spatiul solutiilor: finit ca avem 3 puncte distincte de gasit si daca tinem cont de ordine
# dimensiunea va fi n*(n-1)*(n-2), daca nu, va fi C(n,3)

#5.reprezentarea => vector de numere intregi, dar care vor fi de fapt indicii din lista de puncte
# de forma (x,y)

#6.restrictii: avem din enunt ca punctele trebuie sa fie distincte, dar nu avem restrictii sumplimentare

#7.fitness/fct obiectiv = suma de distante maxima deci fitness = suma distanțelor dintre cele 3 locații alese

#8.mutatie: inlocuire aleatoare fara duplicate

#9.recombinare: discreta/uniforma + reparare

#10.selectie: Pentru selecția părinților se poate utiliza selecția turneu: se aleg aleator mai mulți indivizi,
# iar cel cu fitness maxim este selectat ca părinte.

#11.conditia de terminare -> cand se atinge maximul sau cand se termina numarul de generatii dat

import random
import math

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

def generare_populatie(dim):
    populatie=[]

    for _ in range(dim):
        individ = random.sample(range(n), 3)
        populatie.append(individ)

    return populatie

def distanta(individ1, individ2):
    x1,y1 = puncte[individ1]
    x2,y2 = puncte[individ2]

    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def fitness(individ):
    return distanta(individ[0], individ[1]) + distanta(individ[1], individ[2]) + distanta(individ[2], individ[0])

def mutatie_inlocuire_aleatoare(individ):
    #incluiesc cu un indice care nu e deja in individ un indice din individ luat aleator
    copil = individ.copy()

    pozitie = random.randint(0,2)

    variante = []

    for indice in range(n):
        if indice not in individ:
            variante.append(indice)

    copil[pozitie] = random.choice(variante)
    return copil

def selectie_parinte_turneu(populatie, dim_turneu):
    candidati = random.sample(populatie, dim_turneu)

    cel_mai_bun = candidati[0]

    for individ in candidati:
        if fitness(individ) > fitness(cel_mai_bun):
            cel_mai_bun = individ

    return cel_mai_bun.copy()

def schema_generala_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ = mutatie_inlocuire_aleatoare(individ)
        populatie_noua.append(individ)

    return populatie_noua

def GA(dim_pop, nr_generatii, probabilitate_mutatie, dim_turneu):
    populatie = generare_populatie(dim_pop)

    for _ in range(nr_generatii):
        copii = []

        while len(copii) < dim_pop:
            parinte = selectie_parinte_turneu(populatie, dim_turneu)

            if random.random() < probabilitate_mutatie:
                copil = mutatie_inlocuire_aleatoare(parinte)
            else:
                copil = parinte.copy()

            copii.append(copil)

        total = copii + populatie
        total.sort(key=fitness, reverse=True)

        populatie = total[:dim_pop]

    return max(populatie, key=fitness)

solutie = GA(
    dim_pop = 20,
    nr_generatii = 100,
    probabilitate_mutatie = 0.1,
    dim_turneu = 5,
)

print("Solutie: ", solutie)
print("Fitness: ", fitness(solutie))
print("Punctele alese:", [puncte[i] for i in solutie])

