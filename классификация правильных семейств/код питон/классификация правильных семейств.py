#Среди полученных правильных семейств порядка 3 осуществляется поиск треугольных и ортогональных семейств и семейств, которые не вошли ни в один из этих 2 классов. Также ищутся пересечения этих классов.

import numpy as np
import itertools as it
from ipynb.fs.full.functions_for_clf import check_ort, check_trg_aft_perm
import multiprocessing
from math import ceil

#Выгружаем numpy-массив, состоящий из всех правильных семейств порядка 3

data = np.load('all_fams.npz')['arr_0']

print(data.shape)

#С помощью параллельных вычислений ищем треугольные и ортогональные правильные семейства порядка 3, используя функции проверки из файла functions_for_clf. Результат храним в виде булевой маски ort_res для ортогональных семейств и trg_res для треугольных.

num_workers = multiprocessing.cpu_count()
pool = multiprocessing.Pool(num_workers)
chunksize = ceil(35481915 / (4 * num_workers))

ort_res = np.fromiter(pool.imap(check_ort, data, chunksize=chunksize), dtype=bool)

trg_res = np.fromiter(pool.imap(check_trg_aft_perm, data, chunksize=chunksize), dtype=bool)

pool.close()
pool.join()

#Применяем булеву маску ort_res к массиву всех правильных семейств. Получаем все правильные ортогональные семейства и сохраняем их в сжатый файл

ort_fams = data[ort_res]

print(ort_fams.shape)

np.savez_compressed('ort_fams', ort_fams)

#Применяем булеву маску trg_res к массиву всех правильных семейств. Получаем все правильные треугольные семейства и сохраняем их в сжатый файл

trg_fams = data[trg_res]

print(trg_fams.shape)

np.savez_compressed('trg_fams', trg_fams)

#Ищем пересечение классов ортогональных и треугольных правильных семейств и сохраняем их в файл

ort_trg_fams = data[ort_res & trg_res]

print(ort_trg_fams.shape)

np.savez_compressed('ort_trg_fams', ort_trg_fams)

#Сохраняем булевы маски ort_res и trg_res для дальнейшего переиспользования

np.savez_compressed('ort_res', ort_res)
np.savez_compressed('trg_res', trg_res)

#Так как в правильном семействе i-ая функция не зависит существенно от i-ой переменной, то укоротим массив данных в 3 раза, задав 1 функцию на 0-8 наборах, 2 функцию на 0,1,2,9,10,11,18,19,20 наборах, а 3 функцию на 0,3,6,9,12,15,18,21,24 наборах. Полученный компактный массив правильных семейств порядка 3 сохраним в all_fams_short.

data_1, data_2, data_3 = data[:,0,:9], data[:,1,[0,1,2,9,10,11,18,19,20]], data[:,2,[0,3,6,9,12,15,18,21,24]]

all_fams_short = np.stack((data_1,data_2,data_3), axis=1)

np.savez_compressed('all_fams_short', all_fams_short)

#Так как полная версия массива всех правильных семейств порядка 3 (где каждая функция представлена 27 значениями) занимает много оперативной памяти, то все остальные семейства, не вошедшие в 2 рассмотренных класса, будем искать в укороченном виде путём применения соответствующей булевой маски к сжатой версии массива правильных семейств all_fams_short

other_fams_short = all_fams_short[~(ort_res | trg_res)]

print(other_fams_short.shape)

np.savez_compressed('other_fams_short', other_fams_short)

#Cохраним все ранее полученные результаты в укороченном виде (где каждая функция в семействе будет представлена 9 значениями)

ort_fams_short = all_fams_short[ort_res]
trg_fams_short = all_fams_short[trg_res]
ort_trg_fams_short = all_fams_short[ort_res & trg_res]

np.savez_compressed('ort_fams_short', ort_fams_short)
np.savez_compressed('trg_fams_short', trg_fams_short)
np.savez_compressed('ort_trg_fams_short', ort_trg_fams_short)

## Следующий блок кода относится к мультиаффинным семействам, которые находятся в стадии разработки, поэтому на данный момент этот блок не представляет интереса.

#Загрузим укороченную версию массива всех правильных семейств порядка 3 для поиска мультиаффинных правильных семейств. С помощью параллельных вычислений получим булеву маску mltaff_res в точности как и для предыдущих двух классов.

#all_fams_short = np.load('all_fams_short.npz')['arr_0']

#num_workers = multiprocessing.cpu_count()
#pool = multiprocessing.Pool(num_workers)
#chunksize = ceil(35481915 / (12 * num_workers))

#mltaff_res = np.fromiter(pool.imap(check_mltaff, all_fams_short, chunksize=chunksize), dtype=bool)

#pool.close()
#pool.join()

#np.savez_compressed('mltaff_res', mltaff_res)

#Загрузим все полученные ранее булевы маски для поиска пересечений 3 классов правильных семейств и семейств, не вошедших в эти 3 класса.

#ort_res = np.load('ort_res.npz')['arr_0']
#trg_res = np.load('trg_res.npz')['arr_0']
#mltaff_res = np.load('mltaff_res.npz')['arr_0']

#Применяем булеву маску mltaff_res к исходному массиву всех правильных семейств порядка 3 и получаем все правильные мультиаффинные семейства порядка 3 в переменной mltaff_fams

#mltaff_fams = data[mltaff_res]

#np.savez_compressed('mltaff_fams', mltaff_fams)

#Ищем пересечение классов ортогональных и мультиаффиных правильных семейств порядка 3

#ort_mltaff_fams = data[ort_res & mltaff_res]

#np.savez_compressed('ort_mltaff_fams', ort_mltaff_fams)

#Ищем пересечение треугольных и мультиаффинных правильных семейств порядка 3

#trg_mltaff_fams = data[trg_res & mltaff_res]

#np.savez_compressed('trg_mltaff_fams', trg_mltaff_fams)

#Ищем пересечение всех 3 классов

#ort_trg_mltaff_fams = data[ort_res & trg_res & mltaff_res]

#ort_trg_mltaff_fams.shape

#np.savez_compressed('ort_trg_mltaff_fams', ort_trg_mltaff_fams)

#other_fams_short = all_fams_short[~(ort_res | trg_res | mltaff_res)]

#other_fams_short.shape

#np.savez_compressed('other_fams_short', other_fams_short)
