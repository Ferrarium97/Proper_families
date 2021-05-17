import itertools as it
from tqdm import tqdm

#Генерация наборов аргументов x,y,z вместе с порядковым номером набора

num_args = tuple(enumerate(it.product((0,1,2), repeat = 3)))

#Пары различных нумерованных наборов аргументов

pairs = tuple(it.combinations(num_args, 2))

#Функция возвращает набор позиций, в которых отличаются два вектора x и y

def diff_idx(x,y):
    return (i for (i,(a,b)) in enumerate(zip(x,y)) if a!=b)

#Проверка на правильность по определению (на вход подаётся набор из трёх функций, каждая из которых представлена вектором значений на каждом из наборов переменных)

def func(f):
    for p in pairs:
        flag = False
        for idx in diff_idx(p[0][1],p[1][1]):
            if f[idx][p[0][0]] == f[idx][p[1][0]]:
                flag = True
                break
        if not flag:
            break
    return flag
