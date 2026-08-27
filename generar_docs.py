import os

markdown_content = """# Desglose Técnico del Proyecto PUA (Plataforma Única de Atención a Generadores de Violencia)

## 1. Introducción y Arquitectura General
El proyecto PUA es una plataforma web integral diseñada para la atención, gestión y geointeligencia de generadores de violencia. Está compuesto por una arquitectura Cliente-Servidor separada:
- **Backend:** Desarrollado en Python utilizando el framework FastAPI. Proporciona una API RESTful, manejo de autenticación con JWT, y conexión a una base de datos relacional PostgreSQL con extensión PostGIS para análisis geoespacial.
- **Frontend:** Desarrollado en TypeScript con Angular 21 utilizando el enfoque de Standalone Components. Se encarga de la interfaz de usuario, consumo de la API, y visualización de datos (incluyendo mapas interactivos y gráficos).
- **Base de Datos:** PostgreSQL con PostGIS.

---

## 2. Librerías y Dependencias

### Backend (Python / FastAPI)
- **FastAPI:** Framework web principal para la construcción de la API. Implementa el ruteo, validación y documentación automática (Swagger/OpenAPI).
- **Uvicorn:** Servidor ASGI para ejecutar la aplicación FastAPI.
- **SQLAlchemy:** ORM (Object Relational Mapper) utilizado para interactuar con la base de datos PostgreSQL. Transforma clases de Python en tablas de SQL.
- **GeoAlchemy2:** Extensión de SQLAlchemy para manejar tipos de datos espaciales (Geometry, Geography) de PostGIS.
- **Pydantic:** Librería para validación de datos y gestión de configuraciones basada en anotaciones de tipos de Python. Utilizada para definir los "Schemas".
- **Alembic:** Herramienta de migración de bases de datos para SQLAlchemy.
- **Passlib & Bcrypt:** Librerías para el hashing seguro de contraseñas de usuarios.
- **PyJWT:** Generación y validación de JSON Web Tokens (JWT) para la autenticación y autorización.
- **Psycopg2-binary:** Driver de PostgreSQL para Python.
- **Pytest:** Framework de pruebas unitarias y de integración.

### Frontend (Angular / TypeScript)
- **@angular/core, @angular/common, @angular/router:** Core del framework Angular, directivas comunes y enrutador.
- **@angular/forms:** Manejo de formularios reactivos (`ReactiveFormsModule`).
- **@angular/common/http:** Cliente HTTP (`HttpClient`) para consumir la API del backend.
- **TailwindCSS:** Framework de CSS utilitario para el diseño y maquetación de la interfaz de forma ágil y responsiva.
- **Chart.js & ng2-charts:** Librerías para la renderización de los gráficos de barras, pastel y dona en el Dashboard.
- **Leaflet & leaflet.heat:** Librerías de mapas interactivos de código abierto. `leaflet.heat` se utiliza específicamente para renderizar el mapa de calor geoespacial.
- **Lucide-Angular:** Biblioteca de iconos vectoriales utilizados en toda la interfaz (botones, sidebar, tarjetas).
- **Vitest:** Framework de pruebas para el entorno frontend, rápido y compatible con Vite.

---

## 3. Backend (FastAPI)

### 3.1. Configuración y Core
- **`app/core/config.py`**: Define la clase `Settings` (hereda de `BaseSettings` de Pydantic). Gestiona las variables de entorno (URL de base de datos, Secret Key para JWT, algoritmo).
- **`app/core/security.py`**: Contiene funciones utilitarias:
  - `verify_password(plain_password, hashed_password)`: Compara la contraseña en texto plano con el hash.
  - `get_password_hash(password)`: Genera un hash seguro usando bcrypt.
  - `create_access_token(data, expires_delta)`: Crea el JWT firmado.
- **`app/database.py`**: Configura el motor de SQLAlchemy (`create_engine`) y la fábrica de sesiones (`sessionmaker`). Define la clase base `Base = declarative_base()` de la cual heredarán todos los modelos ORM. Incluye la dependencia `get_db()` para inyectar la sesión en los endpoints.

### 3.2. Modelos ORM (Base de Datos)
Definen la estructura de las tablas en PostgreSQL. Todos heredan de `Base`.

- **`Usuario` (`app/models/usuarios.py`)**: Tabla `usuarios`.
  - **Columnas:** `id`, `email`, `hashed_password`, `nombre_completo`, `is_active`, `rol_id`, `dependencia_id`.
  - **Relaciones:** Pertenece a un `Rol` y a una `Dependencia`.
  - **Propósito:** Almacena los credenciales y perfiles de los operadores del sistema.
- **`Rol` (`app/models/roles.py`)**: Tabla `roles`.
  - **Columnas:** `id`, `nombre`, `descripcion`.
  - **Propósito:** Control de acceso basado en roles (RBAC). Ej: Administrador, Operador, Analista.
- **`Dependencia` (`app/models/dependencias.py`)**: Tabla `dependencias`.
  - **Columnas:** `id`, `nombre`, `siglas`.
  - **Propósito:** Institución a la que pertenece el usuario (ej. Fiscalía, Centro de Justicia).
- **`Agresor` (`app/models/agresores.py`)**: Tabla `agresores`.
  - **Columnas:** `id`, `nombre`, `apellidos`, `alias`, `curp`, `fecha_nacimiento`, `riesgo_feminicida`, `perfil_criminologico`, `estatus_seguimiento`, etc.
  - **Propósito:** Entidad central. Almacena los datos personales y de perfil del generador de violencia.
- **`Expediente` (`app/models/expedientes.py`)**: Tabla `expedientes`.
  - **Columnas:** `id`, `folio`, `agresor_id`, `dependencia_origen_id`, `fecha_apertura`, `delito`, `nivel_riesgo`, `estado_judicial`, `coordenadas` (Geometry('POINT')), etc.
  - **Relaciones:** Relacionado a un `Agresor` (uno a muchos).
  - **Propósito:** Registra los casos/carpetas de investigación asociados a un agresor. Incluye geolocalización.
- **`MedidaProteccion` (`app/models/expedientes.py`)**: Tabla `medidas_proteccion`.
  - **Columnas:** `id`, `expediente_id`, `tipo_medida`, `fecha_inicio`, `fecha_fin`, `activa`.
  - **Propósito:** Controla las medidas cautelares dictadas en un expediente.

### 3.3. Schemas (Pydantic)
Definen la validación y serialización de los datos que entran y salen de la API. Usan el principio de herencia.

- **Esquemas Base (Ej. `AgresorBase`)**: Contiene los atributos comunes y compartidos.
- **Esquemas de Creación (Ej. `AgresorCreate`)**: Hereda de Base. Añade validaciones específicas (ej. campos obligatorios al crear).
- **Esquemas de Respuesta (Ej. `AgresorResponse`)**: Hereda de Base. Añade el `id` y activa `from_attributes = True` (antes `orm_mode`) para parsear objetos SQLAlchemy a JSON automáticamente.
- **Esquemas de Token (`Token`, `TokenData`)**: Estructuras para manejar el login y JWT.

### 3.4. Routers (Endpoints REST)
Agrupan las rutas por entidad usando `APIRouter`.

- **`app/routers/auth.py`**:
  - `POST /token`: Valida usuario y contraseña, devuelve el JWT.
- **`app/routers/agresores.py`**:
  - Implementa operaciones CRUD completas (GET, POST, PUT, DELETE).
  - `GET /agresores`: Soporta paginación, búsqueda por texto, y filtrado dinámico.
- **`app/routers/expedientes.py`**:
  - CRUD para expedientes.
  - Manejo de coordenadas PostGIS en WKT para recepción, e inserción usando `ST_GeomFromText`.
- **`app/routers/dashboard.py`**:
  - Endpoints analíticos optimizados con funciones de agregación SQL (`func.count`, `func.sum`).
  - `GET /dashboard/kpis`: Retorna métricas clave (Total Agresores, Riesgo Alto, Alertas).
  - `GET /dashboard/mapa-calor`: Extrae las coordenadas de los expedientes usando `func.ST_X` y `func.ST_Y` para enviarlas al mapa.
  - `GET /dashboard/violencias` / `adicciones` / `alertas`: Agrupaciones para gráficos.

### 3.5. Servicios y Utilidades
- **`app/services/auth_service.py`**: Contiene la dependencia `get_current_user` y `get_current_active_user`. Estas funciones extraen el Token del header HTTP, lo decodifican, y buscan al usuario en la BD. Si falla, lanzan `HTTPException(401)`.

---

## 4. Frontend (Angular 21)

### 4.1. Arquitectura y Core
- Aplicación basada 100% en **Standalone Components**, eliminando `NgModules`.
- **`app.config.ts`**: Configura proveedores globales, enrutamiento, e inyecta el `HttpClient` global con los interceptores.
- **`app.routes.ts`**: Define el mapeo de URLs a Componentes utilizando Lazy Loading (`loadComponent`) para optimizar el peso inicial de la aplicación.

### 4.2. Servicios
Clases decoradas con `@Injectable({ providedIn: 'root' })` para manejar la lógica de negocio y comunicación con el backend.

- **`BaseCrudService<T, CreateDto, UpdateDto>` (`app/core/services/base-crud.service.ts`)**:
  - **Propósito:** Clase genérica que implementa los métodos estándar (getAll, getById, create, update, delete) utilizando el `HttpClient`.
  - **Variables y Funciones:** `apiUrl` (abstracta), `obtenerTodos()`, `obtenerPorId()`, etc.
  - **Implementación:** Otros servicios como `AgresoresService` heredan de este, pasando su URL específica y las interfaces correspondientes. Evita la duplicación de código HTTP.
- **`AuthService`**: Maneja el estado de sesión (BehaviorSubject), login (llama a `/token`), almacenamiento del token en `localStorage` o cookies, y el logout.
- **`DashboardService`**: Llama a los 5 endpoints de análisis del backend, tipificando las respuestas según interfaces.

### 4.3. Componentes Base y de UI
- **`BaseCrudComponent<ItemType, DetailType>` (`app/shared/base-crud.component.ts`)**:
  - **Propósito:** Componente TypeScript genérico del cual heredan las vistas de catálogo (Usuarios, Agresores, Dependencias).
  - **Variables:** `datosVista`, `formulario`, `modoEdicion`, `cargando`.
  - **Funciones:** `cargarDatos()`, `guardar()`, `editar()`, `eliminar()`, `cerrarModal()`.
  - **Implementación:** Maneja el ciclo de vida de una tabla con modal para Crear/Editar. Incorpora el método protegido `despuesDeCargarDatos()` que permite a los hijos ejecutar código inmeditamente después de popular la tabla.
- **Componentes Feature (Ej. `AgresoresComponent`)**:
  - Hereda de `BaseCrudComponent`.
  - **Implementación específica:** Usa `ActivatedRoute` para leer Query Params (`folio`, `curp`). Al iniciar, si detecta los parámetros, implementa `override despuesDeCargarDatos()` para abrir automáticamente la pestaña de "Ver Expediente" correspondiente al agresor buscado.

### 4.4. Módulo de Dashboard (Geointeligencia)
Se compone de componentes modulares (dumb & smart components).

- **`DashboardComponent` (Contenedor Smart):** Estructura el Grid de la vista e importa los submódulos.
- **`KpiCardsComponent`:** Obtiene y muestra contadores generales.
- **`MapaCalorComponent`:**
  - **Implementación:** Inyecta datos geográficos. Utiliza renderizado dinámico SSR-Safe para instanciar `leaflet`. Crea un mapa con azulejos (tiles) de OpenStreetMap y genera una capa de calor `L.heatLayer` en base a la concentración de expedientes.
- **`GraficaViolenciasComponent` / `GraficaAdiccionesComponent`:** Utilizan `Chart.js` para renderizar canvas visuales. Inyectan los datos del backend y los formatean en `ChartData`.
- **`TablaAlertasComponent`:** Muestra registros críticos y emite eventos (o redirecciones con `queryParams`) hacia el catálogo de agresores.

### 4.5. Guardias e Interceptores
- **`AuthGuard` (`CanActivateFn`)**: Protege rutas (ej. `/dashboard`, `/agresores`). Verifica con el `AuthService` si el usuario está autenticado; si no, redirecciona a `/login`.
- **`AuthInterceptor`**: Captura cada petición saliente del `HttpClient`, y añade el header `Authorization: Bearer <token>`.

---

## 5. Interconexión y Flujo de Datos (Ejemplo Práctico)
*Caso de Uso: Visualización del Mapa de Calor en el Dashboard.*

1. **Usuario** entra a `/dashboard`. El **AuthGuard** valida su sesión.
2. El **DashboardComponent** (Angular) se carga e instancia el **MapaCalorComponent**.
3. En el `ngOnInit()`, el componente inyecta el **DashboardService** y llama a `obtenerMapaCalor()`.
4. El servicio hace un GET `http://localhost:8000/dashboard/mapa-calor`. (El **AuthInterceptor** añade el JWT).
5. La petición llega al **Backend FastAPI** (`app/routers/dashboard.py`).
6. El router inyecta `get_db` y `get_current_active_user` para autorizar.
7. Se ejecuta la consulta SQLAlchemy: extrae coordenadas usando `func.ST_X(Expediente.coordenadas)` y `func.ST_Y`.
8. Se responde un JSON con el array de puntos `[lat, lng, intensidad]`.
9. Angular recibe el JSON. El **MapaCalorComponent** instancia `Leaflet` y `heatLayer`, iterando sobre los puntos y superponiéndolos al mapa base, mostrando zonas de alta incidencia de violencia (rojo) y baja (verde).

---
*Documento autogenerado para revisión técnica y mantenimiento.*
"""

with open('/Users/daredev/Desktop/PUA/Documentacion_Tecnica.md', 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print("Markdown generado exitosamente en /Users/daredev/Desktop/PUA/Documentacion_Tecnica.md")
