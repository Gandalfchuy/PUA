-- ========================================================
-- SCRIPT DE INSERCIÓN DE DATOS INICIALES (SEED DATA)
-- SISTEMA PUA - Plataforma Única de Agresores
-- 20 Registros por tabla | created_by = 1
-- ========================================================

BEGIN;

-- --------------------------------------------------------
-- Tabla: actividadrecreativa (20 registros)
-- --------------------------------------------------------
INSERT INTO actividadrecreativa (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Fútbol', true, 1, false),
  (2, 'Básquetbol', true, 1, false),
  (3, 'Béisbol', true, 1, false),
  (4, 'Natación', true, 1, false),
  (5, 'Ciclismo', true, 1, false),
  (6, 'Atletismo / Running', true, 1, false),
  (7, 'Gimnasio / Pesas', true, 1, false),
  (8, 'Lectura', true, 1, false),
  (9, 'Pintura y Dibujo', true, 1, false),
  (10, 'Música / Tocar instrumento', true, 1, false),
  (11, 'Carpintería', true, 1, false),
  (12, 'Jardinería', true, 1, false),
  (13, 'Ajedrez', true, 1, false),
  (14, 'Senderismo', true, 1, false),
  (15, 'Mecánica básica', true, 1, false),
  (16, 'Cocina / Repostería', true, 1, false),
  (17, 'Videojuegos', true, 1, false),
  (18, 'Boxeo / Artes marciales', true, 1, false),
  (19, 'Teatro', true, 1, false),
  (20, 'Fotografía', true, 1, false);

SELECT setval(pg_get_serial_sequence('actividadrecreativa', 'id'), (SELECT MAX(id) FROM actividadrecreativa));

-- --------------------------------------------------------
-- Tabla: adiccion (20 registros)
-- --------------------------------------------------------
INSERT INTO adiccion (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Ninguna', true, 1, false),
  (2, 'Alcoholismo leve', true, 1, false),
  (3, 'Alcoholismo severo', true, 1, false),
  (4, 'Tabaquismo', true, 1, false),
  (5, 'Marihuana / Cannabis', true, 1, false),
  (6, 'Cocaína', true, 1, false),
  (7, 'Metanfetaminas / Cristal', true, 1, false),
  (8, 'Inhalables / Solventes', true, 1, false),
  (9, 'Benzodiacepinas / Sedantes', true, 1, false),
  (10, 'Opioides / Fentanilo', true, 1, false),
  (11, 'Ludopatía (Apuestas)', true, 1, false),
  (12, 'Adicción a fármacos sin receta', true, 1, false),
  (13, 'Anfetaminas', true, 1, false),
  (14, 'Crack', true, 1, false),
  (15, 'Hongos alucinógenos', true, 1, false),
  (16, 'LSD', true, 1, false),
  (17, 'Nicotina / Vapeo', true, 1, false),
  (18, 'Peyote', true, 1, false),
  (19, 'Éxtasis / MDMA', true, 1, false),
  (20, 'Policonsumo de sustancias', true, 1, false);

SELECT setval(pg_get_serial_sequence('adiccion', 'id'), (SELECT MAX(id) FROM adiccion));

-- --------------------------------------------------------
-- Tabla: estadocivil (20 registros)
-- --------------------------------------------------------
INSERT INTO estadocivil (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Soltero', true, 1, false),
  (2, 'Casado (Bienes Mancomunados)', true, 1, false),
  (3, 'Casado (Bienes Separados)', true, 1, false),
  (4, 'Unión Libre / Concubinato', true, 1, false),
  (5, 'Divorciado', true, 1, false),
  (6, 'Separado de hecho', true, 1, false),
  (7, 'Viudo', true, 1, false),
  (8, 'Comprometido', true, 1, false),
  (9, 'Sociedad de Convivencia', true, 1, false),
  (10, 'Segundas nupcias', true, 1, false),
  (11, 'Separación judicial', true, 1, false),
  (12, 'Concubinato registrado', true, 1, false),
  (13, 'Relación abierta', true, 1, false),
  (14, 'Pacto civil', true, 1, false),
  (15, 'En trámite de divorcio', true, 1, false),
  (16, 'Soltero con dependientes', true, 1, false),
  (17, 'Casado sin cohabitación', true, 1, false),
  (18, 'Separado con custodia', true, 1, false),
  (19, 'No especificado', true, 1, false),
  (20, 'Otro estado civil', true, 1, false);

SELECT setval(pg_get_serial_sequence('estadocivil', 'id'), (SELECT MAX(id) FROM estadocivil));

-- --------------------------------------------------------
-- Tabla: generomusical (20 registros)
-- --------------------------------------------------------
INSERT INTO generomusical (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Banda / Regional Mexicano', true, 1, false),
  (2, 'Ranchera / Mariachi', true, 1, false),
  (3, 'Norteño / Sierreño', true, 1, false),
  (4, 'Cumbia', true, 1, false),
  (5, 'Salsa', true, 1, false),
  (6, 'Reggaeton / Urbano', true, 1, false),
  (7, 'Rock en Español', true, 1, false),
  (8, 'Rock Clásico / Metal', true, 1, false),
  (9, 'Pop Latino', true, 1, false),
  (10, 'Pop Internacional', true, 1, false),
  (11, 'Hip-Hop / Rap', true, 1, false),
  (12, 'Corridos / Corridos Tumbados', true, 1, false),
  (13, 'Baladas Románticas', true, 1, false),
  (14, 'Electrónica / EDM', true, 1, false),
  (15, 'Jazz / Blues', true, 1, false),
  (16, 'Música Clásica', true, 1, false),
  (17, 'Trova / Folk', true, 1, false),
  (18, 'Ska / Reggae', true, 1, false),
  (19, 'Huapango / Son Jarocho', true, 1, false),
  (20, 'Trap Latino', true, 1, false);

SELECT setval(pg_get_serial_sequence('generomusical', 'id'), (SELECT MAX(id) FROM generomusical));

-- --------------------------------------------------------
-- Tabla: modalidadviolencia (20 registros)
-- --------------------------------------------------------
INSERT INTO modalidadviolencia (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Violencia Familiar', true, 1, false),
  (2, 'Violencia en el Noviazgo', true, 1, false),
  (3, 'Violencia Digital / Cibernética', true, 1, false),
  (4, 'Violencia Comunitaria', true, 1, false),
  (5, 'Violencia Laboral', true, 1, false),
  (6, 'Violencia Docente / Escolar', true, 1, false),
  (7, 'Violencia Institucional', true, 1, false),
  (8, 'Violencia en el Ámbito Público', true, 1, false),
  (9, 'Violencia Económica Conyugal', true, 1, false),
  (10, 'Violencia Patrimonial Hereditaria', true, 1, false),
  (11, 'Violencia en Custodia Compartida', true, 1, false),
  (12, 'Violencia Psicológica Continua', true, 1, false),
  (13, 'Violencia Física Domiciliaria', true, 1, false),
  (14, 'Violencia Telefónica / Acoso', true, 1, false),
  (15, 'Violencia Sexual Coercitiva', true, 1, false),
  (16, 'Violencia Obstétrica / Pareja', true, 1, false),
  (17, 'Violencia Simbólica / Descalificación', true, 1, false),
  (18, 'Violencia Vicaria', true, 1, false),
  (19, 'Violencia Mediática', true, 1, false),
  (20, 'Violencia Estructural', true, 1, false);

SELECT setval(pg_get_serial_sequence('modalidadviolencia', 'id'), (SELECT MAX(id) FROM modalidadviolencia));

-- --------------------------------------------------------
-- Tabla: motivoingreso (20 registros)
-- --------------------------------------------------------
INSERT INTO motivoingreso (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Orden Judicial por Medida Cautelar', true, 1, false),
  (2, 'Sentencia Condenatoria con Beneficio', true, 1, false),
  (3, 'Derivación del Ministerio Público', true, 1, false),
  (4, 'Canalización de Fiscalía Especializada', true, 1, false),
  (5, 'Suspensión Condicional del Proceso', true, 1, false),
  (6, 'Acuerdo Reparatorio', true, 1, false),
  (7, 'Solicitud Voluntaria de Reeducación', true, 1, false),
  (8, 'Remisión por Juzgado Cívico', true, 1, false),
  (9, 'Canalización de DIF Municipal', true, 1, false),
  (10, 'Canalización del Instituto de la Mujer', true, 1, false),
  (11, 'Requisito de Libertad Condicionada', true, 1, false),
  (12, 'Mandato de Juzgado de lo Familiar', true, 1, false),
  (13, 'Medida de Protección de Emergencia', true, 1, false),
  (14, 'Convenio en Centro de Mediación', true, 1, false),
  (15, 'Derivación por Denuncia Vecinal', true, 1, false),
  (16, 'Intervención de Trabajo Social', true, 1, false),
  (17, 'Reincidencia en Falta Administrativa', true, 1, false),
  (18, 'Acuerdo en Audiencia Inicial', true, 1, false),
  (19, 'Seguimiento Post-Penitenciario', true, 1, false),
  (20, 'Canalización de Centro de Salud', true, 1, false);

SELECT setval(pg_get_serial_sequence('motivoingreso', 'id'), (SELECT MAX(id) FROM motivoingreso));

-- --------------------------------------------------------
-- Tabla: rangosalarial (20 registros)
-- --------------------------------------------------------
INSERT INTO rangosalarial (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Menos de $3,000 mensuales', true, 1, false),
  (2, '$3,000 a $5,000 mensuales', true, 1, false),
  (3, '$5,001 a $7,500 mensuales', true, 1, false),
  (4, '$7,501 a $10,000 mensuales', true, 1, false),
  (5, '$10,001 a $12,500 mensuales', true, 1, false),
  (6, '$12,501 a $15,000 mensuales', true, 1, false),
  (7, '$15,001 a $18,000 mensuales', true, 1, false),
  (8, '$18,001 a $22,000 mensuales', true, 1, false),
  (9, '$22,001 a $26,000 mensuales', true, 1, false),
  (10, '$26,001 a $30,000 mensuales', true, 1, false),
  (11, '$30,001 a $35,000 mensuales', true, 1, false),
  (12, '$35,001 a $40,000 mensuales', true, 1, false),
  (13, '$40,001 a $50,000 mensuales', true, 1, false),
  (14, '$50,001 a $60,000 mensuales', true, 1, false),
  (15, '$60,001 a $75,000 mensuales', true, 1, false),
  (16, '$75,001 a $100,000 mensuales', true, 1, false),
  (17, 'Más de $100,000 mensuales', true, 1, false),
  (18, 'Ingresos variables por comisión', true, 1, false),
  (19, 'Ingresos por jornal / Destajo', true, 1, false),
  (20, 'Sin ingresos fijos / Desempleado', true, 1, false);

SELECT setval(pg_get_serial_sequence('rangosalarial', 'id'), (SELECT MAX(id) FROM rangosalarial));

-- --------------------------------------------------------
-- Tabla: relacionhijos (20 registros)
-- --------------------------------------------------------
INSERT INTO relacionhijos (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Excelente / Comunicación diaria', true, 1, false),
  (2, 'Buena con convivencia regular', true, 1, false),
  (3, 'Regular / Esporádica', true, 1, false),
  (4, 'Distante / Poca comunicación', true, 1, false),
  (5, 'Conflictiva / Discusiones frecuentes', true, 1, false),
  (6, 'Nula / Sin contacto alguno', true, 1, false),
  (7, 'Restringida por orden judicial', true, 1, false),
  (8, 'Supervisada en Centro de Convivencia', true, 1, false),
  (9, 'Sólo contacto telefónico / digital', true, 1, false),
  (10, 'Convivencia fines de semana', true, 1, false),
  (11, 'Pensión alimenticia sin visitas', true, 1, false),
  (12, 'Pérdida de patria potestad', true, 1, false),
  (13, 'Relación cordial por acuerdo', true, 1, false),
  (14, 'En litigio de custodia', true, 1, false),
  (15, 'Rechazo por parte de los hijos', true, 1, false),
  (16, 'Hijos mayores independientes', true, 1, false),
  (17, 'Convivencia vacacional únicamente', true, 1, false),
  (18, 'Afectuosa pero desordenada', true, 1, false),
  (19, 'Bajo custodia exclusiva materna', true, 1, false),
  (20, 'No tiene hijos', true, 1, false);

SELECT setval(pg_get_serial_sequence('relacionhijos', 'id'), (SELECT MAX(id) FROM relacionhijos));

-- --------------------------------------------------------
-- Tabla: religion (20 registros)
-- --------------------------------------------------------
INSERT INTO religion (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Católica', true, 1, false),
  (2, 'Cristiana Evangélica', true, 1, false),
  (3, 'Testigos de Jehová', true, 1, false),
  (4, 'Mormona (SUD)', true, 1, false),
  (5, 'Bautista', true, 1, false),
  (6, 'Pentecostal', true, 1, false),
  (7, 'Adventista del Séptimo Día', true, 1, false),
  (8, 'Presbiteriana', true, 1, false),
  (9, 'Metodista', true, 1, false),
  (10, 'Judía', true, 1, false),
  (11, 'Musulmana', true, 1, false),
  (12, 'Budista', true, 1, false),
  (13, 'Espiritismo / Santería', true, 1, false),
  (14, 'Ateo / Sin religión', true, 1, false),
  (15, 'Agnóstico', true, 1, false),
  (16, 'Creencias indígenas tradicionales', true, 1, false),
  (17, 'Deísta', true, 1, false),
  (18, 'Cristiana no denominacional', true, 1, false),
  (19, 'Ortodoxa', true, 1, false),
  (20, 'Otra religión / Creencia', true, 1, false);

SELECT setval(pg_get_serial_sequence('religion', 'id'), (SELECT MAX(id) FROM religion));

-- --------------------------------------------------------
-- Tabla: sectorsocial (20 registros)
-- --------------------------------------------------------
INSERT INTO sectorsocial (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Sector Obrero / Manufactura', true, 1, false),
  (2, 'Sector Agrícola / Campesino', true, 1, false),
  (3, 'Comercio Informal / Tianguis', true, 1, false),
  (4, 'Comercio Formal / Minorista', true, 1, false),
  (5, 'Servicios de Transporte (Taxis/Apps)', true, 1, false),
  (6, 'Construcción y Oficios (Albañilería/Plomería)', true, 1, false),
  (7, 'Empleados de Gobierno / Burocracia', true, 1, false),
  (8, 'Profesionistas Independientes', true, 1, false),
  (9, 'Docencia y Educación', true, 1, false),
  (10, 'Sector Salud', true, 1, false),
  (11, 'Seguridad Pública / Privada', true, 1, false),
  (12, 'Sector Hotelero y Restaurantero', true, 1, false),
  (13, 'Técnicos y Mantenimiento', true, 1, false),
  (14, 'Sector Financiero / Administrativo', true, 1, false),
  (15, 'Estudiantes Universitarios', true, 1, false),
  (16, 'Comunidad Indígena Originaria', true, 1, false),
  (17, 'Microempresarios / Emprendedores', true, 1, false),
  (18, 'Población Rural Comunitaria', true, 1, false),
  (19, 'Población Urbana Marginal', true, 1, false),
  (20, 'Jubilados / Pensionados', true, 1, false);

SELECT setval(pg_get_serial_sequence('sectorsocial', 'id'), (SELECT MAX(id) FROM sectorsocial));

-- --------------------------------------------------------
-- Tabla: situacionacademica (20 registros)
-- --------------------------------------------------------
INSERT INTO situacionacademica (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Sin escolaridad / Analfabeta', true, 1, false),
  (2, 'Primaria Incompleta', true, 1, false),
  (3, 'Primaria Concluida', true, 1, false),
  (4, 'Secundaria Incompleta', true, 1, false),
  (5, 'Secundaria Concluida', true, 1, false),
  (6, 'Bachillerato / Preparatoria Incompleta', true, 1, false),
  (7, 'Bachillerato / Preparatoria Concluida', true, 1, false),
  (8, 'Carrera Técnica / Vocacional Incompleta', true, 1, false),
  (9, 'Carrera Técnica Concluida', true, 1, false),
  (10, 'Licenciatura / Ingeniería Incompleta', true, 1, false),
  (11, 'Licenciatura Concluida (Pasante)', true, 1, false),
  (12, 'Licenciatura Titulado', true, 1, false),
  (13, 'Especialidad Médica / Técnica', true, 1, false),
  (14, 'Maestría Incompleta', true, 1, false),
  (15, 'Maestría Concluida', true, 1, false),
  (16, 'Doctorado Incompleto', true, 1, false),
  (17, 'Doctorado Concluido', true, 1, false),
  (18, 'Educación para Adultos (INEA)', true, 1, false),
  (19, 'Diplomados / Certificaciones de Oficio', true, 1, false),
  (20, 'Estudios Comerciales', true, 1, false);

SELECT setval(pg_get_serial_sequence('situacionacademica', 'id'), (SELECT MAX(id) FROM situacionacademica));

-- --------------------------------------------------------
-- Tabla: situacionlaboral (20 registros)
-- --------------------------------------------------------
INSERT INTO situacionlaboral (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Empleado de tiempo completo', true, 1, false),
  (2, 'Empleado de medio tiempo', true, 1, false),
  (3, 'Trabajador por cuenta propia / Freelance', true, 1, false),
  (4, 'Comerciante informal', true, 1, false),
  (5, 'Jornalero agrícola', true, 1, false),
  (6, 'Obrero de fábrica', true, 1, false),
  (7, 'Prestador de servicios profesionales', true, 1, false),
  (8, 'Chofer / Operador de transporte', true, 1, false),
  (9, 'Empleado en empresa privada', true, 1, false),
  (10, 'Servidor público / Gobierno', true, 1, false),
  (11, 'Dueño de negocio / Patrón', true, 1, false),
  (12, 'Desempleado (menos de 3 meses)', true, 1, false),
  (13, 'Desempleado (más de 6 meses)', true, 1, false),
  (14, 'Trabajo temporal / Eventual', true, 1, false),
  (15, 'Subempleado', true, 1, false),
  (16, 'Oficios varios / Chamba diaria', true, 1, false),
  (17, 'Incapacitado temporalmente', true, 1, false),
  (18, 'Pensionado / Jubilado', true, 1, false),
  (19, 'Trabajador doméstico / Mantenimiento', true, 1, false),
  (20, 'Estudiante con empleo parcial', true, 1, false);

SELECT setval(pg_get_serial_sequence('situacionlaboral', 'id'), (SELECT MAX(id) FROM situacionlaboral));

-- --------------------------------------------------------
-- Tabla: situacionvivienda (20 registros)
-- --------------------------------------------------------
INSERT INTO situacionvivienda (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Casa propia totalmente pagada', true, 1, false),
  (2, 'Casa propia con crédito hipotecario (Infonavit)', true, 1, false),
  (3, 'Vivienda en arrendamiento / Renta', true, 1, false),
  (4, 'Vivienda prestada por familiares', true, 1, false),
  (5, 'Cuarto en vecindad / Renta compartida', true, 1, false),
  (6, 'Casa de los padres / Co-residencia', true, 1, false),
  (7, 'Casa de los suegros', true, 1, false),
  (8, 'Vivienda en asentamiento irregular', true, 1, false),
  (9, 'Departamento propio', true, 1, false),
  (10, 'Departamento en renta', true, 1, false),
  (11, 'Vivienda ejidal / Comunal', true, 1, false),
  (12, 'Cuarto de azotea', true, 1, false),
  (13, 'Vivienda de interés social', true, 1, false),
  (14, 'Vivienda en zona rural', true, 1, false),
  (15, 'Casa de campo / Finca', true, 1, false),
  (16, 'Alojamiento temporal en albergue', true, 1, false),
  (17, 'Vivienda en litigio / Intestado', true, 1, false),
  (18, 'Inmueble hipotecado en mora', true, 1, false),
  (19, 'Residencia en condominio privado', true, 1, false),
  (20, 'Vivienda precaria / Materiales provisionales', true, 1, false);

SELECT setval(pg_get_serial_sequence('situacionvivienda', 'id'), (SELECT MAX(id) FROM situacionvivienda));

-- --------------------------------------------------------
-- Tabla: tiporelacion (20 registros)
-- --------------------------------------------------------
INSERT INTO tiporelacion (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Excelente / Apoyo incondicional', true, 1, false),
  (2, 'Buena y armónica', true, 1, false),
  (3, 'Respetuosa pero distante', true, 1, false),
  (4, 'Estrictamente formal', true, 1, false),
  (5, 'Indiferente / Poca empatía', true, 1, false),
  (6, 'Conflictiva con agresiones verbales', true, 1, false),
  (7, 'Hostil y violenta', true, 1, false),
  (8, 'Ruptura total de comunicación', true, 1, false),
  (9, 'Relación de codependencia', true, 1, false),
  (10, 'Sumisión y control', true, 1, false),
  (11, 'Sobreprotectora', true, 1, false),
  (12, 'Relación ambivalente (amor/odio)', true, 1, false),
  (13, 'Distanciamiento por migración', true, 1, false),
  (14, 'Rivalidad constante', true, 1, false),
  (15, 'Abandono emocional', true, 1, false),
  (16, 'Intermitente con reconciliaciones', true, 1, false),
  (17, 'Basada únicamente en intereses económicos', true, 1, false),
  (18, 'Tensión latente por celos', true, 1, false),
  (19, 'Relación asimétrica de poder', true, 1, false),
  (20, 'No aplica / Fallecido', true, 1, false);

SELECT setval(pg_get_serial_sequence('tiporelacion', 'id'), (SELECT MAX(id) FROM tiporelacion));

-- --------------------------------------------------------
-- Tabla: tipoviolencia (20 registros)
-- --------------------------------------------------------
INSERT INTO tipoviolencia (id, nombre, activo, created_by, is_deleted) VALUES
  (1, 'Violencia Psicológica / Emocional', true, 1, false),
  (2, 'Violencia Física Leve (Empujones/Jaloneos)', true, 1, false),
  (3, 'Violencia Física Moderada (Golpes/Contusiones)', true, 1, false),
  (4, 'Violencia Física Grave (Lesiones con secuelas)', true, 1, false),
  (5, 'Violencia Verbal e Insultos', true, 1, false),
  (6, 'Violencia Económica (Retención de dinero)', true, 1, false),
  (7, 'Violencia Patrimonial (Destrucción de bienes)', true, 1, false),
  (8, 'Violencia Sexual / Coerción', true, 1, false),
  (9, 'Violencia Digital / Ciberacoso', true, 1, false),
  (10, 'Violencia Simbólica y Humillación', true, 1, false),
  (11, 'Violencia Vicaria (Daño a través de hijos)', true, 1, false),
  (12, 'Amenazas de Muerte / Intimidación', true, 1, false),
  (13, 'Aislamiento Social Forzado', true, 1, false),
  (14, 'Celos Patológicos / Control de conducta', true, 1, false),
  (15, 'Violencia durante el Embarazo', true, 1, false),
  (16, 'Violencia Ambiental (Golpear paredes/puertas)', true, 1, false),
  (17, 'Negligencia y Omisión de Cuidados', true, 1, false),
  (18, 'Privación Ilegal de la Libertad', true, 1, false),
  (19, 'Hostigamiento Continuo', true, 1, false),
  (20, 'Violencia Cruzada / Escala de conflicto', true, 1, false);

SELECT setval(pg_get_serial_sequence('tipoviolencia', 'id'), (SELECT MAX(id) FROM tipoviolencia));

-- --------------------------------------------------------
-- Tabla: agresor (20 registros)
-- --------------------------------------------------------
INSERT INTO agresor (folio, curp, nombre, apellido_paterno, apellido_materno, edad, lugar_nacimiento, lugar_residencia, lugar_trabajo, parejas_previas, hijos, hermanos, estado_civil_id, situacion_academica_id, situacion_laboral_id, situacion_vivienda_id, rango_salarial_id, religion_id, relacion_hijos_id, created_by, is_deleted) VALUES
  (1, 'ABCD800101HDFRND01', 'Carlos', 'Hernández', 'García', 46, ST_SetSRID(ST_MakePoint(-99.1332, 19.4326), 4326), ST_SetSRID(ST_MakePoint(-99.2312, 18.9211), 4326), ST_SetSRID(ST_MakePoint(-99.22, 18.915), 4326), 2, 2, 3, 1, 5, 1, 3, 4, 1, 2, 1, false),
  (2, 'EFGH820202HDFRND02', 'Jorge', 'Martínez', 'López', 44, ST_SetSRID(ST_MakePoint(-99.2341, 18.9221), 4326), ST_SetSRID(ST_MakePoint(-99.238, 18.925), 4326), ST_SetSRID(ST_MakePoint(-99.215, 18.93), 4326), 1, 3, 2, 2, 7, 6, 1, 6, 1, 1, 1, false),
  (3, 'IJKL850303HDFRND03', 'Roberto', 'González', 'Pérez', 41, ST_SetSRID(ST_MakePoint(-99.182, 19.352), 4326), ST_SetSRID(ST_MakePoint(-99.25, 18.91), 4326), ST_SetSRID(ST_MakePoint(-99.245, 18.905), 4326), 3, 1, 4, 4, 3, 4, 4, 2, 2, 3, 1, false),
  (4, 'MNOP880404HDFRND04', 'Miguel Ángel', 'Rodríguez', 'Sánchez', 38, ST_SetSRID(ST_MakePoint(-99.141, 19.41), 4326), ST_SetSRID(ST_MakePoint(-99.225, 18.935), 4326), ST_SetSRID(ST_MakePoint(-99.21, 18.94), 4326), 0, 0, 1, 1, 10, 7, 9, 8, 1, 20, 1, false),
  (5, 'QRST900505HDFRND05', 'Fernando', 'Ramírez', 'Flores', 36, ST_SetSRID(ST_MakePoint(-99.21, 18.95), 4326), ST_SetSRID(ST_MakePoint(-99.215, 18.948), 4326), ST_SetSRID(ST_MakePoint(-99.23, 18.92), 4326), 2, 2, 2, 5, 5, 8, 2, 5, 1, 4, 1, false),
  (6, 'UVWX920606HDFRND06', 'Alejandro', 'Cruz', 'Morales', 34, ST_SetSRID(ST_MakePoint(-99.15, 19.4), 4326), ST_SetSRID(ST_MakePoint(-99.24, 18.915), 4326), ST_SetSRID(ST_MakePoint(-99.235, 18.91), 4326), 1, 1, 3, 2, 4, 1, 3, 4, 3, 2, 1, false),
  (7, 'YZAB940707HDFRND07', 'Luis Enrique', 'Gómez', 'Vázquez', 32, ST_SetSRID(ST_MakePoint(-99.22, 18.93), 4326), ST_SetSRID(ST_MakePoint(-99.222, 18.932), 4326), ST_SetSRID(ST_MakePoint(-99.218, 18.928), 4326), 2, 2, 1, 4, 7, 9, 10, 7, 1, 1, 1, false),
  (8, 'CDEF950808HDFRND08', 'Ricardo', 'Díaz', 'Reyes', 31, ST_SetSRID(ST_MakePoint(-99.17, 19.38), 4326), ST_SetSRID(ST_MakePoint(-99.26, 18.905), 4326), ST_SetSRID(ST_MakePoint(-99.255, 18.9), 4326), 1, 0, 2, 1, 12, 10, 1, 11, 14, 20, 1, false),
  (9, 'GHIJ960909HDFRND09', 'Héctor', 'Reyes', 'Jiménez', 30, ST_SetSRID(ST_MakePoint(-99.245, 18.918), 4326), ST_SetSRID(ST_MakePoint(-99.248, 18.92), 4326), ST_SetSRID(ST_MakePoint(-99.24, 18.915), 4326), 3, 3, 4, 2, 5, 6, 3, 5, 1, 5, 1, false),
  (10, 'KLMN971010HDFRND10', 'Víctor Manuel', 'Morales', 'Torres', 29, ST_SetSRID(ST_MakePoint(-99.13, 19.42), 4326), ST_SetSRID(ST_MakePoint(-99.23, 18.94), 4326), ST_SetSRID(ST_MakePoint(-99.22, 18.935), 4326), 1, 1, 2, 4, 6, 1, 4, 6, 2, 2, 1, false),
  (11, 'OPQR981111HDFRND11', 'Juan Carlos', 'Ortiz', 'Gutiérrez', 28, ST_SetSRID(ST_MakePoint(-99.205, 18.96), 4326), ST_SetSRID(ST_MakePoint(-99.21, 18.955), 4326), ST_SetSRID(ST_MakePoint(-99.225, 18.94), 4326), 0, 1, 3, 1, 9, 3, 5, 3, 1, 3, 1, false),
  (12, 'STUV991212HDFRND12', 'Daniel', 'Gutiérrez', 'Castro', 27, ST_SetSRID(ST_MakePoint(-99.16, 19.39), 4326), ST_SetSRID(ST_MakePoint(-99.235, 18.928), 4326), ST_SetSRID(ST_MakePoint(-99.24, 18.93), 4326), 2, 2, 1, 2, 7, 7, 2, 7, 1, 1, 1, false),
  (13, 'WXYZ000113HDFRND13', 'Gabriel', 'Castro', 'Romero', 26, ST_SetSRID(ST_MakePoint(-99.235, 18.912), 4326), ST_SetSRID(ST_MakePoint(-99.238, 18.915), 4326), ST_SetSRID(ST_MakePoint(-99.23, 18.91), 4326), 1, 0, 2, 1, 5, 8, 6, 4, 4, 20, 1, false),
  (14, 'BCDE010214HDFRND14', 'Raúl', 'Vargas', 'Ruiz', 25, ST_SetSRID(ST_MakePoint(-99.145, 19.415), 4326), ST_SetSRID(ST_MakePoint(-99.255, 18.908), 4326), ST_SetSRID(ST_MakePoint(-99.25, 18.905), 4326), 1, 1, 4, 4, 3, 1, 3, 3, 1, 4, 1, false),
  (15, 'FGHI020315HDFRND15', 'Arturo', 'Mendoza', 'Medina', 24, ST_SetSRID(ST_MakePoint(-99.215, 18.945), 4326), ST_SetSRID(ST_MakePoint(-99.218, 18.942), 4326), ST_SetSRID(ST_MakePoint(-99.225, 18.938), 4326), 0, 0, 1, 1, 7, 15, 6, 2, 14, 20, 1, false),
  (16, 'JKLM030416HDFRND16', 'Gerardo', 'Aguilar', 'Navarro', 23, ST_SetSRID(ST_MakePoint(-99.175, 19.375), 4326), ST_SetSRID(ST_MakePoint(-99.242, 18.922), 4326), ST_SetSRID(ST_MakePoint(-99.238, 18.92), 4326), 1, 1, 2, 2, 5, 2, 4, 5, 1, 2, 1, false),
  (17, 'NOPQ810517HDFRND17', 'Eduardo', 'Ramos', 'Delgado', 45, ST_SetSRID(ST_MakePoint(-99.225, 18.932), 4326), ST_SetSRID(ST_MakePoint(-99.228, 18.93), 4326), ST_SetSRID(ST_MakePoint(-99.22, 18.925), 4326), 4, 4, 5, 5, 2, 5, 8, 1, 1, 5, 1, false),
  (18, 'RSTU830618HDFRND18', 'Salvador', 'Vega', 'Castillo', 43, ST_SetSRID(ST_MakePoint(-99.135, 19.428), 4326), ST_SetSRID(ST_MakePoint(-99.25, 18.915), 4326), ST_SetSRID(ST_MakePoint(-99.245, 18.912), 4326), 2, 3, 3, 2, 7, 11, 1, 12, 1, 1, 1, false),
  (19, 'VWXY860719HDFRND19', 'Octavio', 'Silva', 'Estrada', 40, ST_SetSRID(ST_MakePoint(-99.25, 18.908), 4326), ST_SetSRID(ST_MakePoint(-99.252, 18.91), 4326), ST_SetSRID(ST_MakePoint(-99.248, 18.905), 4326), 1, 2, 2, 4, 10, 9, 9, 8, 2, 3, 1, false),
  (20, 'ZABC890820HDFRND20', 'Armando', 'Paredes', 'Soto', 37, ST_SetSRID(ST_MakePoint(-99.155, 19.405), 4326), ST_SetSRID(ST_MakePoint(-99.23, 18.935), 4326), ST_SetSRID(ST_MakePoint(-99.225, 18.932), 4326), 3, 1, 1, 2, 5, 6, 3, 6, 1, 2, 1, false);

SELECT setval(pg_get_serial_sequence('agresor', 'folio'), (SELECT MAX(folio) FROM agresor));

-- --------------------------------------------------------
-- Tabla Pivote: agresor_sectorsocial (20 registros)
-- --------------------------------------------------------
INSERT INTO agresor_sectorsocial (agresor_folio, sector_social_id) VALUES
  (1, 2),
  (2, 3),
  (3, 4),
  (4, 5),
  (5, 6),
  (6, 7),
  (7, 8),
  (8, 9),
  (9, 10),
  (10, 11),
  (11, 12),
  (12, 13),
  (13, 14),
  (14, 15),
  (15, 16),
  (16, 17),
  (17, 18),
  (18, 19),
  (19, 20),
  (20, 1);

-- --------------------------------------------------------
-- Tabla Pivote: agresor_actividadrecreativa (20 registros)
-- --------------------------------------------------------
INSERT INTO agresor_actividadrecreativa (agresor_folio, actividad_id) VALUES
  (1, 4),
  (2, 5),
  (3, 6),
  (4, 7),
  (5, 8),
  (6, 9),
  (7, 10),
  (8, 11),
  (9, 12),
  (10, 13),
  (11, 14),
  (12, 15),
  (13, 16),
  (14, 17),
  (15, 18),
  (16, 19),
  (17, 20),
  (18, 1),
  (19, 2),
  (20, 3);

-- --------------------------------------------------------
-- Tabla Pivote: agresor_adiccion (20 registros)
-- --------------------------------------------------------
INSERT INTO agresor_adiccion (agresor_folio, adiccion_id) VALUES
  (1, 3),
  (2, 4),
  (3, 5),
  (4, 6),
  (5, 7),
  (6, 8),
  (7, 9),
  (8, 10),
  (9, 11),
  (10, 12),
  (11, 13),
  (12, 14),
  (13, 15),
  (14, 16),
  (15, 17),
  (16, 18),
  (17, 19),
  (18, 20),
  (19, 1),
  (20, 2);

-- --------------------------------------------------------
-- Tabla Pivote: agresor_generomusical (20 registros)
-- --------------------------------------------------------
INSERT INTO agresor_generomusical (agresor_folio, genero_id) VALUES
  (1, 5),
  (2, 6),
  (3, 7),
  (4, 8),
  (5, 9),
  (6, 10),
  (7, 11),
  (8, 12),
  (9, 13),
  (10, 14),
  (11, 15),
  (12, 16),
  (13, 17),
  (14, 18),
  (15, 19),
  (16, 20),
  (17, 1),
  (18, 2),
  (19, 3),
  (20, 4);

-- --------------------------------------------------------
-- Tabla Pivote: agresor_relacionhermanos (20 registros)
-- --------------------------------------------------------
INSERT INTO agresor_relacionhermanos (agresor_folio, tipo_relacion_id) VALUES
  (1, 6),
  (2, 7),
  (3, 8),
  (4, 9),
  (5, 10),
  (6, 11),
  (7, 12),
  (8, 13),
  (9, 14),
  (10, 15),
  (11, 16),
  (12, 17),
  (13, 18),
  (14, 19),
  (15, 20),
  (16, 1),
  (17, 2),
  (18, 3),
  (19, 4),
  (20, 5);

-- --------------------------------------------------------
-- Tabla Pivote: agresor_relacionmadre (20 registros)
-- --------------------------------------------------------
INSERT INTO agresor_relacionmadre (agresor_folio, tipo_relacion_id) VALUES
  (1, 7),
  (2, 8),
  (3, 9),
  (4, 10),
  (5, 11),
  (6, 12),
  (7, 13),
  (8, 14),
  (9, 15),
  (10, 16),
  (11, 17),
  (12, 18),
  (13, 19),
  (14, 20),
  (15, 1),
  (16, 2),
  (17, 3),
  (18, 4),
  (19, 5),
  (20, 6);

-- --------------------------------------------------------
-- Tabla Pivote: agresor_relacionpadre (20 registros)
-- --------------------------------------------------------
INSERT INTO agresor_relacionpadre (agresor_folio, tipo_relacion_id) VALUES
  (1, 8),
  (2, 9),
  (3, 10),
  (4, 11),
  (5, 12),
  (6, 13),
  (7, 14),
  (8, 15),
  (9, 16),
  (10, 17),
  (11, 18),
  (12, 19),
  (13, 20),
  (14, 1),
  (15, 2),
  (16, 3),
  (17, 4),
  (18, 5),
  (19, 6),
  (20, 7);

-- --------------------------------------------------------
-- Tabla Pivote: agresor_tipoviolenciainfantil (20 registros)
-- --------------------------------------------------------
INSERT INTO agresor_tipoviolenciainfantil (agresor_folio, tipo_violencia_id) VALUES
  (1, 9),
  (2, 10),
  (3, 11),
  (4, 12),
  (5, 13),
  (6, 14),
  (7, 15),
  (8, 16),
  (9, 17),
  (10, 18),
  (11, 19),
  (12, 20),
  (13, 1),
  (14, 2),
  (15, 3),
  (16, 4),
  (17, 5),
  (18, 6),
  (19, 7),
  (20, 8);

-- --------------------------------------------------------
-- Tabla: sesion (20 registros)
-- --------------------------------------------------------
INSERT INTO sesion (folio, nombre, objetivo, created_by, is_deleted) VALUES
  (1, 'Módulo 1: Reconocimiento de la Violencia', 'Identificar los tipos y modalidades de violencia ejercida en el ámbito familiar y de pareja.', 1, false),
  (2, 'Módulo 2: Construcción de la Masculinidad', 'Analizar los mandatos tradicionales de género y su impacto en las relaciones interpersonales.', 1, false),
  (3, 'Módulo 3: Manejo Emocional y Autocontrol', 'Desarrollar herramientas cognitivas para la identificación y contención de la ira.', 1, false),
  (4, 'Módulo 4: Comunicación Asertiva', 'Fomentar el diálogo no violento y la escucha activa en la resolución de conflictos.', 1, false),
  (5, 'Módulo 5: Responsabilidad y Consecuencias', 'Asumir la responsabilidad de los actos violentos sin justificaciones externas.', 1, false),
  (6, 'Módulo 6: Empatía y Reparación del Daño', 'Comprender el impacto psicológico y físico causado en las víctimas y familiares.', 1, false),
  (7, 'Módulo 7: Paternidad Afectiva y Cuidado', 'Promover roles parentales basados en el respeto, el afecto y la no violencia.', 1, false),
  (8, 'Módulo 8: Celos y Necesidad de Control', 'Desarticular conductas de posesión, control digital y celotipia en la pareja.', 1, false),
  (9, 'Módulo 9: Resolución Pacífica de Conflictos', 'Adquirir técnicas de negociación y mediación pacífica ante desacuerdos cotidianos.', 1, false),
  (10, 'Módulo 10: Prevención de Recaídas en Crisis', 'Elaborar un plan personal de acción y contención ante detonantes emocionales.', 1, false),
  (11, 'Módulo 11: Desmitificación del Amor Romántico', 'Cuestionar falsas creencias sobre el amor que legitiman el abuso y la dependencia.', 1, false),
  (12, 'Módulo 12: Uso del Tiempo Libre y Recreación', 'Incorporar actividades recreativas y deportivas saludables libres de adicciones.', 1, false),
  (13, 'Módulo 13: Manejo del Estrés y Ansiedad', 'Aprender técnicas de relajación física y respiración diafragmática para momentos de tensión.', 1, false),
  (14, 'Módulo 14: Violencia Económica y Patrimonial', 'Analizar el manejo equitativo de los recursos económicos y bienes familiares.', 1, false),
  (15, 'Módulo 15: Convivencia con Familia de Origen', 'Establecer límites saludables en las relaciones con padres y hermanos.', 1, false),
  (16, 'Módulo 16: Redes Sociales y Violencia Digital', 'Reconocer conductas invasivas y de acoso en medios digitales y mensajería.', 1, false),
  (17, 'Módulo 17: Redes de Apoyo Positivas', 'Fomentar círculos sociales constructivos y abandonar entornos de socialización violenta.', 1, false),
  (18, 'Módulo 18: Salud Mental y Autocuidado', 'Fomentar hábitos de salud física, mental y la búsqueda oportuna de ayuda profesional.', 1, false),
  (19, 'Módulo 19: Plan de Vida Libre de Violencia', 'Diseñar metas personales, familiares y laborales a mediano y largo plazo.', 1, false),
  (20, 'Módulo 20: Evaluación y Cierre de Proceso', 'Evaluar el grado de internalización de los principios de no violencia y entrega de balance.', 1, false);

SELECT setval(pg_get_serial_sequence('sesion', 'folio'), (SELECT MAX(folio) FROM sesion));

-- --------------------------------------------------------
-- Tabla: grupo (20 registros)
-- --------------------------------------------------------
INSERT INTO grupo (folio, lugar, ubicacion, created_by, is_deleted) VALUES
  (1, 'Centro Comunitario Cuernavaca Centro', ST_SetSRID(ST_MakePoint(-99.2345, 18.9215), 4326), 1, false),
  (2, 'Sede Norte - Chamilpa', ST_SetSRID(ST_MakePoint(-99.245, 18.968), 4326), 1, false),
  (3, 'Centro de Desarrollo Comunitario Jiutepec', ST_SetSRID(ST_MakePoint(-99.178, 18.881), 4326), 1, false),
  (4, 'Módulo DIF Temixco', ST_SetSRID(ST_MakePoint(-99.229, 18.854), 4326), 1, false),
  (5, 'Casa de Cultura Emiliano Zapata', ST_SetSRID(ST_MakePoint(-99.182, 18.835), 4326), 1, false),
  (6, 'Centro Comunitario Cuautla Centro', ST_SetSRID(ST_MakePoint(-98.955, 18.812), 4326), 1, false),
  (7, 'Sede Reeducativa Yautepec', ST_SetSRID(ST_MakePoint(-99.068, 18.882), 4326), 1, false),
  (8, 'Módulo de Atención Xochitepec', ST_SetSRID(ST_MakePoint(-99.231, 18.781), 4326), 1, false),
  (9, 'Centro Social Jojutla', ST_SetSRID(ST_MakePoint(-99.182, 18.615), 4326), 1, false),
  (10, 'Sede DIF Zacatepec', ST_SetSRID(ST_MakePoint(-99.195, 18.654), 4326), 1, false),
  (11, 'Centro Integrador Tepoztlán', ST_SetSRID(ST_MakePoint(-99.098, 18.985), 4326), 1, false),
  (12, 'Módulo Comunitario Huitzilac', ST_SetSRID(ST_MakePoint(-99.268, 19.031), 4326), 1, false),
  (13, 'Centro Reeducativo Puente de Ixtla', ST_SetSRID(ST_MakePoint(-99.321, 18.618), 4326), 1, false),
  (14, 'Sede Yecapixtla', ST_SetSRID(ST_MakePoint(-98.865, 18.882), 4326), 1, false),
  (15, 'Centro Social Ayala', ST_SetSRID(ST_MakePoint(-98.982, 18.765), 4326), 1, false),
  (16, 'Módulo Tlaltizapán Centro', ST_SetSRID(ST_MakePoint(-99.12, 18.685), 4326), 1, false),
  (17, 'Sede Tetecala', ST_SetSRID(ST_MakePoint(-99.401, 18.729), 4326), 1, false),
  (18, 'Centro Comunitario Miacatlán', ST_SetSRID(ST_MakePoint(-99.362, 18.768), 4326), 1, false),
  (19, 'Módulo DIF Tlayacapan', ST_SetSRID(ST_MakePoint(-98.985, 18.956), 4326), 1, false),
  (20, 'Centro de Atención Ocuituco', ST_SetSRID(ST_MakePoint(-98.775, 18.878), 4326), 1, false);

SELECT setval(pg_get_serial_sequence('grupo', 'folio'), (SELECT MAX(folio) FROM grupo));

-- --------------------------------------------------------
-- Tabla: procesoreeducacion (20 registros)
-- --------------------------------------------------------
INSERT INTO procesoreeducacion (folio, agresor_id, fecha_inicio, fecha_termino, fecha_denuncia, denunciante, folio_carpeta_fiscalia, motivo_ingreso_id, tipo_violencia_id, modalidad_violencia_id, created_by, is_deleted) VALUES
  (1, 1, '2026-01-15', '2026-06-15', '2025-11-20', 'María Elena Torres', 'SC01/12345/2025', 1, 1, 1, 1, false),
  (2, 2, '2026-01-20', '2026-07-20', '2025-12-05', 'Patricia Mendoza', 'SC02/23456/2025', 2, 2, 1, 1, false),
  (3, 3, '2026-02-01', '2026-08-01', '2025-12-18', 'Gabriela Soto', 'SC03/34567/2025', 3, 3, 2, 1, false),
  (4, 4, '2026-02-10', '2026-08-10', '2026-01-08', 'Lucía Ramírez', 'SC01/45678/2026', 4, 1, 1, 1, false),
  (5, 5, '2026-02-15', '2026-08-15', '2026-01-14', 'Ana María Castro', 'SC02/56789/2026', 5, 4, 3, 1, false),
  (6, 6, '2026-03-01', '2026-09-01', '2026-01-22', 'Rosa Isela Gómez', 'SC03/67890/2026', 1, 5, 1, 1, false),
  (7, 7, '2026-03-05', '2026-09-05', '2026-02-01', 'Claudia Morales', 'SC01/78901/2026', 2, 6, 2, 1, false),
  (8, 8, '2026-03-10', '2026-09-10', '2026-02-10', 'Verónica Ortiz', 'SC02/89012/2026', 3, 7, 1, 1, false),
  (9, 9, '2026-03-15', '2026-09-15', '2026-02-15', 'Adriana Ruiz', 'SC03/90123/2026', 4, 1, 4, 1, false),
  (10, 10, '2026-04-01', '2026-10-01', '2026-02-28', 'Silvia Hernández', 'SC01/01234/2026', 5, 2, 1, 1, false),
  (11, 11, '2026-04-05', '2026-10-05', '2026-03-05', 'Teresa Gutiérrez', 'SC02/12340/2026', 1, 3, 2, 1, false),
  (12, 12, '2026-04-10', '2026-10-10', '2026-03-12', 'Mónica Delgado', 'SC03/23451/2026', 2, 4, 1, 1, false),
  (13, 13, '2026-04-15', '2026-10-15', '2026-03-18', 'Lorena Castillo', 'SC01/34562/2026', 3, 1, 3, 1, false),
  (14, 14, '2026-05-01', '2026-11-01', '2026-03-25', 'Karla Estrada', 'SC02/45673/2026', 4, 5, 1, 1, false),
  (15, 15, '2026-05-05', '2026-11-05', '2026-04-02', 'Daniela Vargas', 'SC03/56784/2026', 5, 6, 2, 1, false),
  (16, 16, '2026-05-10', '2026-11-10', '2026-04-10', 'Sofía Medina', 'SC01/67895/2026', 1, 7, 1, 1, false),
  (17, 17, '2026-05-15', '2026-11-15', '2026-04-18', 'Guadalupe Reyes', 'SC02/78906/2026', 2, 8, 4, 1, false),
  (18, 18, '2026-06-01', '2026-12-01', '2026-04-25', 'Beatriz Díaz', 'SC03/89017/2026', 3, 1, 1, 1, false),
  (19, 19, '2026-06-05', '2026-12-05', '2026-05-02', 'Sandra Jiménez', 'SC01/90128/2026', 4, 2, 2, 1, false),
  (20, 20, '2026-06-10', '2026-12-10', '2026-05-10', 'Yolanda Navarro', 'SC02/01239/2026', 5, 3, 1, 1, false);

SELECT setval(pg_get_serial_sequence('procesoreeducacion', 'folio'), (SELECT MAX(folio) FROM procesoreeducacion));

-- --------------------------------------------------------
-- Tabla: lista (20 registros de asistencias)
-- --------------------------------------------------------
INSERT INTO lista (id, agresor_id, grupo_id, sesion_id, fecha, created_by, is_deleted) VALUES
  (1, 1, 1, 1, '2026-01-16', 1, false),
  (2, 2, 1, 1, '2026-01-16', 1, false),
  (3, 3, 2, 1, '2026-01-17', 1, false),
  (4, 4, 2, 1, '2026-01-17', 1, false),
  (5, 5, 3, 2, '2026-01-23', 1, false),
  (6, 6, 3, 2, '2026-01-23', 1, false),
  (7, 7, 4, 2, '2026-01-24', 1, false),
  (8, 8, 4, 3, '2026-01-30', 1, false),
  (9, 9, 5, 3, '2026-01-30', 1, false),
  (10, 10, 5, 4, '2026-02-06', 1, false),
  (11, 11, 6, 4, '2026-02-06', 1, false),
  (12, 12, 6, 5, '2026-02-13', 1, false),
  (13, 13, 7, 5, '2026-02-13', 1, false),
  (14, 14, 7, 6, '2026-02-20', 1, false),
  (15, 15, 8, 6, '2026-02-20', 1, false),
  (16, 16, 8, 7, '2026-02-27', 1, false),
  (17, 17, 9, 7, '2026-02-27', 1, false),
  (18, 18, 9, 8, '2026-03-06', 1, false),
  (19, 19, 10, 8, '2026-03-06', 1, false),
  (20, 20, 10, 9, '2026-03-13', 1, false);

SELECT setval(pg_get_serial_sequence('lista', 'id'), (SELECT MAX(id) FROM lista));

COMMIT;

-- ========================================================
-- FIN DEL SCRIPT
-- ========================================================