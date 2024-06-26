from besser.BUML.metamodel.structural import NamedElement, DomainModel, Class
import datetime

class Designer(NamedElement):
    def __init__(self, name: str, position: str):
        super.__init__(name)
        self.position: str = position

    @property
    def position(self) -> str:
        return self.__position

    @position.setter
    def position(self, position: str):
        self.__position = position

class Change(NamedElement):
    def __init__(self, name: str, description: str, element: NamedElement, designer: Designer, timestamp: datetime = datetime.datetime.now()):
        super().__init__(name)
        self.description: str = description
        self.element: NamedElement = element
        self.designer: Designer = designer
        self.timestamp: datetime = timestamp

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        self.__description = description

    @property
    def element(self) -> NamedElement:
        return self.__element
    
    @element.setter
    def element(self, element: NamedElement):
        self.__element = element

    @property
    def designer(self) -> Designer:
        return self.__designer
    
    @designer.setter
    def designer(self, designer: Designer):
        self.__designer = designer

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        self.__timestamp = timestamp
    
    def __repr__(self):
        return f"Change({self.name}, {self.element.name})"

class Revision(NamedElement):
    def __init__(self, name: str, reviewer: Designer, comment: str, changes:set[Change] = set(), timestamp: datetime = datetime.datetime.now()):
        super().__init__(name)
        self.reviewer: Designer = reviewer
        self.comment: str = comment
        self.changes: set[Change] = changes
        self.timestamp: datetime = timestamp

    @property
    def reviewer(self) -> Designer:
        return self.__reviewer
    
    @reviewer.setter
    def reviewer(self, reviewer: Designer):
        self.__reviewer = reviewer

    @property
    def changes(self) -> set[Change]:
        return self.__changes
    
    @changes.setter
    def changes(self, changes: set[Change]):
        self.__changes = changes

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: bool):
        self.__timestamp = timestamp
    
    def __repr__(self):
        return f"Revision({self.name}, {self.comment}, {self.reviewer}, {self.changes})"

##-- Change History Methods
@property
def change_history(self) -> list[Change]:
    return self.changes

@change_history.setter
def change_history(self, changes: list[Change]):
    self.changes = changes

def add_change(self, change: Change):
    self.changes.append(change)

##-- Revision History Methods
@property
def revision_history(self) -> list[Revision]:
    return self.revisions

@revision_history.setter
def revision_history(self, revisions: list[Revision]):
    self.revisions = revisions

def add_revision(self, revision: Revision):
    self.revisions.append(revision)
    if revision.reviewer != "runtime_engine":
        self.obsolete = 0

#--Add obsolescence methods
def add_obsolescence_methods(artifact:any):
    artifact.change_history = change_history
    artifact.revision_history = revision_history
    artifact.add_change = add_change
    artifact.add_revision = add_revision

#--Add obsolescence attributes
def add_obsolescence_attributes(model: DomainModel):
    for cls in model.get_classes():
        cls.obsolete: float = 0
        cls.changes: list[Change] = list()
        cls.revisions: list[Revision] = list()

#--Enable obsolescence properties and methods
def enable_obsolescence(model:DomainModel, date=datetime.datetime.now()):
    add_obsolescence_attributes(model=model)
    add_obsolescence_methods(artifact=Class)
    create_first_revision(model, date=date)

#--Disable obsolescence properties and methods for a specific object or class
def disable_obsolescence_artifact(artifact:any):
    del artifact.changes
    del artifact.revisions
    del artifact.change_history
    del artifact.revision_history
    del artifact.add_change
    del artifact.add_revision

#--Disable obsolescence properties and methods
def disable_obsolescence():
    disable_obsolescence_artifact(artifact=Class)

#--Create the first revision for all classes
def create_first_revision(model:DomainModel, date):
    for cls in model.get_classes():
        cls.add_revision(Revision(name="First register", reviewer="runtime_engine", comment="First register", timestamp=date))