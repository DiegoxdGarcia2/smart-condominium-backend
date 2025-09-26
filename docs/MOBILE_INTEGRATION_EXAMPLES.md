# 📱 Smart Condominium - Ejemplos de Integración Móvil

*Ejemplos específicos para React Native, Flutter, y desarrollo móvil nativo*

---

# 🚀 React Native + Expo

## Instalación de Dependencias
```bash
npm install axios react-native-async-storage @react-native-async-storage/async-storage
# O con Expo
expo install axios @react-native-async-storage/async-storage
```

## Configuración del Cliente API
```javascript
// services/apiClient.js
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'https://smart-condominium-backend.onrender.com';

class ApiClient {
    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 10000, // 10 segundos timeout
        });

        // Interceptor para agregar token
        this.client.interceptors.request.use(
            async (config) => {
                const token = await AsyncStorage.getItem('accessToken');
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
                return config;
            },
            (error) => Promise.reject(error)
        );

        // Interceptor para manejar respuestas
        this.client.interceptors.response.use(
            (response) => response,
            async (error) => {
                if (error.response?.status === 401) {
                    // Token expirado, intentar refrescar
                    await this.refreshToken();
                }
                return Promise.reject(error);
            }
        );
    }

    async refreshToken() {
        try {
            const refreshToken = await AsyncStorage.getItem('refreshToken');
            if (!refreshToken) {
                throw new Error('No refresh token');
            }

            const response = await axios.post(`${API_BASE_URL}/api/token/refresh/`, {
                refresh: refreshToken,
            });

            const { access } = response.data;
            await AsyncStorage.setItem('accessToken', access);
            
            return access;
        } catch (error) {
            // Redirect al login
            await this.logout();
            throw error;
        }
    }

    async logout() {
        await AsyncStorage.multiRemove(['accessToken', 'refreshToken', 'userData']);
        // Navegacion al login screen
    }
}

export default new ApiClient();
```

## Servicio de Autenticación
```javascript
// services/authService.js
import AsyncStorage from '@react-native-async-storage/async-storage';
import apiClient from './apiClient';

export class AuthService {
    async login(email, password) {
        try {
            const response = await apiClient.client.post('/api/token/', {
                email,
                password,
            });

            const { access, refresh } = response.data;
            
            // Guardar tokens
            await AsyncStorage.multiSet([
                ['accessToken', access],
                ['refreshToken', refresh],
            ]);

            // Obtener datos del usuario
            const userResponse = await apiClient.client.get('/api/administration/users/me/');
            await AsyncStorage.setItem('userData', JSON.stringify(userResponse.data));

            return {
                success: true,
                user: userResponse.data,
                tokens: { access, refresh }
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.detail || 'Error de conexión'
            };
        }
    }

    async logout() {
        await AsyncStorage.multiRemove(['accessToken', 'refreshToken', 'userData']);
    }

    async isLoggedIn() {
        const token = await AsyncStorage.getItem('accessToken');
        return !!token;
    }

    async getCurrentUser() {
        try {
            const userData = await AsyncStorage.getItem('userData');
            return userData ? JSON.parse(userData) : null;
        } catch {
            return null;
        }
    }
}

export default new AuthService();
```

## Componente de Login
```jsx
// screens/LoginScreen.js
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert, StyleSheet } from 'react-native';
import authService from '../services/authService';

export default function LoginScreen({ navigation }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async () => {
        if (!email || !password) {
            Alert.alert('Error', 'Por favor completa todos los campos');
            return;
        }

        setLoading(true);
        try {
            const result = await authService.login(email, password);
            
            if (result.success) {
                navigation.replace('Home');
            } else {
                Alert.alert('Error de Login', result.error);
            }
        } catch (error) {
            Alert.alert('Error', 'Error de conexión. Intenta nuevamente.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Smart Condominium</Text>
            
            <TextInput
                style={styles.input}
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
                autoCorrect={false}
            />
            
            <TextInput
                style={styles.input}
                placeholder="Contraseña"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />
            
            <TouchableOpacity 
                style={[styles.button, loading && styles.buttonDisabled]} 
                onPress={handleLogin}
                disabled={loading}
            >
                <Text style={styles.buttonText}>
                    {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
                </Text>
            </TouchableOpacity>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        padding: 20,
        backgroundColor: '#f5f5f5',
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        textAlign: 'center',
        marginBottom: 40,
        color: '#333',
    },
    input: {
        backgroundColor: 'white',
        paddingHorizontal: 15,
        paddingVertical: 12,
        borderRadius: 8,
        marginBottom: 15,
        fontSize: 16,
        borderWidth: 1,
        borderColor: '#ddd',
    },
    button: {
        backgroundColor: '#007AFF',
        paddingVertical: 15,
        borderRadius: 8,
        marginTop: 10,
    },
    buttonDisabled: {
        backgroundColor: '#cccccc',
    },
    buttonText: {
        color: 'white',
        textAlign: 'center',
        fontSize: 16,
        fontWeight: 'bold',
    },
});
```

