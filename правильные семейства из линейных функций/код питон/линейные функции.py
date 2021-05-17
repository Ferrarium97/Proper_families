#Проверка факта, что все правильные семейства из линейных функции - треугольные с точностью до перестановки

import itertools as it
import numpy as np
import copy
from tqdm import tqdm

#Генерируем наборы значений переменных x,y,z

args = np.array(tuple(it.product((0,1,2), repeat = 3)))
print(args)

#Делаем то же самое, но вместе с номером набора

num_args = tuple(enumerate(it.product((0,1,2), repeat = 3)))
print(num_args)

#Генерируем всевозможные пары различных нумерованных наборов значений трёх переменных

pairs = tuple(it.combinations(num_args, 2))
print(pairs)

#Функция, возвращающая индексы позиций, в которых отличаются два вектора

def diff_idx(x,y):
    return (i for (i,(a,b)) in enumerate(zip(x,y)) if a!=b)

#Функция выдаёт список значений линейной функции на всевозможных наборах аргументов

def func_values(coef):
    return np.fromiter((lin_func(coef, arg) for arg in args), dtype=int)

#Функция вычисляет значение линейной функции в точке arg c коэффициентами coef

def lin_func(coef, arg):
    return np.sum(coef*np.append(1,arg))%3

#Проверка семейства на правильность по определению

def check(fam):
    fam = np.array(list(map(func_values,fam)))
    for p in pairs:
        flag = False
        for idx in diff_idx(p[0][1],p[1][1]):
            if fam[idx][p[0][0]] == fam[idx][p[1][0]]:
                flag = True
                break
        if not flag:
            break
    return flag

#Генерация всевозможных линейных функций с помощью коэффициентов (по порядку: 1, x, y, z)

coef = np.array(tuple(it.product((0,1,2), repeat = 4)))

#f_0 - итератор, содержащий все линейные функции не зависящие от x, f_1 - от y, f_2 - от z. В переменной iterator содержится декартово произведение f_0 x f_1 x f_2, то есть семейства-кандидаты на правильность

f_0 = coef[coef[:,1]==0]
f_1 = coef[coef[:,2]==0]
f_2 = coef[coef[:,3]==0]
iterator = it.product(f_0, f_1, f_2)

#Подсчёт правильных семейств линейных функций (переменная s). Правильные семейства хранятся в переменной lst

s = 0
lst = []
for _ in tqdm(range(19683)):
    elem = np.array(next(iterator))
    if check(elem):
        s += 1
        lst.append(elem)
print(s, s/19683)

#Конвератция в numpy-массив для удобной работы в дальнейшем

lst = np.array(lst)
print(lst)

#Проверка семейства на треугольность

def trg(fam):
    if np.all(fam[0][1:] == 0) and np.all(fam[1][2:] == 0) and np.all(fam[2][3:] == 0):
        return True
    else:
        return False

#Генерация семейства, полученного из входного семейства fam путём применения перестановки perm на функциях семейства и их аргументах. Перестановка на аргументах осуществляется перестановкой коэффициентов многочлена в нужном порядке

def fam_perm(fam, perm):
    c = copy.deepcopy(fam)
    for i in range(len(c)):
        c[i][1:] = c[i][1:][perm]
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

#Проверка того, что все правильные семейства (переменная lst) являются треугольными

count = 0
for fam in lst:
    if check_trg(fam):
        count += 1
    else:
        print(fam)
print(count)

