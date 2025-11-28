import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import LocationPicker from '../components/LocationPicker';

const API_URL = 'http://localhost:8000/api/v1';

export default function EditDevicePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    device_type: 'weather_station',
    description: '',
    latitude: '',
    longitude: '',
    address: '',
    status: 'active',
    is_public: false,
    api_endpoint: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadDevice();
  }, [id]);

  const loadDevice = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      const response = await fetch(`${API_URL}/auth/devices/${id}/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) throw new Error('Failed to load device');
      
      const device = await response.json();
      setFormData({
        name: device.name,
        device_type: device.device_type,
        description: device.description || '',
        latitude: device.latitude,
        longitude: device.longitude,
        address: device.address || '',
        status: device.status,
        is_public: device.is_public,
        api_endpoint: device.api_endpoint || '',
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value
    });
  };

  const handleLocationChange = (lat, lng) => {
    setFormData({
      ...formData,
      latitude: lat,
      longitude: lng
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSaving(true);

    const token = localStorage.getItem('access_token');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      const deviceData = {
        ...formData,
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude)
      };

      const response = await fetch(`${API_URL}/auth/devices/${id}/`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(deviceData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(Object.values(errorData)[0]);
      }
      
      navigate(`/device/${id}`);
    } catch (err) {
      setError(err.message || 'Failed to update device');
    } finally {
      setSaving(false);
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

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="mb-6">
            <Link to={`/device/${id}`} className="text-indigo-600 hover:text-indigo-800 text-sm">
              ← Quay lại
            </Link>
          </div>

          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            ✏️ Chỉnh sửa thiết bị
          </h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tên thiết bị *
                </label>
                <input
                  name="name"
                  type="text"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Loại thiết bị *
                </label>
                <select
                  name="device_type"
                  required
                  value={formData.device_type}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="weather_station">🌤️ Weather Station</option>
                  <option value="air_quality_sensor">💨 Air Quality Sensor</option>
                  <option value="traffic_sensor">🚦 Traffic Sensor</option>
                  <option value="custom">📡 Custom Device</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Trạng thái
                </label>
                <select
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="maintenance">Maintenance</option>
                </select>
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Mô tả
                </label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              
              <div className="md:col-span-2">
                <LocationPicker
                  latitude={formData.latitude}
                  longitude={formData.longitude}
                  onLocationChange={handleLocationChange}
                />
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Địa chỉ
                </label>
                <input
                  name="address"
                  type="text"
                  value={formData.address}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  API Endpoint (optional)
                </label>
                <input
                  name="api_endpoint"
                  type="url"
                  value={formData.api_endpoint}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              
              <div className="md:col-span-2">
                <label className="flex items-center">
                  <input
                    name="is_public"
                    type="checkbox"
                    checked={formData.is_public}
                    onChange={handleChange}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">
                    🌐 Công khai thiết bị này (cho phép người khác xem dữ liệu)
                  </span>
                </label>
              </div>
            </div>

            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={saving}
                className="flex-1 py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {saving ? 'Đang lưu...' : '💾 Lưu thay đổi'}
              </button>
              
              <Link
                to={`/device/${id}`}
                className="flex-1 py-2 px-4 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 text-center"
              >
                Hủy
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
