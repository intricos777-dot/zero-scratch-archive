# Watermark: Living_Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work
# Copyright (c) 2026 Living Sin (intricos777-dot) + AI agents (Hermes, Lia, opencode) - collaborative work
# Licensed under Living Sin Proprietary License (LSPL-1.0)
# See LICENSE file for details.
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
