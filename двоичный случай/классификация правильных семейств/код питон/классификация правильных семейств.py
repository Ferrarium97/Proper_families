#Среди полученных правильных семейств порядка 3 осуществляется поиск треугольных и ортогональных семейств и семейств, которые не вошли ни в один из этих 2 классов. Также ищутся пересечения этих классов.

import numpy as np
import itertools as it
from ipynb.fs.full.functions_for_clf import check_ort, check_trg_aft_perm, check_const
import multiprocessing
from math import ceil

#Выгружаем numpy-массив, состоящий из всех правильных семейств порядка 3

data = np.load('all_fams_2.npz')['arr_0']

print(data.shape)

#Количество семейств, содержащих хотя бы одну константу

check_const_res = np.fromiter(map(check_const, data), dtype=bool)
const_fams_2 = data[check_const_res]
print(const_fams_2.shape)

for fam in const_fams_2:
    print(fam)

ort_res = np.fromiter(map(check_ort, data), dtype=bool)
trg_res = np.fromiter(map(check_trg_aft_perm, data), dtype=bool)
ort_trg_res = ort_res & trg_res
other_res = ~(ort_res | trg_res)
ort_fams_2 = data[ort_res]
trg_fams_2 = data[trg_res]
ort_trg_fams_2 = data[ort_trg_res]
other_fams_2 = data[other_res]
np.savez_compressed('ort_fams_2', ort_fams_2)
np.savez_compressed('trg_fams_2', trg_fams_2)
np.savez_compressed('ort_trg_fams_2', ort_trg_fams_2)
np.savez_compressed('other_fams_2', other_fams_2)

print(ort_fams_2.shape[0], ort_fams_2.shape[0]/data.shape[0])

print(trg_fams_2.shape[0], trg_fams_2.shape[0]/data.shape[0])

print(ort_trg_fams_2.shape[0], ort_trg_fams_2.shape[0]/data.shape[0])

print(other_fams_2.shape[0], other_fams_2.shape[0]/data.shape[0])
