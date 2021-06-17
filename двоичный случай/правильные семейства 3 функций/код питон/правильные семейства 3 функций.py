#Подсчёт количества правильных семейств из 3 функций с помощью алгоритма построения правильного семейства N+1 функций из правильных семейств N функций

import itertools as it
from tqdm import tqdm
import numpy as np
import multiprocessing
from ipynb.fs.full.functions import func
from math import ceil

#Генерация наборов значений переменных x и y вместе с порядковым номером набора

num_args_2 = tuple(enumerate(it.product((0,1), repeat = 2)))
print(num_args_2)

#Генерация различных пар наборов

pairs_2 = tuple(it.combinations(num_args_2, 2))
print(pairs_2)

#Выводит индексы позиций, в которых отличаются 2 вектора

def diff_idx(x,y):
    return (i for (i,(a,b)) in enumerate(zip(x,y)) if a!=b)

#Проверка на правильность по определению (на вход подаётся набор из двух функций, каждая из которых представлена вектором значений на каждом из наборов переменных)

def func_2(f):
    for p in pairs_2:
        flag = False
        for idx in diff_idx(p[0][1],p[1][1]):
            if f[idx][p[0][0]] == f[idx][p[1][0]]:
                flag = True
                break
        if not flag:
            break
    return flag

#Так как i-я функция не зависит от i-ой переменной, то нам достаточно знать значения функции на 2/4 наборах, остальные значения определяются по этим 2 наборам.

def f_2(elem, idx):
    l = [0] * 4
    if idx == 0:
        l[0] = l[2] = elem[0]
        l[1] = l[3] = elem[1]
    else:
        l[0] = l[1] = elem[0]
        l[2] = l[3] = elem[1]
    return tuple(l)

#f_0 - итератор, состоящий из функций, не зависящие от x, а f_1 - итератор, состоящий из функций, не зависящие от y. iterator_2 - итератор, состоящий из элементов декартового произведения f_0 и f_1, то есть семейства-кандидаты на правильность. Итератор существует до тех пор, пока не будут перечислены все его элементы, вызываемые методом next. Если элементы в итераторе закончились, то он бросает исключение. Использовал итераторы для экономии памяти.

iter_2 = it.product((0,1), repeat = 2)
f_0 = map(lambda p: f_2(p, 0), iter_2)
iter_2 = it.product((0,1), repeat = 2)
f_1 = map(lambda p: f_2(p, 1), iter_2)
iterator_2 = it.product(f_0, f_1)

#Проходим в цикле по всем семействам и подсчитываем правильные (переменная s) и сохраняем правильные семейства в переменную collect.

s=0
collect = []
for _ in tqdm(range(16)):
    el = next(iterator_2)
    if func_2(el):
        s+=1
        collect.append(el)
print(s)

print(collect)

#Конвертируем collect в numpy-массив для удобства.

collect = np.array(collect)

print(collect)

#Перевод числа от 0 до 4 в двоичную систему счисления (выходные числа длины 2 для удобного представления в виде наборов переменных)

def convert_to_base_2(x):
    if x == 0:
        return np.base_repr(x, base=2, padding=2)
    elif x == 1:
        return np.base_repr(x, base=2, padding=1)
    else:
        return np.base_repr(x, base=2)

#Перевод строкового представления числа в двоичной системе счисления в набор значений переменных на примере числа 3

np.array(list(convert_to_base_2(3)), dtype=int)

#Набор, каждый элемент которого состоит из 2 правильных семейств порядка 2

set_of_fam = np.array(list(it.product(collect, repeat=2)))

#Проверка условия из леммы 3 (возвращает True/False в зависимости от того, нужно ли соединять вершины графа(наборы переменных) ребром).

def check_edge(s, k, g):
    flag = False
    for (i, j) in it.permutations(range(2), 2):
        if set(diff_idx(np.array(list(convert_to_base_2(s)), dtype=int),\
                        np.array(list(convert_to_base_2(k)), dtype=int))).\
           issubset(set(diff_idx(g[i][:, s],g[j][:, k]))):
            flag = True
            break
    return flag

#Поиск всех вершин, находящихся в одной компоненте связности с i-ой вершиной

def find_comp(i, comp, use_vert, graph):
    for j in range(4):
        if graph[i, j] == 1 or graph[j, i] == 1:
            if j not in use_vert:
                use_vert.append(j)
                comp.append(j)
                find_comp(j, comp, use_vert ,graph)

#Поиск всех компонент связности в графе. Выдает количество компонент связности и сами компоненты

def find_components(graph):
    use_vert = []
    components = []
    for i in range(4):
        if i not in use_vert:
            use_vert.append(i)
            comp = [i]
            find_comp(i, comp, use_vert ,graph)
            components.append(comp)
    return len(components), components

#Построение графа (заполняется только верхняя диагональ)

def build_graph(fam):
    graph = np.zeros((4,4), dtype=int)
    for (i, j) in it.combinations(range(4), 2):
        if check_edge(i, j, fam):
            graph[i][j] = 1
    return graph

#Подсчет количества всевозможных правильных семейств порядка 3, построенных по набору из 2 правильных семейств порядка 2. Для каждого такого набора считаем количество всевозможных доопределений третьей функции на каждой компоненте связности графа.

count = 0
for fam in tqdm(set_of_fam):
    graph = build_graph(fam)
    count += 2 ** find_components(graph)[0]
print(count)

#Реализация унарных функций 2-значной логики I_0,...,I_{k-1}

def I_func(x, j):
    return 1 if x==j else 0

#Основный алгоритм построения различных семейств порядка 3, который получает на вход 2 правильных семейства порядка 2 и в результате выполнения функции наполняет список lst правильными семействами порядка 3, полученными путём всевозможных доопределений функции g на всех компонентах связности графа

print(set_of_fam[0].shape)

def build_all_fam(fam, comp_num, components, lst):
    short_fam = tuple(tuple(max(min(I_func(x,0), fam[0,j,y]),\
                                min(I_func(x,1), fam[1,j,y])) for y in range(4) for x in range(2)) for j in range(2))
    var_of_redef = it.product((0,1), repeat=comp_num)
    for var in var_of_redef:
        g = [0] * 8
        for (i,comp) in enumerate(components):
            for arg in comp:
                g[2*arg:2*arg+2] = [var[i]]*2
        new_fam = short_fam + (tuple(g),)
        lst.append(new_fam)

#Строим правильные семейства с помощью алгоритма, использующего граф (реализован в функции build_all_fam), который получает на вход 2 правильных семейства порядка 2 и выдает все построенные семейства порядка 3, полученные с помощью различного доопределения функции на компонентах связности графа

lst = []
for fam in tqdm(set_of_fam):
    graph = build_graph(fam)
    comp_num, components = find_components(graph)
    build_all_fam(fam, comp_num, components, lst)

lst = tuple(lst)

print(len(lst))

#С помощью параллельных вычислений проверяем, что все полученные семейства являются правильными по определению

s = 0
for fam in tqdm(lst):
    if func(fam):
        s+=1
print(s)

#Конвертируем кортеж с правильными семействами в numpy-массив

lst = np.array(lst)

#Записываем результат в файл result.npz с применением сжатия

np.savez_compressed('all_fams_2', lst)
