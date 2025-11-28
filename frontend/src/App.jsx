import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './pages/Dashboard';
import WeatherPage from './pages/WeatherPage';
import AirQualityPage from './pages/AirQualityPage';
import MapPage from './pages/MapPage';
import PublicServicesPage from './pages/PublicServicesPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import MyDevicesPage from './pages/MyDevicesPage';
import AddDevicePage from './pages/AddDevicePage';
import DebugPage from './pages/DebugPage';

function Navigation() {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center px-2 text-xl font-bold text-primary-600">
              🏙️ Smart City Dashboard
            </Link>
            <div className="hidden md:flex md:ml-6 md:space-x-4">
              <Link to="/" className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-primary-600">
                Dashboard
              </Link>
              <Link to="/weather" className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-primary-600">
                Thời tiết
              </Link>
              <Link to="/air-quality" className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-primary-600">
                Chất lượng KK
              </Link>
              <Link to="/map" className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-primary-600">
                Bản đồ
              </Link>
              <Link to="/services" className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-primary-600">
                Dịch vụ
              </Link>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link to="/my-devices" className="inline-flex items-center px-3 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-800">
                  📡 Thiết bị của tôi
                </Link>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-700">👤 {user?.username}</span>
                  <button
                    onClick={logout}
                    className="inline-flex items-center px-3 py-2 text-sm font-medium text-red-600 hover:text-red-800"
                  >
                    Đăng xuất
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link to="/login" className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 hover:text-gray-900">
                  Đăng nhập
                </Link>
                <Link to="/register" className="inline-flex items-center px-3 py-2 text-sm font-medium bg-primary-600 text-white rounded-md hover:bg-primary-700">
                  Đăng ký
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-100">
          <Navigation />

          {/* Content */}
          <main>
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8"><Dashboard /></div>} />
              <Route path="/weather" element={<div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8"><WeatherPage /></div>} />
              <Route path="/air-quality" element={<div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8"><AirQualityPage /></div>} />
              <Route path="/map" element={<div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8"><MapPage /></div>} />
              <Route path="/services" element={<div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8"><PublicServicesPage /></div>} />
              
              {/* Auth routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/debug" element={<DebugPage />} />
              
              {/* Protected routes - Cần đăng nhập */}
              <Route 
                path="/my-devices" 
                element={
                  <ProtectedRoute>
                    <MyDevicesPage />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/add-device" 
                element={
                  <ProtectedRoute>
                    <AddDevicePage />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
