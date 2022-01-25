import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from sympy.plotting import plot3d, plot
import cmath

if __name__=="__main__":

    x, y, z = symbols('x y z')

    equation = cos(2*pi*(x + y )) + I*sin(2*pi*(x+y)) 

    #plot3d(equation, (x,-1,1), (y, -1,1))
   

    x_ = np.linspace(0,1,100)
    y_ = np.linspace(0,1,100)

    xx,yy = np.meshgrid(x_,y_)

    z = cos(2*cmath.pi*(xx+yy)) + 1j*sin(2*cmath.pi*(xx+yy))

    plt.imshow(z)
    plt.show() 
