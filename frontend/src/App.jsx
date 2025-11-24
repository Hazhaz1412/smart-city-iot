import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import WeatherPage from './pages/WeatherPage';
import AirQualityPage from './pages/AirQualityPage';
import MapPage from './pages/MapPage';
import PublicServicesPage from './pages/PublicServicesPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        {/* Navigation */}
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
            </div>
          </div>
        </nav>

        {/* Content */}
        <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/weather" element={<WeatherPage />} />
            <Route path="/air-quality" element={<AirQualityPage />} />
            <Route path="/map" element={<MapPage />} />
            <Route path="/services" element={<PublicServicesPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
