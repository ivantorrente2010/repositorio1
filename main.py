from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, routines, nutrition_plans, metrics
from auth import router as auth_router
from database import Base, engine

# Cargar modelos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5173"],  # Lista de URLs permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(users.router)  # Rutas de usuarios
app.include_router(auth_router)  # Rutas de autenticación
app.include_router(routines.router)  # Rutas de rutinas
app.include_router(nutrition_plans.router)  # Rutas de planes de nutrición
app.include_router(metrics.router)  # Rutas de métricas

# Ruta de prueba para verificar que el backend funciona correctamente
@app.get("/")
def read_root():
    return {"message": "¡API funcionando correctamente!"}





