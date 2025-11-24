import { useState, useEffect } from 'react';
import { weatherObservationAPI, weatherStationAPI } from '../api';

export default function WeatherPage() {
  const [observations, setObservations] = useState([]);
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchCity, setSearchCity] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [obsResponse, stationsResponse] = await Promise.all([
        weatherObservationAPI.getAll({ hours: 24 }),
        weatherStationAPI.getAll(),
      ]);
      setObservations(obsResponse.data.results || obsResponse.data || []);
      setStations(stationsResponse.data.results || stationsResponse.data || []);
    } catch (error) {
      console.error('Error loading weather data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFetchWeather = async (e) => {
    e.preventDefault();
    if (!searchCity) return;

    try {
      const response = await weatherObservationAPI.fetch(null, null, searchCity);
      alert('Dữ liệu thời tiết: ' + JSON.stringify(response.data, null, 2));
      loadData();
    } catch (error) {
      alert('Lỗi: ' + error.message);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Thời tiết</h1>
        <p className="mt-2 text-sm text-gray-600">
          Dữ liệu thời tiết từ các trạm quan trắc
        </p>
      </div>

      {/* Search */}
      <div className="bg-white shadow rounded-lg p-6">
        <form onSubmit={handleFetchWeather} className="flex gap-4">
          <input
            type="text"
            value={searchCity}
            onChange={(e) => setSearchCity(e.target.value)}
            placeholder="Nhập tên thành phố (VD: Hanoi, Saigon)..."
            className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          />
          <button
            type="submit"
            className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
          >
            Tìm kiếm
          </button>
        </form>
      </div>

      {/* Stations */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Trạm Thời tiết ({stations.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {stations.map(station => (
            <div key={station.id} className="border rounded-lg p-4 hover:shadow-md transition">
              <h3 className="font-medium text-gray-900">{station.name}</h3>
              <p className="text-sm text-gray-500 mt-1">{station.address}</p>
              <div className="mt-2 flex items-center justify-between">
                <span className="text-xs text-gray-400">
                  📍 {station.latitude.toFixed(4)}, {station.longitude.toFixed(4)}
                </span>
                <span className={`text-xs px-2 py-1 rounded ${
                  station.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {station.is_active ? 'Hoạt động' : 'Tạm ngưng'}
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
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Vị trí
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nhiệt độ
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Độ ẩm
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Áp suất
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Thời gian
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {observations.slice(0, 10).map(obs => (
                  <tr key={obs.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {obs.location_name || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {obs.temperature ? `${obs.temperature}°C` : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {obs.humidity ? `${obs.humidity}%` : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {obs.pressure ? `${obs.pressure} hPa` : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(obs.observed_at).toLocaleString('vi-VN')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
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
