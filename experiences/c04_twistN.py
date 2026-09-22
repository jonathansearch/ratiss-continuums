#!/usr/bin/env python3
"""C04 : TWIST À N PUITS (extension TEST-79/80/85 : 1->1, 2->-2, 3->0).
Appareil identique : anneau NQ=24 + hubs, K=3, DT=0.3, T=300,
graines 55/100, gaussiennes s=0.5. N puits réguliers, N=1..6,
G0 dans {0, 0.5, 1.0}. Question : twist(N) ? Zéro verdict.
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NQ, KQ, DTQ, T = 24, 3.0, 0.3, 300
OMEGA = np.random.default_rng(55).normal(0, 0.2, NQ)
adj = np.zeros((NQ, NQ))
for i in range(NQ):
    adj[i, (i - 1) % NQ] = adj[i, (i + 1) % NQ] = 1.0
adj[0, :] = adj[:, 0] = 1.0
adj[12, :] = adj[:, 12] = 1.0
np.fill_diagonal(adj, 0.0)
ANG = np.linspace(0, 2 * np.pi, NQ, endpoint=False)


def dist(a, c):
    return np.abs(((a - c + np.pi) % (2 * np.pi)) - np.pi)


def run(n, G0):
    PROF = sum(np.exp(-dist(ANG, k * 2 * np.pi / n) ** 2 / (2 * 0.5 ** 2))
               for k in range(n))
    th = np.random.default_rng(100).uniform(0, 2 * np.pi, NQ)
    om = OMEGA - G0 * PROF
    R = []
    for _ in range(T):
        th = th + DTQ * (om + (KQ / NQ) *
                         (adj * np.sin(th[None, :] - th[:, None])).sum(1))
        R.append(float(np.abs(np.exp(1j * th).mean())))
    dth = np.angle(np.exp(1j * (np.roll(th, -1) - th)))
    return {"n": n, "G0": G0,
            "R_final": round(float(np.mean(R[-50:])), 4),
            "twist": round(float(dth.sum() / (2 * np.pi)), 3)}


lignes = []
for n in (1, 2, 3, 4, 5, 6):
    for G0 in (0, 0.5, 1.0):
        r = run(n, G0)
        lignes.append(r)
        print(f"[c04] n={n} G0={G0} : R={r['R_final']} twist={r['twist']}",
              flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "..", "resultats", "c04.json"), "w"),
          indent=1)
print("[c04] archivé.")
