export interface Usuario{
    id: number;
    rol_id: number;
}
export interface AuditBase{
    created_at: string;
    updated_at?: string;
    deleted_at?: string;
    is_deleted?: boolean;
    created_by?: number;
    updated_by?: number;
    deleted_by?: number;
}

export interface UbicacionGeografica {
  latitud: number;
  longitud: number;
}



export interface Catalogo{
    nombre: string;
    activo?: boolean;
}

export interface CatalogoItem extends Catalogo, AuditBase{
    id: number;
}

export interface Grupo{
    ubicacion:UbicacionGeografica
    lugar:string;
    activo?:boolean 
}

export interface GrupoItem extends Grupo, AuditBase{
    folio:number;
}

export interface Sesion{
  nombre: string;
  objetivo: string;
}

export interface SesionItem  extends Sesion, AuditBase{
folio:number;
}

export interface AgresorBase{
  curp: string;
  nombre: string;
  apellido_paterno: string;
  apellido_materno: string;
  edad: number;
  
  lugar_nacimiento: UbicacionGeografica;
  lugar_residencia: UbicacionGeografica;
  lugar_trabajo: UbicacionGeografica;
  
  parejas_previas: number;
  hijos: number;
  hermanos: number;
}

export interface Agresor extends AgresorBase{
  estado_civil_id?: number | null;
  situacion_academica_id?: number | null;
  situacion_laboral_id?: number | null;
  situacion_vivienda_id?: number | null;
  rango_salarial_id?: number | null;
  religion_id?: number | null;
  relacion_hijos_id?: number | null;
  
  sectores_sociales_ids?: number[];
  actividades_recreativas_ids?: number[];
  adicciones_ids?: number[];
  generos_musicales_ids?: number[];
  relacion_hermanos_ids?: number[];
  relacion_padre_ids?: number[];
  relacion_madre_ids?: number[];
  violencia_infantil_ids?: number[];
}


export interface AgresorItem extends AgresorBase, AuditBase{
  folio: number;
  estado_civil: CatalogoItem
  situacion_academica: CatalogoItem
  situacion_laboral: CatalogoItem
  situacion_vivienda: CatalogoItem
  rango_salarial: CatalogoItem
  religion: CatalogoItem
  relacion_hijos: CatalogoItem
  
  sectores_sociales: CatalogoItem[];
  actividades_recreativas: CatalogoItem[];
  adicciones: CatalogoItem[];
  generos_musicales: CatalogoItem[];
  relacion_hermanos: CatalogoItem[];
  relacion_padre: CatalogoItem[];
  relacion_madre: CatalogoItem[];
  violencia_infantil: CatalogoItem[];

  proceso_reeducacion?:ProcesoReeducacionItem[] | [];
}

export interface ProcesoReeducacionBase{
    fecha_inicio: string;
    fecha_termino?: string | null;
    fecha_denuncia?: string | null;
    denunciante: string;
    folio_carpeta_fiscalia:string;
}

export interface ProcesoReeducacion extends ProcesoReeducacionBase{
    agresor_id: number;
    motivo_ingreso_id: number;
    tipo_violencia_id:number;
    modalidad_violencia_id:number;
}

export interface ProcesoReeducacionItem extends ProcesoReeducacionBase, AuditBase{
    folio:number;
    agresor:AgresorItem;
    motivo_ingreso: CatalogoItem;
    tipo_violencia:CatalogoItem;
    modalidad_violencia:CatalogoItem;
}

export interface ListaBase{
    fecha:string | null;
}

export interface Lista extends ListaBase{
    agresor_id: number;
    grupo_id: number;
    sesion_id: number;
}

export interface ListaItem extends ListaBase, AuditBase{
    id:number;
    agresor: AgresorItem;
    grupo: GrupoItem;
    sesion: SesionItem;
}