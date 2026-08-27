import { Directive, inject, ChangeDetectorRef } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { BaseCrudService } from '../core/services/base-crud';

@Directive()
export abstract class BaseCrudComponent<TItem, T> {
    protected cd = inject(ChangeDetectorRef);

    // ESTADO DE DATOS Y UI 
    datosVista: TItem[] = [];
    cargando = false;
    recursoDinamico: string = '';

    // ESTADO DEL CRUD
    modoEdicion = false;
    idEdicion: number | null=null;
    idPendiente: number | null = null;

    // ESTADO DE MODALES
    mostrarModal = false;
    modalConfig: { tipo: 'exito' | 'error' | 'confirmacion'; titulo: string; mensaje: string } = {
        tipo: 'exito',
        titulo: '',
        mensaje: ''
    };

    // ESTADO DE PAGINACIÓN Y BÚSQUEDA
    terminoBusqueda: string = '';
    paginaActual = 1;
    elementosPorPagina = 5;

    // CONTRATOS:
    abstract formulario: FormGroup;
    abstract servicio: BaseCrudService<TItem, T>;
    abstract mapearPayloadParaGuardar(): T;
    abstract mapearDatosParaEditar(item: TItem): void;
    filtrarDato(item: TItem, busqueda: string): boolean {
        return true;
    }
    abstract getId(item: TItem): number;

    protected antesDeGuardar(payload: T): T {
        return payload;
    }
    protected despuesDeGuardar(): void { }
    protected despuesDeCargarDatos(): void { }

    protected despuesDeParcharEdicion(item: TItem): void { }

    // LECTURA
    cargarDatos() {
        this.cargando = true;
        this.servicio.obtenerTodos(this.recursoDinamico).subscribe({
            next: (datos) => {
                this.datosVista = datos;
                this.paginaActual = 1;
                this.cargando = false;
                this.despuesDeCargarDatos();
                this.cd.markForCheck();
            },
            error: (err) => {
                this.cargando = false;
                this.mostrarMensaje('error', 'Error de conexión', 'No se pudieron cargar los datos.');
                this.cd.markForCheck();
            }
        });
    }

    // ESCRITURA Y ACTUALIZACIÓN
    guardar() {
        if (this.formulario.invalid || this.cargando) {
            this.formulario.markAllAsTouched();
            return;
        }

        const payload = this.mapearPayloadParaGuardar();
        this.cargando = true;
        this.formulario.disable();
        this.cd.markForCheck();

        if (this.modoEdicion && this.idEdicion !== null) {
            this.servicio.actualizar(this.idEdicion, payload, this.recursoDinamico).subscribe({
                next: () => this.exitoAlGuardar('Actualización exitosa', 'Registro actualizado correctamente.'),
                error: (err) => this.errorAlGuardar(err)
            });
        } else {
            this.servicio.crear(payload, this.recursoDinamico).subscribe({
                next: () => this.exitoAlGuardar('Registro exitoso', 'Registro guardado correctamente.'),
                error: (err) => this.errorAlGuardar(err)
            });
        }
    }

    // ELIMINACIÓN 
    eliminar(id: number) {
        this.idPendiente = id;
        this.mostrarMensaje('confirmacion', '¿Eliminar registro?', 'Esta acción no se puede deshacer.');
    }

    ejecutarEliminacion() {
        if (this.idPendiente === null) return;

        this.mostrarModal = false;
        this.cargando = true;
        this.formulario.disable();
        this.cd.markForCheck();

        this.servicio.eliminar(this.idPendiente, this.recursoDinamico).subscribe({
            next: () => {
                this.idPendiente = null;
                this.exitoAlGuardar('Eliminado', 'El registro se eliminó con éxito.');
            },
            error: (err) => this.errorAlGuardar(err)
        });
    }

    // CONTROL DE FORMULARIO 
    editar(item: TItem) {
        this.modoEdicion = true;
        this.mapearDatosParaEditar(item); 
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    cancelarOperacion() {
        this.formulario.reset();
        this.formulario.enable();
        this.modoEdicion = false;
        this.idEdicion = null;
        this.idPendiente = null;
    }

    // PAGINACIÓN Y BÚSQUEDA
    alEscribirBusqueda(texto: string) {
        this.terminoBusqueda = texto;
        this.paginaActual = 1;
    }

    get datosFiltrados(): TItem[] {
        if (!this.terminoBusqueda) return this.datosVista;
        const busqueda = this.terminoBusqueda.toLowerCase();
        return this.datosVista.filter(item => this.filtrarDato(item, busqueda));
    }

   get datosPaginados(): TItem[] {
        const inicio = (this.paginaActual - 1) * this.elementosPorPagina;
        // Ahora corta la lista que ya pasó por los filtros
        return this.datosFiltrados.slice(inicio, inicio + this.elementosPorPagina);
    }

    get totalPaginas(): number {
        // Ahora calcula el total de páginas basándose en los resultados encontrados
        return Math.ceil(this.datosFiltrados.length / this.elementosPorPagina) || 1;
    }

    cambiarPagina(nuevaPagina: number) {
        if (nuevaPagina >= 1 && nuevaPagina <= this.totalPaginas) {
            this.paginaActual = nuevaPagina;
        }
    }

    exitoAlGuardar(titulo: string, msj: string) {
        this.cargarDatos();
        this.cancelarOperacion();
        this.mostrarMensaje('exito', titulo, msj);
    }

    errorAlGuardar(err: any) {
        this.cargando = false;
        this.formulario.enable();
        this.cd.markForCheck();
        const errorMsj = err.error?.detail || 'Ocurrió un error en el servidor.';
        this.mostrarMensaje('error', 'Operación Fallida', errorMsj);
    }

    mostrarMensaje(tipo: any, titulo: string, mensaje: string) {
        this.modalConfig = { tipo, titulo, mensaje };
        this.mostrarModal = true;
    }

    cerrarMensaje() {
        this.mostrarModal = false;
        if (this.modalConfig.tipo === 'confirmacion') this.idPendiente = null;
    }

     
}