# EDA E-Commerce Platform Documentación Técnica Completa 

| Atributo | Detalle |
|---|---|
| Version | 1.0.0 |
| Arquitectura | Event-Driven (EDA) |
| Stack principal | FastAPI, Kafka, PostgreSQL, Redis |
| Patron de diseño | Hexagonal + CQRS + Outbox Pattern |
| Infraestructura | Docker Compose (dev) / Kubernetes-ready |

## 1. Visión General del Sistema 

Este documento describe la arquitectura técnica completa de una plataforma de e-commerce construida con Event-Driven Architecture (EDA). El sistema está diseñado para ser altamente desacoplado, escalable y resiliente, donde cada dominio del negocio reacciona a eventos en lugar de llamadas síncronas directas. 

Principio clave: ningún servicio llama directamente a otro. Toda comunicación ocurre mediante eventos publicados en Apache Kafka. Esto garantiza desacoplamiento total entre dominios. 

### 1.1 Objetivos de negocio 
- Procesar pedidos de forma asíncrona y resiliente sin perder eventos ante fallos
- Escalar dominios de forma independiente según la carga (pagos, inventario, notificaciones)
- Mantener trazabilidad completa de todos los eventos del sistema
- Facilitar la incorporación de nuevos servicios sin modificar los existentes
- Garantizar consistencia eventual entre microservicios mediante el Outbox Pattern

### 1.2 Dominios del sistema

| Dominio | Responsabilidad | Tecnología |
|---|---|---|
| Users | Registro, autenticación y perfiles | FastAPI + JWT |
| Products | Catálogo, stock e imágenes | FastAPI + S3 |
| Orders | Ciclo de vida del pedido | FastAPI + Saga |
| Payments | Procesamiento de pagos | FastAPI + Stripe |
| Inventory | Control de stock en tiempo real | FastAPI + Redis |
| Notifications | Email, push y SMS | FastAPI + SMTP |
| Analytics | Métricas y reportes de negocio | FastAPI + TimescaleDB |

## 2. Arquitectura del Sistema 

### 2.1 Patrón arquitectónico: Hexagonal + EDA 
El sistema combina Arquitectura Hexagonal (Ports & Adapters) con Event-Driven Architecture. Cada dominio expone su lógica de negocio a través de puertos (interfaces Python puras), y los adaptadores concretos implementan la integración con Kafka, PostgreSQL o cualquier infraestructura externa. 

Regla de dependencia: el dominio no importa FastAPI, Kafka ni SQLAlchemy. Las dependencias apuntan siempre hacia adentro (hacia el dominio). Esto garantiza que la lógica de negocio es 100% testeable sin infraestructura. 

### 2.2 Diagrama de flujo de un evento 
Flujo completo cuando un cliente crea un pedido: 
1. Cliente hace POST \`/orders\` con su carrito
2. El endpoint de Orders valida el request con Pydantic
3. El Order Service ejecuta la lógica de negocio y persiste el pedido en PostgreSQL
4. Usando el Outbox Pattern, inserta un registro en la tabla outbox dentro de la misma transacción
5. Un worker de Kafka publica el evento `order.created` desde la tabla outbox
6. Inventory Service consume el evento y descuenta el stock
7. Payment Service consume el evento e inicia el cobro
8. Notifications Service consume el evento y envía el email de confirmación
9. Analytics Service consume el evento y registra la métrica

### 2.3 Patrones aplicados 

| Patrón | Dónde se aplica | Problema que resuelve |
|---|---|---|
| Outbox Pattern | Orders, Payments | Garantiza que el evento se publica si la DB persiste |
| Saga Coreográfica | Orders (flujo completo) | Coordina transacciones distribuidas sin orquestador |
| CQRS | Products, Analytics | Separa escrituras de lecturas para escalar cada una |
| Dead Letter Queue | Todos los consumers | Captura eventos fallidos para reintentar o auditar |
| Event Sourcing | Orders | El estado del pedido se reconstruye desde sus eventos |
| Circuit Breaker | Payment Service | Evita cascada de fallos hacia el gateway de pagos |

## 3. Estructura de Archivos del Proyecto 

### 3.1 Estructura raíz
```plaintext
eda-ecommerce/
├── services/                  # Un directorio por microservicio
│   ├── gateway/               # API Gateway (nginx o Traefik)
│   ├── users/                 # Servicio de usuarios
│   ├── products/              # Servicio de productos
│   ├── orders/                # Servicio de pedidos (core)
│   ├── payments/              # Servicio de pagos
│   ├── inventory/             # Servicio de inventario
│   ├── notifications/         # Servicio de notificaciones
│   └── analytics/             # Servicio de metricas
├── shared/                    # Librerias compartidas
│   ├── events/                # Schemas Pydantic de eventos
│   └── kafka/                 # Helpers producer/consumer
├── infra/                     # Infraestructura como codigo
│   ├── kafka/                 # Topics y configuracion
│   └── postgres/              # Scripts SQL iniciales
├── docker-compose.yml         # Entorno de desarrollo completo
├── docker-compose.test.yml    # Entorno de tests
└── Makefile                   # Comandos de desarrollo
```

## 4. Diseño de Base de Datos 

### 4.1 Estrategia de bases de datos 
Cada servicio tiene su propia base de datos PostgreSQL. Nunca comparten esquemas. La consistencia entre servicios se logra mediante eventos, no joins entre bases de datos. 

## 5. Catálogo de Eventos Kafka 

### 5.1 Tópicos y convenciones 
Convención de nombres: `{dominio}.{entidad}.{accion}`
Ejemplos: `order.order.created` | `payment.payment.completed` | `inventory.stock.depleted`

## 8. Lógica de Negocio 

### 8.1 Saga de creación de pedido (coreografía) 
- **Order Service**: crea el pedido en BD + inserta en outbox
- **Outbox Worker**: envía evento a Kafka `order.order.created`
- **Inventory Service**: reserva stock y emite `inventory.stock.reserved`
- **Payment Service**: cobra y emite `payment.payment.completed`
- **Order Service**: escucha reservas y pagos para cambiar estado a `PAID`
