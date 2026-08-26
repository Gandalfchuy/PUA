import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { CatalogosService } from './catalogos';
import { environment } from '../../../environments/environment';

describe('CatalogosService', () => {
  let service: CatalogosService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        CatalogosService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(CatalogosService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch catalog items via GET', () => {
    const mockData = [{ id: 1, nombre: 'Alcoholismo', activo: true, created_at: '2026-01-01' }];

    service.obtenerTodos('adicciones').subscribe((res) => {
      expect(res.length).toBe(1);
      expect(res[0].nombre).toBe('Alcoholismo');
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/catalogos/adicciones`);
    expect(req.request.method).toBe('GET');
    req.flush(mockData);
  });

  it('should create catalog item via POST', () => {
    const payload = { nombre: 'Tabaco' };
    const mockResponse = { id: 2, nombre: 'Tabaco', activo: true, created_at: '2026-01-01' };

    service.crear(payload, 'adicciones').subscribe((res) => {
      expect(res.id).toBe(2);
      expect(res.nombre).toBe('Tabaco');
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/catalogos/adicciones`);
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });
});
