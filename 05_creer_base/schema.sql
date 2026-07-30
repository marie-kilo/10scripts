-- Géographie minimale à deux niveaux : le schéma doit vivre dans un .sql versionné :
-- on peut ainsi le relire, le relancer, le passer en revue, contrairement à du code enfoui dans un script .py
DROP SCHEMA IF EXISTS demo CASCADE;
CREATE SCHEMA demo;

CREATE TABLE demo.departement (
    code_departement TEXT PRIMARY KEY,
    name             TEXT NOT NULL
);

CREATE TABLE demo.commune (
    insee_code       TEXT PRIMARY KEY,
    name             TEXT NOT NULL,
    population       INTEGER,
    code_departement TEXT NOT NULL REFERENCES demo.departement
);
