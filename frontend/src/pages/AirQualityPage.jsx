import { useState, useEffect } from 'react';
import { airQualityObservationAPI, airQualityAPI } from '../api';

export default function AirQualityPage() {
  const [observations, setObservations] = useState([]);
  const [sensors, setSensors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [obsResponse, sensorsResponse] = await Promise.all([
        airQualityObservationAPI.getAll({ hours: 24 }),
        airQualityAPI.getAll(),
      ]);
      setObservations(obsResponse.data.results || obsResponse.data || []);
      setSensors(sensorsResponse.data.results || sensorsResponse.data || []);
    } catch (error) {
      console.error('Error loading air quality data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getAQILevel = (aqi) => {
    if (!aqi) return { label: 'N/A', color: 'gray' };
    if (aqi <= 50) return { label: 'Tốt', color: 'green' };
    if (aqi <= 100) return { label: 'Trung bình', color: 'yellow' };
    if (aqi <= 150) return { label: 'Kém', color: 'orange' };
    if (aqi <= 200) return { label: 'Xấu', color: 'red' };
    return { label: 'Rất xấu', color: 'purple' };
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Chất lượng Không khí</h1>
        <p className="mt-2 text-sm text-gray-600">
          Dữ liệu chất lượng không khí từ các cảm biến
        </p>
      </div>

      {/* AQI Info */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Chỉ số AQI</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <AQICard level="Tốt" range="0-50" color="bg-green-500" />
          <AQICard level="Trung bình" range="51-100" color="bg-yellow-500" />
          <AQICard level="Kém" range="101-150" color="bg-orange-500" />
          <AQICard level="Xấu" range="151-200" color="bg-red-500" />
          <AQICard level="Rất xấu" range="201+" color="bg-purple-500" />
        </div>
      </div>

      {/* Sensors */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Cảm biến ({sensors.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sensors.map(sensor => (
            <div key={sensor.id} className="border rounded-lg p-4 hover:shadow-md transition">
              <h3 className="font-medium text-gray-900">{sensor.name}</h3>
              <p className="text-sm text-gray-500 mt-1">{sensor.address}</p>
              <div className="mt-2 flex items-center justify-between">
                <span className="text-xs text-gray-400">
                  📍 {sensor.latitude.toFixed(4)}, {sensor.longitude.toFixed(4)}
                </span>
                <span className={`text-xs px-2 py-1 rounded ${
                  sensor.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {sensor.is_active ? 'Hoạt động' : 'Tạm ngưng'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Observations */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Quan trắc Gần đây ({observations.length})
        </h2>
        {loading ? (
          <div className="text-center py-8">Đang tải...</div>
        ) : observations.length > 0 ? (
          <div className="grid grid-cols-1 gap-4">
            {observations.slice(0, 10).map(obs => {
              const aqiLevel = getAQILevel(obs.aqi);
              return (
                <div key={obs.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-medium text-gray-900">
                        {obs.location_name || 'N/A'}
                      </h3>
                      <p className="text-sm text-gray-500 mt-1">
                        {new Date(obs.observed_at).toLocaleString('vi-VN')}
                      </p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium text-white bg-${aqiLevel.color}-500`}>
                      AQI: {obs.aqi || 'N/A'} - {aqiLevel.label}
                    </span>
                  </div>
                  <div className="mt-4 grid grid-cols-2 md:grid-cols-6 gap-3">
                    <div>
                      <p className="text-xs text-gray-500">PM2.5</p>
                      <p className="text-sm font-medium">{obs.pm25 || 'N/A'} μg/m³</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">PM10</p>
                      <p className="text-sm font-medium">{obs.pm10 || 'N/A'} μg/m³</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">NO2</p>
                      <p className="text-sm font-medium">{obs.no2 || 'N/A'} μg/m³</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">O3</p>
                      <p className="text-sm font-medium">{obs.o3 || 'N/A'} μg/m³</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">CO</p>
                      <p className="text-sm font-medium">{obs.co || 'N/A'} μg/m³</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">SO2</p>
                      <p className="text-sm font-medium">{obs.so2 || 'N/A'} μg/m³</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            Chưa có dữ liệu quan trắc
          </div>
        )}
      </div>
    </div>
  );
}

function AQICard({ level, range, color }) {
  return (
    <div className="text-center">
      <div className={`${color} text-white rounded-lg p-3 mb-2`}>
        <div className="text-2xl font-bold">{range}</div>
      </div>
      <div className="text-sm font-medium text-gray-700">{level}</div>
    </div>
  );
}
