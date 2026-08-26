# app/routers/factory.py

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Type, Any
from pydantic import BaseModel
from app.database import get_db

from app.core.usuario import obtener_usuario_actual, VerificadorRol

requiere_admin = VerificadorRol(["SUPER_ADMIN"])

def crear_router_catalogo(
    modelo_db: Any,
    schema_entrada: Type[BaseModel],
    schema_salida: Type[BaseModel],
    prefijo: str,
    etiqueta: str
) -> APIRouter:
    
    router = APIRouter(prefix=prefijo, tags=[etiqueta])

    @router.post("", response_model=schema_salida, status_code=status.HTTP_201_CREATED)
    def crear(
        datos: schema_entrada, #type:ignore
        db: Session = Depends(get_db), 
        usuario_actual = Depends(obtener_usuario_actual)
    ): # type: ignore
        nuevo_registro = modelo_db(**datos.model_dump())

        if hasattr(nuevo_registro, 'created_by'):
            nuevo_registro.created_by = usuario_actual.id 

        if hasattr(nuevo_registro, 'created_at'):
            nuevo_registro.created_at = datetime.now()

        db.add(nuevo_registro)
        db.commit()
        db.refresh(nuevo_registro)
        return nuevo_registro

    @router.get("", response_model=List[schema_salida])
    def obtener_todos(
        incluir_inactivos: bool = False, 
        db: Session = Depends(get_db), 
        usuario_actual = Depends(obtener_usuario_actual)
    ):
        consulta = db.query(modelo_db)
        if hasattr(modelo_db, "is_deleted") and not incluir_inactivos:
            consulta = consulta.filter(modelo_db.is_deleted == False)
        return consulta.all()

    @router.get("/{id}", response_model=schema_salida)
    def obtener_por_id(
        id: int, 
        db: Session = Depends(get_db), 
        usuario_actual = Depends(obtener_usuario_actual)
    ):
        registro_db = db.query(modelo_db).filter(modelo_db.id == id).first()
        if not registro_db or (hasattr(registro_db, "is_deleted") and registro_db.is_deleted):
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return registro_db

    @router.put("/{id}", response_model=schema_salida)
    def actualizar(
        id: int, 
        datos: schema_entrada, #type:ignore
        db: Session = Depends(get_db),
        usuario_actual = Depends(obtener_usuario_actual)
    ): # type: ignore
        registro_db = db.query(modelo_db).filter(modelo_db.id == id).first()
        if not registro_db or (hasattr(registro_db, "is_deleted") and registro_db.is_deleted):
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        if hasattr(registro_db, 'updated_by'):
            registro_db.updated_by = usuario_actual.id 

        if hasattr(registro_db, 'updated_at'):
            registro_db.updated_at = datetime.now()
        
        for campo, valor in datos.model_dump().items():
            if hasattr(registro_db, campo) and campo != "id":
                setattr(registro_db, campo, valor)
            
        db.commit()
        db.refresh(registro_db)
        return registro_db

    @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
    def desactivar(
        id: int, 
        db: Session = Depends(get_db), 
        usuario_admin = Depends(requiere_admin)
    ):
        registro_db = db.query(modelo_db).filter(modelo_db.id == id).first()
        if not registro_db:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        if getattr(registro_db, "is_deleted", False):
            raise HTTPException(status_code=400, detail="El registro ya ha sido eliminado previamente")
        
        if hasattr(registro_db, "deleted_by"):
            registro_db.deleted_by = usuario_admin.id

        if hasattr(registro_db, "deleted_at"):
            registro_db.deleted_at = datetime.now()
        
        if hasattr(registro_db, "is_deleted"):
            registro_db.is_deleted = True

        if hasattr(registro_db, "activo"):
            registro_db.activo = False
            
        db.commit()
            
        return None

    return router