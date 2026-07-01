import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
// 1. Importa withFetch de @angular/common/http
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http'; 
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    // 2. Agrégalo como parámetro aquí adentro 👇
    provideHttpClient(withFetch(), withInterceptors([])) 
  ]
};
