import { Injectable } from '@angular/core';
import { BaseCrudService } from './base-crud';
import { Lista, ListaItem } from '../models/pua.models';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ListasService extends BaseCrudService<ListaItem, Lista> {
  protected override readonly apiUrl = `${environment.apiUrl}/lista`; 
}
