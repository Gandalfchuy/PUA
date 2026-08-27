from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class DashboardKpisResponse(BaseModel):
    total_activos: int
    tasa_asistencia: float
    alertas_desercion: int
    procesos_concluidos: int

class PuntoCalor(BaseModel):
    lat: float
    lng: float
    peso: float = 1.0

class SedeMapa(BaseModel):
    folio: int
    lugar: str
    lat: float
    lng: float

class DashboardMapaResponse(BaseModel):
    puntos_calor: List[PuntoCalor]
    sedes: List[SedeMapa]

class TipoViolenciaStat(BaseModel):
    tipo: str
    total: int
    porcentaje: float

class DashboardViolenciaResponse(BaseModel):
    tipos: List[TipoViolenciaStat]

class AdiccionStat(BaseModel):
    adiccion: str
    total: int
    porcentaje: float

class DashboardAdiccionesResponse(BaseModel):
    adicciones: List[AdiccionStat]

class AlertaDesercionItem(BaseModel):
    agresor_id: int
    curp: str
    nombre_completo: str
    grupo: Optional[str] = None
    faltas_consecutivas: int
    ultima_asistencia: Optional[date] = None
    carpeta_fiscalia: Optional[str] = None

class DashboardAlertasResponse(BaseModel):
    alertas: List[AlertaDesercionItem]
