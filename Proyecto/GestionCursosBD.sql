DROP DATABASE IF EXISTS GestionCursosBD;
CREATE DATABASE GestionCursosBD;
USE GestionCursosBD;

-- Tabla Usuario
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('ADMIN','PROFESOR','ALUMNO') NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    sesion_activa BOOLEAN DEFAULT FALSE,
    ultimo_acceso DATETIME
);

-- Tabla Profesor
CREATE TABLE Profesor (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    especialidad VARCHAR(100),
    departamento VARCHAR(100),
    fecha_contratacion DATE,

    CONSTRAINT fk_profesor_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
    ON DELETE CASCADE
);


-- Tabla Alumno
CREATE TABLE Alumno (
    id_alumno INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    matricula VARCHAR(50) UNIQUE,
    nivel_idioma ENUM('A1','A2','B1','B2','C1','C2'),
    fecha_inscripcion_plataforma DATE,

    CONSTRAINT fk_alumno_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
    ON DELETE CASCADE
);

-- Tabla Administrador
CREATE TABLE Administrador (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    nivel_acceso INT,
    ultimo_acceso DATETIME,
    permisos_especiales JSON,

    CONSTRAINT fk_admin_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuario(id_usuario)
    ON DELETE CASCADE
);

-- Tabla Curso
CREATE TABLE Curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100),
    id_profesor INT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_curso_profesor
    FOREIGN KEY (id_profesor)
    REFERENCES Profesor(id_profesor)
    ON DELETE CASCADE
);

-- Tabla material
CREATE TABLE Material (
    id_material INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    archivo_url TEXT NOT NULL,
    id_curso INT NOT NULL,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_material_curso
    FOREIGN KEY (id_curso)
    REFERENCES Curso(id_curso)
    ON DELETE CASCADE
);

-- Tabla Inscripción
CREATE TABLE Inscripcion (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_alumno INT NOT NULL,
    id_curso INT NOT NULL,
    fecha_inscripcion DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_inscripcion_alumno
    FOREIGN KEY (id_alumno)
    REFERENCES Alumno(id_alumno)
    ON DELETE CASCADE,

    CONSTRAINT fk_inscripcion_curso
    FOREIGN KEY (id_curso)
    REFERENCES Curso(id_curso)
    ON DELETE CASCADE,

    CONSTRAINT unique_inscripcion UNIQUE (id_alumno, id_curso)
);

CREATE USER 'intocable'@'localhost' IDENTIFIED BY 'Ing2026!';
GRANT ALL PRIVILEGES ON GestionCursosBD.* TO 'intocable'@'localhost';
FLUSH PRIVILEGES;

INSERT INTO Usuario (nombre, apellido, correo, contrasena, rol, fecha_registro, sesion_activa, ultimo_acceso) VALUES
('Juan', 'Pérez', 'juan54@correo.com', 'you345', 'ALUMNO', NOW(), FALSE, NULL),
('Maria', 'Lopez', 'maria_lopez@correo.com', 'abc123', 'ADMIN', NOW(), FALSE, NULL),
('Carlos', 'Ruiz', 'charlier45@correo.com', 'MPyAlqm1990', 'PROFESOR', NOW(), FALSE, NULL),
('Ana', 'Gomez', 'angom33@correo.com', 'gomgom3344', 'ALUMNO', NOW(), FALSE, NULL),
('Luis', 'Martinez', 'luismar56@correo.com', '654marluis', 'PROFESOR', NOW(), FALSE, NULL);