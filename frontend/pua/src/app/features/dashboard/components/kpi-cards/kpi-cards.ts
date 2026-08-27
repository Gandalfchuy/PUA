import { Component, inject, OnInit, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { DashboardService } from '../../../../core/services/dashboard.service';
import { DashboardKpis } from '../../../../core/models/dashboard.models';

@Component({
  selector: 'app-kpi-cards',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './kpi-cards.html',
  styles: [`:host { display: block; width: 100%; }`]
})
export class KpiCardsComponent implements OnInit {
  private dashboardService = inject(DashboardService);
  private platformId = inject(PLATFORM_ID);
  private cd = inject(ChangeDetectorRef);

  kpis: DashboardKpis | null = null;
  cargando = true;
  error = false;

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarKpis();
    }
  }

  cargarKpis(): void {
    this.cargando = true;
    this.error = false;
    this.dashboardService.getKpis().subscribe({
      next: (data) => {
        this.kpis = data;
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
