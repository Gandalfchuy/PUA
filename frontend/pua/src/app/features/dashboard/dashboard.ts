import { Component, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { KpiCardsComponent } from './components/kpi-cards/kpi-cards';
import { MapaCalorComponent } from './components/mapa-calor/mapa-calor';
import { GraficaViolenciasComponent } from './components/grafica-violencias/grafica-violencias';
import { GraficaAdiccionesComponent } from './components/grafica-adicciones/grafica-adicciones';
import { TablaAlertasComponent } from './components/tabla-alertas/tabla-alertas';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    KpiCardsComponent,
    MapaCalorComponent,
    GraficaViolenciasComponent,
    GraficaAdiccionesComponent,
    TablaAlertasComponent
  ],
  templateUrl: './dashboard.html',
  styles: [`:host { display: block; width: 100%; }`]
})
export class DashboardComponent {
  @ViewChild(KpiCardsComponent) kpisComp?: KpiCardsComponent;
  @ViewChild(MapaCalorComponent) mapaComp?: MapaCalorComponent;
  @ViewChild(GraficaViolenciasComponent) violenciasComp?: GraficaViolenciasComponent;
  @ViewChild(GraficaAdiccionesComponent) adiccionesComp?: GraficaAdiccionesComponent;
  @ViewChild(TablaAlertasComponent) alertasComp?: TablaAlertasComponent;

  fechaActual = new Date();

  recargarTodo(): void {
    this.fechaActual = new Date();
    this.kpisComp?.cargarKpis();
    this.mapaComp?.cargarDatos();
    this.violenciasComp?.cargarDatos();
    this.adiccionesComp?.cargarDatos();
    this.alertasComp?.cargarAlertas();
  }
}
