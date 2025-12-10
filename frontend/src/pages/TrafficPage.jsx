import { useState, useEffect } from 'react';
import api from '../api';

// Congestion level colors
const CONGESTION_COLORS = {
  free: 'bg-green-100 text-green-800',
  light: 'bg-yellow-100 text-yellow-800',
  moderate: 'bg-orange-100 text-orange-800',
  heavy: 'bg-red-100 text-red-800',
  severe: 'bg-purple-100 text-purple-800'
};

const CONGESTION_LABELS = {
  free: 'Thông thoáng',
  light: 'Nhẹ',
  moderate: 'Trung bình',
  heavy: 'Đông đúc',
  severe: 'Kẹt xe'
};

const INCIDENT_TYPES = {
  accident: { icon: '🚗💥', label: 'Tai nạn', color: 'bg-red-100 text-red-800' },
  roadwork: { icon: '🚧', label: 'Thi công', color: 'bg-yellow-100 text-yellow-800' },
  congestion: { icon: '🚦', label: 'Ùn tắc', color: 'bg-orange-100 text-orange-800' },
  weather: { icon: '🌧️', label: 'Thời tiết', color: 'bg-blue-100 text-blue-800' },
  other: { icon: '⚠️', label: 'Khác', color: 'bg-gray-100 text-gray-800' }
};

const SEVERITY_COLORS = {
  low: 'border-l-green-500',
  medium: 'border-l-yellow-500',
  high: 'border-l-orange-500',
  critical: 'border-l-red-500'
};

