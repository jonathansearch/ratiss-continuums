#!/usr/bin/env python3
"""C09 : SEUIL DE COHÉRENCE COLLECTIVE À N FINI (sonde horizon-conscience,
quantitative seule — aucun claim). Kuramoto champ moyen : N oscillateurs,
K=3.0, spread sigma=0.2 fixes (valeurs focales), T=600, DT=0.1, 5 graines.
R_final(N) = moy. 100 derniers pas. Question : existe-t-il N_c où la
synchronisation s'effondre (fluctuations ~ 1/sqrt(N)) ? Zéro verdict.
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NS = (4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256)
KS, SIG, T, DT = (3.0, 0.35), 0.2, 600, 0.1


def run(n, seed, K):
    rng = np.random.default_rng(seed)
    om = rng.normal(0, SIG, n)
    th = rng.uniform(0, 2 * np.pi, n)
    R = []
    for _ in range(T):
        th = th + DT * (om + (K / n) *
                        np.sin(th[None, :] - th[:, None]).sum(1))
        R.append(float(np.abs(np.exp(1j * th).mean())))
    return round(float(np.mean(R[-100:])), 4)


lignes = []
for K in KS:
    for n in NS:
        rs = [run(n, 900 + s, K) for s in range(5)]
        lignes.append({"K": K, "n": n, "R_moy": round(float(np.mean(rs)), 4),
                       "R_min": round(float(min(rs)), 4),
                       "R_max": round(float(max(rs)), 4)})
        print(f"[c09] K={K} n={n} : R={lignes[-1]['R_moy']} "
              f"[{lignes[-1]['R_min']},{lignes[-1]['R_max']}]", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "..", "resultats", "c09.json"), "w"),
          indent=1)
print("[c09] archivé.")
