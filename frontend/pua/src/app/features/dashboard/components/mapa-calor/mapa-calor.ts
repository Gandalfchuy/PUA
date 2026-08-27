import { Component, inject, OnInit, AfterViewInit, OnDestroy, ElementRef, ViewChild, PLATFORM_ID, ChangeDetectorRef } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { DashboardService } from '../../../../core/services/dashboard.service';
import { DashboardMapa } from '../../../../core/models/dashboard.models';

@Component({
  selector: 'app-mapa-calor',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mapa-calor.html',
  styleUrls: ['./mapa-calor.css']
})
export class MapaCalorComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('mapContainer') mapContainer!: ElementRef<HTMLDivElement>;

  private dashboardService = inject(DashboardService);
  private platformId = inject(PLATFORM_ID);
  private cd = inject(ChangeDetectorRef);

  private map: any = null;
  private heatLayer: any = null;
  private markersLayer: any = null;
  private L: any = null;

  mapData: DashboardMapa | null = null;
  cargando = true;
  error = false;
  mostrarCalor = true;
  mostrarSedes = true;

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.cargarDatos();
    }
  }

  async ngAfterViewInit(): Promise<void> {
    if (isPlatformBrowser(this.platformId)) {
      await this.inicializarInstanciaMapa();
      if (this.mapData) {
        this.renderizarCapas();
      }
    }
  }

  ngOnDestroy(): void {
    if (this.map) {
      this.map.remove();
      this.map = null;
    }
  }

  cargarDatos(): void {
    this.cargando = true;
    this.error = false;
    this.dashboardService.getMapaCalor().subscribe({
      next: (data) => {
        this.mapData = data;
        this.cargando = false;
        this.cd.markForCheck();
        // Si el mapa ya se inicializó, renderizamos las capas de inmediato
        if (this.map && this.L) {
          this.renderizarCapas();
        } else {
          setTimeout(() => this.inicializarInstanciaMapa(), 50);
        }
      },
      error: (err) => {
        console.error('Error al cargar datos del mapa:', err);
        this.error = true;
        this.cargando = false;
        this.cd.markForCheck();
      }
    });
  }

  async inicializarInstanciaMapa(): Promise<void> {
    if (!isPlatformBrowser(this.platformId) || !this.mapContainer) {
      return;
    }

    try {
      if (!this.L) {
        const leafletModule: any = await import('leaflet');
        this.L = leafletModule.default?.map ? leafletModule.default : (leafletModule.map ? leafletModule : (leafletModule.default || leafletModule));
        (window as any).L = this.L;

        try {
          // @ts-ignore
          await import('leaflet.heat');
        } catch (e) {
          console.warn('leaflet.heat no disponible, usando renderizador térmico integrado:', e);
        }
      }

      const container = this.mapContainer.nativeElement;
      if (!container || this.map) return;

      // Inicializar mapa en el contenedor
      this.map = this.L.map(container, {
        center: [18.7350, -99.0700],
        zoom: 10,
        zoomControl: true,
        scrollWheelZoom: true
      });

      // Capa base de OpenStreetMap (100% libre, sin API key)
      this.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      }).addTo(this.map);

      this.markersLayer = this.L.layerGroup().addTo(this.map);

      if (this.mapData) {
        this.renderizarCapas();
      }

      setTimeout(() => {
        if (this.map) {
          this.map.invalidateSize();
        }
      }, 200);

    } catch (err) {
      console.error('Error al crear el mapa:', err);
    }
  }

  renderizarCapas(): void {
    if (!this.map || !this.L || !this.mapData) return;

    const puntos = this.mapData.puntos_calor || [];
    const sedes = this.mapData.sedes || [];

    // Limpiar capas previas si existen
    if (this.heatLayer) {
      this.map.removeLayer(this.heatLayer);
      this.heatLayer = null;
    }
    if (this.markersLayer) {
      this.markersLayer.clearLayers();
    }

    // 1. Capa de Calor
    if (puntos.length > 0) {
      const puntosCoords = puntos.map(p => [p.lat, p.lng, p.peso || 1.0]);

      if (typeof (this.L as any).heatLayer === 'function') {
        this.heatLayer = (this.L as any).heatLayer(puntosCoords, {
          radius: 28,
          blur: 18,
          maxZoom: 14,
          max: 1.0,
          gradient: {
            0.2: '#38bdf8',
            0.4: '#34d399',
            0.6: '#fbbf24',
            0.8: '#f97316',
            1.0: '#ef4444'
          }
        });
      } else {
        // Fallback visual de alta fidelidad: Círculos radiales térmicos
        this.heatLayer = this.L.layerGroup();
        for (const p of puntos) {
          this.L.circleMarker([p.lat, p.lng], {
            radius: 16,
            fillColor: '#ef4444',
            color: '#f97316',
            weight: 1.5,
            opacity: 0.8,
            fillOpacity: 0.45
          }).addTo(this.heatLayer);
        }
      }

      if (this.mostrarCalor && this.heatLayer) {
        this.heatLayer.addTo(this.map);
      }
    }

    // 2. Marcadores de Sedes Comunitarias
    const sedeIcon = this.L.divIcon({
      className: 'custom-sede-pin',
      html: `<div style="background-color: #0f172a; color: #ffffff; padding: 4px 10px; border-radius: 9999px; font-size: 11px; font-weight: 700; border: 2px solid #38bdf8; box-shadow: 0 4px 8px rgba(0,0,0,0.35); display: flex; align-items: center; gap: 5px; white-space: nowrap;">
              <span style="display:inline-block; width:7px; height:7px; background-color:#38bdf8; border-radius:9999px; box-shadow: 0 0 4px #38bdf8;"></span>
              Sede
             </div>`,
      iconSize: [65, 26],
      iconAnchor: [32, 13]
    });

    for (const sede of sedes) {
      const marker = this.L.marker([sede.lat, sede.lng], { icon: sedeIcon });
      marker.bindPopup(`
        <div style="font-family: inherit; font-size: 13px; color: #0f172a; padding: 4px;">
          <span style="display:inline-block; padding: 2px 6px; background:#e0f2fe; color:#0369a1; font-weight:700; font-size:10px; border-radius:4px; margin-bottom:4px;">SEDE COMUNITARIA</span>
          <strong style="display:block; font-size: 14px; margin-bottom: 2px;">${sede.lugar}</strong>
          <span style="color: #64748b; font-size: 11px;">Folio #${sede.folio} | Morelos</span>
        </div>
      `);
      this.markersLayer.addLayer(marker);
    }

    if (this.map) {
      this.map.invalidateSize();
    }
  }

  toggleCalor(): void {
    this.mostrarCalor = !this.mostrarCalor;
    if (!this.map || !this.heatLayer) return;

    if (this.mostrarCalor) {
      this.map.addLayer(this.heatLayer);
    } else {
      this.map.removeLayer(this.heatLayer);
    }
  }

  toggleSedes(): void {
    this.mostrarSedes = !this.mostrarSedes;
    if (!this.map || !this.markersLayer) return;

    if (this.mostrarSedes) {
      this.map.addLayer(this.markersLayer);
    } else {
      this.map.removeLayer(this.markersLayer);
    }
  }
}
