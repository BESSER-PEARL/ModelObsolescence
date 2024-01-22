import datetime
from dateutil.relativedelta import relativedelta
from metamodel import ObsolescenceDeclaration, FixedObsolescence, PeriodicObsolescence
from besser.BUML.metamodel.structural import DomainModel, NamedElement
from metamodel import Revision, CriticalType

def check_obsolescence(obsolescence_declaration: ObsolescenceDeclaration):
    for rule in obsolescence_declaration.obs_declarations:
        if type(rule) == FixedObsolescence and rule.active == True:
            check_temporal_fixed(rule)
        if type(rule) == PeriodicObsolescence and rule.active == True:
            check_temporal_periodic(rule)

def check_temporal_fixed(rule: FixedObsolescence):
    if rule.date <= datetime.datetime.now():
        for impact in rule.impacts:
            for element in impact.elements:
                element.obsolete = 100
                create_revision(element=element, impact=100)
                alert(element=element, criticality=rule.criticality, rule=rule)
                propagate_obsolscence(element=element, propagation_level=impact.propagation_level, impact=100, 
                                          p_impact_loss=impact.propagation_impact, criticality=rule.criticality, rule=rule)
                rule.active = False
                
def check_temporal_periodic(rule: PeriodicObsolescence):
    periodicity = convert_to_datetime(value=rule.periodicity, unit=rule.unit)
    for impact in rule.impacts:
        for element in impact.elements:
            last_revision = element.revision_history[-1].timestamp
            if (datetime.datetime.now() - periodicity >= last_revision):
                if element.obsolete + impact.impact > 100:
                    element.obsolete = 100
                else:
                    element.obsolete += impact.impact
                create_revision(element=element, impact=impact.impact)
                alert(element=element, criticality=rule.criticality, rule=rule)
                propagate_obsolscence(element=element, propagation_level=impact.propagation_level, impact=impact.impact, 
                                          p_impact_loss=impact.propagation_impact, criticality=rule.criticality, rule=rule)

def alert(element: NamedElement, criticality: CriticalType, rule: ObsolescenceDeclaration):
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-6]
    if element.obsolete >= 100:
        print(rule.name + "; \t" + time_now + "; \t" + "\033[91m" + element.name + " is obsolete; \t Criticality: " + criticality.value + "\033[0m")
    else:
        print(rule.name + "; \t" + time_now + "; \t" + element.name + " obsolescence increased to " + str(element.obsolete) + "%")

def convert_to_datetime(value, unit):
    unit_mapping = {
        's': relativedelta(seconds=value),
        'min': relativedelta(minutes=value),
        'h': relativedelta(hours=value),
        'd': relativedelta(days=value),
        'm': relativedelta(months=value),
        'y': relativedelta(years=value),
    }

    if unit not in unit_mapping:
        raise ValueError(f'Invalid unit: {unit}')
    
    time_period = unit_mapping[unit]
    return time_period

def create_revision(element: NamedElement, impact: float):
    comment = "Obsolescence of the element " + element.name + " increased by " + str(impact)
    revision: Revision = Revision(name="Obsolescence revision", reviewer="runtime_engine", comment=comment)
    element.add_revision(revision)

def propagate_obsolscence(element: NamedElement, propagation_level: int, impact: float, p_impact_loss: float, 
                          criticality: CriticalType, rule: ObsolescenceDeclaration):
    propagation_impact = impact * (p_impact_loss / 100)
    elems = set()
    layers = dict()
    layers[0] = {element}
    impacted_elements = set()
    for i in range(0, propagation_level):
        for elem in layers[i]:
            for end in elem.association_ends():
                elems.add(end.type)
                impacted_elements.add(end.type)
        layers[i+1] = elems.copy()
        elems.clear()

    impacted_elements.discard(element)
    for impacted_el in impacted_elements:
        if impacted_el.obsolete + propagation_impact > 100:
            impacted_el.obsolete = 100
        else:
            impacted_el.obsolete += propagation_impact
        alert(impacted_el, criticality=criticality, rule=rule)