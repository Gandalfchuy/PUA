# app/routers/catalogos.py

# 1. Importas tu fábrica
from app.routers.factory import crear_router_catalogo

# 2. Importas tus Bóvedas (Modelos)
from app.models.catalogos import (
    Adiccion, 
    EstadoCivil, 
    SectorSocial, 
    SituacionAcademica,
    ActividadRecreativa,
    GeneroMusical,
    ModalidadViolencia,
    MotivoIngreso,
    RangoSalarial,
    Religion,
    RelacionHijos,
    SituacionLaboral,
    SituacionVivienda,
    TipoRelacion,
    TipoViolencia)

# 3. Importas tus Cadeneros (Schemas)
from app.schemas.catalogos import (
    AdiccionCreate, AdiccionResponse,
    EstadoCivilCreate, EstadoCivilResponse,
    SectorSocialCreate, SectorSocialResponse,
    SituacionAcademicaCreate,SituacionAcademicaResponse,
    ActividadRecreativaCreate, ActividadRecreativaResponse,
    GeneroMusicalCreate, GeneroMusicalResponse,
    ModalidadViolenciaCreate,ModalidadViolenciaResponse,
    MotivoIngresoCreate,MotivoIngresoResponse,
    RangoSalarialCreate, RangoSalarialResponse,
    ReligionCreate, ReligionResponse,
    RelacionHijosCreate, RelacionHijosResponse,
    SituacionLaboralCreate, SituacionLaboralResponse,
    SituacionViviendaCreate, SituacionViviendaResponse,
    TipoRelacionCreate, TipoRelacionResponse,
    TipoViolenciaCreate, TipoViolenciaResponse 
)

# ==========================================
# AQUÍ LLAMAMOS A LA FUNCIÓN (Fabricamos las regletas)
# ==========================================

router_adicciones = crear_router_catalogo(
    modelo_db=Adiccion,
    schema_entrada=AdiccionCreate,
    schema_salida=AdiccionResponse,
    prefijo="/catalogos/adicciones",
    etiqueta="Catálogos - Adicciones"
)

router_estado_civil = crear_router_catalogo(
    modelo_db=EstadoCivil,
    schema_entrada=EstadoCivilCreate,
    schema_salida=EstadoCivilResponse,
    prefijo="/catalogos/estado-civil",
    etiqueta="Catálogos - Estado Civil"
)

router_sectores_sociales = crear_router_catalogo(
    modelo_db=SectorSocial,
    schema_entrada=SectorSocialCreate,
    schema_salida=SectorSocialResponse,
    prefijo="/catalogos/sectores-sociales",
    etiqueta="Catálogos - Sectores Sociales"
)

router_situacion_academica = crear_router_catalogo(
    modelo_db=SituacionAcademica,
    schema_entrada=SituacionAcademicaCreate,
    schema_salida=SituacionAcademicaResponse,
    prefijo="/catalogos/situacion-academica",
    etiqueta="Catálogos - Situación Académica"
)

router_actividad_recreativa = crear_router_catalogo(
    modelo_db=ActividadRecreativa,
    schema_entrada=ActividadRecreativaCreate,
    schema_salida=ActividadRecreativaResponse,
    prefijo="/catalogos/actividad-recreativa",
    etiqueta="Catálogos - Actividad Recreativa"
)

router_genero_musical = crear_router_catalogo(
    modelo_db=GeneroMusical,
    schema_entrada=GeneroMusicalCreate,
    schema_salida=GeneroMusicalResponse,
    prefijo="/catalogos/genero-musical",
    etiqueta="Catálogos - Género Musical"
)

router_modalidad_violencia = crear_router_catalogo(
    modelo_db=ModalidadViolencia,
    schema_entrada=ModalidadViolenciaCreate,
    schema_salida=ModalidadViolenciaResponse,
    prefijo="/catalogos/modalidad-violencia",
    etiqueta="Catálogos - Modalidad Violencia"
)

router_motivo_ingreso = crear_router_catalogo(
    modelo_db=MotivoIngreso,
    schema_entrada=MotivoIngresoCreate,
    schema_salida=MotivoIngresoResponse,
    prefijo="/catalogos/motivo-ingreso",
    etiqueta="Catálogos - Motivo Ingreso"
)

router_rango_salarial = crear_router_catalogo(
    modelo_db=RangoSalarial,
    schema_entrada=RangoSalarialCreate,
    schema_salida=RangoSalarialResponse,
    prefijo="/catalogos/rango-salarial",
    etiqueta="Catálogos - Rango Salarial"
)

router_religion = crear_router_catalogo(
    modelo_db=Religion,
    schema_entrada=ReligionCreate,
    schema_salida=ReligionResponse,
    prefijo="/catalogos/religion",
    etiqueta="Catálogos - Religión"
)

router_relacion_hijos = crear_router_catalogo(
    modelo_db=RelacionHijos,
    schema_entrada=RelacionHijosCreate,
    schema_salida=RelacionHijosResponse,
    prefijo="/catalogos/relacion-hijos",
    etiqueta="Catálogos - Relación Hijos"
)

router_situacion_laboral = crear_router_catalogo(
    modelo_db=SituacionLaboral,
    schema_entrada=SituacionLaboralCreate,
    schema_salida=SituacionLaboralResponse,
    prefijo="/catalogos/situacion-laboral",
    etiqueta="Catálogos - Situación Laboral"
)

router_situacion_academica = crear_router_catalogo(
    modelo_db=SituacionAcademica,
    schema_entrada=SituacionAcademicaCreate,
    schema_salida=SituacionAcademicaResponse,
    prefijo="/catalogos/situacion-academica",
    etiqueta="Catálogos - Situación Académica"
)

router_situacion_vivienda = crear_router_catalogo(
    modelo_db=SituacionVivienda,
    schema_entrada=SituacionViviendaCreate,
    schema_salida=SituacionViviendaResponse,
    prefijo="/catalogos/situacion-vivienda",
    etiqueta="Catálogos - Situación Vivienda"
)

router_tipo_relacion = crear_router_catalogo(
    modelo_db=TipoRelacion,
    schema_entrada=TipoRelacionCreate,
    schema_salida=TipoRelacionResponse,
    prefijo="/catalogos/tipo-relacion",
    etiqueta="Catálogos - Tipo Relación"
)

router_tipo_violencia = crear_router_catalogo(
    modelo_db=TipoViolencia,
    schema_entrada=TipoViolenciaCreate,
    schema_salida=TipoViolenciaResponse,
    prefijo="/catalogos/tipo-violencia",
    etiqueta="Catálogos - Tipo Violencia"
)