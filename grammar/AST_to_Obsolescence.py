import os
from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker
from .ObsolescenceLexer import ObsolescenceLexer
from .ObsolescenceParser import ObsolescenceParser
from .ModelCreationListener import ModelCreationListener
from besser.BUML.metamodel.structural import DomainModel
import tempfile

def obsolescence_declaration(obsolescence_rules: str, domain_model: DomainModel, delete_temp_file: bool = True):
    lexer = ObsolescenceLexer(FileStream(obsolescence_rules))
    parser = ObsolescenceParser(CommonTokenStream(lexer))
    parse_tree = parser.obsolescence()
    # file creation
    dir = os.getcwd() + '/temp/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    temp_file_fd, temp_file_name = tempfile.mkstemp(prefix='obs_' + domain_model.name + '_', suffix='.py', dir=dir)
    os.close(temp_file_fd)
    #output = open(temp_file_name,"w")
    
    #output = open("obs/obsolescence_definition.py","w")
    with open(temp_file_name,"w") as output:
        listen = ModelCreationListener(output)
        walker = ParseTreeWalker()
        walker.walk(listen, parse_tree)
    #output.close()
    
    # model creation
    namespace = {}
    #with open("obs/obsolescence_definition.py", 'r') as obs_model:
    with open(temp_file_name, 'r') as obs_model:
        code = obs_model.read()
        exec(code, namespace)
    function = namespace.get('create_model')
    obs_domain_model = function(domain_model)
    if delete_temp_file == True:
        os.remove(temp_file_name)
    return obs_domain_model