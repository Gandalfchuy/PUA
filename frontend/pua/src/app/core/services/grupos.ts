import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common'; // 👈 1. Importamos la herramienta de validación
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { GrupoItem, Grupo } from '../models/pua.models';

@Injectable({
  providedIn: 'root'
})
export class GruposService {
  private http = inject(HttpClient);
  private platformId = inject(PLATFORM_ID); // 👈 2. Inyectamos el ID de la plataforma
  
  private apiUrl = 'http://localhost:8000/grupos'; 

  private getHeaders(): HttpHeaders {
    let token = '';
    
    // 3. 🛡️ Escudo Anti-SSR: Solo leemos localStorage si estamos en el navegador
    if (isPlatformBrowser(this.platformId)) {
      token = localStorage.getItem('pua_token') || '';
    }

    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
  }

  obtenerItems(): Observable<GrupoItem[]> {
    return this.http.get<GrupoItem[]>(`${this.apiUrl}`, { headers: this.getHeaders() });
  }

  crearItem(payload: Grupo): Observable<GrupoItem> {
    return this.http.post<GrupoItem>(`${this.apiUrl}/`, payload, { headers: this.getHeaders() });
  }

  actualizarItem(folio: number, payload: Grupo): Observable<GrupoItem> {
    return this.http.put<GrupoItem>(`${this.apiUrl}/${folio}`, payload, { headers: this.getHeaders() });
  }

  eliminarItem(folio: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${folio}`, { headers: this.getHeaders() });
  }
}