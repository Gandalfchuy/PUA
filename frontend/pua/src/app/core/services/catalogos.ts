import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common'; // 👈 1. Importamos la herramienta de validación
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CatalogoItem, Catalogo } from '../models/pua.models';

@Injectable({
  providedIn: 'root'
})
export class CatalogosService {
  private http = inject(HttpClient);
  private platformId = inject(PLATFORM_ID); // 👈 2. Inyectamos el ID de la plataforma
  
  private apiUrl = 'http://localhost:8000/catalogos'; 

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

  obtenerItems(tipo: string): Observable<CatalogoItem[]> {
    return this.http.get<CatalogoItem[]>(`${this.apiUrl}/${tipo}`, { headers: this.getHeaders() });
  }

  crearItem(tipo: string, payload: Catalogo): Observable<CatalogoItem> {
    return this.http.post<CatalogoItem>(`${this.apiUrl}/${tipo}`, payload, { headers: this.getHeaders() });
  }

  actualizarItem(tipo: string, id: number, payload: Catalogo): Observable<CatalogoItem> {
    return this.http.put<CatalogoItem>(`${this.apiUrl}/${tipo}/${id}`, payload, { headers: this.getHeaders() });
  }

  eliminarItem(tipo: string, id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${tipo}/${id}`, { headers: this.getHeaders() });
  }
}