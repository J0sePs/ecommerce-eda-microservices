# Presentación: Arquitectura Orientada a Eventos (EDA)

## Diapositiva 1: Título
- **Proyecto:** Sistema de E-Commerce con Arquitectura Orientada a Eventos
- **Curso/Asignatura:** [Nombre del curso]
- **Integrantes:** [Nombres de los integrantes]

## Diapositiva 2: ¿Qué es EDA?
- Paradigma de arquitectura de software.
- Se basa en la producción, detección, consumo y reacción a eventos.
- Permite el diseño de sistemas altamente asíncronos y distribuidos.

## Diapositiva 3: ¿Por qué usar Eventos?
- **Desacoplamiento:** Los servicios no necesitan conocerse entre sí (Productor vs Consumidor).
- **Escalabilidad:** Cada componente puede escalar de forma independiente.
- **Tolerancia a fallos:** Si un servicio de destino cae, los eventos no se pierden, quedan en el Broker.

## Diapositiva 4: Tecnologías utilizadas
- **Apache Kafka:** Broker de eventos, maneja el flujo de mensajes (Tópicos, Particiones).
- **Python (FastAPI):** Para la creación de microservicios ligeros y eficientes.
- **Docker Compose:** Orquestación y despliegue local rápido de todos los contenedores.
- **PostgreSQL:** Bases de datos independientes por microservicio.

## Diapositiva 5: Arquitectura del Sistema
- Flujo de negocio asíncrono.
- Ej: *Orders* crea un pedido -> Emite evento `OrderCreated`.
- Ej: *Payments* e *Inventory* reaccionan a `OrderCreated` -> Procesan y emiten sus propios eventos.
- Ej: *Notifications* informa al usuario el resultado de todo el flujo.

## Diapositiva 6: Conclusiones
- EDA es el estándar para sistemas modernos de alta concurrencia.
- La complejidad principal recae en el diseño (garantizar la consistencia eventual y rastrear errores).
- Kafka resulta ser una pieza fundamental como "columna vertebral" de los datos en movimiento.
