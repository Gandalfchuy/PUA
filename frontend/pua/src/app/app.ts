import { Component, inject, signal } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { SidebarComponent } from './shared/components/sidebar/sidebar';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, SidebarComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  private router = inject(Router);
  protected readonly title = signal('pua');
  mostrarSidebar(): boolean {
    // Si la ruta actual es exactamente '/login', ocultamos el sidebar
    if (this.router.url === '/login') {
      return false;
    }
    // Para cualquier otra ruta (/agresores, /catalogos, etc), lo mostramos
    return true;
  }
}
