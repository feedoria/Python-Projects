# PROBLEMA — Comis-voiajor / TSP
#
# Se dau n orașe și o matrice cost, unde cost[i][j] reprezintă costul deplasării din orașul i în orașul j.
#
# Trebuie determinat un traseu care vizitează toate orașele exact o singură dată și revine la orașul de plecare,
# astfel încât costul total al traseului să fie minim.
#
# Un individ este o permutare a indicilor orașelor.
#
# Exemplu:
# Dacă individul este:
# [0, 3, 1, 2]
#
# atunci traseul este:
# 0 -> 3 -> 1 -> 2 -> 0
#
# Costul traseului este:
# cost[0][3] + cost[3][1] + cost[1][2] + cost[2][0]
#
# Cerințe:
#
# 1. Stabilește fenotipul. => determinarea unui traseu cu cost minim cu drumuri prin care se trece o singura data
# intorcandu se la primul oras (permutare circulara)
# 2. Stabilește genotipul. => permutare circulara cu indicii oraselor
# 3. Precizează forma unui individ. => [2,0,7,3] si traseul va fi 2->0->7->3->2 daca acesta este un traseu fezabil
# 4. Precizează spațiul soluțiilor. => finit, n! fiind o permutare circulara
# 5. Spune dacă problema are restricții sau nu. => Problema nu are restricții suplimentare în reprezentarea aleasă,
# deoarece permutarea garantează că fiecare oraș este vizitat exact o singură dată. Revenirea la orașul inițial este
# tratată în funcția cost.
# 6. Definește funcția cost. => cost = suma costurilor din orasul i la orasul j din individ
# 7. Definește funcția fitness. => trebuie minimizat costul deci fitness = 1/(1+cost)
# 8. Alege un operator de mutație potrivit.=> fiind o permutare circulara, potrivita ar fi interschimbarea mai putin,
#dar merge si aia; ar fi buna mutatia prin inversiune a unui segment? inserare? care e mai buna?
# 9. Alege un operator de recombinare potrivit.#recombinare cu OCX sau CX, PMX merge mai bine la permutare normala
# 10. Alege metoda de selecție a părinților.#selectia cu sus si fps cu sigma scalare este buna pentru modelul
# generational, dar facem momentan inca cu turneu
# 11. Alege metoda de selecție a generației următoare.#selectia se face prin elitism adica pastram dintre populatie si
# copii indivizii cu fitness cat mai mare cat sa incapa in dimensiunea predefinita a populatiei
# 12. Precizează condiția de terminare.=>se termina cand am atins numarul maxim de generatii sau optimul in cazul asta
# costul minim de traseu
# 13. Scrie funcțiile Python pentru:
#     - generarea populației inițiale;
#     - calculul costului;
#     - calculul fitness-ului;
#     - mutație;
#     - selecție turneu;
#     - GA simplificat.
import random

costuri = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

n = len(costuri)


def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = list(range(n))
        random.shuffle(individ)
        populatie.append(individ)

    return populatie


def cost_drum(individ):
    suma_costuri = 0

    for pozitie in range(n - 1):
        oras_curent = individ[pozitie]
        oras_urmator = individ[pozitie + 1]

        suma_costuri += costuri[oras_curent][oras_urmator]

    # întoarcerea de la ultimul oraș la primul
    ultimul_oras = individ[n - 1]
    primul_oras = individ[0]

    suma_costuri += costuri[ultimul_oras][primul_oras]

    return suma_costuri

# def cost_drum(individ):
#     suma_costuri = 0
#
#     for pozitie in range(n):
#         oras_curent = individ[pozitie]
#         oras_urmator = individ[(pozitie + 1) % n]
#
#         suma_costuri += costuri[oras_curent][oras_urmator]
#
#     return suma_costuri

def fitness(individ):
    return 1 / (1 + cost_drum(individ))

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

def selectie_parinte(populatie, dim_turneu):
    candidati = random.sample(populatie, dim_turneu)

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
            parinte = selectie_parinte(populatie, dim_turneu)

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
    nr_generatii=100,
    probab_mutatie=0.3,
    dim_turneu=3
)

print("Solutie:", solutie)
print("Cost:", cost_drum(solutie))
print("Fitness:", fitness(solutie))
print("Traseu complet: ", solutie + [solutie[0]])