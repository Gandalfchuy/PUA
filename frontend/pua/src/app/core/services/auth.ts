import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private platformId = inject(PLATFORM_ID);
  
  private apiUrl = environment.apiUrl; 

  login(correo: string, contrasena: string): Observable<any> {
    const body = new HttpParams()
      .set('username', correo)
      .set('password', contrasena);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    return this.http.post(`${this.apiUrl}/login`, body.toString(), { headers }).pipe(
      tap((respuesta: any) => {
        if (respuesta && respuesta.access_token && isPlatformBrowser(this.platformId)) {
          localStorage.setItem('pua_token', respuesta.access_token);
        }
      })
    );
  }

  estaLogueado(): boolean {
    if (isPlatformBrowser(this.platformId)) {
      return !!localStorage.getItem('pua_token');
    }
    return false;
  }

  cerrarSesion(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('pua_token');
    }
  }
}
