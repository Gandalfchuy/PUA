export interface DashboardKpis {
  total_activos: number;
  tasa_asistencia: number;
  alertas_desercion: number;
  procesos_concluidos: number;
}

export interface PuntoCalor {
  lat: number;
  lng: number;
  peso?: number;
}

export interface SedeMapa {
  folio: number;
  lugar: string;
  lat: number;
  lng: number;
}

export interface DashboardMapa {
  puntos_calor: PuntoCalor[];
  sedes: SedeMapa[];
}

export interface TipoViolenciaStat {
  tipo: string;
  total: number;
  porcentaje: number;
}

export interface DashboardViolencia {
  tipos: TipoViolenciaStat[];
}

export interface AdiccionStat {
  adiccion: string;
  total: number;
  porcentaje: number;
}

export interface DashboardAdicciones {
  adicciones: AdiccionStat[];
}

export interface AlertaDesercionItem {
  agresor_id: number;
  curp: string;
  nombre_completo: string;
  grupo?: string | null;
  faltas_consecutivas: number;
  ultima_asistencia?: string | null;
  carpeta_fiscalia?: string | null;
}

export interface DashboardAlertas {
  alertas: AlertaDesercionItem[];
}
