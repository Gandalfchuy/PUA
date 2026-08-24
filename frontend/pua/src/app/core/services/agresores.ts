import { Injectable} from '@angular/core';
import { AgresorItem, Agresor } from '../models/pua.models';
import { BaseCrudService } from './base-crud';

@Injectable({
  providedIn: 'root'
})
export class AgresoresService extends BaseCrudService<AgresorItem, Agresor> {

  protected override readonly apiUrl = 'http://localhost:8000/agresores'; 

  
}