import { Component, EventEmitter, inject, Input, OnInit, Output, OnChanges, SimpleChanges } from '@angular/core';
import { BaseCrudComponent } from '../../shared/base-crud.component';
import { ProcesoReeducacion, ProcesoReeducacionItem } from '../../core/models/pua.models';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ProcesoReeducacionService } from '../../core/services/proceso-reeducacion';
import { CatalogosService } from '../../core/services/catalogos';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-procesos-modal',
  standalone:true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './proceso-reeducacion.html'
})
export class ProcesoReeducacionComponent extends BaseCrudComponent<ProcesoReeducacionItem, ProcesoReeducacion> implements OnInit {
  
ngOnInit(): void {

    this.cargarCatalogos();

    this.formulario.get('fecha_inicio')?.valueChanges.subscribe(nuevaFechaInicio => {
      const controlTermino = this.formulario.get('fecha_termino');
      const fechaTerminoActual = controlTermino?.value;
      if (fechaTerminoActual && nuevaFechaInicio > fechaTerminoActual) {
        controlTermino?.setValue(''); 
      }
    });
  }


 @Input() agresorId!: number;

  cargarProceso(proceso: any): void {
    console.log("🔥 DATA INYECTADA A LA FUERZA:", proceso);

    if (proceso) {
      this.modoEdicion = true;
      this.idEdicion = proceso.folio; // Asegúrate de que sea tu ID real (id o folio)
      
      setTimeout(() => {
        this.mapearDatosParaEditar(proceso);
      });
    } else {
      this.modoEdicion = false;
      this.idEdicion = null;
      if (this.formulario) {
        this.formulario.reset();
        this.formulario.patchValue({
          motivo_ingreso_id: null, tipo_violencia_id: null, modalidad_violencia_id: null
        });
      }
    }
  }
  @Output() cerrado = new EventEmitter<void>();
  @Output() guardado = new EventEmitter<any>();
  
  private fb = inject(FormBuilder);
  private catalogosService = inject(CatalogosService)
  servicio = inject(ProcesoReeducacionService);
  formulario: FormGroup = this.fb.group({
      fecha_inicio: ['', Validators.required],
      fecha_termino: [''],
      fecha_denuncia: [''],
      denunciante: [''],
      folio_carpeta_fiscalia: [''],
      motivo_ingreso_id: [null, Validators.required],
      tipo_violencia_id: [null, Validators.required],
      modalidad_violencia_id: [null, Validators.required]
  });
  
  catalogos: any = { motivos: [], tipos: [], modalidades: [] };
  cargandoCatalogos = true;

  override mapearPayloadParaGuardar(): ProcesoReeducacion {
    const val = this.formulario.getRawValue();
    return{
      fecha_inicio: val.fecha_inicio,
      fecha_termino: val.fecha_termino ? val.fecha_termino : null,
      fecha_denuncia: val.fecha_denuncia ? val.fecha_denuncia : null,
      denunciante: val.denunciante || '',
      folio_carpeta_fiscalia: val.folio_carpeta_fiscalia || '',
      agresor_id: Number(this.agresorId),
      motivo_ingreso_id: Number(val.motivo_ingreso_id),
      tipo_violencia_id: Number(val.tipo_violencia_id),
      modalidad_violencia_id: Number(val.modalidad_violencia_id)
    };
  }

  override mapearDatosParaEditar(item:ProcesoReeducacionItem):void{
    this.idEdicion = item.folio;
    this.formulario.patchValue({
      fecha_inicio: item.fecha_inicio,
      fecha_termino: item.fecha_termino ? item.fecha_termino : null,
      fecha_denuncia: item.fecha_denuncia ? item.fecha_denuncia : null,
      denunciante: item.denunciante || '',
      folio_carpeta_fiscalia: item.folio_carpeta_fiscalia || '',
      agresor_id: Number(this.agresorId),
      motivo_ingreso_id: item.motivo_ingreso?.id || item.motivo_ingreso.id || null,
      tipo_violencia_id: item.tipo_violencia?.id || item.tipo_violencia.id || null,
      modalidad_violencia_id: item.modalidad_violencia?.id || item.modalidad_violencia.id || null
    });
  }

  cargarCatalogos() {
      forkJoin({
        motivos: this.catalogosService.obtenerTodos('motivo-ingreso'),
        tipos: this.catalogosService.obtenerTodos('tipo-violencia'),
       modalidades: this.catalogosService.obtenerTodos('modalidad-violencia')
      }).subscribe(resultados => {
        this.catalogos = resultados;
        this.cd.markForCheck();
      });
    }
    override cargarDatos(): void {
    // Shhh... no hacemos nada. 
    // El componente padre (Agresores) ya se encarga de actualizar la tabla visualmente.
  }

    get fechaInicioSeleccionada(): string {
    return this.formulario.get('fecha_inicio')?.value || '';
  }

   override getId(item: ProcesoReeducacionItem): number {
      return item.folio;
    }

   override guardar(): void {
    // 1. Validamos que el formulario esté lleno y correcto
    if (this.formulario.invalid) {
      this.formulario.markAllAsTouched();
      return;
    }

    // 2. Activamos el estado de carga (por si tienes un spinner)
    this.cargando = true;

    // 3. Preparamos el JSON limpio para FastAPI
    const payload = this.mapearPayloadParaGuardar();
    
    // 4. Decidimos si es PUT (Editar) o POST (Crear)
    const peticion$ = this.modoEdicion 
      ? this.servicio.actualizar(this.idEdicion!, payload) 
      : this.servicio.crear(payload);
    
    // 5. Disparamos la petición HTTP
    peticion$.subscribe({
      next: (procesoBD) => {
        this.cargando = false;
        
        // 🚀 6. EL AVISO AL PADRE: Le mandamos el dato y la acción
        this.guardado.emit({ 
          proceso: procesoBD, 
          modo: this.modoEdicion ? 'editar' : 'crear' 
        });
        
        // 🚀 7. EL CIERRE: Le decimos al HTML del padre que oculte este componente
        this.cerrado.emit();
      },
      error: (err) => {
        this.cargando = false;
        console.error(" Error al guardar el proceso:", err);
      }
    });
  }

}
