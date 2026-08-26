import unittest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.core.usuario import VerificadorRol
from app.models.usuarios import Usuarios, Roles

class TestRoleVerifier(unittest.TestCase):

    def test_role_permitted(self):
        verificador = VerificadorRol(["SUPER_ADMIN", "COORDINADOR"])
        
        rol = Roles(id=1, nombre="SUPER_ADMIN")
        usuario = Usuarios(id=1, username="admin", rol=rol, is_active=True)

        resultado = verificador(usuario=usuario)
        self.assertEqual(resultado, usuario)

    def test_role_forbidden(self):
        verificador = VerificadorRol(["SUPER_ADMIN"])
        
        rol = Roles(id=2, nombre="OPERADOR")
        usuario = Usuarios(id=2, username="operador", rol=rol, is_active=True)

        with self.assertRaises(HTTPException) as ctx:
            verificador(usuario=usuario)
        
        self.assertEqual(ctx.exception.status_code, 403)

if __name__ == "__main__":
    unittest.main()
