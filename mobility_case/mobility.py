import time, datetime
from besser.BUML.metamodel.structural import DomainModel
from besser.utilities import ModelSerializer
from metamodel import ObsolescenceDeclaration
from runtime_engine import check_obsolescence
from grammar import obsolescence_declaration

serializer: ModelSerializer = ModelSerializer()
mobility_model: DomainModel = serializer.load(model_path="mobility.buml")

# Obsolescence declaration
obs_model: ObsolescenceDeclaration = obsolescence_declaration(obsolescence_rules="obsolescence_rules.txt", domain_model=mobility_model, date=datetime.datetime(2024, 2, 1))

# check model obsolescence
check_obsolescence(obsolescence_declaration=obs_model, date=datetime.datetime(2024, 3, 1))
time.sleep(1)
check_obsolescence(obsolescence_declaration=obs_model, date=datetime.datetime(2024, 4, 1))
time.sleep(1)
check_obsolescence(obsolescence_declaration=obs_model, date=datetime.datetime(2024, 5, 1))
time.sleep(1)
check_obsolescence(obsolescence_declaration=obs_model, date=datetime.datetime(2024, 6, 1))
time.sleep(1)
check_obsolescence(obsolescence_declaration=obs_model, date=datetime.datetime(2024, 7, 1))
time.sleep(1)
check_obsolescence(obsolescence_declaration=obs_model, date=datetime.datetime(2024, 8, 1))