# PROBLEMA — N-regine
#
# Se consideră o tablă de șah de dimensiune n x n. Trebuie să așezăm n regine pe tablă
# astfel încât numărul de perechi de regine care se atacă să fie minim.
#
# O regină atacă o altă regină dacă se află pe aceeași linie,
# aceeași coloană sau aceeași diagonală.
#
# Pentru a evita automat atacurile pe linii și coloane, folosim o reprezentare prin permutare.
#
# Un individ este o permutare p de lungime n, unde:
# p[i] = coloana pe care se află regina de pe linia i.
#
# Exemplu:
# Pentru n = 4, individul:
#
# [2, 0, 3, 1]
#
# înseamnă:
# - pe linia 0, regina este în coloana 2;
# - pe linia 1, regina este în coloana 0;
# - pe linia 2, regina este în coloana 3;
# - pe linia 3, regina este în coloana 1.
#
# Fiind permutare, nu există două regine pe aceeași linie sau pe aceeași coloană.
# Trebuie verificate doar diagonalele.
#
# Două regine aflate pe liniile i și j se atacă pe diagonală dacă:
#
# abs(i - j) == abs(p[i] - p[j])
#
# Cerințe:
#
# 1. Stabilește fenotipul. => plasarea reginelor pe tabla de sah astfel incat sa fie numar cat mai mic
# de perechi de regine care se ataca
# 2. Stabilește genotipul. => vom folosi permutarea pentru a asigura prin aceasta unicitatea reginelor
# si in permutare retinem indicele liniei pe care se afla reprezentand pozitia in lista, iar
# continutul listei permutarii reprezinta valoarea pozitiei coloanei din tabla de sah
# 3. Precizează forma unui individ. => i,j vor reprezenta linia si p[i], p[j] vor reprezenta coloana
# unde matrice cu indice i p[i] e o regina si matrice de j so p[j] e alta regina
# iar un individ arata asa : [2,0,5,3] si de exemplu o regina pe tabla de sah se afla la coordonatele
# in matrice [0][2] respectiv alta regina la [1][0] samd
# 4. Precizează spațiul soluțiilor.=> finit, n! pentru ca e permutare
# 5. Spune dacă problema are restricții sau nu.
#Nu există restricții suplimentare în reprezentarea aleasă, deoarece permutarea garantează
# că fiecare regină se află pe o linie diferită și pe o coloană diferită.
# Rămân de evaluat doar conflictele pe diagonale, tratate prin funcția cost.
#
# => restrictia va fi ca doua regine sa nu se afle pe
# acelasi loc in tabla de sah, dar unicitatea este garantata de reprezentarea aleasa adica prin
# permutare
# 6. Definește funcția cost.=> numarul perechilor de regine care se ataca pe diagonala
# adica daca se adevereste abs(i-j) == abs(p[i] - p[j]) crestem un contor
# 7. Definește funcția fitness. => pentru ca este problema de minimizare a costului
# fitness = 1/(1+cost)
# 8. Alege un operator de mutație potrivit.=>interschimbare
# 9. Alege un operator de recombinare potrivit.=>PMX sau OCX fiind permutare
# 10. Alege metoda de selecție a părinților.=>turneu voi face dar trebuie cu sus si fps cu sigma scalare
# 11. Alege metoda de selecție a generației următoare.=> Se reunesc populația curentă și copiii,
# apoi se păstrează cei mai buni dim_pop indivizi după fitness.
# 12. Precizează condiția de terminare.=. se termina cand se ajunge la nr maxim de generatii sau
# cand se atinge optimul
# 13. Scrie funcțiile Python pentru:
#     - generarea populației inițiale;
#     - calculul costului;
#     - calculul fitness-ului;
#     - mutație;
#     - selecție turneu;
#     - GA simplificat.
import random

from matplotlib.cbook import index_of

n = 8

def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = list(range(n))
        random.shuffle(individ)
        populatie.append(individ)

    return populatie


def cost(individ):
    conflicte = 0

    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(individ[i] - individ[j]):
                conflicte += 1

    return conflicte

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

    for candidat in candidati:
        if fitness(candidat) > fitness(cel_mai_bun):
            cel_mai_bun = candidat

    return cel_mai_bun.copy()

def GA(dim_pop, nr_gen, probab_mutatie, dim_turneu):
    populatie = generare_populatie(dim_pop)

    for _ in range(nr_gen):
        copii = []

        while len(copii) < dim_pop:
            parinte = selectie_parinte_turneu(
                populatie,
                dim_turneu
            )
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
    dim_pop = 8,
    nr_gen = 100,
    probab_mutatie = 0.1,
    dim_turneu = 5,
)

print("Solutie:", solutie)
print("Fitness: ", fitness(solutie))
print("Cost: ", cost(solutie))
