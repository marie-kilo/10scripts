"""Collecte paginée et relançable.

- L'état vit dans la base, pas dans un fichier :
    - le NOMBRE de lignes déjà chargées pour un département donne l'offset de reprise
    - un département complet ne recharge rien, un département interrompu reprend à sa page
- Chaque page est validée (commit) et insérée en ON CONFLICT DO NOTHING : rien n'est dupliqué.

    # crontab -e : tous les jours à 6 h
    0 6 * * * cd /chemin/du/projet && env/bin/python collecte.py
"""

import os

import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv("../01_environnement/.env")

URL = (
    "https://data.education.gouv.fr/api/explore/v2.1"
    "/catalog/datasets/fr-en-annuaire-education/records"
)
DEPTS = ["069", "059"]  # l'annuaire code les départements sur 3 caractères
PAGE = 100  # rappel Opendatasoft: offset + limit doit rester sous 10_000

conn = psycopg2.connect(os.environ.get("DB_URL", "dbname=megabase0"))
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS demo_lycee_cron (
    uai TEXT PRIMARY KEY, name TEXT NOT NULL, commune TEXT, dept TEXT NOT NULL)""")
conn.commit()

for dept in DEPTS:
    cur.execute("SELECT count(*) FROM demo_lycee_cron WHERE dept = %s", (dept,))
    offset = cur.fetchone()[0]
    print(f"{dept} : {offset} lignes déjà en base, reprise à offset={offset}")
    while True:
        r = requests.get(
            URL,
            params={
                "where": f'code_departement="{dept}" and type_etablissement="Lycée"',
                "select": "identifiant_de_l_etablissement,nom_etablissement,nom_commune",
                "order_by": "identifiant_de_l_etablissement",  # sans tri, pages instables !
                "limit": PAGE,
                "offset": offset,
            },
            timeout=30,
        )
        r.raise_for_status()
        lignes = [
            (x["identifiant_de_l_etablissement"], x["nom_etablissement"], x["nom_commune"], dept)
            for x in r.json()["results"]
        ]
        if not lignes:
            break
        cur.executemany(
            "INSERT INTO demo_lycee_cron VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING", lignes
        )
        conn.commit()  # la page est enregistrée!!(même si la suivante échoue)
        offset += PAGE
    cur.execute("SELECT count(*) FROM demo_lycee_cron WHERE dept = %s", (dept,))
    print(f"{dept} : {cur.fetchone()[0]} lignes en base")
conn.close()
