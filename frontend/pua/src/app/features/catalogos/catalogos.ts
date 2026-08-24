import { Component, inject, OnInit, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { CatalogosService } from '../../core/services/catalogos';
import { CatalogoItem, Catalogo } from '../../core/models/pua.models';
import { ModalNotificacion } from '../../shared/components/modal-notificacion/modal-notificacion';
import { BaseCrudComponent } from '../../shared/base-crud.component';
// Si ya implementaste la paginación, descomenta la siguiente línea:
// import { PaginacionComponent } from '../../shared/components/paginacion/paginacion';

@Component({
  selector: 'app-catalogos',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, ModalNotificacion /*, PaginacionComponent */],
  templateUrl: './catalogos.html'
})
export class CatalogosComponent extends BaseCrudComponent<CatalogoItem, Catalogo> implements OnInit {

  private fb = inject(FormBuilder);
  private platformId = inject(PLATFORM_ID);

  servicio = inject(CatalogosService);

  formulario = this.fb.group({
    nombre: ['', [Validators.required, Validators.minLength(3)]],
  });

  listaCatalogos = [
    { id: 'adicciones', nombre: 'Adicciones' },
    { id: 'actividad-recreativa', nombre: 'Actividad Recreativa' },
    { id: 'estado-civil', nombre: 'Estado Civil' },
    { id: 'genero-musical', nombre: 'Género Musical' },
    { id: 'modalidad-violencia', nombre: 'Modalidad de Violencia' },
    { id: 'situacion-academica', nombre: 'Situación Académica' },
    { id: 'motivo-ingreso', nombre: 'Motivo de Ingreso' },
    { id: 'situacion-laboral', nombre: 'Situación Laboral' },
    { id: 'rango-salarial', nombre: 'Rango Salarial' },
    { id: 'relacion-hijos', nombre: 'Relación con Hijos' },
    { id: 'religion', nombre: 'Religión' },
    { id: 'sectores-sociales', nombre: 'Sectores Sociales' },
    { id: 'situacion-vivienda', nombre: 'Situación de Vivienda' },
    { id: 'tipo-relacion', nombre: 'Tipo de Relación' },
    { id: 'tipo-violencia', nombre: 'Tipo de Violencia' },
  ];

  ngOnInit() {
    this.recursoDinamico = 'adicciones';

    if (isPlatformBrowser(this.platformId)) {
      this.cargarDatos();
    }
  }

  cambiarCatalogo(event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    this.recursoDinamico = selectElement.value;
    this.cancelarOperacion();
    this.cargarDatos();
  }

  mapearPayloadParaGuardar(): Catalogo {
    return {
      nombre: this.formulario.value.nombre!.trim(),
    };
  }

  mapearDatosParaEditar(item: CatalogoItem): void {
    this.idEdicion = item.id || null;
    this.formulario.patchValue({ nombre: item.nombre });
  }

  getId(item: CatalogoItem): number {
    return item.id!;
  }

}