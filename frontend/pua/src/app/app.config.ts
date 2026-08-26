import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
// 1. Importa withFetch de @angular/common/http
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http'; 
import { routes } from './app.routes';
import { authInterceptor } from './core/guards/auth-interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withFetch(), withInterceptors([authInterceptor]))
  ]
};
