import os
from fastapi import FastAPI
from app.database import engine, Base
from app.models import mixins, agresores, catalogos, procesos, usuarios
from fastapi.middleware.cors import CORSMiddleware
from app.routers.catalogos import (
   router_adicciones,
   router_actividad_recreativa,
   router_estado_civil,
   router_genero_musical,
   router_modalidad_violencia,
   router_situacion_academica,
   router_motivo_ingreso,
   router_situacion_laboral,
   router_rango_salarial,
   router_relacion_hijos,
   router_religion,
   router_sectores_sociales,
   router_situacion_vivienda,
   router_tipo_relacion,
   router_tipo_violencia
)
from app.routers.agresores import router_agresor
from app.routers.procesosreeducacion import router_proceso
from app.routers.grupos import router_grupo
from app.routers.auth import router_auth
from app.routers.listas import router_lista
from app.routers.sesiones import router_sesion
from app.routers.dashboard import router_dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API PUA")

app.include_router(router_auth)
app.include_router(router_dashboard)
app.include_router(router_lista)
app.include_router(router_sesion)
app.include_router(router_proceso)
app.include_router(router_agresor)
app.include_router(router_grupo)
app.include_router(router_adicciones)
app.include_router(router_actividad_recreativa)
app.include_router(router_estado_civil)
app.include_router(router_genero_musical)
app.include_router(router_modalidad_violencia)
app.include_router(router_situacion_academica)
app.include_router(router_motivo_ingreso)
app.include_router(router_situacion_laboral)
app.include_router(router_rango_salarial)
app.include_router(router_relacion_hijos)
app.include_router(router_religion)
app.include_router(router_sectores_sociales)
app.include_router(router_situacion_vivienda)
app.include_router(router_tipo_relacion)
app.include_router(router_tipo_violencia)

@app.get("/")
def read_root():
    return {"mensaje": "¡Base de datos conectada y tablas creadas con éxito!"}

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200,http://127.0.0.1:4200")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)