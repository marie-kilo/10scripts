-- Volumétrie puis agrégats territoriaux
-- (brief 04, étapes 1 et 2)
--
--     psql -d megabase0 -f requetes.sql

-- 1. Volumétrie : se repérer avant d'analyser
SELECT 'communes' AS source, count(*) AS n FROM commune
UNION ALL SELECT 'pharmacies', count(*) FROM pharmacie
UNION ALL SELECT 'lycees', count(*) FROM lycee
ORDER BY n DESC;

-- 2. Communes par département, avec la région
SELECT r.name AS region, d.name AS departement, count(*) AS communes
FROM commune c
JOIN departement d ON d.code_departement = c.code_departement
JOIN region r      ON r.code_region = d.code_region
GROUP BY r.name, d.name
ORDER BY communes DESC
LIMIT 10;

-- 3. Population par département
SELECT d.name AS departement, sum(c.population) AS population
FROM commune c
JOIN departement d ON d.code_departement = c.code_departement
GROUP BY d.name
ORDER BY population DESC
LIMIT 10;

-- 4. Classement des départements par pharmacies
SELECT d.name AS departement, count(*) AS pharmacies
FROM pharmacie p
JOIN commune c     ON c.insee_code = p.insee_code
JOIN departement d ON d.code_departement = c.code_departement
GROUP BY d.name
ORDER BY pharmacies DESC
LIMIT 10;

-- 5. Moyenne de pharmacies par commune, par département
-- count(p.finess) ne compte que les pharmacies, count(DISTINCT ...) les communes
SELECT d.name AS departement,
       round(count(p.finess)::numeric / count(DISTINCT c.insee_code), 2)
           AS pharmacies_par_commune
FROM departement d
JOIN commune c        ON c.code_departement = d.code_departement
LEFT JOIN pharmacie p ON p.insee_code = c.insee_code
GROUP BY d.name
ORDER BY pharmacies_par_commune DESC
LIMIT 10;
