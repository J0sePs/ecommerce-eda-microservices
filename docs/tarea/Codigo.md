# Código Fuente del Proyecto

El código fuente de este proyecto implementa una Arquitectura Orientada a Eventos (EDA) aplicada a un sistema de comercio electrónico estructurado en microservicios.

## URL del Repositorio
* **Link de GitHub:** [Insertar enlace del repositorio aquí]

## Estructura Principal
El proyecto está dividido en varios microservicios independientes que se comunican exclusivamente a través de mensajes (eventos):

- `services/orders/`: Gestión de la creación y estado de pedidos. Emite eventos cuando un usuario compra algo.
- `services/inventory/`: Verifica el stock de los productos. Escucha órdenes creadas y reserva stock.
- `services/payments/`: Simula el procesamiento de pagos.
- `services/notifications/`: Servicio final que alerta al usuario mediante correos electrónicos simulados basándose en eventos del sistema (ej. "Pago aprobado", "Orden enviada").
- `shared/`: Contiene infraestructura compartida como esquemas base para eventos de Kafka, y clases de Productores/Consumidores que todos los servicios reutilizan.
- `infra/`: Configuraciones de Apache Kafka y PostgreSQL.

## Ejecución (Cómo probarlo)
Al tener el motor de base de datos, el orquestador de eventos (Kafka) y varios microservicios, el sistema ha sido contenedorizado usando Docker para fácil revisión. 

Ejecuta el siguiente comando en la raíz del proyecto:
```bash
docker-compose up -d --build
```
Esto levantará toda la infraestructura y los servicios listos para interactuar a través de sus rutas API (Swagger en `/docs`).