## Servicio para Gestión de Reservas
```javascript
// services/reservationService.js
import apiClient from './apiClient';

export class ReservationService {
    async getMyReservations() {
        try {
            const response = await apiClient.client.get('/api/administration/reservations/');
            return {
                success: true,
                data: response.data
            };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Error obteniendo reservas'
            };
        }
    }

    async createReservation(reservationData) {
        try {
            const response = await apiClient.client.post('/api/administration/reservations/', {
                common_area: reservationData.commonAreaId,
                start_time: reservationData.startTime,
                end_time: reservationData.endTime,
                total_paid: reservationData.totalPaid,
            });

            return {
                success: true,
                data: response.data
            };
        } catch (error) {
            const errorMessage = error.response?.data?.non_field_errors?.[0] || 
                               error.response?.data?.error || 
                               'Error creando reserva';
            
            return {
                success: false,
                error: errorMessage
            };
        }
    }

    async getCommonAreas() {
        try {
            const response = await apiClient.client.get('/api/administration/common-areas/');
            return {
                success: true,
                data: response.data
            };
        } catch (error) {
            return {
                success: false,
                error: 'Error obteniendo áreas comunes'
            };
        }
    }
}

export default new ReservationService();
```

---

# 🎯 Flutter + Dart

## Dependencias en pubspec.yaml
```yaml
dependencies:
  flutter:
    sdk: flutter
  dio: ^5.3.2
  shared_preferences: ^2.2.2
  provider: ^6.0.5
```

## Cliente API con Dio
```dart
// lib/services/api_client.dart
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ApiClient {
  static const String baseUrl = 'https://smart-condominium-backend.onrender.com';
  late Dio _dio;
  
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;
  
  ApiClient._internal() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: Duration(seconds: 10),
      receiveTimeout: Duration(seconds: 10),
      headers: {'Content-Type': 'application/json'},
    ));

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final token = await _getToken();
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          await _refreshToken();
          // Retry request
          final options = error.requestOptions;
          final token = await _getToken();
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
            try {
              final response = await _dio.fetch(options);
              handler.resolve(response);
              return;
            } catch (e) {
              // Si falla el retry, continuar con el error
            }
          }
        }
        handler.next(error);
      },
    ));
  }

  Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token');
  }

  Future<void> _refreshToken() async {
    final prefs = await SharedPreferences.getInstance();
    final refreshToken = prefs.getString('refresh_token');
    
    if (refreshToken != null) {
      try {
        final response = await _dio.post('/api/token/refresh/', 
          data: {'refresh': refreshToken}
        );
        
        final newToken = response.data['access'];
        await prefs.setString('access_token', newToken);
      } catch (e) {
        // Refresh token inválido, logout
        await logout();
      }
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }

  Dio get dio => _dio;
}
```

## Modelo de Usuario
```dart
// lib/models/user.dart
class User {
  final int id;
  final String email;
  final String firstName;
  final String lastName;
  final String? phoneNumber;
  final int? role;
  final String? roleName;
  final bool isActive;
  final DateTime dateJoined;

  User({
    required this.id,
    required this.email,
    required this.firstName,
    required this.lastName,
    this.phoneNumber,
    this.role,
    this.roleName,
    required this.isActive,
    required this.dateJoined,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      phoneNumber: json['phone_number'],
      role: json['role'],
      roleName: json['role_name'],
      isActive: json['is_active'],
      dateJoined: DateTime.parse(json['date_joined']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'first_name': firstName,
      'last_name': lastName,
      'phone_number': phoneNumber,
      'role': role,
      'role_name': roleName,
      'is_active': isActive,
      'date_joined': dateJoined.toIso8601String(),
    };
  }

  String get fullName => '$firstName $lastName';
}
```

