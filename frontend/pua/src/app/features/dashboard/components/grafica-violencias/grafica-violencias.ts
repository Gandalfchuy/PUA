import { Component, inject, OnInit, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { DashboardService } from '../../../../core/services/dashboard.service';
import { TipoViolenciaStat } from '../../../../core/models/dashboard.models';

@Component({
  selector: 'app-grafica-violencias',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './grafica-violencias.html',
  styles: [`:host { display: block; width: 100%; }`]
})
export class GraficaViolenciasComponent implements OnInit {
  private dashboardService = inject(DashboardService);
  private platformId = inject(PLATFORM_ID);
  private cd = inject(ChangeDetectorRef);

  tiposViolencia: TipoViolenciaStat[] = [];
  cargando = true;
  error = false;

  readonly colores: string[] = [
    'bg-indigo-600',
    'bg-sky-500',
    'bg-emerald-500',
    'bg-amber-500',
    'bg-rose-500',
    'bg-purple-500',
    'bg-teal-500'
  ];

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarDatos();
    }
  }

  cargarDatos(): void {
    this.cargando = true;
    this.error = false;
    this.dashboardService.getTiposViolencia().subscribe({
      next: (data) => {
        this.tiposViolencia = data.tipos || [];
        this.cargando = false;
        this.cd.markForCheck();
      },
      error: () => {
        this.error = true;
        this.cargando = false;
        this.cd.markForCheck();
      }
    });
  }

  getColor(index: number): string {
    return this.colores[index % this.colores.length];
  }
}
