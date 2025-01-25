from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    tipo_usuario = Column(String(20), nullable=False)  # "entrenador" o "cliente"

    trainer = relationship("Trainer", back_populates="user", uselist=False)
    client = relationship("Client", back_populates="user", uselist=False)

class Trainer(Base):
    __tablename__ = "trainers"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    especialidad = Column(String(255))

    user = relationship("User", back_populates="trainer")
    clients = relationship("Client", back_populates="trainer")
    routines = relationship("Routine", back_populates="trainer")
    nutrition_plans = relationship("NutritionPlan", back_populates="trainer")

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    objetivos = Column(String(255))
    entrenador_id = Column(Integer, ForeignKey("trainers.id"), nullable=True)

    user = relationship("User", back_populates="client")
    trainer = relationship("Trainer", back_populates="clients")
    routines = relationship("Routine", back_populates="client")
    nutrition_plans = relationship("NutritionPlan", back_populates="client")
    metrics = relationship("Metric", back_populates="client", cascade="all, delete-orphan")

class Routine(Base):
    __tablename__ = "routines"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(1000))
    entrenador_id = Column(Integer, ForeignKey("trainers.id"))
    cliente_id = Column(Integer, ForeignKey("clients.id"))

    trainer = relationship("Trainer", back_populates="routines")
    client = relationship("Client", back_populates="routines")

class NutritionPlan(Base):
    __tablename__ = "nutrition_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(1000))
    entrenador_id = Column(Integer, ForeignKey("trainers.id"))
    cliente_id = Column(Integer, ForeignKey("clients.id"))

    trainer = relationship("Trainer", back_populates="nutrition_plans")
    client = relationship("Client", back_populates="nutrition_plans")

class Metric(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    peso = Column(Float, nullable=False)
    grasa_corporal = Column(Float, nullable=True)
    fecha = Column(DateTime, default=func.now())

    client = relationship("Client", back_populates="metrics")
