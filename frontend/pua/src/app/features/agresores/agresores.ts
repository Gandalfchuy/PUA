import { Component, inject, OnInit, PLATFORM_ID, ViewChild } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { forkJoin } from 'rxjs'; // 👈 Para llamadas en paralelo
import { AgresorItem, Agresor, ProcesoReeducacionItem } from '../../core/models/pua.models';
import { AgresoresService } from '../../core/services/agresores';
import { CatalogosService } from '../../core/services/catalogos';
import { BaseCrudComponent } from '../../shared/base-crud.component';
import { ModalNotificacion } from '../../shared/components/modal-notificacion/modal-notificacion';
import { PaginacionComponent } from '../../shared/components/paginacion/paginacion';
import { HttpClient } from '@angular/common/http';
import { ProcesoReeducacionComponent } from '../proceso-reeducacion/proceso-reeducacion';


@Component({
  selector: 'app-agresores',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, ModalNotificacion, PaginacionComponent, ProcesoReeducacionComponent],
  templateUrl: './agresores.html'
})
export class AgresoresComponent extends BaseCrudComponent<AgresorItem, Agresor> implements OnInit {
  
  private fb = inject(FormBuilder);
  private platformId = inject(PLATFORM_ID);
  private catalogosService = inject(CatalogosService);
  private http = inject(HttpClient);
  private route = inject(ActivatedRoute);

  servicio = inject(AgresoresService);
  procesoSeleccionado: any = null;
  @ViewChild(ProcesoReeducacionComponent) modalFisico!: ProcesoReeducacionComponent;

  mostrandoFormulario = false;
  pestanaActual = 1; // 1 a 5
  mostrarModalProceso = false;
  agresorActual: AgresorItem | null = null;

  filtrosForm = this.fb.group({
    curp: [''],
    nombre: ['']
  });

  filtrosActivos: { curp: string; nombre: string } = { curp: '', nombre: '' };

  aplicarFiltros() {
    this.filtrosActivos = {
      curp: this.filtrosForm.value.curp?.trim() || '',
      nombre: this.filtrosForm.value.nombre?.trim() || ''
    };
    this.paginaActual = 1;
  }

  limpiarFiltros() {
    this.filtrosForm.reset({ curp: '', nombre: '' });
    this.filtrosActivos = { curp: '', nombre: '' };
    this.paginaActual = 1;
  }

  override get datosFiltrados(): AgresorItem[] {
    return this.datosVista.filter(item => {
      const curpBuscada = this.filtrosActivos.curp.toLowerCase();
      const nombreBuscado = this.filtrosActivos.nombre.toLowerCase();

      const coincideCurp = !curpBuscada || (item.curp && item.curp.toLowerCase().includes(curpBuscada));
      
      const nombreCompleto = `${item.nombre || ''} ${item.apellido_paterno || ''} ${item.apellido_materno || ''}`.toLowerCase();
      const coincideNombre = !nombreBuscado || nombreCompleto.includes(nombreBuscado);

      return coincideCurp && coincideNombre;
    });
  }

  catalogos: any = {
    estadoCivil: [], situacionAcademica: [], situacionLaboral: [], situacionVivienda: [],
    rangoSalarial: [], religion: [], relacionHijos: [], sectoresSociales: [],
    actividadRecreativa: [], adicciones: [], generoMusical: [], tipoRelacion: [], tipoViolencia: []
  };

