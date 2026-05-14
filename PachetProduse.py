# PROBLEMA — Alegerea unui pachet de 5 produse
#
# Un magazin are n produse. Pentru fiecare produs se cunosc trei valori:
#
# - pretul produsului;
# - ratingul produsului;
# - popularitatea produsului.
#
# Trebuie să alegem 5 produse distincte pentru a forma un pachet promoțional.
#
# Scopul este să obținem un pachet cu rating total și popularitate totală cât mai mari, dar fără ca prețurile produselor alese să fie foarte dezechilibrate.
#
# Scorul unui pachet este:
#
# scor = suma ratingurilor produselor alese
#        + suma popularităților produselor alese
#        - penalizare
#
# Penalizarea este egală cu diferența dintre cel mai mare preț și cel mai mic preț dintre produsele alese.
#
# Cu alte cuvinte, vrem să alegem 5 produse bune și populare, dar cu prețuri cât de cât apropiate.
#
# Cerințe:
#
# 1. Stabilește fenotipul. => alegerea a 5 produse distincte cu rating si popularitate maxima (scor maxim)
# 2. Stabilește genotipul.  => codificarea fiecarui produs ca un vector cu 3 componente
# 3. Precizează forma unui individ. => o lista care contine pozitiile produselor in vectorul de produse
# 4. Precizează spațiul soluțiilor. => finit, daca conteaza ordinea n*(n-1)*(n-2)*(n-2)*(n-4) si daca nu dimensiunea e C(n,5)
# 5. Spune dacă problema are restricții sau nu. => avem restrictie integrata in problema ca produsele sa fie diferite
# 6. Definește funcția fitness. => fitness = scor
# 7. Alege un operator de mutație potrivit. => mutatie cu inlocuire aleatoare fara duplicate
# 8. Alege un operator de recombinare potrivit. => recombinare discreta/uniforma fara duplicate deci cu reparare
# 9. Alege metoda de selecție a părinților. => selectie turneu
# 10. Alege metoda de selecție a generației următoare. => elitism adica cu fitness cat mai mare
# 11. Precizează condiția de terminare. => cand se termina nr de generatii dat sau cand s a atins maximul
# 12. Scrie funcțiile Python pentru:
#     - generarea populației inițiale;
#     - calculul fitness-ului;
#     - mutație;
#     - selecție turneu;
#     - GA simplificat.

#consideram rating maxim 5 si popularitate maxima 10
import random

produse = [
    [20, 8, 7],
    [35, 9, 6],
    [15, 6, 9],
    [40, 10, 5],
    [25, 7, 8],
    [30, 8, 10],
    [18, 5, 7],
    [45, 9, 9]
]

n = len(produse)


def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = random.sample(range(n), 5)
        populatie.append(individ)

    return populatie


def fitness(individ):
    suma_ratinguri = 0
    suma_popularitate = 0
    preturi = []

    for indice_produs in individ:
        pret = produse[indice_produs][0]
        rating = produse[indice_produs][1]
        popularitate = produse[indice_produs][2]

        suma_ratinguri += rating
        suma_popularitate += popularitate
        preturi.append(pret)

    penalizare = max(preturi) - min(preturi)

    scor = suma_ratinguri + suma_popularitate - penalizare

    return scor


def mutatie_inlocuire_aleatoare(individ):
    copil = individ.copy()

    pozitie = random.randint(0, 4)

    variante = []

    for indice in range(n):
        if indice not in copil:
            variante.append(indice)

    copil[pozitie] = random.choice(variante)

    return copil


def schema_generala_mutatie(populatie, probabilitate_mutatie):
    populatie_noua = []

    for individ in populatie:
        if random.random() < probabilitate_mutatie:
            individ = mutatie_inlocuire_aleatoare(individ)

        populatie_noua.append(individ)

    return populatie_noua


def selectie_turneu(populatie, dim_turneu):
    candidati = random.sample(populatie, dim_turneu)

    cel_mai_bun = candidati[0]

    for candidat in candidati:
        if fitness(candidat) > fitness(cel_mai_bun):
            cel_mai_bun = candidat

    return cel_mai_bun.copy()

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


def GA(dim_pop, nr_gen, probabilitate_mutatie, dim_turneu):
    populatie = generare_populatie(dim_pop)

    for _ in range(nr_gen):
        copii = []

        while len(copii) < dim_pop:
            parinte = selectie_turneu(populatie, dim_turneu)

            if random.random() < probabilitate_mutatie:
                copil = mutatie_inlocuire_aleatoare(parinte)
            else:
                copil = parinte.copy()

            copii.append(copil)

        total = populatie + copii
        total.sort(key=fitness, reverse=True)

        populatie = total[:dim_pop]

    return max(populatie, key=fitness)


solutie = GA(
    dim_pop=20,
    nr_gen=100,
    probabilitate_mutatie=0.1,
    dim_turneu=5
)

print("Solutie:", solutie)
print("Fitness:", fitness(solutie))
print("Produsele alese:", [produse[i] for i in solutie])