import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Cargamos el .env local solo si existe (para desarrollo en tu Mac)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# 2. Leemos la variable (la leerá del .env en tu Mac, o de Coolify en el servidor)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 3. Freno de emergencia por si olvidaste inyectarla en Coolify o crear tu .env
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError(f"🚨 ERROR CRÍTICO: No se encontró DATABASE_URL. Verifica tus variables de entorno o tu archivo en: {dotenv_path}")

# 4. CORRECCIÓN CLAVE: SQLAlchemy moderno exige 'postgresql://' en lugar de 'postgres://'
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Crear el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()