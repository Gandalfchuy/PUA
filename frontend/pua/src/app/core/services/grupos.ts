import { Injectable } from '@angular/core';
import { GrupoItem, Grupo } from '../models/pua.models';
import { BaseCrudService } from './base-crud';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class GruposService extends BaseCrudService<GrupoItem, Grupo> {
  protected override readonly apiUrl = `${environment.apiUrl}/grupos`; 
}