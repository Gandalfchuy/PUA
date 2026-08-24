import { Injectable} from '@angular/core';
import { CatalogoItem, Catalogo } from '../models/pua.models';
import { BaseCrudService } from './base-crud';

@Injectable({
  providedIn: 'root'
})
export class CatalogosService extends BaseCrudService<CatalogoItem, Catalogo> {

  protected override readonly apiUrl = 'http://localhost:8000/catalogos'; 

  
}