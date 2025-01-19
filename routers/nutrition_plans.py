from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import NutritionPlan, Client, User
from schemas import NutritionPlanCreate, NutritionPlanResponse
from auth import get_current_user

router = APIRouter(
    prefix="/nutrition-plans",
    tags=["Nutrition Plans"]
)


# Crear un plan de nutrición
@router.post("/", response_model=NutritionPlanResponse)
def create_plan(plan: NutritionPlanCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.tipo_usuario != "entrenador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear planes de nutrición."
        )

    cliente = db.query(Client).filter(Client.id == plan.cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente no existe."
        )

    nuevo_plan = NutritionPlan(
        descripcion=plan.descripcion,
        entrenador_id=current_user.id,
        cliente_id=plan.cliente_id
    )
    db.add(nuevo_plan)
    db.commit()
    db.refresh(nuevo_plan)
    return nuevo_plan



# Obtener el plan de nutrición asignado a un cliente
@router.get("/client/{cliente_id}", response_model=list[NutritionPlanResponse])
def get_client_plan(cliente_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["tipo_usuario"] == "cliente" and current_user["id"] != cliente_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este plan de nutrición."
        )

    planes = db.query(NutritionPlan).filter(NutritionPlan.cliente_id == cliente_id).all()
    if not planes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay planes de nutrición asignados a este cliente."
        )

    return planes
