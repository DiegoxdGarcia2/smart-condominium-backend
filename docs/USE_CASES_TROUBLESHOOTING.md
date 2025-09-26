# 🛠️ Smart Condominium - Casos de Uso y Troubleshooting

*Guía de casos de uso comunes y solución de problemas para desarrollo móvil*

---

# 🎯 Casos de Uso Comunes

## 1. 🏠 Flujo de Onboarding de Usuario

### Paso 1: Login
```javascript
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const { access, refresh } = await response.json();
            
            // Guardar tokens
            await AsyncStorage.multiSet([
                ['accessToken', access],
                ['refreshToken', refresh]
            ]);

            return { success: true };
        } else {
            const error = await response.json();
            return { success: false, error: error.detail };
        }
    } catch (error) {
        return { success: false, error: 'Error de conexión' };
    }
}
```

### Paso 2: Obtener Datos del Usuario
```javascript
async function fetchUserProfile() {
    try {
        const token = await AsyncStorage.getItem('accessToken');
        const response = await fetch(`${API_BASE_URL}/api/administration/users/me/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const userData = await response.json();
            
            // Guardar datos del usuario
            await AsyncStorage.setItem('userData', JSON.stringify(userData));
            
            return userData;
        }
    } catch (error) {
        console.error('Error fetching profile:', error);
        return null;
    }
}
```

### Paso 3: Configuración Inicial
```javascript
async function setupUserEnvironment(userData) {
    // Configurar notificaciones push
    await registerForPushNotifications(userData.id);
    
    // Pre-cargar datos críticos
    const [commonAreas, myVehicles, myPets] = await Promise.all([
        fetchCommonAreas(),
        fetchMyVehicles(),
        fetchMyPets()
    ]);
    
    // Guardar en cache local
    await AsyncStorage.multiSet([
        ['commonAreas', JSON.stringify(commonAreas)],
        ['myVehicles', JSON.stringify(myVehicles)],
        ['myPets', JSON.stringify(myPets)]
    ]);
}
```

---

## 2. 📅 Sistema de Reservas Completo

### Listar Áreas Disponibles
```javascript
async function getAvailableAreas(date, startTime, endTime) {
    try {
        // Obtener todas las áreas comunes
        const areasResponse = await apiClient.get('/api/administration/common-areas/');
        const allAreas = areasResponse.data;

        // Obtener reservas existentes para la fecha
        const reservationsResponse = await apiClient.get('/api/administration/reservations/', {
            params: {
                date: date.toISOString().split('T')[0], // YYYY-MM-DD
            }
        });
        const existingReservations = reservationsResponse.data;

        // Filtrar áreas disponibles
        const availableAreas = allAreas.filter(area => {
            if (!area.is_available) return false;

            // Verificar si hay conflictos de horario
            const hasConflict = existingReservations.some(reservation => {
                if (reservation.common_area !== area.id) return false;
                
                const resStart = new Date(reservation.start_time);
                const resEnd = new Date(reservation.end_time);
                
                return (startTime < resEnd && endTime > resStart);
            });

            return !hasConflict;
        });

        return availableAreas;
    } catch (error) {
        console.error('Error getting available areas:', error);
        return [];
    }
}
```

### Crear Reserva con Validación
```javascript
async function createReservation(areaId, startTime, endTime) {
    try {
        // Calcular costo
        const area = await getCommonAreaById(areaId);
        const duration = (endTime - startTime) / (1000 * 60 * 60); // horas
        const totalCost = duration * parseFloat(area.hourly_rate);

        const reservationData = {
            common_area: areaId,
            start_time: startTime.toISOString(),
            end_time: endTime.toISOString(),
            total_paid: totalCost.toFixed(2)
        };

        const response = await apiClient.post('/api/administration/reservations/', reservationData);

        if (response.status === 201) {
            // Actualizar cache local
            await updateLocalReservations();
            
            return {
                success: true,
                reservation: response.data,
                message: 'Reserva creada exitosamente'
            };
        }
    } catch (error) {
        if (error.response?.data?.non_field_errors) {
            return {
                success: false,
                error: error.response.data.non_field_errors[0]
            };
        }
        
        return {
            success: false,
            error: 'Error creando la reserva. Intenta nuevamente.'
        };
    }
}
```

---

## 3. 💳 Integración de Pagos con Stripe

### Iniciar Proceso de Pago
```javascript
async function initiatePayment(financialFeeId) {
    try {
        const response = await apiClient.post('/api/administration/payments/initiate_payment/', {
            financial_fee_id: financialFeeId
        });

        const { payment_url, transaction_id, existing } = response.data;

        if (existing) {
            // Mostrar mensaje sobre transacción pendiente
            Alert.alert(
                'Pago Pendiente',
                'Ya tienes un pago en proceso para esta cuota. ¿Deseas continuar?',
                [
                    { text: 'Cancelar', style: 'cancel' },
                    { text: 'Continuar', onPress: () => openPaymentUrl(payment_url) }
                ]
            );
        } else {
            // Nuevo pago
            openPaymentUrl(payment_url);
        }

        return { transaction_id, payment_url };
    } catch (error) {
        Alert.alert(
            'Error de Pago',
            error.response?.data?.error || 'No se pudo iniciar el pago'
        );
        throw error;
    }
}

