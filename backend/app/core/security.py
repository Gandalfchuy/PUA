import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional

def get_password_hash(password: str) -> str:
    # bcrypt requiere que los strings se conviertan a bytes
    pwd_bytes = password.encode('utf-8')
    # Generamos la sal y el hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Lo regresamos como string normal para guardarlo en la base de datos
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convertimos ambos a bytes para la comparación matemática
    password_bytes = plain_password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hash_bytes)

SECRET_KEY = "tu_super_clave_secreta_super_segura_y_larga" # Cambia esto por algo aleatorio luego
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 horas de jornada laboral

# 2. La función que fabrica el Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # Hacemos una copia de los datos que queremos guardar en el token (ej. ID y Rol)
    to_encode = data.copy()
    
    # Calculamos la fecha y hora exacta en la que el token "morirá"
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    # Agregamos la fecha de expiración ('exp') al paquete de datos
    to_encode.update({"exp": expire})
    
    # Sellamos el token con nuestra llave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt