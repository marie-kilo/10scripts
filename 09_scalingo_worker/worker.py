"""Un worker en production qui surveille la latence d'une API publique.

- En local : python3 worker.py.
- Sur Scalingo : le Procfile le lance, les prints partent dans les logs de l'app.
- Quand il se termine, Scalingo le relance :
    - il faut penser à passer le worker à 0 conteneur quand la surveillance ne sert plus.
"""

import os
import time

import requests

URL = "https://geo.api.gouv.fr/departements/69/communes"
ITERATIONS = int(os.environ.get("ITERATIONS", "5"))
INTERVALLE = int(os.environ.get("INTERVALLE", "10"))

for i in range(ITERATIONS):
    debut = time.perf_counter()
    r = requests.get(URL, timeout=30)
    ms = (time.perf_counter() - debut) * 1000
    # flush : sans lui, les logs Scalingo peuvent arriver par paquets tardifs
    print(f"[{i + 1}/{ITERATIONS}] {r.status_code} en {ms:.0f} ms", flush=True)
    time.sleep(INTERVALLE)

print("mesures terminées", flush=True)
