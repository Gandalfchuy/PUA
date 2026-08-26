import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { GruposService } from './grupos';
import { environment } from '../../../environments/environment';

describe('GruposService', () => {
  let service: GruposService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        GruposService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(GruposService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch all grupos via GET', () => {
    const mockData = [{ folio: 1, lugar: 'Sede Centro', ubicacion: { latitud: 18.9, longitud: -99.2 } }];

    service.obtenerTodos().subscribe((res) => {
      expect(res.length).toBe(1);
      expect(res[0].lugar).toBe('Sede Centro');
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/grupos`);
    expect(req.request.method).toBe('GET');
    req.flush(mockData);
  });
});
