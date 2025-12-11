/**
 * NGSI-LD Parser Utilities
 * Converts NGSI-LD format to flat objects for easier frontend use
 */

/**
 * Extract value from NGSI-LD Property
 * @param {Object} property - NGSI-LD property object
 * @returns {*} - Extracted value
 */
export const getValue = (property) => {
  if (!property) return null;
  if (typeof property === 'object' && property.value !== undefined) {
    return property.value;
  }
  return property;
};

/**
 * Extract coordinates from GeoProperty
 * @param {Object} location - NGSI-LD GeoProperty
 * @returns {Object} - {latitude, longitude}
 */
export const getLocation = (location) => {
  if (!location || !location.value) return { latitude: 0, longitude: 0 };
  const coords = location.value.coordinates || [0, 0];
  return {
    longitude: coords[0],
    latitude: coords[1]
  };
};

/**
 * Extract address string from NGSI-LD address property
 * @param {Object} address - NGSI-LD address property
 * @returns {string}
 */
export const getAddress = (address) => {
  if (!address || !address.value) return '';
  const addr = address.value;
  const parts = [addr.streetAddress, addr.addressLocality, addr.addressCountry].filter(Boolean);
  return parts.join(', ');
};

/**
 * Parse Bus Station from NGSI-LD format
 */
export const parseBusStation = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  name: getValue(entity.name),
  station_type: getValue(entity.stationType),
  status: getValue(entity.status),
  routes: getValue(entity.refRoutes) || [],
  ...getLocation(entity.location),
  address: getAddress(entity.address),
  city: entity.address?.value?.addressLocality || '',
  has_shelter: entity.accessibilityFeatures?.value?.hasShelter || false,
  has_bench: entity.accessibilityFeatures?.value?.hasBench || false,
  wheelchair_accessible: entity.accessibilityFeatures?.value?.wheelchairAccessible || false,
  has_real_time_info: entity.accessibilityFeatures?.value?.hasRealTimeInfo || false,
  type: entity.type
});

/**
 * Parse Traffic Flow from NGSI-LD format
 */
export const parseTrafficFlow = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  name: getValue(entity.name),
  road_name: entity.address?.value?.streetAddress || getValue(entity.name) || '',
  city: entity.address?.value?.addressLocality || '',
  vehicle_count: getValue(entity.intensity),
  average_speed: getValue(entity.averageVehicleSpeed),
  congestion_level: getValue(entity.congestionLevel),
  occupancy: getValue(entity.occupancy),
  observed_at: getValue(entity.dateObserved),
  ...getLocation(entity.location),
  type: entity.type
});

/**
 * Parse Traffic Incident from NGSI-LD format
 */
export const parseTrafficIncident = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  incident_type: getValue(entity.incidentType),
  title: getValue(entity.title),
  description: getValue(entity.description),
  severity: getValue(entity.severity),
  status: getValue(entity.status),
  address: entity.address?.value?.streetAddress || '',
  city: entity.address?.value?.addressLocality || '',
  reported_at: getValue(entity.reportedAt),
  resolved_at: getValue(entity.resolvedAt),
  ...getLocation(entity.location),
  type: entity.type
});

/**
 * Parse Parking Spot from NGSI-LD format
 */
export const parseParkingSpot = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  name: getValue(entity.name),
  total_spaces: getValue(entity.totalSpotNumber),
  available_spaces: getValue(entity.availableSpotNumber),
  occupancy_rate: getValue(entity.occupancyRate),
  parking_type: getValue(entity.parkingType),
  price_per_hour: getValue(entity.pricePerHour),
  status: getValue(entity.status),
  opening_hours: getValue(entity.openingHours),
  ...getLocation(entity.location),
  address: getAddress(entity.address),
  city: entity.address?.value?.addressLocality || '',
  type: entity.type
});

/**
 * Parse Water Supply Point from NGSI-LD format
 */
export const parseWaterSupply = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  name: getValue(entity.name),
  point_type: getValue(entity.waterType),
  capacity: getValue(entity.capacity),
  current_level: getValue(entity.currentLevel),
  fill_percentage: getValue(entity.fillPercentage),
  flow_rate: getValue(entity.flowRate),
  pressure: getValue(entity.pressure),
  ph_level: entity.waterQuality?.value?.phLevel,
  chlorine_level: entity.waterQuality?.value?.chlorineLevel,
  turbidity: entity.waterQuality?.value?.turbidity,
  status: getValue(entity.status),
  ...getLocation(entity.location),
  address: getAddress(entity.address),
  city: entity.address?.value?.addressLocality || '',
  type: entity.type
});

/**
 * Parse Drainage Point from NGSI-LD format
 */
export const parseDrainage = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  name: getValue(entity.name),
  point_type: getValue(entity.drainageType),
  capacity: getValue(entity.capacity),
  current_level: getValue(entity.currentLevel),
  flow_rate: getValue(entity.flowRate),
  status: getValue(entity.status),
  flood_risk: getValue(entity.floodRisk),
  ...getLocation(entity.location),
  address: getAddress(entity.address),
  city: entity.address?.value?.addressLocality || '',
  type: entity.type
});

