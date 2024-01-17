from besser.BUML.metamodel.structural import NamedElement, DomainModel, Class
import datetime

class Change(NamedElement):
    def __init__(self, name: str, timestamp: datetime = datetime.datetime.now()):
        super().__init__(name)
        self.timestamp = timestamp

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: bool):
        self.__timestamp = timestamp

class Revision(NamedElement):
    def __init__(self, name: str, reviewer: str, timestamp: datetime = datetime.datetime.now()):
        super().__init__(name)
        self.reviewer = reviewer
        self.timestamp = timestamp

    @property
    def reviewer(self) -> str:
        return self.__reviewer
    
    @reviewer.setter
    def reviewer(self, reviewer: bool):
        self.__reviewer = reviewer

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, timestamp: bool):
        self.__timestamp = timestamp

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
def revision_history(self) -> set[Revision]:
    return self.revisions

@revision_history.setter
def revision_history(self, revisions: set[Revision]):
    self.revisions = revisions

def add_revision(self, revision: Revision):
    self.revisions.add(revision)

#--Enable obsolescence properties and methods for a specific object or class
def enable_obsolescence_artifact(artifact:any):
    artifact.obsolete: float = 0
    artifact.changes: list[Change] = list()
    artifact.revisions: set[Revision] = set()
    artifact.change_history = change_history
    artifact.revision_history = revision_history
    artifact.add_change = add_change
    artifact.add_revision = add_revision

#--Enable obsolescence properties and methods
def enable_obsolescence():
    enable_obsolescence_artifact(artifact=Class)

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