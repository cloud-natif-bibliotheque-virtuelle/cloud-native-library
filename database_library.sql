DROP DATABASE IF EXISTS library;
CREATE DATABASE library;
USE library;

-- créer une table clients
DROP TABLE IF EXISTS liste_livres;
CREATE TABLE liste_livres(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT UNIQUE,
    titre VARCHAR(255),
    infos VARCHAR(255),
    url_blob VARCHAR(255),
    nombre_mot LONGTEXT
);
-- SELECT * FROM library.liste_livres;
