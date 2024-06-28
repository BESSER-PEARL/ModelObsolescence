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
segment_slope: Property = Property(name="slope", type=int_type)
segment_distance: Property = Property(name="distance", type=float_type)
segment_coating: Property = Property(name="coating", type=coating_type)
segment_GeoPath: Property = Property(name="GeoPath", type=str_type)
segment: Class = Class(name="Segment", attributes={segment_slope, segment_distance, segment_coating, segment_GeoPath})

# BusLine class definition 
line_lineNumber: Property = Property(name="lineNumber", type=int_type)
busline: Class = Class(name="BusLine", attributes={line_lineNumber})

# ChargingPoint class definition 
chargingPoint_type: Property = Property(name="type", type=station_type)
chargingPoint_maxPower: Property = Property(name="maxPower", type=int_type)
chargingPoint_state: Property = Property(name="state", type=charging_state)
chargingPoint: Class = Class(name="ChargingPoint", attributes={chargingPoint_type, chargingPoint_maxPower, chargingPoint_state})

# BusStop class definition 
busStop: Class = Class(name="BusStop", attributes=set())

# Road class definition 
road_name: Property = Property(name="name", type=str_type)
road: Class = Class(name="Road", attributes={road_name})

# Vehicle class definition 
vehicle_brand: Property = Property(name="brand", type=str_type)
vehicle: Class = Class(name="Vehicle", attributes={vehicle_brand})

# Sensor class definition 
sensor_temp: Property = Property(name="temperature", type=int_type)
sensor_time: Property = Property(name="timeReach", type=time_type)
sensor: Class = Class(name="Sensor", attributes={sensor_temp, sensor_time})

# ElectricBus class definition 
electricBus_batteryCapability: Property = Property(name="batteryCapability", type=int_type)
electricBus: Class = Class(name="ElectricBus", attributes={electricBus_batteryCapability})

# Bus class definition 
bus_tankCapability: Property = Property(name="tankCapability", type=int_type)
bus: Class = Class(name="Bus", attributes={bus_tankCapability})

# Point class definition 
Point: Class = Class(name="Point", attributes={})

# Relationships
ends: BinaryAssociation = BinaryAssociation(name="ends", ends={
        Property(name="ends", type=Point, multiplicity=Multiplicity(1, 1)),
        Property(name="segments", type=segment, multiplicity=Multiplicity(1, "*"))})
routes: BinaryAssociation = BinaryAssociation(name="routes", ends={
        Property(name="has_segments", type=busline, multiplicity=Multiplicity(0, "*")),
        Property(name="routes", type=segment, multiplicity=Multiplicity(1, "*"))})
route: BinaryAssociation = BinaryAssociation(name="route", ends={
        Property(name="route", type=busline, multiplicity=Multiplicity(1, 1)),
        Property(name="bus", type=bus, multiplicity=Multiplicity(1, "*"))})
is_hosting: BinaryAssociation = BinaryAssociation(name="is_hosting", ends={
        Property(name="is_hosting", type=busStop, multiplicity=Multiplicity(0, 1)),
        Property(name="is_hosting", type=chargingPoint, multiplicity=Multiplicity(1, "*"))})
sensor_measurments: Association = Association(name="measurements", ends={
        Property(name="bus_stop", type=busStop, multiplicity=Multiplicity(0, "*")),
        Property(name="bus", type=bus, multiplicity=Multiplicity(0, "*")),
        Property(name="sensor", type=sensor, multiplicity=Multiplicity(1, "*"))})


# Generalizations
gen_Vehicle_ElectricBus: Generalization = Generalization(general=vehicle, specific=electricBus)
gen_Vehicle_Bus: Generalization = Generalization(general=vehicle, specific=bus)
gen_Point_BusStop: Generalization = Generalization(general=Point, specific=busStop)
gen_Segment_Road: Generalization = Generalization(general=segment, specific=road)


# Domain Model
domain: DomainModel = DomainModel(name="mobility_model", types={segment, busline, chargingPoint, busStop, road, vehicle, electricBus, bus, sensor}, 
                                  associations={ends, routes, route, is_hosting, sensor_measurments}, 
                                  generalizations={gen_Vehicle_ElectricBus, gen_Vehicle_Bus, gen_Point_BusStop, gen_Segment_Road},
                                  enumerations={charging_state, coating_type, station_type})


serializer: ModelSerializer = ModelSerializer()
serializer.dump(model=domain)