from owlready2 import *
onto = get_ontology("Atlas_Zwierzat.owl").load()
print(list(onto.classes()))
print(list(onto.object_properties()))