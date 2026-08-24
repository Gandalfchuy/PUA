import { inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common'; // 👈 1. Importamos la herramienta de validación
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export abstract class BaseCrudService<TItem, T> {

  protected http = inject(HttpClient);
  private buildUrl(pathAdicional?: string, id?: number): string {
    let url = pathAdicional ? `${this.apiUrl}/${pathAdicional}` : this.apiUrl;
    if (id) url = `${url}/${id}`;
    return url;
  }


  protected abstract readonly apiUrl: string;

  obtenerTodos(pathAdicional:string=''): Observable<TItem[]> {
    return this.http.get<TItem[]>(this.buildUrl(pathAdicional));
  }

  obtenerPorId(id: number,pathAdicional:string=''): Observable<TItem> {
    return this.http.get<TItem>(this.buildUrl(pathAdicional, id));
  }

  crear(payload: T, pathAdicional:string='' ): Observable<TItem> {
    return this.http.post<TItem>(this.buildUrl(pathAdicional), payload);
  }

  actualizar(id: number, payload: T, pathAdicional:string=''): Observable<TItem> {
    return this.http.put<TItem>(this.buildUrl(pathAdicional, id), payload);
  }

  eliminar(id: number,pathAdicional:string=''): Observable<void> {
    return this.http.delete<void>(this.buildUrl(pathAdicional, id));
  }
}
