#Подсчёт количества правильных семейств из квадратичных и линейных функций от 3 переменных и проверка на треугольность

import itertools as it
from math import ceil
import numpy as np
import multiprocessing
from ipynb.fs.full.my_functions import check_3
from functools import partial
import copy

#Создаём набор из 10 коэффициентов для квадратичных функций(по порядку: x^2, y^2, z^2, xy, xz, yz, x, y, z, c)

coef = np.array(tuple(it.product((0,1,2), repeat = 10)))

#Отбираем наборы коэффициентов, в которых есть хотя бы один ненулевой при квадратичном члене

coef = coef[(coef[:, 0] != 0) | (coef[:, 1] != 0) | (coef[:, 2] != 0) | (coef[:, 3] != 0) | (coef[:, 4] != 0) | (coef[:, 5] != 0)]

#f_0 - кортеж квадратичных функций (каждая функция задаётся наборов коэффициентов), не зависящих от x, f_1 - от y, f_2 - от z. В переменной iterator находятся семейства-кандидаты на правильность (элементы декартова произведения f_0 x f_1 x f_2)

f_0 = coef[(coef[:,0]==0) & (coef[:,3]==0) & (coef[:,4]==0) & (coef[:,6]==0)]
f_0 = tuple(map(tuple, f_0))
f_1 = coef[(coef[:,1]==0) & (coef[:,3]==0) & (coef[:,5]==0) & (coef[:,7]==0)]
f_1 = tuple(map(tuple, f_1))
f_2 = coef[(coef[:,2]==0) & (coef[:,4]==0) & (coef[:,5]==0) & (coef[:,8]==0)]
f_2 = tuple(map(tuple, f_2))

#Создаём набор из 10 коэффициентов для линейных функций в том же формате, что и для квадратичных (по порядку: x^2, y^2, z^2, xy, xz, yz, x, y, z, c)

coef_1 = np.array(tuple(it.product((0,1,2), repeat = 10)))

#Отбираем линейные функции, т.е. те наборы коэффициентов, у которых квадратичная составляющая равна 0 (первые 6 коэффициентов)

coef_1 = coef_1[np.all(coef_1[:,:6]==0, axis=1)]

#l_0 - кортеж линейных функций (каждая функция задаётся наборов коэффициентов), не зависящих от x, l_1 - от y, l_2 - от z.

l_0 = coef_1[coef_1[:,6]==0]
l_0 = tuple(map(tuple, l_0))
l_1 = coef_1[coef_1[:,7]==0]
l_1 = tuple(map(tuple, l_1))
l_2 = coef_1[coef_1[:,8]==0]
l_2 = tuple(map(tuple, l_2))

#В iterator_(1..6) содержатся семейства-кандидаты на правильность, состоящие из всевозможных комбинаций квадратичных и линейных функций

iterator_1 = it.product(f_0, f_1, l_2)
iterator_2 = it.product(f_0, l_1, f_2)
iterator_3 = it.product(l_0, f_1, f_2)
iterator_4 = it.product(f_0, l_1, l_2)
iterator_5 = it.product(l_0, f_1, l_2)
iterator_6 = it.product(l_0, l_1, f_2)

#Функция calculate с помощью параллельных вычислений считает количество правильных семейств (1 выходной аргумент) и сохраняет их в переменную lst (2 выходной аргумент). Для проверки правильности используем функцию check_3 (вспомогательные объекты для её реализации и описание находятся в файле my_functions.ipynb)

def calculate(pool, iterator, chunksize):
    manager = multiprocessing.Manager()
    lst = manager.list()
    res =  pool.imap(partial(check_3, lst=lst), iterator, chunksize=chunksize)
    return np.sum(np.array(tuple(res))), np.array(lst)

num_workers = multiprocessing.cpu_count()
pool = multiprocessing.Pool(num_workers)

chunksize = ceil(13305708 / (3 * num_workers))

s_1, lst_1 = calculate(pool, iterator_1, chunksize)
print(s_1)

print(lst_1)

s_2, lst_2 = calculate(pool, iterator_2, chunksize)
print(s_2)

print(lst_2)

s_3, lst_3 = calculate(pool, iterator_3, chunksize)
print(s_3)

print(lst_3)

chunksize = ceil(511758 / num_workers)

s_4, lst_4 = calculate(pool, iterator_4, chunksize)
print(s_4)

print(lst_4)

s_5, lst_5 = calculate(pool, iterator_5, chunksize)
print(s_5)

print(lst_5)

s_6, lst_6 = calculate(pool, iterator_6, chunksize)
print(s_6)

print(lst_6)

pool.close()
pool.join()

#Проверка семейства на треугольность: 1 функция - константа, 2 функция - зависит от x, 3 функция - зависит от x и y

def trg(fam):
    if np.all(fam[0][:9] == 0) and np.all(fam[1][[1,2,3,4,5,7,8]] == 0) and np.all(fam[2][[2,4,5,8]] == 0):
        return True
    else:
        return False

#Генерация семейства, полученного из входного семейства fam путём применения перестановки perm на функциях семейства и их аргументах. Перестановка на аргументах осуществляется перестановкой коэффициентов многочлена в нужном порядке. Коэффициенты при x^2, y^2 и z^2 и x,y,z переставляются так же, как и аргументы, а перестановка коэффициентов при смешанных квадратичных членах xy, xz, yz осуществляется согласно перестановке аргументов (не всегда с помощью той же перестановки)

def fam_perm(fam, perm):
    c = copy.deepcopy(fam)
    if np.array_equal(perm, np.array([0,2,1])):
        perm_1 = np.array([1,0,2])
    elif np.array_equal(perm, np.array([1,0,2])):
        perm_1 = np.array([0,2,1])
    elif np.array_equal(perm, np.array([1,2,0])):
        perm_1 = np.array([2,0,1])
    elif np.array_equal(perm, np.array([2,0,1])):
        perm_1 = np.array([1,2,0])
    else:
        perm_1 = perm.copy()
    for i in range(len(c)):
        c[i][:3] = c[i][:3][perm]
        c[i][6:9] = c[i][6:9][perm]
        c[i][3:6] = c[i][3:6][perm_1]
    return c[perm]

#Всевозможные перестановки из 3 элементов

perm = np.array(tuple(it.permutations(range(3))))
print(perm)

#Проверка семейства на треугольность посредством проверки на треугольность всевозможных семейств, полученных из входного fam c помощью всевозможных перестановок на функциях семейства и их аргументах

def check_trg(fam):
    flag = False
    for p in perm:
        if trg(fam_perm(fam, p)):
            flag = True
            break
    return flag

#Подсчёт количества треугольных семейств среди правильных

count_1 = 0
for fam in lst_1:
    if check_trg(fam):
        count_1 += 1
print(count_1, count_1 / len(lst_1))

count_2 = 0
for fam in lst_2:
    if check_trg(fam):
        count_2 += 1
print(count_2, count_2 / len(lst_2))

count_3 = 0
for fam in lst_3:
    if check_trg(fam):
        count_3 += 1
print(count_3, count_3 / len(lst_3))

count_4 = 0
for fam in lst_4:
    if check_trg(fam):
        count_4 += 1
print(count_4, count_4 / len(lst_4))

count_5 = 0
for fam in lst_5:
    if check_trg(fam):
        count_5 += 1
print(count_5, count_5 / len(lst_5))

count_6 = 0
for fam in lst_6:
    if check_trg(fam):
        count_6 += 1
print(count_6, count_6 / len(lst_6))
