#Подсчёт количества правильных семейств из квадратичных функций от 3 переменных

import itertools as it
from math import ceil
import numpy as np
import multiprocessing
from ipynb.fs.full.my_functions import check_2

#Создаём набор из 10 коэффициентов для квадратичных функций(по порядку: x^2, y^2, z^2, xy, xz, yz, x, y, z, c)

coef = np.array(tuple(it.product((0,1,2), repeat = 10)))

#Отбираем наборы коэффициентов, в которых есть хотя бы один ненулевой при квадратичном члене

coef = coef[(coef[:, 0] != 0) | (coef[:, 1] != 0) | (coef[:, 2] != 0) | (coef[:, 3] != 0) | (coef[:, 4] != 0) | (coef[:, 5] != 0)]

#f_0 - кортеж функций (каждая функция задаётся наборов коэффициентов), не зависящих от x, f_1 - от y, f_2 - от z. В переменной iterator находятся семейства-кандидаты на правильность (элементы декартова произведения f_0 x f_1 x f_2)

f_0 = coef[(coef[:,0]==0) & (coef[:,3]==0) & (coef[:,4]==0) & (coef[:,6]==0)]
f_0 = tuple(map(tuple, f_0))
f_1 = coef[(coef[:,1]==0) & (coef[:,3]==0) & (coef[:,5]==0) & (coef[:,7]==0)]
f_1 = tuple(map(tuple, f_1))
f_2 = coef[(coef[:,2]==0) & (coef[:,4]==0) & (coef[:,5]==0) & (coef[:,8]==0)]
f_2 = tuple(map(tuple, f_2))
iterator = it.product(f_0, f_1, f_2)

#С помощью параллельных вычислений считаем количество правильных семейств из квадратичных функций. Для проверки правильности используем функцию check_2 (вспомогательные объекты для её реализации и описание находятся в файле my_functions.ipynb)

num_workers = multiprocessing.cpu_count()
pool = multiprocessing.Pool(num_workers)
chunksize = ceil(345948408 / (4 * num_workers))
result = pool.imap(check_2, iterator, chunksize=chunksize)
pool.close()
pool.join()
s = np.sum(np.array(tuple(result)))
print(s)

