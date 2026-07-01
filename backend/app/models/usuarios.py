from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.mixins import CatalogoMixin


class Roles(CatalogoMixin, Base):
    __tablename__ = "roles"
    
    descripcion = Column(String(255), nullable=True)



class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    correo = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    nombre_completo = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=True)
    ultimo_acceso = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), onupdate=text('CURRENT_TIMESTAMP'))

    rol = relationship("Roles")