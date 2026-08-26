import unittest
from datetime import timedelta
import jwt

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)

class TestSecurity(unittest.TestCase):

    def test_password_hashing_and_verification(self):
        password = "MiPasswordSeguro123!"
        hashed = get_password_hash(password)
        
        self.assertNotEqual(password, hashed)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("PasswordIncorrecto", hashed))

    def test_create_access_token(self):
        data = {"sub": "1", "rol_id": 2}
        token = create_access_token(data=data, expires_delta=timedelta(minutes=30))
        
        self.assertIsInstance(token, str)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(payload["sub"], "1")
        self.assertEqual(payload["rol_id"], 2)
        self.assertIn("exp", payload)

    def test_invalid_token_decode(self):
        invalid_token = "token.invalido.falso"
        with self.assertRaises(jwt.PyJWTError):
            jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])

if __name__ == "__main__":
    unittest.main()
