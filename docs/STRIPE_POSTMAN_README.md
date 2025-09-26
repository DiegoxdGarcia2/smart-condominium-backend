SmartCondominium - Colección Postman: Stripe Payments (Sandbox)

Objetivo
- Probar la pasarela de pagos basada en Stripe en modo sandbox/test.
- Incluir pasos para obtener tokens JWT, crear sesión de Checkout y simular webhooks firmados.

Requisitos
- Backend corriendo localmente o en un entorno accesible. Ajusta `base_url` en el environment.
- STRIPE_SECRET_KEY y STRIPE_WEBHOOK_SECRET configurados en las variables de entorno del servidor.
- Una `FinancialFee` existente en la base de datos (usa `financial_fee_id` en el environment).
- Usuario con credenciales en el environment (`email`/`password`).

Colección
- `Auth - Obtener JWT (POST /api/token/)` — obtiene `access_token` y `refresh_token` y los guarda en el environment.
- `Initiate Payment` — hay dos variantes: la ruta directa `initiate-payment/` y la registrada en el router `payments/initiate_payment/`. Ambas requieren Authorization Bearer y `financial_fee_id` en el JSON.
- `Get My Payments` — lista las transacciones del usuario autenticado.
- `Payment Webhook (signed)` — pre-request construye un payload de tipo `checkout.session.completed` y calcula una cabecera `Stripe-Signature` compatible con la verificación HMAC-SHA256 usando `stripe_webhook_secret` del environment. Envía el webhook al endpoint.

Cómo usar
1. Importa la colección `postman/Stripe_Payments.postman_collection.json` en Postman.
2. Importa el environment `postman/Stripe_Payments.environment.json`.
3. Ajusta `base_url` (por ejemplo `http://localhost:8000` o la URL de Render).
4. Ajusta `stripe_webhook_secret` en el environment por el valor real de tu Stripe test webhook secret (o el valor que tengas en `STRIPE_WEBHOOK_SECRET`).
5. Ejecuta la petición `Auth - Obtener JWT`.
6. Ejecuta `Initiate Payment` (cualquiera de las dos rutas) para crear una sesión de checkout; la respuesta debe contener `payment_url`.
7. Usa `Payment Webhook (signed)` para simular que Stripe notificó la sesión completada. El pre-request script generará el payload y la cabecera `Stripe-Signature` automáticamente.

Notas y limitaciones
- La implementación espera metadata con `financial_fee_id` y `resident_id` dentro de la sesión de Checkout. El webhook simulado respeta esto.
- El script de Postman construye la firma usando CryptoJS (disponible en el sandbox de Postman). Asegúrate de que `stripe_webhook_secret` sea el mismo que `STRIPE_WEBHOOK_SECRET` configurado en el backend para que la verificación pase.
- Si tu backend usa moneda distinta a USD, ajusta la creación de sesión en `administration/views.py` o en la petición `Initiate Payment`.
- En producción usa claves reales y URL real del frontend en `FRONTEND_URL`.

Siguientes pasos recomendados
- Añadir ejemplos de respuestas esperadas en tests de Postman.
- (Opcional) Añadir collection runner o Newman para integración continua.

