import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login';
import { CatalogosComponent } from './features/catalogos/catalogos';
import { GruposComponent } from './features/grupos/grupos';
// Si usaste el alias del tsconfig, la importación se vería así:
// import { LoginComponent } from '@features/auth/login/login.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'catalogos', component: CatalogosComponent },
  {path: 'grupos', component:GruposComponent}
];
