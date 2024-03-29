from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker
from .ObsolescenceLexer import ObsolescenceLexer
from .ObsolescenceParser import ObsolescenceParser
from .ModelCreationListener import ModelCreationListener
from besser.BUML.metamodel.structural import DomainModel
from metamodel import enable_obsolescence
import os

def obsolescence_declaration(obsolescence_rules: str, domain_model: DomainModel):
    lexer = ObsolescenceLexer(FileStream(obsolescence_rules))
    parser = ObsolescenceParser(CommonTokenStream(lexer))
    parse_tree = parser.obsolescence()
    # file creation
    if not os.path.exists("obs"):
        os.makedirs("obs")
    output = open("obs/obsolescence_definition.py","w")
    listen = ModelCreationListener(output)
    walker = ParseTreeWalker()
    walker.walk(listen, parse_tree)
    output.close()
    # model creation
    namespace = {}
    with open("obs/obsolescence_definition.py", 'r') as obs_model:
        code = obs_model.read()
        exec(code, namespace)
    function = namespace.get('create_model')
    obs_domain_model = function(domain_model)
    return obs_domain_model