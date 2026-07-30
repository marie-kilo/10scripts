"""Le moniteur du 09, mais les mesures sont stockées : un vrai historique en base.

En local, il écrit dans megabase0 ; sur Scalingo, dans la base de l'addon via
DATABASE_URL. Même code partout.
"""

import os
import time

import psycopg2
import requests

URL = "https://geo.api.gouv.fr/departements/69/communes"

conn = psycopg2.connect(os.environ.get("DATABASE_URL", "dbname=megabase0"))
conn.autocommit = True  # chaque mesure est gardée, même si le worker est coupé
cur = conn.cursor()
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS demo_latence_api (
        id        SERIAL PRIMARY KEY,
        status    INTEGER NOT NULL,
        ms        NUMERIC(8, 1) NOT NULL,
        mesure_le TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """
)

for _ in range(int(os.environ.get("ITERATIONS", "5"))):
    debut = time.perf_counter()
    r = requests.get(URL, timeout=30)
    ms = round((time.perf_counter() - debut) * 1000, 1)
    cur.execute("INSERT INTO demo_latence_api (status, ms) VALUES (%s, %s)", (r.status_code, ms))
    print(f"{r.status_code} en {ms} ms, stocké", flush=True)
    time.sleep(int(os.environ.get("INTERVALLE", "10")))

cur.execute("SELECT count(*), round(avg(ms), 1) FROM demo_latence_api")
total, moyenne = cur.fetchone()
print(f"historique : {total} mesures, latence moyenne {moyenne} ms", flush=True)
conn.close()
