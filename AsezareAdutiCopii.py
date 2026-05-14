# # Problema — Așezarea adulților și copiilor la o masă circulară
# #
# # La o masă circulară cu n locuri trebuie așezate n persoane.
# # Dintre acestea, m sunt adulți, iar restul sunt copii.
# #
# # O așezare este considerată bună dacă fiecare copil are cel puțin un vecin adult.
# # Fiind masă circulară, primul loc este vecin cu ultimul loc.
# #
# # Se cere determinarea unei așezări astfel încât numărul copiilor care NU au niciun
# vecin adult
# # să fie minim.
# #
# # Date de test:
#
import random

n = 12
m = 5

# 1 = adult
# 0 = copil

def generare_populatie(dim):
    populatie = []

    for _ in range(dim):
        individ = []
        nr_adulti = 0
        for i in range(n):
            individ.append(random.randint(0,1))
            if individ[i] == 1:
                nr_adulti += 1

        while nr_adulti != m:
            pozitie = random.randint(0, n-1)
            individ[pozitie] = 1 - individ[pozitie]
            if individ[pozitie] == 1:
                nr_adulti += 1
            else:
                nr_adulti -= 1

        for i in range(0, n - 1):
            if abs(individ[i] - individ[i+1]) != 1:
                individ[i] = 1 - individ[i]

    return populatie
