# Topología de la Arquitectura del Sistema (EDA)

Este diagrama representa la arquitectura general de alto nivel del sistema de comercio electrónico, destacando la separación de los microservicios, el API Gateway como punto de entrada, las bases de datos por servicio y el núcleo de eventos (Apache Kafka).

```mermaid
flowchart TD
    %% Definición de Actores
    U([🧑‍💻 Cliente / Frontend])

    %% Punto de Entrada
    Gateway[API Gateway]

    %% Agrupación de Microservicios
    subgraph Microservices ["Capa de Microservicios (FastAPI)"]
        O[🛍️ Orders Service]
        I[📦 Inventory Service]
        P[💳 Payments Service]
        N[✉️ Notifications Service]
        A[📊 Analytics Service]
    end

    %% Agrupación de Bus de Eventos
    subgraph Messaging ["Capa de Mensajería y Eventos"]
        K{{"🚌 Apache Kafka\n(Broker Central)"}}
    end

    %% Agrupación de Bases de Datos Aisladas
    subgraph Databases ["Capa de Persistencia (PostgreSQL)"]
        DB_O[(Orders DB)]
        DB_I[(Inventory DB)]
        DB_P[(Payments DB)]
        DB_A[(Analytics DB)]
    end

    %% Conexiones: Cliente -> Gateway -> Servicios
    U -->|HTTP / REST| Gateway
    Gateway -->|Enruta Peticiones| O
    Gateway -->|Enruta Peticiones| I

    %% Conexiones: Servicios <-> Kafka
    O <-->|Publica/Consume Eventos| K
    I <-->|Publica/Consume Eventos| K
    P <-->|Publica/Consume Eventos| K
    N <-->|Solo Consume Eventos| K
    A <-->|Solo Consume Eventos| K

    %% Conexiones: Servicios <-> Bases de Datos
    O -.->|Lee/Escribe exclusiva| DB_O
    I -.->|Lee/Escribe exclusiva| DB_I
    P -.->|Lee/Escribe exclusiva| DB_P
    A -.->|Lee/Escribe exclusiva| DB_A

    %% Estilizado
    style K fill:#ff9900,stroke:#333,stroke-width:2px,color:#000
    style Gateway fill:#34495e,stroke:#333,color:#fff
    style U fill:#bdc3c7,stroke:#333,color:#000

    %% Estilos de los servicios
    style O fill:#3498db,color:#fff
    style I fill:#2ecc71,color:#fff
    style P fill:#9b59b6,color:#fff
    style N fill:#e67e22,color:#fff
    style A fill:#e74c3c,color:#fff
```

### Elementos Clave del Diagrama:
1. **API Gateway:** Único punto de entrada público que recibe las llamadas HTTP iniciales del frontend y las dirige hacia los microservicios pertinentes.
2. **Microservicios Independientes:** Desarrollados en FastAPI, se agrupan en su propia capa. Destacan servicios reactivos puros como `Notifications` y `Analytics`.
3. **Broker Central (Kafka):** El corazón de la comunicación asíncrona. Los servicios suben sus actualizaciones (eventos) y reaccionan a los publicados por los demás.
4. **Persistencia Aislada (Database per Service):** Ni el Gateway ni los servicios interfieren en las bases de datos ajenas, garantizando nulo acoplamiento estructural a nivel de base de datos.