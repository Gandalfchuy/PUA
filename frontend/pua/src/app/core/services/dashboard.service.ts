import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  DashboardKpis,
  DashboardMapa,
  DashboardViolencia,
  DashboardAdicciones,
  DashboardAlertas
} from '../models/dashboard.models';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiUrl}/dashboard`;

  getKpis(): Observable<DashboardKpis> {
    return this.http.get<DashboardKpis>(`${this.baseUrl}/kpis`);
  }

  getMapaCalor(): Observable<DashboardMapa> {
    return this.http.get<DashboardMapa>(`${this.baseUrl}/mapa-calor`);
  }

  getTiposViolencia(): Observable<DashboardViolencia> {
    return this.http.get<DashboardViolencia>(`${this.baseUrl}/tipos-violencia`);
  }

  getAdicciones(): Observable<DashboardAdicciones> {
    return this.http.get<DashboardAdicciones>(`${this.baseUrl}/adicciones`);
  }

  getAlertas(): Observable<DashboardAlertas> {
    return this.http.get<DashboardAlertas>(`${this.baseUrl}/alertas`);
  }
}
