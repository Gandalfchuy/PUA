import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { AuthService } from './auth';
import { environment } from '../../../environments/environment';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        AuthService,
        provideHttpClient(),
        provideHttpClientTesting()
      ]
    });
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
    localStorage.clear();
  });

  afterEach(() => {
    httpMock.verify();
    localStorage.clear();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should send login request and save token to localStorage on success', () => {
    const mockResponse = { access_token: 'fake-jwt-token-123', token_type: 'bearer' };

    service.login('admin@pua.gob.mx', 'Password123').subscribe((res) => {
      expect(res.access_token).toBe('fake-jwt-token-123');
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/login`);
    expect(req.request.method).toBe('POST');
    expect(req.request.headers.get('Content-Type')).toBe('application/x-www-form-urlencoded');

    req.flush(mockResponse);

    expect(localStorage.getItem('pua_token')).toBe('fake-jwt-token-123');
    expect(service.estaLogueado()).toBe(true);
  });

  it('should remove token on cerrarSesion', () => {
    localStorage.setItem('pua_token', 'token-activo');
    expect(service.estaLogueado()).toBe(true);

    service.cerrarSesion();
    expect(localStorage.getItem('pua_token')).toBeNull();
    expect(service.estaLogueado()).toBe(false);
  });
});
