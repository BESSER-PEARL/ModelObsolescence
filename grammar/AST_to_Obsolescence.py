from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker
from .ObsolescenceLexer import ObsolescenceLexer
from .ObsolescenceParser import ObsolescenceParser
from .ModelCreationListener import ModelCreationListener
from BUML.metamodel.structural import DomainModel
from metamodel import ObsolescenceRulesModel
import os

class Obsolescence:

    def __init__(self, obsolescence_rules: str, buml_model: DomainModel):
        self.obsolescence_rules: str = obsolescence_rules
        self.buml_model: DomainModel = buml_model
        self.obsolescence_model: ObsolescenceRulesModel = None

    def generate_obsolescence_model(self):
        lexer = ObsolescenceLexer(FileStream(self.obsolescence_rules))
        parser = ObsolescenceParser(CommonTokenStream(lexer))
        parse_tree = parser.obsolescence()
        # file creation
        if not os.path.exists("buml"):
            os.makedirs("buml")
        output = open("buml/obsol_model.py","w")
        listen = ModelCreationListener(output)
        walker = ParseTreeWalker()
        walker.walk(listen, parse_tree)
        output.close()
        # model creation
        namespace = {}
        with open("buml/obsol_model.py", 'r') as obs_model:
            code = obs_model.read()
            exec(code, namespace)
        function = namespace.get('create_model')
        self.obsolescence_model = function(self.buml_model)
        return self.obsolescence_model

    @property
    def obsolescence_model(self) -> ObsolescenceRulesModel:
        return self.__obsolescence_model

    @obsolescence_model.setter
    def obsolescence_model(self, obsolescence_model: ObsolescenceRulesModel):
        self.__obsolescence_model = obsolescence_model
