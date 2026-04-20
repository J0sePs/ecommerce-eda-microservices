# Arquitectura del Proyecto

Este proyecto implementa una **Arquitectura Orientada a Eventos (EDA - Event-Driven Architecture)** como base de diseño de sistema. La solución desglosa un e-commerce tradicional en un conjunto de microservicios que utilizan un *Broker de Eventos* (Kafka) como bus principal de comunicación.

## Principios Arquitectónicos Implementados

### 1. Desacoplamiento de Servicios
Los subdominios del negocio (`Orders`, `Inventory`, `Payments`, `Notifications`) han sido construidos como entidades total y lógicamente independientes. A diferencia de arquitecturas cliente-servidor clásicas, aquí ningún servicio invoca directamente a otro mediante llamadas de red síncronas HTTP/REST (por ejemplo, el servicio de Órdenes no realiza una petición a Inventario bajo demanda directa). En su lugar, operan mediante el modelo Pub/Sub, **emitiendo eventos** en el bus central bajo una lógica asíncrona.

### 2. Base de Datos por Microservicio (Polyglot Persistence Pattern)
Para garantizar la independencia estricta y evitar cuellos de botella de bloqueo de tablas comunes:
- Cada servicio de dominio domina y maneja en exclusiva su correspondiente base de datos.
- Se restringe absolutamente que algún servicio cruce la frontera para consultar la base de datos de un tercero.
- Toda información compartida o necesitada por los consumidores viaja incrustada en la misma carga útil (Payload) adjunta a sus eventos (Event-carried State Transfer), favoreciendo la meta de alcanzar una *consistencia eventual* (Eventual Consistency) del ecosistema general.

### 3. Procesamiento Paralelo y Asíncrono
De cara a la experiencia del cliente final, los procesos que tardan en resolverse operan de fondo (en *Background*). La API de generación de órdenes es capaz de registrar la solicitud inmediatamente (respondiendo `HTTP 202 Accepted`) mientras los servicios dependientes auditan el stock y procesan tarjetas concurrentemente mediante el Event Broker. 

## Componentes y Tecnologías de la Solución

1. **Apache Kafka (Event Broker):** Componente crucial. Es la columna vertebral del desacoplamiento. Funciona como un bitácora secuencial (commit log) distribuido, recogiendo masivamente los datos emitidos por un "Productor", almacenándolos ordenadamente y despachándolos hacia múltiples sistemas "Consumidores".
2. **FastAPI (Python):** El framework ágil implementado para diseñar y montar velozmente las APIs de cada microservicio, procesar datos y enlazar la base computacional conectando productores a Kafka.
3. **PostgreSQL:** El motor relacional individual por servicio elegido para garantizar la integridad e historial persistente (Orders info, Stock items).
4. **Docker & Docker Compose:** Permite "conteinerizar" todos los actores. En EDA, como existen muchas piezas aisladas, Docker orquesta automáticamente Kafka, Zookeeper, múltiples bases de datos y la instancia de Python individual por microservicio dentro de una misma red perimetral virtual.

## Modelo de Transacciones Distribuidas (Saga Pattern)
A fin de resolver la problemática tradicional de *"¿Qué ocurre cuando falla un subsistema en un entorno desacoplado y sin rollback central?"*:

Se aplica el principio coreográfico del **Patrón Saga**. De forma ilustrativa, si ocurre un fracaso posterior a una inserción (como falta repentina de stock después de aceptarse la orden), dicho servicio difunde proactivamente su estatus fallido como un nuevo evento oficial (`InventoryFailed`). Los demás servicios en la cadena consumen esta notificación de fracaso, implementando rutinas defensivas de compensación, como cancelar un cobro parcial o actualizar el estado base temporal de la orden a `CANCELLED`, equilibrando el balance universal del sistema sin romper las operaciones.