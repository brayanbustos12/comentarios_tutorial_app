export interface Comentario {
  id: number;
  contenido: string;
  tutorial_id: number;
  fecha_creacion: string;
  fecha_actualizacion: string;
}

export interface ComentarioGuardar {
  contenido: string;
}
