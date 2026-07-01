import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-modal-notificacion',
  imports: [CommonModule],
  templateUrl: './modal-notificacion.html',
  styleUrl: './modal-notificacion.css',
})
export class ModalNotificacion {
  @Input() mostrar = false;
  @Input() tipo: 'exito' | 'error' | 'confirmacion' = 'exito';
  @Input() titulo = '';
  @Input() mensaje = '';


  @Output() cerrado = new EventEmitter<void>();
  @Output() confirmado = new EventEmitter<void>();

  cerrar() {
    this.cerrado.emit();
  }

  confirmar() {
    this.confirmado.emit();
  }
}
