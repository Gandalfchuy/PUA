import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { AgresoresService } from './agresores';
import { environment } from '../../../environments/environment';

describe('AgresoresService', () => {
  let service: AgresoresService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        AgresoresService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(AgresoresService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch all agresores via GET', () => {
    const mockData = [{ folio: 1, curp: 'ABCD123456HDFRND01', nombre: 'Juan' }];

    service.obtenerTodos().subscribe((res) => {
      expect(res.length).toBe(1);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/agresores`);
    expect(req.request.method).toBe('GET');
    req.flush(mockData);
  });
});
