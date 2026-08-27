import { Component, inject, OnInit, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { SesionItem, Sesion } from '../../core/models/pua.models';
import { SesionesService } from '../../core/services/sesiones';
import { BaseCrudComponent } from '../../shared/base-crud.component';
import { ModalNotificacion } from '../../shared/components/modal-notificacion/modal-notificacion';
import { PaginacionComponent } from '../../shared/components/paginacion/paginacion';

@Component({
  selector: 'app-sesiones',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, ModalNotificacion, PaginacionComponent],
  templateUrl: './sesiones.html'
})
export class SesionesComponent extends BaseCrudComponent<SesionItem, Sesion> implements OnInit {
  
  private fb = inject(FormBuilder);
  private platformId = inject(PLATFORM_ID);

  servicio = inject(SesionesService);

  formulario = this.fb.group({
    nombre: ['', [Validators.required, Validators.minLength(3)]],
    objetivo: ['', [Validators.required, Validators.minLength(5)]]
  });

  filtrosForm = this.fb.group({
    nombre: ['']
  });

  filtrosActivos: { nombre: string } = { nombre: '' };

  aplicarFiltros() {
    this.filtrosActivos = {
      nombre: this.filtrosForm.value.nombre?.trim() || ''
    };
    this.paginaActual = 1;
  }

  limpiarFiltros() {
    this.filtrosForm.reset({ nombre: '' });
    this.filtrosActivos = { nombre: '' };
    this.paginaActual = 1;
  }

  override get datosFiltrados(): SesionItem[] {
    return this.datosVista.filter(item => {
      const nombreBuscado = this.filtrosActivos.nombre.toLowerCase();
      return !nombreBuscado || (item.nombre && item.nombre.toLowerCase().includes(nombreBuscado));
    });
  }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarDatos();
    }
  }

  mapearPayloadParaGuardar(): Sesion {
    return {
      nombre: (this.formulario.value.nombre || '').trim(),
      objetivo: (this.formulario.value.objetivo || '').trim()
    };
  }

  mapearDatosParaEditar(item: SesionItem): void {
    this.idEdicion = item.folio;
    this.formulario.patchValue({
      nombre: item.nombre,
      objetivo: item.objetivo
    });
  }

  getId(item: SesionItem): number {
    return item.folio;
  }

}