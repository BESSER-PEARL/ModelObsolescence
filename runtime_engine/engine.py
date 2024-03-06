import datetime, os
from dateutil.relativedelta import relativedelta
from metamodel import ObsolescenceDeclaration, FixedObsolescence, PeriodicObsolescence
from besser.BUML.metamodel.structural import DomainModel, NamedElement
from metamodel import Revision, CriticalType
from runtime_engine.report import Report

#def check_obsolescence(obsolescence_declaration: ObsolescenceDeclaration):
def check_obsolescence(obsolescence_declaration: ObsolescenceDeclaration, date=datetime.datetime.now()):
    report: Report = Report()
    for rule in obsolescence_declaration.obs_declarations:
        if type(rule) == FixedObsolescence and rule.active == True:
            check_temporal_fixed(rule, report, date)
        if type(rule) == PeriodicObsolescence and rule.active == True:
            check_temporal_periodic(rule, report, date)
    if not os.path.exists("report"):
        os.makedirs("report")
    report_name = "report/" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(":", "-")
    report.generate_report(report_name, obsolescence_declaration.name, date=date)

def check_temporal_fixed(rule: FixedObsolescence, report, date):
    #if rule.date <= datetime.datetime.now():
    if rule.date <= date:
        for impact in rule.impacts:
            for element in impact.elements:
                element.obsolete = 100
                propagate_obsolscence(element=element, propagation_level=impact.propagation_level, impact=100, 
                                          p_impact_loss=impact.propagation_impact, criticality=rule.criticality, 
                                          rule=rule, report=report)
                create_revision(element=element, impact=100, date=date)
                alert(element=element, criticality=rule.criticality, rule=rule, report=report)
                rule.active = False
                
def check_temporal_periodic(rule: PeriodicObsolescence, report, date):
    periodicity = convert_to_datetime(value=rule.periodicity, unit=rule.unit)
    for impact in rule.impacts:
        for element in impact.elements:
            last_revision = element.revision_history[-1].timestamp
            #if (datetime.datetime.now() - periodicity >= last_revision):
            if (date - periodicity >= last_revision):
                if element.obsolete + impact.impact > 100:
                    element.obsolete = 100
                else:
                    element.obsolete += impact.impact
                propagate_obsolscence(element=element, propagation_level=impact.propagation_level, impact=impact.impact, 
                                          p_impact_loss=impact.propagation_impact, criticality=rule.criticality, 
                                          rule=rule, report=report)
                create_revision(element=element, impact=impact.impact, date=date)
                alert(element=element, criticality=rule.criticality, rule=rule, report=report)

def alert(element: NamedElement, criticality: CriticalType, rule: ObsolescenceDeclaration, report):
    if element.obsolete >= 100:
        alert = [element.name, "The class is obsolete", rule.name, criticality.value]
        report.add_obsolete(alert)
        
    else:
        alert = [element.name, "Obsolescence of the class increased to " + str(element.obsolete) + "%", rule.name, criticality.value]
        report.add_alert(alert)
    print(alert)

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

def create_revision(element: NamedElement, impact: float, date):
    comment = "Obsolescence of the element " + element.name + " increased by " + str(impact)
    #revision: Revision = Revision(name="Obsolescence revision", reviewer="runtime_engine", comment=comment)
    revision: Revision = Revision(name="Obsolescence revision", reviewer="runtime_engine", comment=comment, timestamp=date)
    element.add_revision(revision)

def propagate_obsolscence(element: NamedElement, propagation_level: int, impact: float, p_impact_loss: float, 
                          criticality: CriticalType, rule: ObsolescenceDeclaration, report):
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
        alert(impacted_el, criticality=criticality, rule=rule, report=report)