import { Injectable } from '@angular/core';
import { BaseCrudService } from './base-crud';
import { ProcesoReeducacion, ProcesoReeducacionItem } from '../models/pua.models';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ProcesoReeducacionService extends BaseCrudService<ProcesoReeducacionItem, ProcesoReeducacion> {
  protected override readonly apiUrl = `${environment.apiUrl}/proceso-reeducacion`; 
}
