import { Component, inject, OnInit, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { DashboardService } from '../../../../core/services/dashboard.service';
import { AdiccionStat } from '../../../../core/models/dashboard.models';

interface SegmentoDonut {
  adiccion: string;
  total: number;
  porcentaje: number;
  color: string;
  dashArray: string;
  dashOffset: number;
}

@Component({
  selector: 'app-grafica-adicciones',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './grafica-adicciones.html',
  styles: [`:host { display: block; width: 100%; }`]
})
export class GraficaAdiccionesComponent implements OnInit {
  private dashboardService = inject(DashboardService);
  private platformId = inject(PLATFORM_ID);
  private cd = inject(ChangeDetectorRef);

  adicciones: AdiccionStat[] = [];
  segmentos: SegmentoDonut[] = [];
  totalCasos = 0;
  cargando = true;
  error = false;

  readonly paletaColores: string[] = [
    '#6366f1', // Indigo
    '#0ea5e9', // Sky
    '#10b981', // Emerald
    '#f59e0b', // Amber
    '#f43f5e', // Rose
    '#8b5cf6', // Purple
    '#64748b'  // Slate
  ];

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarDatos();
    }
  }

  cargarDatos(): void {
    this.cargando = true;
    this.error = false;
    this.dashboardService.getAdicciones().subscribe({
      next: (data) => {
        this.adicciones = data.adicciones || [];
        this.calcularSegmentos();
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

  calcularSegmentos(): void {
    this.totalCasos = this.adicciones.reduce((sum, item) => sum + item.total, 0);
    const circunferencia = 2 * Math.PI * 40; // radio = 40 => perímetro ≈ 251.32
    let acumuladoOffset = 0;

    this.segmentos = this.adicciones.map((item, idx) => {
      const porcentaje = this.totalCasos > 0 ? (item.total / this.totalCasos) : 0;
      const longitudArco = porcentaje * circunferencia;
      const dashArray = `${longitudArco} ${circunferencia - longitudArco}`;
      const dashOffset = -acumuladoOffset;

      acumuladoOffset += longitudArco;

      return {
        adiccion: item.adiccion,
        total: item.total,
        porcentaje: item.porcentaje,
        color: this.paletaColores[idx % this.paletaColores.length],
        dashArray,
        dashOffset
      };
    });
  }
}
