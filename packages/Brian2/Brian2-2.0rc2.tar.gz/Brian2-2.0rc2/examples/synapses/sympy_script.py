from sympy import simplify, cos, sin
from sympy.abc import x, y
a = (x + x**2)/(x*sin(y)**2 + x*cos(y)**2)
print(a)
(x**2 + x)/(x*sin(y)**2 + x*cos(y)**2)
print(simplify(a))
