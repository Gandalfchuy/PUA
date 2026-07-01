import { Component, inject, OnInit, ChangeDetectorRef, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Grupo, GrupoItem } from '../../core/models/pua.models';
// NOTA: Asumo que crearás un GruposService similar al CatalogosService
import { GruposService } from '../../core/services/grupos'; 
import { finalize } from 'rxjs/operators';
import { ModalNotificacion } from '../../shared/components/modal-notificacion/modal-notificacion';
import { PaginacionComponent } from '../../shared/components/paginacion/paginacion';

@Component({
  selector: 'app-grupos',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, ModalNotificacion, PaginacionComponent],
  templateUrl: './grupos.html'
})
export class GruposComponent implements OnInit {
  private fb = inject(FormBuilder);
  private gruposService = inject(GruposService);
  private cd = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);

  datosVista: GrupoItem[] = [];
  cargando = false;
  modoEdicion = false;
  idEdicion: number | null = null;
  paginaActual: number = 1;
  elementosPorPagina: number = 10

  // Variables del Modal Compartido
  mostrarModal = false;
  tipoModal: 'exito' | 'error' | 'confirmacion' = 'exito';
  tituloModal = '';
  mensajeModal = '';
  idPendiente: number | null = null;

  // Formulario con validaciones geoespaciales
  grupoForm: FormGroup = this.fb.group({
    lugar: ['', [Validators.required, Validators.minLength(3)]],
    // Longitud (X): Rango de -180 a 180
    longitud: ['', [Validators.required, Validators.min(-180), Validators.max(180)]],
    // Latitud (Y): Rango de -90 a 90
    latitud: ['', [Validators.required, Validators.min(-90), Validators.max(90)]],
  });

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarDatos();
    }
  }

  cargarDatos() {
    this.cargando = true;
    this.grupoForm.disable();
    this.cd.markForCheck();

    this.gruposService.obtenerItems().pipe(
      finalize(() => {
        this.cargando = false;
        this.grupoForm.enable();
        this.cd.markForCheck();
      })
    ).subscribe({
      next: (data) => this.datosVista = data,
      error: (err) => console.error('Error al cargar grupos:', err)
    });
  }

 guardar() {
    // Depuración: Revisamos el estado de cada pieza del formulario
    console.log('Clic detectado. Estado:', this.grupoForm.status);
    console.log('¿Es inválido?', this.grupoForm.invalid);
    console.log('¿Está cargando?', this.cargando);
    console.log('Errores en el campo lugar:', this.grupoForm.get('lugar')?.errors);
    console.log('Errores en el campo latitud:', this.grupoForm.get('latitud')?.errors);
    console.log('Errores en el campo longitud:', this.grupoForm.get('longitud')?.errors);

    if (this.grupoForm.invalid || this.cargando) {
      this.grupoForm.markAllAsTouched();
      return;
    }

    // Armamos el payload con la estructura del objeto (como lo pide FastAPI)
    const payload: Grupo = {
      lugar: this.grupoForm.value.lugar.trim(),
      ubicacion: {
        latitud: Number(this.grupoForm.value.latitud),
        longitud: Number(this.grupoForm.value.longitud)
      }
    };

    this.cargando = true;
    this.grupoForm.disable(); 
    this.cd.markForCheck();

    if (this.modoEdicion && this.idEdicion !== null) {
      this.gruposService.actualizarItem(this.idEdicion, payload)
        .subscribe({
          next: () => {
            this.cargarDatos();
            this.cancelarOperacion();
            this.mostrarMensaje('exito', 'Actualización exitosa', 'El registro ha sido actualizado correctamente.');
          },
          error: (err) => {
            this.cargando = false;
            this.grupoForm.enable();
            this.cd.markForCheck();
            console.error('Error al actualizar:', err);
            this.mostrarMensaje('error', 'Actualización Fallida', 'El registro no ha sido actualizado correctamente.');
          }
        });
    } else {
      this.gruposService.crearItem(payload)
        .subscribe({
          next: () => {
            this.cargarDatos();
            this.cancelarOperacion();
            this.mostrarMensaje('exito', 'Registro exitoso', 'El registro ha sido guardado correctamente.');
          },
          error: (err) => {
            this.cargando = false;
            this.grupoForm.enable();
            this.cd.markForCheck();
            console.error('Error al guardar:', err);
            // Agregué el modal de error aquí para que no se quede solo en consola
            const msj = err.error?.detail || 'Ocurrió un error al guardar el registro.';
            this.mostrarMensaje('error', 'Registro Fallido', msj);
          }
        });
    }
  }

  manejarErrorGuardado(err: any) {
    this.cargando = false;
    this.grupoForm.enable();
    this.cd.markForCheck();
    const msj = err.error?.detail || 'Ocurrió un error al procesar la solicitud.';
    this.mostrarMensaje('error', 'Error en el sistema', msj);
  }

