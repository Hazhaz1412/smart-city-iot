"""
Test Orion-LD connection and create sample entities
"""
from core.orion_client import OrionLDClient
from core.ngsi_ld import (
    create_weather_station_entity,
    create_air_quality_sensor_entity,
    create_air_quality_observed_entity
)
from datetime import datetime

print("Testing Orion-LD connection...")

client = OrionLDClient()

# Test 1: Create Weather Station
print("\n1. Creating Weather Station entity...")
weather_station = create_weather_station_entity(
    station_id="test-station-1",
    name="Test Weather Station",
    latitude=21.0285,
    longitude=105.8542,
    address="Hanoi, Vietnam"
)

success = client.create_entity(weather_station)
if success:
    print("✓ Weather Station created successfully")
else:
    print("✗ Failed to create Weather Station")

# Test 2: Create Air Quality Sensor
print("\n2. Creating Air Quality Sensor entity...")
aq_sensor = create_air_quality_sensor_entity(
    sensor_id="test-aq-1",
    name="Test AQ Sensor",
    latitude=21.0285,
    longitude=105.8542
)

success = client.create_entity(aq_sensor)
if success:
    print("✓ Air Quality Sensor created successfully")
else:
    print("✗ Failed to create Air Quality Sensor")

# Test 3: Create Air Quality Observation
print("\n3. Creating Air Quality Observation...")
aq_observation = create_air_quality_observed_entity(
    observation_id="test-obs-1",
    latitude=21.0285,
    longitude=105.8542,
    aqi=85,
    pm25=28.5,
    pm10=45.2,
    date_observed=datetime.now()
)

success = client.create_entity(aq_observation)
if success:
    print("✓ Air Quality Observation created successfully")
else:
    print("✗ Failed to create Air Quality Observation")

# Test 4: Query entities
print("\n4. Querying all entities...")
entities = client.query_entities(limit=10)
print(f"Found {len(entities)} entities:")
for entity in entities:
    print(f"  - {entity.get('type')}: {entity.get('id')}")

print("\nOrion-LD connection test completed!")
