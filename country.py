from owlready2 import *

onto = get_ontology("http://test.org/onto_country.owl")

with onto:
    class abbrev(Thing >> str): pass
    class part_of(Thing >> Thing, TransitiveProperty): pass

    # Country
    class Country(Thing): pass

    # State
    class State(Thing): pass
    class in_country(part_of): pass
   
    # City
    class City(Thing): pass
    class in_state(part_of): pass
    class zip_code(City >> str): pass
    class population(City >> int): pass

    AllDisjoint([Country, State, City])

    # infered Classes
    class BigCity(City): pass 
    class SmallCity(City): pass
    # AllDisjoint([BigCity, SmallCity])

    class BigCityinUSA(BigCity): pass
    class SmallCityinUSA(BigCity): pass
    # AllDisjoint([BigCityinUSA, SmallCityinUSA])

    usa = Country("UnitedStatesofAmerica")
    usa.abbrev.append("USA")

    mass = State("Massachusetts", in_country = [usa])
    vermont = State("Vermont", in_country = [usa])

    boston = City("Boston", in_state = [mass])
    boston.zip_code.append("02108")
    boston.population.append(617594)

    andover = City("Andover", in_state = [mass])
    andover.zip_code.append("01810")
    andover.population.append(33201)
    
    montpelier = City("Montpelier", in_state = [vermont])
    montpelier.zip_code.append("05601")
    montpelier.population.append(7855)    

    burlington = City("Burlington", in_state = [vermont])
    burlington.zip_code.append("05401")
    burlington.population.append(42211)

    AllDifferent([boston, andover, montpelier, burlington])

    canada = Country("Canada")
    canada.abbrev.append("CA")

    quebec = State("Quebec", in_country = [canada])

    montreal = City("Montreal", in_state = [quebec])
    montreal.zip_code.append("66023")
    montreal.population.append(1704694)      

    Imp().set_as_rule("City(?c), population(?c, ?pop), greaterThan(?pop, 200000) -> BigCity(?c)")
    Imp().set_as_rule("City(?c), population(?c, ?pop), lessThan(?pop, 30000) -> SmallCity(?c)")
    # Imp().set_as_rule("BigCity(?c), part_of(?c, ?country), abbrev(?country, ?ab), stringEqualIgnoreCase(?ab, 'USA') -> BigCityinUSA(?c)")   
    # Imp().set_as_rule("SmallCity(?c), part_of(?c, ?country), abbrev(?country, ?ab), stringEqualIgnoreCase(?ab, 'USA') -> SmallCityinUSA(?c)")    
    # close_world(Country)
 
# sync_reasoner_pellet()
sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
graph = default_world.as_rdflib_graph()

print(usa.is_a, usa.abbrev)
print(canada.is_a, canada.abbrev)

print("disjoint classes")
for d in City.disjoints():
    print(d.entities)

print("Inferred classes")
print(BigCity, list(BigCity.instances()))
print(SmallCity, list(SmallCity.instances()))
print(BigCityinUSA, list(BigCityinUSA.instances()))
print(SmallCityinUSA, list(SmallCityinUSA.instances()))

print(boston, boston.is_a)
print(andover, andover.is_a)
print(montpelier, montpelier.is_a)
print(burlington, burlington.is_a)
print(montreal, montreal.is_a)

print("Infered relations")
print(vermont, vermont.INDIRECT_part_of)
print(montpelier, montpelier.INDIRECT_part_of)
print(burlington, burlington.INDIRECT_part_of)

print(mass, mass.INDIRECT_part_of)
print(andover, andover.INDIRECT_part_of)
print(boston, boston.INDIRECT_part_of)

print("Countries:")
print(list(Country.instances()))

print("Countries (SPARQL):")
print(list(graph.query_owlready("""
SELECT ?b WHERE {
?b <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://test.org/onto_country.owl#Country> .
} """)))
