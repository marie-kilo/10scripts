"""Écrire un DataFrame en base.

- On recommende de typer la table AVANT !!!!
- Puis, to_sql ne fait qu'ajouter. Laisser to_sql créer la table donne des types devinés (TEXT partout ou pire).
- On déclare le DDL soi-même, puis on insère avec if_exists="append".
"""

import os

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv("../01_environnement/.env")  # charge .env s'il existe et ne touche jamais aux variables déjà définies

url = os.environ.get("DATABASE_URL", "postgresql://localhost/megabase0")
engine = create_engine(url.replace("postgres://", "postgresql://", 1))

df = pd.DataFrame(
    {
        "insee_code": ["69123", "59350", "75056"],
        "pharmacies_10k_hab": [3.04, 3.23, 4.15],
    }
)

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS demo_indicateurs"))
    conn.execute(
        text(
            """
            CREATE TABLE demo_indicateurs (
                insee_code TEXT PRIMARY KEY,
                pharmacies_10k_hab NUMERIC(6, 2) NOT NULL
            )
            """
        )
    )

df.to_sql("demo_indicateurs", engine, if_exists="append", index=False)

print(pd.read_sql("SELECT * FROM demo_indicateurs ORDER BY insee_code", engine))
