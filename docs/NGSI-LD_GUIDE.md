# NGSI-LD và Smart Data Models

## Tổng quan về NGSI-LD

NGSI-LD (Next Generation Service Interface - Linked Data) là API tiêu chuẩn do ETSI ISG CIM phát triển cho IoT và Smart Cities. 

### Đặc điểm chính:
- Dựa trên JSON-LD
- Hỗ trợ Linked Data và Semantic Web
- Tương thích với FIWARE platform
- Hỗ trợ temporal và geospatial queries

## NGSI-LD Entity Structure

### Basic Entity

```json
{
  "id": "urn:ngsi-ld:WeatherStation:hanoi-1",
  "type": "WeatherStation",
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
  ],
  "name": {
    "type": "Property",
    "value": "Hanoi Weather Station"
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [105.8542, 21.0285]
    }
  },
  "temperature": {
    "type": "Property",
    "value": 28.5,
    "unitCode": "CEL",
    "observedAt": "2024-11-24T10:00:00Z"
  },
  "refDevice": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Device:sensor-001"
  }
}
```

### Entity Components

1. **id**: Unique identifier (URI format)
   - Format: `urn:ngsi-ld:{Type}:{id}`
   - Example: `urn:ngsi-ld:WeatherStation:hanoi-1`

2. **type**: Entity type
   - Describes what kind of entity this is
   - Should follow Smart Data Models when possible

3. **@context**: JSON-LD context
   - Defines vocabulary and namespaces
   - Can be array of contexts

4. **Properties**: Attributes with values
   ```json
   "temperature": {
     "type": "Property",
     "value": 28.5,
     "unitCode": "CEL",
     "observedAt": "2024-11-24T10:00:00Z"
   }
   ```

5. **Relationships**: Links to other entities
   ```json
   "refDevice": {
     "type": "Relationship",
     "object": "urn:ngsi-ld:Device:sensor-001"
   }
   ```

6. **GeoProperties**: Geographic locations
   ```json
   "location": {
     "type": "GeoProperty",
     "value": {
       "type": "Point",
       "coordinates": [105.8542, 21.0285]
     }
   }
   ```

## SOSA/SSN Ontology

SOSA (Sensor, Observation, Sample, and Actuator) và SSN (Semantic Sensor Network) là ontology của W3C cho IoT.

### Core Concepts

```
Platform (nơi đặt sensor)
  ↓ hosts
Sensor (thiết bị đo)
  ↓ observes
ObservableProperty (thuộc tính được đo)
  ↓ isObservedBy
Observation (kết quả đo)
```

### Example: Temperature Sensor

```json
{
  "id": "urn:ngsi-ld:Sensor:temp-001",
  "type": "Sensor",
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    {
      "sosa": "http://www.w3.org/ns/sosa/"
    }
  ],
  "observes": {
    "type": "Relationship",
    "object": "sosa:Temperature"
  },
  "isHostedBy": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Platform:station-001"
  }
}
```

### Example: Observation

```json
{
  "id": "urn:ngsi-ld:Observation:obs-001",
  "type": "Observation",
  "@context": [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    {
      "sosa": "http://www.w3.org/ns/sosa/"
    }
  ],
  "madeBySensor": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:Sensor:temp-001"
  },
  "observedProperty": {
    "type": "Relationship",
    "object": "sosa:Temperature"
  },
  "hasSimpleResult": {
    "type": "Property",
    "value": 28.5
  },
  "resultTime": {
    "type": "Property",
    "value": "2024-11-24T10:00:00Z"
  }
}
```

## Smart Data Models

Smart Data Models là tập hợp các data models chuẩn cho Smart Cities do FIWARE cung cấp.

### Environment Domain

#### WeatherObserved
```json
{
  "id": "urn:ngsi-ld:WeatherObserved:Spain-WeatherObserved-Valladolid-2016-11-30T07:00:00.00Z",
  "type": "WeatherObserved",
  "dateObserved": {
    "type": "Property",
    "value": "2016-11-30T07:00:00.00Z"
  },
  "temperature": {
    "type": "Property",
    "value": 3.3,
    "unitCode": "CEL"
  },
  "relativeHumidity": {
    "type": "Property",
    "value": 1.0,
    "unitCode": "P1"
  },
  "atmosphericPressure": {
    "type": "Property",
    "value": 938.9,
    "unitCode": "A97"
  }
}
```

