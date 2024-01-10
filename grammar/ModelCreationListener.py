from .ObsolescenceListener import ObsolescenceListener
from .ObsolescenceParser import ObsolescenceParser

class ModelCreationListener(ObsolescenceListener):

    def __init__(self, output):
        self.output = output
        self.__obs_text: str = ""
        self.__impact_text: str = ""
        self.__impact_counter: int = 0
        self.__obs_rule_list: list = list()
        self.__impact_list: list = list()
        self.__element_list: list = list()

    def enterObsolescence(self, ctx:ObsolescenceParser.ObsolescenceContext):
        text = "import datetime \nfrom BUML.metamodel.structural import DomainModel \n"
        text += "from metamodel.obsolescence import ObsolescenceDeclaration, ObsolescenceRulesModel, Impact, \\\n\tFixedObsolescence, PeriodicObsolescence, InternalObsolescence, DataObsolescence, CriticalType \n\n"
        text += "def create_model(buml_model: DomainModel): \n"
        self.output.write(text)

    def exitObsolescence(self, ctx: ObsolescenceParser.ObsolescenceContext):
        obs_rules = ", ".join(self.__obs_rule_list)
        text = "\tobsolescence_model = ObsolescenceRulesModel(name=\"" + ctx.model.ID().getText() + "_obs\", obs_declarations={" + obs_rules + "})"
        self.output.write("\t# Definition of the Obsolescence Model \n")
        self.output.write(text)
        self.output.write("\n\n\treturn obsolescence_model")

    def enterObsolescenceDeclaration(self, ctx:ObsolescenceParser.ObsolescenceDeclarationContext):
        self.output.write("\t# Definition of the <<" + ctx.ID().getText() + ">> obsolescence rule \n")
        self.__impact_list = []
        self.__impact_counter = 0
        obs_type = get_obs_type(ctx)
        self.__obs_text = "\t" + ctx.ID().getText() + " = "+ obs_type +"(name=\"" + ctx.ID().getText() \
            + "\", criticality=CriticalType." + ctx.criticalityType().getText() + ", confidence=" + ctx.criticalityType().getText() \
            + ", date_set=datetime.datetime.now()"
    
    def exitObsolescenceDeclaration(self, ctx:ObsolescenceParser.ObsolescenceDeclarationContext):
        impacts = ", ".join(self.__impact_list)
        self.__obs_text += ", impacts={" + impacts + "}) \n"
        self.output.write(self.__obs_text + "\n")
        self.__obs_rule_list.append(ctx.ID().getText())

    def enterInternalDeclaration(self, ctx:ObsolescenceParser.InternalDeclarationContext):
        self.__obs_text += ", rule=" + ctx.STRING().getText()

    def enterDataDeclaration(self, ctx:ObsolescenceParser.DataDeclarationContext):
        self.__obs_text += ", discrepancy=" + ctx.INT().getText()

    def enterDateReached(self, ctx:ObsolescenceParser.DateReachedContext):
        self.__obs_text += ", date=datetime.datetime("+ ctx.until.INT(2).getText() + ", " + ctx.until.INT(1).getText() + ", " + ctx.until.INT(0).getText() + ")"

    def enterDateRecurring(self, ctx:ObsolescenceParser.DateRecurringContext):
        self.__obs_text += ", periodicity=" + ctx.every.INT().getText() + ", unit=\"" + ctx.every.tUnit().getText() + "\""

    def enterImpact(self, ctx: ObsolescenceParser.ImpactContext):
        self.__element_list = []
        self.__impact_counter += 1
        impact_name: str = ctx.parentCtx.ID().getText() + "_impact_" + str(self.__impact_counter)
        self.__impact_text = "\t" + impact_name + " = Impact(name=\"" + impact_name +"\", elements={"
        self.__impact_list.append(impact_name)

    def exitImpact(self, ctx: ObsolescenceParser.ImpactContext):
        elements = ", ".join(self.__element_list)
        self.__impact_text += elements + "}, impact= " + ctx.INT(0).getText() + ", propagation_level= " + ctx.INT(1).getText() \
            + ", propagation_impact= " + ctx.INT(2).getText() + ") \n"
        self.output.write(self.__impact_text)  

    def enterClass(self, ctx: ObsolescenceParser.ClassContext):
        elem = "buml_model.get_class_by_name(\"" + ctx.ID().getText() + "\")"
        self.__element_list.append(elem)
    
    def enterAttribute(self, ctx: ObsolescenceParser.AttributeContext):
        self.__element_list.append(ctx.ID(0).getText())

def get_obs_type(ctx: ObsolescenceParser.ObsolescenceDeclarationContext):
    obs_type: str = "ObsolescenceDeclaration"
    for chl in ctx.children:
        if isinstance(chl, ObsolescenceParser.InternalDeclarationContext):
            obs_type = "InternalObsolescence"
        elif isinstance(chl, ObsolescenceParser.DataDeclarationContext):
            obs_type = "DataObsolescence"
        elif isinstance(chl, ObsolescenceParser.TemporalDeclarationContext):
            if chl.fixed is not None:
                obs_type = "FixedObsolescence"
            elif chl.periodic is not None:
                obs_type = "PeriodicObsolescence"
    return obs_type   
