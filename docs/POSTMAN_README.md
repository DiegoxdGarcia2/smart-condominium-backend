# Postman - SmartCondominium

Esta carpeta contiene una colección y un environment para probar la API del backend SmartCondominium.

Archivos:

- `postman/SmartCondominium.postman_collection.json` - Colección Postman con requests para autenticación (JWT) y endpoints comunes (usuarios, pagos).
- `postman/SmartCondominium.postman_environment.json` - Environment con variables: `base_url`, `email`, `password`, `access_token`, `refresh_token`, `financial_fee_id`, `stripe_signature`.

Cómo usar:

1. Importa la colección y el environment en Postman.
2. Selecciona el environment "SmartCondominium - Production".
3. Ejecuta la request "Auth -> Login - Obtain JWT".
   - Si el login es exitoso, en la pestaña Tests la colección almacenará `access_token` y `refresh_token` en el environment.
4. Ejecuta "Administration -> List Users" para verificar una petición protegida. Debería devolver 200 y listar usuarios.
5. Para probar el flujo de pagos:
   - Rellena la variable `financial_fee_id` con un id válido y ejecuta "Initiate Payment" (POST).
   - Para el webhook, añade en `stripe_signature` una firma válida si pruebas una webhook real. De lo contrario, la ruta devolverá 400 con "Firma inválida" (comportamiento esperado).

Notas:

- Por seguridad, cambia `email` y `password` si usas credenciales reales.
- Si vas a ejecutar tests automatizados, puedes usar `newman` para ejecutar la colección desde la línea de comandos.

Ejecutar con newman (opcional):

```bash
# Instalar newman
npm install -g newman
# Ejecutar colección con environment
newman run postman/SmartCondominium.postman_collection.json -e postman/SmartCondominium.postman_environment.json
```

Si quieres, puedo añadir un script que ejecute la colección con newman o un script Python que use `requests` para validar endpoints en CI.
