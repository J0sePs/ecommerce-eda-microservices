# E-Commerce: Arquitectura Orientada a Eventos (EDA) 🚀

Este proyecto es una implementación práctica de una **Arquitectura Orientada a Eventos (Event-Driven Architecture)** para un sistema de comercio electrónico (E-Commerce), diseñada con microservicios independientes y altamente escalables.

## 🏗️ Sobre la Arquitectura

En lugar de tener servicios que se acoplan mediante peticiones HTTP/REST síncronas que se bloquean esperando respuestas, este sistema utiliza **Apache Kafka** como un *Event Broker* central. Cada microservicio es un actor autónomo que emite "Eventos" (hechos en el pasado) al bus de mensajes y reacciona de forma asíncrona a los eventos que le interesan.

**Características principales:**
- 🧩 **Desacoplamiento Total:** Los microservicios no se comunican directamente entre sí.
- 🗄️ **Base de Datos por Servicio:** Cada servicio maneja su propia base de datos (Polyglot Persistence).
- ⚡ **Asincronismo:** Tareas pesadas (pagos, inventario, notificaciones) ocurren en paralelo.
- 🛡️ **Resiliencia:** Si un servicio cae, los eventos se encolan en Kafka y se procesan al volver en línea.

## 🛠️ Stack Tecnológico

- **Lenguaje / Framework:** Python 3.11 + FastAPI
- **Event Broker:** Apache Kafka + Zookeeper
- **Bases de Datos:** PostgreSQL (para cada servicio), TimescaleDB (Analytics), Redis
- **Infraestructura:** Docker & Docker Compose
- **Librerías Clave:** Pydantic, SQLAlchemy, Asyncpg, Aiokafka

## 📁 Estructura del Proyecto

- `services/`: Contiene el código fuente de cada microservicio (Orders, Inventory, Payments, Users, Notifications, Analytics, etc).
- `shared/`: Modelos de eventos compartidos (los "contratos") y utilidades comunes de Kafka.
- `docs/`: Documentación detallada, presentaciones y diagramas (UML y Flowcharts).
- `docker-compose.yml`: Orquestación completa de la infraestructura.

## 📚 Documentación y Diagramas

Consulta la carpeta `/docs/` para entender el flujo a fondo:
- [Arquitectura y Fundamentos](docs/arquitectura.md)
- [Diagramas de Arquitectura General](docs/diagramas/arquitectura_general.md)
- [Diagramas de Flujo y Secuencia (Saga Pattern)](docs/diagramas/diagramas_secuencia.md)
- [Taller de Modelado de Eventos](docs/workshop/01_event_modeling.md)

## 🚀 Cómo Ejecutar el Proyecto Localmente

Para levantar toda la infraestructura (Kafka, Bases de Datos, y los Microservicios), asegúrate de tener Docker instalado y ejecuta:

```bash
docker compose up -d --build
```

- **Kafka UI** estará disponible en: [http://localhost:8110](http://localhost:8110)
- **MailHog** (Bandeja de correos de prueba) en: [http://localhost:8055](http://localhost:8055)
- Las APIs de cada servicio levantarán en sus respectivos puertos (ver `docker-compose.yml`).
