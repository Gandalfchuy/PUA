import { Injectable } from '@angular/core';
import { CatalogoItem, Catalogo } from '../models/pua.models';
import { BaseCrudService } from './base-crud';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CatalogosService extends BaseCrudService<CatalogoItem, Catalogo> {
  protected override readonly apiUrl = `${environment.apiUrl}/catalogos`; 
}