#找最低點
import random

def hillClimbing(f, x, y,z, h=0.1):
    while (True):
        fxyz = f(x, y,z)
        print('x={0:.3f} y={1:.3f} z={2: .3f} f(x,y,z)={3:.3f}'.format(x, y,z,fxyz))
        if f(x+h, y,z) <= fxyz:
            x = x + h
        elif f(x-h, y,z) <= fxyz:
            x = x - h
        elif f(x, y+h,z) <= fxyz:
            y = y + h
        elif f(x, y-h,z) <= fxyz:
            y = y - h
        elif f(x, y,z+h) <= fxyz:
            z = z + h
        elif f(x, y,z-h) <= fxyz:
            z = z - h    
        else:
            break
    return (x,y,z,fxyz)

def f(x, y,z):
    return x**2 + y**2 + z**2 - 2*x - 4*y - 6*z + 8

hillClimbing(f, 0, 0,0)