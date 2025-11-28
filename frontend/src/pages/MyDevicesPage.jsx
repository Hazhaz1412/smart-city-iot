import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { userDeviceAPI } from '../api';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function MyDevicesPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [devices, setDevices] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);

  useEffect(() => {
    // Set a safety timeout to prevent infinite loading
    const timeout = setTimeout(() => {
      setLoading(false);
    }, 3000);

    loadData().finally(() => {
      clearTimeout(timeout);
    });

    return () => clearTimeout(timeout);
  }, []);

  const loadData = async () => {
    try {
      // Fetch devices and stats in parallel
      const [devicesData, statsData] = await Promise.all([
        userDeviceAPI.getMyDevices().catch(err => {
          console.error('Failed to fetch devices:', err);
          return { results: [] };
        }),
        userDeviceAPI.getStatistics().catch(err => {
          console.error('Failed to fetch stats:', err);
          return null;
        })
      ]);

      setDevices(devicesData.results || devicesData || []);
      setStats(statsData);
    } catch (error) {
      console.error('Failed to load data:', error);
      setDevices([]);
      setStats(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getDeviceTypeIcon = (type) => {
    const icons = {
      weather_station: '🌤️',
      air_quality_sensor: '💨',
      traffic_sensor: '🚦',
      custom: '📡'
    };
    return icons[type] || '📡';
  };

  const getStatusColor = (status) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      inactive: 'bg-gray-100 text-gray-800',
      maintenance: 'bg-yellow-100 text-yellow-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Đang tải...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                🌆 Thiết bị của tôi
              </h1>
              <p className="text-sm text-gray-600">
                Xin chào, {user?.username}!
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/"
                className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Dashboard
              </Link>
              <Link
                to="/map"
                className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Bản đồ
              </Link>
              <button
                onClick={handleLogout}
                className="text-red-600 hover:text-red-800 px-3 py-2 rounded-md text-sm font-medium"
              >
                Đăng xuất
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Statistics */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-sm font-medium text-gray-500">Tổng thiết bị</div>
              <div className="mt-2 text-3xl font-semibold text-gray-900">{stats.total_devices}</div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-sm font-medium text-gray-500">Đang hoạt động</div>
              <div className="mt-2 text-3xl font-semibold text-green-600">{stats.active_devices}</div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-sm font-medium text-gray-500">Public</div>
              <div className="mt-2 text-3xl font-semibold text-blue-600">{stats.public_devices}</div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-sm font-medium text-gray-500">Tổng dữ liệu</div>
              <div className="mt-2 text-3xl font-semibold text-purple-600">{stats.total_readings}</div>
            </div>
          </div>
        )}

        {/* Add Device Button */}
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-900">Danh sách thiết bị</h2>
          <Link
            to="/add-device"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
          >
            + Thêm thiết bị mới
          </Link>
        </div>

        {/* Devices Grid */}
        {devices.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <div className="text-6xl mb-4">📡</div>
            <h3 className="text-xl font-medium text-gray-900 mb-2">
              Chưa có thiết bị nào
            </h3>
            <p className="text-gray-600 mb-6">
              Thêm thiết bị IoT đầu tiên của bạn để bắt đầu thu thập dữ liệu!
            </p>
            <Link
              to="/add-device"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Thêm thiết bị ngay
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {devices.map(device => (
              <div key={device.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow">
                <div className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="text-4xl mb-3">{getDeviceTypeIcon(device.device_type)}</div>
                    <span className={`px-2 py-1 text-xs font-medium rounded ${getStatusColor(device.status)}`}>
                      {device.status}
                    </span>
                  </div>
                  
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {device.name}
                  </h3>
                  
                  <p className="text-sm text-gray-600 mb-4">
                    {device.description || 'Không có mô tả'}
                  </p>
                  
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center text-gray-600">
                      <span className="font-medium mr-2">Device ID:</span>
                      <code className="text-xs bg-gray-100 px-2 py-1 rounded">{device.device_id}</code>
                    </div>
                    
                    <div className="flex items-center text-gray-600">
                      <span className="font-medium mr-2">📍 Vị trí:</span>
                      <span className="text-xs">{device.address || `${device.latitude}, ${device.longitude}`}</span>
                    </div>
                    
                    {device.is_public && (
                      <div className="flex items-center text-blue-600">
                        <span>🌐 Public device</span>
                      </div>
                    )}
                    
                    {device.latest_reading && (
                      <div className="mt-4 pt-4 border-t border-gray-200">
                        <div className="text-xs text-gray-500 mb-2">Dữ liệu mới nhất:</div>
                        <pre className="text-xs bg-gray-50 p-2 rounded overflow-x-auto">
                          {JSON.stringify(device.latest_reading.data, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex justify-between">
                  <Link
                    to={`/device/${device.id}`}
                    className="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
                  >
                    Xem chi tiết →
                  </Link>
                  <Link
                    to={`/device/${device.id}/readings`}
                    className="text-gray-600 hover:text-gray-800 text-sm font-medium"
                  >
                    📊 Dữ liệu
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