## Servicio de Autenticación
```dart
// lib/services/auth_service.dart
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user.dart';
import 'api_client.dart';

class AuthService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final response = await _apiClient.dio.post('/api/token/', data: {
        'email': email,
        'password': password,
      });

      final accessToken = response.data['access'];
      final refreshToken = response.data['refresh'];

      // Guardar tokens
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access_token', accessToken);
      await prefs.setString('refresh_token', refreshToken);

      // Obtener datos del usuario
      final userResponse = await _apiClient.dio.get('/api/administration/users/me/');
      final user = User.fromJson(userResponse.data);
      
      await prefs.setString('user_data', userResponse.data.toString());

      return {
        'success': true,
        'user': user,
      };
    } on DioException catch (e) {
      return {
        'success': false,
        'error': e.response?.data['detail'] ?? 'Error de conexión',
      };
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }

  Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.containsKey('access_token');
  }

  Future<User?> getCurrentUser() async {
    try {
      final response = await _apiClient.dio.get('/api/administration/users/me/');
      return User.fromJson(response.data);
    } catch (e) {
      return null;
    }
  }
}
```

## Screen de Login
```dart
// lib/screens/login_screen.dart
import 'package:flutter/material.dart';
import '../services/auth_service.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;

  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    final authService = AuthService();
    final result = await authService.login(
      _emailController.text.trim(),
      _passwordController.text,
    );

    setState(() => _isLoading = false);

    if (result['success']) {
      Navigator.pushReplacementNamed(context, '/home');
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(result['error'])),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Smart Condominium',
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              SizedBox(height: 48),
              TextFormField(
                controller: _emailController,
                decoration: InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
                keyboardType: TextInputType.emailAddress,
                validator: (value) {
                  if (value?.isEmpty ?? true) {
                    return 'Por favor ingresa tu email';
                  }
                  return null;
                },
              ),
              SizedBox(height: 16),
              TextFormField(
                controller: _passwordController,
                decoration: InputDecoration(
                  labelText: 'Contraseña',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
                validator: (value) {
                  if (value?.isEmpty ?? true) {
                    return 'Por favor ingresa tu contraseña';
                  }
                  return null;
                },
              ),
              SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _handleLogin,
                  child: _isLoading
                      ? CircularProgressIndicator()
                      : Text('Iniciar Sesión'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

---

# 🤖 Android Nativo (Kotlin)

## Dependencias en build.gradle
```kotlin
dependencies {
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.11.0'
    implementation 'androidx.security:security-crypto:1.1.0-alpha06'
}
```

## Clase de Cliente API
```kotlin
// ApiClient.kt
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import android.content.Context

class ApiClient private constructor() {
    companion object {
        private const val BASE_URL = "https://smart-condominium-backend.onrender.com/"
        
        @Volatile
        private var INSTANCE: ApiClient? = null
        
        fun getInstance(): ApiClient {
            return INSTANCE ?: synchronized(this) {
                INSTANCE ?: ApiClient().also { INSTANCE = it }
            }
        }
    }

    fun getApiService(context: Context): ApiService {
        val authInterceptor = Interceptor { chain ->
            val token = TokenManager.getToken(context)
            val request = if (token != null) {
                chain.request().newBuilder()
                    .addHeader("Authorization", "Bearer $token")
                    .build()
            } else {
                chain.request()
            }
            chain.proceed(request)
        }

        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BODY
        }

        val client = OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .addInterceptor(loggingInterceptor)
            .build()

        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        return retrofit.create(ApiService::class.java)
    }
}
```

## Interface de API
```kotlin
// ApiService.kt
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    @POST("api/token/")
    suspend fun login(@Body loginRequest: LoginRequest): Response<LoginResponse>

    @GET("api/administration/users/me/")
    suspend fun getCurrentUser(): Response<User>

    @GET("api/administration/reservations/")
    suspend fun getReservations(): Response<List<Reservation>>

    @POST("api/administration/reservations/")
    suspend fun createReservation(@Body reservation: CreateReservationRequest): Response<Reservation>

    @GET("api/administration/common-areas/")
    suspend fun getCommonAreas(): Response<List<CommonArea>>

    @POST("api/administration/vehicles/")
    suspend fun registerVehicle(@Body vehicle: CreateVehicleRequest): Response<Vehicle>
}

data class LoginRequest(
    val email: String,
    val password: String
)

data class LoginResponse(
    val access: String,
    val refresh: String
)
```

## Gestión de Tokens
```kotlin
// TokenManager.kt
import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKeys

object TokenManager {
    private const val PREFS_NAME = "secure_prefs"
    private const val ACCESS_TOKEN_KEY = "access_token"
    private const val REFRESH_TOKEN_KEY = "refresh_token"

