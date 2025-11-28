import { useEffect, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export default function LocationPicker({ latitude, longitude, onLocationChange }) {
  const [map, setMap] = useState(null);
  const [marker, setMarker] = useState(null);
  const [address, setAddress] = useState('');

  useEffect(() => {
    // Initialize map
    const defaultLat = latitude || 21.0285;
    const defaultLng = longitude || 105.8542;

    try {
      const mapInstance = L.map('location-picker-map').setView([defaultLat, defaultLng], 13);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(mapInstance);

      // Add initial marker
      const markerInstance = L.marker([defaultLat, defaultLng], {
        draggable: true
      }).addTo(mapInstance);

      // Update coordinates when marker is dragged
      markerInstance.on('dragend', async function(e) {
        const position = e.target.getLatLng();
        onLocationChange(position.lat, position.lng);
        await reverseGeocode(position.lat, position.lng);
      });

      // Click on map to move marker
      mapInstance.on('click', async function(e) {
        markerInstance.setLatLng(e.latlng);
        onLocationChange(e.latlng.lat, e.latlng.lng);
        await reverseGeocode(e.latlng.lat, e.latlng.lng);
      });

      setMap(mapInstance);
      setMarker(markerInstance);

      // Initial reverse geocode
      if (latitude && longitude) {
        reverseGeocode(latitude, longitude);
      }

      return () => {
        try {
          mapInstance.remove();
        } catch (err) {
          console.error('Error removing map:', err);
        }
      };
    } catch (error) {
      console.error('Error initializing map:', error);
    }
  }, []);

  // Update marker when props change
  useEffect(() => {
    if (marker && latitude && longitude) {
      marker.setLatLng([latitude, longitude]);
      if (map) {
        map.setView([latitude, longitude], map.getZoom());
      }
    }
  }, [latitude, longitude, marker, map]);

  const reverseGeocode = async (lat, lng) => {
    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
      );
      const data = await response.json();
      if (data.display_name) {
        setAddress(data.display_name);
      }
    } catch (error) {
      console.error('Reverse geocode failed:', error);
    }
  };

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      alert('Trình duyệt không hỗ trợ geolocation');
      return;
    }

    // Show loading state
    const button = document.activeElement;
    if (button) {
      button.disabled = true;
      button.textContent = '⏳ Đang lấy vị trí...';
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        
        if (marker) {
          marker.setLatLng([lat, lng]);
        }
        if (map) {
          map.setView([lat, lng], 15);
        }
        
        onLocationChange(lat, lng);
        reverseGeocode(lat, lng);

        // Reset button
        if (button) {
          button.disabled = false;
          button.textContent = '📍 Vị trí hiện tại';
        }
      },
      (error) => {
        console.error('Geolocation error:', error);
        let errorMessage = 'Không thể lấy vị trí hiện tại';
        
        switch(error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = '🚫 Bạn đã từ chối quyền truy cập vị trí.\n\nVui lòng:\n1. Cho phép vị trí trong trình duyệt\n2. Hoặc chọn vị trí trên bản đồ';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = '📍 GPS không khả dụng.\n\nMáy tính thường không có GPS tốt.\nHãy click trên bản đồ để chọn vị trí.';
            break;
          case error.TIMEOUT:
            errorMessage = '⏱️ GPS timeout (15 giây).\n\nMáy tính desktop thường không có GPS.\nHãy click trên bản đồ để chọn vị trí thay thế.';
            break;
          default:
            errorMessage = 'Lỗi: ' + error.message + '\n\nHãy click trên bản đồ để chọn vị trí.';
        }
        
        alert(errorMessage);

        // Reset button
        if (button) {
          button.disabled = false;
          button.textContent = '📍 Vị trí hiện tại';
        }
      },
      {
        enableHighAccuracy: false,
        timeout: 15000,
        maximumAge: 60000
      }
    );
  };

  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center">
        <label className="block text-sm font-medium text-gray-700">
          📍 Chọn vị trí trên bản đồ
        </label>
        <button
          type="button"
          onClick={getCurrentLocation}
          className="text-xs px-3 py-1 bg-blue-50 text-blue-600 rounded hover:bg-blue-100"
        >
          📍 Vị trí hiện tại
        </button>
      </div>
      
      <div 
        id="location-picker-map" 
        style={{ height: '400px', width: '100%' }} 
        className="rounded-lg border border-gray-300"
      ></div>
      
      <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
        <p className="font-medium mb-1">💡 Hướng dẫn:</p>
        <ul className="text-xs space-y-1 ml-4 list-disc">
          <li>Click vào bản đồ để đặt marker</li>
          <li>Kéo thả marker để di chuyển</li>
          <li>Click "Vị trí hiện tại" để dùng GPS</li>
        </ul>
      </div>

      {address && (
        <div className="text-sm text-gray-600 bg-blue-50 p-3 rounded">
          <p className="font-medium text-blue-900">📍 Địa chỉ:</p>
          <p className="text-xs mt-1">{address}</p>
        </div>
      )}

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">
            Latitude
          </label>
          <input
            type="number"
            step="0.000001"
            value={latitude || ''}
            onChange={(e) => onLocationChange(parseFloat(e.target.value) || 0, longitude)}
            className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">
            Longitude
          </label>
          <input
            type="number"
            step="0.000001"
            value={longitude || ''}
            onChange={(e) => onLocationChange(latitude, parseFloat(e.target.value) || 0)}
            className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>
    </div>
  );
}
