from app.database import Base
from app.models.mixins import AuditMixin, CatalogoMixin

class ActividadRecreativa(AuditMixin,CatalogoMixin,Base):
    __tablename__="actividadrecreativa"

class Adiccion(AuditMixin,CatalogoMixin,Base):
    __tablename__="adiccion"

class EstadoCivil(AuditMixin,CatalogoMixin,Base):
    __tablename__="estadocivil"

class GeneroMusical(AuditMixin,CatalogoMixin,Base):
    __tablename__="generomusical"

class ModalidadViolencia(AuditMixin,CatalogoMixin,Base):
    __tablename__="modalidadviolencia"

class MotivoIngreso(AuditMixin,CatalogoMixin,Base):
    __tablename__="motivoingreso"

class RangoSalarial(AuditMixin,CatalogoMixin,Base):
    __tablename__="rangosalarial"

class RelacionHijos(AuditMixin,CatalogoMixin,Base):
    __tablename__="relacionhijos"

class Religion(AuditMixin,CatalogoMixin,Base):
    __tablename__="religion"

class SectorSocial(AuditMixin,CatalogoMixin,Base):
    __tablename__="sectorsocial"

class SituacionAcademica(AuditMixin,CatalogoMixin,Base):
    __tablename__="situacionacademica"

class SituacionLaboral(AuditMixin,CatalogoMixin,Base):
    __tablename__="situacionlaboral"

class SituacionVivienda(AuditMixin,CatalogoMixin,Base):
    __tablename__="situacionvivienda"

class TipoRelacion(AuditMixin,CatalogoMixin,Base):
    __tablename__="tiporelacion"

class TipoViolencia(AuditMixin,CatalogoMixin,Base):
    __tablename__="tipoviolencia"

