import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dviread import find_tex_file


def fitness(x):
    n = len(x)
    nr = 0

    for i in range(n-1):
        for j in range(i+1,n):
            if x[i] < x[j]:
                nr +=1

    return nr

# punctul a) -> generare populatie

def generare_populatie(n, dim):
    populatie = np.zeros([dim, n+1], dtype = int)

    for i in range(dim):
        permutare = np.random.permutation(n)
        populatie[i][:-1] = permutare
        populatie[i][-1] = fitness(permutare)

    return populatie

def mutatie_interschimbare(x): # x reprezinta o permutare si trb sa alegem la intamplare 2 elemente si sa le schimbam intre ele
    copie = np.copy(x)
    n = len(x)
    poz = [i for i in range(n)]

    i = random.choice(poz)
    poz.remove(i)
    j = random.choice(poz)

    copie[i], copie[j] = copie[j], copie[i]

    return copie

def mutatie_populatie(populatie, p): # avem nev si de propabilitate de mutatie pentru fiecare individ
    dim = populatie.shape[0]
    n = populatie.shape[1] - 1

    copie = np.copy(populatie)
    for i in range(dim):
        pb = np.random.uniform(0, 1)
        if pb <= p:
            copie[i][:-1] = mutatie_interschimbare(copie[i][:-1])
            copie[i][-1] = fitness(copie[i][:-1])

if __name__ == '__main__':
    n = 8
    dim = 50
    p = 0.2


    populatie = generare_populatie(n, dim)
    print(populatie)

    populatie_mutata = mutatie_populatie(populatie, p)


    plt.plot([populatie[i][-1] for i in range(dim)], 'bs', ms=12,
             label='populatie initiala')
    plt.plot([populatie[i][-1] for i in range(dim)], 'rs', ms=5,
             label='populatie mutata')  # bs = blue square si ms = marker size
    plt.legend()
    plt.ylabel('Fitness')
    plt.xlabel('Generation')
    plt.show()

# ---------ex 1 -----------


# import numpy as np
# import matplotlib.pyplot as plt
# from math import sin
#
# import sigma
#
#
# def fitness(x): # x va fi un vector cu 4 elem
#     return 1 + sin(2*x[0] - x[2]) + (x[1]*x[3]) ** (1/3)
#
# def generare_populatie(dim, a, b): # a = vectorul cu inceputul intervalelor in care sunt x1, x2, x3, x4 si b = vector cu capatul din dr a interv
#     p = []
#     for i in range(dim):
#         v = np.random.uniform(a, b, 4)
#         fit = fitness(v)
#         # p.append((v, fit))
#         p.append([v, fit])
#     return p
#
# def mutatie_individ(x, a, b): # a si b vor fi niste numere: capetele unui interval ; x este doar un element dintre: x1,x2,x3,x4 nu vctr
#     copie = np.copy(x)
#     e = np.random.normal(0, sigma) # 0 = centrul distributiei si sigma parametrul primit
#     y = x + e # e poate sa fie >0 sau <0
#     if y < a:
#         y = a
#     elif y > b:
#         y = b
#     return y  # am modificat un singur numar, ii dau intervalele care sunt si pot sa il modific
#
# def mutatie_populatie(populatie, a, b, sigma, dim, p): # a si b sunt vectori si p probabilitatea de mutatie
#     m_populatie = populatie.copy()
#     for i in range(dim):
#         mutat = False
#         for j in range(4): # cele 4 elem ale fiecarui individ
#             if np.random.uniform(0, 1) < p:
#                 # atunci individul sufera o mutatie:
#                 m_populatie[i][j] = mutatie_individ(m_populatie[i][j], a[j], b[j], sigma) # a si b lim interv pt elem meu
#                 mutat = True
#         if mutat == True:
#             m_populatie[i][4] = fitness(m_populatie[i][:4]) # :4 -> pana la 4
#             print("Elementul mutat: ")
#     return populatie
#
# if __name__ == "__main__":
#     a = [-1, 0, 0 , 0]
#     b = [1, 0.2, 1, 5]
#     dim = 50
#     sigma = 0.2
#     populatie = generare_populatie(dim, a, b)
#     print(populatie)
#     m_pop = mutatie_populatie(populatie, a, b, sigma, dim, 0.1) # este rezultat(populatie) in urma mutatiei
#     print(m_pop)
#
#     plt.plot([populatie[i][-1] for i in range(dim)], 'bs', ms = 10, label = 'populatie')
#     plt.legend()
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.show()
