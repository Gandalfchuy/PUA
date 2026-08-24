from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import extract
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from app.database import get_db
from app.models.procesos import Lista
from app.schemas.procesos import ListaResponse, ListaCreate
from app.core.usuario import VerificadorRol, obtener_usuario_actual

requiere_admin = VerificadorRol(["SUPER_ADMIN"])

router_lista = APIRouter(prefix ="/lista", tags=["Listas"])

@router_lista.post("/", response_model=ListaResponse, status_code=status.HTTP_201_CREATED)
def crear_asistencia(datos:ListaCreate, db:Session = Depends(get_db), usuario_id: int = Depends(obtener_usuario_actual)):

    nueva_asistencia=Lista(**datos.model_dump())

    nueva_asistencia.created_by = usuario_id.id
    nueva_asistencia.created_at = datetime.now()

    db.add(nueva_asistencia)
    db.commit()
    db.refresh(nueva_asistencia)

    return nueva_asistencia

@router_lista.get("/", response_model=List[ListaResponse])
def listar_lista(db: Session = Depends(get_db), usuario_id: int = Depends(obtener_usuario_actual)):
    
    sesion_db = db.query(Lista).filter(Lista.is_deleted == False).all()
    
    return sesion_db

