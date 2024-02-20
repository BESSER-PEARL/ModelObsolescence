from besser.BUML.metamodel.structural import NamedElement
from enum import Enum
import datetime

class CriticalType(Enum):
    Warning = "Warning"
    Error = "Error"

class Impact(NamedElement):
    def __init__(self, name: str, elements: set[NamedElement], impact: float, propagation_level: int, propagation_impact: float):
        super().__init__(name)
        self.elements: set[NamedElement] = elements
        self.impact: float = impact
        self.propagation_level: int = propagation_level
        self.propagation_impact: float = propagation_impact

    @property
    def elements(self) -> set[NamedElement]:
        return self.__elements

    @elements.setter
    def elements(self, elements: set[NamedElement]):
        self.__elements = elements

    @property
    def impact(self) -> float:
        return self.__impact

    @impact.setter
    def impact(self, impact: float):
        self.__impact = impact

    @property
    def propagation_level(self) -> int:
        return self.__propagation_level

    @propagation_level.setter
    def propagation_level(self, propagation_level: int):
        self.__propagation_level = propagation_level

    @property
    def propagation_impact(self) -> float:
        return self.__propagation_impact

    @propagation_impact.setter
    def propagation_impact(self, propagation_impact: float):
        self.__propagation_impact = propagation_impact

    def __repr__(self) -> str:
        return f'Impact({self.elements},{self.impact},{self.propagation_level},{self.propagation_impact})'

class ObsolescenceDeclaration(NamedElement):

    def __init__(self, name: str, criticality: CriticalType, date_set: datetime, impacts: set[Impact], active: bool = True):
        super().__init__(name)
        self.criticality: CriticalType = criticality
        self.date_set: datetime = date_set
        self.impacts: set[Impact] = impacts
        self.active: bool = active
    
    @property
    def criticality(self) -> CriticalType:
        return self.__criticality

    @criticality.setter
    def criticality(self, criticality: CriticalType):
        self.__criticality = criticality

    @property
    def date_set(self) -> datetime:
        return self.__date_set

    @date_set.setter
    def date_set(self, date_set: datetime):
        self.__date_set = date_set
    
    @property
    def impacts(self) -> set[Impact]:
        return self.__impacts

    @impacts.setter
    def impacts(self, impacts: set[Impact]):
        self.__impacts = impacts
    
    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, active: bool):
        self.__active = active

    def __repr__(self) -> str:
        return f'ManualObs({self.name},{self.criticality},{self.date_set},{self.impacts},{self.active})'

class TemporalObsolescence(ObsolescenceDeclaration):
    pass
        
class PeriodicObsolescence(TemporalObsolescence):
    def __init__(self, name: str, criticality: CriticalType, date_set: datetime, periodicity: int, unit: str, impacts: set[Impact], active: bool = True):
        super().__init__(name, criticality, date_set, impacts, active)
        self.periodicity: int = periodicity
        self.unit: str = unit

    @property
    def periodicity(self) -> int:
        return self.__periodicity

    @periodicity.setter
    def periodicity(self, periodicity: int):
        self.__periodicity = periodicity   

    @property
    def unit(self) -> str:
        return self.__unit

    @unit.setter
    def unit(self, unit: str):
        self.__unit = unit

    def __repr__(self) -> str:
        return f'PeriodicObs({self.name},{self.criticality},{self.date_set},{self.impacts},{self.periodicity},{self.unit},{self.active})'

class FixedObsolescence(TemporalObsolescence):
    def __init__(self, name: str, criticality: CriticalType, date_set: datetime, date: datetime, impacts: set[Impact], active: bool = True):
        super().__init__(name, criticality, date_set, impacts, active)
        self.date: datetime = date

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, date: datetime):
        self.__date = date

    def __repr__(self) -> str:
        return f'FixedObs({self.name},{self.criticality},{self.date_set},{self.impacts},{self.date},{self.active})'

class InternalObsolescence(TemporalObsolescence):
    def __init__(self, name: str, criticality: CriticalType, date_set: datetime, rule: str, impacts: set[Impact], active: bool = True):
        super().__init__(name, criticality, date_set, impacts, active)
        self.rule: str = rule

    @property
    def rule(self) -> str:
        return self.__rule

    @rule.setter
    def rule(self, rule: str):
        self.__rule = rule

    def __repr__(self) -> str:
        return f'ObsDeclaration({self.name},{self.criticality},{self.date_set},{self.impacts},{self.rule},{self.active})'

class DataObsolescence(TemporalObsolescence):
    def __init__(self, name: str, criticality: CriticalType, date_set: datetime, discrepancy: int, impacts: set[Impact], active: bool = True):
        super().__init__(name, criticality, date_set, impacts, active)
        self.discrepancy: int = discrepancy

    @property
    def discrepancy(self) -> int:
        return self.__discrepancy

    @discrepancy.setter
    def discrepancy(self, discrepancy: int):
        self.__discrepancy = discrepancy

    def __repr__(self) -> str:
        return f'ObsDeclaration({self.name},{self.criticality},{self.date_set},{self.impacts},{self.discrepancy},{self.active})'

class ObsolescenceRulesModel(NamedElement):
    def __init__(self, name: str, obs_declarations: set[ObsolescenceDeclaration]):
        super().__init__(name)
        self.obs_declarations: set[ObsolescenceDeclaration] = obs_declarations
    
    @property
    def obs_declarations(self) -> set[ObsolescenceDeclaration]:
        return self.__obs_declarations

    @obs_declarations.setter
    def obs_declarations(self, obs_declarations: set[ObsolescenceDeclaration]):
        self.__obs_declarations = obs_declarations

    def __repr__(self) -> str:
        return f'ObsDeclaration({self.name},{self.obs_declarations})'