import time, datetime
from metamodel import ObsolescenceDeclaration, FixedObsolescence
from BUML.metamodel.structural import DomainModel

def check_obsolescence(obsolescence_declaration: ObsolescenceDeclaration, buml_model: DomainModel):
    for rule in obsolescence_declaration.obs_declarations:
        if type(rule) == FixedObsolescence:
            temporal_fixed(rule)

def temporal_fixed(rule: FixedObsolescence):
    for impact in rule.impacts:
        for element in impact.elements:
            print(element.name)
            print(str(impact.impact))