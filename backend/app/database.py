import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Calculamos la ruta absoluta a la raíz de tu proyecto (carpeta backend)
# __file__ es app/database.py. Subimos un nivel para llegar a backend/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, ".env")

# 2. Forzamos a cargar específicamente ese archivo
load_dotenv(dotenv_path)

# 3. Leemos la variable
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 4. Freno de emergencia (Si sigue fallando, te dirá exactamente dónde lo buscó)
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError(f"🚨 ERROR CRÍTICO: No se encontró DATABASE_URL. \nPor favor verifica que tu archivo exista exactamente en esta ruta: {dotenv_path} \ny que la variable se llame 'DATABASE_URL'.")

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