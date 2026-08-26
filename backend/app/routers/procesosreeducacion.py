from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List 
from app.database import get_db
from app.models.procesos import ProcesoReeducacion
from app.models.usuarios import Usuarios
from app.schemas.procesos import ProcesoReeducacionResponse, ProcesoReeducacionCreate
from app.core.usuario import VerificadorRol, obtener_usuario_actual

requiere_admin = VerificadorRol(["SUPER_ADMIN"])

router_proceso = APIRouter(prefix="/proceso-reeducacion", tags=["Procesos de Reeducacion"])

@router_proceso.post("", response_model=ProcesoReeducacionResponse, status_code=status.HTTP_201_CREATED)
def crear_proceso(datos: ProcesoReeducacionCreate, db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    
    nuevo_proceso = ProcesoReeducacion(**datos.model_dump())
    nuevo_proceso.created_by = usuario_actual.id
    nuevo_proceso.created_at = datetime.now()
    db.add(nuevo_proceso)
    db.commit()
    db.refresh(nuevo_proceso)

    return nuevo_proceso

@router_proceso.get("", response_model=List[ProcesoReeducacionResponse])
def obtener_procesos(db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    procesos_db = db.query(ProcesoReeducacion).filter(ProcesoReeducacion.is_deleted == False).all()
    return procesos_db

@router_proceso.get("/{folio}", response_model=ProcesoReeducacionResponse)
def obtener_proceso_por_folio(
    folio: int, 
    db: Session = Depends(get_db), 
    usuario_actual: Usuarios = Depends(obtener_usuario_actual)
):
    proceso = db.query(ProcesoReeducacion).filter(
        ProcesoReeducacion.folio == folio, 
        ProcesoReeducacion.is_deleted == False
    ).first()
    
    if not proceso:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
        
    return proceso

@router_proceso.put("/{folio}", response_model=ProcesoReeducacionResponse)
def actualizar_proceso(folio: int, datos: ProcesoReeducacionCreate, db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):

    proceso_db = db.query(ProcesoReeducacion).filter(ProcesoReeducacion.folio == folio, ProcesoReeducacion.is_deleted == False).first()
    
    if not proceso_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El proceso no existe o fue eliminado"
        )

    datos_completos = datos.model_dump()

    for llave, valor in datos_completos.items():
        setattr(proceso_db, llave, valor)
    
    proceso_db.updated_by = usuario_actual.id
    proceso_db.updated_at = datetime.now()

    db.commit()
    db.refresh(proceso_db)

    return proceso_db

@router_proceso.delete("/{folio}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_proceso(folio: int, db: Session = Depends(get_db), usuario_admin: Usuarios = Depends(requiere_admin)):

    proceso_db = db.query(ProcesoReeducacion).filter(ProcesoReeducacion.folio == folio).first()
    
    if not proceso_db:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
        
    if proceso_db.is_deleted:
        raise HTTPException(status_code=400, detail="El proceso ya ha sido eliminado previamente")

    proceso_db.is_deleted = True
    proceso_db.deleted_by = usuario_admin.id
    proceso_db.deleted_at = datetime.now()
    
    db.commit()

    return None