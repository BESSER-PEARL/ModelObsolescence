import datetime
from dateutil.relativedelta import relativedelta
from metamodel import ObsolescenceDeclaration, FixedObsolescence, PeriodicObsolescence
from besser.BUML.metamodel.structural import DomainModel, NamedElement
from metamodel import Revision, CriticalType

def check_obsolescence(obsolescence_declaration: ObsolescenceDeclaration, buml_model: DomainModel):
    for rule in obsolescence_declaration.obs_declarations:
        if type(rule) == FixedObsolescence:
            check_temporal_fixed(rule)
        if type(rule) == PeriodicObsolescence:
            check_temporal_periodic(rule)

def check_temporal_fixed(rule: FixedObsolescence):
    print("Cheking temporal fixed.... ")
    if rule.date <= datetime.datetime.now():
        for impact in rule.impacts:
            for element in impact.elements:
                element.obsolete = 100
                create_revision(element=element, impact=100)
                alert(element=element, criticality=rule.criticality)
                if impact.propagation_level >= 1:
                    propagate_obsolscence(element=element, propagation_level=impact.propagation_level, impact=impact.impact, 
                                          p_impact_loss=impact.propagation_impact, criticality=rule.criticality)
                
def check_temporal_periodic(rule: PeriodicObsolescence):
    print("Cheking temporal periodic.... ")
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
                alert(element=element, criticality=rule.criticality)

def alert(element: NamedElement, criticality: CriticalType):
    if element.obsolete >= 100:
        print(element.name + " is obsolete. Criticality: " + criticality.value)
    else:
        print(element.name + " obsolescence increased to " + str(element.obsolete) + "%")

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

def propagate_obsolscence(element: NamedElement, propagation_level: int, impact: float, p_impact_loss: float, criticality:CriticalType):
    propagation_impact = impact * (p_impact_loss / 100)
    for end in element.association_ends():
        impacted_element = end.type
        if impacted_element.obsolete + impact > 100:
            impacted_element.obsolete = 100
        else:
            impacted_element.obsolete += propagation_impact
        alert(impacted_element, criticality=criticality)