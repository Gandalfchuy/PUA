import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  
  // Como ya no hay SSR, siempre estamos en el navegador
  const token = localStorage.getItem('pua_token'); 

  if (token) {
    return true; 
  } else {
    // Si no hay token, lo redirigimos al login
    return router.createUrlTree(['/login']); 
  }
};