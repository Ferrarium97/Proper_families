import numpy as np
import itertools as it

#Создаём массив наборов аргументов x,y,z

args = np.array(list(it.product(range(3), repeat=3)))

#Перевод набора аргументов, который можно представить в виде троичного числа, в его десятичную запись

def construct(arg):
    return int(''.join(map(str, arg)),3)

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
       np.all([fam[1][i:i+9] == fam[1,i] for i in range(0,27,9)]) and \
       np.all([fam[2][i:i+3] == fam[2,i] for i in range(0,27,3)]):
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

## Следующий блок кода относится к мультиаффинным семействам, которые находятся в стадии разработки, поэтому на данный момент этот блок не представляет интереса.

#Следующий блок закомментированных команд был направлен на получение всевозможных конъюнкций (минимума в троичной случае) линейных функций для проверки семейства на мультиаффинность. Эти конъюнкции представлены в укороченном виде: так как i-я функция не зависит от i-ой переменной, то для i-ой функции (если она мультиаффинная) конъюнкции должны состоять из линейных функций, которые не зависят от i-ой переменной. Поскольку 1 функцию (которая не зависит от x) достаточно задать на 0-8 наборе (нумерация от 0), 2 функцию (которая не зависит от y) достаточно задать на 0,1,2,9,10,11,18,19,20 наборах, а 3 функцию (которая не зависит от z) достаточно задать на 0,3,6,9,12,15,18,21,24 наборах, то и всевозможные конъюнкции линейных функций (не зависящих от x для 1 функции, не зависящих от y для 2 функции и не зависящих от z для 3 функции) достаточно задать на соответствующих 9 наборах. Поскольку список значений всевозможных линейных функций , не зависящих от x, на 0-8 наборе совпадает со списком значений для линейных функций, не зависящих от y, на 0,1,2,9,10,11,18,19,20 наборах, а также со списком значений для линейных функций, не зависящих от z, на 0,3,6,9,12,15,18,21,24 наборах, то достаточно рассмотреть один из них и из него получить всевозможные конъюнкции, представленные своими значениями на 9 наборах (для 1 функции это будет 0-8 наборы, для 2 функции это будет 0,1,2,9,10,11,18,19,20 наборы, для 3 функции это будет 0,3,6,9,12,15,18,21,24 наборы).

#Линейные функции будут представлены наборами коэффициентов (a_0, a_1, a_2, a_3) и задаваться формулой a_0 + a_1 * x + a_2 * y + a_3 * z

#Подсчёт значения линейной функции по набору коэффициентов и значению аргументов

#def lin_func(coef, arg):
#    return np.sum(coef*np.append(1,arg))%3

#Построение вектора значений на 0-8 наборах линейной функции по её набору коэффициентов

#def build_linfunc(coef):
#    return np.fromiter((lin_func(coef, arg) for arg in args[:9]), dtype=int)

#Генерация всевозможных наборов коэффициентов для линейных функций

#coef = np.array(list(it.product(range(3), repeat = 4)))

#Отбираем только функции, которые не зависят от x (см. замечание в блоке пояснений выше про равенство списков)

#coef_1 = coef[coef[:,1]==0]

#Строим список векторов значений на 0-8 наборах для всех линейных функций, не зависящих от x

#linfunc_1 = np.array(list(map(build_linfunc, coef_1)))

#Строим список всевозможных конъюнкций линейных функций, не зависящих от x, которые представляют собой векторы значений на 0-8 наборах (из списка линейных функций убираем 0 функцию для ускорения вычислений, потому что минимум с ней всегда даст 0, а конъюнкция по всем остальным линейным фунциям и так даст 0, так что мы его не потеряем)

#all_linf_conj = np.array(list(np.min(elem, axis=0) for i in range(1,linfunc_1.shape[0]) for elem in it.combinations(linfunc_1[1:],i)))

#Отбираем только уникальные из них

#all_linf_conj = np.unique(all_linf_conj, axis=0)

#Сохраняем полученные функции в сжатый файл

#np.savez_compressed('all_linf_conj', all_linf_conj)

#Выгружаем всевозможные конъюнкции из файла (без их предварительного пересчёта) для ускорения при повторных пересчётах

#all_linf_conj = np.load('all_linf_conj.npz')['arr_0']

#Проверка семейства на мультиаффинность. Семейство подаётся в укороченном виде (1 функция представлена вектором значений на 0-8 наборе, 2 функция - на 0,1,2,9,10,11,18,19,20 наборах, 3 функция - на 0,3,6,9,12,15,18,21,24 наборах). Проверяется мультиаффинность каждой из функций (то есть принадлежность к списку всевозможных конъюнкций из линейных функций)

#def check_mltaff(short_fam):
#    if any(np.array_equal(x, short_fam[0]) for x in all_linf_conj) and \
#       any(np.array_equal(x, short_fam[1]) for x in all_linf_conj) and \
#       any(np.array_equal(x, short_fam[2]) for x in all_linf_conj):
#        return True
#    else:
#        return False
