from owlready2 import *
onto = get_ontology("Atlas_Zwierzat.owl").load()
print(list(onto.classes()))
print(list(onto.object_properties()))
print(list(onto.data_properties()))


with onto:
    sync_reasoner_pellet() # Wnioskowanie Pelletem