function openPaymentUrl(url) {
    // React Native
    Linking.openURL(url);
    
    // O usar WebView personalizada
    navigation.navigate('PaymentWebView', { url });
}
```

### Verificar Estado de Pago
```javascript
async function checkPaymentStatus(transactionId) {
    try {
        const response = await apiClient.get('/api/administration/payments/', {
            params: { transaction_id: transactionId }
        });

        const transactions = response.data;
        const transaction = transactions.find(t => t.transaction_id === transactionId);

        if (transaction) {
            switch (transaction.status) {
                case 'Completado':
                    return { status: 'completed', message: 'Pago completado exitosamente' };
                case 'Fallido':
                    return { status: 'failed', message: 'El pago falló. Intenta nuevamente.' };
                case 'Pendiente':
                case 'Procesando':
                    return { status: 'pending', message: 'Pago en proceso...' };
                default:
                    return { status: 'unknown', message: 'Estado desconocido' };
            }
        }

        return { status: 'not_found', message: 'Transacción no encontrada' };
    } catch (error) {
        return { status: 'error', message: 'Error verificando el pago' };
    }
}
```

---

## 4. 🚗 Gestión de Vehículos y Mascotas

### Registrar Vehículo con Validación
```javascript
async function registerVehicle(vehicleData) {
    try {
        // Validación local
        const validation = validateVehicleData(vehicleData);
        if (!validation.isValid) {
            return { success: false, errors: validation.errors };
        }

        const response = await apiClient.post('/api/administration/vehicles/', {
            license_plate: vehicleData.licensePlate.toUpperCase(),
            brand: vehicleData.brand,
            model: vehicleData.model,
            color: vehicleData.color
        });

        if (response.status === 201) {
            // Actualizar lista local
            await refreshMyVehicles();
            
            return {
                success: true,
                vehicle: response.data,
                message: 'Vehículo registrado exitosamente'
            };
        }
    } catch (error) {
        if (error.response?.status === 400) {
            const serverErrors = error.response.data;
            
            // Manejar error de placa duplicada
            if (serverErrors.license_plate) {
                return {
                    success: false,
                    error: 'Esta placa ya está registrada en el sistema'
                };
            }
            
            return {
                success: false,
                error: 'Datos inválidos. Revisa la información ingresada.',
                details: serverErrors
            };
        }
        
        return {
            success: false,
            error: 'Error registrando el vehículo. Intenta nuevamente.'
        };
    }
}

