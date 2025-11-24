# Hướng dẫn Tích hợp Mobile App

Tài liệu này hướng dẫn cách gọi API từ mobile app (React Native, Flutter, Native iOS/Android) đến hệ thống Smart City backend.

## 📋 Mục lục

- [Thông tin API](#thông-tin-api)
- [Authentication](#authentication)
- [React Native](#react-native)
- [Flutter](#flutter)
- [Native iOS (Swift)](#native-ios-swift)
- [Native Android (Kotlin)](#native-android-kotlin)
- [Best Practices](#best-practices)

---

## 🔌 Thông tin API

### Base URL
```
Development: http://localhost:8000/api/v1
Production: https://your-domain.com/api/v1
```

### Content-Type
```
Content-Type: application/json
Accept: application/json
```

### CORS
Backend đã cấu hình CORS cho phép các origin khác nhau. Trong production, cần cấu hình `CORS_ALLOWED_ORIGINS` trong settings.

---

## 🔐 Authentication

Hiện tại API đang ở chế độ public (không yêu cầu authentication). Để bảo mật production, khuyến nghị thêm:

### Django Token Authentication (DRF)
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

Sau đó trong mobile app:
```
Authorization: Token your_token_here
```

### OAuth2/JWT (Khuyến nghị)
Sử dụng `djangorestframework-simplejwt`:
```
Authorization: Bearer your_jwt_token
```

---

## ⚛️ React Native

### 1. Cài đặt Dependencies

```bash
npm install axios
# hoặc
yarn add axios
```

### 2. API Client Setup

Tạo file `src/services/api.js`:

```javascript
import axios from 'axios';

const BASE_URL = 'http://10.0.2.2:8000/api/v1'; // Android emulator
// const BASE_URL = 'http://localhost:8000/api/v1'; // iOS simulator
// const BASE_URL = 'https://your-domain.com/api/v1'; // Production

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Add token interceptor if using authentication
api.interceptors.request.use(
  async (config) => {
    // const token = await AsyncStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;
```

### 3. API Services

Tạo file `src/services/smartCity.js`:

```javascript
import api from './api';

export const weatherAPI = {
  // Lấy tất cả trạm thời tiết
  getAllStations: async () => {
    const response = await api.get('/weather-stations/');
    return response.data;
  },

  // Lấy chi tiết trạm
  getStation: async (id) => {
    const response = await api.get(`/weather-stations/${id}/`);
    return response.data;
  },

  // Lấy observations
  getObservations: async (params = {}) => {
    const response = await api.get('/weather-observations/', { params });
    return response.data;
  },

  // Lấy observation mới nhất
  getLatestObservation: async () => {
    const response = await api.get('/weather-observations/latest/');
    return response.data;
  },

  // Fetch dữ liệu từ OpenWeatherMap
  fetchWeatherData: async (latitude, longitude, city) => {
    const response = await api.post('/weather-observations/fetch/', {
      latitude,
      longitude,
      city,
    });
    return response.data;
  },
};

export const airQualityAPI = {
  // Lấy tất cả cảm biến
  getAllSensors: async () => {
    const response = await api.get('/air-quality-sensors/');
    return response.data;
  },

  // Lấy observations
  getObservations: async (params = {}) => {
    const response = await api.get('/air-quality-observations/', { params });
    return response.data;
  },

  // Lấy observation mới nhất
  getLatestObservation: async () => {
    const response = await api.get('/air-quality-observations/latest/');
    return response.data;
  },

  // Fetch dữ liệu từ OpenAQ
  fetchAirQualityData: async (latitude, longitude, city) => {
    const response = await api.post('/air-quality-observations/fetch/', {
      latitude,
      longitude,
      city,
    });
    return response.data;
  },
};

export const publicServicesAPI = {
  getAll: async (params = {}) => {
    const response = await api.get('/public-services/', { params });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/public-services/${id}/`);
    return response.data;
  },

  nearby: async (latitude, longitude, radius = 5000, serviceType = null) => {
    const params = { latitude, longitude, radius };
    if (serviceType) params.type = serviceType;
    const response = await api.get('/public-services/nearby/', { params });
    return response.data;
  },
};

export const integrationAPI = {
  syncWeather: async () => {
    const response = await api.post('/integrations/sync/weather/');
    return response.data;
  },

  syncAirQuality: async () => {
    const response = await api.post('/integrations/sync/air-quality/');
    return response.data;
  },

  getStatus: async () => {
    const response = await api.get('/integrations/status/');
    return response.data;
  },
};

export const healthAPI = {
  check: async () => {
    const response = await api.get('/health/');
    return response.data;
  },
};
```

### 4. Component Example

Tạo component `WeatherScreen.js`:

```javascript
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { weatherAPI } from '../services/smartCity';

const WeatherScreen = () => {
  const [observations, setObservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadWeatherData();
  }, []);

  const loadWeatherData = async () => {
    try {
      setLoading(true);
      const data = await weatherAPI.getObservations({ hours: 24 });
      setObservations(data.results || data);
    } catch (error) {
      console.error('Error loading weather:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadWeatherData();
    setRefreshing(false);
  };

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <Text style={styles.location}>{item.location_name || 'Unknown'}</Text>
      <View style={styles.row}>
        <Text style={styles.temperature}>{item.temperature}°C</Text>
        <Text style={styles.humidity}>💧 {item.humidity}%</Text>
      </View>
      <Text style={styles.time}>
        {new Date(item.observed_at).toLocaleString()}
      </Text>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={observations}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderItem}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  card: {
    backgroundColor: 'white',
    margin: 10,
    padding: 15,
    borderRadius: 8,
    elevation: 2,
  },
  location: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  temperature: {
    fontSize: 24,
    color: '#ff6b6b',
  },
  humidity: {
    fontSize: 18,
    color: '#4dabf7',
  },
  time: {
    fontSize: 12,
    color: '#868e96',
  },
});

export default WeatherScreen;
```

### 5. Location-based Services

Sử dụng `@react-native-community/geolocation` hoặc `expo-location`:

```javascript
import Geolocation from '@react-native-community/geolocation';
import { publicServicesAPI } from '../services/smartCity';

const findNearbyServices = () => {
  Geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords;
      
      try {
        const services = await publicServicesAPI.nearby(
          latitude,
          longitude,
          5000, // radius 5km
          'hospital' // service type
        );
        console.log('Nearby hospitals:', services);
      } catch (error) {
        console.error('Error finding services:', error);
      }
    },
    (error) => console.error('Location error:', error),
    { enableHighAccuracy: true, timeout: 20000, maximumAge: 1000 }
  );
};
```

---

## 🎯 Flutter

### 1. Cài đặt Dependencies

Thêm vào `pubspec.yaml`:

```yaml
dependencies:
  http: ^1.1.0
  dio: ^5.3.3  # Alternative, powerful HTTP client
  geolocator: ^10.1.0  # For location
  flutter_map: ^6.0.1  # For maps
```

### 2. API Client Setup

Tạo file `lib/services/api_client.dart`:

```dart
import 'package:dio/dio.dart';

class ApiClient {
  static const String baseUrl = 'http://10.0.2.2:8000/api/v1'; // Android
  // static const String baseUrl = 'http://localhost:8000/api/v1'; // iOS
  
  late final Dio _dio;

  ApiClient() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    // Add interceptors
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          // Add token if needed
          // final token = await storage.getToken();
          // options.headers['Authorization'] = 'Bearer $token';
          return handler.next(options);
        },
        onError: (error, handler) {
          print('API Error: ${error.response?.data ?? error.message}');
          return handler.next(error);
        },
      ),
    );
  }

  Dio get dio => _dio;
}
```

### 3. Weather Service

Tạo file `lib/services/weather_service.dart`:

```dart
import 'package:dio/dio.dart';
import 'api_client.dart';

