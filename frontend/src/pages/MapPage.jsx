import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { 
  weatherStationAPI, 
  airQualityAPI, 
  publicServiceAPI 
} from '../api';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export default function MapPage() {
  const [weatherStations, setWeatherStations] = useState([]);
  const [airQualitySensors, setAirQualitySensors] = useState([]);
  const [publicServices, setPublicServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [layers, setLayers] = useState({
    weather: true,
    airQuality: true,
    services: true,
  });

  const center = [21.0285, 105.8542]; // Hanoi

  useEffect(() => {
    loadMapData();
  }, []);

  const loadMapData = async () => {
    try {
      setLoading(true);
      const [weather, airQuality, services] = await Promise.all([
        weatherStationAPI.getAll(),
        airQualityAPI.getAll(),
        publicServiceAPI.getAll(),
      ]);

      setWeatherStations(weather.data.results || weather.data || []);
      setAirQualitySensors(airQuality.data.results || airQuality.data || []);
      setPublicServices(services.data.results || services.data || []);
    } catch (error) {
      console.error('Error loading map data:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleLayer = (layer) => {
    setLayers(prev => ({ ...prev, [layer]: !prev[layer] }));
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Bản đồ Thành phố</h1>
        <p className="mt-2 text-sm text-gray-600">
          Hiển thị các trạm quan trắc và dịch vụ công cộng
        </p>
      </div>

      {/* Layer Controls */}
      <div className="bg-white shadow rounded-lg p-4">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Lớp hiển thị</h3>
        <div className="flex flex-wrap gap-4">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={layers.weather}
              onChange={() => toggleLayer('weather')}
              className="rounded text-primary-600 mr-2"
            />
            <span className="text-sm">🌤️ Trạm thời tiết ({weatherStations.length})</span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={layers.airQuality}
              onChange={() => toggleLayer('airQuality')}
              className="rounded text-primary-600 mr-2"
            />
            <span className="text-sm">🌫️ Cảm biến chất lượng KK ({airQualitySensors.length})</span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={layers.services}
              onChange={() => toggleLayer('services')}
              className="rounded text-primary-600 mr-2"
            />
            <span className="text-sm">🏛️ Dịch vụ công cộng ({publicServices.length})</span>
          </label>
        </div>
      </div>

      {/* Map */}
      <div className="bg-white shadow rounded-lg overflow-hidden" style={{ height: '600px' }}>
        <MapContainer center={center} zoom={12} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Weather Stations */}
          {layers.weather && weatherStations.map(station => (
            <Marker 
              key={station.id} 
              position={[station.latitude, station.longitude]}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-bold text-blue-600">🌤️ {station.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{station.address}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {station.is_active ? '✅ Hoạt động' : '❌ Không hoạt động'}
                  </p>
                </div>
              </Popup>
              <Circle
                center={[station.latitude, station.longitude]}
                radius={500}
                pathOptions={{ color: 'blue', fillColor: 'blue', fillOpacity: 0.1 }}
              />
            </Marker>
          ))}

          {/* Air Quality Sensors */}
          {layers.airQuality && airQualitySensors.map(sensor => (
            <Marker 
              key={sensor.id} 
              position={[sensor.latitude, sensor.longitude]}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-bold text-purple-600">🌫️ {sensor.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{sensor.address}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {sensor.is_active ? '✅ Hoạt động' : '❌ Không hoạt động'}
                  </p>
                </div>
              </Popup>
              <Circle
                center={[sensor.latitude, sensor.longitude]}
                radius={500}
                pathOptions={{ color: 'purple', fillColor: 'purple', fillOpacity: 0.1 }}
              />
            </Marker>
          ))}

          {/* Public Services */}
          {layers.services && publicServices.map(service => (
            <Marker 
              key={service.id} 
              position={[service.latitude, service.longitude]}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-bold text-green-600">
                    {getServiceIcon(service.service_type)} {service.name}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">{service.service_type_display}</p>
                  {service.address && (
                    <p className="text-sm text-gray-600">{service.address}</p>
                  )}
                  {service.opening_hours && (
                    <p className="text-xs text-gray-500 mt-1">🕐 {service.opening_hours}</p>
                  )}
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Legend */}
      <div className="bg-white shadow rounded-lg p-4">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Chú thích</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-blue-500 mr-2"></div>
            <span>Trạm thời tiết</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-purple-500 mr-2"></div>
            <span>Cảm biến chất lượng KK</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-green-500 mr-2"></div>
            <span>Dịch vụ công cộng</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function getServiceIcon(type) {
  const icons = {
    park: '🏞️',
    parking: '🅿️',
    bus_stop: '🚌',
    hospital: '🏥',
    school: '🏫',
    library: '📚',
    other: '📍',
  };
  return icons[type] || '📍';
}
