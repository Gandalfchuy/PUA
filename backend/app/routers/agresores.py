from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement
from typing import List 
from app.database import get_db
from app.models.agresores import Agresor
from app.models.catalogos import Adiccion, TipoViolencia, SectorSocial, ActividadRecreativa, GeneroMusical, TipoRelacion
from app.models.usuarios import Usuarios
from app.schemas.agresores import AgresorCreate, AgresorResponse
from app.core.usuario import obtener_usuario_actual, VerificadorRol

requiere_admin = VerificadorRol(["SUPER_ADMIN"])

router_agresor = APIRouter(prefix="/agresores", tags=["Agresores"])

@router_agresor.post("/", response_model=AgresorResponse, status_code=status.HTTP_201_CREATED)
def crear_agresor(datos: AgresorCreate, db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):

    if datos.curp:
        agresor_duplicado = db.query(Agresor).filter(Agresor.curp == datos.curp).first()
        if agresor_duplicado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Ya se encuentra registrado un expediente con el CURP: {datos.curp}")
    
    datos_dic = datos.model_dump(
        exclude={"lugar_nacimiento",
                 "lugar_residencia",
                 "lugar_trabajo",
                 "adicciones",
                 "sectores_sociales",
                 "actividades_recreativas",
                 "generos_musicales",
                 "relacion_hermanos",
                 "relacion_padre",
                 "relacion_madre",
                 "violencia_infantil"
                                })

    
    nuevo_agresor = Agresor(**datos_dic)

    if datos.lugar_nacimiento:
        lon = datos.lugar_nacimiento.longitud
        lat = datos.lugar_nacimiento.latitud
        nuevo_agresor.lugar_nacimiento = WKTElement(f"POINT({lon} {lat})", srid=4326)

    if datos.lugar_trabajo:
        lon = datos.lugar_trabajo.longitud
        lat = datos.lugar_trabajo.latitud
        nuevo_agresor.lugar_trabajo = WKTElement(f"POINT({lon} {lat})", srid=4326)

    if datos.lugar_residencia:
        lon = datos.lugar_residencia.longitud
        lat = datos.lugar_residencia.latitud
        nuevo_agresor.lugar_residencia = WKTElement(f"POINT({lon} {lat})", srid=4326)

    if datos.adicciones:
        adicciones_db = db.query(Adiccion).filter(Adiccion.id.in_(datos.adicciones)).all()
        nuevo_agresor.adicciones = adicciones_db
    
    if datos.sectores_sociales:
        sectores_sociales_db = db.query(SectorSocial).filter(SectorSocial.id.in_(datos.sectores_sociales)).all()
        nuevo_agresor.sectores_sociales = sectores_sociales_db

    if datos.actividades_recreativas:
        actividades_recreativas_db = db.query(ActividadRecreativa).filter(ActividadRecreativa.id.in_(datos.actividades_recreativas)).all()
        nuevo_agresor.actividades_recreativas = actividades_recreativas_db

    if datos.generos_musicales:
        generos_musicales_db = db.query(GeneroMusical).filter(GeneroMusical.id.in_(datos.generos_musicales)).all()
        nuevo_agresor.generos_musicales = generos_musicales_db
    
    if datos.relacion_hermanos:
        relacion_hermanos_db = db.query(TipoRelacion).filter(TipoRelacion.id.in_(datos.relacion_hermanos)).all()
        nuevo_agresor.relacion_hermanos = relacion_hermanos_db

    if datos.relacion_padre:
        relacion_padre_db = db.query(TipoRelacion).filter(TipoRelacion.id.in_(datos.relacion_padre)).all()
        nuevo_agresor.relacion_padre = relacion_padre_db

    if datos.relacion_madre:
        relacion_madre_db = db.query(TipoRelacion).filter(TipoRelacion.id.in_(datos.relacion_madre)).all()
        nuevo_agresor.relacion_madre = relacion_madre_db

    if datos.violencia_infantil:
        violencia_db = db.query(TipoViolencia).filter(TipoViolencia.id.in_(datos.violencia_infantil)).all()
        nuevo_agresor.violencia_infantil = violencia_db

    nuevo_agresor.created_by = usuario_actual.id
    nuevo_agresor.created_at = datetime.now()

    db.add(nuevo_agresor)
    db.commit()
    db.refresh(nuevo_agresor)

    return nuevo_agresor