class WeatherService {
  final ApiClient _apiClient = ApiClient();

  Future<List<dynamic>> getAllStations() async {
    try {
      final response = await _apiClient.dio.get('/weather-stations/');
      return response.data['results'] ?? response.data;
    } on DioException catch (e) {
      throw Exception('Failed to load stations: ${e.message}');
    }
  }

  Future<Map<String, dynamic>> getStation(int id) async {
    try {
      final response = await _apiClient.dio.get('/weather-stations/$id/');
      return response.data;
    } on DioException catch (e) {
      throw Exception('Failed to load station: ${e.message}');
    }
  }

  Future<List<dynamic>> getObservations({int? hours}) async {
    try {
      final queryParams = hours != null ? {'hours': hours} : {};
      final response = await _apiClient.dio.get(
        '/weather-observations/',
        queryParameters: queryParams,
      );
      return response.data['results'] ?? response.data;
    } on DioException catch (e) {
      throw Exception('Failed to load observations: ${e.message}');
    }
  }

  Future<Map<String, dynamic>> getLatestObservation() async {
    try {
      final response = await _apiClient.dio.get('/weather-observations/latest/');
      return response.data;
    } on DioException catch (e) {
      throw Exception('Failed to load latest observation: ${e.message}');
    }
  }

  Future<Map<String, dynamic>> fetchWeatherData({
    double? latitude,
    double? longitude,
    String? city,
  }) async {
    try {
      final response = await _apiClient.dio.post(
        '/weather-observations/fetch/',
        data: {
          if (latitude != null) 'latitude': latitude,
          if (longitude != null) 'longitude': longitude,
          if (city != null) 'city': city,
        },
      );
      return response.data;
    } on DioException catch (e) {
      throw Exception('Failed to fetch weather: ${e.message}');
    }
  }
}
```

### 4. Widget Example

Tạo file `lib/screens/weather_screen.dart`:

```dart
import 'package:flutter/material.dart';
import '../services/weather_service.dart';

