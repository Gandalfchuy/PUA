import { describe, it, expect, beforeEach } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ɵresolveComponentResources as resolveComponentResources } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter } from '@angular/router';
import { DashboardComponent } from './dashboard';
import { KpiCardsComponent } from './components/kpi-cards/kpi-cards';
import { GraficaViolenciasComponent } from './components/grafica-violencias/grafica-violencias';
import { GraficaAdiccionesComponent } from './components/grafica-adicciones/grafica-adicciones';
import { TablaAlertasComponent } from './components/tabla-alertas/tabla-alertas';
import { DashboardService } from '../../core/services/dashboard.service';

describe('DashboardComponent Suite', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async () => {
    await resolveComponentResources(() => Promise.resolve('<div></div>'));
    await TestBed.configureTestingModule({
      imports: [
        DashboardComponent,
        KpiCardsComponent,
        GraficaViolenciasComponent,
        GraficaAdiccionesComponent,
        TablaAlertasComponent
      ],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([]),
        DashboardService
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
  });

  it('debe crearse el DashboardComponent exitosamente', () => {
    expect(component).toBeTruthy();
  });

  it('debe inicializar la fecha actual', () => {
    expect(component.fechaActual).toBeInstanceOf(Date);
  });

  it('debe crear KpiCardsComponent correctamente', () => {
    const kpiFixture = TestBed.createComponent(KpiCardsComponent);
    const kpiComp = kpiFixture.componentInstance;
    expect(kpiComp).toBeTruthy();
    expect(kpiComp.cargando).toBe(true);
  });

  it('debe crear GraficaViolenciasComponent correctamente', () => {
    const violFixture = TestBed.createComponent(GraficaViolenciasComponent);
    const violComp = violFixture.componentInstance;
    expect(violComp).toBeTruthy();
    expect(violComp.cargando).toBe(true);
  });

  it('debe crear GraficaAdiccionesComponent y calcular segmentos', () => {
    const adicFixture = TestBed.createComponent(GraficaAdiccionesComponent);
    const adicComp = adicFixture.componentInstance;
    adicComp.adicciones = [
      { adiccion: 'Alcohol', total: 10, porcentaje: 50.0 },
      { adiccion: 'Cannabis', total: 10, porcentaje: 50.0 }
    ];
    adicComp.calcularSegmentos();
    expect(adicComp.totalCasos).toBe(20);
    expect(adicComp.segmentos.length).toBe(2);
  });

  it('debe crear TablaAlertasComponent correctamente', () => {
    const alertasFixture = TestBed.createComponent(TablaAlertasComponent);
    const alertasComp = alertasFixture.componentInstance;
    expect(alertasComp).toBeTruthy();
    expect(alertasComp.cargando).toBe(true);
  });
});
