import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Weather Stations
export const weatherStationAPI = {
  getAll: () => api.get('/weather-stations/'),
  getById: (id) => api.get(`/weather-stations/${id}/`),
  create: (data) => api.post('/weather-stations/', data),
  update: (id, data) => api.put(`/weather-stations/${id}/`, data),
  delete: (id) => api.delete(`/weather-stations/${id}/`),
  getNearby: (lat, lon, radius) => 
    api.get(`/weather-stations/nearby/?lat=${lat}&lon=${lon}&radius=${radius}`),
};

// Air Quality Sensors
export const airQualityAPI = {
  getAll: () => api.get('/air-quality-sensors/'),
  getById: (id) => api.get(`/air-quality-sensors/${id}/`),
  create: (data) => api.post('/air-quality-sensors/', data),
};

// Weather Observations
export const weatherObservationAPI = {
  getAll: (params) => api.get('/weather/', { params }),
  getLatest: (lat, lon) => api.get(`/weather/latest/?lat=${lat}&lon=${lon}`),
  fetch: (lat, lon, city) => {
    const params = new URLSearchParams();
    if (lat && lon) {
      params.append('lat', lat);
      params.append('lon', lon);
    }
    if (city) params.append('city', city);
    return api.get(`/fetch/weather?${params.toString()}`);
  },
};

// Air Quality Observations
export const airQualityObservationAPI = {
  getAll: (params) => api.get('/air-quality/', { params }),
  getLatest: (lat, lon) => api.get(`/air-quality/latest/?lat=${lat}&lon=${lon}`),
  fetch: (lat, lon) => api.get(`/fetch/air-quality?lat=${lat}&lon=${lon}`),
};

// Traffic Observations
export const trafficAPI = {
  getAll: (params) => api.get('/traffic/', { params }),
};

// Public Services
export const publicServiceAPI = {
  getAll: (params) => api.get('/public-services/', { params }),
  getNearby: (lat, lon, radius, type) => {
    const params = new URLSearchParams();
    params.append('lat', lat);
    params.append('lon', lon);
    params.append('radius', radius);
    if (type) params.append('type', type);
    return api.get(`/public-services/nearby/?${params.toString()}`);
  },
};

// Integration
export const integrationAPI = {
  syncWeather: () => api.post('/sync/weather'),
  syncAirQuality: () => api.post('/sync/air-quality'),
};

// Health
export const healthAPI = {
  check: () => api.get('/health'),
};

export default api;