class WeatherScreen extends StatefulWidget {
  const WeatherScreen({Key? key}) : super(key: key);

  @override
  State<WeatherScreen> createState() => _WeatherScreenState();
}

class _WeatherScreenState extends State<WeatherScreen> {
  final WeatherService _weatherService = WeatherService();
  List<dynamic> _observations = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadWeatherData();
  }

  Future<void> _loadWeatherData() async {
    try {
      setState(() => _loading = true);
      final data = await _weatherService.getObservations(hours: 24);
      setState(() {
        _observations = data;
        _loading = false;
      });
    } catch (e) {
      setState(() => _loading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Weather'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadWeatherData,
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadWeatherData,
              child: ListView.builder(
                itemCount: _observations.length,
                itemBuilder: (context, index) {
                  final obs = _observations[index];
                  return Card(
                    margin: const EdgeInsets.all(8),
                    child: ListTile(
                      title: Text(obs['location_name'] ?? 'Unknown'),
                      subtitle: Text(
                        DateTime.parse(obs['observed_at']).toLocal().toString(),
                      ),
                      trailing: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            '${obs['temperature']}°C',
                            style: const TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Text('💧 ${obs['humidity']}%'),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
    );
  }
}
```

### 5. Location Services

```dart
import 'package:geolocator/geolocator.dart';
import '../services/api_client.dart';

class LocationService {
  final ApiClient _apiClient = ApiClient();

  Future<Position> getCurrentPosition() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      throw Exception('Location services are disabled.');
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        throw Exception('Location permissions are denied');
      }
    }

    return await Geolocator.getCurrentPosition();
  }

  Future<List<dynamic>> getNearbyServices(String serviceType) async {
    final position = await getCurrentPosition();
    
    final response = await _apiClient.dio.get(
      '/public-services/nearby/',
      queryParameters: {
        'latitude': position.latitude,
        'longitude': position.longitude,
        'radius': 5000,
        'type': serviceType,
      },
    );
    
    return response.data;
  }
}
```

---

## 📱 Native iOS (Swift)

### 1. API Client Setup

Tạo file `APIClient.swift`:

```swift
import Foundation

class APIClient {
    static let shared = APIClient()
    
    private let baseURL = "http://localhost:8000/api/v1"
    private let session: URLSession
    
    private init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 10
        config.timeoutIntervalForResource = 10
        session = URLSession(configuration: config)
    }
    
    func request<T: Decodable>(
        endpoint: String,
        method: String = "GET",
        body: Data? = nil,
        completion: @escaping (Result<T, Error>) -> Void
    ) {
        guard let url = URL(string: baseURL + endpoint) else {
            completion(.failure(NSError(domain: "Invalid URL", code: -1)))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.httpBody = body
        
        // Add token if needed
        // if let token = UserDefaults.standard.string(forKey: "token") {
        //     request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        // }
        
        session.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data else {
                completion(.failure(NSError(domain: "No data", code: -1)))
                return
            }
            
            do {
                let decoded = try JSONDecoder().decode(T.self, from: data)
                completion(.success(decoded))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}
```

### 2. Weather Service

Tạo file `WeatherService.swift`:

```swift
import Foundation

struct WeatherObservation: Codable {
    let id: Int
    let locationName: String?
    let temperature: Double?
    let humidity: Double?
    let pressure: Double?
    let observedAt: String
    
    enum CodingKeys: String, CodingKey {
        case id
        case locationName = "location_name"
        case temperature
        case humidity
        case pressure
        case observedAt = "observed_at"
    }
}

struct WeatherResponse: Codable {
    let results: [WeatherObservation]
}

class WeatherService {
    static let shared = WeatherService()
    private let apiClient = APIClient.shared
    
    func getObservations(hours: Int? = nil, completion: @escaping (Result<[WeatherObservation], Error>) -> Void) {
        var endpoint = "/weather-observations/"
        if let hours = hours {
            endpoint += "?hours=\(hours)"
        }
        
        apiClient.request(endpoint: endpoint) { (result: Result<WeatherResponse, Error>) in
            switch result {
            case .success(let response):
                completion(.success(response.results))
            case .failure(let error):
                completion(.failure(error))
            }
        }
    }
    
    func getLatestObservation(completion: @escaping (Result<WeatherObservation, Error>) -> Void) {
        apiClient.request(endpoint: "/weather-observations/latest/", completion: completion)
    }
    
    func fetchWeatherData(latitude: Double?, longitude: Double?, city: String?, completion: @escaping (Result<WeatherObservation, Error>) -> Void) {
        var body: [String: Any] = [:]
        if let lat = latitude { body["latitude"] = lat }
        if let lon = longitude { body["longitude"] = lon }
        if let city = city { body["city"] = city }
        
        guard let jsonData = try? JSONSerialization.data(withJSONObject: body) else {
            completion(.failure(NSError(domain: "Invalid JSON", code: -1)))
            return
        }
        
        apiClient.request(
            endpoint: "/weather-observations/fetch/",
            method: "POST",
            body: jsonData,
            completion: completion
        )
    }
}
```

### 3. ViewController Example

```swift
import UIKit

class WeatherViewController: UITableViewController {
    private var observations: [WeatherObservation] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        title = "Weather"
        
        navigationItem.rightBarButtonItem = UIBarButtonItem(
            barButtonSystemItem: .refresh,
            target: self,
            action: #selector(loadWeatherData)
        )
        
        loadWeatherData()
    }
    
    @objc private func loadWeatherData() {
        WeatherService.shared.getObservations(hours: 24) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let observations):
                    self?.observations = observations
                    self?.tableView.reloadData()
                case .failure(let error):
                    print("Error: \(error)")
                    self?.showError(error)
                }
            }
        }
    }
    
    private func showError(_ error: Error) {
        let alert = UIAlertController(
            title: "Error",
            message: error.localizedDescription,
            preferredStyle: .alert
        )
        alert.addAction(UIAlertAction(title: "OK", style: .default))
        present(alert, animated: true)
    }
    
    // MARK: - Table View
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return observations.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "WeatherCell") ?? UITableViewCell(style: .subtitle, reuseIdentifier: "WeatherCell")
        
        let obs = observations[indexPath.row]
        cell.textLabel?.text = obs.locationName ?? "Unknown"
        cell.detailTextLabel?.text = "\(obs.temperature ?? 0)°C, \(obs.humidity ?? 0)%"
        
        return cell
    }
}
```

---

## 🤖 Native Android (Kotlin)

### 1. Dependencies

Thêm vào `build.gradle.kts`:

```kotlin
dependencies {
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
```

### 2. API Client Setup

Tạo file `ApiClient.kt`:

```kotlin
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object ApiClient {
    private const val BASE_URL = "http://10.0.2.2:8000/api/v1/"
    
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }
    
    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .addInterceptor { chain ->
            val request = chain.request().newBuilder()
                .addHeader("Content-Type", "application/json")
                .addHeader("Accept", "application/json")
                // Add token if needed
                // .addHeader("Authorization", "Bearer $token")
                .build()
            chain.proceed(request)
        }
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(10, TimeUnit.SECONDS)
        .build()
    
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val weatherService: WeatherService = retrofit.create(WeatherService::class.java)
    val airQualityService: AirQualityService = retrofit.create(AirQualityService::class.java)
    val publicServicesService: PublicServicesService = retrofit.create(PublicServicesService::class.java)
}
```

### 3. Data Models

Tạo file `Models.kt`:

```kotlin
import com.google.gson.annotations.SerializedName

