from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Routine, Client, Trainer
from schemas import RoutineCreate, RoutineUpdate, RoutineResponse
from auth import get_current_user

router = APIRouter(
    prefix="/routines",
    tags=["Routines"]
)

# Crear una rutina

@router.post("/", response_model=RoutineResponse)
def create_routine(
    routine: RoutineCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
    ):
    # Verificar que el usuario sea un entrenador
    if current_user.tipo_usuario!= "entrenador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear rutinas."
        )

    # Verificar que el cliente exista
    cliente = db.query(Client).filter(Client.id == routine.cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente no existe."
        )

    # Crear la rutina
    nueva_rutina = Routine(
        nombre=routine.nombre,
        descripcion=routine.descripcion,
        entrenador_id=current_user.id,
        cliente_id=routine.cliente_id
    )
    db.add(nueva_rutina)
    db.commit()
    db.refresh(nueva_rutina)

    return {
    "id": nueva_rutina.id,
    "nombre": nueva_rutina.nombre,
    "descripcion": nueva_rutina.descripcion,
    "cliente_id": nueva_rutina.cliente_id,
    "entrenador_id": nueva_rutina.entrenador_id
}

# Obtener las rutinas de un cliente
@router.get("/client/{cliente_id}", response_model=list[RoutineResponse])
def get_client_routines(cliente_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Verificar que el cliente exista
    cliente = db.query(Client).filter(Client.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente no existe."
        )

    # Solo entrenadores o el propio cliente pueden ver las rutinas
    if current_user["tipo_usuario"] == "cliente" and current_user["id"] != cliente_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver las rutinas de este cliente."
        )

    rutinas = db.query(Routine).filter(Routine.cliente_id == cliente_id).all()
    
    # Transformar rutinas en el formato esperado por RoutineResponse
    return [
        {
            "id": rutina.id,
            "nombre": rutina.nombre,
            "descripcion": rutina.descripcion,
            "cliente_id": rutina.cliente_id,
            "entrenador_id": rutina.entrenador_id,
        }
        for rutina in rutinas
    ]

# Actualizar una rutina
@router.put("/{rutina_id}", response_model=RoutineResponse)
def update_routine(rutina_id: int, routine: RoutineUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Buscar la rutina
    rutina = db.query(Routine).filter(Routine.id == rutina_id).first()
    if not rutina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La rutina no existe."
        )

    # Verificar que el usuario sea el entrenador de la rutina
    if current_user["tipo_usuario"] != "entrenador" or rutina.entrenador_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar esta rutina."
        )

    rutina.nombre = routine.nombre
    rutina.descripcion = routine.descripcion
    db.commit()
    db.refresh(rutina)
    return rutina

# Eliminar una rutina
@router.delete("/{rutina_id}")
def delete_routine(rutina_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Buscar la rutina
    rutina = db.query(Routine).filter(Routine.id == rutina_id).first()
    if not rutina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La rutina no existe."
        )

    # Verificar que el usuario sea el entrenador de la rutina
    if current_user["tipo_usuario"] != "entrenador" or rutina.entrenador_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta rutina."
        )

    db.delete(rutina)
    db.commit()
    return {"message": "Rutina eliminada con éxito"}
