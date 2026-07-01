# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuarios import Usuarios
from app.core.security import verify_password, create_access_token

router_auth = APIRouter(tags=["Autenticación"])

@router_auth.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuarios).filter(Usuarios.correo == form_data.username).first()

    if not usuario or not verify_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not usuario.is_active:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este usuario está inactivo"
        )
    datos_del_token = {
        "sub": str(usuario.id),
        "rol_id": usuario.rol_id 
    }
    
    access_token = create_access_token(data=datos_del_token)

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "usuario": {
            "nombre": usuario.nombre_completo,
            "rol_id": usuario.rol_id
        }
    }