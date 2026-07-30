"""Les comptes du quotidien : combien, par groupe, trié."""

import pandas as pd

# dtype force le code INSEE en texte: sinon 2A004 casse et 01001 perd son zéro
df = pd.read_csv("communes.csv", dtype={"insee_code": str})

print(df.shape)
print()
print(df["departement"].value_counts())
print()
print(
    df.groupby("departement", as_index=False)["population"]
    .sum()
    .sort_values("population", ascending=False)
)
print()
print("plus de 100 000 habitants :", df[df["population"] > 100_000]["commune"].tolist())
