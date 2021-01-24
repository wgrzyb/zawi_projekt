from owlready2 import *
import owlready2

### Playground for ontologies - nothing related to main app here

# owlready2.JAVA_HOME = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"
onto_path.append('./')
onto = get_ontology("Atlas_Zwierzat.owl").load()
#print(onto.base_iri)


# classess = list(onto.classes())
# print(list(onto.object_properties()))
# print(list(onto.data_properties()))
# print(onto.get_instances_of(onto.Cecha))
# print(onto.get_instances_of(onto.Gromada))
# print("gat",onto.get_instances_of(onto.Gatunek))
# print(onto.get_instances_of(onto.Kategoria_zagrozenia_wyginieciem))
# print(onto.get_instances_of(onto.Obszar))
# print(onto.get_instances_of(onto.Rodzaj))
# print(onto.get_instances_of(onto.Sposob_odzywiania))
# print(onto.get_instances_of(onto.Umiejetnosc))




# close_world(onto)
# print(onto.search())
# print(onto.search(posiada_ceche="*"))
def reason(onto):
    with onto:
        Imp().set_as_rule("Gatunek(?G), posiada_umiejetnosc(?G, Latanie) -> posiada_ceche(?G, Skrzydla)")
        Imp().set_as_rule("Gatunek(?G) , Rodzaj(?R) , nalezy_do_rodzaju(?G, ?R) , nalezy_do_gromady(?R, Ptaki) -> posiada_liczbe_odnozy(?G, 2)")
        Imp().set_as_rule("Gatunek(?G) , posiada_ceche(?G, Traba) -> posiada_liczbe_odnozy(?G, 4)")
        Imp().set_as_rule("Gatunek(?G) , posiada_ceche(?G, Traba) -> ma_sposob_odzywiania(?G, Roslinozernosc)")
        Imp().set_as_rule("Gatunek(?G) , nalezy_do_rodzaju(?G, ?R) , posiada_ceche(?G, Traba) -> nalezy_do_gromady(?R, Ssaki)")
        Imp().set_as_rule("Gatunek(?G) , nalezy_do_rodziny(?G, kotowate) -> posiada_liczbe_odnozy(?G, 4)")
        sync_reasoner_pellet(infer_data_property_values=True, infer_property_values=True)
    return onto

onto = reason(onto)


gatunek = 'Sarna'
gromada = 'Gromada'
rodzina = 'Rodzina'
obszar = 'Europa'

if onto['Lew_afrykanski']:
    print(onto[''])

onto_obszar = onto.Obszar(obszar)
sarna = onto.Gatunek(gatunek, wystepuje_na_obszarze=[onto[obszar]])



# result.append(onto.search(posiada_liczbe_odnozy=4))
# result.append(onto.search(posiada_ceche='*'))
# obszar = 'Afryka'
# obszar = 'all'
# result=onto.search(wystepuje_na_obszarze=[onto['Las']])
# animals = set()
#
#
# print(result)






