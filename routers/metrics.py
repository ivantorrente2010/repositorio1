from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Metric, Client
from schemas import MetricCreate, MetricResponse
from auth import get_current_user
from sqlalchemy.sql import func


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

# Registrar una nueva métrica
@router.post("/", response_model=MetricResponse)
def create_metric(metric: MetricCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Verificar que el usuario sea un cliente o entrenador
    if current_user["tipo_usuario"] == "entrenador":
        cliente = db.query(Client).filter(Client.id == metric.cliente_id).first()
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El cliente no existe."
            )
    elif current_user["tipo_usuario"] == "cliente":
        if current_user["id"] != metric.cliente_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para registrar métricas para este cliente."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para registrar métricas."
        )

    nueva_metrica = Metric(
        peso=metric.peso,
        grasa_corporal=metric.grasa_corporal,
        rendimiento=metric.rendimiento,
        cliente_id=metric.cliente_id
    )
    db.add(nueva_metrica)
    db.commit()
    db.refresh(nueva_metrica)
    return nueva_metrica

# Obtener métricas históricas de un cliente
@router.get("/{cliente_id}", response_model=list[MetricResponse])
def get_metrics(cliente_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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
            detail="No tienes permiso para ver las métricas de este cliente."
        )

    metrics = db.query(Metric).filter(Metric.cliente_id == cliente_id).order_by(Metric.fecha.desc()).all()
    return metrics

    # Obtener progreso de un cliente

@router.get("/progress/{cliente_id}")
def get_client_progress(cliente_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Verificar que el cliente existe
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
            detail="No tienes permiso para ver el progreso de este cliente."
        )

    # Obtener las métricas del cliente
    metrics = db.query(Metric).filter(Metric.cliente_id == cliente_id).order_by(Metric.fecha).all()
    if not metrics:
        return {"message": "No hay métricas registradas para este cliente."}

    # Resumen del progreso
    progress = {
        "peso_inicial": metrics[0].peso,
        "peso_actual": metrics[-1].peso,
        "grasa_inicial": metrics[0].grasa_corporal,
        "grasa_actual": metrics[-1].grasa_corporal,
        "promedio_peso": db.query(func.avg(Metric.peso)).filter(Metric.cliente_id == cliente_id).scalar(),
        "promedio_grasa": db.query(func.avg(Metric.grasa_corporal)).filter(Metric.cliente_id == cliente_id).scalar(),
        "historial": [
            {
                "fecha": m.fecha,
                "peso": m.peso,
                "grasa_corporal": m.grasa_corporal
            }
            for m in metrics
        ]
    }
    return progress

    