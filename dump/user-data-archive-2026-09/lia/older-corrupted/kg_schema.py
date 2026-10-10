from owlready2 import
onto = get_ontology("http://example.com/myOnto.owl")
with onto:
    Entity
    class Entity(Thing): pass
hasName Entity
class hasName(Entity):
    'class hasName(Property): domain = [Entity] range = [str]`
    `my_entity = Entity('Lia')`
    `my_entity.hasName.append('Lia.cli')`
    `onto.save()`