  formulario = this.fb.group({
    // Pestaña 1: Datos Generales
    curp: ['', [Validators.required, Validators.minLength(18), Validators.maxLength(18)]],
    nombre: ['', [Validators.required]],
    apellido_paterno: ['', [Validators.required]],
    apellido_materno: ['', [Validators.required]],
    edad: [0, [Validators.required, Validators.min(18)]],

    // Pestaña 2: Ubicaciones (Agrupadas para mejor manejo)
    lugar_nacimiento: this.fb.group({ latitud: [0], longitud: [0] }),
    lugar_residencia: this.fb.group({ latitud: [0], longitud: [0] }),
    lugar_trabajo: this.fb.group({ latitud: [0], longitud: [0] }),

    // Pestaña 3: Entorno Familiar
    parejas_previas: [0, Validators.required],
    hijos: [0, Validators.required],
    hermanos: [0, Validators.required],
    estado_civil_id: [0],
    relacion_hijos_id: [0],
    relacion_hermanos_ids: [[] as number []],
    relacion_padre_ids: [[] as number []],
    relacion_madre_ids: [[] as number []],
    violencia_infantil_ids: [[] as number []],

    // Pestaña 4: Perfil Socioeconómico
    situacion_academica_id: [0],
    situacion_laboral_id: [0],
    situacion_vivienda_id: [0],
    rango_salarial_id: [0],
    religion_id: [0],
    sectores_sociales_ids: [[] as number []],

    // Pestaña 5: Psicosocial
    actividades_recreativas_ids: [[] as number []],
    adicciones_ids: [[] as number []],
    generos_musicales_ids: [[] as number []]
  });

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarDatos();
      this.cargarCatalogos();
      this.verificarParametrosRuta();
    }
  }

  verificarParametrosRuta() {
    this.route.queryParams.subscribe(params => {
      const folio = params['folio'] ? Number(params['folio']) : (params['id'] ? Number(params['id']) : null);
      const curp = params['curp'] ? String(params['curp']).trim() : null;

      if (folio || curp) {
        if (curp) {
          this.filtrosForm.patchValue({ curp });
          this.filtrosActivos.curp = curp;
        }

        // Si los datos ya se encuentran en memoria
        if (this.datosVista && this.datosVista.length > 0) {
          const agresor = this.datosVista.find(a => 
            (folio && a.folio === folio) || 
            (curp && a.curp?.toLowerCase() === curp.toLowerCase())
          );
          if (agresor) {
            this.editar(agresor);
            return;
          }
        }

        // Si los datos aún no llegan por red o se busca por ID puntual
        if (folio) {
          this.servicio.obtenerPorId(folio).subscribe({
            next: (agresorApi) => {
              if (agresorApi) {
                this.editar(agresorApi);
              }
            },
            error: (e) => console.warn('No se pudo abrir el expediente del agresor:', e)
          });
        }
      }
    });
  }

  override despuesDeGuardar(): void {}

  protected override despuesDeCargarDatos(): void {
    const params = this.route.snapshot.queryParams;
    const folio = params['folio'] ? Number(params['folio']) : (params['id'] ? Number(params['id']) : null);
    const curp = params['curp'] ? String(params['curp']).trim() : null;

    if ((folio || curp) && !this.mostrandoFormulario) {
      const agresor = this.datosVista.find(a => 
        (folio && a.folio === folio) || 
        (curp && a.curp?.toLowerCase() === curp.toLowerCase())
      );
      if (agresor) {
        this.editar(agresor);
      }
    }
  }

abrirModalProcesos(event: Event, proceso: any = null): void {
    event.preventDefault();
    console.log("1. Botón presionado. Proceso a editar:", proceso);
    
    // Primero, le decimos a Angular que dibuje el modal en pantalla
    this.mostrarModalProceso = true;
    this.cd.markForCheck(); 

    // Segundo: Le damos un milisegundo a Angular para que termine de dibujarlo 
    // y luego le disparamos los datos directamente por la espalda
    setTimeout(() => {
      if (this.modalFisico) {
        this.modalFisico.cargarProceso(proceso);
      } else {
        console.error("❌ El modal no se encontró en el DOM.");
      }
    }, 0);
  }

  override editar(item: AgresorItem) {
    console.log(item)
    this.mostrandoFormulario = true;
    this.pestanaActual = 1;
    setTimeout(() => {
      super.editar(item); 
    }, 0);
  }
