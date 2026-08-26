import unittest
from datetime import date
from pydantic import ValidationError

from app.schemas.agresores import AgresorCreate
from app.schemas.catalogos import ActividadRecreativaCreate
from app.schemas.procesos import ProcesoReeducacionCreate, SesionCreate, GrupoCreate, ListaCreate
from app.schemas.mixins import Coordenadas

class TestSchemas(unittest.TestCase):

    def test_catalogo_create_valid(self):
        cat = ActividadRecreativaCreate(nombre="Fútbol", activo=True)
        self.assertEqual(cat.nombre, "Fútbol")
        self.assertTrue(cat.activo)

    def test_catalogo_create_invalid_length(self):
        with self.assertRaises(ValidationError):
            ActividadRecreativaCreate(nombre="A")  # min_length is 2

    def test_coordenadas_valid(self):
        coord = Coordenadas(latitud=18.921, longitud=-99.234)
        self.assertEqual(coord.latitud, 18.921)
        self.assertEqual(coord.longitud, -99.234)

    def test_agresor_create_valid(self):
        agresor = AgresorCreate(
            curp="ABCD123456HDFRND01",
            nombre="Juan",
            apellido_paterno="Pérez",
            apellido_materno="López",
            edad=35,
            parejas_previas=1,
            hijos=2,
            hermanos=3,
            estado_civil_id=1,
            situacion_academica_id=1,
            situacion_laboral_id=1,
            situacion_vivienda_id=1,
            rango_salarial_id=1,
            religion_id=1,
            relacion_hijos_id=1,
            lugar_nacimiento=Coordenadas(latitud=19.4326, longitud=-99.1332),
            lugar_residencia=Coordenadas(latitud=19.4326, longitud=-99.1332),
            lugar_trabajo=Coordenadas(latitud=19.4326, longitud=-99.1332),
            adicciones=[1, 2],
            sectores_sociales=[1]
        )
        self.assertEqual(agresor.curp, "ABCD123456HDFRND01")
        self.assertEqual(agresor.edad, 35)

    def test_agresor_create_invalid_curp(self):
        with self.assertRaises(ValidationError):
            AgresorCreate(
                curp="CURP_CORTA",  # Invalid length / pattern
                nombre="Juan",
                apellido_paterno="Pérez",
                edad=35,
                parejas_previas=1,
                hijos=2,
                hermanos=3,
                estado_civil_id=1,
                situacion_academica_id=1,
                situacion_laboral_id=1,
                situacion_vivienda_id=1,
                rango_salarial_id=1,
                religion_id=1,
                relacion_hijos_id=1
            )

    def test_proceso_reeducacion_create_valid(self):
        proceso = ProcesoReeducacionCreate(
            agresor_id=1,
            fecha_inicio=date(2026, 1, 15),
            fecha_termino=date(2026, 6, 15),
            denunciante="Persona A",
            folio_carpeta_fiscalia="EXP-2026-001",
            motivo_ingreso_id=1,
            tipo_violencia_id=1,
            modalidad_violencia_id=1
        )
        self.assertEqual(proceso.agresor_id, 1)
        self.assertEqual(proceso.denunciante, "Persona A")

    def test_sesion_create_valid(self):
        sesion = SesionCreate(nombre="Manejo de la Ira", objetivo="Desarrollar autocontrol emocional")
        self.assertEqual(sesion.nombre, "Manejo de la Ira")

    def test_grupo_create_valid(self):
        grupo = GrupoCreate(lugar="Centro Comunitario Norte", ubicacion=Coordenadas(latitud=18.9, longitud=-99.2))
        self.assertEqual(grupo.lugar, "Centro Comunitario Norte")

    def test_lista_create_valid(self):
        lista = ListaCreate(agresor_id=1, grupo_id=1, sesion_id=1, fecha=date(2026, 2, 1))
        self.assertEqual(lista.agresor_id, 1)

if __name__ == "__main__":
    unittest.main()
