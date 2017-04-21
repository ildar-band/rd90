import sympy
x = sympy.symbols('x')


value_list = list(zip([-40, -20, 0, 20, 40], [0.1, 0.2, 0.1, 1, 2.2]))
print(sympy.interpolate(value_list, 40))

print(list(zip([-40, -20, 0, 20, 40], [0.1, 0.2, 0.1, 1, 2.2])))