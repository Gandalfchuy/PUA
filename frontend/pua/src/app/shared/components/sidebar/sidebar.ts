import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.html'
})
export class SidebarComponent {
  private router = inject(Router);

  cerrarSesion(): void {
    localStorage.removeItem('pua_token');
    this.router.navigate(['/login']);
  }
}