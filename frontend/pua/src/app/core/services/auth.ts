import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  
  // Ajusta este puerto al que usa tu servidor de FastAPI
  private apiUrl = 'http://localhost:8000'; 

  login(correo: string, contrasena: string): Observable<any> {
    // 1. Transformamos los datos al formato que exige FastAPI (x-www-form-urlencoded)
    const body = new HttpParams()
      .set('username', correo) // FastAPI exige la llave 'username'
      .set('password', contrasena);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded'
    });

    // 2. Hacemos el POST a tu endpoint real
    return this.http.post(`${this.apiUrl}/login`, body.toString(), { headers }).pipe(
      tap((respuesta: any) => {
        // 3. Interceptamos la respuesta exitosa para guardar el Token JWT
        if (respuesta && respuesta.access_token) {
          localStorage.setItem('pua_token', respuesta.access_token);
          console.log('Token guardado exitosamente');
        }
      })
    );
  }

  // Método auxiliar para saber si hay sesión activa
  estaLogueado(): boolean {
    return !!localStorage.getItem('pua_token');
  }

  cerrarSesion(): void {
    localStorage.removeItem('pua_token');
  }
}
