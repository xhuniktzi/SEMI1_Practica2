CREATE DATABASE IF NOT EXISTS FAUNADEX;
USE FAUNADEX;

-- Creación de la tabla Usuarios
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nickname VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    rutaFotoPerfil VARCHAR(255),
    UNIQUE (nickname)
);

-- Creación de la tabla Fotos
CREATE TABLE Fotos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion VARCHAR(255),
    rutaFoto VARCHAR(255) NOT NULL,
    usuarioId INT,
    FOREIGN KEY (usuarioId) REFERENCES Usuarios(id)
);

-- Creación de la tabla Etiquetas
CREATE TABLE Etiquetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    etiqueta VARCHAR(255) NOT NULL,
    UNIQUE (etiqueta)
);

-- Creación de la tabla intermedia FotoEtiquetas
CREATE TABLE FotoEtiquetas (
    fotoId INT,
    etiquetaId INT,
    PRIMARY KEY (fotoId, etiquetaId),
    FOREIGN KEY (fotoId) REFERENCES Fotos(id),
    FOREIGN KEY (etiquetaId) REFERENCES Etiquetas(id)
);
