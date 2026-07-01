import { Component, inject, OnInit, ChangeDetectorRef,PLATFORM_ID } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { isPlatformBrowser } from '@angular/common';
import { CommonModule } from '@angular/common';
import { CatalogosService } from '../../core/services/catalogos';
import { finalize } from 'rxjs/operators';
import { CatalogoItem, Catalogo } from '../../core/models/pua.models';
import { ModalComponent } from '../../shared/components/modal/modal';
import { ModalNotificacion } from '../../shared/components/modal-notificacion/modal-notificacion';

@Component({
  selector: 'app-catalogos',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule,ModalNotificacion],
  templateUrl: './catalogos.html'
})
export class CatalogosComponent implements OnInit {
  private fb = inject(FormBuilder);
  private catalogosService = inject(CatalogosService);
  private cd = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);
  private modal = new(ModalNotificacion);

  mostrarModal = false;
  tipoModal: 'exito' | 'error' | 'confirmacion' = 'exito';
  tituloModal = '';
  mensajeModal = '';
  idPendiente: number | null = null;

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

  catalogoActual = 'adicciones';
  datosVista: CatalogoItem[] = [];
  cargando = false;
  modoEdicion = false;
  idEdicion: number | null = null;

  catalogoForm: FormGroup = this.fb.group({
    nombre: ['', [Validators.required, Validators.minLength(3)]],
  });

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarDatos();
    }
  }

  cambiarCatalogo(event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    this.catalogoActual = selectElement.value;
    this.cancelarOperacion();
    this.cargarDatos();
  }

cargarDatos() {
    this.cargando = true;
    this.catalogoForm.disable();
    this.cd.markForCheck();

    this.catalogosService.obtenerItems(this.catalogoActual)
      .pipe(
        finalize(() => {
          this.cargando = false;
          this.catalogoForm.enable();
          this.cd.markForCheck();
        })
      )
      .subscribe({
        next: (data: CatalogoItem[]) => {
          this.datosVista = data;
        },
        error: (err) => {
          console.error('Error al recuperar el catálogo:', err);
        }
      });
  }

  guardar() {

    console.log('Clic detectado. Estado:', this.catalogoForm.status);
    console.log('¿Es inválido?', this.catalogoForm.invalid);
    console.log('¿Está cargando?', this.cargando);
    console.log('Errores en el campo nombre:', this.catalogoForm.get('nombre')?.errors);
    if (this.catalogoForm.invalid || this.cargando) {
      this.catalogoForm.markAllAsTouched();
      return;
    }

    const payload: Catalogo = {
      nombre: this.catalogoForm.value.nombre.trim(),
    };

    this.cargando = true;
    this.catalogoForm.disable(); 
    this.cd.markForCheck();

    if (this.modoEdicion && this.idEdicion !== null) {
      this.catalogosService.actualizarItem(this.catalogoActual, this.idEdicion, payload)
        .subscribe({
          next: () => {
            this.cargarDatos();
            this.cancelarOperacion();
            this.mostrarMensaje('exito', 'Actualización exitosa', 'El registro ha sido actualizado correctamente.');
          },
          error: (err) => {
            this.cargando = false;
            this.catalogoForm.enable();
            this.cd.markForCheck();
            console.error('Error al actualizar:', err);
            this.mostrarMensaje('error', 'Actualización Fallida', 'El registro no ha sido actualizado correctamente.');
          }
        });
    } else {
      this.catalogosService.crearItem(this.catalogoActual, payload)
        .subscribe({
          next: () => {
            this.cargarDatos();
            this.cancelarOperacion();
            this.mostrarMensaje('exito', 'Actualización exitosa', 'El registro ha sido guardado correctamente.');
          },
          error: (err) => {
            this.cargando = false;
            this.catalogoForm.enable();
            this.cd.markForCheck();
            console.error('Error al guardar:', err);
          }
        });
    }
  }

  editar(item: CatalogoItem) {
    this.modoEdicion = true;
    this.idEdicion = item.id;
    this.catalogoForm.patchValue({ nombre: item.nombre });
    this.cd.markForCheck();
  }

  eliminar(id: number) {
    this.idPendiente = id;
    this.mostrarMensaje('confirmacion', '¿Eliminar registro?', 'Esta acción no se puede deshacer. ¿Estás seguro de que deseas eliminar este elemento de la base de datos?');
  }

  ejecutarEliminacion() {
    if (this.idPendiente === null) return;

    this.mostrarModal = false;
    this.cargando = true;
    this.catalogoForm.disable(); 
    this.cd.markForCheck();

    this.catalogosService.eliminarItem(this.catalogoActual, this.idPendiente)
      .subscribe({
        next: () => {
          this.idPendiente = null;
          this.cargarDatos();
          // Mostramos el modal de éxito
          this.mostrarMensaje('exito', 'Registro eliminado', 'El catálogo se ha actualizado correctamente.');
        },
        error: (err) => {
          this.idPendiente = null;
          this.cargando = false;
          this.catalogoForm.enable();
          this.cd.markForCheck();
          const msj = err.error?.detail || 'Ocurrió un error al eliminar.';
          this.mostrarMensaje('error', 'Error', msj);
        }
      });
  }



  cancelarOperacion() {
    this.modoEdicion = false;
    this.idEdicion = null;
    this.catalogoForm.reset();
    this.catalogoForm.enable(); 
    this.cd.markForCheck();
  }

  mostrarMensaje(tipo: 'exito' | 'error' | 'confirmacion', titulo: string, mensaje: string) {
    this.tipoModal = tipo;
    this.tituloModal = titulo;
    this.mensajeModal = mensaje;
    this.mostrarModal = true;
    this.cd.markForCheck();
  }

 cerrarModal() {
    this.mostrarModal = false;
    this.idPendiente = null; 
    this.cd.markForCheck();
  }
}