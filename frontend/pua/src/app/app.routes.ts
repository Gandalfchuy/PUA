import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login';
import { CatalogosComponent } from './features/catalogos/catalogos';
import { GruposComponent } from './features/grupos/grupos';
import { SesionesComponent } from './features/sesiones/sesiones';
import { AgresoresComponent } from './features/agresores/agresores';
import { authGuard } from './core/guards/auth-guard';
import { ListasComponent } from './features/lista-asistencia/lista-asistencia';
// Si usaste el alias del tsconfig, la importación se vería así:
// import { LoginComponent } from '@features/auth/login/login.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
{path: '', canActivate:[authGuard],
  children:[
  { path: 'catalogos', component: CatalogosComponent },
  {path: 'grupos', component:GruposComponent},
  {path: 'sesiones',component: SesionesComponent},
  {path: 'agresores',component: AgresoresComponent},
  {path: 'listas',component: ListasComponent}
  ]
},
{ path: '**', redirectTo: 'login' }

];
