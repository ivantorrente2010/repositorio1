from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import NutritionPlan, Client
from schemas import NutritionPlanCreate, NutritionPlanUpdate, NutritionPlanResponse
from auth import get_current_user

router = APIRouter(
    prefix="/nutrition-plans",
    tags=["Nutrition Plans"]
)

# Crear un plan de nutrición
@router.post("/", response_model=NutritionPlanResponse)
def create_plan(plan: NutritionPlanCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Verificar que el usuario sea un entrenador
    if current_user["tipo_usuario"] != "entrenador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear planes de nutrición."
        )

    # Verificar que el cliente exista
    cliente = db.query(Client).filter(Client.id == plan.cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente no existe."
        )

    # Crear el plan de nutrición
    nuevo_plan = NutritionPlan(
        descripcion=plan.descripcion,
        entrenador_id=current_user["id"],
        cliente_id=plan.cliente_id
    )
    db.add(nuevo_plan)
    db.commit()
    db.refresh(nuevo_plan)
    return nuevo_plan

# Obtener los planes de un cliente
@router.get("/{cliente_id}", response_model=list[NutritionPlanResponse])
def get_client_plans(cliente_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Verificar que el cliente exista
    cliente = db.query(Client).filter(Client.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente no existe."
        )

    # Verificar permisos
    if current_user["tipo_usuario"] == "cliente" and current_user["id"] != cliente_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver los planes de este cliente."
        )

    planes = db.query(NutritionPlan).filter(NutritionPlan.cliente_id == cliente_id).all()
    return planes

# Actualizar un plan de nutrición
@router.put("/{plan_id}", response_model=NutritionPlanResponse)
def update_plan(plan_id: int, plan: NutritionPlanUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Buscar el plan
    plan_db = db.query(NutritionPlan).filter(NutritionPlan.id == plan_id).first()
    if not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El plan no existe."
        )

    # Verificar permisos
    if current_user["tipo_usuario"] != "entrenador" or plan_db.entrenador_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para actualizar este plan."
        )

    plan_db.descripcion = plan.descripcion
    db.commit()
    db.refresh(plan_db)
    return plan_db

# Eliminar un plan de nutrición
@router.delete("/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Buscar el plan
    plan = db.query(NutritionPlan).filter(NutritionPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El plan no existe."
        )

    # Verificar permisos
    if current_user["tipo_usuario"] != "entrenador" or plan.entrenador_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este plan."
        )

    db.delete(plan)
    db.commit()
    return {"message": "Plan eliminado con éxito"}