editar(item: GrupoItem) {
    this.modoEdicion = true;

    this.idEdicion=item.folio || null;
    this.grupoForm.patchValue({
      lugar: item.lugar,
      latitud: item.ubicacion.latitud,
      longitud: item.ubicacion.longitud
    });
    
    this.cd.markForCheck();
  }

  eliminar(id: number) {
    this.idPendiente = id;
    this.mostrarMensaje('confirmacion', '¿Eliminar grupo?', '¿Estás seguro de que deseas eliminar permanentemente este grupo y sus coordenadas?');
  }

  ejecutarEliminacion() {
    if (this.idPendiente === null) return;

    this.mostrarModal = false;
    this.cargando = true;
    this.grupoForm.disable();
    this.cd.markForCheck();

    this.gruposService.eliminarItem(this.idPendiente).subscribe({
      next: () => {
        this.idPendiente = null;
        this.cargarDatos();
        this.mostrarMensaje('exito', 'Grupo eliminado', 'El registro se eliminó con éxito.');
      },
      error: (err) => {
        this.idPendiente = null;
        this.manejarErrorGuardado(err);
      }
    });
  }

  cancelarOperacion() {
    this.modoEdicion = false;
    this.idEdicion = null;
    this.grupoForm.reset({ activo: true });
    this.grupoForm.enable();
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

  pegarDesdeGoogleMaps(event: ClipboardEvent) {
    const textoPegado = event.clipboardData?.getData('text') || '';
    
    const regexUrl = /@(-?\d+\.\d+),(-?\d+\.\d+)/;
    const matchUrl = textoPegado.match(regexUrl);

    if (matchUrl) {
      event.preventDefault();
      this.grupoForm.patchValue({
        latitud: Number(matchUrl[1]),
        longitud: Number(matchUrl[2])
      });
      return;
    }
    const regexTexto = /(-?\d+\.\d+)(?:,\s*|\s+)(-?\d+\.\d+)/;
    const matchTexto = textoPegado.match(regexTexto);

    if (matchTexto) {
      event.preventDefault();
      this.grupoForm.patchValue({
        latitud: Number(matchTexto[1]),
        longitud: Number(matchTexto[2])
      });
    }
  }
  obtenerUbicacionActual() {
    if (!navigator.geolocation) {
      this.mostrarMensaje('error', 'No soportado', 'Tu navegador no soporta geolocalización.');
      return;
    }

    this.cargando = true;
    this.cd.markForCheck();

    navigator.geolocation.getCurrentPosition(
      (position) => {
        // Llenamos el formulario automáticamente con alta precisión
        this.grupoForm.patchValue({
          latitud: Number(position.coords.latitude.toFixed(6)),
          longitud: Number(position.coords.longitude.toFixed(6))
        });
        this.cargando = false;
        this.cd.markForCheck();
      },
      (error) => {
        this.cargando = false;
        this.cd.markForCheck();
        this.mostrarMensaje('error', 'Error de GPS', 'Por favor permite el acceso a tu ubicación en el navegador.');
      },
      { enableHighAccuracy: true } // 👈 Obliga a usar el GPS si está en celular
    );
  }

  get datosPaginados() {
    const inicio = (this.paginaActual - 1) * this.elementosPorPagina;
    const fin = inicio + this.elementosPorPagina;
    return this.datosVista.slice(inicio, fin);
  }

  alCambiarPagina(pagina: number) {
    this.paginaActual = pagina;
  }
}