    private fun getEncryptedPrefs(context: Context) = 
        EncryptedSharedPreferences.create(
            PREFS_NAME,
            MasterKeys.getOrCreate(MasterKeys.AES256_GCM_SPEC),
            context,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )

    fun saveTokens(context: Context, accessToken: String, refreshToken: String) {
        getEncryptedPrefs(context).edit()
            .putString(ACCESS_TOKEN_KEY, accessToken)
            .putString(REFRESH_TOKEN_KEY, refreshToken)
            .apply()
    }

    fun getToken(context: Context): String? {
        return getEncryptedPrefs(context).getString(ACCESS_TOKEN_KEY, null)
    }

    fun getRefreshToken(context: Context): String? {
        return getEncryptedPrefs(context).getString(REFRESH_TOKEN_KEY, null)
    }

    fun clearTokens(context: Context) {
        getEncryptedPrefs(context).edit().clear().apply()
    }
}
```

## Repository Pattern
```kotlin
// UserRepository.kt
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class UserRepository(private val apiService: ApiService) {

    suspend fun login(email: String, password: String): Result<LoginResponse> {
        return withContext(Dispatchers.IO) {
            try {
                val response = apiService.login(LoginRequest(email, password))
                if (response.isSuccessful) {
                    Result.success(response.body()!!)
                } else {
                    Result.failure(Exception("Login failed"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    }

    suspend fun getCurrentUser(): Result<User> {
        return withContext(Dispatchers.IO) {
            try {
                val response = apiService.getCurrentUser()
                if (response.isSuccessful) {
                    Result.success(response.body()!!)
                } else {
                    Result.failure(Exception("Failed to get user"))
                }
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
    }
}
```

---

# 📱 iOS Nativo (Swift)

## Dependencias (URLSession nativo)
```swift
// ApiClient.swift
import Foundation

class ApiClient {
    static let shared = ApiClient()
    private let baseURL = "https://smart-condominium-backend.onrender.com"
    private let session = URLSession.shared
    
    private init() {}
    
    private func createRequest(endpoint: String, method: HTTPMethod = .GET) -> URLRequest? {
        guard let url = URL(string: baseURL + endpoint) else { return nil }
        
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Agregar token si existe
        if let token = KeychainService.getToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        
        return request
    }
    
    func login(email: String, password: String) async throws -> LoginResponse {
        guard let request = createRequest(endpoint: "/api/token/", method: .POST) else {
            throw APIError.invalidURL
        }
        
        var modifiedRequest = request
        let loginData = LoginRequest(email: email, password: password)
        modifiedRequest.httpBody = try JSONEncoder().encode(loginData)
        
        let (data, response) = try await session.data(for: modifiedRequest)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.invalidResponse
        }
        
        return try JSONDecoder().decode(LoginResponse.self, from: data)
    }
    
    func getCurrentUser() async throws -> User {
        guard let request = createRequest(endpoint: "/api/administration/users/me/") else {
            throw APIError.invalidURL
        }
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.invalidResponse
        }
        
        return try JSONDecoder().decode(User.self, from: data)
    }
}

enum HTTPMethod: String {
    case GET = "GET"
    case POST = "POST"
    case PUT = "PUT"
    case DELETE = "DELETE"
    case PATCH = "PATCH"
}

enum APIError: Error {
    case invalidURL
    case invalidResponse
    case noData
}
```

## Modelos de Datos
```swift
// Models.swift
import Foundation

struct LoginRequest: Codable {
    let email: String
    let password: String
}

struct LoginResponse: Codable {
    let access: String
    let refresh: String
}

struct User: Codable {
    let id: Int
    let email: String
    let firstName: String
    let lastName: String
    let phoneNumber: String?
    let role: Int?
    let roleName: String?
    let isActive: Bool
    let dateJoined: String
    
    enum CodingKeys: String, CodingKey {
        case id, email, role
        case firstName = "first_name"
        case lastName = "last_name"
        case phoneNumber = "phone_number"
        case roleName = "role_name"
        case isActive = "is_active"
        case dateJoined = "date_joined"
    }
    
    var fullName: String {
        return "\(firstName) \(lastName)"
    }
}
```

## Servicio de Keychain
```swift
// KeychainService.swift
import Foundation
import Security

class KeychainService {
    static let accessTokenKey = "access_token"
    static let refreshTokenKey = "refresh_token"
    
    static func saveToken(_ token: String, key: String) {
        let data = token.data(using: .utf8)!
        
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data
        ]
        
        SecItemDelete(query as CFDictionary)
        SecItemAdd(query as CFDictionary, nil)
    }
    
    static func getToken(key: String = accessTokenKey) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]
        
        var dataTypeRef: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &dataTypeRef)
        
        if status == noErr, let data = dataTypeRef as? Data {
            return String(data: data, encoding: .utf8)
        }
        
        return nil
    }
    
    static func deleteToken(key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]
        
        SecItemDelete(query as CFDictionary)
    }
}
```

---

# 🧪 Testing de Endpoints

## Script de Testing en Python
```python
# test_api_endpoints.py
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://smart-condominium-backend.onrender.com"

