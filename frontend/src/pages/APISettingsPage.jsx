import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function APISettingsPage() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [providers, setProviders] = useState([]);
  const [userKeys, setUserKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('providers');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showKeyModal, setShowKeyModal] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [userRes, providersRes, keysRes] = await Promise.all([
        api.get('/auth/profile/'),
        api.get('/api-providers/'),
        api.get('/my-api-keys/')
      ]);
      setUser(userRes.data);
      setProviders(providersRes.data.results || providersRes.data);
      setUserKeys(keysRes.data.results || keysRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryIcon = (category) => {
    const icons = {
      weather: '🌤️',
      air_quality: '💨',
      traffic: '🚗',
      maps: '🗺️',
      notifications: '🔔',
      other: '🔧'
    };
    return icons[category] || '🔧';
  };

  const getCategoryColor = (category) => {
    const colors = {
      weather: 'bg-blue-100 text-blue-800',
      air_quality: 'bg-green-100 text-green-800',
      traffic: 'bg-yellow-100 text-yellow-800',
      maps: 'bg-purple-100 text-purple-800',
      notifications: 'bg-red-100 text-red-800',
      other: 'bg-gray-100 text-gray-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const handleAddKey = (provider) => {
    setSelectedProvider(provider);
    setShowKeyModal(true);
  };

  const handleSaveKey = async (apiKey) => {
    try {
      // Check if user already has a key for this provider
      const existingKey = userKeys.find(k => k.provider === selectedProvider.id);
      
      if (existingKey) {
        await api.patch(`/my-api-keys/${existingKey.id}/`, {
          api_key: apiKey,
          is_active: true
        });
        setMessage({ type: 'success', text: `API key đã cập nhật cho ${selectedProvider.name}` });
      } else {
        await api.post('/my-api-keys/', {
          provider: selectedProvider.id,
          api_key: apiKey
        });
        setMessage({ type: 'success', text: `API key đã thêm cho ${selectedProvider.name}` });
      }
      
      setShowKeyModal(false);
      setSelectedProvider(null);
      loadData();
    } catch (error) {
      setMessage({ type: 'error', text: 'Lỗi khi lưu API key: ' + (error.response?.data?.detail || error.message) });
    }
  };

  const handleDeleteKey = async (keyId) => {
    if (!window.confirm('Bạn có chắc muốn xóa API key này?')) return;
    
    try {
      await api.delete(`/my-api-keys/${keyId}/`);
      setMessage({ type: 'success', text: 'Đã xóa API key' });
      loadData();
    } catch (error) {
      setMessage({ type: 'error', text: 'Lỗi khi xóa API key' });
    }
  };

  const handleSetSystemKey = async (provider, apiKey) => {
    try {
      await api.post(`/api-providers/${provider.id}/set_system_key/`, {
        api_key: apiKey
      });
      setMessage({ type: 'success', text: `System key đã cập nhật cho ${provider.name}` });
      loadData();
    } catch (error) {
      setMessage({ type: 'error', text: 'Lỗi khi lưu system key' });
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
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">🔐 Quản lý API Keys</h1>
          <p className="mt-2 text-gray-600">
            Quản lý các API key cho các dịch vụ bên thứ 3
          </p>
        </div>
      </div>

      {/* Message */}
      {message.text && (
        <div className={`p-4 rounded-lg ${message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {message.text}
          <button onClick={() => setMessage({ type: '', text: '' })} className="float-right">×</button>
        </div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('providers')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'providers'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📦 Nhà cung cấp API
          </button>
          <button
            onClick={() => setActiveTab('my-keys')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'my-keys'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            🔑 API Keys của tôi
          </button>
          {user?.is_staff && (
            <button
              onClick={() => setActiveTab('system-keys')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'system-keys'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              ⚙️ System Keys (Admin)
            </button>
          )}
          {user?.is_staff && (
            <button
              onClick={() => setActiveTab('add-provider')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'add-provider'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              ➕ Thêm Provider (Admin)
            </button>
          )}
        </nav>
      </div>

      {/* Providers Tab */}
      {activeTab === 'providers' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {providers.map(provider => (
            <div key={provider.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getCategoryIcon(provider.category)}</span>
                  <div>
                    <h3 className="font-semibold text-gray-900">{provider.name}</h3>
                    <span className={`text-xs px-2 py-1 rounded ${getCategoryColor(provider.category)}`}>
                      {provider.category_display}
                    </span>
                  </div>
                </div>
                {provider.is_premium && (
                  <span className="text-yellow-500">⭐</span>
                )}
              </div>
              
              <p className="mt-3 text-sm text-gray-600 line-clamp-2">
                {provider.description || 'Không có mô tả'}
              </p>
              
              <div className="mt-4 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Xác thực:</span>
                  <span className="font-medium">{provider.auth_type_display}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Rate limit:</span>
                  <span className="font-medium">{provider.rate_limit_per_minute}/phút</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">System key:</span>
                  <span className={provider.has_system_key ? 'text-green-600' : 'text-gray-400'}>
                    {provider.has_system_key ? '✓ Có' : '✗ Chưa'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Key của bạn:</span>
                  <span className={provider.has_user_key ? 'text-green-600' : 'text-gray-400'}>
                    {provider.has_user_key ? '✓ Có' : '✗ Chưa'}
                  </span>
                </div>
              </div>
              
              <div className="mt-4 flex space-x-2">
                <button
                  onClick={() => handleAddKey(provider)}
                  className="flex-1 px-3 py-2 text-sm bg-primary-600 text-white rounded hover:bg-primary-700"
                >
                  {provider.has_user_key ? '✏️ Sửa key' : '➕ Thêm key'}
                </button>
                {provider.documentation_url && (
                  <a
                    href={provider.documentation_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-2 text-sm border border-gray-300 rounded hover:bg-gray-50"
                  >
                    📖
                  </a>
                )}
              </div>
            </div>
          ))}
          
          {providers.length === 0 && (
            <div className="col-span-full text-center py-12 text-gray-500">
              Chưa có nhà cung cấp API nào được cấu hình
            </div>
          )}
        </div>
      )}

      {/* My Keys Tab */}
      {activeTab === 'my-keys' && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Provider</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">API Key</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Trạng thái</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sử dụng</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Hành động</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {userKeys.map(key => (
                <tr key={key.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <span className="mr-2">{getCategoryIcon(key.provider_category)}</span>
                      <span className="font-medium">{key.provider_name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap font-mono text-sm text-gray-500">
                    {key.api_key_masked || '********'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs rounded ${key.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {key.is_active ? 'Hoạt động' : 'Tắt'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {key.usage_count} lần
                    {key.last_used && (
                      <span className="block text-xs">
                        Cuối: {new Date(key.last_used).toLocaleDateString('vi-VN')}
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <button
                      onClick={() => {
                        const provider = providers.find(p => p.id === key.provider);
                        if (provider) handleAddKey(provider);
                      }}
                      className="text-primary-600 hover:text-primary-900 mr-3"
                    >
                      Sửa
                    </button>
                    <button
                      onClick={() => handleDeleteKey(key.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Xóa
                    </button>
                  </td>
                </tr>
              ))}
              {userKeys.length === 0 && (
                <tr>
                  <td colSpan="5" className="px-6 py-12 text-center text-gray-500">
                    Bạn chưa có API key nào. Vào tab "Nhà cung cấp API" để thêm.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* System Keys Tab (Admin) */}
      {activeTab === 'system-keys' && user?.is_staff && (
        <SystemKeysManager 
          providers={providers} 
          onSave={handleSetSystemKey}
          onRefresh={loadData}
        />
      )}

      {/* Add Provider Tab (Admin) */}
      {activeTab === 'add-provider' && user?.is_staff && (
        <AddProviderForm onSuccess={() => { loadData(); setActiveTab('providers'); }} />
      )}

      {/* Add/Edit Key Modal */}
      {showKeyModal && selectedProvider && (
        <APIKeyModal
          provider={selectedProvider}
          existingKey={userKeys.find(k => k.provider === selectedProvider.id)}
          onSave={handleSaveKey}
          onClose={() => { setShowKeyModal(false); setSelectedProvider(null); }}
        />
      )}
    </div>
  );
}

// Modal for adding/editing API key
function APIKeyModal({ provider, existingKey, onSave, onClose }) {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (apiKey.trim()) {
      onSave(apiKey.trim());
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 className="text-lg font-semibold mb-4">
          {existingKey ? '✏️ Cập nhật' : '➕ Thêm'} API Key - {provider.name}
        </h3>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              API Key
            </label>
            <div className="relative">
              <input
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder={existingKey ? 'Nhập key mới để thay thế...' : 'Nhập API key...'}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                required
              />
              <button
                type="button"
                onClick={() => setShowKey(!showKey)}
                className="absolute right-2 top-2 text-gray-400 hover:text-gray-600"
              >
                {showKey ? '🙈' : '👁️'}
              </button>
            </div>
            {existingKey && (
              <p className="text-xs text-gray-500 mt-1">
                Key hiện tại: {existingKey.api_key_masked}
              </p>
            )}
          </div>
          
          <div className="mb-4 p-3 bg-blue-50 rounded text-sm">
            <p className="font-medium text-blue-800">Hướng dẫn lấy API key:</p>
            <p className="text-blue-600 mt-1">
              1. Truy cập: <a href={provider.documentation_url || provider.base_url} target="_blank" rel="noopener noreferrer" className="underline">{provider.base_url}</a>
            </p>
            <p className="text-blue-600">2. Đăng ký tài khoản (nếu chưa có)</p>
            <p className="text-blue-600">3. Vào trang API Keys hoặc Developer Console</p>
            <p className="text-blue-600">4. Tạo API key mới và copy vào đây</p>
          </div>
          
          <div className="flex space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Hủy
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
            >
              Lưu
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// System Keys Manager (Admin only)
function SystemKeysManager({ providers, onSave, onRefresh }) {
  const [editingProvider, setEditingProvider] = useState(null);
  const [apiKey, setApiKey] = useState('');

  const handleSave = async () => {
    if (editingProvider && apiKey.trim()) {
      await onSave(editingProvider, apiKey.trim());
      setEditingProvider(null);
      setApiKey('');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">⚙️ System API Keys</h3>
      <p className="text-sm text-gray-600 mb-4">
        System keys được dùng làm mặc định khi user không có key riêng. Keys này được mã hóa an toàn.
      </p>
      
      <div className="space-y-4">
        {providers.map(provider => (
          <div key={provider.id} className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-center space-x-3">
              <span className="text-xl">{provider.category === 'weather' ? '🌤️' : provider.category === 'air_quality' ? '💨' : '🔧'}</span>
              <div>
                <span className="font-medium">{provider.name}</span>
                <span className={`ml-2 text-xs px-2 py-1 rounded ${provider.has_system_key ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'}`}>
                  {provider.has_system_key ? '✓ Đã cấu hình' : 'Chưa cấu hình'}
                </span>
              </div>
            </div>
            
            {editingProvider?.id === provider.id ? (
              <div className="flex items-center space-x-2">
                <input
                  type="password"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="Nhập API key..."
                  className="px-3 py-1 border rounded text-sm"
                />
                <button
                  onClick={handleSave}
                  className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
                >
                  Lưu
                </button>
                <button
                  onClick={() => { setEditingProvider(null); setApiKey(''); }}
                  className="px-3 py-1 border rounded text-sm hover:bg-gray-50"
                >
                  Hủy
                </button>
              </div>
            ) : (
              <button
                onClick={() => setEditingProvider(provider)}
                className="px-3 py-1 text-sm border border-primary-600 text-primary-600 rounded hover:bg-primary-50"
              >
                {provider.has_system_key ? 'Cập nhật' : 'Thêm key'}
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// Add Provider Form (Admin only)
function AddProviderForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    name: '',
    slug: '',
    category: 'other',
    description: '',
    base_url: '',
    documentation_url: '',
    auth_type: 'api_key_query',
    auth_key_name: 'api_key',
    rate_limit_per_minute: 60,
    rate_limit_per_day: 1000,
    is_active: true,
    is_premium: false
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Auto-generate slug from name
    if (name === 'name') {
      setFormData(prev => ({
        ...prev,
        slug: value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      await api.post('/api-providers/', formData);
      onSuccess();
    } catch (err) {
      setError(err.response?.data?.detail || 'Lỗi khi thêm provider');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold mb-4">➕ Thêm Nhà cung cấp API mới</h3>
      
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Tên Provider *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="vd: OpenWeatherMap"
              className="mt-1 w-full px-3 py-2 border rounded-md"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Slug *</label>
            <input
              type="text"
              name="slug"
              value={formData.slug}
              onChange={handleChange}
              placeholder="vd: openweathermap"
              className="mt-1 w-full px-3 py-2 border rounded-md bg-gray-50"
              required
            />
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Danh mục *</label>
            <select
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="mt-1 w-full px-3 py-2 border rounded-md"
            >
              <option value="weather">🌤️ Thời tiết</option>
              <option value="air_quality">💨 Chất lượng không khí</option>
              <option value="traffic">🚗 Giao thông</option>
              <option value="maps">🗺️ Bản đồ</option>
              <option value="notifications">🔔 Thông báo</option>
              <option value="other">🔧 Khác</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Loại xác thực *</label>
            <select
              name="auth_type"
              value={formData.auth_type}
              onChange={handleChange}
              className="mt-1 w-full px-3 py-2 border rounded-md"
            >
              <option value="api_key_query">API Key trong Query Params</option>
              <option value="api_key_header">API Key trong Header</option>
              <option value="bearer_token">Bearer Token</option>
              <option value="basic_auth">Basic Auth</option>
              <option value="none">Không cần xác thực</option>
            </select>
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Mô tả</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="2"
            className="mt-1 w-full px-3 py-2 border rounded-md"
            placeholder="Mô tả ngắn về API provider..."
          />
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Base URL *</label>
            <input
              type="url"
              name="base_url"
              value={formData.base_url}
              onChange={handleChange}
              placeholder="https://api.example.com"
              className="mt-1 w-full px-3 py-2 border rounded-md"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Tên param API Key</label>
            <input
              type="text"
              name="auth_key_name"
              value={formData.auth_key_name}
              onChange={handleChange}
              placeholder="vd: appid, X-API-Key"
              className="mt-1 w-full px-3 py-2 border rounded-md"
            />
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Link tài liệu</label>
          <input
            type="url"
            name="documentation_url"
            value={formData.documentation_url}
            onChange={handleChange}
            placeholder="https://docs.example.com/api"
            className="mt-1 w-full px-3 py-2 border rounded-md"
          />
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Rate limit (per minute)</label>
            <input
              type="number"
              name="rate_limit_per_minute"
              value={formData.rate_limit_per_minute}
              onChange={handleChange}
              className="mt-1 w-full px-3 py-2 border rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Rate limit (per day)</label>
            <input
              type="number"
              name="rate_limit_per_day"
              value={formData.rate_limit_per_day}
              onChange={handleChange}
              className="mt-1 w-full px-3 py-2 border rounded-md"
            />
          </div>
        </div>
        
        <div className="flex items-center space-x-6">
          <label className="flex items-center">
            <input
              type="checkbox"
              name="is_active"
              checked={formData.is_active}
              onChange={handleChange}
              className="mr-2"
            />
            <span className="text-sm">Kích hoạt</span>
          </label>
          <label className="flex items-center">
            <input
              type="checkbox"
              name="is_premium"
              checked={formData.is_premium}
              onChange={handleChange}
              className="mr-2"
            />
            <span className="text-sm">⭐ Premium (trả phí)</span>
          </label>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50"
        >
          {loading ? 'Đang lưu...' : '➕ Thêm Provider'}
        </button>
      </form>
    </div>
  );
}
