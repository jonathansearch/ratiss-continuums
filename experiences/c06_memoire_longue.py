#!/usr/bin/env python3
"""C06 : MÉMOIRE À LONG TERME (extension TEST-70/71/72, court->long).
RUQ-1 focal (12 agents, graine 7001, conteneur copié) : phase A 400 pas
GROUPÉS (barrière R>=0.85 sinon INVALIDE), séparation brusque, phase B
dispersée TB dans {100, 1000, 10000}. R(t) (sous-échantillonné /10 à
10000), t_half, fits H1 exponentielle (log R vs t) vs H2 puissance
(log R vs log t) sur R>0.05. Question : expo ou puissance ?
Zéro verdict.
"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C

N, TA = 12, 400
K, DT, GAM = 2.0, 0.3, 1.0
ALPHA, BETA = 0.05, 0.1
W = 0.05


def fit_r2(x, y):
    a, b = np.polyfit(x, y, 1)
    pred = a * np.array(x) + b
    return round(float(1 - ((y - pred) ** 2).sum() /
                       max(((y - y.mean()) ** 2).sum(), 1e-12)), 4)


def run(TB):
    rng = np.random.default_rng(7001)
    g = C.fond(seed=24)[:160].copy()

    def etape(g):
        d2 = ((g[:, None, :] - g[None, :, :]) ** 2).sum(-1)
        g = g + 0.1 * (g[np.argsort(d2, axis=1)[:, 1:6]].mean(1) - g)
        return g + rng.normal(0, 0.005, g.shape)

    bb0, bb1 = g.min(0), g.max(0)
    DIAG = float(np.linalg.norm(bb1 - bb0))
    STEP, RAYON = DIAG / 150, DIAG / 8
    X = rng.uniform(bb0, bb1, (N, 3))
    th = rng.uniform(0, 2 * np.pi, N)
    q = np.zeros(N)
    W0 = rng.normal(0, 0.2, N)
    PH = rng.uniform(0, 2 * np.pi, N)

    def densites(X, g):
        d = np.sqrt(((g[None, :, :] - X[:, None, :]) ** 2).sum(-1))
        dd = 1 / (np.sort(d, axis=1)[:, :5].mean(1) + 1e-9)
        lo, hi = dd.min(), dd.max()
        return (dd - lo) / max(hi - lo, 1e-9)

    def pas_ruq(X, th, q, g):
        s = densites(X, g)
        dmat = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
        for i in range(N):
            vois = [j for j in range(N) if j != i and dmat[i, j] < RAYON]
            if vois:
                th[i] += DT * (K / N) * float(np.sin(th[vois] - th[i]).sum())
                q[i] += BETA * (float(q[vois].mean()) - q[i])
        th = th + DT * W0 + GAM * (s - 0.5) * DT
        q = q + ALPHA * (s - q)
        return th, q

    for _ in range(TA):
        g = etape(g)
        th, q = pas_ruq(X, th, q, g)
        c = g.mean(0)
        X = X + rng.normal(0, DIAG / 100, (N, 3))
        rel = X - c
        nrm = np.linalg.norm(rel, axis=1, keepdims=True)
        X = np.where(nrm > DIAG / 20, c + rel / nrm * DIAG / 20, X)
    R_A = float(np.abs(np.exp(1j * th).mean()))
    if R_A < 0.85:
        return {"TB": TB, "classe": "INVALIDE", "R_A": round(R_A, 3)}
    X = rng.uniform(bb0, bb1, (N, 3))
    sub = 10 if TB >= 10000 else 1
    ts, Rs = [], []
    for t in range(TB):
        g = etape(g)
        th, q = pas_ruq(X, th, q, g)
        X = X + STEP * np.column_stack(
            [np.cos(W * t + PH), np.sin(1.3 * W * t + PH),
             np.cos(0.7 * W * t + 2 * PH)]) + rng.normal(0, STEP / 3, (N, 3))
        X = np.clip(X, bb0 - DIAG * 0.25, bb1 + DIAG * 0.25)
        if t % sub == 0:
            ts.append(t + 1)
            Rs.append(float(np.abs(np.exp(1j * th).mean())))
    Rs = np.array(Rs)
    t = np.array(ts, float)
    R_fin = float(Rs[-50:].mean()) if len(Rs) >= 50 else float(Rs[-1])
    mi = (R_A + R_fin) / 2
    below = np.where(Rs < mi)[0]
    t_half = int(ts[below[0]]) if len(below) else None
    m = Rs > 0.05
    r2e = fit_r2(t[m], np.log(Rs[m])) if m.sum() > 5 else None
    r2p = fit_r2(np.log(t[m]), np.log(Rs[m])) if m.sum() > 5 else None
    return {"TB": TB, "R_A": round(R_A, 4), "R_fin": round(R_fin, 4),
            "t_half": t_half, "R2_exp": r2e, "R2_puiss": r2p,
            "t": ts[::max(1, len(ts) // 100)], "R": [
                round(float(v), 4) for v in Rs[::max(1, len(Rs) // 100)]]}


lignes = []
for TB in (100, 1000, 10000):
    r = run(TB)
    lignes.append(r)
    print(f"[c06] TB={TB} : R_A={r.get('R_A')} R_fin={r.get('R_fin')} "
          f"t_half={r.get('t_half')} R2exp={r.get('R2_exp')} "
          f"R2p={r.get('R2_puiss')}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "..", "resultats", "c06.json"), "w"))
print("[c06] archivé.")
