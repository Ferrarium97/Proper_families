import numpy as np
import itertools as it

#Создаём массив наборов аргументов x,y,z

args = np.array(list(it.product(range(2), repeat=3)))

#Перевод набора аргументов, который можно представить в виде двоичного числа, в его десятичную запись

def construct(arg):
    return int(''.join(map(str, arg)),2)

#Создание перестановки на значениях функции по перестановке на аргументах

def perm_on_val(perm):
    args_perm = args[:, perm].tolist()
    return list(map(construct, args_perm))

#Создание всех перестановок на аргументах

perm = list(map(list, it.permutations(range(3))))

#Список пар, состоящих из перестановки на аргументах и перестановки на значениях функции

perm_couple = [(p, perm_on_val(p)) for p in perm]

#Построение семейства, полученного из исходного fam путём перестановки p[0] на аргументах функций и самих функций в семействе

def fam_aft_perm(fam, p):
    return fam[:, p[1]][p[0]]

#Проверка семейства на свойство треугольности: первая функция - константа, вторая функция не зависит от y и z, а третья функция не зависит от z.

def check_trg(fam):
    if np.all(fam[0] == fam[0,0]) and \
       np.all([fam[1][i:i+4] == fam[1,i] for i in range(0,8,4)]) and \
       np.all([fam[2][i:i+2] == fam[2,i] for i in range(0,8,2)]):
        return True
    else:
        return False

#Проверка семейства на треугольность: если существует перестановка на аргументах и функциях семейства, которая делает из исходного семейство, обладающее свойством треугольности, то семейство треугольное.

def check_trg_aft_perm(fam):
    for pc in perm_couple:
        if check_trg(fam_aft_perm(fam, pc)):
            return True
    return False

#Проверка семейства на ортогональность: все функции в семействе должны быть попарно ортогональны.

def check_ort(fam):
    return np.all(np.count_nonzero(fam == 0, axis=0)>1)

#Проверка семейства на содержание хотя бы одной константы

def check_const(fam):
    return np.all(fam[0] == fam[0,0]) or np.all(fam[1] == fam[1,0]) or np.all(fam[2] == fam[2,0])
