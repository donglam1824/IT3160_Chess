from visualiser.visualiser import Visualiser

@Visualiser(node_properties_kwargs={"shape":"record", "color":"#f57542", "style":"filled", "fillcolor":"grey"})
def fibonacci(n):
  if n <= 2: 
    return 1
  return fibonacci(n = n-1) + fibonacci(n = n-2)

print(fibonacci(6))
Visualiser.make_animation("Fib.gif", 2)
