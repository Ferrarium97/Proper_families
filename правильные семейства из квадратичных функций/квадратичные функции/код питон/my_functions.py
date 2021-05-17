import itertools as it

#Генерация наборов аргументов x,y,z

args = tuple(it.product((0,1,2), repeat = 3))

#Генерация наборов аргументов x,y,z вместе с порядковым номером набора

num_args = tuple(enumerate(it.product((0,1,2), repeat = 3)))

#Пары различных нумерованных наборов аргументов

pairs = tuple(it.combinations(num_args, 2))

#Функция возвращает набор позиций, в которых отличаются два вектора x и y

def diff_idx(x,y):
    return (i for (i,(a,b)) in enumerate(zip(x,y)) if a!=b)

#Вовзращает значение функции, задаемой набором коэффиентов coef в точке arg (arg - набор (x, y, z))

def quad_func(coef, arg):
    return (coef[0] * arg[0] * arg[0] + coef[1] * arg[1] * arg[1] + coef[2] * arg[2] * arg[2] + \
            coef[3] * arg[0] * arg[1] + coef[4] * arg[0] * arg[2] + coef[5] * arg[1] * arg[2] + \
            coef[6] * arg[0] + coef[7] * arg[1] + coef[8] * arg[2] + coef[9])%3

#Функция возвращает кортеж из значений функции, задаваемой коэффициентами coef, для всех аргументов

def quad_func_values(coef):
    return tuple(quad_func(coef, arg) for arg in args)

#Проверка семейства на правильность по определению. На вход подаётся семейство fam в виже кортежа, состоящего из наборов коэффициентов, задающих функции семейства. Далее каждый набор коэффициентов заменяется на значения функции для всех аргументов с помощью функции quad_func_values

def check_2(fam):
    fam = tuple(map(quad_func_values,fam))
    for p in pairs:
        flag = False
        for idx in diff_idx(p[0][1],p[1][1]):
            if fam[idx][p[0][0]] == fam[idx][p[1][0]]:
                flag = True
                break
        if not flag:
            break
    return flag

#Функция делает то же самое, что и check_2 + сохраняет правильное семейство в общий список lst

def check_3(fam, lst):
    fam_1 = tuple(map(quad_func_values,fam))
    for p in pairs:
        flag = False
        for idx in diff_idx(p[0][1],p[1][1]):
            if fam_1[idx][p[0][0]] == fam_1[idx][p[1][0]]:
                flag = True
                break
        if not flag:
            break
    if flag:
        lst.append(fam)
    return flag
