from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.procesos import Lista
from app.models.usuarios import Usuarios
from app.schemas.procesos import ListaResponse, ListaCreate
from app.core.usuario import VerificadorRol, obtener_usuario_actual

requiere_admin = VerificadorRol(["SUPER_ADMIN"])

router_lista = APIRouter(prefix="/lista", tags=["Listas"])

@router_lista.post("", response_model=ListaResponse, status_code=status.HTTP_201_CREATED)
def crear_asistencia(datos: ListaCreate, db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):

    nueva_asistencia = Lista(**datos.model_dump())
    nueva_asistencia.created_by = usuario_actual.id
    nueva_asistencia.created_at = datetime.now()

    db.add(nueva_asistencia)
    db.commit()
    db.refresh(nueva_asistencia)

    return nueva_asistencia

@router_lista.get("", response_model=List[ListaResponse])
def listar_asistencias(db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    listas_db = db.query(Lista).filter(Lista.is_deleted == False).all()
    return listas_db

@router_lista.get("/{id}", response_model=ListaResponse)
def obtener_asistencia(id: int, db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    asistencia_db = db.query(Lista).filter(Lista.id == id, Lista.is_deleted == False).first()
    if not asistencia_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Asistencia no encontrada"
        )
    return asistencia_db

@router_lista.put("/{id}", response_model=ListaResponse)
def actualizar_asistencia(id: int, datos: ListaCreate, db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    asistencia_db = db.query(Lista).filter(Lista.id == id, Lista.is_deleted == False).first()
    if not asistencia_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Asistencia no encontrada"
        )
    
    for llave, valor in datos.model_dump().items():
        setattr(asistencia_db, llave, valor)

    asistencia_db.updated_by = usuario_actual.id
    asistencia_db.updated_at = datetime.now()

    db.commit()
    db.refresh(asistencia_db)
    return asistencia_db

@router_lista.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_asistencia(id: int, db: Session = Depends(get_db), usuario_admin: Usuarios = Depends(requiere_admin)):
    asistencia_db = db.query(Lista).filter(Lista.id == id).first()
    if not asistencia_db:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    
    if asistencia_db.is_deleted:
        raise HTTPException(status_code=400, detail="La asistencia ya ha sido eliminada previamente")

    asistencia_db.is_deleted = True
    asistencia_db.deleted_by = usuario_admin.id
    asistencia_db.deleted_at = datetime.now()
    db.commit()

    return None

