from micrograd.engine import Value

x = Value(0.0)
y = Value(0.0)
z = Value(0.0)

step = 0.01
for i in range(1000):
    f = x**2 + y**2 + z**2 - 2*x - 4*y - 6*z + 8
    x.grad=0
    y.grad=0
    z.grad=0
    f.backward()
    x.data-=step*x.grad
    y.data-=step*y.grad
    z.data-=step*z.grad
print(f"x={x} y={y} z={z} f(x,y,z)={f}")