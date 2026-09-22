#!/usr/bin/env python3
"""C08 : VERROU QPU DU TRIANGLE — Ramsey vs écho, fit 2-paramètres.
Miroir hardware de C03 (analogique, assumé) : le canal GAUSSIEN (a,
étalement statique/inhomogène) joue le rôle du pilier grav, le canal
EXPONENTIEL (b, bruit rapide) celui du pilier thermo. Ramsey H-d-H
garde a+b ; écho Hahn H-d/2-X-d/2-H refocalise le statique (a->0).
y = 2*P0-1 = exp(-a*t²-b*t), t en us. 10 délais x 2 séquences =
20 circuits, 1 job, shots 2000. Simu = modèles + binomial (Aer ne
mord pas sur les délais, constaté PONT-T2). Zéro verdict.
"""
import json
import os
import sys
import numpy as np
from qiskit import QuantumCircuit, transpile

HERE = os.path.dirname(os.path.abspath(__file__))
DELAIS = [0, 10, 20, 40, 70, 100, 150, 200, 250, 300]
SHOTS = 2000


def circ(t_us, echo):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    if t_us > 0:
        if echo:
            qc.delay(t_us / 2, 0, unit="us")
            qc.x(0)
            qc.delay(t_us / 2, 0, unit="us")
        else:
            qc.delay(t_us, 0, unit="us")
    qc.h(0)
    qc.measure(0, 0)
    return qc


def ajuste(ps):
    y = np.array([2 * v - 1 for v in ps])
    x = np.array(DELAIS, float)
    m = y > 0.05
    if m.sum() < 4:
        return {"a": None, "b": None, "R2": None}
    X = np.column_stack([x[m] ** 2, x[m]])
    (a, b), _, _, _ = np.linalg.lstsq(X, -np.log(y[m]), rcond=None)
    yh = X @ np.array([a, b])
    r2 = 1 - ((yh + np.log(y[m])) ** 2).sum() / \
        (((-np.log(y[m])) - (-np.log(y[m])).mean()) ** 2).sum()
    return {"a": round(float(a), 8), "b": round(float(b), 6),
            "R2": round(float(r2), 4)}


def run_simulateur():
    rng = np.random.default_rng(808)
    out = {}
    for echo, (a0, b0) in ((False, ((1 / 70) ** 2, 1 / 200)),
                           (True, (0.0, 1 / 200))):
        ps = []
        for t in DELAIS:
            p = 0.5 + 0.5 * np.exp(-a0 * t ** 2 - b0 * t)
            ps.append(float(rng.binomial(SHOTS, p) / SHOTS))
        tag = "echo" if echo else "ramsey"
        out[tag] = {"P0": [round(v, 4) for v in ps], **ajuste(ps)}
        print(f"[c08] simu {tag} : a={out[tag]['a']} b={out[tag]['b']} "
              f"R2={out[tag]['R2']}", flush=True)
    return out


def run_reel(token):
    import time
    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    QiskitRuntimeService.save_account(
        channel="ibm_quantum_platform", token=token, instance="auto",
        filename="/tmp/qiskit-ibm.json", overwrite=True)
    service = QiskitRuntimeService(channel="ibm_quantum_platform",
                                   filename="/tmp/qiskit-ibm.json")
    files = []
    for b in service.backends(simulator=False, operational=True):
        try:
            files.append((b.status().pending_jobs, b))
        except Exception:
            pass
    backend = sorted(files, key=lambda f: f[0])[0][1]
    print(f"[c08] backend réel : {backend.name}", flush=True)
    pubs = []
    for echo in (False, True):
        for t in DELAIS:
            pubs.append(transpile(circ(t, echo), backend))
    job = Sampler(backend).run(pubs, shots=SHOTS)
    print(f"[c08] job envoyé : {job.job_id()}", flush=True)
    while str(job.status()) != "DONE":
        print(f"[c08] statut={job.status()}", flush=True)
        if str(job.status()) in ("ERROR", "CANCELLED"):
            raise RuntimeError(f"job {job.status()}")
        time.sleep(60)
    res = job.result()
    out = {}
    for i, echo in enumerate((False, True)):
        ps = [res[10 * i + j].data.c.get_counts().get("0", 0) / SHOTS
              for j in range(10)]
        tag = "echo" if echo else "ramsey"
        out[tag] = {"P0": [round(float(v), 4) for v in ps], **ajuste(ps)}
        print(f"[c08] réel {tag} : a={out[tag]['a']} b={out[tag]['b']} "
              f"R2={out[tag]['R2']}", flush=True)
    return out, job.job_id(), backend.name


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--reel":
        out, job_id, backend = run_reel(sys.argv[2])
        out = {"job": job_id, "backend": backend, "delais_us": DELAIS, **out}
        p = os.path.join(HERE, "..", "resultats", "c08_reel.json")
    else:
        out = {"delais_us": DELAIS, **run_simulateur()}
        p = os.path.join(HERE, "..", "resultats", "c08_simulateur.json")
    json.dump(out, open(p, "w"), indent=1)
    print(f"[c08] archivé : {p}")
