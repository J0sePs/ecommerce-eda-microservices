# Diagramas de Secuencia: Arquitectura Orientada a Eventos

Estos diagramas ilustran el comportamiento temporal y el intercambio de mensajes asíncronos entre los distintos microservicios a través del Event Broker.

## 1. Camino Feliz (Proceso Exitoso)
Muestra la respuesta asíncrona exitosa del ecosistema cuando se crea una orden y todos los servicios de dominio operan sin contratiempos.

```mermaid
sequenceDiagram
    actor Cliente
    participant O as 🛍️ Orders Service
    participant K as 🚌 Apache Kafka (Broker)
    participant I as 📦 Inventory Service
    participant P as 💳 Payments Service
    participant N as ✉️ Notifications Service

    Cliente->>O: 1. POST /orders (Comprar artículo)
    note over O: Guarda en BD (Estado: PENDING)
    O->>K: 2. Publica evento: {OrderCreated}
    O-->>Cliente: 3. HTTP 202 Accepted ("Procesando orden...")
    
    par Procesamiento en paralelo
        K-->>I: 4a. Consume {OrderCreated}
        note over I: Valida y descuenta stock
        I->>K: 5a. Publica evento: {InventoryReserved}
    and
        K-->>P: 4b. Consume {OrderCreated}
        note over P: Inicia verificación de pago
        P->>K: 5b. Publica evento: {PaymentProcessed}
    end

    K-->>O: 6. Consume {Payment... / Inventory...}
    note over O: Actualiza orden (Estado: COMPLETED)

    K-->>N: 7. Consume eventos de éxito
    note over N: Genera plantilla de éxito
    N-->>Cliente: 8. Envía Email: "Tu compra fue exitosa"
```

## 2. Flujo de Compensación (Fallo de Inventario)
Muestra cómo reacciona el ecosistema para lidiar con problemas (ej. falta de stock de un artículo). Permite abortar transacciones distribuidas sin acoplar temporalmente los componentes.

```mermaid
sequenceDiagram
    actor Cliente
    participant O as 🛍️ Orders Service
    participant K as 🚌 Apache Kafka (Broker)
    participant I as 📦 Inventory Service
    participant P as 💳 Payments Service
    participant N as ✉️ Notifications Service

    O->>K: 1. Publica evento: {OrderCreated}
    
    K-->>I: 2. Consume {OrderCreated}
    note over I: Valida stock... ¡No hay stock!
    I->>K: 3. Publica evento de fallo: {InventoryFailed}
    
    par Procesando la cancelación
        K-->>O: 4a. Consume {InventoryFailed}
        note over O: Cambia estado a CANCELLED
    and
        K-->>P: 4b. Consume {InventoryFailed}
        note over P: Evita hacer el cobro temporal
    and
        K-->>N: 4c. Consume {InventoryFailed}
        note over N: Genera plantilla de rechazo
        N-->>Cliente: 5. Envía Email: "Perdón, nos quedamos sin stock"
    end
```