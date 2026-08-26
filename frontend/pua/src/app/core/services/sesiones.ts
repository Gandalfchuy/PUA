import { Injectable } from '@angular/core';
import { SesionItem, Sesion } from '../models/pua.models';
import { BaseCrudService } from './base-crud';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SesionesService extends BaseCrudService<SesionItem, Sesion> {
  protected override readonly apiUrl = `${environment.apiUrl}/sesiones`; 
}
