-- ==========================================
-- 0. HABILITAR EXTENSIÓN ESPACIAL
-- ==========================================
-- Requerido para usar los campos GEOGRAPHY
CREATE EXTENSION IF NOT EXISTS postgis;

-- ==========================================
-- 1. GESTIÓN DE ACCESO Y AUDITORÍA
-- ==========================================
-- Se crean primero para poder referenciarlas en los campos created_by, updated_by

CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  descripcion TEXT,
  activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  nombre_completo VARCHAR(255) NOT NULL,
  correo VARCHAR(255) UNIQUE NOT NULL,
  rol_id INT NOT NULL REFERENCES roles(id),
  ultimo_acceso TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

-- ==========================================
-- 2. TABLAS CATÁLOGO (Select Simple & Multiselect)
-- ==========================================

CREATE TABLE estadocivil (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE relacionhijos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE situacionacademica (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE situacionlaboral (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE situacionvivienda (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE rangosalarial (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE religion (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE tiporelacion (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE adiccion (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE sectorsocial (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE actividadrecreativa (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE generomusical (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE motivoingreso (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE tipoviolencia (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE modalidadviolencia (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) UNIQUE NOT NULL,
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

-- ==========================================
-- 3. ENTIDAD PRINCIPAL: AGRESOR
-- ==========================================

CREATE TABLE agresor (
  folio SERIAL PRIMARY KEY,
  curp VARCHAR(18) UNIQUE NOT NULL,
  nombre VARCHAR(255) NOT NULL,
  apellido_paterno VARCHAR(255) NOT NULL,
  apellido_materno VARCHAR(255) NOT NULL,
  edad INT NOT NULL,
  
  -- Campos geográficos (PostGIS)
  lugar_nacimiento GEOGRAPHY(Point, 4326),
  lugar_residencia GEOGRAPHY(Point, 4326),
  lugar_trabajo GEOGRAPHY(Point, 4326),
  
  parejas_previas INT NOT NULL,
  hijos INT NOT NULL,
  hermanos INT NOT NULL,
  
  estado_civil_id INT REFERENCES estadocivil(id),
  situacion_academica_id INT REFERENCES situacionacademica(id),
  situacion_laboral_id INT REFERENCES situacionlaboral(id),
  situacion_vivienda_id INT REFERENCES situacionvivienda(id),
  rango_salarial_id INT REFERENCES rangosalarial(id),
  religion_id INT REFERENCES religion(id),
  relacion_hijos_id INT REFERENCES relacionhijos(id),
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

-- ==========================================
-- 4. TABLAS INTERMEDIAS (Muchos a Muchos)
-- ==========================================

CREATE TABLE agresor_adiccion (
  agresor_folio INT REFERENCES agresor(folio),
  adiccion_id INT REFERENCES adiccion(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (agresor_folio, adiccion_id)
);

CREATE TABLE agresor_tipoviolenciainfantil (
  agresor_folio INT REFERENCES agresor(folio),
  tipo_violencia_id INT REFERENCES tipoviolencia(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (agresor_folio, tipo_violencia_id)
);

CREATE TABLE agresor_relacionpadre (
  agresor_folio INT REFERENCES agresor(folio),
  tipo_relacion_id INT REFERENCES tiporelacion(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (agresor_folio, tipo_relacion_id)
);

CREATE TABLE agresor_relacionmadre (
  agresor_folio INT REFERENCES agresor(folio),
  tipo_relacion_id INT REFERENCES tiporelacion(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (agresor_folio, tipo_relacion_id)
);

CREATE TABLE agresor_relacionhermanos (
  agresor_folio INT REFERENCES agresor(folio),
  tipo_relacion_id INT REFERENCES tiporelacion(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (agresor_folio, tipo_relacion_id)
);

CREATE TABLE agresor_sectorsocial (
  agresor_folio INT REFERENCES agresor(folio),
  sector_social_id INT REFERENCES sectorsocial(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (agresor_folio, sector_social_id)
);

CREATE TABLE agresor_actividadrecreativa (
  agresor_folio INT REFERENCES agresor(folio),
  actividad_id INT REFERENCES actividadrecreativa(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (agresor_folio, actividad_id)
);

CREATE TABLE agresor_generomusical (
  agresor_folio INT REFERENCES agresor(folio),
  genero_id INT REFERENCES generomusical(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (agresor_folio, genero_id)
);

-- ==========================================
-- 5. TABLAS DE PROCESO DE REEDUCACIÓN
-- ==========================================

CREATE TABLE procesoreeducacion (
  folio SERIAL PRIMARY KEY,
  agresor_id INT NOT NULL REFERENCES agresor(folio),
  fecha_inicio TIMESTAMP NOT NULL,
  fecha_termino TIMESTAMP,
  fecha_denuncia TIMESTAMP,
  denunciante VARCHAR(255) NOT NULL,
  folio_carpeta_fiscalia VARCHAR(255) NOT NULL,
  
  motivo_ingreso_id INT REFERENCES motivoingreso(id),
  tipo_violencia_id INT REFERENCES tipoviolencia(id),
  modalidad_violencia_id INT REFERENCES modalidadviolencia(id),
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE grupo (
  folio SERIAL PRIMARY KEY,
  -- Campo geográfico para el lugar de reunión
  ubicacion GEOGRAPHY(Point, 4326),
  lugar VARCHAR(255) NOT NULL,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE sesion (
  folio SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  objetivo TEXT NOT NULL,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE lista (
  id SERIAL PRIMARY KEY,
  agresor_id INT NOT NULL REFERENCES agresor(folio),
  grupo_id INT NOT NULL REFERENCES grupo(folio),
  sesion_id INT NOT NULL REFERENCES sesion(folio),
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INT REFERENCES usuarios(id),
  updated_by INT REFERENCES usuarios(id),
  deleted_at TIMESTAMP,
  deleted_by INT REFERENCES usuarios(id),
  is_deleted BOOLEAN DEFAULT FALSE
);