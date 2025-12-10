import React, { useState, useEffect, useCallback } from 'react';
import api from '../api';

// Vietnamese cities with coordinates
const CITIES = [
  { id: 'hanoi', name: 'Hà Nội', lat: 21.0285, lon: 105.8542 },
  { id: 'hcmc', name: 'TP. Hồ Chí Minh', lat: 10.8231, lon: 106.6297 },
  { id: 'danang', name: 'Đà Nẵng', lat: 16.0544, lon: 108.2022 },
  { id: 'haiphong', name: 'Hải Phòng', lat: 20.8449, lon: 106.6881 },
  { id: 'cantho', name: 'Cần Thơ', lat: 10.0452, lon: 105.7469 },
  { id: 'nhatrang', name: 'Nha Trang', lat: 12.2388, lon: 109.1967 },
  { id: 'hue', name: 'Huế', lat: 16.4637, lon: 107.5909 },
  { id: 'vungtau', name: 'Vũng Tàu', lat: 10.3460, lon: 107.0843 },
];

// Weather icon mapping
const getWeatherIcon = (description) => {
  const desc = description?.toLowerCase() || '';
  if (desc.includes('clear') || desc.includes('sunny')) return '☀️';
  if (desc.includes('cloud')) return '☁️';
  if (desc.includes('rain') || desc.includes('drizzle')) return '🌧️';
  if (desc.includes('thunder') || desc.includes('storm')) return '⛈️';
  if (desc.includes('snow')) return '❄️';
  if (desc.includes('mist') || desc.includes('fog') || desc.includes('haze')) return '🌫️';
  return '🌤️';
};

// AQI level info
const getAQIInfo = (aqi) => {
  if (!aqi) return { level: 'N/A', color: 'bg-gray-100 text-gray-600', emoji: '❓' };
  if (aqi <= 50) return { level: 'Tốt', color: 'bg-green-100 text-green-800', emoji: '😊' };
  if (aqi <= 100) return { level: 'Trung bình', color: 'bg-yellow-100 text-yellow-800', emoji: '😐' };
  if (aqi <= 150) return { level: 'Không tốt cho nhóm nhạy cảm', color: 'bg-orange-100 text-orange-800', emoji: '😷' };
  if (aqi <= 200) return { level: 'Không tốt', color: 'bg-red-100 text-red-800', emoji: '😨' };
  if (aqi <= 300) return { level: 'Rất không tốt', color: 'bg-purple-100 text-purple-800', emoji: '🤢' };
  return { level: 'Nguy hiểm', color: 'bg-rose-200 text-rose-900', emoji: '☠️' };
};

