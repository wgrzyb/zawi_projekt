from owlready2 import *
import owlready2

### Playground for ontologies - nothing related to main app here

# owlready2.JAVA_HOME = "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java"

onto = get_ontology("Atlas.owl").load()


# print(onto.base_iri)


# classess = list(onto.classes())
# print(list(onto.object_properties()))
# print(list(onto.data_properties()))
# print(onto.get_instances_of(onto.Cecha))
# print(onto.get_instances_of(onto.Gromada))
print("gat",onto.get_instances_of(onto.Gatunek))
result=onto.search(posiada_liczbe_odnozy=4)
print(result)
# print(onto.get_instances_of(onto.Kategoria_zagrozenia_wyginieciem))
# print(onto.get_instances_of(onto.Obszar))
# print(onto.get_instances_of(onto.Rodzaj))
# print(onto.get_instances_of(onto.Sposob_odzywiania))
# print(onto.get_instances_of(onto.Umiejetnosc))
#onto.save(file='Atlas_Zwierzat_3.owl')

# close_world(onto)
# print(onto.search())
# print(onto.search(posiada_ceche="*"))




onto = reason(onto)
# onto_obszar = onto.Obszar(obszar)
# sarna = onto.Gatunek(gatunek, wystepuje_na_obszarze=[onto[obszar]])

result=onto.search(posiada_ceche='*')
print(result)
#onto.save(file='Atlas_Zwierzat_3.owl')

# gatunek = 'Pantera brodata'
# gromada = 'Ssaki zle sa'
# rodzina = 'Kotowate'
# obszar = 'Europa wschodnia'
#
# gatunek = gatunek.replace(' ', '_')
# rodzina = rodzina.replace(' ', '_')
#
# print(gatunek, rodzina)
# if not onto[gromada]:
#     onto.Gromada(gromada)
#
# if not onto[rodzina]:
#     onto.Rodzina(rodzina)
#
# if not onto[obszar]:
#     onto.Obszar(obszar)
#
# if not onto[gatunek]:
#     onto.Gatunek(gatunek, nalezy_do_gromady=[onto[gromada]],
#                           wystepuje_na_obszarze=[onto[obszar]],
#                           nalezy_do_rodziny=[onto[rodzina]])
# #
# onto.save()
#
# onto = reason(onto)
# # onto_obszar = onto.Obszar(obszar)
# # sarna = onto.Gatunek(gatunek, wystepuje_na_obszarze=[onto[obszar]])
#
# result=onto.search(posiada_liczbe_odnozy=4)
# # result.append(onto.search(posiada_ceche='*'))
# # obszar = 'Afryka'
# # obszar = 'all'
# # result=onto.search(wystepuje_na_obszarze=[onto['Las']])
# # animals = set()
# #
# #
# print(result)
