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

@router_lista.get("/grupos/{id_grupo}/lista", response_model=List[ListaResponse])
def obtener_listas_por_grupo_y_fecha(
    id_grupo: int, 
    fecha_exacta: Optional[date] = Query(None, description="Día específico YYYY-MM-DD"),
    mes: Optional[int] = Query(None, ge=1, le=12, description="Mes numérico (1-12)"),
    anio: Optional[int] = Query(None, description="Año (ej. 2026)"),
    db: Session = Depends(get_db),
    usuario_actual = Depends(obtener_usuario_actual)
):
    consulta = db.query(Lista).filter(Lista.grupo_id == id_grupo)
                 

    if fecha_exacta:
        consulta = consulta.filter(Lista.fecha == fecha_exacta)
        
    elif mes and anio:
        consulta = consulta.filter(
            extract('month', Lista.fecha) == mes,
            extract('year', Lista.fecha) == anio
        )
        
    elif mes and not anio:
        consulta = consulta.filter(
            extract('month', Lista.fecha) == mes,
            extract('year', Lista.fecha) == date.today().year
        )

    resultados = consulta.all()
    
    if not resultados:
        raise HTTPException(
            status_code=404, 
            detail=f"No se encontraron listas para el grupo {id_grupo} en la fecha especificada."
        )

    return resultados

