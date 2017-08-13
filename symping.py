import sympy
import pandas as pd
import numpy as np
import scipy.interpolate
from scipy.interpolate import interp1d
import math

# x = np.arange(0, 4, 1)


# y = np.arange(0, 4, 1)
# xx, yy = np.meshgrid(x, y)
# z = xx*2+yy




x = sympy.symbols('x')




value_list = list(zip([-40, -20, 0, 20, 40], [0.1, 0.2, 0.1, 1, 2.2]))
# print(sympy.interpolate(value_list, x))

print(list(zip([-40, -20, 0, 20, 40], [0.1, 0.2, 0.1, 1, 2.2])))
print(sympy.interpolate(value_list, -42))
ff = interp1d([-40, -20, 0, 20, 40], [0.1, 0.2, 0.1, 1, 2.2])
print(ff(-39))


value_list1 = list(zip([0.38, 0.85, 1.25, 3.16, 4.75, 9.18, 12.53, 19.20, 29.56], [0.01, 0.05, 0.1, 0.5, 1, 3, 5, 10, 20]))
value_list2 = list(zip([0.01, 0.05, 0.1, 0.5, 1.0, 3.0, 5.0, 10.0, 20.0], [0.38, 0.85, 1.25, 3.16, 4.75, 9.18, 12.53, 19.20, 29.56]))

print(value_list1)
print(sympy.interpolate(value_list1, x))
print(sympy.interpolate(value_list2, 7.0))


k4 = list(zip([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], [1, 1.33, 1.67, 2.0, 2.34, 2.67, 3.0, 3.34, 3.67, 4.0, 5.68]))

x = 12
int_k4 = sympy.interpolate(k4, x)

print('k4 %s' % int_k4)

k5 = list(zip([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], [0.38, 0.26, 0.22, 0.19, 0.17, 0.15, 0.14, 0.13, 0.12, 0.12, 0.11, 0.11, 0.10, 0.10, 0.10]))
print(sympy.interpolate(k5, 3.5))



print(sympy.interpolate(k4, 2))


def equivalent_amount_1():
    pass


