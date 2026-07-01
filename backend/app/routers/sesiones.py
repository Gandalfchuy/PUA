from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.procesos import Sesion
from app.schemas.procesos import SesionResponse, SesionCreate
from app.core.usuario import VerificadorRol, obtener_usuario_actual

requiere_admin = VerificadorRol(["SUPER_ADMIN"])

router_sesion = APIRouter(prefix ="/sesiones", tags=["Sesiones"])

@router_sesion.post("/", response_model=SesionResponse, status_code=status.HTTP_201_CREATED)
def crear_sesion(datos:SesionCreate, db:Session = Depends(get_db), usuario_id: int = Depends(obtener_usuario_actual)): 

    nueva_sesion=Sesion(**datos.model_dump())

    nueva_sesion.created_by = usuario_id.id
    nueva_sesion.created_at = datetime.now()
    
    db.add(nueva_sesion)
    db.commit()
    db.refresh(nueva_sesion)

    return nueva_sesion

@router_sesion.get("/", response_model=List[SesionResponse])
def listar_sesion(db: Session = Depends(get_db), usuario_id: int = Depends(obtener_usuario_actual)):
    
    sesion_db = db.query(Sesion).filter(Sesion.is_deleted == False).all()
    
    return sesion_db

@router_sesion.put("/{sesion_id}", response_model=SesionResponse)
def actualizar_sesion(sesion_id: int, datos: SesionCreate, db: Session = Depends(get_db), usuario_id: int = Depends(obtener_usuario_actual)):

    sesion_db = db.query(Sesion).filter(Sesion.folio== sesion_id, Sesion.is_deleted == False).first()
    
    if not sesion_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El grupo no existe o fue eliminado"
        )

    datos_completos = datos.model_dump()

    for llave, valor in datos_completos.items():
        setattr(sesion_db, llave, valor)

    sesion_db.updated_by = usuario_id.id
    sesion_db.updated_at = datetime.now()

    db.commit()
    db.refresh(sesion_db)

    return sesion_db

@router_sesion.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_sesion(id: int, db: Session = Depends(get_db), usuario_id: int = Depends(requiere_admin)):

    sesion_db = db.query(Sesion).filter(Sesion.folio == id).first()
    
    if not sesion_db:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
        
    if not sesion_db.is_deleted:
        raise HTTPException(status_code=400, detail="Grupo eliminado")

    sesion_db.is_deleted = True
    
    sesion_db.deleted_by = usuario_id.id
    sesion_db.deleted_at = datetime.now()
    
    db.commit()

    return None