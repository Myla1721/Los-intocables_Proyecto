USE GestionCursosBD

CREATE USER 'USER'@'localhost' IDENTIFIED BY 'PASSWORD';
GRANT ALL PRIVILEGES ON GestionCursosBD.* TO 'USER'@'localhost';
FLUSH PRIVILEGES;

-- Usuarios
INSERT INTO Usuario (nombre, apellido, correo, contrasena, rol, fecha_registro, sesion_activa, ultimo_acceso) VALUES
('Juan', 'Pérez', 'juan54@correo.com', 'you345', 'ALUMNO', NOW(), FALSE, NULL),
('Maria', 'Lopez', 'maria_lopez@correo.com', 'abc123', 'ADMIN', NOW(), FALSE, NULL),
('Carlos', 'Ruiz', 'charlier45@correo.com', 'MPyAlqm1990', 'PROFESOR', NOW(), FALSE, NULL),
('Ana', 'Gomez', 'angom33@correo.com', 'gomgom3344', 'ALUMNO', NOW(), FALSE, NULL),
('Luis', 'Martinez', 'luismar56@correo.com', '654marluis', 'PROFESOR', NOW(), FALSE, NULL);

-- Profesores
INSERT INTO Profesor (id_usuario, especialidad, departamento, fecha_contratacion) VALUES
(3, 'Inglés Avanzado', 'Idiomas', '2023-08-15'),
(5, 'Gramática Inglesa', 'Idiomas', '2024-01-10');

-- Alumnos
INSERT INTO Alumno (id_usuario, matricula, nivel_idioma, fecha_inscripcion_plataforma) VALUES
(1, 'A2026001', 'A2', '2026-01-15'),
(4, 'A2026002', 'B1', '2026-02-20');

-- Administrador
INSERT INTO Administrador (id_usuario, nivel_acceso, ultimo_acceso, permisos_especiales) VALUES
(2, 10, NOW(), '{"gestion_usuarios": true, "gestion_cursos": true}');

-- Cursos
INSERT INTO Curso (nombre, descripcion, categoria, id_profesor) VALUES
('Inglés Básico', 'Curso introductorio de inglés', 'Idioma', 1),
('Inglés Intermedio', 'Curso de nivel intermedio', 'Idioma', 2);

-- Materiales
INSERT INTO Material (nombre, archivo_url, id_curso) VALUES
('Guía Unidad 1', '/materiales/guia1.pdf', 1),
('Ejercicios Básicos', '/materiales/ejercicios1.pdf', 1),
('Lectura Intermedia', '/materiales/lectura2.pdf', 2);

-- Inscripciones
INSERT INTO Inscripcion (id_alumno, id_curso) VALUES
(1, 1),
(1, 2),
(2, 1);
