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

    print("Datos del plan creado:", nuevo_plan)

    # Retorna un diccionario que coincida con el esquema
    return {
        "id": nuevo_plan.id,
        "descripcion": nuevo_plan.descripcion,
        "cliente_id": nuevo_plan.cliente_id,
        "entrenador_id": nuevo_plan.entrenador_id
    }



# Obtener el plan de nutrición asignado a un cliente

@router.get("/client/{cliente_id}", response_model=list[NutritionPlanResponse])
def get_client_plan(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar que un cliente no acceda a datos de otro cliente
    if current_user.tipo_usuario == "cliente" and current_user.id != cliente_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver los planes de otro cliente."
        )

    # Obtener los planes asignados al cliente
    planes = db.query(NutritionPlan).filter(NutritionPlan.cliente_id == cliente_id).all()

    # Debugging: imprime los datos antes de retornarlos
    print("Planes encontrados:", planes)

    if not planes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay planes de nutrición asignados a este cliente."
        )

   # Asegúrate de retornar un formato que coincida con NutritionPlanResponse
    return [{"id": plan.id, "descripcion": plan.descripcion, "cliente_id": plan.cliente_id, "entrenador_id": plan.entrenador_id} for plan in planes]

