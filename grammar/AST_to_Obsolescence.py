from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker
from .ObsolescenceLexer import ObsolescenceLexer
from .ObsolescenceParser import ObsolescenceParser
from .ModelCreationListener import ModelCreationListener
from besser.BUML.metamodel.structural import DomainModel
from metamodel import enable_obsolescence
import os

def obsolescence_declaration(obsolescence_rules: str, buml_model: DomainModel):
    lexer = ObsolescenceLexer(FileStream(obsolescence_rules))
    parser = ObsolescenceParser(CommonTokenStream(lexer))
    parse_tree = parser.obsolescence()
    # file creation
    if not os.path.exists("buml"):
        os.makedirs("buml")
    output = open("buml/obsolescence_definition.py","w")
    listen = ModelCreationListener(output)
    walker = ParseTreeWalker()
    walker.walk(listen, parse_tree)
    output.close()
    # model creation
    namespace = {}
    with open("buml/obsolescence_definition.py", 'r') as obs_model:
        code = obs_model.read()
        exec(code, namespace)
    function = namespace.get('create_model')
    obsolescence_model = function(buml_model)
    enable_obsolescence()
    return obsolescence_model