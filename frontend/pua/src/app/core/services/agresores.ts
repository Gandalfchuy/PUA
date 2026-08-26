import { Injectable } from '@angular/core';
import { AgresorItem, Agresor } from '../models/pua.models';
import { BaseCrudService } from './base-crud';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AgresoresService extends BaseCrudService<AgresorItem, Agresor> {
  protected override readonly apiUrl = `${environment.apiUrl}/agresores`; 
}