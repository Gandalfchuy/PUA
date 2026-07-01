# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import os
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuarios import Usuarios
from app.core.security import SECRET_KEY, ALGORITHM 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 

def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o el token expiró",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise credenciales_exception
            
    except jwt.PyJWTError:
        raise credenciales_exception

    usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    
    if usuario is None or not usuario.is_active:
        raise credenciales_exception

    return usuario

class VerificadorRol:
    def __init__(self, roles_permitidos: list[str]):
        self.roles_permitidos = roles_permitidos

    def __call__(self, usuario: Usuarios = Depends(obtener_usuario_actual)):
        nombre_rol = usuario.rol.nombre 
        
        if nombre_rol not in self.roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios para realizar esta acción"
            )
            
        return usuario