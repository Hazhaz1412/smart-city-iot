import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const API_URL = 'http://localhost:8000/api/v1';

export default function DeviceDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [device, setDevice] = useState(null);
  const [readings, setReadings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [mapReady, setMapReady] = useState(false);

  useEffect(() => {
    loadDeviceData();
  }, [id]);

  useEffect(() => {
    // Initialize map after device loads
    if (device && !mapReady) {
      const timer = setTimeout(() => {
        try {
          const map = L.map('device-map').setView([device.latitude, device.longitude], 15);
          
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          }).addTo(map);
          
          L.marker([device.latitude, device.longitude])
            .addTo(map)
            .bindPopup(`<strong>${device.name}</strong><br/>${device.device_type}`);
          
          setMapReady(true);
        } catch (err) {
          console.error('Map initialization error:', err);
        }
      }, 100);
      
      return () => clearTimeout(timer);
    }
  }, [device, mapReady]);

  const loadDeviceData = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      setLoading(true);
      
      // Load device info
      const deviceRes = await fetch(`${API_URL}/auth/devices/${id}/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (!deviceRes.ok) {
        throw new Error('Failed to load device');
      }
      
      const deviceData = await deviceRes.json();
      console.log('Device data:', deviceData);
      setDevice(deviceData);

      // Load recent readings
      try {
        const readingsRes = await fetch(`${API_URL}/auth/devices/${id}/readings/?limit=10`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (readingsRes.ok) {
          const readingsData = await readingsRes.json();
          console.log('Readings data:', readingsData);
          setReadings(Array.isArray(readingsData) ? readingsData : []);
        }
      } catch (readingsErr) {
        console.error('Failed to load readings:', readingsErr);
        setReadings([]);
      }
    } catch (err) {
      console.error('Load device error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Bạn có chắc muốn xóa thiết bị này?')) return;

    const token = localStorage.getItem('access_token');
    try {
      const res = await fetch(`${API_URL}/auth/devices/${id}/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        navigate('/my-devices');
      } else {
        alert('Không thể xóa thiết bị');
      }
    } catch (err) {
      alert('Lỗi: ' + err.message);
    }
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

  if (error || !device) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">Không tìm thấy thiết bị</p>
          <Link to="/my-devices" className="text-indigo-600 hover:text-indigo-800">
            ← Quay lại
          </Link>
        </div>
      </div>
    );
  }

  const getDeviceIcon = (type) => {
    const icons = {
      weather_station: '🌤️',
      air_quality_sensor: '💨',
      traffic_sensor: '🚦',
      custom: '📡'
    };
    return icons[type] || '📡';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-6">
          <Link to="/my-devices" className="text-indigo-600 hover:text-indigo-800 text-sm">
            ← Quay lại danh sách
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Info */}
          <div className="lg:col-span-2 space-y-6">
            {/* Device Card */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <span className="text-4xl">{getDeviceIcon(device.device_type)}</span>
                  <div>
                    <h1 className="text-2xl font-bold text-gray-900">{device.name}</h1>
                    <div className="flex items-center space-x-2 mt-1">
                      <span className="text-sm text-gray-500">ID: {device.device_id}</span>
                      {device.is_verified && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                          ✓ Đã xác minh
                        </span>
                      )}
                      {device.is_public && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                          🌐 Public
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  device.status === 'active' 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {device.status}
                </span>
              </div>

              {device.description && (
                <p className="text-gray-600 mb-4">{device.description}</p>
              )}

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-500">Loại:</span>
                  <p className="text-gray-900">{device.device_type}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Địa chỉ:</span>
                  <p className="text-gray-900">{device.address || 'N/A'}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Tọa độ:</span>
                  <p className="text-gray-900">{device.latitude}, {device.longitude}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-500">Tạo lúc:</span>
                  <p className="text-gray-900">{new Date(device.created_at).toLocaleDateString('vi-VN')}</p>
                </div>
              </div>

              {/* Actions */}
              <div className="mt-6 flex space-x-3">
                <Link
                  to={`/device/${id}/edit`}
                  className="flex-1 px-4 py-2 bg-indigo-600 text-white text-center rounded-lg hover:bg-indigo-700"
                >
                  ✏️ Chỉnh sửa
                </Link>
                <button
                  onClick={handleDelete}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                >
                  🗑️ Xóa
                </button>
              </div>
            </div>

            {/* Recent Readings */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                📊 Dữ liệu gần đây
              </h2>
              {readings.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Chưa có dữ liệu nào</p>
              ) : (
                <div className="space-y-3">
                  {readings.map((reading, idx) => (
                    <div key={idx} className="border border-gray-200 rounded p-3">
                      <div className="flex justify-between items-start mb-2">
                        <span className="text-xs text-gray-500">
                          {new Date(reading.timestamp).toLocaleString('vi-VN')}
                        </span>
                      </div>
                      <pre className="text-xs bg-gray-50 p-2 rounded overflow-x-auto">
                        {JSON.stringify(reading.data, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Map */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-4 sticky top-4">
              <h2 className="text-lg font-semibold text-gray-900 mb-3">📍 Vị trí</h2>
              <div id="device-map" style={{ height: '400px', width: '100%' }} className="rounded overflow-hidden bg-gray-100"></div>
              <div className="mt-3 text-sm text-gray-600">
                <p>📍 {device.latitude}, {device.longitude}</p>
                {device.address && <p>🏠 {device.address}</p>}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
