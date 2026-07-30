"""Créer une base relationnelle depuis Python, et tester la clef étrangère."""

import os
import pathlib

import dotenv
import psycopg2
from dotenv import load_dotenv


load_dotenv("../01_environnement/.env")

conn = psycopg2.connect(os.environ.get("DB_URL", "dbname=megabase0"))
cur = conn.cursor()

cur.execute(pathlib.Path("schema.sql").read_text())
cur.execute("INSERT INTO demo.departement VALUES ('69', 'Rhône'), ('59', 'Nord')")
cur.executemany(
    "INSERT INTO demo.commune VALUES (%s, %s, %s, %s)",
    [("69123", "Lyon", 522250, "69"), ("59350", "Lille", 236234, "59")],
)
conn.commit()

# la FK refuse l'orphelin : le département 99 n'existe pas
try:
    cur.execute("INSERT INTO demo.commune VALUES ('99999', 'Nulle-Part', 0, '99')")
except psycopg2.errors.ForeignKeyViolation as e:
    conn.rollback()
    print("insertion refusée par la clé étrangère :", str(e).splitlines()[0])

cur.execute(
    """
    SELECT c.name, d.name, c.population
    FROM demo.commune c
    JOIN demo.departement d ON d.code_departement = c.code_departement
    ORDER BY c.population DESC
    """
)
for ligne in cur.fetchall():
    print(ligne)
conn.close()