override guardar(): void {
    if (this.formulario.invalid) {
      this.formulario.markAllAsTouched();
      return;
    }

    this.cargando = true;

    const val = this.formulario.getRawValue();
    
    const payload = {
      curp: (val.curp || '').toUpperCase(),
      nombre: val.nombre || '',
      apellido_paterno: val.apellido_paterno || '',
      apellido_materno: val.apellido_materno || '',
      edad: Number(val.edad || 0),
      
      lugar_nacimiento: { latitud: Number(val.lugar_nacimiento?.latitud || 0), longitud: Number(val.lugar_nacimiento?.longitud || 0) },
      lugar_residencia: { latitud: Number(val.lugar_residencia?.latitud || 0), longitud: Number(val.lugar_residencia?.longitud || 0) },
      lugar_trabajo: { latitud: Number(val.lugar_trabajo?.latitud || 0), longitud: Number(val.lugar_trabajo?.longitud || 0) },
      
      parejas_previas: Number(val.parejas_previas || 0),
      hijos: Number(val.hijos || 0),
      hermanos: Number(val.hermanos || 0),
      
      estado_civil_id: val.estado_civil_id ? Number(val.estado_civil_id) : null,
      situacion_academica_id: val.situacion_academica_id ? Number(val.situacion_academica_id) : null,
      situacion_laboral_id: val.situacion_laboral_id ? Number(val.situacion_laboral_id) : null,
      situacion_vivienda_id: val.situacion_vivienda_id ? Number(val.situacion_vivienda_id) : null,
      rango_salarial_id: val.rango_salarial_id ? Number(val.rango_salarial_id) : null,
      religion_id: val.religion_id ? Number(val.religion_id) : null,
      relacion_hijos_id: val.relacion_hijos_id ? Number(val.relacion_hijos_id) : null,
      
      sectores_sociales: (val.sectores_sociales_ids || []).map(Number),
      actividades_recreativas: (val.actividades_recreativas_ids || []).map(Number),
      adicciones: (val.adicciones_ids || []).map(Number),
      generos_musicales: (val.generos_musicales_ids || []).map(Number),
      relacion_hermanos: (val.relacion_hermanos_ids || []).map(Number),
      relacion_padre: (val.relacion_padre_ids || []).map(Number),
      relacion_madre: (val.relacion_madre_ids || []).map(Number),
      violencia_infantil: (val.violencia_infantil_ids || []).map(Number)
    };

    const peticion$ = this.modoEdicion && this.idEdicion !== null
      ? this.servicio.actualizar(this.idEdicion, payload as any)
      : this.servicio.crear(payload as any);

    peticion$.subscribe({
     next: () => this.exitoAlGuardar(
       this.modoEdicion ? 'Actualización exitosa' : 'Registro exitoso',
       this.modoEdicion ? 'Registro actualizado correctamente.' : 'Registro guardado correctamente.'
     ),
     error: (err) => this.errorAlGuardar(err)
    });
  }

  // --- CARGA MASIVA DE CATÁLOGOS EN PARALELO ---
  cargarCatalogos() {
    forkJoin({
      estadoCivil: this.catalogosService.obtenerTodos('estado-civil'),
      situacionAcademica: this.catalogosService.obtenerTodos('situacion-academica'),
      situacionLaboral: this.catalogosService.obtenerTodos('situacion-laboral'),
      situacionVivienda: this.catalogosService.obtenerTodos('situacion-vivienda'),
      rangoSalarial: this.catalogosService.obtenerTodos('rango-salarial'),
      religion: this.catalogosService.obtenerTodos('religion'),
      relacionHijos: this.catalogosService.obtenerTodos('relacion-hijos'),
      sectoresSociales: this.catalogosService.obtenerTodos('sectores-sociales'),
      actividadRecreativa: this.catalogosService.obtenerTodos('actividad-recreativa'),
      adicciones: this.catalogosService.obtenerTodos('adicciones'),
      generoMusical: this.catalogosService.obtenerTodos('genero-musical'),
      tipoRelacion: this.catalogosService.obtenerTodos('tipo-relacion'),
      tipoViolencia: this.catalogosService.obtenerTodos('tipo-violencia')
    }).subscribe(resultados => {
      this.catalogos = resultados;
      this.cd.markForCheck();
    });
  }

  abrirNuevo() {
    this.formulario.reset();
    this.pestanaActual = 1;
    this.modoEdicion = false;
    this.idEdicion = null;
    this.mostrandoFormulario = true;
  }

  override cancelarOperacion() {
    super.cancelarOperacion();
    this.mostrandoFormulario = false;
  }

  cambiarPestana(numero: number) {
    this.pestanaActual = numero;
  }

 override mapearPayloadParaGuardar(): Agresor { 
    const val = this.formulario.value;
    
    return {

      // 1. Datos Generales
      curp: (val.curp || '').toUpperCase(),
      nombre: val.nombre || '',
      apellido_paterno: val.apellido_paterno || '',
      apellido_materno: val.apellido_materno || '',
      edad: Number(val.edad || 0),
      
      // 2. Ubicaciones
      lugar_nacimiento: { 
        latitud: Number(val.lugar_nacimiento?.latitud || 0), 
        longitud: Number(val.lugar_nacimiento?.longitud || 0) 
      },
      lugar_residencia: { 
        latitud: Number(val.lugar_residencia?.latitud || 0), 
        longitud: Number(val.lugar_residencia?.longitud || 0) 
      },
      lugar_trabajo: { 
        latitud: Number(val.lugar_trabajo?.latitud || 0), 
        longitud: Number(val.lugar_trabajo?.longitud || 0) 
      },
      
      // 3. Contadores
      parejas_previas: Number(val.parejas_previas || 0),
      hijos: Number(val.hijos || 0),
      hermanos: Number(val.hermanos || 0),
      
      // --- 4. Catálogos Simples ---
      estado_civil_id: val.estado_civil_id ? Number(val.estado_civil_id) : null,
      situacion_academica_id: val.situacion_academica_id ? Number(val.situacion_academica_id) : null,
      situacion_laboral_id: val.situacion_laboral_id ? Number(val.situacion_laboral_id) : null,
      situacion_vivienda_id: val.situacion_vivienda_id ? Number(val.situacion_vivienda_id) : null,
      rango_salarial_id: val.rango_salarial_id ? Number(val.rango_salarial_id) : null,
      religion_id: val.religion_id ? Number(val.religion_id) : null,
      relacion_hijos_id: val.relacion_hijos_id ? Number(val.relacion_hijos_id) : null,
      
      // --- 5. Selecciones Múltiples (Respetamos los nombres _ids de tu interfaz Agresor) ---
      sectores_sociales_ids: (val.sectores_sociales_ids || []).map((id: any) => Number(id)),
      actividades_recreativas_ids: (val.actividades_recreativas_ids || []).map((id: any) => Number(id)),
      adicciones_ids: (val.adicciones_ids || []).map((id: any) => Number(id)),
      generos_musicales_ids: (val.generos_musicales_ids || []).map((id: any) => Number(id)),
      relacion_hermanos_ids: (val.relacion_hermanos_ids || []).map((id: any) => Number(id)),
      relacion_padre_ids: (val.relacion_padre_ids || []).map((id: any) => Number(id)),
      relacion_madre_ids: (val.relacion_madre_ids || []).map((id: any) => Number(id)),
      violencia_infantil_ids: (val.violencia_infantil_ids || []).map((id: any) => Number(id))
    };
    
  }

