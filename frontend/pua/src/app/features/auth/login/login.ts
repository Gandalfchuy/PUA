import { Component, inject, ChangeDetectorRef } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth';
import { ModalComponent } from '../../../shared/components/modal/modal';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, ModalComponent],
  templateUrl: './login.html'
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private cd = inject(ChangeDetectorRef);

  cargando = false;
  mostrarModal = false;
  tipoModal: 'exito' | 'error' = 'error';
  tituloModal = '';
  mensajeModal = '';

  loginForm: FormGroup = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required]
  });

  ingresar() {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.cargando = true;
    const { email, password } = this.loginForm.value;

    this.authService.login(email, password).subscribe({
      next: (respuesta) => {
        this.cargando = false;
        
        // Configuramos el modal de éxito
        this.tipoModal = 'exito';
        this.tituloModal = 'Acceso Autorizado';
        this.mensajeModal = 'Credenciales correctas. Ingresando al sistema...';
        this.mostrarModal = true;
        
        this.cd.markForCheck();
        
        // Aquí redirigirás al dashboard
        console.log('¡Bienvenido! Redirigiendo...', respuesta);
      },
      error: (err) => {
        this.cargando = false;
        
        // Configuramos el modal de error
        this.tipoModal = 'error';
        this.tituloModal = 'Error de Autenticación';
        
        // Si FastAPI devuelve un error 401 o 400
        if (err.status === 401 || err.status === 400) {
          this.mensajeModal = 'El correo institucional o la contraseña son incorrectos.';
        } else {
          this.mensajeModal = 'Error de conexión con el servidor. Intenta más tarde.';
        }
        
        this.mostrarModal = true;
        this.cd.markForCheck();
        console.error(err);
      }
    });
  }

  cerrarModal() {
    this.mostrarModal = false;
    this.cd.markForCheck();
  }
}