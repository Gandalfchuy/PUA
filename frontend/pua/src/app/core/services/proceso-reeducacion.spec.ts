import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ProcesoReeducacionService } from './proceso-reeducacion';
import { environment } from '../../../environments/environment';

describe('ProcesoReeducacionService', () => {
  let service: ProcesoReeducacionService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        ProcesoReeducacionService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(ProcesoReeducacionService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should create a process via POST', () => {
    const payload = {
      agresor_id: 1,
      fecha_inicio: '2026-01-01',
      denunciante: 'Persona A',
      folio_carpeta_fiscalia: 'EXP-1',
      motivo_ingreso_id: 1,
      tipo_violencia_id: 1,
      modalidad_violencia_id: 1
    };

    service.crear(payload as any).subscribe((res) => {
      expect(res.folio).toBe(10);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/proceso-reeducacion`);
    expect(req.request.method).toBe('POST');
    req.flush({ folio: 10, ...payload });
  });
});
