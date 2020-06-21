'''
Created on May 17, 2020

@author: nandroid
'''
from sympy import solve, Symbol, exp

def main():
    
#    x = 14.7296138519
    x = Symbol('x')
    alpha = Symbol('alpha', real=True)
    sol = solve([-alpha * x**2 - 0.01, x - 8 ], alpha, x)
    print(sol)
    
if __name__ == '__main__':
    main()