import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth-guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { 
    path: 'login', 
    loadComponent: () => import('./features/auth/login/login').then(m => m.LoginComponent) 
  },
  {
    path: '',
    canActivate: [authGuard],
    children: [
      { 
        path: 'dashboard', 
        loadComponent: () => import('./features/dashboard/dashboard').then(m => m.DashboardComponent) 
      },
      { 
        path: 'catalogos', 
        loadComponent: () => import('./features/catalogos/catalogos').then(m => m.CatalogosComponent) 
      },
      { 
        path: 'grupos', 
        loadComponent: () => import('./features/grupos/grupos').then(m => m.GruposComponent) 
      },
      { 
        path: 'sesiones', 
        loadComponent: () => import('./features/sesiones/sesiones').then(m => m.SesionesComponent) 
      },
      { 
        path: 'agresores', 
        loadComponent: () => import('./features/agresores/agresores').then(m => m.AgresoresComponent) 
      },
      { 
        path: 'listas', 
        loadComponent: () => import('./features/lista-asistencia/lista-asistencia').then(m => m.ListasComponent) 
      }
    ]
  },
  { path: '**', redirectTo: 'login' }
];
