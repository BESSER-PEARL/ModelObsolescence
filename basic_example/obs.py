# Add Python Path
#import sys
#sys.path.append("../")

from grammar import obsolescence_declaration
from besser.BUML.notations.plantUML import plantuml_to_buml
from besser.BUML.metamodel.structural import DomainModel, Class
from metamodel import ObsolescenceDeclaration, enable_obsolescence, Change, Revision
from runtime_engine import check_obsolescence
import datetime, time

# PlantUML to BUML using ANTLR
modeltest: DomainModel = plantuml_to_buml(plantUML_model_path='target_model.plantuml')

# Obsolescence declaration
obs_model: ObsolescenceDeclaration = obsolescence_declaration(obsolescence_rules="obsolescence_declaration.txt", buml_model=modeltest)

# Extend the model with obsolescence attrs and methods
enable_obsolescence(model=modeltest)

# check model obsolescence
time.sleep(3)
check_obsolescence(obsolescence_declaration=obs_model)

time.sleep(3)
check_obsolescence(obsolescence_declaration=obs_model)