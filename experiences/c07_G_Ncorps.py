#!/usr/bin/env python3
"""C07 : GRAVITÉ INFORMATIONNELLE À N CORPS (extension TEST-48/49).
N tores 160 pts (fond, graine 24+k), etape focale (al=0.1, sg=0.005) +
couplage inter-tores : chaque tore attiré vers le centroïde GLOBAL
(c=0.005, assumé minimal). T=1500. G(N) = moy. p_sig/PREF_k sur les
200 derniers pas (échantillonné /50). Contrôle c=0. N dans {1,2,4,8}.
Question : G extensif, saturant, ou rompant avec N ? Zéro verdict.
"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

T = 1500


def run(n, c):
    rng = np.random.default_rng(42)
    tores = [C.fond(seed=24 + k)[:160].copy() for k in range(n)]
    prefs = [C.p_sig(g) for g in tores]
    hist = []
    for t in range(T):
        for i in range(n):
            g = tores[i]
            d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
            g = g + 0.1 * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
            tores[i] = g + rng.normal(0, 0.005, g.shape)
        if c > 0 and n > 1:
            G = np.mean(tores, axis=(0, 1))
            for i in range(n):
                tores[i] = tores[i] + c * (G - tores[i])
        if (t + 1) % 50 == 0:
            hist.append([round(float(C.p_sig(tores[i]) / prefs[i]), 4)
                         for i in range(n)])
    fin = np.array(hist[-4:]).mean()
    return {"n": n, "couplage": c, "G_final": round(float(fin), 4),
            "trace_moy": [round(float(np.mean(h)), 4) for h in hist]}


lignes = []
for n in (1, 2, 4, 8):
    for c in ((0.0,) if n == 1 else (0.005, 0.001, 0.0)):
        r = run(n, c)
        lignes.append(r)
        print(f"[c07] n={n} c={c} : G={r['G_final']}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "..", "resultats", "c07.json"), "w"),
          indent=1)
print("[c07] archivé.")
