from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    tipo_usuario: str  # "entrenador" o "cliente"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

# Esquema del token con el rol incluido
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str  # Nuevo campo para el rol del usuario

class TokenData(BaseModel):
    email: str | None = None

# Esquemas para rutinas
class RoutineBase(BaseModel):
    nombre: str
    descripcion: str
    cliente_id: int

class RoutineCreate(RoutineBase):
    pass

class RoutineUpdate(BaseModel):
    nombre: str
    descripcion: str

class RoutineResponse(RoutineBase):
    id: int
    nombre: str
    descripcion: str
    cliente_id: int
    entrenador_id: int

    class Config:
        from_attributes = True

# Esquemas para planes de nutrición
class NutritionPlanBase(BaseModel):
    descripcion: str
    cliente_id: int

class NutritionPlanCreate(NutritionPlanBase):
    pass

class NutritionPlanUpdate(BaseModel):
    descripcion: str

class NutritionPlanResponse(NutritionPlanBase):
    id: int
    entrenador_id: int

    class Config:
        from_attributes = True

# Esquemas para métricas
class MetricBase(BaseModel):
    peso: float
    grasa_corporal: Optional[float] = None

class MetricCreate(MetricBase):
    cliente_id: int

class MetricResponse(MetricBase):
    id: int
    cliente_id: int
    peso: float
    grasa_corporal: Optional[float] = None
    fecha: str

    class Config:
        orm_mode = True

# Esquema para el login
class LoginRequest(BaseModel):
    email: str
    password: str
