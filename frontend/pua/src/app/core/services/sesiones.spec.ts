import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { SesionesService } from './sesiones';
import { environment } from '../../../environments/environment';

describe('SesionesService', () => {
  let service: SesionesService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        SesionesService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(SesionesService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch all sesiones via GET', () => {
    const mockData = [{ folio: 1, nombre: 'Sesión 1', objetivo: 'Objetivo 1' }];

    service.obtenerTodos().subscribe((res) => {
      expect(res.length).toBe(1);
      expect(res[0].nombre).toBe('Sesión 1');
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/sesiones`);
    expect(req.request.method).toBe('GET');
    req.flush(mockData);
  });
});
