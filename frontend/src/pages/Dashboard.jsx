import { useState, useEffect } from 'react';
import { 
  weatherObservationAPI, 
  airQualityObservationAPI,
  weatherStationAPI,
  integrationAPI,
  healthAPI
} from '../api';

export default function Dashboard() {
  const [stats, setStats] = useState({
    weatherStations: 0,
    weatherObservations: 0,
    airQualityObservations: 0,
    systemHealth: 'checking...'
  });
  const [loading, setLoading] = useState(true);
  const [latestWeather, setLatestWeather] = useState(null);
  const [latestAirQuality, setLatestAirQuality] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Get counts
      const [weatherStations, weatherObs, airQualityObs, health] = await Promise.all([
        weatherStationAPI.getAll(),
        weatherObservationAPI.getAll({ hours: 24 }),
        airQualityObservationAPI.getAll({ hours: 24 }),
        healthAPI.check()
      ]);

      setStats({
        weatherStations: weatherStations.data.results?.length || weatherStations.data.count || 0,
        weatherObservations: weatherObs.data.results?.length || weatherObs.data.count || 0,
        airQualityObservations: airQualityObs.data.results?.length || airQualityObs.data.count || 0,
        systemHealth: health.data.status
      });

      // Get latest data for Hanoi
      try {
        const weather = await weatherObservationAPI.getLatest(21.0285, 105.8542);
        setLatestWeather(weather.data);
      } catch (err) {
        console.log('No weather data available');
      }

      try {
        const airQuality = await airQualityObservationAPI.getLatest(21.0285, 105.8542);
        setLatestAirQuality(airQuality.data);
      } catch (err) {
        console.log('No air quality data available');
      }

    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSync = async (type) => {
    try {
      if (type === 'weather') {
        await integrationAPI.syncWeather();
        alert('Đã bắt đầu đồng bộ dữ liệu thời tiết!');
      } else {
        await integrationAPI.syncAirQuality();
        alert('Đã bắt đầu đồng bộ dữ liệu chất lượng không khí!');
      }
      setTimeout(loadDashboardData, 3000);
    } catch (error) {
      alert('Lỗi: ' + error.message);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard Tổng Quan</h1>
        <p className="mt-2 text-sm text-gray-600">
          Tổng quan về dữ liệu thành phố thông minh
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Trạm Thời tiết"
          value={stats.weatherStations}
          icon="🌤️"
          color="blue"
        />
        <StatCard
          title="Quan trắc Thời tiết"
          value={stats.weatherObservations}
          subtitle="24h qua"
          icon="📊"
          color="green"
        />
        <StatCard
          title="Quan trắc Chất lượng KK"
          value={stats.airQualityObservations}
          subtitle="24h qua"
          icon="🌫️"
          color="purple"
        />
        <StatCard
          title="Trạng thái Hệ thống"
          value={stats.systemHealth}
          icon="💚"
          color="emerald"
        />
      </div>

      {/* Latest Data */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Weather */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              🌤️ Thời tiết Hà Nội
            </h3>
            {latestWeather ? (
              <div className="space-y-3">
                <DataRow label="Nhiệt độ" value={`${latestWeather.temperature}°C`} />
                <DataRow label="Độ ẩm" value={`${latestWeather.humidity}%`} />
                <DataRow label="Áp suất" value={`${latestWeather.pressure} hPa`} />
                <DataRow label="Gió" value={`${latestWeather.wind_speed} m/s`} />
                <DataRow 
                  label="Thời gian" 
                  value={new Date(latestWeather.observed_at).toLocaleString('vi-VN')} 
                />
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500 mb-4">Chưa có dữ liệu</p>
                <button
                  onClick={() => handleSync('weather')}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  Đồng bộ dữ liệu
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Air Quality */}
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              🌫️ Chất lượng Không khí Hà Nội
            </h3>
            {latestAirQuality ? (
              <div className="space-y-3">
                <DataRow 
                  label="AQI" 
                  value={latestAirQuality.aqi || 'N/A'}
                  highlight={getAQIColor(latestAirQuality.aqi)}
                />
                <DataRow label="PM2.5" value={`${latestAirQuality.pm25 || 'N/A'} μg/m³`} />
                <DataRow label="PM10" value={`${latestAirQuality.pm10 || 'N/A'} μg/m³`} />
                <DataRow label="NO2" value={`${latestAirQuality.no2 || 'N/A'} μg/m³`} />
                <DataRow 
                  label="Thời gian" 
                  value={new Date(latestAirQuality.observed_at).toLocaleString('vi-VN')} 
                />
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500 mb-4">Chưa có dữ liệu</p>
                <button
                  onClick={() => handleSync('airquality')}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  Đồng bộ dữ liệu
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Thao tác nhanh</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <button
            onClick={() => handleSync('weather')}
            className="inline-flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            🔄 Đồng bộ Thời tiết
          </button>
          <button
            onClick={() => handleSync('airquality')}
            className="inline-flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700"
          >
            🔄 Đồng bộ Chất lượng KK
          </button>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, subtitle, icon, color }) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    emerald: 'bg-emerald-50 text-emerald-600',
  };

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className={`flex-shrink-0 rounded-md p-3 ${colorClasses[color]}`}>
            <span className="text-2xl">{icon}</span>
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd className="flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">{value}</div>
                {subtitle && (
                  <div className="ml-2 text-sm text-gray-500">{subtitle}</div>
                )}
              </dd>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
}

function DataRow({ label, value, highlight }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-sm text-gray-600">{label}:</span>
      <span className={`text-sm font-medium ${highlight || 'text-gray-900'}`}>
        {value}
      </span>
    </div>
  );
}

function getAQIColor(aqi) {
  if (!aqi) return 'text-gray-500';
  if (aqi <= 50) return 'text-green-600';
  if (aqi <= 100) return 'text-yellow-600';
  if (aqi <= 150) return 'text-orange-600';
  if (aqi <= 200) return 'text-red-600';
  return 'text-purple-600';
}
