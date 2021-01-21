from owlready2 import *
onto = get_ontology("AtlasZwierzat.owl").load()
print(list(onto.classes()))
print(list(onto.object_properties()))