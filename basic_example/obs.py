# Add Python Path
import sys
sys.path.append("../")

from grammar import Obsolescence
from BUML.notations.plantUML import plantuml_to_buml
from BUML.metamodel.structural import DomainModel

#PlantUML to BUML using ANTLR
modeltest: DomainModel = plantuml_to_buml(plantUML_model_path='target_model.plantuml')

# Obsolescence declaration
obsolescence: Obsolescence = Obsolescence(obsolescence_rules="obsolescence_declaration.txt", buml_model=modeltest)
obs_model = obsolescence.generate_obsolescence_model()

# Access obsolescence model
# obs_model = obsolescence.obsolescence_model

for obs_dec in obs_model.obs_declarations:
    print("\nRule: " + obs_dec.name)
    for impact in obs_dec.impacts:
        for element in impact.elements:
            print("\t Element: " + element.name + "\ttype: " + str(type(element)))
            #print(type(element))