# Taller 1: Modelando y Emitiendo tu Primer Evento

**Objetivo:** Aprender en la práctica cómo se diseña (modela) un evento, cómo un microservicio lo emite (Productor) y cómo otro servicio reacciona a él (Consumidor). Todo de forma completamente desacoplada usando EDA.

**Escenario Práctico:** 
Imagina que queremos agregar una nueva funcionalidad: Cuando un nuevo usuario se registra en nuestro E-Commerce, queremos enviarle un correo de "¡Bienvenido!".
En lugar de que el servicio de **Users** (Usuarios) llame directamente al de **Notifications** (Notificaciones), el servicio de Usuarios simplemente emitirá un evento llamado `UserCreated` (Usuario Creado) al mundo (nuestro Broker Kafka).

¡Manos a la obra! Sigue estos 3 pasos:

---

### Paso 1: Modelar el Evento (El "Contrato")

En EDA, un evento es un mensaje que contiene datos sobre algo que **ya pasó**. Necesitamos definir qué datos van a viajar en ese mensaje.

📍 **Ruta del archivo:** Crea un nuevo archivo en `shared/events/user_events.py`

💻 **Copia y pega este código:**
```python
from pydantic import BaseModel
from datetime import datetime

class UserCreatedEvent(BaseModel):
    user_id: int
    email: str
    username: str
    created_at: datetime = datetime.now()
```

📝 **Explicación simple:** 
Estamos definiendo la estructura de nuestro evento. Usamos `BaseModel` (de Pydantic) para asegurar que el evento de un nuevo usuario siempre lleve un `user_id`, un `email` y un `username`. Este archivo vivirá en la carpeta `shared/` porque es un "contrato" que tanto el que emite como el que recibe deben conocer.

---

### Paso 2: Emitir el Evento (El Productor)

Ahora vamos a enseñarle a nuestro servicio de Usuarios que, cada vez que registre a alguien con éxito, se lo comunique al broker de Kafka.

📍 **Ruta del archivo:** Abre u ocupa el archivo `services/users/main.py`

💻 **Agrega este código (o adáptalo a tu endpoint de crear usuario):**
```python
from fastapi import FastAPI
from shared.events.user_events import UserCreatedEvent
# Asumiendo que tienes una función productora en shared/kafka/producer.py
from shared.kafka.producer import publish_event 

app = FastAPI()

@app.post("/users/")
def create_user(email: str, username: str):
    # 1. Aquí iría tu lógica habitual para guardar en la Base de Datos
    new_user_id = 123 # ID simulado devuelto por la Base de Datos
    
    # 2. Construir el Evento con el modelo que creamos en el Paso 1
    evento = UserCreatedEvent(
        user_id=new_user_id,
        email=email,
        username=username
    )
    
    # 3. Publicar el evento en Kafka (en el "topic" de usuarios)
    publish_event(topic="users_topic", event=evento.model_dump_json())
    
    return {"msg": "Usuario creado con éxito y evento emitido"}
```

📝 **Explicación simple:** 
El servicio de usuarios hace su trabajo principal (registrar en la DB) y luego literalmente "grita" hacia el bus de mensajes: *"Oigan, acabo de crear un usuario, aquí están sus datos"*. Al servicio de Usuarios **no le importa** quién va a leer este mensaje. Logramos un desacoplamiento perfecto.

---

### Paso 3: Consumir el Evento (El Consumidor)

Finalmente, el servicio de Notificaciones estará esperando silenciosamente a que aparezcan eventos en el `users_topic`. 

📍 **Ruta del archivo:** Abre u ocupa el archivo `services/notifications/main.py`

💻 **Copia y pega este código (estructura básica del consumidor):**
```python
import json
from shared.events.user_events import UserCreatedEvent

def handle_user_created(message_value: str):
    # 1. Recibimos el mensaje en texto (JSON) y lo convertimos a nuestro Modelo
    datos = json.loads(message_value)
    evento = UserCreatedEvent(**datos)
    
    # 2. Reaccionar al evento con la lógica de negocio del consumidor
    print(f"📧 Enviando email de BIENVENIDA a: {evento.email}")
    print(f"Hola {evento.username}, bienvenido a nuestra tienda.")

# -> El consumidor de Kafka de este servicio se configuraría para escuchar "users_topic"
# -> y ejecutar 'handle_user_created' por cada mensaje que llegue.
```

📝 **Explicación simple:** 
El servicio de notificaciones está suscrito al canal de usuarios (`users_topic`). Cuando detecta que llegó un mensaje, lo transforma utilizando el modelo que hicimos en el Paso 1, lee el correo, y envía la notificación. Todo esto ocurre de fondo (asíncronamente).

---

### 🎉 Conclusión del Taller
Si seguiste estos pasos, acabas de implementar el corazón de la arquitectura orientada a eventos: **Un productor emitió un hecho que ya ocurrió, y un consumidor reaccionó a él de manera totalmente independiente.** Si el servicio de Notificaciones se apaga, el usuario se sigue creando sin problemas y el evento se queda guardado en Kafka hasta que el servicio de Notificaciones vuelva a encenderse.