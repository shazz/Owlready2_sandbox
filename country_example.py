from owlready2 import *
from rdflib import URIRef
import sys

ontology = 'http://example.org/onto_country#'
onto = get_ontology(ontology)

with onto:

    # Defining the ontology
    class abbrev(Thing >> str): pass
    class part_of(Thing >> Thing, TransitiveProperty): pass

    # Country
    class Country(Thing): pass

    # State (US concept)
    class State(Thing): pass
    class in_country(part_of): pass

    # Province (Canadian concept)
    class Province(Thing): pass
    class in_province(part_of): pass

    # County (US Concept)
    class County(Thing): pass
    class in_state(part_of): pass    
    
    # City
    class City(Thing): pass
    class in_county(part_of): pass
    class zip_code(City >> str): pass
    class population(City >> int): pass

    # A instance cannot be at the same time more than one of
    AllDisjoint([State, Province])
    AllDisjoint([Country, State, County, City])

    # inferred classes
    class CanadianCity(City):
        equivalent_to = [ City & ( in_province.some(Province) ) ]
    class USCity(City):
        equivalent_to = [ City & ( in_county.some(County) ) ]

    # Creating instances
    usa = Country("UnitedStatesofAmerica")
    usa.abbrev.append("USA")

    mass = State("Massachusetts", in_country = [usa])
    vermont = State("Vermont", in_country = [usa])

    suffolk = County("Suffolk", in_state = [mass])
    essex = County("Essex", in_state = [mass])
    washington = County("Washington", in_state = [vermont])
    chittenden = County("Chittenden", in_state = [vermont])

    boston = City("Boston", in_county = [suffolk])
    boston.zip_code.append("02108")
    boston.population.append(617594)

    andover = City("Andover", in_county = [essex])
    andover.zip_code.append("01810")
    andover.population.append(33201)
    
    montpelier = City("Montpelier", in_county = [washington])
    montpelier.zip_code.append("05601")
    montpelier.population.append(7855)    

    burlington = City("Burlington", in_county = [chittenden])
    burlington.zip_code.append("05401")
    burlington.population.append(42211)

    canada = Country("Canada")
    canada.abbrev.append("CA")

    quebec = Province("Quebec", in_country = [canada])

    montreal = City("Montreal", in_province = [quebec])
    montreal.zip_code.append("66023")
    montreal.population.append(1704694)

    quebeccity = City("Quebec", in_province = [quebec])
    quebeccity.zip_code.append("23027")
    quebeccity.population.append(531902)         

# Starting the reasoner
sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
graph = default_world.as_rdflib_graph()

print("Infered relations")
print(vermont, vermont.INDIRECT_part_of)
print(montpelier, montpelier.INDIRECT_part_of)
print(burlington, burlington.INDIRECT_part_of)

print(mass, mass.INDIRECT_part_of)
print(andover, andover.INDIRECT_part_of)
print(boston, boston.INDIRECT_part_of)

print("Infered classes")
print("Montreal is inferred as:", montreal, montreal.is_a)
print("Boston is inferred as:", boston, boston.is_a)

RDF = URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
UC = URIRef('http://example.org/onto_country#')
print("Namespaces: {} and {}".format(RDF, UC))

try:
    print("\n**** Country ****")
    print("Countries:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:Country }', initNs={'UC':UC, 'RDF': RDF})))
    print("Country's abbreviation:", list(graph.query_owlready('SELECT DISTINCT ?a ?c WHERE { ?a UC:abbrev ?c }', initNs={'UC':UC, 'RDF': RDF})))
    print("Country which abbreviation is CA:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a UC:abbrev "CA" }', initNs={'UC':UC, 'RDF': RDF})))

    print("\n**** State ****")
    print("States:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:State }', initNs={'UC':UC, 'RDF': RDF})))
    print("States in Canada:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:State . ?a UC:in_country UC:Canada }', initNs={'UC':UC, 'RDF': RDF})))
    print("States in USA:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:State . ?a UC:in_country UC:UnitedStatesofAmerica }', initNs={'UC':UC, 'RDF': RDF})))

    print("\n**** County ****")
    print("Counties in Mass:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:County . ?a UC:in_state UC:Massachusetts }', initNs={ 'UC':UC, 'RDF': RDF })))
    print("Counties in USA:", list(graph.query_owlready('SELECT DISTINCT ?a ?c WHERE { ?a RDF:type UC:County . ?a UC:part_of UC:UnitedStatesofAmerica . ?c RDF:type UC:State}', initNs={'UC':UC, 'RDF': RDF})))

    print("\n**** Provinces ****")
    print("Provinces:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:Province }', initNs={'UC':UC, 'RDF': RDF})))
    print("Provinces in Canada:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:Province . ?a UC:in_country UC:Canada }', initNs={'UC':UC, 'RDF': RDF})))
    print("Provinces in USA:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:Province . ?a UC:in_country UC:UnitedStatesofAmerica }', initNs={'UC':UC, 'RDF': RDF})))

    print("\n**** Cities ****")
    print("Cities:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:City }', initNs={'UC':UC, 'RDF': RDF})))
    print("Cities in USA:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:City . ?a UC:part_of UC:UnitedStatesofAmerica }', initNs={'UC':UC, 'RDF': RDF})))
    print("Cities in Canada:", list(graph.query_owlready('SELECT DISTINCT ?a WHERE { ?a RDF:type UC:City . ?a UC:part_of UC:Canada }', initNs={'UC':UC, 'RDF': RDF})))

    print("\n**** Counting ****")
    print("Population of Cities:", list(graph.query_owlready('SELECT DISTINCT ?a ?c WHERE { ?a RDF:type UC:City . ?a UC:population ?c }', initNs={'UC':UC, 'RDF': RDF})))
    print("Population of Cities in USA:", list(graph.query_owlready('SELECT DISTINCT ?a ?c WHERE { ?a UC:part_of UC:UnitedStatesofAmerica . ?a UC:population ?c . }', initNs={'UC':UC, 'RDF': RDF})))
    print("Total Population of Cities in USA:", list(graph.query_owlready('SELECT (SUM(?c) as ?sum) WHERE { ?a RDF:type UC:City . ?a UC:part_of UC:UnitedStatesofAmerica . ?a UC:population ?c . }', initNs={'UC':UC, 'RDF': RDF})))
    print("Cities in USA with pop > 30K:", list(graph.query_owlready('SELECT DISTINCT ?a ?c WHERE { ?a RDF:type UC:City . ?a UC:part_of UC:UnitedStatesofAmerica . ?a UC:population ?c. FILTER ( ?c > 30000) } ', initNs={'UC':UC, 'RDF': RDF})))
    print("Number of cities in Canada:", list(graph.query_owlready('SELECT DISTINCT (count(?a) as ?count) WHERE { ?a RDF:type UC:City . ?a UC:part_of UC:Canada . ?a UC:population ?c. } ', initNs={'UC':UC, 'RDF': RDF})))
    
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print("Exception: {} {}".format(exc_type, exc_tb.tb_lineno))
