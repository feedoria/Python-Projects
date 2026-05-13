# PROBLEMA — Alegerea unei echipe de 4 angajați
#
# O firmă are n angajați. Pentru fiecare angajat se cunosc două valori:
#
# - competența tehnică;
# - capacitatea de colaborare.
#
# Trebuie să alegem 4 angajați distincti pentru formarea unei echipe de proiect, astfel încât scorul echipei să fie maxim.
#
# Scorul unei echipe este calculat astfel:
#
# scor = suma competențelor tehnice ale celor 4 angajați
#        + suma capacităților de colaborare ale celor 4 angajați
#        - penalizare
#
# Penalizarea este egală cu diferența dintre cea mai mare competență tehnică și cea mai mică competență tehnică din echipă.
#
# Cu alte cuvinte, vrem o echipă cu scor mare, dar și cât de cât echilibrată tehnic.
#
# Cerințe:
#
# 1. Stabilește fenotipul. = gasirea celor 4 angajati care dau scorul echipei maxim
# 2. Stabilește genotipul. = Genotipul este un vector de 4 indici distincți [i, j, k, l].
# Fiecare indice indică un angajat din lista angajaților.
# 3. Precizează forma unui individ. => daca avem individ = [2,5,0,7] inseamna ca 2,5,0,7 sunt pozitiile angajatilor din
# lista de angajati (de vectori de 2 componente)
# 4. Precizează spațiul soluțiilor. => finit , daca cont ordinea e n*(n-1)*(n-2)*(n-3) si daca nu e: C(n,4)
# 5. Spune dacă problema are restricții sau nu. => are restrictie in problema ca angajatii sa fie diferiti,
# dar putem incorpora asta deja daca bagam in populatie din start prin random.sample(range(n), 4)
# 6. Definește funcția fitness. => fitness = scorul si e optim cand e maxim scorul calculat
# 7. Alege un operator de mutație potrivit. => mutatie prin inlocuire aleatoare dar fara duplicate care sunt deja in individ
# 8. Alege un operator de recombinare potrivit. => discreta/uniforma cu reparare ca sa nu avem dubluri
# 9. Alege metoda de selecție a părinților.=> turneu -> luam candidati random din populatie si in functie de fitness il
#luam pe cel mai bun
# 10. Alege metoda de selecție a generației următoare.=>Selecția generației următoare = elitism.
# 11. Precizează condiția de terminare.
# 12. Scrie funcțiile Python pentru:
#     - generarea populației inițiale;
#     - calculul fitness-ului;
#     - mutație;
#     - selecție turneu;
#     - GA simplificat.

import random
import math

angajati = [
    [10,8],
    [9,10],
    [5,3],
    [10,2],
    [2,8],
    [7,7]
]

n = len(angajati)

def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = random.sample(range(n), 4)
        populatie.append(individ)

    return populatie

# deci asta returneaza un scor pentru fiecare echipa
def fitness(individ):
    suma_competente = 0
    suma_colaborare = 0
    competente_tehnice = []

    for indice_angajat in individ:
        competenta = angajati[indice_angajat][0]
        colaborare = angajati[indice_angajat][1]

        suma_competente += competenta
        suma_colaborare += colaborare
        competente_tehnice.append(competenta)

    penalizare = max(competente_tehnice) - min(competente_tehnice)

    scor = suma_competente + suma_colaborare - penalizare

    return scor

def mutatie_inlocuire_aleatoare(individ):
    copil = individ.copy()

    pozitie = random.randint(0,3)

    variante = []

    for indice in range(n):
        if indice not in individ:
            variante.append(indice)

    copil[pozitie] = random.choice(variante)
    return copil

def schema_generala_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ = mutatie_inlocuire_aleatoare(individ)
        populatie_noua.append(individ)

    return populatie_noua

def selectie_parinte_turneu(populatie,dim_turneu):
    candidati = random.sample(populatie, dim_turneu)
    cel_mai_bun = candidati[0]

    for candidat in candidati:
        if fitness(candidat) > fitness(cel_mai_bun):
            cel_mai_bun = candidat

    return cel_mai_bun.copy()

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