export default function TrafficPage() {
  const [activeTab, setActiveTab] = useState('bus-stations');
  const [busStations, setBusStations] = useState([]);
  const [trafficFlows, setTrafficFlows] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [parkingSpots, setParkingSpots] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCity, setSelectedCity] = useState('all');

  const cities = [
    { value: 'all', label: 'Tất cả thành phố' },
    { value: 'Ho Chi Minh', label: 'TP. Hồ Chí Minh' },
    { value: 'Ha Noi', label: 'Hà Nội' },
    { value: 'Da Nang', label: 'Đà Nẵng' },
    { value: 'Can Tho', label: 'Cần Thơ' },
    { value: 'Hai Phong', label: 'Hải Phòng' }
  ];

  useEffect(() => {
    fetchData();
  }, [selectedCity]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const cityParam = selectedCity !== 'all' ? `?city=${selectedCity}` : '';
      
      const [busRes, flowRes, incidentRes, parkingRes, statsRes] = await Promise.all([
        api.get(`/traffic/bus-stations/${cityParam}`),
        api.get(`/traffic/traffic-flows/${cityParam}`),
        api.get(`/traffic/incidents/${cityParam}`),
        api.get(`/traffic/parking/${cityParam}`),
        api.get('/traffic/summary/')
      ]);

      setBusStations(busRes.data.results || busRes.data);
      setTrafficFlows(flowRes.data.results || flowRes.data);
      setIncidents(incidentRes.data.results || incidentRes.data);
      setParkingSpots(parkingRes.data.results || parkingRes.data);
      setStatistics(statsRes.data);
    } catch (err) {
      console.error('Error fetching traffic data:', err);
      setError('Không thể tải dữ liệu giao thông');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'bus-stations', label: '🚌 Bến xe', count: busStations.length },
    { id: 'traffic-flow', label: '🚗 Lưu lượng', count: trafficFlows.length },
    { id: 'incidents', label: '⚠️ Sự cố', count: incidents.filter(i => i.status === 'active').length },
    { id: 'parking', label: '🅿️ Đỗ xe', count: parkingSpots.length }
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">🚦 Giao thông</h1>
          <p className="text-gray-600 mt-1">Quản lý bến xe, lưu lượng giao thông và bãi đỗ xe</p>
        </div>
        <div className="flex items-center gap-4">
          <select
            value={selectedCity}
            onChange={(e) => setSelectedCity(e.target.value)}
            className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            {cities.map(city => (
              <option key={city.value} value={city.value}>{city.label}</option>
            ))}
          </select>
          <button
            onClick={fetchData}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            🔄 Làm mới
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {/* Statistics Cards */}
      {statistics && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-xl shadow-lg p-4">
            <div className="text-3xl mb-2">🚌</div>
            <div className="text-2xl font-bold text-gray-900">{statistics.total_bus_stations || busStations.length}</div>
            <div className="text-sm text-gray-500">Bến xe/Trạm</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-4">
            <div className="text-3xl mb-2">🚗</div>
            <div className="text-2xl font-bold text-gray-900">{statistics.total_traffic_flows || trafficFlows.length}</div>
            <div className="text-sm text-gray-500">Điểm đo lưu lượng</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-4">
            <div className="text-3xl mb-2">⚠️</div>
            <div className="text-2xl font-bold text-red-600">{statistics.active_incidents || incidents.filter(i => i.status === 'active').length}</div>
            <div className="text-sm text-gray-500">Sự cố đang xảy ra</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-4">
            <div className="text-3xl mb-2">🅿️</div>
            <div className="text-2xl font-bold text-green-600">
              {parkingSpots.reduce((sum, p) => sum + (p.available_spaces || 0), 0)}
            </div>
            <div className="text-sm text-gray-500">Chỗ đỗ trống</div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-4 py-4 text-center font-medium ${
                  activeTab === tab.id
                    ? 'border-b-2 border-primary-500 text-primary-600 bg-primary-50'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                {tab.label}
                <span className={`ml-2 px-2 py-0.5 text-xs rounded-full ${
                  activeTab === tab.id ? 'bg-primary-100' : 'bg-gray-100'
                }`}>
                  {tab.count}
                </span>
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {/* Bus Stations Tab */}
          {activeTab === 'bus-stations' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Danh sách bến xe và trạm</h3>
              {busStations.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Không có dữ liệu bến xe</p>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {busStations.map(station => (
                    <div key={station.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="font-semibold text-gray-900">{station.name}</h4>
                          <p className="text-sm text-gray-500">{station.city}</p>
                        </div>
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          station.status === 'operational' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                        }`}>
                          {station.status === 'operational' ? 'Hoạt động' : station.status}
                        </span>
                      </div>
                      <div className="mt-3 space-y-1 text-sm">
                        <p><span className="text-gray-500">Loại:</span> {
                          station.station_type === 'bus_terminal' ? '🚌 Bến xe buýt' :
                          station.station_type === 'bus_stop' ? '🚏 Trạm xe buýt' :
                          station.station_type === 'metro_station' ? '🚇 Ga metro' : station.station_type
                        }</p>
                        {station.routes && station.routes.length > 0 && (
                          <p><span className="text-gray-500">Tuyến:</span> {station.routes.join(', ')}</p>
                        )}
                        <div className="flex gap-2 mt-2">
                          {station.has_shelter && <span title="Có mái che">🏠</span>}
                          {station.wheelchair_accessible && <span title="Tiếp cận xe lăn">♿</span>}
                          {station.has_real_time_info && <span title="Thông tin thời gian thực">📺</span>}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Traffic Flow Tab */}
          {activeTab === 'traffic-flow' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Tình trạng lưu lượng giao thông</h3>
              {trafficFlows.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Không có dữ liệu lưu lượng</p>
              ) : (
                <div className="space-y-3">
                  {trafficFlows.map(flow => (
                    <div key={flow.id} className="border rounded-lg p-4 flex items-center justify-between">
                      <div className="flex-1">
                        <h4 className="font-semibold text-gray-900">{flow.road_name}</h4>
                        <p className="text-sm text-gray-500">{flow.city}</p>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-center">
                          <div className="text-lg font-bold">{flow.average_speed?.toFixed(0) || '--'}</div>
                          <div className="text-xs text-gray-500">km/h</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold">{flow.vehicle_count || '--'}</div>
                          <div className="text-xs text-gray-500">xe/giờ</div>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${CONGESTION_COLORS[flow.congestion_level] || 'bg-gray-100'}`}>
                          {CONGESTION_LABELS[flow.congestion_level] || flow.congestion_level}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Incidents Tab */}
          {activeTab === 'incidents' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Sự cố giao thông</h3>
              {incidents.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Không có sự cố</p>
              ) : (
                <div className="space-y-3">
                  {incidents.map(incident => {
                    const incidentType = INCIDENT_TYPES[incident.incident_type] || INCIDENT_TYPES.other;
                    return (
                      <div 
                        key={incident.id} 
                        className={`border-l-4 ${SEVERITY_COLORS[incident.severity] || 'border-l-gray-500'} bg-white rounded-lg p-4 shadow-sm`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex items-start gap-3">
                            <span className="text-2xl">{incidentType.icon}</span>
                            <div>
                              <h4 className="font-semibold text-gray-900">{incident.title}</h4>
                              <p className="text-sm text-gray-600">{incident.description}</p>
                              <p className="text-xs text-gray-400 mt-1">{incident.city} • {new Date(incident.created_at).toLocaleString('vi-VN')}</p>
                            </div>
                          </div>
                          <div className="flex flex-col items-end gap-2">
                            <span className={`px-2 py-1 text-xs rounded-full ${incidentType.color}`}>
                              {incidentType.label}
                            </span>
                            <span className={`px-2 py-1 text-xs rounded-full ${
                              incident.status === 'active' ? 'bg-red-100 text-red-800' :
                              incident.status === 'resolved' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                            }`}>
                              {incident.status === 'active' ? 'Đang xảy ra' :
                               incident.status === 'resolved' ? 'Đã xử lý' : incident.status}
                            </span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* Parking Tab */}
          {activeTab === 'parking' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Bãi đỗ xe</h3>
              {parkingSpots.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Không có dữ liệu bãi đỗ xe</p>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {parkingSpots.map(parking => {
                    const availablePercent = parking.total_spaces > 0 
                      ? (parking.available_spaces / parking.total_spaces) * 100 
                      : 0;
                    return (
                      <div key={parking.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <h4 className="font-semibold text-gray-900">{parking.name}</h4>
                            <p className="text-sm text-gray-500">{parking.city}</p>
                          </div>
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            parking.status === 'open' ? 'bg-green-100 text-green-800' :
                            parking.status === 'full' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                          }`}>
                            {parking.status === 'open' ? 'Mở cửa' :
                             parking.status === 'full' ? 'Đầy' :
                             parking.status === 'closed' ? 'Đóng' : parking.status}
                          </span>
                        </div>
                        
                        {/* Availability bar */}
                        <div className="mb-3">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-600">Chỗ trống</span>
                            <span className="font-semibold">
                              {parking.available_spaces} / {parking.total_spaces}
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                availablePercent > 50 ? 'bg-green-500' :
                                availablePercent > 20 ? 'bg-yellow-500' : 'bg-red-500'
                              }`}
                              style={{ width: `${availablePercent}%` }}
                            ></div>
                          </div>
                        </div>

                        <div className="space-y-1 text-sm">
                          <p><span className="text-gray-500">Loại:</span> {
                            parking.parking_type === 'public' ? 'Công cộng' :
                            parking.parking_type === 'private' ? 'Tư nhân' :
                            parking.parking_type === 'street' ? 'Ven đường' : parking.parking_type
                          }</p>
                          {parking.price_per_hour && (
                            <p><span className="text-gray-500">Giá:</span> {parking.price_per_hour.toLocaleString('vi-VN')}đ/giờ</p>
                          )}
                          <div className="flex gap-2 mt-2">
                            {parking.is_24h && <span title="24/7">🕐</span>}
                            {parking.has_security && <span title="Có bảo vệ">🛡️</span>}
                            {parking.has_cctv && <span title="Camera">📷</span>}
                            {parking.has_ev_charging && <span title="Sạc điện">⚡</span>}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
