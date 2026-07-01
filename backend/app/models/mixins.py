from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, text
from sqlalchemy.orm import declared_attr

class AuditMixin:
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)

    @declared_attr
    def created_by(cls):
        return Column(Integer, ForeignKey('usuarios.id'), nullable=True)

    @declared_attr
    def updated_by(cls):
        return Column(Integer, ForeignKey('usuarios.id'), nullable=True)

    @declared_attr
    def deleted_by(cls):
        return Column(Integer, ForeignKey('usuarios.id'), nullable=True)

# ==========================================
# NUEVO: Mixin para Catálogos
# ==========================================

class CatalogoMixin:
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), unique=True, nullable=False)
    activo = Column(Boolean, default=True)