override mapearDatosParaEditar(item: AgresorItem): void { 
    this.idEdicion = item.folio;

    this.agresorActual = item;
    console.log(item);

    this.formulario.patchValue({
      // 1. Datos Generales
      curp: item.curp,
      nombre: item.nombre,
      apellido_paterno: item.apellido_paterno,
      apellido_materno: item.apellido_materno,
      edad: item.edad,

      // 2. Ubicaciones
        lugar_nacimiento: { 
        latitud: item.lugar_nacimiento?.latitud,
        longitud: item.lugar_nacimiento?.longitud,
      },
      lugar_residencia: { 
        latitud: Number(item.lugar_residencia?.latitud || 0), 
        longitud: Number(item.lugar_residencia?.longitud || 0) 
      },
      lugar_trabajo: { 
        latitud: Number(item.lugar_trabajo?.latitud || 0), 
        longitud: Number(item.lugar_trabajo?.longitud || 0) 
      },

      // 3. Contadores Numéricos
      parejas_previas: item.parejas_previas,
      hijos: item.hijos,
      hermanos: item.hermanos,

      // 4. Objetos Individuales -> Extraemos el .id y lo mandamos a los campos _id
      estado_civil_id: item.estado_civil?.id || null,
      situacion_academica_id: item.situacion_academica?.id || null,
      situacion_laboral_id: item.situacion_laboral?.id || null,
      situacion_vivienda_id: item.situacion_vivienda?.id || null,
      rango_salarial_id: item.rango_salarial?.id || null,
      religion_id: item.religion?.id || null,
      relacion_hijos_id: item.relacion_hijos?.id || null,

      // 5. Arreglos de Objetos -> Extraemos los ids y los mandamos a los campos _ids del form
      sectores_sociales_ids: (item.sectores_sociales || []).map((c: any) => c.id),
      actividades_recreativas_ids: (item.actividades_recreativas || []).map((c: any) => c.id),
      adicciones_ids: (item.adicciones || []).map((c: any) => c.id),
      generos_musicales_ids: (item.generos_musicales || []).map((c: any) => c.id),
      relacion_hermanos_ids: (item.relacion_hermanos || []).map((c: any) => c.id),
      relacion_padre_ids: (item.relacion_padre || []).map((c: any) => c.id),
      relacion_madre_ids: (item.relacion_madre || []).map((c: any) => c.id),
      violencia_infantil_ids: (item.violencia_infantil || []).map((c: any) => c.id)
    });
  }
  getId(item: AgresorItem): number {
    return item.folio;
  }
  pegarDesdeGoogleMaps(event: ClipboardEvent, nombreGrupo: string): void {
    const textoPegado = event.clipboardData?.getData('text') || '';

    // Buscamos el patrón clásico de Google Maps: @18.8329,-99.2312 o q=18.8329,-99.2312
    const regex = /[@=](-?\d+\.\d+),(-?\d+\.\d+)/;
    const coincidencias = textoPegado.match(regex);

    if (coincidencias) {
      // Si detectamos que es un enlace, evitamos que se pegue la URL enorme
      event.preventDefault(); 
      
      const latitudExtraida = Number(coincidencias[1]);
      const longitudExtraida = Number(coincidencias[2]);

      // Apuntamos exactamente al grupo que nos pasaron por parámetro
      const grupoUbicacion = this.formulario.get(nombreGrupo);
      
      if (grupoUbicacion) {
        grupoUbicacion.patchValue({
          latitud: latitudExtraida,
          longitud: longitudExtraida
        });
        
        grupoUbicacion.markAsDirty();
        console.log(`📍 Coordenadas mapeadas con éxito en [${nombreGrupo}]:`, latitudExtraida, longitudExtraida);
      }
    }
  }

alGuardarProceso(resultado: any): void {
  const tabTemporal = this.pestanaActual;
    console.log("🚩 2. Hilo del padre: ¡Datos recibidos del modal!", resultado);

    // Verificamos si el arreglo existe, porque si es null, jamás entrará a hacer el push/reemplazo
    console.log("Estado del arreglo antes de actualizar:", this.agresorActual?.proceso_reeducacion);

    if (this.agresorActual) {
      const arreglo = this.agresorActual.proceso_reeducacion as any[];
      
      if (resultado.modo === 'crear') {
        arreglo.push(resultado.proceso);
        console.log("🚩 3. Padre: ¡Se agregó un proceso nuevo a la tabla!");
      } else {
        const idBuscado = resultado.proceso.id || resultado.proceso.folio;
        const index = arreglo.findIndex((p: any) => (p.id || p.folio) === idBuscado);
        if (index !== -1) {
          arreglo[index] = resultado.proceso;
          console.log("🚩 3. Padre: ¡Se actualizó el proceso en la tabla!");
        }
      }
    }
    
    this.mostrarModalProceso = false; // (O la variable que uses)
    this.pestanaActual = tabTemporal;
    this.cd.markForCheck();
  }
}