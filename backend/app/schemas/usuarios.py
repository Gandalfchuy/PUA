from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

from app.schemas.mixins import CatalogoBase


class RolesCreate(CatalogoBase):
    descripcion: str = Field(..., min_length=2, max_length=250)


class RolesResponse(RolesCreate):
    id: int

    class Config:
        from_attributes = True

class UsuariosBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=250)
    correo: str = Field(..., min_length=2, max_length=250)
    nombre_completo: str = Field(..., min_length=2, max_length=250)
    is_active: bool
    ultimo_acceso: datetime
    created_at: datetime
    updated_at: datetime


class UsuariosCreate(UsuariosBase):
    rol_id:int
    hashed_password: str = Field(..., min_length=2, max_length=250)

class UsuariosResponse(UsuariosBase):
    id: int
    rol: Optional[RolesResponse]=None

    class Config:
        from_attributes = True
    