#### AirQualityObserved
```json
{
  "id": "urn:ngsi-ld:AirQualityObserved:Madrid-AmbientObserved-28079004-2016-03-15T11:00:00",
  "type": "AirQualityObserved",
  "dateObserved": {
    "type": "Property",
    "value": "2016-03-15T11:00:00/2016-03-15T12:00:00"
  },
  "airQualityIndex": {
    "type": "Property",
    "value": 65
  },
  "pm25": {
    "type": "Property",
    "value": 25,
    "unitCode": "GQ"
  },
  "pm10": {
    "type": "Property",
    "value": 40,
    "unitCode": "GQ"
  },
  "no2": {
    "type": "Property",
    "value": 22,
    "unitCode": "GQ"
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [-3.712247222222222, 40.423852777777775]
    }
  }
}
```

### Transport Domain

#### TrafficFlowObserved
```json
{
  "id": "urn:ngsi-ld:TrafficFlowObserved:TrafficFlowObserved-Valladolid-osm-60821110",
  "type": "TrafficFlowObserved",
  "laneId": {
    "type": "Property",
    "value": 1
  },
  "dateObserved": {
    "type": "Property",
    "value": "2016-12-07T11:10:00/2016-12-07T11:15:00"
  },
  "averageVehicleSpeed": {
    "type": "Property",
    "value": 52.6,
    "unitCode": "KMH"
  },
  "intensity": {
    "type": "Property",
    "value": 197
  },
  "occupancy": {
    "type": "Property",
    "value": 0.76,
    "unitCode": "P1"
  },
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "LineString",
      "coordinates": [
        [-4.73735395519672, 41.6538181849672],
        [-4.73414858659993, 41.6600594193478]
      ]
    }
  }
}
```

## Custom Context Definition

Trong project này, chúng ta định nghĩa custom context:

```json
{
  "@context": {
    "sosa": "http://www.w3.org/ns/sosa/",
    "ssn": "http://www.w3.org/ns/ssn/",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "schema": "https://schema.org/",
    "smartcity": "https://smartcity.example.com/ontology#",
    
    "temperature": "smartcity:temperature",
    "humidity": "smartcity:humidity",
    "airQualityIndex": "smartcity:airQualityIndex",
    "pm25": "smartcity:pm25",
    
    "observes": "sosa:observes",
    "madeBySensor": "sosa:madeBySensor",
    "hasSimpleResult": "sosa:hasSimpleResult",
    "resultTime": "sosa:resultTime"
  }
}
```

## Best Practices

### 1. Entity IDs
- Luôn sử dụng URN format
- Format: `urn:ngsi-ld:{Type}:{uniqueId}`
- Unique ID nên có ý nghĩa và dễ đọc

### 2. Context
- Sử dụng standard contexts khi có thể
- Thêm custom context khi cần thiết
- Context nên được host ở URL stable

### 3. Properties
- Sử dụng unitCode cho các đơn vị đo
- Thêm observedAt cho temporal data
- Sử dụng metadata khi cần thiết

### 4. Relationships
- Luôn sử dụng URN đầy đủ trong relationships
- Tránh circular relationships
- Document relationship semantics

### 5. GeoProperties
- Sử dụng GeoJSON format
- Coordinates theo format [longitude, latitude]
- Hỗ trợ Point, LineString, Polygon

## Tài liệu tham khảo

- [NGSI-LD Primer](https://www.etsi.org/deliver/etsi_gr/CIM/001_099/008/01.01.01_60/gr_CIM008v010101p.pdf)
- [SOSA/SSN Ontology](https://www.w3.org/TR/vocab-ssn/)
- [Smart Data Models](https://smartdatamodels.org/)
- [FIWARE Data Models](https://github.com/smart-data-models)
- [JSON-LD Specification](https://www.w3.org/TR/json-ld11/)
