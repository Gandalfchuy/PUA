import { Injectable} from '@angular/core';
import { SesionItem, Sesion } from '../models/pua.models';
import { BaseCrudService } from './base-crud';

@Injectable({
  providedIn: 'root'
})
export class SesionesService extends BaseCrudService<SesionItem, Sesion>{
  
  protected override readonly apiUrl = 'http://localhost:8000/sesiones'; 


}