data class WeatherObservation(
    val id: Int,
    @SerializedName("location_name") val locationName: String?,
    val temperature: Double?,
    val humidity: Double?,
    val pressure: Double?,
    @SerializedName("observed_at") val observedAt: String
)

data class WeatherResponse(
    val results: List<WeatherObservation>
)

data class FetchWeatherRequest(
    val latitude: Double? = null,
    val longitude: Double? = null,
    val city: String? = null
)
```

### 4. Weather Service Interface

Tạo file `WeatherService.kt`:

```kotlin
import retrofit2.Response
import retrofit2.http.*

interface WeatherService {
    @GET("weather-stations/")
    suspend fun getAllStations(): Response<List<WeatherStation>>
    
    @GET("weather-stations/{id}/")
    suspend fun getStation(@Path("id") id: Int): Response<WeatherStation>
    
    @GET("weather-observations/")
    suspend fun getObservations(
        @Query("hours") hours: Int? = null
    ): Response<WeatherResponse>
    
    @GET("weather-observations/latest/")
    suspend fun getLatestObservation(): Response<WeatherObservation>
    
    @POST("weather-observations/fetch/")
    suspend fun fetchWeatherData(
        @Body request: FetchWeatherRequest
    ): Response<WeatherObservation>
}
```

### 5. Repository

Tạo file `WeatherRepository.kt`:

```kotlin
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class WeatherRepository {
    private val weatherService = ApiClient.weatherService
    
    suspend fun getObservations(hours: Int? = null): Result<List<WeatherObservation>> =
        withContext(Dispatchers.IO) {
            try {
                val response = weatherService.getObservations(hours)
                if (response.isSuccessful) {
                    Result.success(response.body()?.results ?: emptyList())
                } else {
                    Result.failure(Exception("Error: ${response.code()}"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    
    suspend fun getLatestObservation(): Result<WeatherObservation> =
        withContext(Dispatchers.IO) {
            try {
                val response = weatherService.getLatestObservation()
                if (response.isSuccessful && response.body() != null) {
                    Result.success(response.body()!!)
                } else {
                    Result.failure(Exception("Error: ${response.code()}"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    
    suspend fun fetchWeatherData(
        latitude: Double? = null,
        longitude: Double? = null,
        city: String? = null
    ): Result<WeatherObservation> = withContext(Dispatchers.IO) {
        try {
            val request = FetchWeatherRequest(latitude, longitude, city)
            val response = weatherService.fetchWeatherData(request)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Error: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

### 6. ViewModel

Tạo file `WeatherViewModel.kt`:

```kotlin
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class WeatherViewModel : ViewModel() {
    private val repository = WeatherRepository()
    
    private val _observations = MutableLiveData<List<WeatherObservation>>()
    val observations: LiveData<List<WeatherObservation>> = _observations
    
    private val _loading = MutableLiveData<Boolean>()
    val loading: LiveData<Boolean> = _loading
    
    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error
    
    fun loadObservations(hours: Int? = 24) {
        viewModelScope.launch {
            _loading.value = true
            repository.getObservations(hours)
                .onSuccess { _observations.value = it }
                .onFailure { _error.value = it.message }
            _loading.value = false
        }
    }
    
    fun fetchWeatherData(city: String) {
        viewModelScope.launch {
            _loading.value = true
            repository.fetchWeatherData(city = city)
                .onSuccess { loadObservations() }
                .onFailure { _error.value = it.message }
            _loading.value = false
        }
    }
}
```

### 7. Activity Example

Tạo file `WeatherActivity.kt`:

```kotlin
import android.os.Bundle
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.android.material.snackbar.Snackbar

class WeatherActivity : AppCompatActivity() {
    private val viewModel: WeatherViewModel by viewModels()
    private lateinit var adapter: WeatherAdapter
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_weather)
        
        setupRecyclerView()
        observeViewModel()
        
        viewModel.loadObservations()
    }
    
    private fun setupRecyclerView() {
        adapter = WeatherAdapter()
        recyclerView.apply {
            layoutManager = LinearLayoutManager(this@WeatherActivity)
            adapter = this@WeatherActivity.adapter
        }
    }
    
    private fun observeViewModel() {
        viewModel.observations.observe(this) { observations ->
            adapter.submitList(observations)
        }
        
        viewModel.loading.observe(this) { loading ->
            progressBar.visibility = if (loading) View.VISIBLE else View.GONE
        }
        
        viewModel.error.observe(this) { error ->
            error?.let {
                Snackbar.make(rootView, it, Snackbar.LENGTH_LONG).show()
            }
        }
    }
}
```

---

## 🎯 Best Practices

### 1. Error Handling
```javascript
// React Native / JavaScript
try {
  const data = await weatherAPI.getObservations();
  // Handle success
} catch (error) {
  if (error.response) {
    // Server responded with error
    console.error('Server error:', error.response.status, error.response.data);
  } else if (error.request) {
    // No response received
    console.error('Network error:', error.message);
  } else {
    console.error('Error:', error.message);
  }
}
```

### 2. Caching Strategy
- Cache dữ liệu quan trắc trong local storage/database
- Implement offline mode với AsyncStorage (RN) hoặc SharedPreferences (Android)
- Sử dụng cache-first strategy cho dữ liệu ít thay đổi

### 3. Performance
- Pagination: Sử dụng `?page=1&page_size=20` cho lists
- Lazy loading: Load dữ liệu khi cần
- Debounce search requests
- Compress images và data khi upload

### 4. Security
- **HTTPS Only**: Sử dụng HTTPS trong production
- **Token Storage**: Lưu tokens an toàn (Keychain/KeyStore)
- **Certificate Pinning**: Implement cho production apps
- **Input Validation**: Validate mọi input từ user

### 5. Testing
```javascript
// Jest test example
describe('WeatherAPI', () => {
  it('should fetch observations', async () => {
    const data = await weatherAPI.getObservations({ hours: 24 });
    expect(data).toBeDefined();
    expect(Array.isArray(data.results)).toBe(true);
  });
});
```

---

## 📊 API Endpoints Summary

### Weather
- `GET /api/v1/weather-stations/` - Danh sách trạm
- `GET /api/v1/weather-stations/{id}/` - Chi tiết trạm
- `GET /api/v1/weather-observations/` - Danh sách quan trắc
- `GET /api/v1/weather-observations/latest/` - Quan trắc mới nhất
- `POST /api/v1/weather-observations/fetch/` - Lấy dữ liệu mới

### Air Quality
- `GET /api/v1/air-quality-sensors/` - Danh sách cảm biến
- `GET /api/v1/air-quality-observations/` - Danh sách quan trắc
- `GET /api/v1/air-quality-observations/latest/` - Quan trắc mới nhất
- `POST /api/v1/air-quality-observations/fetch/` - Lấy dữ liệu mới

### Public Services
- `GET /api/v1/public-services/` - Danh sách dịch vụ
- `GET /api/v1/public-services/nearby/` - Tìm dịch vụ gần

### Integration
- `POST /api/v1/integrations/sync/weather/` - Sync weather data
- `POST /api/v1/integrations/sync/air-quality/` - Sync air quality data
- `GET /api/v1/integrations/status/` - Trạng thái integration

### Health
- `GET /api/v1/health/` - Health check

---

## 🔧 Troubleshooting

### iOS Simulator không kết nối được localhost
```
Use: http://localhost:8000
```

### Android Emulator không kết nối được localhost
```
Use: http://10.0.2.2:8000
```

### CORS Issues
Kiểm tra `CORS_ALLOWED_ORIGINS` trong Django settings.

### SSL Certificate Issues (iOS)
Thêm vào `Info.plist`:
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

---

## 📞 Support

Nếu gặp vấn đề, check:
1. Backend đang chạy: `http://localhost:8000/api/v1/health/`
2. Network connectivity
3. API response trong logs
4. Django logs: `docker-compose logs -f django`

---

**Chúc bạn code mobile app thành công! 🚀**
