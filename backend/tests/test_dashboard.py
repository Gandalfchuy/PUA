import unittest
from datetime import date
from pydantic import ValidationError

from app.schemas.dashboard import (
    DashboardKpisResponse,
    PuntoCalor,
    SedeMapa,
    DashboardMapaResponse,
    TipoViolenciaStat,
    DashboardViolenciaResponse,
    AdiccionStat,
    DashboardAdiccionesResponse,
    AlertaDesercionItem,
    DashboardAlertasResponse
)

class TestDashboardSchemas(unittest.TestCase):

    def test_kpis_response_valid(self):
        kpis = DashboardKpisResponse(
            total_activos=25,
            tasa_asistencia=82.5,
            alertas_desercion=3,
            procesos_concluidos=12
        )
        self.assertEqual(kpis.total_activos, 25)
        self.assertEqual(kpis.tasa_asistencia, 82.5)
        self.assertEqual(kpis.alertas_desercion, 3)
        self.assertEqual(kpis.procesos_concluidos, 12)

    def test_mapa_response_valid(self):
        puntos = [PuntoCalor(lat=18.92, lng=-99.23, peso=1.0)]
        sedes = [SedeMapa(folio=1, lugar="Centro Cuernavaca", lat=18.921, lng=-99.235)]
        mapa = DashboardMapaResponse(puntos_calor=puntos, sedes=sedes)
        
        self.assertEqual(len(mapa.puntos_calor), 1)
        self.assertEqual(len(mapa.sedes), 1)
        self.assertEqual(mapa.sedes[0].lugar, "Centro Cuernavaca")

    def test_violencias_response_valid(self):
        tipos = [
            TipoViolenciaStat(tipo="Violencia Psicológica", total=15, porcentaje=60.0),
            TipoViolenciaStat(tipo="Violencia Física", total=10, porcentaje=40.0)
        ]
        resp = DashboardViolenciaResponse(tipos=tipos)
        self.assertEqual(len(resp.tipos), 2)
        self.assertEqual(resp.tipos[0].tipo, "Violencia Psicológica")

    def test_adicciones_response_valid(self):
        stats = [
            AdiccionStat(adiccion="Alcoholismo", total=12, porcentaje=50.0),
            AdiccionStat(adiccion="Cannabis", total=6, porcentaje=25.0)
        ]
        resp = DashboardAdiccionesResponse(adicciones=stats)
        self.assertEqual(len(resp.adicciones), 2)
        self.assertEqual(resp.adicciones[0].total, 12)

    def test_alertas_response_valid(self):
        alertas = [
            AlertaDesercionItem(
                agresor_id=1,
                curp="ABCD800101HDFRND01",
                nombre_completo="Carlos Hernández García",
                grupo="Sede Centro",
                faltas_consecutivas=3,
                ultima_asistencia=date(2026, 1, 15),
                carpeta_fiscalia="EXP-1234/2026"
            )
        ]
        resp = DashboardAlertasResponse(alertas=alertas)
        self.assertEqual(len(resp.alertas), 1)
        self.assertEqual(resp.alertas[0].agresor_id, 1)
        self.assertEqual(resp.alertas[0].faltas_consecutivas, 3)

if __name__ == "__main__":
    unittest.main()
