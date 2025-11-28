import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors (token expired)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Try to refresh token
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken
          });
          localStorage.setItem('access_token', response.data.access);
          if (response.data.refresh) {
            localStorage.setItem('refresh_token', response.data.refresh);
          }
          // Retry original request
          error.config.headers.Authorization = `Bearer ${response.data.access}`;
          return axios(error.config);
        } catch (refreshError) {
          // Refresh failed, logout
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  login: (username, password) => 
    api.post('/auth/login/', { username, password }).then(res => res.data),
  register: (userData) => 
    api.post('/auth/register/', userData).then(res => res.data),
  googleLogin: (token) => 
    api.post('/auth/google/', { token }).then(res => res.data),
  getProfile: () => 
    api.get('/auth/profile/').then(res => res.data),
  updateProfile: (data) => 
    api.put('/auth/profile/', data).then(res => res.data),
};

// User Devices API
export const userDeviceAPI = {
  getMyDevices: (params) => 
    api.get('/auth/devices/', { params }).then(res => res.data),
  getDeviceById: (id) => 
    api.get(`/auth/devices/${id}/`).then(res => res.data),
  createDevice: (data) => 
    api.post('/auth/devices/', data).then(res => res.data),
  updateDevice: (id, data) => 
    api.put(`/auth/devices/${id}/`, data).then(res => res.data),
  deleteDevice: (id) => 
    api.delete(`/auth/devices/${id}/`),
  addReading: (deviceId, data) => 
    api.post(`/auth/devices/${deviceId}/add_reading/`, data).then(res => res.data),
  getReadings: (deviceId, params) => 
    api.get(`/auth/devices/${deviceId}/readings/`, { params }).then(res => res.data),
  getStatistics: () => 
    api.get('/auth/devices/statistics/').then(res => res.data),
  getPublicDevices: () => 
    api.get('/auth/public-devices/').then(res => res.data),
};

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
