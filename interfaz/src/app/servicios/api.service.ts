import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { Comentario, ComentarioGuardar } from '../modelos/comentario';
import { Tutorial, TutorialCrear } from '../modelos/tutorial';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly urlBase = 'http://127.0.0.1:8000/api/v1';

  listarTutoriales(): Observable<Tutorial[]> {
    return this.http.get<Tutorial[]>(`${this.urlBase}/tutoriales`);
  }

  crearTutorial(datos: TutorialCrear): Observable<Tutorial> {
    return this.http.post<Tutorial>(`${this.urlBase}/tutoriales`, datos);
  }

  listarComentarios(tutorialId: number): Observable<Comentario[]> {
    return this.http.get<Comentario[]>(
      `${this.urlBase}/tutoriales/${tutorialId}/comentarios`,
    );
  }

  crearComentario(
    tutorialId: number,
    datos: ComentarioGuardar,
  ): Observable<Comentario> {
    return this.http.post<Comentario>(
      `${this.urlBase}/tutoriales/${tutorialId}/comentarios`,
      datos,
    );
  }

  actualizarComentario(
    comentarioId: number,
    datos: ComentarioGuardar,
  ): Observable<Comentario> {
    return this.http.put<Comentario>(
      `${this.urlBase}/comentarios/${comentarioId}`,
      datos,
    );
  }

  eliminarComentario(comentarioId: number): Observable<void> {
    return this.http.delete<void>(
      `${this.urlBase}/comentarios/${comentarioId}`,
    );
  }
}
