from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from hashing import Hash
from models import User
from schemas import Token
from schemas import LoginRequest

# Configuración del token JWT
SECRET_KEY = "P@ssw0rdak47ak47"  # Cambia esto por una clave segura y secreta
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 esquema para recibir tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Crear un token de acceso
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verificar un token de acceso
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Dependencia para proteger rutas
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )
    return user

# Router de autenticación
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Endpoint de inicio de sesión

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        print(f"Intentando iniciar sesión con: {request.email}")
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            print("Usuario no encontrado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )

        print(f"Hash almacenado en la BD: {user.password}")
        if not Hash.verify(user.password, request.password):
            print("La verificación del hash falló")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )

        # Crear el token incluyendo el tipo_usuario
        access_token = create_access_token(data={"sub": user.email, "role": user.tipo_usuario})

        # Incluir el tipo_usuario en la respuesta
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user.tipo_usuario  # Este es el campo que indica el rol
        }
    except Exception as e:
        print(f"Error en login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al iniciar sesión",
        )
