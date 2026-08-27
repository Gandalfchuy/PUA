import { describe, it, expect, beforeEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { DashboardService } from './dashboard.service';
import { environment } from '../../../environments/environment';

describe('DashboardService', () => {
  let service: DashboardService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        DashboardService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(DashboardService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('debe obtener los KPIs correctamente', () => {
    const mockKpis = {
      total_activos: 20,
      tasa_asistencia: 85.0,
      alertas_desercion: 2,
      procesos_concluidos: 5
    };

    service.getKpis().subscribe((res) => {
      expect(res.total_activos).toBe(20);
      expect(res.tasa_asistencia).toBe(85.0);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/dashboard/kpis`);
    expect(req.request.method).toBe('GET');
    req.flush(mockKpis);
  });

  it('debe obtener los datos del mapa de calor', () => {
    const mockMapa = {
      puntos_calor: [{ lat: 18.92, lng: -99.23, peso: 1.0 }],
      sedes: [{ folio: 1, lugar: 'Cuernavaca', lat: 18.92, lng: -99.23 }]
    };

    service.getMapaCalor().subscribe((res) => {
      expect(res.puntos_calor.length).toBe(1);
      expect(res.sedes.length).toBe(1);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/dashboard/mapa-calor`);
    expect(req.request.method).toBe('GET');
    req.flush(mockMapa);
  });

  it('debe obtener las alertas de deserción', () => {
    const mockAlertas = {
      alertas: [
        {
          agresor_id: 1,
          curp: 'ABCD800101HDFRND01',
          nombre_completo: 'Carlos Hernández',
          faltas_consecutivas: 3
        }
      ]
    };

    service.getAlertas().subscribe((res) => {
      expect(res.alertas.length).toBe(1);
      expect(res.alertas[0].faltas_consecutivas).toBe(3);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/dashboard/alertas`);
    expect(req.request.method).toBe('GET');
    req.flush(mockAlertas);
  });
});