function validateVehicleData(data) {
    const errors = {};
    
    if (!data.licensePlate || data.licensePlate.trim().length < 3) {
        errors.licensePlate = 'La placa debe tener al menos 3 caracteres';
    }
    
    if (!data.brand || data.brand.trim().length === 0) {
        errors.brand = 'La marca es requerida';
    }
    
    if (!data.model || data.model.trim().length === 0) {
        errors.model = 'El modelo es requerido';
    }
    
    return {
        isValid: Object.keys(errors).length === 0,
        errors
    };
}
```

---

## 5. 👥 Sistema de Visitantes

### Registrar Visitante con QR
```javascript
async function registerVisitor(visitorData) {
    try {
        const response = await apiClient.post('/api/administration/visitor-logs/', {
            visitor_name: visitorData.name,
            visitor_id: visitorData.idDocument,
            unit_visited: visitorData.unitId,
            purpose: visitorData.purpose,
            expected_duration: visitorData.expectedHours
        });

        if (response.status === 201) {
            const visitor = response.data;
            
            // Generar código QR para salida rápida
            const qrData = {
                type: 'visitor_exit',
                visitor_log_id: visitor.id,
                entry_time: visitor.entry_time,
                visitor_name: visitor.visitor_name
            };
            
            return {
                success: true,
                visitor: visitor,
                qrCode: JSON.stringify(qrData),
                message: 'Visitante registrado. Guarda el código QR para la salida.'
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error.response?.data?.error || 'Error registrando visitante'
        };
    }
}

async function processVisitorExit(qrCodeData) {
    try {
        const data = JSON.parse(qrCodeData);
        
        if (data.type !== 'visitor_exit') {
            return { success: false, error: 'Código QR inválido' };
        }

        const response = await apiClient.post(
            `/api/administration/visitor-logs/${data.visitor_log_id}/register_exit/`
        );

        if (response.status === 200) {
            return {
                success: true,
                message: `Salida registrada para ${data.visitor_name}`
            };
        }
    } catch (error) {
        return {
            success: false,
            error: 'Error procesando la salida del visitante'
        };
    }
}
```

---

# 🚨 Troubleshooting Común

## 1. Error 401 - Token Inválido

### Problema
```
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

### Solución
```javascript
async function handleTokenExpired() {
    try {
        const refreshToken = await AsyncStorage.getItem('refreshToken');
        
        if (!refreshToken) {
            // No hay refresh token, redirect al login
            await AsyncStorage.clear();
            navigation.navigate('Login');
            return;
        }

        // Intentar refrescar el token
        const response = await fetch(`${API_BASE_URL}/api/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (response.ok) {
            const { access } = await response.json();
            await AsyncStorage.setItem('accessToken', access);
            
            // Reintentar la request original
            return true;
        } else {
            // Refresh token también inválido
            await AsyncStorage.clear();
            navigation.navigate('Login');
            return false;
        }
    } catch (error) {
        console.error('Error refreshing token:', error);
        await AsyncStorage.clear();
        navigation.navigate('Login');
        return false;
    }
}
```

## 2. Error 400 - Datos de Validación

### Problema
```json
{
    "license_plate": ["Este campo debe ser único."],
    "start_time": ["La fecha de inicio no puede ser en el pasado."]
}
```

### Solución
```javascript
function handleValidationErrors(errors) {
    const messages = [];
    
    Object.keys(errors).forEach(field => {
        const fieldErrors = Array.isArray(errors[field]) ? errors[field] : [errors[field]];
        
        fieldErrors.forEach(error => {
            // Traducir nombres de campos
            const fieldName = translateFieldName(field);
            messages.push(`${fieldName}: ${error}`);
        });
    });

    return messages.join('\n');
}

function translateFieldName(field) {
    const translations = {
        'license_plate': 'Placa',
        'start_time': 'Fecha de inicio',
        'end_time': 'Fecha de fin',
        'common_area': 'Área común',
        'visitor_name': 'Nombre del visitante',
        'financial_fee_id': 'Cuota financiera'
    };
    
    return translations[field] || field;
}
```

## 3. Error de Conexión

### Problema
```javascript
// Network request failed
// TypeError: Network request failed
```

### Solución con Retry
```javascript
async function apiCallWithRetry(apiCall, maxRetries = 3) {
    let lastError;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await apiCall();
        } catch (error) {
            lastError = error;
            
            if (attempt === maxRetries) break;
            
            // Esperar antes del próximo intento (exponential backoff)
            const delay = Math.min(1000 * Math.pow(2, attempt - 1), 5000);
            await new Promise(resolve => setTimeout(resolve, delay));
            
            console.log(`Retry attempt ${attempt + 1}/${maxRetries} in ${delay}ms`);
        }
    }
    
    throw lastError;
}

// Uso
try {
    const result = await apiCallWithRetry(async () => {
        return await apiClient.get('/api/administration/users/me/');
    });
} catch (error) {
    showNetworkError();
}
```

## 4. Problemas con Stripe Checkout

### URL de Pago Inválida
```javascript
async function validateStripeUrl(url) {
    // Verificar que la URL sea de Stripe y esté bien formada
    const stripePattern = /^https:\/\/checkout\.stripe\.com\/c\/pay\/cs_[a-zA-Z0-9]+/;
    
    if (!stripePattern.test(url)) {
        throw new Error('URL de pago inválida. Contacta al administrador.');
    }
    
    return url;
}

