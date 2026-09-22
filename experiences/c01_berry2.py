#!/usr/bin/env python3
"""C01 : BERRY À 2 QUBITS INTRIQUÉS (piste interdite).
Paire de Bell + boucle fermée v2 (méridien-équateur-méridien) sur CHAQUE
qubit, orientations (oA,oB) = (++) ou (+-). Deux lectures :
- Bell (CNOT+H+mesure) : P(00) = cos²((oA+oB)·phi/2). Prédit : (++)
  frange DOUBLÉE (flip complet à phi=pi/2), (+-) PLAT à 1.0 (annulation).
- Z (mesure directe, sans rotation) : marginales = 1/2 partout, toute
  orientation — aveugle en local, frange en corrélations = signature
  d'intrication. Si les franges respirent ensemble : le pli est un tissu.
5 phi x 2 orientations x 2 lectures = 20 circuits, sim + 1 job QPU.
Shots 4000. Observation pure, zéro verdict.
"""
import json
import os
import sys
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate

HERE = os.path.dirname(os.path.abspath(__file__))
PHIS = [0.0, float(np.pi / 2), float(np.pi),
        float(3 * np.pi / 2), float(2 * np.pi)]
TH, SHOTS = float(np.pi / 2), 4000


def mats(phi):
    t = TH
    U_out = np.array([[np.cos(t / 2), -np.sin(t / 2)],
                      [np.sin(t / 2), np.cos(t / 2)]])
    U_lat = np.array([[np.exp(-1j * phi / 2), 0],
                      [0, np.exp(1j * phi / 2)]])
    nx, ny = -np.sin(phi), np.cos(phi)
    sx = np.array([[0, 1], [1, 0]])
    sy = np.array([[0, -1j], [1j, 0]])
    U_ret = (np.cos(t / 2) * np.eye(2)
             + 1j * np.sin(t / 2) * (nx * sx + ny * sy))
    return [U_out, U_lat, U_ret]


def fermeture(phi):
    U_out, U_lat, U_ret = mats(phi)
    v = (U_ret @ U_lat @ U_out)[:, 0]
    return float(abs(v[1]) ** 2), float(np.angle(v[0]))


def circ(phi, oB_plus, lecture_bell):
    piecesA = mats(phi)
    piecesB = (mats(phi) if oB_plus
               else [p.conj().T for p in reversed(mats(phi))])
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    for U in piecesA:
        qc.append(UnitaryGate(U), [0])
    for U in piecesB:
        qc.append(UnitaryGate(U), [1])
    if lecture_bell:
        qc.cx(0, 1)
        qc.h(0)
    qc.measure([0, 1], [0, 1])
    return qc


def stats(counts):
    n = sum(counts.values())
    p = {k: counts.get(k, 0) / n for k in ("00", "01", "10", "11")}
    return {"P00": round(p["00"], 4), "P01": round(p["01"], 4),
            "P10": round(p["10"], 4), "P11": round(p["11"], 4),
            "marg0": round(p["00"] + p["01"], 4),
            "marg1": round(p["00"] + p["10"], 4)}


def run_simulateur():
    from qiskit_aer import AerSimulator
    sim = AerSimulator()
    lignes = []
    for phi in PHIS:
        leak, gamma = fermeture(phi)
        row = {"phi": round(phi, 4), "fuite": round(leak, 6),
               "gamma": round(gamma, 4)}
        for oB in (True, False):
            for bell in (True, False):
                c = sim.run(transpile(circ(phi, oB, bell), sim),
                            shots=SHOTS).result().get_counts()
                s = stats(c)
                tag = f"{'pp' if oB else 'pm'}_{'bell' if bell else 'z'}"
                row[tag] = s
        lignes.append(row)
        print(f"[c01] simu phi={phi:.3f} fuite={leak:.1e} "
              f"bell_pp00={row['pp_bell']['P00']} "
              f"bell_pm00={row['pm_bell']['P00']} "
              f"z_marg={row['pp_z']['marg0']}/{row['pm_z']['marg0']}",
              flush=True)
    return lignes


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
    print(f"[c01] backend réel : {backend.name}", flush=True)
    pubs = []
    for phi in PHIS:
        for oB in (True, False):
            for bell in (True, False):
                pubs.append(transpile(circ(phi, oB, bell), backend))
    job = Sampler(backend).run(pubs, shots=SHOTS)
    print(f"[c01] job envoyé : {job.job_id()}", flush=True)
    while str(job.status()) != "DONE":
        print(f"[c01] statut={job.status()}", flush=True)
        if str(job.status()) in ("ERROR", "CANCELLED"):
            raise RuntimeError(f"job {job.status()}")
        time.sleep(60)
    res = job.result()
    lignes = []
    for i, phi in enumerate(PHIS):
        row = {"phi": round(phi, 4)}
        for j, (oB, bell) in enumerate([(True, True), (True, False),
                                        (False, True), (False, False)]):
            c = res[4 * i + j].data.c.get_counts()
            tag = f"{'pp' if oB else 'pm'}_{'bell' if bell else 'z'}"
            row[tag] = stats(c)
        lignes.append(row)
        print(f"[c01] réel phi={phi:.3f} "
              f"bell_pp00={row['pp_bell']['P00']} "
              f"bell_pm00={row['pm_bell']['P00']} "
              f"z_marg={row['pp_z']['marg0']}/{row['pm_z']['marg0']}",
              flush=True)
    return lignes, job.job_id(), backend.name


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--reel":
        lignes, job_id, backend = run_reel(sys.argv[2])
        out = os.path.join(HERE, "..", "resultats", "c01_reel.json")
        json.dump({"job": job_id, "backend": backend, "lignes": lignes},
                  open(out, "w"), indent=0)
    else:
        lignes = run_simulateur()
        out = os.path.join(HERE, "..", "resultats", "c01_simulateur.json")
        json.dump({"lignes": lignes}, open(out, "w"), indent=0)
    print(f"[c01] archivé : {out}")
