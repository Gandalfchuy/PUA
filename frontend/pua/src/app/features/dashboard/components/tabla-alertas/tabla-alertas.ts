import { Component, inject, OnInit, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { DashboardService } from '../../../../core/services/dashboard.service';
import { AlertaDesercionItem } from '../../../../core/models/dashboard.models';

@Component({
  selector: 'app-tabla-alertas',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './tabla-alertas.html',
  styles: [`:host { display: block; width: 100%; }`]
})
export class TablaAlertasComponent implements OnInit {
  private dashboardService = inject(DashboardService);
  private platformId = inject(PLATFORM_ID);
  private cd = inject(ChangeDetectorRef);

  alertas: AlertaDesercionItem[] = [];
  cargando = true;
  error = false;

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarAlertas();
    }
  }

  cargarAlertas(): void {
    this.cargando = true;
    this.error = false;
    this.dashboardService.getAlertas().subscribe({
      next: (data) => {
        this.alertas = data.alertas || [];
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
}
