import { Injectable } from '@angular/core';
import { BaseCrudService } from './base-crud';
import { Lista, ListaItem } from '../models/pua.models';

@Injectable({
  providedIn: 'root',
})
export class ListasService extends BaseCrudService<ListaItem, Lista> {
    protected override readonly apiUrl = 'http://localhost:8000/lista'; 
}
