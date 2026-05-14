# PROBLEMA — Aranjarea circulară a unor melodii
#
# Se dau n melodii, fiecare melodie având un nivel de energie exprimat printr-un număr întreg.
#
# Trebuie să aranjăm toate cele n melodii într-o ordine circulară pentru un playlist de petrecere,
# astfel încât diferențele de energie dintre melodii vecine să fie cât mai mici.
#
# Fiind o aranjare circulară, ultima melodie este considerată vecină cu prima melodie.
#
# Pentru un individ care reprezintă o permutare a melodiilor, costul este:
#
# cost = |energie[p[0]] - energie[p[1]]|
#      + |energie[p[1]] - energie[p[2]]|
#      + ...
#      + |energie[p[n-1]] - energie[p[0]]|
#
# Trebuie să minimizăm acest cost.
#
# Cerințe:
#
# 1. Stabilește fenotipul. => Fenotipul este aranjarea circulară a celor n melodii astfel încât
# diferențele de energie dintre melodii vecine să fie cât mai mici.
# 2. Stabilește genotipul. => codificarea prin permutare a indicilor melodiilor
# 3. Precizează forma unui individ. [2,3,5,0,1,6,4] pentru n = 7
# 4. Precizează spațiul soluțiilor. => finit, n!
# 5. Spune dacă problema are restricții sau nu. => Problema nu are restricții suplimentare în reprezentarea
# aleasă, deoarece individul este o permutare și fiecare melodie apare exact o singură dată.
# Caracterul circular este tratat în funcția cost, unde ultimul element este legat de primul.
# 6. Definește funcția cost. cost = suma diferențelor absolute dintre energiile melodiilor vecine.
# 7. Definește funcția fitness. fitness/fct obiectiv = 1/(1+cost)
# 8. Alege un operator de mutație potrivit. => interschimbare/inversiune
# 9. Alege un operator de recombinare potrivit. => PMX/OCX
# 10. Alege metoda de selecție a părinților. => turneu sau SUS cu FPS si sigma scalare
# 11. Alege metoda de selecție a generației următoare. => elitism adica luam indivizii cu cel mai mare fitness
# 12. Precizează condiția de terminare. => cand s a atins numarul maxim de generatii sau cand s a atins optimul
# 13. Scrie funcțiile Python pentru:
#     - generarea populației inițiale;
#     - calculul costului;
#     - calculul fitness-ului;
#     - mutație;
#     - selecție turneu;
#     - GA simplificat.

import random

energie = [
    70,
    100,
    20,
    45,
    67,
    90
]

n = len(energie)

def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = list(range(n))
        random.shuffle(individ)
        populatie.append(individ)

    return populatie

def cost(individ):
    suma = 0

    for indice in range(n - 1):
        indice_vecin = indice + 1
        diferenta = abs(energie[individ[indice]] - energie[individ[indice_vecin]])
        suma += diferenta

    diferenta = abs(energie[individ[n - 1]] - energie[individ[0]])
    suma += diferenta

    return suma

def fitness(individ):
    return 1/(1+cost(individ))

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

def selectie_parinte_turneu(populatie, dim_turneu):
    candidati = random.sample(populatie, dim_turneu)

    cel_mai_bun = candidati[0]

    for individ in candidati:
        if fitness(individ) > fitness(cel_mai_bun):
            cel_mai_bun = individ

    return cel_mai_bun.copy()

def GA(dim_pop, nr_gen, probab_mutatie, dim_turneu):
    populatie = generare_populatie(dim_pop)

    for _ in range(nr_gen):
        copii = []
        while len(copii) < dim_pop:
            parinte = selectie_parinte_turneu(populatie, dim_turneu)

            if random.random() < probab_mutatie:
                copil = mutatie_interschimbare(parinte)
            else:
                copil = parinte.copy()

            copii.append(copil)

        total = copii + populatie
        total.sort(key = fitness, reverse = True)

        populatie = total[:dim_pop]

    return max(populatie, key = fitness)

solutie = GA(
    dim_pop=20,
    nr_gen=100,
    probab_mutatie = 0.5,
    dim_turneu = 5,
)

print("Solutie: ", solutie)
print("Fitness: ", fitness(solutie))
print("Cost:", cost(solutie))
print("Energii in ordine:", [energie[i] for i in solutie])




