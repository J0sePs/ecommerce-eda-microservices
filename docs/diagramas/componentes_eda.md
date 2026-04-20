# Componentes Fundamentales de una Arquitectura Orientada a Eventos (EDA)

Este diagrama ilustra de manera general y conceptual las partes que componen un ecosistema EDA (Productor, Evento, Broker y Consumidor), demostrando cómo un mismo evento puede detonar múltiples reacciones sin que el creador original se entere.

```mermaid
flowchart LR
    %% Definición de Nodos principales
    subgraph Productor ["1. El Productor (Event Producer)"]
        P["Servicio de Usuarios<br/>Detecta que algo importante pasó"]
    end

    subgraph Evento ["2. El Evento (The Event)"]
        E1["📄 Mensaje: UserCreated<br/>'Un usuario fue creado'<br/>(Datos inmutables del pasado)"]
    end

    subgraph Broker ["3. El Broker (Event Broker / Bus)"]
        B{{"🚌 Apache Kafka<br/>(Recibe, guarda y distribuye)"}}
    end

    subgraph Consumidores ["4. Los Consumidores (Event Consumers)"]
        C1["Servicio de Notificaciones<br/>📧 (Reacciona enviando correo)"]
        C2["Servicio de Analítica<br/>📊 (Reacciona sumando métricas)"]
    end

    %% Conexiones flujos
    P -->|"Emite"| E1
    E1 -->|"Se publica en"| B
    B -->|"Entrega a Suscriptor A"| C1
    B -->|"Entrega a Suscriptor B<br/>(en paralelo)"| C2

    %% Estilos
    style P fill:#3498db,stroke:#333,color:#fff
    style E1 fill:#f1c40f,stroke:#333,color:#000
    style B fill:#ff9900,stroke:#333,stroke-width:2px,color:#000
    style C1 fill:#2ecc71,stroke:#333,color:#fff
    style C2 fill:#9b59b6,stroke:#333,color:#fff
```

### Explicación del Flujo Conceptual:
1. **El Productor** hace su tarea principal (registrar un usuario en su propia base de datos) y construye un paquete de datos.
2. **El Evento** es ese paquete. Lleva un nombre en pasado (`UserCreated`) porque representa un hecho consumado que no se puede cambiar.
3. **El Broker** recibe este evento, lo guarda en disco (para no perderlo jamás) y alerta a todos los interesados.
4. **Los Consumidores** escuchan este mensaje y hacen su trabajo de forma totalmente independiente: uno manda correos, otro actualiza gráficas, y el Productor original ni se entera de que existen.