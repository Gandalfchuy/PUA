from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from app.database import Base
from app.models.mixins import AuditMixin

class Sesion(AuditMixin, Base):
    __tablename__ = "sesion"

    folio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    objetivo = Column(Text, nullable=False)

class Grupo(AuditMixin, Base):
    __tablename__ = "grupo"

    folio = Column(Integer, primary_key=True, index=True)
    ubicacion = Column(Geography(geometry_type='POINT', srid=4326), nullable= False)
    lugar = Column(String(255), nullable=False)

class Lista(AuditMixin, Base):
    __tablename__ = "lista"

    id = Column(Integer, primary_key=True, index=True)
    agresor_id = Column(Integer, ForeignKey("agresor.folio"))
    grupo_id = Column(Integer, ForeignKey("grupo.folio"))
    sesion_id = Column(Integer, ForeignKey("sesion.folio"))
    fecha = Column(Date, nullable=False)

    agresor = relationship("Agresor", back_populates="asistencias")
    grupo = relationship("Grupo")
    sesion = relationship("Sesion")

class ProcesoReeducacion(AuditMixin, Base):
    __tablename__ = "procesoreeducacion"

    folio = Column(Integer, primary_key=True, index = True)
    agresor_id = Column(Integer, ForeignKey("agresor.folio"))
    fecha_inicio = Column(Date)
    fecha_termino = Column(Date)
    fecha_denuncia = Column(Date)
    denunciante = Column(String(255), nullable=False)
    folio_carpeta_fiscalia = Column(String(255))
    motivo_ingreso_id = Column(Integer, ForeignKey("motivoingreso.id"))
    tipo_violencia_id = Column(Integer, ForeignKey("tipoviolencia.id"))
    modalidad_violencia_id = Column(Integer, ForeignKey("modalidadviolencia.id"))

    agresor = relationship("Agresor", back_populates="proceso_reeducacion")
    motivo_ingreso = relationship("MotivoIngreso")
    tipo_violencia = relationship("TipoViolencia")
    modalidad_violencia = relationship("ModalidadViolencia")



