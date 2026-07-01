from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, date
from app.schemas.mixins import AgresorBase, AuditResponseMixin, Coordenadas,  ListaBase, ProcesoReeducacionBase
from app.schemas.catalogos import TipoViolenciaResponse, ModalidadViolenciaResponse, MotivoIngresoResponse

class AgresorLightResponse(AgresorBase):
    folio:int

    @field_validator('lugar_nacimiento', 'lugar_residencia', 'lugar_trabajo', mode='before')
    @classmethod
    def decodificar_postgis(cls, valor):
        if isinstance(valor, WKBElement):
            punto = to_shape(valor)
            return {"latitud": punto.y, "longitud": punto.x}
        return valor


class SesionCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=250)
    objetivo: str = Field(..., min_length=2, max_length=250)

class SesionResponse(SesionCreate,AuditResponseMixin):
    folio: int

    class Config:
        from_attributes = True


class GrupoCreate(BaseModel):
    ubicacion: Optional[Coordenadas]=None
    lugar: str = Field(..., min_length=2, max_length=250)

class GrupoResponse(GrupoCreate,AuditResponseMixin):
    folio: int

    @field_validator('ubicacion', mode='before')
    @classmethod
    def decodificar_postgis(cls, valor):
        if isinstance(valor, WKBElement):
            punto = to_shape(valor)
            
            return {
                "latitud": punto.y, 
                "longitud": punto.x
            }
        return valor
    
    class Config:
        from_attributes = True


class ListaCreate(ListaBase):
    agresor_id: int
    grupo_id: int
    sesion_id: int

class ListaResponse(ListaBase, AuditResponseMixin):
    id: int

    agresor: Optional[AgresorLightResponse]=None
    grupo: Optional[GrupoResponse]=None
    sesion: Optional[SesionResponse]=None

    class Config:
        from_attributes = True

class ProcesoReeducacionCreate(ProcesoReeducacionBase):
    agresor_id: int
    motivo_ingreso_id: int
    tipo_violencia_id: int
    modalidad_violencia_id: int

class ProcesoReeducacionResponse(ProcesoReeducacionBase, AuditResponseMixin):
    folio: int

    agresor: Optional[AgresorLightResponse]=None
    motivo_ingreso: Optional[MotivoIngresoResponse]=None
    tipo_violencia: Optional[TipoViolenciaResponse]=None
    modalidad_violencia: Optional[ModalidadViolenciaResponse]=None 

    class Config:
        from_attributes = True






