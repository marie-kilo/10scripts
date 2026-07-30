"""Charger beaucoup de lignes : executemany contre COPY, temps d'exécution mesurés.

- Le coût dominant est l'aller-retour par instruction.
- COPY envoie un seul flux.
"""

import io
import os
import time

import psycopg2

from dotenv import load_dotenv


load_dotenv("../01_environnement/.env")

conn = psycopg2.connect(os.environ.get("DB_URL", "dbname=megabase0"))
cur = conn.cursor()
cur.execute("CREATE TEMP TABLE mesure (id INTEGER, valeur TEXT)")

t = time.perf_counter()
cur.executemany("INSERT INTO mesure VALUES (%s, %s)", [(i, f"v{i}") for i in range(10_000)])
print(f"executemany :  10 000 lignes en {time.perf_counter() - t:.2f} s")

flux = io.StringIO("".join(f"{i}\tv{i}\n" for i in range(100_000)))
t = time.perf_counter()
cur.copy_expert("COPY mesure FROM STDIN", flux)
print(f"COPY        : 100 000 lignes en {time.perf_counter() - t:.2f} s")

cur.execute("SELECT count(*) FROM mesure")
print("lignes en table :", cur.fetchone()[0])
conn.rollback()
