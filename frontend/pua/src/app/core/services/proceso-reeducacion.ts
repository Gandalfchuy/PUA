import { inject, Injectable } from '@angular/core';
import { BaseCrudService } from './base-crud';
import { ProcesoReeducacion, ProcesoReeducacionItem } from '../models/pua.models';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ProcesoReeducacionService extends BaseCrudService<ProcesoReeducacionItem, ProcesoReeducacion> {
   protected override readonly apiUrl = 'http://localhost:8000/proceso-reeducacion'; 
    private httpClient = inject(HttpClient);

override crear(payload: ProcesoReeducacion, pathAdicional?: string) {
    // Le indicamos a post<> qué tipo de dato va a devolver
    return this.httpClient.post<ProcesoReeducacionItem>(this.apiUrl, payload);
  }

  override actualizar(id: number | string, payload: ProcesoReeducacion, pathAdicional?: string) {
    // Le indicamos a put<> qué tipo de dato va a devolver
    return this.httpClient.put<ProcesoReeducacionItem>(`${this.apiUrl}/${id}`, payload);
  }
}
