import owlready2
from owlready2 import *

# load a local ontology :
pizza_onto = owlready2.get_ontology("ontologies/pizza_onto.owl").load()

with pizza_onto:
    class NonVegetarianPizza(pizza_onto.Pizza):
        equivalent_to = [ pizza_onto.Pizza & ( pizza_onto.has_topping.some(pizza_onto.MeatTopping) | pizza_onto.has_topping.some(pizza_onto.FishTopping) ) ]

    class VegetarianPizza(pizza_onto.Pizza):
        equivalent_to = [ pizza_onto.Pizza & Not(pizza_onto.NonVegetarianPizza) ]

    class VeganPizza(pizza_onto.Pizza):
        equivalent_to = [ pizza_onto.Pizza & pizza_onto.has_topping.only(pizza_onto.TomatoTopping) ]

# create instances
margarita = pizza_onto.Pizza("margarita")
margarita.has_topping = [ pizza_onto.CheeseTopping(), pizza_onto.TomatoTopping() ]
margarita.is_a.append(pizza_onto.has_topping.only(pizza_onto.CheeseTopping | pizza_onto.TomatoTopping))

napolitana = pizza_onto.Pizza("napolitana")
napolitana.has_topping = [ pizza_onto.CheeseTopping(), pizza_onto.TomatoTopping(), pizza_onto.MeatTopping() ]
napolitana.is_a.append(pizza_onto.has_topping.only(pizza_onto.CheeseTopping | pizza_onto.TomatoTopping | pizza_onto.MeatTopping))

portlandia = pizza_onto.Pizza("portlandia")
portlandia.has_topping = [ pizza_onto.TomatoTopping() ]
portlandia.is_a.append(pizza_onto.has_topping.only(pizza_onto.TomatoTopping))

# close_world(pizza_onto.Pizza)

print("---- List Individuals -----")
for instance in pizza_onto.Pizza.instances(): 
    print(instance)

# try reasoning
with pizza_onto:
    owlready2.sync_reasoner(infer_property_values = True)

print("---- What about -----")
print("What about a margarita ? {}".format(margarita.is_a))
print("What about a napolitana ? {}".format(napolitana.is_a))
print("What about a portlandia ? {}".format(portlandia.is_a))

print("---- Individual Search -----")
print("Individuals of NonVegetarianPizza are {}".format(pizza_onto.search(type = pizza_onto.NonVegetarianPizza)))
print("Individuals of VegetarianPizza are {}".format(pizza_onto.search(type = pizza_onto.VegetarianPizza)))
print("Individuals of VeganPizza are {}".format(pizza_onto.search(type = pizza_onto.VeganPizza)))

print("---- What is it -----")
print("Is margarita a Pizza ?", pizza_onto.Pizza in margarita.is_a, "And a Veggy Pizza ?", pizza_onto.VegetarianPizza in margarita.is_a)
print("Is napolitana a Non Veggy Pizza ?", pizza_onto.NonVegetarianPizza in napolitana.is_a)
print("Is portlandia a Vegan Pizza ?", pizza_onto.VeganPizza in portlandia.is_a)

print("---- Find pizzas -----")
print("Pizza with Tomato", pizza_onto.search(is_a = pizza_onto.Pizza, has_topping = pizza_onto.search(is_a = pizza_onto.TomatoTopping)))
print("Pizza non veggy with Tomato", pizza_onto.search(is_a = pizza_onto.NonVegetarianPizza, has_topping = pizza_onto.search(is_a = pizza_onto.TomatoTopping)))
print("Pizza veggy", pizza_onto.search(is_a = pizza_onto.VegetarianPizza ))
print("Pizza veggy with Cheese", pizza_onto.search(is_a = pizza_onto.VegetarianPizza, has_topping = pizza_onto.search(is_a = pizza_onto.CheeseTopping)))
print("Pizza vegan", pizza_onto.search(is_a = pizza_onto.VeganPizza ))

pizza_onto.save(file = "my_pizza.rdfxml", format = "rdfxml")

graph = default_world.as_rdflib_graph()
r = list(graph.query("""SELECT ?pizza WHERE { ?pizza  <pizza_onto#Pizza>  "napolitana" }"""))
print(r)
