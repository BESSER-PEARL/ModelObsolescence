# Add Python Path
#import sys
#sys.path.append("../")

from grammar import obsolescence_declaration
from besser.BUML.notations.plantUML import plantuml_to_buml
from besser.BUML.metamodel.structural import DomainModel, Class
from metamodel import ObsolescenceDeclaration, Change, Revision
from runtime_engine import check_obsolescence
import datetime, time

#PlantUML to BUML using ANTLR
modeltest: DomainModel = plantuml_to_buml(plantUML_model_path='target_model.plantuml')

# Obsolescence declaration
obs_model: ObsolescenceDeclaration = obsolescence_declaration(obsolescence_rules="obsolescence_declaration.txt", buml_model=modeltest)

book = modeltest.get_class_by_name(class_name="Book")

# check model obsolescence
time.sleep(3)
check_obsolescence(obsolescence_declaration=obs_model)

time.sleep(3)
check_obsolescence(obsolescence_declaration=obs_model)


'''
for revision in book.revision_history:
    print(revision)


author = modeltest.get_class_by_name(class_name="Author")
for revision in author.revision_history:
    print (revision.comment + "   reviewer: " + revision.reviewer)
print("Obsolescence author: " + str(author.obsolete))
'''
# Add revision
#revision: Revision = Revision(name="Revision 1", reviewer="Manager1")
#book.add_revision(revision)
