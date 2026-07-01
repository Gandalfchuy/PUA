from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class AuditResponseMixin(BaseModel):
    created_at:datetime
    updated_at:Optional[datetime]=None
    deleted_at:Optional[datetime]=None
    is_deleted:bool

    created_by:Optional[int]=None
    updated_by:Optional[int]=None
    deleted_by:Optional[int]=None

class CatalogoBase(BaseModel):
    nombre:str=Field(...,min_length=2,max_length=100)
    activo:bool = True

class CatalogoResponse(CatalogoBase, AuditResponseMixin):
    id: int
    class Config:
        from_attributes = True

class Coordenadas(BaseModel):
    latitud: float
    longitud: float

class AgresorBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    apellido_paterno: str = Field(..., min_length=2, max_length=150)
    apellido_materno: Optional[str] = None
    curp: str = Field(..., min_length=18, max_length=18, pattern="^[A-Z0-9]{18}$")
    edad:int
    lugar_nacimiento: Optional[Coordenadas]=None
    lugar_residencia: Optional[Coordenadas]=None
    lugar_trabajo: Optional[Coordenadas]=None
    parejas_previas:int
    hijos: int
    hermanos: int

class ListaBase(BaseModel):
    fecha: date

class ProcesoReeducacionBase(BaseModel):
    fecha_inicio: date
    fecha_termino: Optional[date]=None
    fecha_denuncia: Optional[date]=None
    denunciante: str = Field(..., min_length=2, max_length=150)
    folio_carpeta_fiscalia: str = Field(..., min_length=2, max_length=150)

class UsuariosBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=250)
    correo: str = Field(..., min_length=2, max_length=250)
    nombre_completo: str = Field(..., min_length=2, max_length=250)
    is_active: bool
    ultimo_acceso: datetime
    created_at: datetime
    updated_at: datetime
