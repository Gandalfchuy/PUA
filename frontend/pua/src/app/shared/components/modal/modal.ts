import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './modal.html'
})
export class ModalComponent {
  // Entradas dinámicas para controlar el contenido
  @Input() mostrar = false;
  @Input() tipo: 'exito' | 'error' = 'error';
  @Input() titulo = '';
  @Input() mensaje = '';

  // Evento para avisar al padre que el botón "Entendido" fue presionado
  @Output() alCerrar = new EventEmitter<void>();

  cerrar() {
    this.alCerrar.emit();
  }
}
