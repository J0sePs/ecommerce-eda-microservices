# Resumen Ejecutivo: Implementación de Arquitectura Orientada a Eventos (EDA)

## Introducción
La Arquitectura Orientada a Eventos (Event-Driven Architecture o EDA) es un paradigma de diseño de software centrado en la producción, detección, consumo y reacción a eventos (cambios de estado o sucesos notables en el sistema). El presente proyecto implementa un sistema backend de E-Commerce utilizando este patrón para lograr un alto rendimiento, robustez, escalabilidad y un bajo nivel de acoplamiento entre sus distintos componentes de dominio.

## Motivación y Objetivo del Proyecto
Las arquitecturas tradicionales (monolíticas o microservicios que se comunican exclusivamente vía llamadas REST/HTTP síncronas) a menudo sufren de "acoplamiento temporal". Esto significa que si un sistema A necesita al sistema B para completar una transacción, y B está inoperativo, A también falla o se bloquea. 

El objetivo principal de este proyecto es desglosar un sistema de comercio electrónico en dominios independientes (Orders, Inventory, Payments, Notifications) comunicados de forma **asíncrona** a través de un bus o broker de eventos. Así, si el microservicio de notificaciones cae, las órdenes de los clientes se siguen registrando sin bloqueos ni pérdida de operaciones.

## Tecnologías Principales y su Rol
- **Apache Kafka:** Actúa como el Event Broker, la columna vertebral central del ecosistema. Provee partición, distribución y una enorme capacidad para almacenar los eventos garantizando su posterior entrega. A diferencia de las colas tradicionales, Kafka funciona como un *append-only log* distribuido, garantizando retención a largo plazo.
- **Python (Micro-framewok FastAPI):** Utilizado para construir microservicios rápidos, fácilmente extensibles y robustos para cada servicio independiente de nuestro dominio.
- **Micro-bases de datos aisladas (PostgreSQL):** Siguiendo el principio de bases de datos por microservicio, garantizando que el único puente de comunicación entre servicios sean los eventos en Kafka, no las bases de datos compartidas.
- **Docker & Docker Compose:** Contenedores que garantizan paridad entre el desarrollo local y el entorno de despliegue, montando rápidamente servicios paralelos.

## Flujo Lógico y Beneficios Obtenidos
El sistema reacciona en cadena a sucesos concretos. Cuando la API recibe una petición para comprar un artículo, se inyecta en Kafka un evento: `OrderCreated`. Esto desata la arquitectura en tiempo real:
1. El servicio `Inventory` consume el evento, evalúa el stock y lanza `InventoryReserved`.
2. El servicio `Payments` analiza las intenciones de pago en paralelo.
3. El servicio `Notifications` espera la resolución para enviar el correo digital a la persona involucrada.

### Conclusión
La implementación de un ecosistema EDA ha comprobado separar drásticamente las responsabilidades temporales y lógicas del negocio. El despliegue a través de microservicios e infraestructura de colas de alto rendimiento (Kafka) resulta ser indispensable para empresas modernas que requieren procesar transacciones sin cuellos de botella sincronizados y tolerando fallos parciales sin afectar la experiencia principal del usuario.
