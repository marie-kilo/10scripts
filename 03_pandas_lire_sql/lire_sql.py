"""Lire PostgreSQL dans un DataFrame."""

import os

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv("../01_environnement/.env")  # charge .env s'il existe et ne touche jamais aux variables déjà définies

url = os.environ.get("DATABASE_URL", "postgresql://localhost/megabase0")
# Scalingo fournit postgres://, SQLAlchemy exige postgresql+psycopg2://
engine = create_engine(url.replace("postgres://", "postgresql+psycopg2://", 1))

df = pd.read_sql(
    """
    SELECT d.name AS departement, count(*) AS pharmacies
    FROM pharmacie p
    JOIN commune c ON c.insee_code = p.insee_code
    JOIN departement d ON d.code_departement = c.code_departement
    GROUP BY d.name
    ORDER BY pharmacies DESC
    LIMIT 5
    """,
    engine,
)

print(df)
print()
print("total :", df["pharmacies"].sum())
