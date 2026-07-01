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
export interface Catalogo{
    nombre: string;
    activo?: boolean;
}

export interface CatalogoItem extends Catalogo, AuditBase{
    id: number;
}

export interface Grupo{
    ubicacion:{
        latitud:number,
        longitud:number
    };
    lugar:string;
    activo?:boolean 
}

export interface GrupoItem extends Grupo, AuditBase{
    folio:number;
}
