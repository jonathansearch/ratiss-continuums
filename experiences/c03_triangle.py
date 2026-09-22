#!/usr/bin/env python3
"""C03 : TRIANGLE RG x QM x THERMO — comment les trois échelles se couplent.
Base C02 (N qubits, branches A/B à r0/r0+dh, spread interne sw) + flux
entropique ETH (doctrine : "pas de flux -> pas de temps", "la décohérence
n'est pas un taux, c'est un intervalle entre trajectoires") : bruit de
Wiener indépendant par branche, variance 2*kappa*dt sur la phase relative.
Modèle : C(t) = exp(-a*t^2 - b*t), a=(Df*sw*sqrt(N)/sqrt(2))^2 (grav),
b=kappa (thermo). Fit 2-paramètres par cas.
Question : a bouge-t-il avec kappa ? b bouge-t-il avec G0 ?
Factorisation (non) vs interaction (oui). M=400, T=1000. Zéro verdict.
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "resultats", "c03.json")

M, T, DT = 2000, 1000.0, 1.0
W0, SIG, R0 = 1.0, 3.0, 2.0
SEEDS = (21, 22, 23, 24, 25)


def f(r, g0):
    return 1.0 - g0 * math.exp(-r / SIG)


def run_case(n, dh, g0, sw, kappa, seed=21, courbe=False):
    df = f(R0, g0) - f(R0 + dh, g0)
    steps = int(T / DT)
    sig = math.sqrt(2 * kappa * DT)
    acc, ts = None, []
    for sd in SEEDS:
        rng = np.random.default_rng(sd)
        if sw > 0:
            W = rng.normal(W0, sw, (M, n)).sum(axis=1)
        else:
            W = np.full(M, n * W0)
        phi = np.zeros(M)
        cs = []
        for s in range(steps + 1):
            if s % 10 == 0:
                if sd == SEEDS[0]:
                    ts.append(s * DT)
                cs.append(float(abs(np.mean(np.exp(1j * phi)))))
            phi = phi + W * df * DT + sig * rng.normal(0, 1, M)
        acc = np.array(cs) if acc is None else acc + np.array(cs)
    cs = acc / len(SEEDS)
    t = np.array(ts)
    m = cs > 0.08
    X = np.column_stack([t[m] ** 2, t[m]])
    y = -np.log(cs[m])
    (a, b), _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ np.array([a, b])
    denom = ((y - y.mean()) ** 2).sum()
    r2 = 1 - ((y - yhat) ** 2).sum() / denom if denom > 0 else 1.0
    a_th = (df * sw * math.sqrt(n) / math.sqrt(2)) ** 2 if sw > 0 else 0.0
    res = {"n": n, "dh": dh, "g0": g0, "sw": sw, "kappa": kappa,
           "a_mes": round(float(a), 8), "a_theo": round(a_th, 8),
           "b_mes": round(float(b), 6), "b_theo": kappa,
           "R2": round(float(r2), 4), "C_fin": round(float(cs[-1]), 4)}
    if courbe:
        res["t"] = ts
        res["C"] = [round(c, 4) for c in cs]
    return res


if __name__ == "__main__":
    print("n dh g0  sw  kap   a_mes      a_theo     b_mes   b_theo R2",
          flush=True)
    grid = [(4, 5, 0.1, 0.1, 0.0, True), (4, 5, 0.1, 0.1, 0.002, True),
            (4, 5, 0.1, 0.1, 0.005, True), (1, 5, 0.1, 0.1, 0.005, False),
            (4, 5, 0.0, 0.1, 0.005, True), (4, 5, 0.1, 0.0, 0.005, False),
            (4, 0, 0.0, 0.1, 0.0, False), (8, 5, 0.1, 0.1, 0.005, False)]
    cas = []
    for n, dh, g0, sw, kap, courbe in grid:
        r = run_case(n, dh, g0, sw, kap, courbe=courbe)
        cas.append(r)
        print(f"{n} {dh:<2} {g0:<3} {sw:<3} {kap:<5} {r['a_mes']:<10} "
              f"{r['a_theo']:<10} {r['b_mes']:<7} {r['b_theo']:<6} {r['R2']}",
              flush=True)
    json.dump({"cas": cas}, open(OUT, "w"), indent=0)
    print(f"[c03] archivé : {OUT}")
