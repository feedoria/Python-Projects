# PROBLEMA — Alegerea unor cursuri opționale
#
# O studentă are la dispoziție n cursuri opționale. Pentru fiecare curs se cunosc:
#
# - numărul de ore necesare pe săptămână;
# - utilitatea cursului pentru carieră.
#
# Studenta poate aloca cel mult H ore pe săptămână pentru aceste cursuri.
#
# Trebuie să aleagă o submulțime de cursuri astfel încât utilitatea totală să fie maximă,
# fără să depășească limita de H ore.
#
# Un curs poate fi ales sau nu.
#
# Cerințe:
#
# 1. Stabilește fenotipul.=> alegerea unei submultimi de cursuri pentru utilitate totala si incadrare in H ore
# 2. Stabilește genotipul.=>Genotipul este un vector binar de lungime n.
# Fiecare poziție corespunde unui curs.
# Valoarea 1 înseamnă că alegem cursul, iar valoarea 0 înseamnă că nu îl alegem.
# 3. Precizează forma unui individ.=>individul este intregul vector binar 0-neales 1-ales pentru lista de
#cursuri data
# 4. Precizează spațiul soluțiilor.=>finit dimensiunea e 2^n
# 5. Spune dacă problema are restricții sau nu.=> avem restrictia sa nu se depaseaza H ore pe sapt
# 6. Definește funcția fitness. => fitness = suma utilitatilor
#Dacă individul nu este fezabil, îl respingem sau îi dăm fitness 0.
# 7. Alege un operator de mutație potrivit.=> bitflip (nu stiu cum se face totusi) se interschimba random
# un 1 cu un 0?
# 8. Alege un operator de recombinare potrivit.=>crossover unipunct/multipunct sau uniforma?
# 9. Alege metoda de selecție a părinților.=>turneu ca e singura pe care o stiu=>>>>>
# 10. Alege metoda de selecție a generației următoare.=>elitism -> se iau indivizii cu fitness cat mai mare
# 11. Precizează condiția de terminare.=>cand se atinge utilitatea maxima sau cand se termina nr de gen dat


#----------------------------------------------------------
# 1. Fenotip = submulțimea de cursuri alese.
#
# 2. Genotip = vector binar de lungime n, unde gena i este 1 dacă alegem cursul i și 0 dacă nu îl alegem.
#
# 3. Forma individului = [0,1,1,0,...], cu valori în {0,1}.
#
# 4. Spațiul soluțiilor = finit, de dimensiune 2^n.
#
# 5. Problema are restricții, deoarece suma orelor cursurilor alese trebuie să fie cel mult H.
#
# 6. Fitness = suma utilităților cursurilor alese, dacă individul este fezabil. Dacă nu este fezabil, fitness = 0 sau individul este respins.
#
# 7. Mutație = bitflip, adică se alege o poziție și valoarea 0 devine 1, iar 1 devine 0.
#
# 8. Recombinare = crossover unipunct / multipunct / uniform.
#
# 9. Selecție părinți = selecție turneu.
#
# 10. Selecție generație următoare = elitism.
#
# 11. Terminare = număr maxim de generații sau atingerea unei soluții optime.
#-------------------------------------------------------

# 12. Scrie funcțiile Python pentru:
#     - generarea populației inițiale;
#     - verificarea fezabilității;
#     - calculul fitness-ului;
#     - mutație;
#     - selecție turneu;
#     - GA simplificat.
import random

lista_cursuri = ["Algebra", "Analiza", "Robotica", "Japoneza","Italiana"]
lista_info = [[5,7],[7,6],[3,10],[6,10],[2,4]]
H = 15

n = len(lista_cursuri)

def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = []
        for i in range(n):
            individ.append(random.randint(0, 1))

        populatie.append(individ)
    return populatie
#trebuie sa avem cursuri sa se incadreze in H ore pe saptamana si utilitatea sa fie maxima
#deci calculam suma utilitatilor dintr o lista de indivizi si suma cu numarul lor de ore
def fitness(individ):
    nr_ore = 0
    suma_utilitati = 0

    for indice in range(len(individ)):
        if individ[indice] == 1:
            nr_ore += lista_info[indice][0]
            suma_utilitati += lista_info[indice][1]

    if nr_ore <= H:
        return suma_utilitati
    else:
        return 0

def numar_ore_pe_saptamana(individ):
    nr_ore = 0
    for indice in range(len(individ)):
        if individ[indice] == 1:
            nr_ore += lista_info[indice][0]
    return nr_ore

#un 1 il transformam in 0 sau invers
def mutatie_bitflip(individ):
    copil = individ.copy()

    pozitie = random.randint(0, len(individ)-1)

    copil[pozitie] = 1 - copil[pozitie]

    if numar_ore_pe_saptamana(copil) > H:
        copil[pozitie] = 1 - copil[pozitie] #daca nu respecta restrictia de timp ne intoarcem la initial

    return copil

def schema_generala_mutatie(populatie, pm):
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm:
            individ = mutatie_bitflip(individ)
        populatie_noua.append(individ)
    return populatie_noua

def selectare_parinte_turneu(populatie,dim_turneu):
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
            parinte = selectare_parinte_turneu(populatie, dim_turneu)

            if random.random() < probab_mutatie:
                copil = mutatie_bitflip(parinte)
            else:
                copil = parinte.copy()

            copii.append(copil)

        total = copii + populatie
        total.sort(key=fitness, reverse=True)

        populatie = total[:dim_pop]

    return max(populatie, key=fitness)