export default function Dashboard() {
  const [selectedCity, setSelectedCity] = useState(() => {
    const saved = localStorage.getItem('dashboard_city');
    return saved || 'hanoi';
  });
  const [stats, setStats] = useState({ devices: 0, active: 0, alerts: 0 });
  const [weather, setWeather] = useState(null);
  const [airQuality, setAirQuality] = useState(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState({ weather: false, air: false });
  const [error, setError] = useState(null);

  const currentCity = CITIES.find(c => c.id === selectedCity) || CITIES[0];

  const loadDashboardData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [devicesRes, weatherRes, airRes] = await Promise.all([
        api.get('/auth/devices/'),
        api.get('/integrations/weather/').catch(() => ({ data: null })),
        api.get('/integrations/air-quality/').catch(() => ({ data: null })),
      ]);

      const devices = devicesRes.data?.results || devicesRes.data || [];
      setStats({
        devices: devices.length,
        active: devices.filter(d => d.is_active).length,
        alerts: devices.filter(d => d.status === 'alert').length,
      });
      setWeather(weatherRes.data);
      setAirQuality(airRes.data);
    } catch (err) {
      setError('Không thể tải dữ liệu. Vui lòng thử lại.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  useEffect(() => {
    localStorage.setItem('dashboard_city', selectedCity);
  }, [selectedCity]);

  const handleSync = async (type) => {
    setSyncing(prev => ({ ...prev, [type]: true }));
    try {
      const endpoint = type === 'weather' ? '/integrations/sync/weather' : '/integrations/sync/air-quality';
      await api.post(endpoint, {
        lat: currentCity.lat,
        lon: currentCity.lon,
        city: currentCity.name,
      });
      await loadDashboardData();
    } catch (err) {
      setError(`Không thể đồng bộ ${type === 'weather' ? 'thời tiết' : 'chất lượng không khí'}`);
    } finally {
      setSyncing(prev => ({ ...prev, [type]: false }));
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải dữ liệu...</p>
        </div>
      </div>
    );
  }

  const aqiInfo = getAQIInfo(airQuality?.aqi);
  const weatherIcon = getWeatherIcon(weather?.description);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
            <p className="text-gray-500 mt-1">Tổng quan hệ thống IoT thành phố thông minh</p>
          </div>
          
          {/* City Selector */}
          <div className="flex items-center gap-3">
            <label className="text-sm font-medium text-gray-600">📍 Thành phố:</label>
            <select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
              className="px-4 py-2 bg-white border border-gray-200 rounded-xl shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            >
              {CITIES.map(city => (
                <option key={city.id} value={city.id}>{city.name}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
          ⚠️ {error}
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard
          icon="📱"
          title="Tổng thiết bị"
          value={stats.devices}
          subtitle="Thiết bị đã đăng ký"
          gradient="from-blue-500 to-blue-600"
        />
        <StatCard
          icon="✅"
          title="Đang hoạt động"
          value={stats.active}
          subtitle={`${stats.devices > 0 ? Math.round((stats.active / stats.devices) * 100) : 0}% thiết bị`}
          gradient="from-green-500 to-emerald-600"
        />
        <StatCard
          icon="🚨"
          title="Cảnh báo"
          value={stats.alerts}
          subtitle="Cần xử lý"
          gradient="from-red-500 to-rose-600"
        />
      </div>

      {/* Weather & Air Quality */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Weather Card */}
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className="bg-gradient-to-r from-sky-400 to-blue-500 p-6 text-white">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-medium opacity-90">Thời tiết</h3>
                <p className="text-sm opacity-75">{currentCity.name}</p>
              </div>
              <button
                onClick={() => handleSync('weather')}
                disabled={syncing.weather}
                className="px-3 py-1.5 bg-white/20 hover:bg-white/30 rounded-lg text-sm transition-colors disabled:opacity-50"
              >
                {syncing.weather ? '⏳' : '🔄'} Đồng bộ
              </button>
            </div>
            
            {weather ? (
              <div className="mt-6 flex items-center gap-4">
                <span className="text-7xl">{weatherIcon}</span>
                <div>
                  <div className="text-5xl font-light">{Math.round(weather.temperature || 0)}°C</div>
                  <div className="text-white/80 capitalize mt-1">{weather.description || 'N/A'}</div>
                </div>
              </div>
            ) : (
              <div className="mt-6 text-center py-8 text-white/70">
                <p>Chưa có dữ liệu thời tiết</p>
                <p className="text-sm mt-1">Nhấn "Đồng bộ" để cập nhật</p>
              </div>
            )}
          </div>
          
          {weather && (
            <div className="p-6 grid grid-cols-3 gap-4">
              <WeatherDetail icon="💧" label="Độ ẩm" value={`${weather.humidity || 0}%`} />
              <WeatherDetail icon="💨" label="Gió" value={`${weather.wind_speed || 0} m/s`} />
              <WeatherDetail icon="🌡️" label="Áp suất" value={`${weather.pressure || 0} hPa`} />
            </div>
          )}
        </div>

        {/* Air Quality Card */}
        <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div className={`p-6 ${airQuality?.aqi ? 'bg-gradient-to-r from-purple-400 to-indigo-500' : 'bg-gradient-to-r from-gray-400 to-gray-500'} text-white`}>
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-medium opacity-90">Chất lượng không khí</h3>
                <p className="text-sm opacity-75">{airQuality?.station || currentCity.name}</p>
              </div>
              <button
                onClick={() => handleSync('air')}
                disabled={syncing.air}
                className="px-3 py-1.5 bg-white/20 hover:bg-white/30 rounded-lg text-sm transition-colors disabled:opacity-50"
              >
                {syncing.air ? '⏳' : '🔄'} Đồng bộ
              </button>
            </div>
            
            {airQuality?.aqi ? (
              <div className="mt-6 flex items-center gap-4">
                <div className="w-24 h-24 rounded-full bg-white/20 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-4xl font-bold">{airQuality.aqi}</div>
                    <div className="text-xs opacity-75">AQI</div>
                  </div>
                </div>
                <div>
                  <div className="text-2xl font-medium">{aqiInfo.emoji} {aqiInfo.level}</div>
                  <div className="text-white/80 mt-1 text-sm">
                    {airQuality.dominant_pollutant && `Chất ô nhiễm chính: ${airQuality.dominant_pollutant.toUpperCase()}`}
                  </div>
                </div>
              </div>
            ) : (
              <div className="mt-6 text-center py-8 text-white/70">
                <p>Chưa có dữ liệu chất lượng không khí</p>
                <p className="text-sm mt-1">Nhấn "Đồng bộ" để cập nhật</p>
              </div>
            )}
          </div>
          
          {airQuality?.aqi && (
            <div className="p-6">
              <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${aqiInfo.color} mb-4`}>
                {aqiInfo.level}
              </div>
              <div className="grid grid-cols-2 gap-4">
                {airQuality.pm25 && <PollutantBadge name="PM2.5" value={airQuality.pm25} unit="µg/m³" />}
                {airQuality.pm10 && <PollutantBadge name="PM10" value={airQuality.pm10} unit="µg/m³" />}
                {airQuality.o3 && <PollutantBadge name="O₃" value={airQuality.o3} unit="ppb" />}
                {airQuality.no2 && <PollutantBadge name="NO₂" value={airQuality.no2} unit="ppb" />}
                {airQuality.so2 && <PollutantBadge name="SO₂" value={airQuality.so2} unit="ppb" />}
                {airQuality.co && <PollutantBadge name="CO" value={airQuality.co} unit="ppm" />}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">⚡ Thao tác nhanh</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <QuickAction
            icon="📱"
            label="Quản lý thiết bị"
            href="/devices"
          />
          <QuickAction
            icon="🗺️"
            label="Bản đồ"
            href="/map"
          />
          <QuickAction
            icon="📊"
            label="Thống kê"
            href="/analytics"
          />
          <QuickAction
            icon="👤"
            label="Hồ sơ"
            href="/profile"
          />
        </div>
      </div>

      {/* Last Updated */}
      <div className="mt-6 text-center text-sm text-gray-400">
        Cập nhật lúc: {new Date().toLocaleString('vi-VN')}
      </div>
    </div>
  );
}

// Sub-components
function StatCard({ icon, title, value, subtitle, gradient }) {
  return (
    <div className={`bg-gradient-to-br ${gradient} rounded-2xl p-6 text-white shadow-lg transform hover:scale-[1.02] transition-transform`}>
      <div className="flex items-center justify-between">
        <span className="text-4xl">{icon}</span>
        <div className="text-right">
          <div className="text-3xl font-bold">{value}</div>
          <div className="text-sm opacity-80">{title}</div>
        </div>
      </div>
      <div className="mt-4 text-sm opacity-75">{subtitle}</div>
    </div>
  );
}

function WeatherDetail({ icon, label, value }) {
  return (
    <div className="text-center">
      <span className="text-2xl">{icon}</span>
      <div className="text-gray-500 text-xs mt-1">{label}</div>
      <div className="font-semibold text-gray-700">{value}</div>
    </div>
  );
}

function PollutantBadge({ name, value, unit }) {
  return (
    <div className="bg-gray-50 rounded-lg p-3">
      <div className="text-xs text-gray-500">{name}</div>
      <div className="font-semibold text-gray-800">{value} <span className="text-xs font-normal">{unit}</span></div>
    </div>
  );
}

function QuickAction({ icon, label, href }) {
  return (
    <a
      href={href}
      className="flex flex-col items-center gap-2 p-4 bg-gray-50 hover:bg-gray-100 rounded-xl transition-colors group"
    >
      <span className="text-3xl group-hover:scale-110 transition-transform">{icon}</span>
      <span className="text-sm font-medium text-gray-600">{label}</span>
    </a>
  );
}
