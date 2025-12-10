import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { 
  weatherStationAPI, 
  airQualityAPI, 
  publicServiceAPI 
} from '../api';
import api from '../api';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const API_URL = 'http://localhost:8000/api/v1';

export default function MapPage() {
  const [weatherStations, setWeatherStations] = useState([]);
  const [airQualitySensors, setAirQualitySensors] = useState([]);
  const [publicServices, setPublicServices] = useState([]);
  const [userDevices, setUserDevices] = useState([]);
  const [busStations, setBusStations] = useState([]);
  const [parkingSpots, setParkingSpots] = useState([]);
  const [trafficFlows, setTrafficFlows] = useState([]);
  const [streetLights, setStreetLights] = useState([]);
  const [telecomTowers, setTelecomTowers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [layers, setLayers] = useState({
    weather: true,
    airQuality: true,
    services: true,
    userDevices: true,
    busStations: true,
    parking: true,
    trafficFlow: false,
    streetLights: false,
    telecom: false,
  });
  const [showUnverified, setShowUnverified] = useState(true);

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

      // Load traffic data
      try {
        const [busRes, parkingRes, flowRes] = await Promise.all([
          api.get('/api/v1/traffic/bus-stations/'),
          api.get('/api/v1/traffic/parking/'),
          api.get('/api/v1/traffic/traffic-flows/'),
        ]);
        setBusStations(busRes.data.results || busRes.data || []);
        setParkingSpots(parkingRes.data.results || parkingRes.data || []);
        setTrafficFlows(flowRes.data.results || flowRes.data || []);
      } catch (err) {
        console.error('Failed to load traffic data:', err);
      }

      // Load infrastructure data
      try {
        const [lightsRes, telecomRes] = await Promise.all([
          api.get('/api/v1/infrastructure/street-lights/'),
          api.get('/api/v1/infrastructure/telecom/'),
        ]);
        setStreetLights(lightsRes.data.results || lightsRes.data || []);
        setTelecomTowers(telecomRes.data.results || telecomRes.data || []);
      } catch (err) {
        console.error('Failed to load infrastructure data:', err);
      }

      // Load public user devices
      try {
        const devicesRes = await fetch(`${API_URL}/auth/public-devices/`);
        if (devicesRes.ok) {
          const devicesData = await devicesRes.json();
          console.log('Public devices:', devicesData);
          setUserDevices(devicesData.results || devicesData || []);
        }
      } catch (err) {
        console.error('Failed to load user devices:', err);
      }
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
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={layers.userDevices}
              onChange={() => toggleLayer('userDevices')}
              className="rounded text-primary-600 mr-2"
            />
            <span className="text-sm">📡 Thiết bị người dùng ({userDevices.length})</span>
          </label>
        </div>
        
        {/* Traffic & Infrastructure Layers */}
        <div className="flex flex-wrap gap-4 mt-3 pt-3 border-t border-gray-200">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={layers.busStations}
              onChange={() => toggleLayer('busStations')}
              className="rounded text-red-600 mr-2"
            />
            <span className="text-sm">🚌 Bến xe/Trạm ({busStations.length})</span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={layers.parking}
              onChange={() => toggleLayer('parking')}
              className="rounded text-cyan-600 mr-2"
            />
            <span className="text-sm">🅿️ Bãi đỗ xe ({parkingSpots.length})</span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={layers.trafficFlow}
              onChange={() => toggleLayer('trafficFlow')}
              className="rounded text-orange-600 mr-2"
            />
            <span className="text-sm">🚗 Lưu lượng GT ({trafficFlows.length})</span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={layers.streetLights}
              onChange={() => toggleLayer('streetLights')}
              className="rounded text-yellow-600 mr-2"
            />
            <span className="text-sm">💡 Đèn đường ({streetLights.length})</span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={layers.telecom}
              onChange={() => toggleLayer('telecom')}
              className="rounded text-pink-600 mr-2"
            />
            <span className="text-sm">📡 Viễn thông ({telecomTowers.length})</span>
          </label>
        </div>
        
        {/* Verified Filter */}
        {layers.userDevices && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={showUnverified}
                onChange={(e) => setShowUnverified(e.target.checked)}
                className="rounded text-primary-600 mr-2"
              />
              <span className="text-sm">Hiển thị thiết bị chưa xác minh</span>
            </label>
          </div>
        )}
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

          {/* User Devices */}
          {layers.userDevices && userDevices
            .filter(device => showUnverified || device.is_verified)
            .map(device => (
            <Marker 
              key={`user-${device.id}`} 
              position={[device.latitude, device.longitude]}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-bold text-indigo-600">
                    {getDeviceIcon(device.device_type)} {device.name}
                  </h3>
                  {device.is_verified && (
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 mt-1">
                      ✓ Đã xác minh
                    </span>
                  )}
                  <p className="text-sm text-gray-600 mt-1">
                    <strong>Owner:</strong> {device.user_username}
                  </p>
                  {device.description && (
                    <p className="text-sm text-gray-600 mt-1">{device.description}</p>
                  )}
                  {device.address && (
                    <p className="text-xs text-gray-500 mt-1">📍 {device.address}</p>
                  )}
                  <p className="text-xs text-gray-500 mt-1">
                    {device.status === 'active' ? '✅ Hoạt động' : '❌ Không hoạt động'}
                  </p>
                </div>
              </Popup>
              <Circle
                center={[device.latitude, device.longitude]}
                radius={300}
                pathOptions={{ 
                  color: device.is_verified ? 'indigo' : 'orange', 
                  fillColor: device.is_verified ? 'indigo' : 'orange', 
                  fillOpacity: 0.1 
                }}
              />
            </Marker>
          ))}

          {/* Bus Stations */}
          {layers.busStations && busStations.map(station => (
            <Marker 
              key={`bus-${station.id}`} 
              position={[station.latitude, station.longitude]}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-bold text-red-600">🚌 {station.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{station.city}</p>
                  <p className="text-xs text-gray-500">
                    Loại: {station.station_type === 'bus_terminal' ? 'Bến xe' : 
                          station.station_type === 'metro_station' ? 'Ga metro' : 'Trạm xe buýt'}
                  </p>
                  {station.routes && station.routes.length > 0 && (
                    <p className="text-xs text-gray-500">Tuyến: {station.routes.join(', ')}</p>
                  )}
                  <div className="flex gap-1 mt-1">
                    {station.has_shelter && <span title="Có mái che">🏠</span>}
                    {station.wheelchair_accessible && <span title="Xe lăn">♿</span>}
                    {station.has_real_time_info && <span title="Thông tin thời gian thực">📺</span>}
                  </div>
                </div>
              </Popup>
              <Circle
                center={[station.latitude, station.longitude]}
                radius={200}
                pathOptions={{ color: 'red', fillColor: 'red', fillOpacity: 0.2 }}
              />
            </Marker>
          ))}

          {/* Parking Spots */}
          {layers.parking && parkingSpots.map(parking => (
            <Marker 
              key={`parking-${parking.id}`} 
              position={[parking.latitude, parking.longitude]}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-bold text-cyan-600">🅿️ {parking.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{parking.city}</p>
                  <p className="text-sm font-medium mt-1">
                    Trống: <span className={parking.available_spaces > 20 ? 'text-green-600' : 'text-red-600'}>
                      {parking.available_spaces}/{parking.total_spaces}
                    </span>
                  </p>
                  {parking.price_per_hour && (
                    <p className="text-xs text-gray-500">Giá: {parking.price_per_hour.toLocaleString()}đ/giờ</p>
                  )}
                  <span className={`inline-block mt-1 px-2 py-0.5 text-xs rounded ${
                    parking.status === 'open' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {parking.status === 'open' ? 'Mở cửa' : parking.status === 'full' ? 'Đầy' : 'Đóng'}
                  </span>
                </div>
              </Popup>
              <Circle
                center={[parking.latitude, parking.longitude]}
                radius={150}
                pathOptions={{ color: 'cyan', fillColor: 'cyan', fillOpacity: 0.2 }}
              />
            </Marker>
          ))}

          {/* Traffic Flow Points */}
          {layers.trafficFlow && trafficFlows.map(flow => {
            const congestionColor = {
              free: 'green',
              light: 'lime',
              moderate: 'yellow',
              heavy: 'orange',
              severe: 'red'
            }[flow.congestion_level] || 'gray';
            return (
              <Marker 
                key={`flow-${flow.id}`} 
                position={[flow.latitude, flow.longitude]}
              >
                <Popup>
                  <div className="p-2">
                    <h3 className="font-bold text-orange-600">🚗 {flow.road_name}</h3>
                    <p className="text-sm text-gray-600 mt-1">{flow.city}</p>
                    <p className="text-sm">Tốc độ TB: <strong>{flow.average_speed?.toFixed(0) || '--'} km/h</strong></p>
                    <span className={`inline-block mt-1 px-2 py-0.5 text-xs rounded bg-${congestionColor}-100 text-${congestionColor}-800`}>
                      {flow.congestion_level === 'free' ? 'Thông thoáng' :
                       flow.congestion_level === 'light' ? 'Nhẹ' :
                       flow.congestion_level === 'moderate' ? 'Trung bình' :
                       flow.congestion_level === 'heavy' ? 'Đông đúc' : 'Kẹt xe'}
                    </span>
                  </div>
                </Popup>
                <Circle
                  center={[flow.latitude, flow.longitude]}
                  radius={300}
                  pathOptions={{ color: congestionColor, fillColor: congestionColor, fillOpacity: 0.3 }}
                />
              </Marker>
            );
          })}

          {/* Street Lights */}
          {layers.streetLights && streetLights.map(light => (
            <Marker 
              key={`light-${light.id}`} 
              position={[light.latitude, light.longitude]}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-bold text-yellow-600">💡 {light.pole_id}</h3>
                  <p className="text-sm text-gray-600 mt-1">{light.city}</p>
                  <p className="text-xs">Loại: {light.lamp_type?.toUpperCase()}</p>
                  <p className="text-xs">Công suất: {light.power_rating}W</p>
                  <div className="flex gap-1 mt-1">
                    {light.is_smart && <span className="px-1 bg-blue-100 text-blue-800 text-xs rounded">IoT</span>}
                    {light.has_motion_sensor && <span title="Cảm biến chuyển động">👁️</span>}
                  </div>
                  <span className={`inline-block mt-1 px-2 py-0.5 text-xs rounded ${
                    light.status === 'on' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {light.status === 'on' ? 'Bật' : light.status === 'dimmed' ? 'Giảm sáng' : 'Tắt'}
                  </span>
                </div>
              </Popup>
            </Marker>
          ))}

          {/* Telecom Towers */}
          {layers.telecom && telecomTowers.map(tower => (
            <Marker 
              key={`telecom-${tower.id}`} 
              position={[tower.latitude, tower.longitude]}
            >
              <Popup>
                <div className="p-2">
                  <h3 className="font-bold text-pink-600">📡 {tower.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{tower.city}</p>
                  <span className={`inline-block px-2 py-0.5 text-xs rounded ${
                    tower.provider === 'Viettel' ? 'bg-red-100 text-red-800' :
                    tower.provider === 'VNPT' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'
                  }`}>
                    {tower.provider}
                  </span>
                  {tower.technologies && tower.technologies.map(tech => (
                    <span key={tech} className="ml-1 px-1 bg-purple-100 text-purple-800 text-xs rounded">{tech}</span>
                  ))}
                  <p className="text-xs mt-1">Kết nối: {tower.active_connections}/{tower.max_connections}</p>
                  <p className="text-xs">Phủ sóng: {tower.coverage_radius}m</p>
                </div>
              </Popup>
              <Circle
                center={[tower.latitude, tower.longitude]}
                radius={tower.coverage_radius || 500}
                pathOptions={{ color: 'pink', fillColor: 'pink', fillOpacity: 0.1 }}
              />
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Legend */}
      <div className="bg-white shadow rounded-lg p-4">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Chú thích</h3>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-4 text-sm">
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
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-indigo-500 mr-2"></div>
            <span>Thiết bị đã xác minh</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-red-500 mr-2"></div>
            <span>Bến xe/Trạm</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-cyan-500 mr-2"></div>
            <span>Bãi đỗ xe</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-orange-500 mr-2"></div>
            <span>Lưu lượng giao thông</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-yellow-500 mr-2"></div>
            <span>Đèn đường</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-pink-500 mr-2"></div>
            <span>Trạm viễn thông</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function getDeviceIcon(type) {
  const icons = {
    weather_station: '🌤️',
    air_quality_sensor: '💨',
    traffic_sensor: '🚦',
    custom: '📡'
  };
  return icons[type] || '📡';
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
