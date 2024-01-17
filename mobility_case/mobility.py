from besser.BUML.metamodel.structural import DomainModel
from besser.utilities import ModelSerializer


serializer: ModelSerializer = ModelSerializer()
mobility_model: DomainModel = serializer.load(model_path="mobility.buml")

