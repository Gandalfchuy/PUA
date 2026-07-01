import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-paginacion',
  standalone: true,
  templateUrl: './paginacion.html'
})
export class PaginacionComponent {
  // 📥 Entradas (Lo que le manda el componente padre)
  @Input() totalRegistros: number = 0;
  @Input() elementosPorPagina: number = 5;
  @Input() paginaActual: number = 1;

  // 📤 Salidas (El evento que avisa al padre que cambiaron de página)
  @Output() cambioDePagina = new EventEmitter<number>();

  // Referencia a Math para el HTML
  protected readonly Math = Math;

  get totalPaginas(): number {
    return Math.ceil(this.totalRegistros / this.elementosPorPagina) || 1;
  }

  cambiar(nuevaPagina: number) {
    if (nuevaPagina >= 1 && nuevaPagina <= this.totalPaginas) {
      this.cambioDePagina.emit(nuevaPagina);
    }
  }
}