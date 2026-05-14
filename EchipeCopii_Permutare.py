# Un grup de n copii (număr par) vor să formeze două echipe (număr egal) de fotbal pentru un meci
# amical.
# Valoarea fiecărui jucător este estimată printr-un numär intreg intre 1 șı 10.
# Utilizați un algoritm genetic pentru a realiza o împărțire a grupului astfel încit valorile echipelor
# să fie cît mai apropiate
# (valoarea unei echipe e dată de suma valorilor jucătorilor). n este o valoare întreagă între 10 și 20.
# Note:
# • Răspunsurile corecte pentru întrebările 2-11 consideră reprezentarea corectă, aleasă în întrebarea 1.
# • Răspunsurile corecte pentru întrebarea 12 consideră alegerile corecte la întrebările anterioare.

#1. Fenotip
# impartirea echipelor in 2 echipe egale numeric

#2. Genotip
#codificarea solutiei
# alegem: permutarea indicilor copiilor
# primele n/2 pozitii = echipa 1
# ultimele n/2 pozitii = echipa 2

#3. Forma individului
# un individ este o permutare de la 0 la n-1
# adica fiecare copil apare exact o data

#4. Spatiul solutiilor
# individul fiind o permutare -> spatiul este finit, n!

#5. Restrictii
# problema cere sa fie 2 echipe cu nr egal de copii
# fiecare copil sa fie intr o singura echipa
# reprezentarea individului fiind prin permutare sunt incluse acestea
# deci nu avem restrictii suplimentare

#6. Functia obiectiv/fitness
# vrem ca cele 2 echipe sa fie cat mai apropiate
# suma1 = suma val din ech 1
# suma2 = suma val din ech 2
# diferenta = |suma1 - suma2|
# -> problema este de MINIMIZARE A DIFERENTEI
# dar GA de obicei lucreaza cu minimizare deci
# -> functia fitness = 1 / (1 + diferenta)

#7. Modelul populational
# alegem modelul generational cu pop de dimensiune constanta
# adica pornim de la o populatie de dim indivizi
# generam descendenti
# alegem generatia urmatoare
# mentinem dimensiunea pop constanta

#8. Selectia parintilor
# se poate utiliza SUS cu FPS si sigma-scalare
# pentru ca indivizii cu fitness mai mare trebuie sa aiba sanse mai mari in reproducere

#9. Recombinare
# NU alegem crossovr unipunct simplu pentru ca poate produce duplicate
# alegem PMX/OCX
# PMX pastreaza proprietatea de permutare, adica fiecare copil apare o data

#10. Mutatie
# pentru permutare cea mai simpla mutatie este INTERSCHIMBAREA A 2 POZITII

#11. Selectia urmatoarei generatii
# alegem ELITISM
# adica pastram cei mai buni indivizi

#12. Conditia de terminare
#algo se opreste dupa un nr max de generatii sau cand s a atins val maxima a functiei obiectiv

import random #biblioteca care ne ajuta sa genera lucruri aleatoare

valori = [7, 3, 9, 5, 4, 8, 2, 6, 1, 10] # copilul cu indecele 0 are valoarea 7
# deci cand in individ vad valoarea 5 -> inseamna copilul cu indicele 5 care are valoarea 8
n = len(valori)

#genereaza dim permutari ale copiilor si returneaza populatia
def genereaza_populatie(dim): #dim = cati indivizi vrem sa generam
    populatie = []

    for _ in range(dim):
        individ = list(range(n)) # aici construim  lista cu indicii copiilor
        # daca n = 10 -> transforma asta in lista: [0,1,2,3,4,5,6,7,8,9] -> asta e indiv initial inainte
        # sa l amestecam
        random.shuffle(individ) #aici amestecam lista individ (modifica lista direct nu return o lista noua)
        populatie.append(individ) #adaug individul in populatie

    return populatie

