"""Configuration d'un projet data : .env en local, variables d'environnement en prod.

Le même code lit sa connexion partout : load_dotenv charge .env s'il existe
et ne touche jamais aux variables déjà définies (celles de Scalingo gagnent).
"""

import os

from dotenv import load_dotenv

# cherche un .env dans le working directory
# il sera trouvé en local, mais pas en production
# et donc lcoalement, on charge la variable DATABASE_URL spécifiée dans le .env
load_dotenv()

# La variable DATABASE_URL existe déjà dans l'environnement en production
# et on vient de la charger localement
# et on a ajouté une valeur par défaut
DB_URL = os.environ.get("DATABASE_URL", "dbname=megabase0")

if __name__ == "__main__":
    # jamais l'URL complète dans un terminal : elle peut contenir un mot de passe
    cible = DB_URL.rsplit("@", 1)[-1] if "@" in DB_URL else DB_URL
    print(f"connexion cible : {cible}")
