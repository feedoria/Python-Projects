# PROBLEMA — Împărțirea studenților în două grupe echilibrate
#
# Se dau n studenți, unde n este număr par. Pentru fiecare student se cunoaște un nivel de experiență în programare,
# exprimat printr-un număr întreg.
#
# Trebuie să împărțim cei n studenți în două grupe cu același număr de membri, astfel încât diferența dintre suma nivelurilor
# de experiență ale celor două grupe să fie cât mai mică.
#
# O soluție trebuie să conțină toți studenții, fiecare student apărând exact o singură dată.
#
# Exemplu:
# experienta = [8, 3, 6, 10, 4, 7, 2, 9]
#
# Dacă un individ este:
# [0, 3, 5, 2, 1, 4, 6, 7]
#
# atunci:
# - prima jumătate reprezintă grupa 1;
# - a doua jumătate reprezintă grupa 2.
#
# Pentru exemplul de mai sus:
# grupa 1 = [0, 3, 5, 2]
# grupa 2 = [1, 4, 6, 7]
#
# Cerințe:
#
# 1. Stabilește fenotipul.=> 2 echipe de studenti cu diferenta cat mai mica de nivel de experienta
# 2. Stabilește genotipul.=> Genotipul este o permutare a indicilor studenților.
# Primele n/2 elemente formează prima grupă, iar ultimele n/2 elemente formează a doua grupă.
# 3. Precizează forma unui individ.=> Un individ reprezintă o împărțire completă a tuturor studenților în două grupe.
# Individul este o permutare de indici, nu o listă de niveluri de experiență.
# 4. Precizează spațiul soluțiilor.=>finit n!
# 5. Spune dacă problema are restricții sau nu.=>are restrictii integrate in problema: un student sa apara o singura data si echipele sa
#aiba nr egal de studenti
# 6. Definește funcția fitness.=> 1/(1+diferenta) diferenta = |suma nivel exp din echipa 1 - suma niv exp din ech 2|
# 7. Alege un operator de mutație potrivit.=> mutatie prin interschimbare
# 8. Alege un operator de recombinare potrivit.=> recombinare PMX/OCX
# 9. Alege metoda de selecție a părinților.=>selectie prin turneu ca e singura pe care o stiu:))))) sau mai sunt SUS/FPS + sigma scalare
#dar nu stiu ce inseamna :))))))
# 10. Alege metoda de selecție a generației următoare.=>elitism adica alegem pe cel cu fitness cat mai mare
# 11. Precizează condiția de terminare.=> cand se termina nr de generatii dat sau cand se atinge optimul
# 12. Scrie funcțiile Python pentru:
#     - generarea populației inițiale;
#     - calculul fitness-ului;
#     - mutație;
#     - selecție turneu;
#     - GA simplificat.
import random

experienta = [10, 8, 5, 0, 2, 9, 7, 4]  # n trebuie sa fie par

n = len(experienta)


def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = list(range(n))
        random.shuffle(individ)
        populatie.append(individ)

    return populatie


def fitness(individ):
    echipa1 = individ[:n // 2]
    echipa2 = individ[n // 2:]

    suma1 = 0
    suma2 = 0

    for student in echipa1:
        suma1 = suma1 + experienta[student]

    for student in echipa2:
        suma2 = suma2 + experienta[student]

    diferenta = abs(suma1 - suma2)

    return 1 / (1 + diferenta)


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


def selectare_parinte_turneu(populatie, dim_turneu):
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
            parinte = selectare_parinte_turneu(populatie, dim_turneu)

            if random.random() < probab_mutatie:
                copil = mutatie_interschimbare(parinte)
            else:
                copil = parinte.copy()

            copii.append(copil)

        total = copii + populatie
        total.sort(key=fitness, reverse=True)

        populatie = total[:dim_pop]

    return max(populatie, key=fitness)


solutie = GA(
    dim_pop=100,
    nr_gen=20,
    probab_mutatie=0.5,
    dim_turneu=5,
)

print("Solutie:", solutie)
print("Fitness:", fitness(solutie))
print("Echipa 1:", solutie[:n // 2])
print("Echipa 2:", solutie[n // 2:])

print("Valori echipa 1:", [experienta[i] for i in solutie[:n // 2]])
print("Valori echipa 2:", [experienta[i] for i in solutie[n // 2:]])