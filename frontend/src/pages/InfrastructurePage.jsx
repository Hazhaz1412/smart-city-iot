import { useState, useEffect } from 'react';
import api from '../api';
import { parseWaterSupply, parseDrainage, parseStreetLight, parseEnergyMeter, parseTelecomTower } from '../utils/ngsiParser';

// Status colors
const STATUS_COLORS = {
  operational: 'bg-green-100 text-green-800',
  active: 'bg-green-100 text-green-800',
  on: 'bg-green-100 text-green-800',
  maintenance: 'bg-yellow-100 text-yellow-800',
  dimmed: 'bg-yellow-100 text-yellow-800',
  offline: 'bg-gray-100 text-gray-800',
  off: 'bg-gray-100 text-gray-800',
  fault: 'bg-red-100 text-red-800',
  error: 'bg-red-100 text-red-800'
};

const STATUS_LABELS = {
  operational: 'Hoạt động',
  active: 'Hoạt động',
  on: 'Bật',
  maintenance: 'Bảo trì',
  dimmed: 'Giảm sáng',
  offline: 'Ngoại tuyến',
  off: 'Tắt',
  fault: 'Lỗi',
  error: 'Lỗi'
};

export default function InfrastructurePage() {
  const [activeTab, setActiveTab] = useState('water');
  const [waterSupply, setWaterSupply] = useState([]);
  const [drainage, setDrainage] = useState([]);
  const [streetLights, setStreetLights] = useState([]);
  const [energyMeters, setEnergyMeters] = useState([]);
  const [telecomTowers, setTelecomTowers] = useState([]);
  const [summary, setSummary] = useState(null);
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
      
      // Fetch NGSI-LD format data
      const [waterRes, drainageRes, lightsRes, energyRes, telecomRes, summaryRes] = await Promise.all([
        api.get(`/infrastructure/water-supply/ngsi-ld/${cityParam}`),
        api.get(`/infrastructure/drainage/ngsi-ld/${cityParam}`),
        api.get(`/infrastructure/street-lights/ngsi-ld/${cityParam}`),
        api.get(`/infrastructure/energy/ngsi-ld/${cityParam}`),
        api.get(`/infrastructure/telecom/ngsi-ld/${cityParam}`),
        api.get('/infrastructure/summary/')
      ]);

      // Parse NGSI-LD to flat objects
      const waterData = (waterRes.data || []).map(parseWaterSupply);
      const drainageData = (drainageRes.data || []).map(parseDrainage);
      const lightsData = (lightsRes.data || []).map(parseStreetLight);
      const energyData = (energyRes.data || []).map(parseEnergyMeter);
      const telecomData = (telecomRes.data || []).map(parseTelecomTower);

      setWaterSupply(waterData);
      setDrainage(drainageData);
      setStreetLights(lightsData);
      setEnergyMeters(energyData);
      setTelecomTowers(telecomData);
      setSummary(summaryRes.data);
    } catch (err) {
      console.error('Error fetching infrastructure data:', err);
      setError('Không thể tải dữ liệu hạ tầng');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'water', label: '💧 Cấp nước', count: waterSupply.length },
    { id: 'drainage', label: '🚰 Thoát nước', count: drainage.length },
    { id: 'lights', label: '💡 Đèn đường', count: streetLights.length },
    { id: 'energy', label: '⚡ Năng lượng', count: energyMeters.length },
    { id: 'telecom', label: '📡 Viễn thông', count: telecomTowers.length }
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
          <h1 className="text-3xl font-bold text-gray-900">🏗️ Hạ tầng kỹ thuật</h1>
          <p className="text-gray-600 mt-1">Quản lý hệ thống cấp thoát nước, điện chiếu sáng và viễn thông</p>
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

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-white rounded-xl shadow-lg p-4">
            <div className="text-3xl mb-2">💧</div>
            <div className="text-2xl font-bold text-blue-600">{summary.water_supply_count || waterSupply.length}</div>
            <div className="text-sm text-gray-500">Điểm cấp nước</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-4">
            <div className="text-3xl mb-2">🚰</div>
            <div className="text-2xl font-bold text-cyan-600">{summary.drainage_count || drainage.length}</div>
            <div className="text-sm text-gray-500">Điểm thoát nước</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-4">
            <div className="text-3xl mb-2">💡</div>
            <div className="text-2xl font-bold text-yellow-600">{summary.streetlight_count || streetLights.length}</div>
            <div className="text-sm text-gray-500">Đèn đường</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-4">
            <div className="text-3xl mb-2">⚡</div>
            <div className="text-2xl font-bold text-orange-600">{summary.energy_meter_count || energyMeters.length}</div>
            <div className="text-sm text-gray-500">Đồng hồ điện</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-4">
            <div className="text-3xl mb-2">📡</div>
            <div className="text-2xl font-bold text-purple-600">{summary.telecom_tower_count || telecomTowers.length}</div>
            <div className="text-sm text-gray-500">Trạm viễn thông</div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="border-b border-gray-200 overflow-x-auto">
          <nav className="flex -mb-px">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 px-4 py-4 text-center font-medium whitespace-nowrap ${
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
          {/* Water Supply Tab */}
          {activeTab === 'water' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Hệ thống cấp nước</h3>
              {waterSupply.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Không có dữ liệu cấp nước</p>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {waterSupply.map(point => (
                    <div key={point.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h4 className="font-semibold text-gray-900">{point.name}</h4>
                          <p className="text-sm text-gray-500">{point.city}</p>
                        </div>
                        <span className={`px-2 py-1 text-xs rounded-full ${STATUS_COLORS[point.status] || 'bg-gray-100'}`}>
                          {STATUS_LABELS[point.status] || point.status}
                        </span>
                      </div>
                      
                      {/* Capacity bar */}
                      {point.capacity > 0 && (
                        <div className="mb-3">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-600">Mức nước</span>
                            <span className="font-semibold">
                              {((point.current_level / point.capacity) * 100).toFixed(0)}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${Math.min(100, (point.current_level / point.capacity) * 100)}%` }}
                            ></div>
                          </div>
                        </div>
                      )}

                      <div className="space-y-1 text-sm">
                        <p><span className="text-gray-500">Loại:</span> {
                          point.point_type === 'treatment_plant' ? 'Nhà máy xử lý' :
                          point.point_type === 'pump_station' ? 'Trạm bơm' :
                          point.point_type === 'reservoir' ? 'Bể chứa' :
                          point.point_type === 'distribution_point' ? 'Điểm phân phối' : point.point_type
                        }</p>
                        {point.flow_rate && <p><span className="text-gray-500">Lưu lượng:</span> {point.flow_rate} m³/h</p>}
                        {point.pressure && <p><span className="text-gray-500">Áp suất:</span> {point.pressure} bar</p>}
                        {point.ph_level && <p><span className="text-gray-500">pH:</span> {point.ph_level}</p>}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Drainage Tab */}
          {activeTab === 'drainage' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Hệ thống thoát nước</h3>
              {drainage.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Không có dữ liệu thoát nước</p>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {drainage.map(point => (
                    <div key={point.id} className={`border rounded-lg p-4 hover:shadow-md transition-shadow ${
                      point.flood_risk === 'high' ? 'border-red-300 bg-red-50' : ''
                    }`}>
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h4 className="font-semibold text-gray-900">{point.name}</h4>
                          <p className="text-sm text-gray-500">{point.city}</p>
                        </div>
                        <div className="flex flex-col gap-1 items-end">
                          <span className={`px-2 py-1 text-xs rounded-full ${STATUS_COLORS[point.status] || 'bg-gray-100'}`}>
                            {STATUS_LABELS[point.status] || point.status}
                          </span>
                          {point.flood_risk && point.flood_risk !== 'low' && (
                            <span className={`px-2 py-1 text-xs rounded-full ${
                              point.flood_risk === 'high' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                            }`}>
                              {point.flood_risk === 'high' ? '⚠️ Ngập cao' : '⚠️ Ngập TB'}
                            </span>
                          )}
                        </div>
                      </div>
                      
                      {/* Level indicator */}
                      <div className="mb-3">
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-600">Mức nước</span>
                          <span className="font-semibold">{point.current_level?.toFixed(0) || 0}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${
                              point.current_level > 80 ? 'bg-red-500' :
                              point.current_level > 50 ? 'bg-yellow-500' : 'bg-cyan-500'
                            }`}
                            style={{ width: `${Math.min(100, point.current_level || 0)}%` }}
                          ></div>
                        </div>
                      </div>

                      <div className="space-y-1 text-sm">
                        <p><span className="text-gray-500">Loại:</span> {
                          point.point_type === 'storm_drain' ? 'Cống thoát mưa' :
                          point.point_type === 'sewer_main' ? 'Cống chính' :
                          point.point_type === 'pump_station' ? 'Trạm bơm' :
                          point.point_type === 'outfall' ? 'Cửa xả' : point.point_type
                        }</p>
                        {point.flow_rate && <p><span className="text-gray-500">Lưu lượng:</span> {point.flow_rate} m³/h</p>}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Street Lights Tab */}
          {activeTab === 'lights' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-900">Đèn đường thông minh</h3>
                <div className="flex gap-4 text-sm">
                  <span className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded-full bg-green-500"></span>
                    Bật: {streetLights.filter(l => l.status === 'on').length}
                  </span>
                  <span className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
                    Giảm: {streetLights.filter(l => l.status === 'dimmed').length}
                  </span>
                  <span className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded-full bg-gray-400"></span>
                    Tắt: {streetLights.filter(l => l.status === 'off').length}
                  </span>
                </div>
              </div>
              {streetLights.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Không có dữ liệu đèn đường</p>
              ) : (
                <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-4">
                  {streetLights.map(light => (
                    <div key={light.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className={`text-2xl ${
                            light.status === 'on' ? 'text-yellow-500' :
                            light.status === 'dimmed' ? 'text-yellow-300' : 'text-gray-400'
                          }`}>💡</span>
                          <span className="font-mono text-sm">{light.pole_id}</span>
                        </div>
                        <span className={`px-2 py-1 text-xs rounded-full ${STATUS_COLORS[light.status] || 'bg-gray-100'}`}>
                          {STATUS_LABELS[light.status] || light.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500 mb-2">{light.city}</p>
                      <div className="space-y-1 text-xs">
                        <p><span className="text-gray-500">Loại:</span> {light.lamp_type?.toUpperCase()}</p>
                        <p><span className="text-gray-500">Công suất:</span> {light.power_rating || 0}W</p>
                        {light.brightness_level && (
                          <div>
                            <span className="text-gray-500">Độ sáng:</span>
                            <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                              <div 
                                className="bg-yellow-400 h-1.5 rounded-full"
                                style={{ width: `${light.brightness_level}%` }}
                              ></div>
                            </div>
                          </div>
                        )}
                        <div className="flex gap-2 mt-2">
                          {light.is_smart && <span title="Đèn thông minh" className="bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded">IoT</span>}
                          {light.has_motion_sensor && <span title="Cảm biến chuyển động">👁️</span>}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Energy Tab */}
          {activeTab === 'energy' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Đồng hồ điện thông minh</h3>
              {energyMeters.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Không có dữ liệu đồng hồ điện</p>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {energyMeters.map(meter => (
                    <div key={meter.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h4 className="font-semibold text-gray-900">{meter.name}</h4>
                          <p className="text-sm text-gray-500">{meter.city}</p>
                          <p className="text-xs text-gray-400 font-mono">{meter.meter_id}</p>
                        </div>
                        <span className={`px-2 py-1 text-xs rounded-full ${STATUS_COLORS[meter.status] || 'bg-gray-100'}`}>
                          {STATUS_LABELS[meter.status] || meter.status}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-3 mb-3">
                        <div className="bg-gray-50 rounded p-2 text-center">
                          <div className="text-lg font-bold text-orange-600">{meter.current_power?.toFixed(0) || 0}</div>
                          <div className="text-xs text-gray-500">W hiện tại</div>
                        </div>
                        <div className="bg-gray-50 rounded p-2 text-center">
                          <div className="text-lg font-bold text-blue-600">{meter.voltage?.toFixed(0) || 220}</div>
                          <div className="text-xs text-gray-500">V</div>
                        </div>
                      </div>

                      <div className="space-y-1 text-sm">
                        <p><span className="text-gray-500">Loại:</span> {
                          meter.meter_type === 'residential' ? 'Dân cư' :
                          meter.meter_type === 'commercial' ? 'Thương mại' :
                          meter.meter_type === 'industrial' ? 'Công nghiệp' :
                          meter.meter_type === 'public' ? 'Công cộng' : meter.meter_type
                        }</p>
                        <p><span className="text-gray-500">Hôm nay:</span> {meter.today_consumption?.toFixed(1) || 0} kWh</p>
                        <p><span className="text-gray-500">Tháng này:</span> {meter.month_consumption?.toFixed(1) || 0} kWh</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Telecom Tab */}
          {activeTab === 'telecom' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Trạm viễn thông</h3>
              {telecomTowers.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Không có dữ liệu viễn thông</p>
              ) : (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {telecomTowers.map(tower => {
                    const loadPercent = tower.max_connections > 0 
                      ? (tower.active_connections / tower.max_connections) * 100 
                      : 0;
                    return (
                      <div key={tower.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <h4 className="font-semibold text-gray-900">{tower.name}</h4>
                            <p className="text-sm text-gray-500">{tower.city}</p>
                            <p className="text-xs text-gray-400 font-mono">{tower.tower_id}</p>
                          </div>
                          <span className={`px-2 py-1 text-xs rounded-full ${STATUS_COLORS[tower.status] || 'bg-gray-100'}`}>
                            {STATUS_LABELS[tower.status] || tower.status}
                          </span>
                        </div>

                        {/* Provider badge */}
                        <div className="mb-3">
                          <span className={`px-2 py-1 text-xs rounded font-medium ${
                            tower.provider === 'Viettel' ? 'bg-red-100 text-red-800' :
                            tower.provider === 'VNPT' ? 'bg-blue-100 text-blue-800' :
                            tower.provider === 'MobiFone' ? 'bg-green-100 text-green-800' : 'bg-gray-100'
                          }`}>
                            {tower.provider}
                          </span>
                          {tower.technologies && tower.technologies.map(tech => (
                            <span key={tech} className="ml-1 px-2 py-1 text-xs rounded bg-purple-100 text-purple-800">
                              {tech}
                            </span>
                          ))}
                        </div>

                        {/* Connection load */}
                        <div className="mb-3">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-600">Kết nối</span>
                            <span className="font-semibold">
                              {tower.active_connections} / {tower.max_connections}
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                loadPercent > 80 ? 'bg-red-500' :
                                loadPercent > 60 ? 'bg-yellow-500' : 'bg-green-500'
                              }`}
                              style={{ width: `${loadPercent}%` }}
                            ></div>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-2 text-sm">
                          <div>
                            <span className="text-gray-500">Loại:</span> {
                              tower.tower_type === 'macro' ? 'Macro' :
                              tower.tower_type === 'micro' ? 'Micro' :
                              tower.tower_type === 'small_cell' ? 'Small Cell' : tower.tower_type
                            }
                          </div>
                          <div>
                            <span className="text-gray-500">Cao:</span> {tower.height}m
                          </div>
                          <div>
                            <span className="text-gray-500">Phủ sóng:</span> {tower.coverage_radius}m
                          </div>
                          <div>
                            <span className="text-gray-500">Tín hiệu:</span> {tower.signal_strength}%
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
