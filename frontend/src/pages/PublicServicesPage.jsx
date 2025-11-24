import { useState, useEffect } from 'react';
import { publicServiceAPI } from '../api';

export default function PublicServicesPage() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadServices();
  }, [filter]);

  const loadServices = async () => {
    try {
      setLoading(true);
      const params = filter !== 'all' ? { type: filter } : {};
      const response = await publicServiceAPI.getAll(params);
      setServices(response.data.results || response.data || []);
    } catch (error) {
      console.error('Error loading services:', error);
    } finally {
      setLoading(false);
    }
  };

  const serviceTypes = [
    { value: 'all', label: 'Tất cả', icon: '📍' },
    { value: 'park', label: 'Công viên', icon: '🏞️' },
    { value: 'parking', label: 'Bãi đỗ xe', icon: '🅿️' },
    { value: 'bus_stop', label: 'Trạm xe buýt', icon: '🚌' },
    { value: 'hospital', label: 'Bệnh viện', icon: '🏥' },
    { value: 'school', label: 'Trường học', icon: '🏫' },
    { value: 'library', label: 'Thư viện', icon: '📚' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dịch vụ Công cộng</h1>
        <p className="mt-2 text-sm text-gray-600">
          Các dịch vụ công cộng trong thành phố
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white shadow rounded-lg p-4">
        <div className="flex flex-wrap gap-2">
          {serviceTypes.map(type => (
            <button
              key={type.value}
              onClick={() => setFilter(type.value)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                filter === type.value
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {type.icon} {type.label}
            </button>
          ))}
        </div>
      </div>

      {/* Services List */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Danh sách Dịch vụ ({services.length})
        </h2>
        {loading ? (
          <div className="text-center py-8">Đang tải...</div>
        ) : services.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {services.map(service => (
              <ServiceCard key={service.id} service={service} />
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            Không có dịch vụ nào
          </div>
        )}
      </div>
    </div>
  );
}

function ServiceCard({ service }) {
  const getIcon = (type) => {
    const icons = {
      park: '🏞️',
      parking: '🅿️',
      bus_stop: '🚌',
      hospital: '🏥',
      school: '🏫',
      library: '📚',
      other: '📍',
    };
    return icons[type] || '📍';
  };

  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition">
      <div className="flex items-start justify-between">
        <div className="flex items-center">
          <span className="text-2xl mr-2">{getIcon(service.service_type)}</span>
          <div>
            <h3 className="font-medium text-gray-900">{service.name}</h3>
            <p className="text-xs text-gray-500">{service.service_type_display}</p>
          </div>
        </div>
        <span className={`text-xs px-2 py-1 rounded ${
          service.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
        }`}>
          {service.is_active ? 'Hoạt động' : 'Đóng cửa'}
        </span>
      </div>

      {service.description && (
        <p className="mt-2 text-sm text-gray-600">{service.description}</p>
      )}

      <div className="mt-3 space-y-1">
        {service.address && (
          <p className="text-sm text-gray-500">
            📍 {service.address}
          </p>
        )}
        {service.opening_hours && (
          <p className="text-sm text-gray-500">
            🕐 {service.opening_hours}
          </p>
        )}
        {service.contact_phone && (
          <p className="text-sm text-gray-500">
            📞 {service.contact_phone}
          </p>
        )}
        {service.website && (
          <a
            href={service.website}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary-600 hover:text-primary-700"
          >
            🌐 Website
          </a>
        )}
      </div>

      <div className="mt-3 pt-3 border-t text-xs text-gray-400">
        {service.latitude.toFixed(4)}, {service.longitude.toFixed(4)}
      </div>
    </div>
  );
}
