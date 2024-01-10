# Add Python Path
import sys
sys.path.append("../")

from grammar import obsolescence_declaration
from BUML.notations.plantUML import plantuml_to_buml
from BUML.metamodel.structural import DomainModel, Class
from metamodel import ObsolescenceDeclaration, Change, Revision
from runtime_engine import check_obsolescence

#PlantUML to BUML using ANTLR
modeltest: DomainModel = plantuml_to_buml(plantUML_model_path='target_model.plantuml')

# Obsolescence declaration
obs_model: ObsolescenceDeclaration = obsolescence_declaration(obsolescence_rules="obsolescence_declaration.txt", buml_model=modeltest)

# Add a change to the Book class
book_change = Change(name="an attribute updated")
book = modeltest.get_class_by_name(class_name="Book")
book.add_change(change=book_change)

# check model obsolescence
check_obsolescence(obsolescence_declaration=obs_model, buml_model=obs_model)