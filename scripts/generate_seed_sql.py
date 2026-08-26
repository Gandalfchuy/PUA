#!/usr/bin/env python3
"""
Script generador del archivo SQL con 20 inserciones por tabla.
Excluye 'usuarios' y 'roles'.
Asigna created_by = 1 a todos los registros.
Maneja geometrías PostGIS ST_SetSRID(ST_MakePoint(longitud, latitud), 4326).
"""

import os

def generate_sql():
    sql = []
    sql.append("-- ========================================================")
    sql.append("-- SCRIPT DE INSERCIÓN DE DATOS INICIALES (SEED DATA)")
    sql.append("-- SISTEMA PUA - Plataforma Única de Agresores")
    sql.append("-- 20 Registros por tabla | created_by = 1")
    sql.append("-- ========================================================\n")
    sql.append("BEGIN;\n")

    # 1. CATÁLOGOS (15 TABLAS, 20 REGISTROS C/U)
    catalogos = {
        "actividadrecreativa": [
            "Fútbol", "Básquetbol", "Béisbol", "Natación", "Ciclismo",
            "Atletismo / Running", "Gimnasio / Pesas", "Lectura", "Pintura y Dibujo", "Música / Tocar instrumento",
            "Carpintería", "Jardinería", "Ajedrez", "Senderismo", "Mecánica básica",
            "Cocina / Repostería", "Videojuegos", "Boxeo / Artes marciales", "Teatro", "Fotografía"
        ],
        "adiccion": [
            "Ninguna", "Alcoholismo leve", "Alcoholismo severo", "Tabaquismo", "Marihuana / Cannabis",
            "Cocaína", "Metanfetaminas / Cristal", "Inhalables / Solventes", "Benzodiacepinas / Sedantes", "Opioides / Fentanilo",
            "Ludopatía (Apuestas)", "Adicción a fármacos sin receta", "Anfetaminas", "Crack", "Hongos alucinógenos",
            "LSD", "Nicotina / Vapeo", "Peyote", "Éxtasis / MDMA", "Policonsumo de sustancias"
        ],
        "estadocivil": [
            "Soltero", "Casado (Bienes Mancomunados)", "Casado (Bienes Separados)", "Unión Libre / Concubinato", "Divorciado",
            "Separado de hecho", "Viudo", "Comprometido", "Sociedad de Convivencia", "Segundas nupcias",
            "Separación judicial", "Concubinato registrado", "Relación abierta", "Pacto civil", "En trámite de divorcio",
            "Soltero con dependientes", "Casado sin cohabitación", "Separado con custodia", "No especificado", "Otro estado civil"
        ],
        "generomusical": [
            "Banda / Regional Mexicano", "Ranchera / Mariachi", "Norteño / Sierreño", "Cumbia", "Salsa",
            "Reggaeton / Urbano", "Rock en Español", "Rock Clásico / Metal", "Pop Latino", "Pop Internacional",
            "Hip-Hop / Rap", "Corridos / Corridos Tumbados", "Baladas Románticas", "Electrónica / EDM", "Jazz / Blues",
            "Música Clásica", "Trova / Folk", "Ska / Reggae", "Huapango / Son Jarocho", "Trap Latino"
        ],
        "modalidadviolencia": [
            "Violencia Familiar", "Violencia en el Noviazgo", "Violencia Digital / Cibernética", "Violencia Comunitaria", "Violencia Laboral",
            "Violencia Docente / Escolar", "Violencia Institucional", "Violencia en el Ámbito Público", "Violencia Económica Conyugal", "Violencia Patrimonial Hereditaria",
            "Violencia en Custodia Compartida", "Violencia Psicológica Continua", "Violencia Física Domiciliaria", "Violencia Telefónica / Acoso", "Violencia Sexual Coercitiva",
            "Violencia Obstétrica / Pareja", "Violencia Simbólica / Descalificación", "Violencia Vicaria", "Violencia Mediática", "Violencia Estructural"
        ],
        "motivoingreso": [
            "Orden Judicial por Medida Cautelar", "Sentencia Condenatoria con Beneficio", "Derivación del Ministerio Público", "Canalización de Fiscalía Especializada", "Suspensión Condicional del Proceso",
            "Acuerdo Reparatorio", "Solicitud Voluntaria de Reeducación", "Remisión por Juzgado Cívico", "Canalización de DIF Municipal", "Canalización del Instituto de la Mujer",
            "Requisito de Libertad Condicionada", "Mandato de Juzgado de lo Familiar", "Medida de Protección de Emergencia", "Convenio en Centro de Mediación", "Derivación por Denuncia Vecinal",
            "Intervención de Trabajo Social", "Reincidencia en Falta Administrativa", "Acuerdo en Audiencia Inicial", "Seguimiento Post-Penitenciario", "Canalización de Centro de Salud"
        ],
        "rangosalarial": [
            "Menos de $3,000 mensuales", "$3,000 a $5,000 mensuales", "$5,001 a $7,500 mensuales", "$7,501 a $10,000 mensuales", "$10,001 a $12,500 mensuales",
            "$12,501 a $15,000 mensuales", "$15,001 a $18,000 mensuales", "$18,001 a $22,000 mensuales", "$22,001 a $26,000 mensuales", "$26,001 a $30,000 mensuales",
            "$30,001 a $35,000 mensuales", "$35,001 a $40,000 mensuales", "$40,001 a $50,000 mensuales", "$50,001 a $60,000 mensuales", "$60,001 a $75,000 mensuales",
            "$75,001 a $100,000 mensuales", "Más de $100,000 mensuales", "Ingresos variables por comisión", "Ingresos por jornal / Destajo", "Sin ingresos fijos / Desempleado"
        ],
        "relacionhijos": [
            "Excelente / Comunicación diaria", "Buena con convivencia regular", "Regular / Esporádica", "Distante / Poca comunicación", "Conflictiva / Discusiones frecuentes",
            "Nula / Sin contacto alguno", "Restringida por orden judicial", "Supervisada en Centro de Convivencia", "Sólo contacto telefónico / digital", "Convivencia fines de semana",
            "Pensión alimenticia sin visitas", "Pérdida de patria potestad", "Relación cordial por acuerdo", "En litigio de custodia", "Rechazo por parte de los hijos",
            "Hijos mayores independientes", "Convivencia vacacional únicamente", "Afectuosa pero desordenada", "Bajo custodia exclusiva materna", "No tiene hijos"
        ],
        "religion": [
            "Católica", "Cristiana Evangélica", "Testigos de Jehová", "Mormona (SUD)", "Bautista",
            "Pentecostal", "Adventista del Séptimo Día", "Presbiteriana", "Metodista", "Judía",
            "Musulmana", "Budista", "Espiritismo / Santería", "Ateo / Sin religión", "Agnóstico",
            "Creencias indígenas tradicionales", "Deísta", "Cristiana no denominacional", "Ortodoxa", "Otra religión / Creencia"
        ],
        "sectorsocial": [
            "Sector Obrero / Manufactura", "Sector Agrícola / Campesino", "Comercio Informal / Tianguis", "Comercio Formal / Minorista", "Servicios de Transporte (Taxis/Apps)",
            "Construcción y Oficios (Albañilería/Plomería)", "Empleados de Gobierno / Burocracia", "Profesionistas Independientes", "Docencia y Educación", "Sector Salud",
            "Seguridad Pública / Privada", "Sector Hotelero y Restaurantero", "Técnicos y Mantenimiento", "Sector Financiero / Administrativo", "Estudiantes Universitarios",
            "Comunidad Indígena Originaria", "Microempresarios / Emprendedores", "Población Rural Comunitaria", "Población Urbana Marginal", "Jubilados / Pensionados"
        ],
        "situacionacademica": [
            "Sin escolaridad / Analfabeta", "Primaria Incompleta", "Primaria Concluida", "Secundaria Incompleta", "Secundaria Concluida",
            "Bachillerato / Preparatoria Incompleta", "Bachillerato / Preparatoria Concluida", "Carrera Técnica / Vocacional Incompleta", "Carrera Técnica Concluida", "Licenciatura / Ingeniería Incompleta",
            "Licenciatura Concluida (Pasante)", "Licenciatura Titulado", "Especialidad Médica / Técnica", "Maestría Incompleta", "Maestría Concluida",
            "Doctorado Incompleto", "Doctorado Concluido", "Educación para Adultos (INEA)", "Diplomados / Certificaciones de Oficio", "Estudios Comerciales"
        ],
        "situacionlaboral": [
            "Empleado de tiempo completo", "Empleado de medio tiempo", "Trabajador por cuenta propia / Freelance", "Comerciante informal", "Jornalero agrícola",
            "Obrero de fábrica", "Prestador de servicios profesionales", "Chofer / Operador de transporte", "Empleado en empresa privada", "Servidor público / Gobierno",
            "Dueño de negocio / Patrón", "Desempleado (menos de 3 meses)", "Desempleado (más de 6 meses)", "Trabajo temporal / Eventual", "Subempleado",
            "Oficios varios / Chamba diaria", "Incapacitado temporalmente", "Pensionado / Jubilado", "Trabajador doméstico / Mantenimiento", "Estudiante con empleo parcial"
        ],
        "situacionvivienda": [
            "Casa propia totalmente pagada", "Casa propia con crédito hipotecario (Infonavit)", "Vivienda en arrendamiento / Renta", "Vivienda prestada por familiares", "Cuarto en vecindad / Renta compartida",
            "Casa de los padres / Co-residencia", "Casa de los suegros", "Vivienda en asentamiento irregular", "Departamento propio", "Departamento en renta",
            "Vivienda ejidal / Comunal", "Cuarto de azotea", "Vivienda de interés social", "Vivienda en zona rural", "Casa de campo / Finca",
            "Alojamiento temporal en albergue", "Vivienda en litigio / Intestado", "Inmueble hipotecado en mora", "Residencia en condominio privado", "Vivienda precaria / Materiales provisionales"
        ],
        "tiporelacion": [
            "Excelente / Apoyo incondicional", "Buena y armónica", "Respetuosa pero distante", "Estrictamente formal", "Indiferente / Poca empatía",
            "Conflictiva con agresiones verbales", "Hostil y violenta", "Ruptura total de comunicación", "Relación de codependencia", "Sumisión y control",
            "Sobreprotectora", "Relación ambivalente (amor/odio)", "Distanciamiento por migración", "Rivalidad constante", "Abandono emocional",
            "Intermitente con reconciliaciones", "Basada únicamente en intereses económicos", "Tensión latente por celos", "Relación asimétrica de poder", "No aplica / Fallecido"
        ],
        "tipoviolencia": [
            "Violencia Psicológica / Emocional", "Violencia Física Leve (Empujones/Jaloneos)", "Violencia Física Moderada (Golpes/Contusiones)", "Violencia Física Grave (Lesiones con secuelas)", "Violencia Verbal e Insultos",
            "Violencia Económica (Retención de dinero)", "Violencia Patrimonial (Destrucción de bienes)", "Violencia Sexual / Coerción", "Violencia Digital / Ciberacoso", "Violencia Simbólica y Humillación",
            "Violencia Vicaria (Daño a través de hijos)", "Amenazas de Muerte / Intimidación", "Aislamiento Social Forzado", "Celos Patológicos / Control de conducta", "Violencia durante el Embarazo",
            "Violencia Ambiental (Golpear paredes/puertas)", "Negligencia y Omisión de Cuidados", "Privación Ilegal de la Libertad", "Hostigamiento Continuo", "Violencia Cruzada / Escala de conflicto"
        ]
    }

    for table_name, items in catalogos.items():
        sql.append(f"-- --------------------------------------------------------")
        sql.append(f"-- Tabla: {table_name} (20 registros)")
        sql.append(f"-- --------------------------------------------------------")
        sql.append(f"INSERT INTO {table_name} (id, nombre, activo, created_by, is_deleted) VALUES")
        values_list = []
        for i, item in enumerate(items, 1):
            val_escaped = item.replace("'", "''")
            values_list.append(f"  ({i}, '{val_escaped}', true, 1, false)")
        sql.append(",\n".join(values_list) + ";\n")
        sql.append(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), (SELECT MAX(id) FROM {table_name}));\n")

    # 2. TABLA: agresor (20 REGISTROS)
    sql.append("-- --------------------------------------------------------")
    sql.append("-- Tabla: agresor (20 registros)")
    sql.append("-- --------------------------------------------------------")
    sql.append("INSERT INTO agresor (folio, curp, nombre, apellido_paterno, apellido_materno, edad, lugar_nacimiento, lugar_residencia, lugar_trabajo, parejas_previas, hijos, hermanos, estado_civil_id, situacion_academica_id, situacion_laboral_id, situacion_vivienda_id, rango_salarial_id, religion_id, relacion_hijos_id, created_by, is_deleted) VALUES")

    agresores = [
        ("ABCD800101HDFRND01", "Carlos", "Hernández", "García", 46, -99.1332, 19.4326, -99.2312, 18.9211, -99.2200, 18.9150, 2, 2, 3, 1, 5, 1, 3, 4, 1, 2),
        ("EFGH820202HDFRND02", "Jorge", "Martínez", "López", 44, -99.2341, 18.9221, -99.2380, 18.9250, -99.2150, 18.9300, 1, 3, 2, 2, 7, 6, 1, 6, 1, 1),
        ("IJKL850303HDFRND03", "Roberto", "González", "Pérez", 41, -99.1820, 19.3520, -99.2500, 18.9100, -99.2450, 18.9050, 3, 1, 4, 4, 3, 4, 4, 2, 2, 3),
        ("MNOP880404HDFRND04", "Miguel Ángel", "Rodríguez", "Sánchez", 38, -99.1410, 19.4100, -99.2250, 18.9350, -99.2100, 18.9400, 0, 0, 1, 1, 10, 7, 9, 8, 1, 20),
        ("QRST900505HDFRND05", "Fernando", "Ramírez", "Flores", 36, -99.2100, 18.9500, -99.2150, 18.9480, -99.2300, 18.9200, 2, 2, 2, 5, 5, 8, 2, 5, 1, 4),
        ("UVWX920606HDFRND06", "Alejandro", "Cruz", "Morales", 34, -99.1500, 19.4000, -99.2400, 18.9150, -99.2350, 18.9100, 1, 1, 3, 2, 4, 1, 3, 4, 3, 2),
        ("YZAB940707HDFRND07", "Luis Enrique", "Gómez", "Vázquez", 32, -99.2200, 18.9300, -99.2220, 18.9320, -99.2180, 18.9280, 2, 2, 1, 4, 7, 9, 10, 7, 1, 1),
        ("CDEF950808HDFRND08", "Ricardo", "Díaz", "Reyes", 31, -99.1700, 19.3800, -99.2600, 18.9050, -99.2550, 18.9000, 1, 0, 2, 1, 12, 10, 1, 11, 14, 20),
        ("GHIJ960909HDFRND09", "Héctor", "Reyes", "Jiménez", 30, -99.2450, 18.9180, -99.2480, 18.9200, -99.2400, 18.9150, 3, 3, 4, 2, 5, 6, 3, 5, 1, 5),
        ("KLMN971010HDFRND10", "Víctor Manuel", "Morales", "Torres", 29, -99.1300, 19.4200, -99.2300, 18.9400, -99.2200, 18.9350, 1, 1, 2, 4, 6, 1, 4, 6, 2, 2),
        ("OPQR981111HDFRND11", "Juan Carlos", "Ortiz", "Gutiérrez", 28, -99.2050, 18.9600, -99.2100, 18.9550, -99.2250, 18.9400, 0, 1, 3, 1, 9, 3, 5, 3, 1, 3),
        ("STUV991212HDFRND12", "Daniel", "Gutiérrez", "Castro", 27, -99.1600, 19.3900, -99.2350, 18.9280, -99.2400, 18.9300, 2, 2, 1, 2, 7, 7, 2, 7, 1, 1),
        ("WXYZ000113HDFRND13", "Gabriel", "Castro", "Romero", 26, -99.2350, 18.9120, -99.2380, 18.9150, -99.2300, 18.9100, 1, 0, 2, 1, 5, 8, 6, 4, 4, 20),
        ("BCDE010214HDFRND14", "Raúl", "Vargas", "Ruiz", 25, -99.1450, 19.4150, -99.2550, 18.9080, -99.2500, 18.9050, 1, 1, 4, 4, 3, 1, 3, 3, 1, 4),
        ("FGHI020315HDFRND15", "Arturo", "Mendoza", "Medina", 24, -99.2150, 18.9450, -99.2180, 18.9420, -99.2250, 18.9380, 0, 0, 1, 1, 7, 15, 6, 2, 14, 20),
        ("JKLM030416HDFRND16", "Gerardo", "Aguilar", "Navarro", 23, -99.1750, 19.3750, -99.2420, 18.9220, -99.2380, 18.9200, 1, 1, 2, 2, 5, 2, 4, 5, 1, 2),
        ("NOPQ810517HDFRND17", "Eduardo", "Ramos", "Delgado", 45, -99.2250, 18.9320, -99.2280, 18.9300, -99.2200, 18.9250, 4, 4, 5, 5, 2, 5, 8, 1, 1, 5),
        ("RSTU830618HDFRND18", "Salvador", "Vega", "Castillo", 43, -99.1350, 19.4280, -99.2500, 18.9150, -99.2450, 18.9120, 2, 3, 3, 2, 7, 11, 1, 12, 1, 1),
        ("VWXY860719HDFRND19", "Octavio", "Silva", "Estrada", 40, -99.2500, 18.9080, -99.2520, 18.9100, -99.2480, 18.9050, 1, 2, 2, 4, 10, 9, 9, 8, 2, 3),
        ("ZABC890820HDFRND20", "Armando", "Paredes", "Soto", 37, -99.1550, 19.4050, -99.2300, 18.9350, -99.2250, 18.9320, 3, 1, 1, 2, 5, 6, 3, 6, 1, 2)
    ]

    agresor_rows = []
    for idx, a in enumerate(agresores, 1):
        curp, nom, ap, am, edad, lon_nac, lat_nac, lon_res, lat_res, lon_tra, lat_tra, prev, hij, herm, ec, sa, sl, sv, rs, rel, rh = a
        geom_nac = f"ST_SetSRID(ST_MakePoint({lon_nac}, {lat_nac}), 4326)"
        geom_res = f"ST_SetSRID(ST_MakePoint({lon_res}, {lat_res}), 4326)"
        geom_tra = f"ST_SetSRID(ST_MakePoint({lon_tra}, {lat_tra}), 4326)"
        row_str = f"  ({idx}, '{curp}', '{nom}', '{ap}', '{am}', {edad}, {geom_nac}, {geom_res}, {geom_tra}, {prev}, {hij}, {herm}, {ec}, {sa}, {sl}, {sv}, {rs}, {rel}, {rh}, 1, false)"
        agresor_rows.append(row_str)
    sql.append(",\n".join(agresor_rows) + ";\n")
    sql.append("SELECT setval(pg_get_serial_sequence('agresor', 'folio'), (SELECT MAX(folio) FROM agresor));\n")

    # 3. TABLAS PIVOTE M:N (20 REGISTROS C/U)
    pivots = [
        ("agresor_sectorsocial", "agresor_folio", "sector_social_id", [(i, (i % 20) + 1) for i in range(1, 21)]),
        ("agresor_actividadrecreativa", "agresor_folio", "actividad_id", [(i, ((i + 2) % 20) + 1) for i in range(1, 21)]),
        ("agresor_adiccion", "agresor_folio", "adiccion_id", [(i, ((i + 1) % 20) + 1) for i in range(1, 21)]),
        ("agresor_generomusical", "agresor_folio", "genero_id", [(i, ((i + 3) % 20) + 1) for i in range(1, 21)]),
        ("agresor_relacionhermanos", "agresor_folio", "tipo_relacion_id", [(i, ((i + 4) % 20) + 1) for i in range(1, 21)]),
        ("agresor_relacionmadre", "agresor_folio", "tipo_relacion_id", [(i, ((i + 5) % 20) + 1) for i in range(1, 21)]),
        ("agresor_relacionpadre", "agresor_folio", "tipo_relacion_id", [(i, ((i + 6) % 20) + 1) for i in range(1, 21)]),
        ("agresor_tipoviolenciainfantil", "agresor_folio", "tipo_violencia_id", [(i, ((i + 7) % 20) + 1) for i in range(1, 21)])
    ]

    for p_table, col1, col2, pairs in pivots:
        sql.append(f"-- --------------------------------------------------------")
        sql.append(f"-- Tabla Pivote: {p_table} (20 registros)")
        sql.append(f"-- --------------------------------------------------------")
        sql.append(f"INSERT INTO {p_table} ({col1}, {col2}) VALUES")
        sql.append(",\n".join([f"  ({c1}, {c2})" for c1, c2 in pairs]) + ";\n")

    # 4. TABLA: sesion (20 REGISTROS)
    sql.append("-- --------------------------------------------------------")
    sql.append("-- Tabla: sesion (20 registros)")
    sql.append("-- --------------------------------------------------------")
    sql.append("INSERT INTO sesion (folio, nombre, objetivo, created_by, is_deleted) VALUES")
    sesiones = [
        ("Módulo 1: Reconocimiento de la Violencia", "Identificar los tipos y modalidades de violencia ejercida en el ámbito familiar y de pareja."),
        ("Módulo 2: Construcción de la Masculinidad", "Analizar los mandatos tradicionales de género y su impacto en las relaciones interpersonales."),
        ("Módulo 3: Manejo Emocional y Autocontrol", "Desarrollar herramientas cognitivas para la identificación y contención de la ira."),
        ("Módulo 4: Comunicación Asertiva", "Fomentar el diálogo no violento y la escucha activa en la resolución de conflictos."),
        ("Módulo 5: Responsabilidad y Consecuencias", "Asumir la responsabilidad de los actos violentos sin justificaciones externas."),
        ("Módulo 6: Empatía y Reparación del Daño", "Comprender el impacto psicológico y físico causado en las víctimas y familiares."),
        ("Módulo 7: Paternidad Afectiva y Cuidado", "Promover roles parentales basados en el respeto, el afecto y la no violencia."),
        ("Módulo 8: Celos y Necesidad de Control", "Desarticular conductas de posesión, control digital y celotipia en la pareja."),
        ("Módulo 9: Resolución Pacífica de Conflictos", "Adquirir técnicas de negociación y mediación pacífica ante desacuerdos cotidianos."),
        ("Módulo 10: Prevención de Recaídas en Crisis", "Elaborar un plan personal de acción y contención ante detonantes emocionales."),
        ("Módulo 11: Desmitificación del Amor Romántico", "Cuestionar falsas creencias sobre el amor que legitiman el abuso y la dependencia."),
        ("Módulo 12: Uso del Tiempo Libre y Recreación", "Incorporar actividades recreativas y deportivas saludables libres de adicciones."),
        ("Módulo 13: Manejo del Estrés y Ansiedad", "Aprender técnicas de relajación física y respiración diafragmática para momentos de tensión."),
        ("Módulo 14: Violencia Económica y Patrimonial", "Analizar el manejo equitativo de los recursos económicos y bienes familiares."),
        ("Módulo 15: Convivencia con Familia de Origen", "Establecer límites saludables en las relaciones con padres y hermanos."),
        ("Módulo 16: Redes Sociales y Violencia Digital", "Reconocer conductas invasivas y de acoso en medios digitales y mensajería."),
        ("Módulo 17: Redes de Apoyo Positivas", "Fomentar círculos sociales constructivos y abandonar entornos de socialización violenta."),
        ("Módulo 18: Salud Mental y Autocuidado", "Fomentar hábitos de salud física, mental y la búsqueda oportuna de ayuda profesional."),
        ("Módulo 19: Plan de Vida Libre de Violencia", "Diseñar metas personales, familiares y laborales a mediano y largo plazo."),
        ("Módulo 20: Evaluación y Cierre de Proceso", "Evaluar el grado de internalización de los principios de no violencia y entrega de balance.")
    ]
    sesion_rows = []
    for idx, (nom, obj) in enumerate(sesiones, 1):
        nom_esc = nom.replace("'", "''")
        obj_esc = obj.replace("'", "''")
        sesion_rows.append(f"  ({idx}, '{nom_esc}', '{obj_esc}', 1, false)")
    sql.append(",\n".join(sesion_rows) + ";\n")
    sql.append("SELECT setval(pg_get_serial_sequence('sesion', 'folio'), (SELECT MAX(folio) FROM sesion));\n")

    # 5. TABLA: grupo (20 REGISTROS)
    sql.append("-- --------------------------------------------------------")
    sql.append("-- Tabla: grupo (20 registros)")
    sql.append("-- --------------------------------------------------------")
    sql.append("INSERT INTO grupo (folio, lugar, ubicacion, created_by, is_deleted) VALUES")
    grupos = [
        ("Centro Comunitario Cuernavaca Centro", -99.2345, 18.9215),
        ("Sede Norte - Chamilpa", -99.2450, 18.9680),
        ("Centro de Desarrollo Comunitario Jiutepec", -99.1780, 18.8810),
        ("Módulo DIF Temixco", -99.2290, 18.8540),
        ("Casa de Cultura Emiliano Zapata", -99.1820, 18.8350),
        ("Centro Comunitario Cuautla Centro", -98.9550, 18.8120),
        ("Sede Reeducativa Yautepec", -99.0680, 18.8820),
        ("Módulo de Atención Xochitepec", -99.2310, 18.7810),
        ("Centro Social Jojutla", -99.1820, 18.6150),
        ("Sede DIF Zacatepec", -99.1950, 18.6540),
        ("Centro Integrador Tepoztlán", -99.0980, 18.9850),
        ("Módulo Comunitario Huitzilac", -99.2680, 19.0310),
        ("Centro Reeducativo Puente de Ixtla", -99.3210, 18.6180),
        ("Sede Yecapixtla", -98.8650, 18.8820),
        ("Centro Social Ayala", -98.9820, 18.7650),
        ("Módulo Tlaltizapán Centro", -99.1200, 18.6850),
        ("Sede Tetecala", -99.4010, 18.7290),
        ("Centro Comunitario Miacatlán", -99.3620, 18.7680),
        ("Módulo DIF Tlayacapan", -98.9850, 18.9560),
        ("Centro de Atención Ocuituco", -98.7750, 18.8780)
    ]
    grupo_rows = []
    for idx, (lug, lon, lat) in enumerate(grupos, 1):
        geom_str = f"ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326)"
        lug_esc = lug.replace("'", "''")
        grupo_rows.append(f"  ({idx}, '{lug_esc}', {geom_str}, 1, false)")
    sql.append(",\n".join(grupo_rows) + ";\n")
    sql.append("SELECT setval(pg_get_serial_sequence('grupo', 'folio'), (SELECT MAX(folio) FROM grupo));\n")

    # 6. TABLA: procesoreeducacion (20 REGISTROS)
    sql.append("-- --------------------------------------------------------")
    sql.append("-- Tabla: procesoreeducacion (20 registros)")
    sql.append("-- --------------------------------------------------------")
    sql.append("INSERT INTO procesoreeducacion (folio, agresor_id, fecha_inicio, fecha_termino, fecha_denuncia, denunciante, folio_carpeta_fiscalia, motivo_ingreso_id, tipo_violencia_id, modalidad_violencia_id, created_by, is_deleted) VALUES")
    procesos = [
        (1, "2026-01-15", "2026-06-15", "2025-11-20", "María Elena Torres", "SC01/12345/2025", 1, 1, 1),
        (2, "2026-01-20", "2026-07-20", "2025-12-05", "Patricia Mendoza", "SC02/23456/2025", 2, 2, 1),
        (3, "2026-02-01", "2026-08-01", "2025-12-18", "Gabriela Soto", "SC03/34567/2025", 3, 3, 2),
        (4, "2026-02-10", "2026-08-10", "2026-01-08", "Lucía Ramírez", "SC01/45678/2026", 4, 1, 1),
        (5, "2026-02-15", "2026-08-15", "2026-01-14", "Ana María Castro", "SC02/56789/2026", 5, 4, 3),
        (6, "2026-03-01", "2026-09-01", "2026-01-22", "Rosa Isela Gómez", "SC03/67890/2026", 1, 5, 1),
        (7, "2026-03-05", "2026-09-05", "2026-02-01", "Claudia Morales", "SC01/78901/2026", 2, 6, 2),
        (8, "2026-03-10", "2026-09-10", "2026-02-10", "Verónica Ortiz", "SC02/89012/2026", 3, 7, 1),
        (9, "2026-03-15", "2026-09-15", "2026-02-15", "Adriana Ruiz", "SC03/90123/2026", 4, 1, 4),
        (10, "2026-04-01", "2026-10-01", "2026-02-28", "Silvia Hernández", "SC01/01234/2026", 5, 2, 1),
        (11, "2026-04-05", "2026-10-05", "2026-03-05", "Teresa Gutiérrez", "SC02/12340/2026", 1, 3, 2),
        (12, "2026-04-10", "2026-10-10", "2026-03-12", "Mónica Delgado", "SC03/23451/2026", 2, 4, 1),
        (13, "2026-04-15", "2026-10-15", "2026-03-18", "Lorena Castillo", "SC01/34562/2026", 3, 1, 3),
        (14, "2026-05-01", "2026-11-01", "2026-03-25", "Karla Estrada", "SC02/45673/2026", 4, 5, 1),
        (15, "2026-05-05", "2026-11-05", "2026-04-02", "Daniela Vargas", "SC03/56784/2026", 5, 6, 2),
        (16, "2026-05-10", "2026-11-10", "2026-04-10", "Sofía Medina", "SC01/67895/2026", 1, 7, 1),
        (17, "2026-05-15", "2026-11-15", "2026-04-18", "Guadalupe Reyes", "SC02/78906/2026", 2, 8, 4),
        (18, "2026-06-01", "2026-12-01", "2026-04-25", "Beatriz Díaz", "SC03/89017/2026", 3, 1, 1),
        (19, "2026-06-05", "2026-12-05", "2026-05-02", "Sandra Jiménez", "SC01/90128/2026", 4, 2, 2),
        (20, "2026-06-10", "2026-12-10", "2026-05-10", "Yolanda Navarro", "SC02/01239/2026", 5, 3, 1)
    ]
    proceso_rows = []
    for idx, (agr_id, f_ini, f_ter, f_den, den, fol_fisc, mi, tv, mv) in enumerate(procesos, 1):
        den_esc = den.replace("'", "''")
        proceso_rows.append(f"  ({idx}, {agr_id}, '{f_ini}', '{f_ter}', '{f_den}', '{den_esc}', '{fol_fisc}', {mi}, {tv}, {mv}, 1, false)")
    sql.append(",\n".join(proceso_rows) + ";\n")
    sql.append("SELECT setval(pg_get_serial_sequence('procesoreeducacion', 'folio'), (SELECT MAX(folio) FROM procesoreeducacion));\n")

    # 7. TABLA: lista (20 REGISTROS DE ASISTENCIA)
    sql.append("-- --------------------------------------------------------")
    sql.append("-- Tabla: lista (20 registros de asistencias)")
    sql.append("-- --------------------------------------------------------")
    sql.append("INSERT INTO lista (id, agresor_id, grupo_id, sesion_id, fecha, created_by, is_deleted) VALUES")
    listas = [
        (1, 1, 1, 1, "2026-01-16"),
        (2, 2, 1, 1, "2026-01-16"),
        (3, 3, 2, 1, "2026-01-17"),
        (4, 4, 2, 1, "2026-01-17"),
        (5, 5, 3, 2, "2026-01-23"),
        (6, 6, 3, 2, "2026-01-23"),
        (7, 7, 4, 2, "2026-01-24"),
        (8, 8, 4, 3, "2026-01-30"),
        (9, 9, 5, 3, "2026-01-30"),
        (10, 10, 5, 4, "2026-02-06"),
        (11, 11, 6, 4, "2026-02-06"),
        (12, 12, 6, 5, "2026-02-13"),
        (13, 13, 7, 5, "2026-02-13"),
        (14, 14, 7, 6, "2026-02-20"),
        (15, 15, 8, 6, "2026-02-20"),
        (16, 16, 8, 7, "2026-02-27"),
        (17, 17, 9, 7, "2026-02-27"),
        (18, 18, 9, 8, "2026-03-06"),
        (19, 19, 10, 8, "2026-03-06"),
        (20, 20, 10, 9, "2026-03-13")
    ]
    lista_rows = []
    for idx, agr_id, grp_id, ses_id, fec in listas:
        lista_rows.append(f"  ({idx}, {agr_id}, {grp_id}, {ses_id}, '{fec}', 1, false)")
    sql.append(",\n".join(lista_rows) + ";\n")
    sql.append("SELECT setval(pg_get_serial_sequence('lista', 'id'), (SELECT MAX(id) FROM lista));\n")

    sql.append("COMMIT;\n")
    sql.append("-- ========================================================")
    sql.append("-- FIN DEL SCRIPT")
    sql.append("-- ========================================================")

    return "\n".join(sql)

if __name__ == "__main__":
    content = generate_sql()
    output_path = "/Users/daredev/Desktop/PUA/backend/seed_data.sql"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Archivo SQL generado con éxito en: {output_path}")
