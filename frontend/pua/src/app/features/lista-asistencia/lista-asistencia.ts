import { Component, inject, OnInit, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormBuilder, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';

import { ListaItem, Lista } from '../../core/models/pua.models'; 

import { BaseCrudComponent } from '../../shared/base-crud.component';
import { ModalNotificacion } from '../../shared/components/modal-notificacion/modal-notificacion';
import { PaginacionComponent } from '../../shared/components/paginacion/paginacion';
import { ListasService } from '../../core/services/listas';
import { AgresoresService } from '../../core/services/agresores';
import { SesionesService } from '../../core/services/sesiones';
import { GruposService } from '../../core/services/grupos';

@Component({
  selector: 'app-listas',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, ModalNotificacion, PaginacionComponent, FormsModule],
  templateUrl: './lista-asistencia.html'
})
export class ListasComponent extends BaseCrudComponent<ListaItem, Lista> implements OnInit {
  
  private fb = inject(FormBuilder);
  private platformId = inject(PLATFORM_ID);

  servicio = inject(ListasService);
  filtrosActivos: any = { curp: '', tema: '', grupo: '', fecha: '' };
  
  private agresorService = inject(AgresoresService);
  private sesionService = inject(SesionesService);
  private grupoService = inject(GruposService);

  agresores: any[] = [];
  temas: any[] = [];
  grupos: any[] = [];

  dropdownAbierto = false;
  textoBusqueda = '';

  formulario = this.fb.group({
    agresor_id: ['', Validators.required],
    sesion_id: ['', Validators.required],
    grupo_id: ['', Validators.required],
    fecha: ['', Validators.required]
  });

  filtrosForm = this.fb.group({
    curp: [''],
    tema: [''],
    grupo: [''],
    fecha: ['']
  });

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarCatalogos();
      this.cargarDatos(); 
    }
  }

  cargarCatalogos() {
    this.agresorService.obtenerTodos().subscribe(res => this.agresores = res);
    this.sesionService.obtenerTodos().subscribe(res => this.temas = res);
    this.grupoService.obtenerTodos().subscribe(res => this.grupos = res);
  }


   override mapearPayloadParaGuardar(): Lista {
     const val = this.formulario.getRawValue();
     return{
      agresor_id:Number(val.agresor_id),
      grupo_id:Number(val.grupo_id),
      sesion_id:Number(val.sesion_id),
      fecha: val.fecha?val.fecha:null
     };
   }

  mapearDatosParaEditar(item: ListaItem): void {
    this.idEdicion = item.id; 
    
    this.formulario.patchValue({
      agresor_id: item.agresor?.folio.toString(),
      grupo_id: item.grupo?.folio.toString(),
      sesion_id: item.sesion?.folio.toString(),
      fecha: item.fecha
    });
  }

  getId(item: ListaItem): number {
    return item.id; 
  }

  get agresoresFiltrados() {
    const termino = this.textoBusqueda.toLowerCase();
    return this.agresores.filter(a => 
      a.curp.toLowerCase().includes(termino) || 
      (a.nombre && a.nombre.toLowerCase().includes(termino))
    );
  }

 aplicarFiltros() {
    this.filtrosActivos = this.filtrosForm.value;
    this.paginaActual = 1;
  }

  // 3. Limpiar filtros ahora resetea ambos estados
  limpiarFiltros() {
    this.filtrosForm.reset({ curp: '', tema: '', grupo: '', fecha: '' });
    this.filtrosActivos = { curp: '', tema: '', grupo: '', fecha: '' };
    this.paginaActual = 1; 
  }

  // 4. Sobrescribimos el comportamiento del BaseCrudComponent
  override get datosFiltrados(): ListaItem[] {
    return this.datosVista.filter(item => {
      const form = this.filtrosActivos;

      // Comparamos los valores seleccionados con las propiedades anidadas de tu ListaItem
      const coincideCurp = !form.curp || item.agresor?.folio?.toString() === form.curp?.toString();
      const coincideTema = !form.tema || item.sesion?.folio?.toString() === form.tema?.toString();
      const coincideGrupo = !form.grupo || item.grupo?.folio?.toString() === form.grupo?.toString();
      const coincideFecha = !form.fecha || item.fecha === form.fecha;

      return coincideCurp && coincideTema && coincideGrupo && coincideFecha;
    });
  }

  seleccionarAgresor(agresor: any) {
    this.formulario.patchValue({ agresor_id: agresor.folio }); 
    this.textoBusqueda = agresor.curp; 
    this.dropdownAbierto = false; 
  }
}