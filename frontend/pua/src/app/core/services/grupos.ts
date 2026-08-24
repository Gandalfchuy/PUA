import { Injectable} from '@angular/core';
import { GrupoItem, Grupo } from '../models/pua.models';
import { BaseCrudService } from './base-crud';

@Injectable({
  providedIn: 'root'
})
export class GruposService extends BaseCrudService<GrupoItem, Grupo>{
  
  protected override readonly apiUrl = 'http://localhost:8000/grupos'; 


}