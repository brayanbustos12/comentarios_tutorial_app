import { CommonModule } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { finalize } from 'rxjs';

import { Comentario } from './modelos/comentario';
import { Tutorial, TutorialCrear } from './modelos/tutorial';
import { ApiService } from './servicios/api.service';

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App implements OnInit {
  private readonly api = inject(ApiService);

  readonly tutoriales = signal<Tutorial[]>([]);
  readonly comentarios = signal<Comentario[]>([]);
  readonly tutorialSeleccionado = signal<Tutorial | null>(null);
  readonly mensajeError = signal('');
  readonly cargandoTutoriales = signal(false);
  readonly cargandoComentarios = signal(false);

  nuevoTutorial = {
    titulo: '',
    descripcion: '',
    fecha_publicacion: '',
  };

  nuevoComentario = '';

  ngOnInit(): void {
    this.cargarTutoriales();
  }

  cargarTutoriales(): void {
    this.cargandoTutoriales.set(true);

    this.api
      .listarTutoriales()
      .pipe(finalize(() => this.cargandoTutoriales.set(false)))
      .subscribe({
        next: (tutoriales) => {
          this.tutoriales.set(tutoriales);
          this.mensajeError.set('');

          if (tutoriales.length > 0 && !this.tutorialSeleccionado()) {
            this.seleccionarTutorial(tutoriales[0]);
          }
        },
        error: () => {
          this.mensajeError.set('No fue posible cargar los tutoriales.');
        },
      });
  }

  crearTutorial(): void {
    if (
      !this.nuevoTutorial.titulo.trim() ||
      !this.nuevoTutorial.descripcion.trim() ||
      !this.nuevoTutorial.fecha_publicacion
    ) {
      this.mensajeError.set('Completa todos los campos del tutorial.');
      return;
    }

    const datos: TutorialCrear = {
      titulo: this.nuevoTutorial.titulo.trim(),
      descripcion: this.nuevoTutorial.descripcion.trim(),
      fecha_publicacion: new Date(
        this.nuevoTutorial.fecha_publicacion,
      ).toISOString(),
    };

    this.api.crearTutorial(datos).subscribe({
      next: (tutorial) => {
        this.tutoriales.update((tutoriales) => [tutorial, ...tutoriales]);
        this.nuevoTutorial = {
          titulo: '',
          descripcion: '',
          fecha_publicacion: '',
        };
        this.mensajeError.set('');
        this.seleccionarTutorial(tutorial);
      },
      error: () => {
        this.mensajeError.set('No fue posible registrar el tutorial.');
      },
    });
  }

  seleccionarTutorial(tutorial: Tutorial): void {
    this.tutorialSeleccionado.set(tutorial);
    this.comentarios.set([]);
    this.cargarComentarios(tutorial.id);
  }

  cargarComentarios(tutorialId: number): void {
    this.cargandoComentarios.set(true);

    this.api
      .listarComentarios(tutorialId)
      .pipe(finalize(() => this.cargandoComentarios.set(false)))
      .subscribe({
        next: (comentarios) => {
          this.comentarios.set(comentarios);
          this.mensajeError.set('');
        },
        error: () => {
          this.mensajeError.set('No fue posible cargar los comentarios.');
        },
      });
  }

  crearComentario(): void {
    const contenido = this.nuevoComentario.trim();
    const tutorial = this.tutorialSeleccionado();

    if (!tutorial || !contenido) {
      return;
    }

    this.api.crearComentario(tutorial.id, { contenido }).subscribe({
      next: (comentario) => {
        this.comentarios.update((comentarios) => [
          ...comentarios,
          comentario,
        ]);
        this.nuevoComentario = '';
        this.mensajeError.set('');
      },
      error: () => {
        this.mensajeError.set('No fue posible registrar el comentario.');
      },
    });
  }

  editarComentario(comentario: Comentario): void {
    const contenido = window.prompt(
      'Nuevo contenido del comentario:',
      comentario.contenido,
    );

    if (contenido === null || !contenido.trim()) {
      return;
    }

    this.api
      .actualizarComentario(comentario.id, { contenido: contenido.trim() })
      .subscribe({
        next: (actualizado) => {
          this.comentarios.update((comentarios) =>
            comentarios.map((item) =>
              item.id === actualizado.id ? actualizado : item,
            ),
          );
          this.mensajeError.set('');
        },
        error: () => {
          this.mensajeError.set('No fue posible modificar el comentario.');
        },
      });
  }

  eliminarComentario(comentario: Comentario): void {
    const confirmado = window.confirm('¿Deseas eliminar este comentario?');

    if (!confirmado) {
      return;
    }

    this.api.eliminarComentario(comentario.id).subscribe({
      next: () => {
        this.comentarios.update((comentarios) =>
          comentarios.filter((item) => item.id !== comentario.id),
        );
        this.mensajeError.set('');
      },
      error: () => {
        this.mensajeError.set('No fue posible eliminar el comentario.');
      },
    });
  }
}
