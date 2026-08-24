import { Component, inject, OnInit, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Grupo, GrupoItem } from '../../core/models/pua.models';
import { GruposService } from '../../core/services/grupos';
import { ModalNotificacion } from '../../shared/components/modal-notificacion/modal-notificacion';
import { PaginacionComponent } from '../../shared/components/paginacion/paginacion';
import { BaseCrudComponent } from '../../shared/base-crud.component';

@Component({
  selector: 'app-grupos',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, ModalNotificacion, PaginacionComponent],
  templateUrl: './grupos.html'
})
export class GruposComponent extends BaseCrudComponent<GrupoItem, Grupo> implements OnInit {

  private fb = inject(FormBuilder);
  private platformId = inject(PLATFORM_ID);
  servicio = inject(GruposService);

  formulario: FormGroup = this.fb.group({
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

  mapearPayloadParaGuardar(): Grupo {
    return {
      lugar: this.formulario.value.lugar.trim(),
      ubicacion: {
        latitud: Number(this.formulario.value.latitud),
        longitud: Number(this.formulario.value.longitud)
      }
    };
  }

  mapearDatosParaEditar(item: GrupoItem): void {
    this.idEdicion = item.folio || null;
    this.formulario.patchValue({
      lugar: item.lugar,
      latitud: item.ubicacion.latitud,
      longitud: item.ubicacion.longitud
    });
  }

  getId(item: GrupoItem): number {
    return item.folio;
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
        this.formulario.patchValue({
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
      { enableHighAccuracy: true }
    );
  }
   pegarDesdeGoogleMaps(event: ClipboardEvent) {
    const textoPegado = event.clipboardData?.getData('text') || '';

    const regexUrl = /@(-?\d+\.\d+),(-?\d+\.\d+)/;
    const matchUrl = textoPegado.match(regexUrl);

    if (matchUrl) {
      event.preventDefault();
      this.formulario.patchValue({
        latitud: Number(matchUrl[1]),
        longitud: Number(matchUrl[2])
      });
      return;
    }
    const regexTexto = /(-?\d+\.\d+)(?:,\s*|\s+)(-?\d+\.\d+)/;
    const matchTexto = textoPegado.match(regexTexto);

    if (matchTexto) {
      event.preventDefault();
      this.formulario.patchValue({
        latitud: Number(matchTexto[1]),
        longitud: Number(matchTexto[2])
      });
    }
  }
}