async function handlePaymentUrl(paymentUrl) {
    try {
        const validUrl = await validateStripeUrl(paymentUrl);
        
        // Abrir en WebView o navegador
        if (Platform.OS === 'ios') {
            Linking.openURL(validUrl);
        } else {
            // Android - usar WebView personalizada
            navigation.navigate('PaymentWebView', { url: validUrl });
        }
    } catch (error) {
        Alert.alert('Error', error.message);
    }
}
```

## 5. Sincronización de Datos

### Cache Inconsistente
```javascript
class DataSyncManager {
    static async syncUserData() {
        try {
            const [profile, vehicles, pets, reservations] = await Promise.all([
                apiClient.get('/api/administration/users/me/'),
                apiClient.get('/api/administration/vehicles/'),
                apiClient.get('/api/administration/pets/'),
                apiClient.get('/api/administration/reservations/')
            ]);

            // Actualizar cache local
            await AsyncStorage.multiSet([
                ['userData', JSON.stringify(profile.data)],
                ['myVehicles', JSON.stringify(vehicles.data)],
                ['myPets', JSON.stringify(pets.data)],
                ['myReservations', JSON.stringify(reservations.data)],
                ['lastSync', Date.now().toString()]
            ]);

            return { success: true };
        } catch (error) {
            console.error('Sync failed:', error);
            return { success: false, error: error.message };
        }
    }

    static async shouldSync() {
        try {
            const lastSync = await AsyncStorage.getItem('lastSync');
            if (!lastSync) return true;

            const lastSyncTime = parseInt(lastSync);
            const now = Date.now();
            const fiveMinutes = 5 * 60 * 1000;

            return (now - lastSyncTime) > fiveMinutes;
        } catch {
            return true;
        }
    }
}
```

---

# 📊 Monitoring y Analytics

## Logging de Errores
```javascript
class ErrorLogger {
    static log(error, context) {
        const errorData = {
            timestamp: new Date().toISOString(),
            message: error.message,
            stack: error.stack,
            context: context,
            userId: getCurrentUserId(),
            platform: Platform.OS,
            version: getAppVersion()
        };

        // Enviar a servicio de logging (ej: Crashlytics, Sentry)
        console.error('App Error:', errorData);
        
        // También guardar localmente para debug
        this.saveLocalError(errorData);
    }

    static async saveLocalError(errorData) {
        try {
            const errors = await AsyncStorage.getItem('localErrors') || '[]';
            const errorList = JSON.parse(errors);
            
            errorList.push(errorData);
            
            // Mantener solo los últimos 50 errores
            const recentErrors = errorList.slice(-50);
            
            await AsyncStorage.setItem('localErrors', JSON.stringify(recentErrors));
        } catch (e) {
            console.error('Failed to save error locally:', e);
        }
    }
}
```

## Métricas de Performance
```javascript
class PerformanceMonitor {
    static startTimer(operation) {
        const startTime = Date.now();
        
        return {
            end: () => {
                const duration = Date.now() - startTime;
                this.logMetric(operation, duration);
                return duration;
            }
        };
    }

    static logMetric(operation, duration) {
        const metric = {
            operation,
            duration,
            timestamp: new Date().toISOString()
        };

        console.log(`Performance: ${operation} took ${duration}ms`);
        
        // Enviar a analytics
        // Analytics.track('api_call_duration', metric);
    }
}

// Uso
const timer = PerformanceMonitor.startTimer('login_request');
try {
    await authService.login(email, password);
} finally {
    timer.end();
}
```

---

# 🔍 Testing y QA

## Test de Endpoints
```javascript
// __tests__/api.test.js
import ApiClient from '../services/apiClient';

describe('API Integration Tests', () => {
    let apiClient;
    let authToken;

    beforeAll(async () => {
        apiClient = new ApiClient();
        
        // Login para obtener token
        const loginResult = await apiClient.login('test@example.com', 'password123');
        expect(loginResult.success).toBe(true);
        authToken = loginResult.token;
    });

    test('should get user profile', async () => {
        const result = await apiClient.getCurrentUser();
        expect(result.success).toBe(true);
        expect(result.data).toHaveProperty('email');
    });

    test('should create and delete vehicle', async () => {
        const vehicleData = {
            licensePlate: 'TEST123',
            brand: 'Toyota',
            model: 'Test',
            color: 'Blue'
        };

        // Crear
        const createResult = await apiClient.createVehicle(vehicleData);
        expect(createResult.success).toBe(true);
        
        const vehicleId = createResult.data.id;
        
        // Eliminar
        const deleteResult = await apiClient.deleteVehicle(vehicleId);
        expect(deleteResult.success).toBe(true);
    });
});
```

---

*Guía de casos de uso y troubleshooting para Smart Condominium Backend*
*Última actualización: 24 de Septiembre de 2025*