from besser.BUML.metamodel.structural import NamedElement, DomainModel, Type, Class, \
        Property, PrimitiveDataType, Multiplicity, Association, BinaryAssociation, Generalization, \
        GeneralizationSet, AssociationClass, EnumerationLiteral, Enumeration

from besser.utilities import ModelSerializer

# Primitive Data Types 
int_type = PrimitiveDataType("int")
float_type = PrimitiveDataType("float")
str_type = PrimitiveDataType("str")

# ChargingState Ennum
charging_state: Enumeration = Enumeration(name="ChargingState", literals={
    EnumerationLiteral(name="available", owner=None),
    EnumerationLiteral(name="charging", owner=None),
    EnumerationLiteral(name="offline", owner=None)})

# CoatingTypes Ennum
coating_types: Enumeration = Enumeration(name="CoatingTypes", literals={
    EnumerationLiteral(name="gravel", owner=None),
    EnumerationLiteral(name="asphalt", owner=None),
    EnumerationLiteral(name="pavingStone", owner=None)})

# StationType Ennum
station_type: Enumeration = Enumeration(name="StationType", literals={
    EnumerationLiteral(name="busStop", owner=None),
    EnumerationLiteral(name="charger", owner=None),
    EnumerationLiteral(name="supercharger", owner=None)})

# Segment class definition 
Segment_slope: Property = Property(name="slope", property_type=int_type)
Segment_distance: Property = Property(name="distance", property_type=float_type)
Segment_coating: Property = Property(name="coating", property_type=str_type)
Segment_GeoPath: Property = Property(name="GeoPath", property_type=str_type)
Segment: Class = Class(name="Segment", attributes={Segment_slope, Segment_distance, Segment_coating, Segment_GeoPath})

# Line class definition 
Line_lineNumber: Property = Property(name="lineNumber", property_type=int_type)
Line: Class = Class(name="Line", attributes={Line_lineNumber})

# ChargingPoint class definition 
ChargingPoint_type: Property = Property(name="type", property_type=str_type)
ChargingPoint_maxPower: Property = Property(name="maxPower", property_type=int_type)
ChargingPoint_state: Property = Property(name="state", property_type=str_type)
ChargingPoint: Class = Class(name="ChargingPoint", attributes={ChargingPoint_type, ChargingPoint_maxPower, ChargingPoint_state})

# BusStop class definition 
BusStop: Class = Class(name="BusStop", attributes=set())

# Road class definition 
Road_name: Property = Property(name="name", property_type=str_type)
Road: Class = Class(name="Road", attributes={Road_name})

# Vehicle class definition 
Vehicle_brand: Property = Property(name="brand", property_type=str_type)
Vehicle: Class = Class(name="Vehicle", attributes={Vehicle_brand})

# ElectricBus class definition 
ElectricBus_batteryCapability: Property = Property(name="batteryCapability", property_type=int_type)
ElectricBus: Class = Class(name="ElectricBus", attributes={ElectricBus_batteryCapability})

# Bus class definition 
Bus_tankCapability: Property = Property(name="tankCapability", property_type=int_type)
Bus: Class = Class(name="Bus", attributes={Bus_tankCapability})

# Point class definition 
Point: Class = Class(name="Point", attributes={})

# Relationships
points: BinaryAssociation = BinaryAssociation(name="points", ends={
        Property(name="points", property_type=Segment, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="points", property_type=Point, multiplicity=Multiplicity(2, 2), is_navigable=True)})
segments: BinaryAssociation = BinaryAssociation(name="segments", ends={
        Property(name="segments", property_type=Point, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="segments", property_type=Segment, multiplicity=Multiplicity(1, "*"), is_navigable=True)})
has_segments: BinaryAssociation = BinaryAssociation(name="has_segments", ends={
        Property(name="has_segments", property_type=Line, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="has_segments", property_type=Segment, multiplicity=Multiplicity(2, "*"), is_navigable=True)})
has_points: BinaryAssociation = BinaryAssociation(name="has_points", ends={
        Property(name="has_points", property_type=Line, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="has_points", property_type=Point, multiplicity=Multiplicity(2, "*"), is_navigable=True)})
lines: BinaryAssociation = BinaryAssociation(name="lines", ends={
        Property(name="lines", property_type=BusStop, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="lines", property_type=Line, multiplicity=Multiplicity(1, "*"), is_navigable=True)})
is_hosting: BinaryAssociation = BinaryAssociation(name="is_hosting", ends={
        Property(name="is_hosting", property_type=BusStop, multiplicity=Multiplicity(0, 1), is_navigable=False),
        Property(name="is_hosting", property_type=ChargingPoint, multiplicity=Multiplicity(1, "*"), is_navigable=True)})

# Generalizations
gen_Vehicle_ElectricBus: Generalization = Generalization(general=Vehicle, specific=ElectricBus)
gen_Vehicle_Bus: Generalization = Generalization(general=Vehicle, specific=Bus)
gen_Point_BusStop: Generalization = Generalization(general=Point, specific=BusStop)
gen_Segment_Road: Generalization = Generalization(general=Segment, specific=Road)


# Domain Model
domain: DomainModel = DomainModel(name="mobility", types={Segment, Line, ChargingPoint, BusStop, Road, Vehicle, ElectricBus, Bus}, 
                                  associations={points, segments, has_segments, has_points, lines, is_hosting}, 
                                  generalizations={gen_Vehicle_ElectricBus, gen_Vehicle_Bus, gen_Point_BusStop, gen_Segment_Road},
                                  enumerations={charging_state, coating_types, station_type})


serializer: ModelSerializer = ModelSerializer()
serializer.dump(model=domain)