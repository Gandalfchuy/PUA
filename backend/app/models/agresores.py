from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Boolean, text
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from app.database import Base
from app.models.mixins import AuditMixin
from geoalchemy2.shape import to_shape

# Tablas pivote
agresor_sectorsocial = Table(
    'agresor_sectorsocial',
    Base.metadata,
    Column('agresor_folio', Integer, ForeignKey('agresor.folio'), primary_key=True),
    Column('sector_social_id', Integer, ForeignKey('sectorsocial.id'), primary_key=True)
)

agresor_actividadrecreativa = Table(
    'agresor_actividadrecreativa',
    Base.metadata,
    Column('agresor_folio', Integer, ForeignKey('agresor.folio'), primary_key=True),
    Column('actividad_id', Integer, ForeignKey('actividadrecreativa.id'), primary_key=True)
)

agresor_adiccion = Table(
    'agresor_adiccion',
    Base.metadata,
    Column('agresor_folio', Integer, ForeignKey('agresor.folio'), primary_key=True),
    Column('adiccion_id', Integer, ForeignKey('adiccion.id'), primary_key=True)
)

agresor_generomusical = Table(
    'agresor_generomusical',
    Base.metadata,
    Column('agresor_folio', Integer, ForeignKey('agresor.folio'), primary_key=True),
    Column('genero_id', Integer, ForeignKey('generomusical.id'), primary_key=True)
)

agresor_relacionhermanos = Table(
    'agresor_relacionhermanos',
    Base.metadata,
    Column('agresor_folio', Integer, ForeignKey('agresor.folio'), primary_key=True),
    Column('tipo_relacion_id', Integer, ForeignKey('tiporelacion.id'), primary_key=True)
)

agresor_relacionmadre = Table(
    'agresor_relacionmadre',
    Base.metadata,
    Column('agresor_folio', Integer, ForeignKey('agresor.folio'), primary_key=True),
    Column('tipo_relacion_id', Integer, ForeignKey('tiporelacion.id'), primary_key=True)
)

agresor_relacionpadre = Table(
    'agresor_relacionpadre',
    Base.metadata,
    Column('agresor_folio', Integer, ForeignKey('agresor.folio'), primary_key=True),
    Column('tipo_relacion_id', Integer, ForeignKey('tiporelacion.id'), primary_key=True)
)

agresor_tipoviolenciainfantil = Table(
    'agresor_tipoviolenciainfantil',
    Base.metadata,
    Column('agresor_folio', Integer, ForeignKey('agresor.folio'), primary_key=True),
    Column('tipo_violencia_id', Integer, ForeignKey('tipoviolencia.id'), primary_key=True)
)

class Agresor(AuditMixin, Base):
    __tablename__ = "agresor"

    folio = Column(Integer, primary_key=True, index=True)
    curp = Column(String(18), unique=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    apellido_paterno = Column(String(255), nullable=False)
    apellido_materno = Column(String(255), nullable=False)
    edad = Column(Integer, nullable=False)
    lugar_nacimiento = Column(Geography(geometry_type='POINT', srid=4326), nullable= False)
    lugar_residencia = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    lugar_trabajo = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    parejas_previas = Column(Integer, nullable=False)
    hijos = Column(Integer, nullable=False)
    hermanos = Column(Integer, nullable=False)
    estado_civil_id = Column(Integer, ForeignKey("estadocivil.id"))
    situacion_academica_id = Column(Integer, ForeignKey("situacionacademica.id"))
    situacion_laboral_id = Column(Integer, ForeignKey("situacionlaboral.id"))
    situacion_vivienda_id = Column(Integer, ForeignKey("situacionvivienda.id"))
    rango_salarial_id = Column(Integer, ForeignKey("rangosalarial.id"))
    religion_id = Column(Integer, ForeignKey("religion.id"))
    relacion_hijos_id = Column(Integer, ForeignKey("relacionhijos.id"))

    estado_civil = relationship("EstadoCivil")
    situacion_academica = relationship("SituacionAcademica")
    situacion_laboral = relationship("SituacionLaboral")
    situacion_vivienda = relationship("SituacionVivienda")
    rango_salarial = relationship("RangoSalarial")
    religion = relationship("Religion")
    relacion_hijos = relationship("RelacionHijos")

    sectores_sociales = relationship("SectorSocial", secondary=agresor_sectorsocial)
    actividades_recreativas = relationship("ActividadRecreativa", secondary=agresor_actividadrecreativa)
    adicciones = relationship("Adiccion", secondary=agresor_adiccion)
    generos_musicales = relationship("GeneroMusical", secondary=agresor_generomusical)
    relacion_hermanos = relationship("TipoRelacion", secondary=agresor_relacionhermanos)
    relacion_padre = relationship("TipoRelacion", secondary=agresor_relacionpadre)
    relacion_madre = relationship("TipoRelacion", secondary=agresor_relacionmadre)
    violencia_infantil = relationship("TipoViolencia", secondary=agresor_tipoviolenciainfantil)

    proceso_reeducacion = relationship("ProcesoReeducacion", back_populates="agresor")
    asistencias = relationship("Lista", back_populates="agresor")

    @property
    def coordenadas_nacimiento(self):
        if self.lugar_nacimiento is None:
            return None
        punto = to_shape(self.lugar_nacimiento)
        return {
            "latitud": punto.y,
            "longitud": punto.x
        }
    
    @property
    def coordenadas_residencia(self):
        if self.lugar_residencia is None:
            return None
        punto = to_shape(self.lugar_residencia)
        return {
            "latitud": punto.y,
            "longitud": punto.x
        }
    
    @property
    def coordenadas_trabajo(self):
        if self.lugar_trabajo is None:
            return None
        punto = to_shape(self.lugar_trabajo)
        return {
            "latitud": punto.y,
            "longitud": punto.x
        }