from pydantic import BaseModel, Field, field_validator 
from typing import List, Optional
from datetime import date
from app.schemas.mixins import AuditResponseMixin, AgresorBase, Coordenadas, ListaBase, ProcesoReeducacionBase
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement

from app.schemas.catalogos import (
    ModalidadViolenciaResponse,
    MotivoIngresoResponse,
    SectorSocialResponse, 
    AdiccionResponse, 
    TipoViolenciaResponse,
    ActividadRecreativaResponse,
    EstadoCivilResponse,
    GeneroMusicalResponse,
    RangoSalarialResponse,
    SituacionAcademicaResponse,
    SituacionLaboralResponse,
    SituacionViviendaResponse,
    TipoRelacionResponse,
    ReligionResponse
)
from app.schemas.procesos import GrupoResponse, SesionResponse

class ProcesoReeducacionLightResponse(ProcesoReeducacionBase):
    folio: int
    motivo_ingreso: Optional[MotivoIngresoResponse]=None
    tipo_violencia: Optional[TipoViolenciaResponse]=None
    modalidad_violencia: Optional[ModalidadViolenciaResponse]=None

    class Config:
        from_attributes = True

class ListaLightResponse(ListaBase):
    id: int
    grupo: Optional[GrupoResponse]=None
    sesion: Optional[SesionResponse]=None

    class Config:
        from_attributes = True

class AgresorCreate(AgresorBase):
    estado_civil_id: int
    situacion_academica_id: int
    situacion_laboral_id: int
    situacion_vivienda_id: int
    rango_salarial_id: int
    religion_id: int
    relacion_hijos_id: int
    
    sectores_sociales: List[int] = []
    actividades_recreativas: List[int] = []
    adicciones: List[int] = []
    generos_musicales: List[int] = []
    relacion_hermanos: List[int] = []
    relacion_padre: List[int] = []
    relacion_madre: List[int] = []
    violencia_infantil: List[int] = [] 



class AgresorResponse(AgresorBase, AuditResponseMixin):
    folio: int 
    
    estado_civil: Optional[EstadoCivilResponse]=None
    situacion_academica: Optional[SituacionAcademicaResponse]=None
    situacion_laboral: Optional[SituacionLaboralResponse]=None
    situacion_vivienda: Optional[SituacionViviendaResponse]=None
    rango_salarial: Optional[RangoSalarialResponse]=None
    religion: Optional[ReligionResponse]=None
    relacion_hijos: Optional[TipoRelacionResponse]=None

    sectores_sociales: List[SectorSocialResponse]=[]
    actividades_recreativas: List[ActividadRecreativaResponse]=[]
    adicciones: List[AdiccionResponse]=[]
    generos_musicales: List[GeneroMusicalResponse]=[]
    relacion_hermanos: List[TipoRelacionResponse]=[]
    relacion_padre: List[TipoRelacionResponse]=[]
    relacion_madre: List[TipoRelacionResponse]=[]
    violencia_infantil: List[TipoViolenciaResponse]=[]
    proceso_reeducacion: List[ProcesoReeducacionLightResponse]=[]
    asistencias:List[ListaLightResponse]=[]

    @field_validator('lugar_nacimiento', 'lugar_residencia', 'lugar_trabajo', mode='before')
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
