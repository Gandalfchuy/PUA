from fastapi import APIRouter, Depends, HTTPException, status
from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.procesos import Grupo
from app.schemas.procesos import GrupoResponse, GrupoCreate
from app.core.usuario import VerificadorRol, obtener_usuario_actual

requiere_admin = VerificadorRol(["SUPER_ADMIN"])

router_grupo = APIRouter(prefix ="/grupos", tags=["Grupos"])

@router_grupo.post("/", response_model=GrupoResponse, status_code=status.HTTP_201_CREATED)
def crear_grupo(datos:GrupoCreate, db:Session = Depends(get_db), usuario_id: int = Depends(obtener_usuario_actual)): 

    nuevo_grupo=Grupo(**datos.model_dump())

    if datos.ubicacion:
        lon = datos.ubicacion.longitud
        lat = datos.ubicacion.latitud
        nuevo_grupo.ubicacion = WKTElement(f"POINT({lon} {lat})", srid=4326)

    nuevo_grupo.created_by = usuario_id.id
    nuevo_grupo.created_at = datetime.now()

    db.add(nuevo_grupo)
    db.commit()
    db.refresh(nuevo_grupo)

    return nuevo_grupo

@router_grupo.get("/", response_model=List[GrupoResponse])
def listar_grupos(db: Session = Depends(get_db), usuario_id: int = Depends(obtener_usuario_actual)):
    
    grupos_db = db.query(Grupo).filter(Grupo.is_deleted == False).all()
    
    return grupos_db

@router_grupo.put("/{grupo_id}", response_model=GrupoResponse)
def actualizar_grupo(grupo_id: int, datos: GrupoCreate, db: Session = Depends(get_db), usuario_id: int = Depends(obtener_usuario_actual)):

    grupo_db = db.query(Grupo).filter(Grupo.folio== grupo_id, Grupo.is_deleted == False).first()
    
    if not grupo_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El grupo no existe o fue eliminado"
        )

    datos_completos = datos.model_dump()

    for llave, valor in datos_completos.items():
        setattr(grupo_db, llave, valor)

    grupo_db.updated_by = usuario_id.id
    grupo_db.updated_at = datetime.now()

    if datos.ubicacion:
        lon = datos.ubicacion.longitud
        lat = datos.ubicacion.latitud
        grupo_db.ubicacion = WKTElement(f"POINT({lon} {lat})", srid=4326)


    db.commit()
    db.refresh(grupo_db)

    return grupo_db

@router_grupo.delete("/{folio}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_grupo(folio: int, db: Session = Depends(get_db), usuario_id: int = Depends(requiere_admin)):

    grupo_db = db.query(Grupo).filter(Grupo.folio == folio).first()

    if not grupo_db:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        # Corrección aplicada a las asignaciones de campos
    if hasattr(grupo_db, "deleted_by"):
            grupo_db.deleted_by = usuario_id.id

    if hasattr(grupo_db, "deleted_at"):
            grupo_db.deleted_at = datetime.now()
        
    if hasattr(grupo_db, "is_deleted"):
            grupo_db.is_deleted = True
            db.commit()
            
    return None

