# 10scripts : les gestes fondateurs

## Gestes et scripts

- Dix scripts autonomes (5 à 50 lignes).
- Un par geste que le métier de data engineer implique de faire régulièrement.
- Les scripts se lancent tels quels sur `megabase0` (ou sur la base spécifiée via `DATABASE_URL`). 
- Ils couvrent le programme jusqu'aux requêtes analytiques et au déploiement, hors dbt.

| Dossier | Geste | Compétences (RNCP-37638) |
|---|---|---|
| `01_environnement` | venv, `.env`, `load_dotenv`, `DATABASE_URL` avec repli local | C16, CT1 |
| `02_pandas_comptes` | compter, grouper, trier un fichier | C10 |
| `03_pandas_lire_sql` | lire PostgreSQL dans un DataFrame | C9, C10 |
| `04_pandas_ecrire_sql` | écrire un DataFrame en base, table typée d'abord | C11 |
| `05_creer_base` | créer un schéma relationnel versionné, FK à l'appui | C11 |
| `06_copy_insertion` | charger massivement : executemany contre COPY, chronométrés | C11 |
| `07_cron_api_reprise` | collecte par groupes relançable par cron, état dans la base | C8, C15 |
| `08_requetes_sql` | volumétrie et agrégats territoriaux (brief 04, étapes 1 et 2) | C9, C10 |
| `09_scalingo_worker` | un worker en production : moniteur de latence d'API | C14 |
| `10_scalingo_worker_postgres` | le même worker, mesures stockées en base | C14, C16 |


## Prérequis

-  Exécuter le script `01_environnement` une fois (l'environnement sert à tous).
- `megabase0` chargée avec les données.


## Note 
> Les scripts qui écrivent le font dans des objets `demo_*` ou temporaires : les "vraies" tables ne sont pas modifiées.

***********

Les commandes :

- 1. créer l'environnement (env)
 ~/.pyenv/pyenv-win/versions/3.14.2/python.exe -m venv env
 env/Scripts/activate 

 pip install -r requirements.txt  

 - 2. créer fichier .env: 
 (avec psycopg2 pour sqlalchemy) :
 DATABASE_URL= postgresql+psycopg2://postgres:Mkilo1990@localhost:5432/megabase0
 (sans psycopg2 , avec psql):
DB_URL=postgresql://postgres:Mkilo1990@localhost:5432/megabase0

**** 
# pour toute les fichier (pour l'utiliser l'url)

from dotenv import load_dotenv
load_dotenv("../01_environnement/.env")

****

# Executer:
**********
01_environnement: python config.py 
02_pandas_comptes: python comptes.py  
03_pandas_lire_sql: python lire_sql.p  
04_pandas_ecrire_sql: python ecrire_sql.py    
05_creer_bases: python creer_base.py  
06_copy_insertion:  python copy_rapide.py s
07_cron_api_reprise: python collecte.py    
08_requetes_sql: $env:PATH += ";C:\Program Files\PostgreSQL\18\bin"  
                                psql -U postgres -d megabase0 -f requetes.sql 