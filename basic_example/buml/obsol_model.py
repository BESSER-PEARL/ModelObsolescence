import datetime 
from BUML.metamodel.structural import DomainModel 
from BUML.metamodel.obsolescence import ObsolescenceDeclaration, ObsolescenceRulesModel, Impact, \
	FixedObsolescence, PeriodicObsolescence, InternalObsolescence, DataObsolescence, CriticalType 

def create_model(buml_model: DomainModel): 
	# Definition of the <<internal_obs>> obsolescence rule 
	internal_obs_impact_1 = Impact(name="internal_obs_impact_1", elements={buml_model.get_class_by_name("Library")}, impact= 50, propagation_level= 2, propagation_impact= 10) 
	internal_obs = InternalObsolescence(name="internal_obs", criticality=CriticalType.Warning, confidence=Warning, date_set=datetime.datetime.now(), rule="Rule Test", impacts={internal_obs_impact_1}) 

	# Definition of the <<temp_fixed>> obsolescence rule 
	temp_fixed_impact_1 = Impact(name="temp_fixed_impact_1", elements={buml_model.get_class_by_name("Book")}, impact= 50, propagation_level= 2, propagation_impact= 10) 
	temp_fixed = FixedObsolescence(name="temp_fixed", criticality=CriticalType.Warning, confidence=Warning, date_set=datetime.datetime.now(), date=datetime.datetime(2024, 12, 15), impacts={temp_fixed_impact_1}) 

	# Definition of the <<temp_periodic>> obsolescence rule 
	temp_periodic_impact_1 = Impact(name="temp_periodic_impact_1", elements={buml_model.get_class_by_name("Book")}, impact= 50, propagation_level= 2, propagation_impact= 10) 
	temp_periodic = PeriodicObsolescence(name="temp_periodic", criticality=CriticalType.Warning, confidence=Warning, date_set=datetime.datetime.now(), periodicity=10, unit="day", impacts={temp_periodic_impact_1}) 

	# Definition of the <<data_obs>> obsolescence rule 
	data_obs_impact_1 = Impact(name="data_obs_impact_1", elements={buml_model.get_class_by_name("Author")}, impact= 50, propagation_level= 2, propagation_impact= 10) 
	data_obs = DataObsolescence(name="data_obs", criticality=CriticalType.Warning, confidence=Warning, date_set=datetime.datetime.now(), discrepancy=50, impacts={data_obs_impact_1}) 

	# Definition of the <<manual>> obsolescence rule 
	manual_impact_1 = Impact(name="manual_impact_1", elements={buml_model.get_class_by_name("Book"), buml_model.get_class_by_name("Library")}, impact= 50, propagation_level= 2, propagation_impact= 10) 
	manual_impact_2 = Impact(name="manual_impact_2", elements={buml_model.get_class_by_name("Book")}, impact= 30, propagation_level= 2, propagation_impact= 10) 
	manual = ObsolescenceDeclaration(name="manual", criticality=CriticalType.Warning, confidence=Warning, date_set=datetime.datetime.now(), impacts={manual_impact_1, manual_impact_2}) 

	# Definition of the Obsolescence Model 
	obsolescence_model = ObsolescenceRulesModel(name="TestModel_obs", obs_declarations={internal_obs, temp_fixed, temp_periodic, data_obs, manual})

	return obsolescence_model