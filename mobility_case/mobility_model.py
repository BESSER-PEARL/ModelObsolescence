from besser.BUML.metamodel.structural import DomainModel, Class,  Property, PrimitiveDataType, \
        Multiplicity, Association, BinaryAssociation, Generalization, EnumerationLiteral, Enumeration
from besser.utilities import ModelSerializer

# Primitive Data Types 
int_type = PrimitiveDataType("int")
float_type = PrimitiveDataType("float")
str_type = PrimitiveDataType("str")
time_type = PrimitiveDataType("time")

# ChargingState Enum
charging_state: Enumeration = Enumeration(name="ChargingState", literals={
    EnumerationLiteral(name="available", owner=None),
    EnumerationLiteral(name="charging", owner=None),
    EnumerationLiteral(name="offline", owner=None)})

# CoatingTypes Enum
coating_type: Enumeration = Enumeration(name="CoatingTypes", literals={
    EnumerationLiteral(name="gravel", owner=None),
    EnumerationLiteral(name="asphalt", owner=None),
    EnumerationLiteral(name="pavingStone", owner=None)})

# StationType Enum
station_type: Enumeration = Enumeration(name="StationType", literals={
    EnumerationLiteral(name="busStop", owner=None),
    EnumerationLiteral(name="charger", owner=None),
    EnumerationLiteral(name="supercharger", owner=None)})

# Segment class definition 
segment_slope: Property = Property(name="slope", property_type=int_type)
segment_distance: Property = Property(name="distance", property_type=float_type)
segment_coating: Property = Property(name="coating", property_type=coating_type)
segment_GeoPath: Property = Property(name="GeoPath", property_type=str_type)
segment: Class = Class(name="Segment", attributes={segment_slope, segment_distance, segment_coating, segment_GeoPath})

# Line class definition 
line_lineNumber: Property = Property(name="lineNumber", property_type=int_type)
line: Class = Class(name="Line", attributes={line_lineNumber})

# ChargingPoint class definition 
chargingPoint_type: Property = Property(name="type", property_type=station_type)
chargingPoint_maxPower: Property = Property(name="maxPower", property_type=int_type)
chargingPoint_state: Property = Property(name="state", property_type=charging_state)
chargingPoint: Class = Class(name="ChargingPoint", attributes={chargingPoint_type, chargingPoint_maxPower, chargingPoint_state})

# BusStop class definition 
busStop: Class = Class(name="BusStop", attributes=set())

# Road class definition 
road_name: Property = Property(name="name", property_type=str_type)
road: Class = Class(name="Road", attributes={road_name})

# Vehicle class definition 
vehicle_brand: Property = Property(name="brand", property_type=str_type)
vehicle: Class = Class(name="Vehicle", attributes={vehicle_brand})

# Sensor class definition 
sensor_temp: Property = Property(name="temperature", property_type=int_type)
sensor_time: Property = Property(name="timeReach", property_type=time_type)
sensor: Class = Class(name="Sensor", attributes={sensor_temp, sensor_time})

# ElectricBus class definition 
electricBus_batteryCapability: Property = Property(name="batteryCapability", property_type=int_type)
electricBus: Class = Class(name="ElectricBus", attributes={electricBus_batteryCapability})

# Bus class definition 
bus_tankCapability: Property = Property(name="tankCapability", property_type=int_type)
bus: Class = Class(name="Bus", attributes={bus_tankCapability})

# Point class definition 
Point: Class = Class(name="Point", attributes={})

# Relationships
points: BinaryAssociation = BinaryAssociation(name="points", ends={
        Property(name="points", property_type=segment, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="points", property_type=Point, multiplicity=Multiplicity(2, 2), is_navigable=True)})
segments: BinaryAssociation = BinaryAssociation(name="segments", ends={
        Property(name="segments", property_type=Point, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="segments", property_type=segment, multiplicity=Multiplicity(1, "*"), is_navigable=True)})
has_segments: BinaryAssociation = BinaryAssociation(name="has_segments", ends={
        Property(name="has_segments", property_type=line, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="has_segments", property_type=segment, multiplicity=Multiplicity(2, "*"), is_navigable=True)})
has_points: BinaryAssociation = BinaryAssociation(name="has_points", ends={
        Property(name="has_points", property_type=line, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="has_points", property_type=Point, multiplicity=Multiplicity(2, "*"), is_navigable=True)})
lines: BinaryAssociation = BinaryAssociation(name="lines", ends={
        Property(name="lines", property_type=busStop, multiplicity=Multiplicity(1, 1), is_navigable=False),
        Property(name="lines", property_type=line, multiplicity=Multiplicity(1, "*"), is_navigable=True)})
is_hosting: BinaryAssociation = BinaryAssociation(name="is_hosting", ends={
        Property(name="is_hosting", property_type=busStop, multiplicity=Multiplicity(0, 1), is_navigable=False),
        Property(name="is_hosting", property_type=chargingPoint, multiplicity=Multiplicity(1, "*"), is_navigable=True)})
sensor_measurments: Association = Association(name="measurements", ends={
        Property(name="bus_stop", property_type=busStop, multiplicity=Multiplicity(0, "*"), is_navigable=True),
        Property(name="bus", property_type=bus, multiplicity=Multiplicity(0, "*"), is_navigable=True),
        Property(name="sensor", property_type=sensor, multiplicity=Multiplicity(1, "*"), is_navigable=True)})


# Generalizations
gen_Vehicle_ElectricBus: Generalization = Generalization(general=vehicle, specific=electricBus)
gen_Vehicle_Bus: Generalization = Generalization(general=vehicle, specific=bus)
gen_Point_BusStop: Generalization = Generalization(general=Point, specific=busStop)
gen_Segment_Road: Generalization = Generalization(general=segment, specific=road)


# Domain Model
domain: DomainModel = DomainModel(name="mobility_model", types={segment, line, chargingPoint, busStop, road, vehicle, electricBus, bus, sensor}, 
                                  associations={points, segments, has_segments, has_points, lines, is_hosting, sensor_measurments}, 
                                  generalizations={gen_Vehicle_ElectricBus, gen_Vehicle_Bus, gen_Point_BusStop, gen_Segment_Road},
                                  enumerations={charging_state, coating_type, station_type})


serializer: ModelSerializer = ModelSerializer()
serializer.dump(model=domain)