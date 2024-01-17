# Add Python Path
#import sys
#sys.path.append("../")

from grammar import obsolescence_declaration
from besser.BUML.notations.plantUML import plantuml_to_buml
from besser.BUML.metamodel.structural import DomainModel, Class
from metamodel import ObsolescenceDeclaration, Change, Revision
from runtime_engine import check_obsolescence
import datetime

#PlantUML to BUML using ANTLR
modeltest: DomainModel = plantuml_to_buml(plantUML_model_path='target_model.plantuml')

# Obsolescence declaration
obs_model: ObsolescenceDeclaration = obsolescence_declaration(obsolescence_rules="obsolescence_declaration.txt", buml_model=modeltest)

# Add changes to the Book class
change_1 = Change(name="Attribute updated", timestamp=datetime.datetime(2023, 12, 15))
change_2 = Change(name="Class name updated", timestamp=datetime.datetime(2024, 1, 2))
book = modeltest.get_class_by_name(class_name="Book")
book.change_history = [change_1, change_2]

# check model obsolescence
check_obsolescence(obsolescence_declaration=obs_model, buml_model=obs_model)