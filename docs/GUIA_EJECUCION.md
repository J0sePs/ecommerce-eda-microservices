# Guía de Ejecución y Puertos (EDA System)

Esta guía contiene todo lo que necesitas saber para levantar, probar y detener tu aplicación basada en arquitectura orientada a eventos (EDA) en cualquier momento.

## 🚀 1. Cómo iniciar la aplicación

Abre tu terminal en la raíz del proyecto (la carpeta `EDA`) y ejecuta el siguiente comando para levantar toda la infraestructura (Bases de datos, Kafka, Redis, etc.) y los microservicios en segundo plano:

```bash
docker compose up -d
```

*(Opcional) Si en el futuro agregas nuevas dependencias o cambias los Dockerfiles, puedes forzar la reconstrucción de las imágenes con:*
```bash
docker compose up -d --build
```

---

## 🛑 2. Cómo detener la aplicación

Para apagar de forma segura todos los contenedores y liberar los puertos de tu máquina, ejecuta:

```bash
docker compose down
```

*Nota: Esto **no** borra los datos de las bases de datos (están persistidos en los volúmenes). Si alguna vez quieres reiniciar todo desde cero (borrar datos), usa `docker compose down -v`.*

---

## 🌐 3. URLs y Puertos de la Infraestructura

Una vez que los contenedores estén corriendo, puedes acceder a las herramientas visuales desde tu navegador:

*   **Kafka UI (Gestión de Mensajes):** [http://localhost:8110](http://localhost:8110)
    *Aquí puedes ver los tópicos, los mensajes fluyendo entre microservicios, grupos de consumidores, etc.*
*   **MailHog (Simulador de Emails):** [http://localhost:8055](http://localhost:8055)
    *Bandeja de entrada local para ver los correos que envía el servicio de notificaciones.*
*   **MinIO Console (Almacenamiento S3 local):** [http://localhost:9031](http://localhost:9031)
    *Usado por el servicio de Productos. (User: `admin` / Password: `password`)*

---

## 📖 4. Documentación de las APIs (Swagger UI)

Cada microservicio interactúa de forma independiente y tiene su propia interfaz de Swagger. Ingresa a las siguientes URLs para ver los endpoints y probar peticiones HTTP:

*   📦 **Orders Service:** [http://localhost:8031/docs](http://localhost:8031/docs)
*   👤 **Users Service:** [http://localhost:8032/docs](http://localhost:8032/docs)
*   🛍️ **Products Service:** [http://localhost:8033/docs](http://localhost:8033/docs)
*   💳 **Payments Service:** [http://localhost:8034/docs](http://localhost:8034/docs)
*   🏭 **Inventory Service:** [http://localhost:8035/docs](http://localhost:8035/docs)
*   ✉️ **Notifications Service:** [http://localhost:8036/docs](http://localhost:8036/docs)
*   📊 **Analytics Service:** [http://localhost:8037/docs](http://localhost:8037/docs)

---

## 🛠️ 5. Cómo probar el flujo completo (Ejemplo)

Para ver el sistema en acción (Patrón Outbox + Kafka), dirígete al Swagger de **Orders Service** ([http://localhost:8031/docs](http://localhost:8031/docs)). 

1. Abre el endpoint `POST /api/v1/orders/`.
2. Dale a **"Try it out"**.
3. Pega este JSON correcto de prueba:

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "items": [
    {
      "product_id": "123e4567-e89b-12d3-a456-426614174000",
      "product_name": "Widget",
      "sku": "WIDGET-1",
      "unit_price": 99.99,
      "quantity": 10
    }
  ],
  "shipping_address": {
    "street": "123 Main St",
    "city": "Anytown",
    "country": "USA",
    "state": "CA",
    "zip_code": "12345"
  }
}
```

4. Haz click en **Execute**.
5. Revisa [Kafka UI](http://localhost:8110) bajo el tópico `order.order.created`. Deberías ver un mensaje nuevo publicado automáticamente con los datos de tu orden.

---

## 🐛 6. Ver Logs (Solución de problemas)

Si algo no funciona o quieres ver el output de un servicio específico usando la terminal:

Para ver todos los logs juntos:
```bash
docker compose logs -f
```

Para ver los logs de un servicio específico (ej: orders-service):
```bash
docker compose logs -f orders-service
```
*(Presiona `Ctrl+C` para salir del visor de logs).*
