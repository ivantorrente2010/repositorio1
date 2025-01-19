from database import engine, Base
from models import User, Trainer, Client
from hashing import Hash
from database import SessionLocal

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Insertar datos iniciales

def insertar_datos_iniciales():
    db = SessionLocal()

    # Insertar entrenador inicial
    if not db.query(User).filter(User.email == "trainer@example.com").first():
        trainer = User(
            nombre="Trainer Example",
            email="trainer@example.com",
            password=Hash.bcrypt("password123"),  # Contraseña hash
            tipo_usuario="entrenador"
        )
        db.add(trainer)
        db.commit()
        db.refresh(trainer)

        trainer_data = Trainer(id=trainer.id, especialidad="General")
        db.add(trainer_data)
        db.commit()

    # Insertar cliente inicial
    if not db.query(User).filter(User.email == "client@example.com").first():
        client = User(
            nombre="Client Example",
            email="client@example.com",
            password=Hash.bcrypt("password123"),  # Contraseña hash
            tipo_usuario="cliente"
        )
        db.add(client)
        db.commit()
        db.refresh(client)

        client_data = Client(id=client.id, objetivos="Perder peso", entrenador_id=trainer.id)
        db.add(client_data)
        db.commit()

    db.close()

# Llamar a la función para insertar los datos iniciales
insertar_datos_iniciales()

