from owlready2 import *

onto = get_ontology("http://test.org/onto_pizza.owl")

with onto:
    # pizzas
    class Pizza(Thing): pass
    class Pizzananas(Pizza): pass

    # ingredients
    class Ingredient(Thing): pass

    class Meat(Ingredient): pass    
    class Ham(Meat): pass
    class Sausage(Meat): pass

    class Cheese(Ingredient): pass
    class Mozzarella(Cheese): pass
    
    class Vegetables(Ingredient): pass
    class Tomato(Vegetables): pass
    class Pepper(Vegetables): pass
    class Olive(Vegetables): pass

    class Fruits(Ingredient): pass
    class Pineapple(Fruits): pass
    class Mango(Fruits): pass

    # relations
    class has_ingredient(Pizza >> Ingredient): pass

    # infered subclasses
    class Margarita(Pizza): 
        equivalent_to = [ Pizza & ( has_ingredient.some(Tomato) ) & ( has_ingredient.some(Cheese) ) ]
        # equivalent_to = [ Pizza & ( ( has_ingredient.some(Tomato) & has_ingredient.some(Cheese) ) & has_ingredient.exactly(2, Ingredient)) ]
    class Napolitana(Pizza): 
        equivalent_to = [ Pizza & ( has_ingredient.some(Tomato) ) & ( has_ingredient.some(Cheese) ) & ( has_ingredient.some(Meat) ) ]
        # equivalent_to = [ Pizza & ( ( has_ingredient.some(Tomato) & has_ingredient.some(Cheese) & has_ingredient.some(Meat) ) & has_ingredient.exactly(3, Ingredient)) ]
    class Portlandia(Pizza): 
        equivalent_to = [ Pizza & ( has_ingredient.only(Tomato) ) ]
    class Indiana(Pizza): 
        equivalent_to = [ Pizza & ( has_ingredient.some(Mango) ) ]
    class Pizzananas(Pizza): 
        equivalent_to = [ Pizza & ( has_ingredient.some(Pineapple) & has_ingredient.some(Ham) & has_ingredient.some(Tomato) ) ]

    # suitable for claases
    class NonVeggyPizza(Pizza):
        equivalent_to = [ Pizza & ( has_ingredient.some(Meat) ) ]
    class VeggyPizza(Pizza):
        equivalent_to = [ Pizza & Not(NonVeggyPizza) ]
    class VeganPizza(Pizza):
        equivalent_to = [ Pizza & ( has_ingredient.only(Vegetables) | has_ingredient.only(Fruits) )]

    pizzas = []
    p = Pizza("a_Margarita")
    p.has_ingredient.append(Mozzarella())
    p.has_ingredient.append(Tomato())
    p.is_a.append(has_ingredient.only(Cheese | Tomato))
    pizzas.append({ "obj": p, "as known as": Margarita, "suitable for": VeggyPizza })

    p = Pizza("a_Pizzananas")
    p.has_ingredient.append(Pineapple())
    p.has_ingredient.append(Tomato())
    p.has_ingredient.append(Ham())
    p.is_a.append(has_ingredient.only(Pineapple | Tomato | Ham))
    pizzas.append({ "obj": p, "as known as": Pizzananas, "suitable for": NonVeggyPizza })

    p = Pizza("a_Portlandia")
    p.has_ingredient.append(Tomato())
    p.is_a.append(has_ingredient.only(Tomato))
    pizzas.append({ "obj": p, "as known as": Portlandia, "suitable for": VeganPizza })

    p = Pizza("a_Napolitana")
    p.has_ingredient.append(Tomato())
    p.has_ingredient.append(Ham())
    p.has_ingredient.append(Mozzarella())
    p.is_a.append(has_ingredient.only(Tomato | Ham | Mozzarella))
    pizzas.append({ "obj": p, "as known as": Napolitana, "suitable for": NonVeggyPizza })

    p = Pizza("a_Indiana")
    p.has_ingredient.append(Mango())
    p.is_a.append(has_ingredient.only(Mango))
    pizzas.append({ "obj": p, "as known as": Indiana, "suitable for": VeganPizza })

    # imp = Imp()
    # imp.set_as_rule("Pizza(?a), Pineapple(?o), has_ingredient(?a, ?o) -> Pizzananas(?a)")

    # close_world(Pizza)
 
sync_reasoner_pellet()
graph = default_world.as_rdflib_graph()

print("Inferred classes")
for pizza in pizzas:
    print("{} is infered as {} and that's {} and {}!".format(pizza['obj'], pizza['obj'].is_a, pizza['as known as'] in pizza['obj'].is_a, pizza['suitable for'] in pizza['obj'].is_a))


print("Pizzas:")
print(list(Pizza.instances()))

print("Pizzas (SPARQL):")
print(list(graph.query_owlready("""
SELECT ?b WHERE {
?b <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://test.org/onto_pizza.owl#Pizza> .
} """)))

print("Pizzananas:")
print(list(Pizzananas.instances()))

print("Pizzananas (SPARQL):")
print(list(graph.query_owlready("""
SELECT ?b WHERE {
?b <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://test.org/onto_pizza.owl#Pizzananas> .
} """)))

onto.save(file = "my_pizza.rdfxml", format = "rdfxml")
