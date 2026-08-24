import { Component, Input, Output, EventEmitter, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './modal.html'
})
export class ModalComponent {
  // Entradas dinámicas para controlar el contenido
  @Input() mostrar = false;
  @Input() tipo:  'acceso_autorizado' | 'exito' | 'error' = 'error';
  @Input() titulo = '';
  @Input() mensaje = '';
  @Output() alCerrar = new EventEmitter<void>();
  private router = inject(Router)

  cerrar() {
    if (this.tipo === 'acceso_autorizado') {
      this.router.navigate(['/agresores']);
    }
    this.alCerrar.emit();
  }
}
