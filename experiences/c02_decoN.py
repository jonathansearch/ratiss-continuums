#!/usr/bin/env python3
"""C02 : RG x QM À N QUBITS — loi d'échelle de la décohérence
gravitationnelle (extension TEST-94, pilier virtuel du simulateur).
Superposition à N qubits : branche A (tous à r0) vs branche B
(tous à r0+dh). Fréquences internes INDÉPENDANTES w_j ~ N(w0, sw).
Phase relative PHI(t) = (sum_j w_j) * Df * t, intégrée pas à pas.
Prédit : C_N(t) = exp(-(t/tau_N)^2), tau_N = sqrt(2)/(Df*sw*sqrt(N)).
Loi : 1/tau proportionnel à sqrt(N). Contrôles : dh/G0/sw=0 -> infini.
Ensemble M=400, T=1000. Zéro verdict.
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "resultats", "c02.json")

M, T, DT = 400, 1000.0, 1.0
W0, SIG, R0 = 1.0, 3.0, 2.0


def f(r, g0):
    return 1.0 - g0 * math.exp(-r / SIG)


def run_case(n, dh, g0, sw, seed=11, courbe=False):
    rng = np.random.default_rng(seed)
    if sw > 0:
        W = rng.normal(W0, sw, (M, n)).sum(axis=1)
    else:
        W = np.full(M, n * W0)
    df = f(R0, g0) - f(R0 + dh, g0)
    dphi = W * df * DT
    steps = int(T / DT)
    phi = np.zeros(M)
    ts, cs = [], []
    for s in range(steps + 1):
        if s % 10 == 0:
            ts.append(s * DT)
            cs.append(float(abs(np.mean(np.exp(1j * phi)))))
        phi = phi + dphi
    cs = np.array(cs)
    m = cs > 0.3
    if m.sum() > 5 and cs[m][-1] < 0.95:
        slope = np.polyfit((np.array(ts)[m]) ** 2, np.log(cs[m]), 1)[0]
        tau = float(math.sqrt(-1 / slope)) if slope < 0 else float("inf")
    else:
        tau = float("inf")
    theo = (float(math.sqrt(2) / (abs(df) * sw * math.sqrt(n)))
            if (sw > 0 and abs(df) > 1e-12) else float("inf"))
    res = {"n": n, "dh": dh, "g0": g0, "sw": sw, "Df": round(df, 6),
           "tau_mes": round(tau, 1) if tau != float("inf") else "inf",
           "tau_theo": round(theo, 1) if theo != float("inf") else "inf",
           "C_fin": round(float(cs[-1]), 4)}
    if courbe:
        res["t"] = ts
        res["C"] = [round(c, 4) for c in cs]
    return res


if __name__ == "__main__":
    print("n  dh  g0   sw   Df       tau_mes tau_theo C_fin", flush=True)
    cas = []
    grid = [(1, 5, 0.1, 0.1, True), (2, 5, 0.1, 0.1, True),
            (4, 5, 0.1, 0.1, True), (8, 5, 0.1, 0.1, True),
            (8, 0, 0.1, 0.1, False), (8, 5, 0.0, 0.1, False),
            (8, 5, 0.1, 0.0, False), (4, 5, 0.2, 0.1, False)]
    for n, dh, g0, sw, courbe in grid:
        r = run_case(n, dh, g0, sw, courbe=courbe)
        cas.append(r)
        print(f"{n}  {dh:<3} {g0:<4} {sw:<4} {r['Df']:<8} "
              f"{r['tau_mes']!s:<7} {r['tau_theo']!s:<8} {r['C_fin']}",
              flush=True)
    json.dump({"cas": cas}, open(OUT, "w"), indent=0)
    print(f"[c02] archivé : {OUT}")
