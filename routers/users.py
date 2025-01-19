from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Client, Trainer
from schemas import UserCreate, UserResponse
from hashing import Hash

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Crear un usuario
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    user_existente = db.query(User).filter(User.email == user.email).first()
    if user_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    
    nuevo_usuario = User(
        nombre=user.nombre,
        email=user.email,
        password=Hash.bcrypt(user.password),
        tipo_usuario=user.tipo_usuario
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # Insertar en clients o trainers según el tipo_usuario
    if user.tipo_usuario == "cliente":
        nuevo_cliente = Client(
            id=nuevo_usuario.id,
            objetivos="Definir objetivos",  # Personalizable
            entrenador_id=None  # Esto puede ser asignado después
        )
        db.add(nuevo_cliente)
    elif user.tipo_usuario == "entrenador":
        nuevo_entrenador = Trainer(
            id=nuevo_usuario.id,
            especialidad="General"  # Personalizable
        )
        db.add(nuevo_entrenador)

    db.commit()
    return nuevo_usuario

# Leer todos los usuarios
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Registrar un nuevo usuario
@router.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el correo ya está registrado
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Crear nuevo usuario
    hashed_password = Hash.bcrypt(user.password)
    new_user = User(
        nombre=user.nombre,
        email=user.email,
        password=hashed_password,
        tipo_usuario=user.tipo_usuario,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Insertar en clients o trainers según el tipo_usuario
    if user.tipo_usuario == "cliente":
        nuevo_cliente = Client(
            id=new_user.id,
            objetivos="Definir objetivos",  # Personalizable
            entrenador_id=None  # Esto puede ser asignado después
        )
        db.add(nuevo_cliente)
    elif user.tipo_usuario == "entrenador":
        nuevo_entrenador = Trainer(
            id=new_user.id,
            especialidad="General"  # Personalizable
        )
        db.add(nuevo_entrenador)

    db.commit()
    return {"message": "Usuario registrado exitosamente"}
