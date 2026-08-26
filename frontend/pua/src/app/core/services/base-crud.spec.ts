import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { Injectable } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { BaseCrudService } from './base-crud';

interface TestItem {
  id: number;
  nombre: string;
}

interface TestPayload {
  nombre: string;
}

@Injectable({ providedIn: 'root' })
class TestCrudService extends BaseCrudService<TestItem, TestPayload> {
  protected override readonly apiUrl = 'http://localhost:8000/test-items';
}

describe('BaseCrudService', () => {
  let service: TestCrudService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        TestCrudService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(TestCrudService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should get all items', () => {
    const mockItems: TestItem[] = [{ id: 1, nombre: 'Item 1' }];

    service.obtenerTodos().subscribe((items) => {
      expect(items.length).toBe(1);
      expect(items[0].nombre).toBe('Item 1');
    });

    const req = httpMock.expectOne('http://localhost:8000/test-items');
    expect(req.request.method).toBe('GET');
    req.flush(mockItems);
  });

  it('should get item by id', () => {
    const mockItem: TestItem = { id: 1, nombre: 'Item 1' };

    service.obtenerPorId(1).subscribe((item) => {
      expect(item.id).toBe(1);
    });

    const req = httpMock.expectOne('http://localhost:8000/test-items/1');
    expect(req.request.method).toBe('GET');
    req.flush(mockItem);
  });

  it('should create item', () => {
    const payload: TestPayload = { nombre: 'Nuevo Item' };
    const mockCreated: TestItem = { id: 2, nombre: 'Nuevo Item' };

    service.crear(payload).subscribe((item) => {
      expect(item.id).toBe(2);
    });

    const req = httpMock.expectOne('http://localhost:8000/test-items');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(payload);
    req.flush(mockCreated);
  });

  it('should update item', () => {
    const payload: TestPayload = { nombre: 'Item Actualizado' };
    const mockUpdated: TestItem = { id: 1, nombre: 'Item Actualizado' };

    service.actualizar(1, payload).subscribe((item) => {
      expect(item.nombre).toBe('Item Actualizado');
    });

    const req = httpMock.expectOne('http://localhost:8000/test-items/1');
    expect(req.request.method).toBe('PUT');
    req.flush(mockUpdated);
  });

  it('should delete item', () => {
    service.eliminar(1).subscribe();

    const req = httpMock.expectOne('http://localhost:8000/test-items/1');
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