/**
 * Parse Street Light from NGSI-LD format
 */
export const parseStreetLight = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  name: getValue(entity.name),
  pole_id: getValue(entity.poleId),
  lamp_type: getValue(entity.lampType),
  power_rating: getValue(entity.powerConsumption),
  brightness_level: getValue(entity.illuminanceLevel),
  is_smart: getValue(entity.isAutomatic),
  status: getValue(entity.status),
  energy_consumed_today: getValue(entity.energyConsumedToday),
  has_motion_sensor: entity.features?.value?.hasMotionSensor || false,
  has_light_sensor: entity.features?.value?.hasLightSensor || false,
  has_camera: entity.features?.value?.hasCamera || false,
  ...getLocation(entity.location),
  address: getAddress(entity.address),
  city: entity.address?.value?.addressLocality || '',
  type: entity.type
});

/**
 * Parse Energy Meter from NGSI-LD format
 */
export const parseEnergyMeter = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  name: getValue(entity.name),
  meter_type: getValue(entity.meterType),
  current_power: getValue(entity.currentPower),
  voltage: getValue(entity.voltage),
  current: getValue(entity.current),
  power_factor: getValue(entity.powerFactor),
  frequency: getValue(entity.frequency),
  today_consumption: getValue(entity.totalEnergyConsumed),
  month_consumption: getValue(entity.monthConsumption),
  status: getValue(entity.status),
  ...getLocation(entity.location),
  address: getAddress(entity.address),
  city: entity.address?.value?.addressLocality || '',
  type: entity.type
});

/**
 * Parse Telecom Tower from NGSI-LD format
 */
export const parseTelecomTower = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  name: getValue(entity.name),
  tower_type: getValue(entity.towerType),
  provider: getValue(entity.operator),
  technologies: getValue(entity.supportedTechnologies) || [],
  frequency_bands: getValue(entity.frequencyBands) || [],
  height: getValue(entity.height),
  coverage_radius: getValue(entity.coverageRadius),
  max_connections: getValue(entity.maxConnections),
  active_connections: getValue(entity.activeConnections),
  utilization_rate: getValue(entity.utilizationRate),
  signal_strength: getValue(entity.signalStrength),
  status: getValue(entity.status),
  ...getLocation(entity.location),
  address: getAddress(entity.address),
  city: entity.address?.value?.addressLocality || '',
  type: entity.type
});

/**
 * Parse Public Service from NGSI-LD format
 */
export const parsePublicService = (entity) => ({
  id: entity.id,
  entity_id: entity.id,
  name: getValue(entity.name),
  service_type: getValue(entity.serviceType),
  service_type_display: getValue(entity.category),
  description: getValue(entity.description),
  is_active: getValue(entity.isActive),
  opening_hours: getValue(entity.openingHours),
  contact_phone: entity.contactPoint?.value?.telephone || '',
  website: getValue(entity.url),
  ...getLocation(entity.location),
  address: getAddress(entity.address),
  type: entity.type
});

/**
 * Parse Weather Observation from NGSI-LD format
 */
export const parseWeatherObservation = (entity) => ({
  id: entity.id,
  observation_id: entity.id,
  location_name: getValue(entity.name),
  temperature: getValue(entity.temperature),
  humidity: getValue(entity.relativeHumidity),
  pressure: getValue(entity.atmosphericPressure),
  wind_speed: getValue(entity.windSpeed),
  wind_direction: getValue(entity.windDirection),
  precipitation: getValue(entity.precipitation),
  weather_description: getValue(entity.weatherType),
  observed_at: getValue(entity.dateObserved),
  source: getValue(entity.source),
  ...getLocation(entity.location),
  type: entity.type
});

/**
 * Parse Air Quality Observation from NGSI-LD format
 */
export const parseAirQualityObservation = (entity) => ({
  id: entity.id,
  observation_id: entity.id,
  location_name: getValue(entity.name),
  aqi: getValue(entity.airQualityIndex),
  aqi_level: getValue(entity.airQualityLevel),
  pm25: getValue(entity.pm25),
  pm10: getValue(entity.pm10),
  no2: getValue(entity.no2),
  o3: getValue(entity.o3),
  co: getValue(entity.co),
  so2: getValue(entity.so2),
  observed_at: getValue(entity.dateObserved),
  source: getValue(entity.source),
  ...getLocation(entity.location),
  type: entity.type
});

export default {
  getValue,
  getLocation,
  getAddress,
  parseBusStation,
  parseTrafficFlow,
  parseTrafficIncident,
  parseParkingSpot,
  parseWaterSupply,
  parseDrainage,
  parseStreetLight,
  parseEnergyMeter,
  parseTelecomTower,
  parsePublicService,
  parseWeatherObservation,
  parseAirQualityObservation
};