@router_agresor.get("/{folio}", response_model=AgresorResponse)
def obtener_agresor(folio: int, db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    agresor_db = db.query(Agresor).filter(Agresor.folio == folio, Agresor.is_deleted == False).first()
    
    if not agresor_db:
        raise HTTPException(status_code=404, detail="Agresor no encontrado")
        
    return agresor_db


@router_agresor.get("/", response_model=List[AgresorResponse])
def obtener_agresores(db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    agresores_db = db.query(Agresor).filter(Agresor.is_deleted == False).all()
    
    return agresores_db



@router_agresor.put("/{folio}", response_model=AgresorResponse)
def actualizar_agresor(folio: int, datos: AgresorCreate, db: Session = Depends(get_db), usuario_actual: Usuarios = Depends(obtener_usuario_actual)):
    agresor_db = db.query(Agresor).filter(Agresor.folio == folio, Agresor.is_deleted == False).first()
    if not agresor_db:
        raise HTTPException(status_code=404, detail="Agresor no encontrado")
        
    datos_dic = datos.model_dump(
        exclude={"lugar_nacimiento",
                 "lugar_residencia",
                 "lugar_trabajo",
                 "adicciones",
                 "sectores_sociales",
                 "actividades_recreativas",
                 "generos_musicales",
                 "relacion_hermanos",
                 "relacion_padre",
                 "relacion_madre",
                 "violencia_infantil"
                                })
    for campo, valor in datos_dic.items():
        setattr(agresor_db, campo, valor)

    if datos.lugar_nacimiento:
        lon = datos.lugar_nacimiento.longitud
        lat = datos.lugar_nacimiento.latitud
        agresor_db.lugar_nacimiento = WKTElement(f"POINT({lon} {lat})", srid=4326)

    if datos.lugar_trabajo:
        lon = datos.lugar_trabajo.longitud
        lat = datos.lugar_trabajo.latitud
        agresor_db.lugar_trabajo = WKTElement(f"POINT({lon} {lat})", srid=4326)

    if datos.lugar_residencia:
        lon = datos.lugar_residencia.longitud
        lat = datos.lugar_residencia.latitud
        agresor_db.lugar_residencia = WKTElement(f"POINT({lon} {lat})", srid=4326)

    if datos.adicciones:
        adicciones_db = db.query(Adiccion).filter(Adiccion.id.in_(datos.adicciones)).all()
        agresor_db.adicciones = adicciones_db
    
    if datos.sectores_sociales:
        sectores_sociales_db = db.query(SectorSocial).filter(SectorSocial.id.in_(datos.sectores_sociales)).all()
        agresor_db.sectores_sociales = sectores_sociales_db

    if datos.actividades_recreativas:
        actividades_recreativas_db = db.query(ActividadRecreativa).filter(ActividadRecreativa.id.in_(datos.actividades_recreativas)).all()
        agresor_db.actividades_recreativas = actividades_recreativas_db

    if datos.generos_musicales:
        generos_musicales_db = db.query(GeneroMusical).filter(GeneroMusical.id.in_(datos.generos_musicales)).all()
        agresor_db.generos_musicales = generos_musicales_db
    
    if datos.relacion_hermanos:
        relacion_hermanos_db = db.query(TipoRelacion).filter(TipoRelacion.id.in_(datos.relacion_hermanos)).all()
        agresor_db.relacion_hermanos = relacion_hermanos_db

    if datos.relacion_padre:
        relacion_padre_db = db.query(TipoRelacion).filter(TipoRelacion.id.in_(datos.relacion_padre)).all()
        agresor_db.relacion_padre = relacion_padre_db

    if datos.relacion_madre:
        relacion_madre_db = db.query(TipoRelacion).filter(TipoRelacion.id.in_(datos.relacion_madre)).all()
        agresor_db.relacion_madre = relacion_madre_db

    if datos.violencia_infantil:
        violencia_db = db.query(TipoViolencia).filter(TipoViolencia.id.in_(datos.violencia_infantil)).all()
        agresor_db.violencia_infantil = violencia_db

    agresor_db.updated_by = usuario_actual.id
    agresor_db.updated_at = datetime.now()

    db.commit()
    db.refresh(agresor_db)
    
    return agresor_db

@router_agresor.delete("/{folio}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_agresor(folio: int, db: Session = Depends(get_db), usuario_admin: Usuarios = Depends(requiere_admin)):

    agresor_db = db.query(Agresor).filter(Agresor.folio == folio).first()
    
    if not agresor_db:
        raise HTTPException(status_code=404, detail="Agresor no encontrado")
        
    if agresor_db.is_deleted:
        raise HTTPException(status_code=400, detail="El agresor ya ha sido eliminado previamente")

    agresor_db.is_deleted = True
    agresor_db.deleted_by = usuario_admin.id 
    agresor_db.deleted_at = datetime.now()
    
    db.commit()

    return None