#calculeaza cat de bun este un individ
def fitness(individ):
    echipa1 = individ[:n // 2] #ia elem de la inceput pana la n/2 EXCLUSIV
    echipa2 = individ[n // 2:]

    suma1 = 0
    suma2 = 0

    for copil in echipa1:
        suma1 += valori[copil]

    for copil in echipa2:
        suma2 += valori[copil]

    diferenta = abs(suma1 - suma2)

    return 1/ (1 + diferenta) # daca diferenta este mica, fitness ul este mare => sol perf are fit 1

def mutatie_interschimbare(individ):
    copil = individ.copy()

    i, j = random.sample(range(n), 2) # alege 2 valori diferite (si nu ia de ex 2 si 2 in acelasi timp)

    copil[i], copil[j] = copil[j], copil[i]

    return copil

def schema_generala_mutatie(populatie, pm): # pm = probabilitatea de mutatie
    populatie_noua = []

    for individ in populatie:
        if random.random() < pm: # random.random() genereaza un nr aleator intre 0 si 1
            individ = mutatie_interschimbare(individ)

        populatie_noua.append(individ)

    return populatie_noua

import random

def probabilitati_fps_sigma_scalare(populatie, c=2):
    # 1. Calculez fitness-ul fiecarui individ
    valori_fitness = []

    for individ in populatie:
        valori_fitness.append(fitness(individ))

    # 2. Calculez media fitness-urilor
    media = sum(valori_fitness) / len(valori_fitness)

    # 3. Calculez sigma = deviatia standard
    suma_patrate = 0

    for valoare in valori_fitness:
        suma_patrate += (valoare - media) ** 2

    sigma = (suma_patrate / len(valori_fitness)) ** 0.5

    # 4. Aplic sigma-scalarea
    valori_scalate = []

    for valoare in valori_fitness:
        g = max(valoare - (media - c * sigma), 0)
        valori_scalate.append(g)

    # 5. Transform valorile scalate in probabilitati FPS
    suma_scalata = sum(valori_scalate)

    probabilitati = []

    if suma_scalata == 0:
        # daca toate valorile sunt 0, alegem uniform
        for _ in populatie:
            probabilitati.append(1 / len(populatie))
    else:
        for valoare in valori_scalate:
            probabilitati.append(valoare / suma_scalata)

    return probabilitati

def selectie_SUS_sigma_scalare(populatie, nr_parinti):
    # 1. Calculez probabilitatile FPS cu sigma-scalare
    probabilitati = probabilitati_fps_sigma_scalare(populatie)

    # 2. Construiesc distributia cumulata
    cumul = []
    suma = 0

    for p in probabilitati:
        suma += p
        cumul.append(suma)

    # 3. Generez punctele SUS
    parinti = []

    pas = 1 / nr_parinti
    start = random.uniform(0, pas)

    puncte = []

    for k in range(nr_parinti):
        puncte.append(start + k * pas)

    # 4. Pentru fiecare punct, gasesc individul corespunzator in distributia cumulata
    i = 0

    for punct in puncte:
        while i < len(cumul) - 1 and punct > cumul[i]:
            i += 1

        parinti.append(populatie[i].copy())

    return parinti


def GA(dim, nr_gen, pm): #nr_gen = nr de generatii/iteratii, pm=probab de mutatie
    populatie = genereaza_populatie(dim)

    for _ in range(nr_gen):
        copii = schema_generala_mutatie(populatie) # aplicam mutatia curenta si obt o populatie de copii
        # aici copiii = indivizii obtinuti dupa mutatie
        total = populatie + copii #combinam pop veche cu pop de copii
        # ex: daca pop veche are 20 indivizi si copii are 20 de indivizi => total = 40
        total.sort(key=fitness, reverse=True) #sortam lista total dupa fitness
        # reverse=True inseamna in ord descrescatoare => cel mai bun indiv va fi primul

        populatie = total[:dim] # pastram doar primii indivizi adica cei mai buni

    return max(populatie, key=fitness) #returnam cel mai bun individ din populatie

solutie = GA(dim=20, nr_gen=50, pm=0.1)

print("Solutie:", solutie)
print("Fitness:", fitness(solutie))
print("Echipa 1:", solutie[:n//2])
print("Echipa 2:", solutie[n//2:])













