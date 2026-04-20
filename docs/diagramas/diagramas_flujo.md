# Diagramas de Flujo: Topología y Datos

Estos diagramas de flujo representan la topología de red, la relación entre componentes y la dirección explícita de los eventos procesados en la arquitectura central.

## 1. Topología Principal del Ecosistema
Ilustra la separación entre los microservicios del ecosistema comercial, el uso central de Kafka y el principio de las bases de datos aisladas.

```mermaid
flowchart TD
    %% Definición de Actores y Componentes
    U([🧑‍💻 Cliente])
    
    subgraph Microservicios
        O[🛍️ Orders Service]
        I[📦 Inventory Service]
        P[💳 Payments Service]
        N[✉️ Notifications Service]
    end

    subgraph EventBroker [Broker de Eventos]
        K{{"🚌 Apache Kafka"}}
    end

    subgraph BasesDeDatos [Bases de Datos Aisladas]
        DB_O[(PostgreSQL Orders)]
        DB_I[(PostgreSQL Inventory)]
        DB_P[(PostgreSQL Payments)]
    end

    %% Relaciones de Base de Datos
    O -.- DB_O
    I -.- DB_I
    P -.- DB_P

    %% Flujo Creado
    U -- "1. POST /orders" --> O
    O -- "2. Publica Evento\n[OrderCreated]" --> K
    O -- "3. HTTP 202 (Asíncrono)" --> U
    
    %% Consumo en Paralelo
    K -- "4a. Consume\n[OrderCreated]" --> I
    K -- "4b. Consume\n[OrderCreated]" --> P

    %% Respuesta de Microservicios
    I -- "5a. Publica Evento\n[InventoryReserved]" --> K
    P -- "5b. Publica Evento\n[PaymentProcessed]" --> K

    %% Resolución
    K -- "6. Consume Resultados\n[Actualiza Orden]" --> O
    K -- "7. Consume Resultados" --> N
    N -- "8. Envía Email de Confirmación" --> U

    %% Estilos
    style K fill:#ff9900,stroke:#333,stroke-width:2px,color:#000
    style O fill:#3498db,color:#fff
    style I fill:#2ecc71,color:#fff
    style P fill:#9b59b6,color:#fff
    style N fill:#e67e22,color:#fff
```

## 2. Árbol de Decisión Lógico (Fallo de Stock)
Visualización enfocada al comportamiento del flujo de decisión lógica cuando ocurre un fallo por reglas de negocio, y las consecuentes tareas de recuperación.

```mermaid
flowchart LR
    %% Nodos
    OrderStart([Inicio: Orden Creada\nen estado PENDING])
    Kafka1{Kafka:\nOrderCreated}
    InvCheck{¿Hay Stock?}
    
    StockFailed([Fallo: Emitir\nInventoryFailed])
    Kafka2{Kafka:\nInventoryFailed}
    
    OrdersCancel[Orders Service:\nCambia estado a CANCELLED]
    PayCancel[Payments Service:\nCancela proceso de cobro]
    NotifReject[Notifications Service:\nEnvía email de disculpas]
    
    %% Flujo principal
    OrderStart --> Kafka1
    Kafka1 -->|Consume| InvCheck
    
    %% Fallo
    InvCheck -->|No| StockFailed
    StockFailed -->|Publica| Kafka2
    
    %% Reacciones en paralelo al fallo
    Kafka2 -->|Consume| OrdersCancel
    Kafka2 -->|Consume| PayCancel
    Kafka2 -->|Consume| NotifReject
    
    %% Estilos de error
    style StockFailed fill:#e74c3c,color:#fff
    style Kafka2 fill:#ff9900,color:#000
    style OrdersCancel fill:#c0392b,color:#fff
    style PayCancel fill:#c0392b,color:#fff
```