class ApiTester:
    def __init__(self):
        self.token = None
        self.base_url = BASE_URL
        
    def login(self, email="admin@smartcondo.com", password="admin123"):
        """Login y obtener token"""
        response = requests.post(f"{self.base_url}/api/token/", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access"]
            print(f"✅ Login exitoso. Token obtenido.")
            return True
        else:
            print(f"❌ Login falló: {response.text}")
            return False
    
    def get_headers(self):
        """Headers con autorización"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def test_get_profile(self):
        """Probar obtener perfil"""
        response = requests.get(
            f"{self.base_url}/api/administration/users/me/",
            headers=self.get_headers()
        )
        
        print(f"GET /users/me/ -> {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Usuario: {data['first_name']} {data['last_name']}")
    
    def test_create_vehicle(self):
        """Probar crear vehículo"""
        vehicle_data = {
            "license_plate": f"TEST{datetime.now().strftime('%H%M%S')}",
            "brand": "Toyota",
            "model": "Camry",
            "color": "Azul"
        }
        
        response = requests.post(
            f"{self.base_url}/api/administration/vehicles/",
            headers=self.get_headers(),
            json=vehicle_data
        )
        
        print(f"POST /vehicles/ -> {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"  Vehículo creado: {data['license_plate']}")
            return data['id']
        else:
            print(f"  Error: {response.text}")
    
    def test_update_vehicle(self, vehicle_id):
        """Probar actualizar vehículo"""
        update_data = {
            "license_plate": f"UPD{datetime.now().strftime('%H%M%S')}",
            "brand": "Honda",
            "model": "Civic",
            "color": "Negro",
            "is_active": True
        }
        
        response = requests.put(
            f"{self.base_url}/api/administration/vehicles/{vehicle_id}/",
            headers=self.get_headers(),
            json=update_data
        )
        
        print(f"PUT /vehicles/{vehicle_id}/ -> {response.status_code}")
        if response.status_code == 200:
            print("  ✅ Vehículo actualizado")
        else:
            print(f"  ❌ Error: {response.text}")

if __name__ == "__main__":
    tester = ApiTester()
    
    if tester.login():
        tester.test_get_profile()
        vehicle_id = tester.test_create_vehicle()
        if vehicle_id:
            tester.test_update_vehicle(vehicle_id)
```

---

# 🔧 Tips de Optimización

## 1. Caching Estratégico
```javascript
// React Native - Implementar cache simple
class CacheService {
    static cache = new Map();
    static CACHE_DURATION = 5 * 60 * 1000; // 5 minutos

    static set(key, data) {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });
    }

    static get(key) {
        const cached = this.cache.get(key);
        if (!cached) return null;

        const isExpired = Date.now() - cached.timestamp > this.CACHE_DURATION;
        if (isExpired) {
            this.cache.delete(key);
            return null;
        }

        return cached.data;
    }
}
```

## 2. Retry Logic
```javascript
// Retry automático para requests fallidas
async function apiCallWithRetry(apiCall, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await apiCall();
        } catch (error) {
            if (attempt === maxRetries) throw error;
            
            const delay = Math.min(1000 * Math.pow(2, attempt), 10000);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}
```

## 3. Error Handling Centralizado
```javascript
class ApiErrorHandler {
    static handle(error) {
        switch (error.response?.status) {
            case 400:
                return 'Datos inválidos. Revisa la información enviada.';
            case 401:
                return 'Sesión expirada. Por favor inicia sesión nuevamente.';
            case 403:
                return 'No tienes permisos para realizar esta acción.';
            case 404:
                return 'El recurso solicitado no fue encontrado.';
            case 500:
                return 'Error interno del servidor. Intenta más tarde.';
            default:
                return 'Error de conexión. Verifica tu conexión a internet.';
        }
    }
}
```

---

*Documentación de integración móvil para Smart Condominium Backend*
*Actualizada: 24 de Septiembre de 2025*