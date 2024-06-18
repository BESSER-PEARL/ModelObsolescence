import datetime 
from besser.BUML.metamodel.structural import DomainModel 
from metamodel.obsolescence import ObsolescenceDeclaration, ObsolescenceRulesModel, Impact, \
	FixedObsolescence, PeriodicObsolescence, InternalObsolescence, DataObsolescence, CriticalType 

def create_model(buml_model: DomainModel): 
	# Definition of the <<Req1>> obsolescence rule 
	Req1_impact_1 = Impact(name="Req1_impact_1", elements={buml_model.get_class_by_name("Vehicle"), buml_model.get_class_by_name("Segment")}, impact=100, propagation_level=0, propagation_impact=0) 
	Req1 = FixedObsolescence(name="Req1", criticality=CriticalType.Error, date_set=datetime.datetime.now(), date=datetime.datetime(2024, 8, 1), impacts={Req1_impact_1}) 

	# Definition of the <<Req2>> obsolescence rule 
	Req2_impact_1 = Impact(name="Req2_impact_1", elements={buml_model.get_class_by_name("ChargingPoint")}, impact=10, propagation_level=1, propagation_impact=50) 
	Req2 = PeriodicObsolescence(name="Req2", criticality=CriticalType.Warning, date_set=datetime.datetime.now(), periodicity=1, unit="m", impacts={Req2_impact_1}) 

	# Definition of the <<Req3>> obsolescence rule 
	Req3_impact_1 = Impact(name="Req3_impact_1", elements={buml_model.get_class_by_name("Sensor")}, impact=100, propagation_level=0, propagation_impact=0) 
	Req3 = DataObsolescence(name="Req3", criticality=CriticalType.Error, date_set=datetime.datetime.now(), discrepancy=20, impacts={Req3_impact_1}) 

	# Definition of the <<Req4>> obsolescence rule 
	Req4_impact_1 = Impact(name="Req4_impact_1", elements={}, impact=100, propagation_level=0, propagation_impact=0) 
	Req4 = InternalObsolescence(name="Req4", criticality=CriticalType.Warning, date_set=datetime.datetime.now(), rule="isObsolescence(BusStop) == true", impacts={Req4_impact_1}) 

	# Definition of the Obsolescence Model 
	obsolescence_model = ObsolescenceRulesModel(name="mobility_model_obs", obs_declarations={Req1, Req2, Req3, Req4})

	return obsolescence_model