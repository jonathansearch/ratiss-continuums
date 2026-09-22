#!/usr/bin/env python3
"""C05 : FOCALISATION À N CONDENSATEURS (extension TEST-04/05).
Appareil TEST-04 (organes copiés, config A.json) : N injecteurs
(graine 7+k, filet=4 chacun — flux total proportionnel à N, assumé)
+ N groupes de porteurs (graine 3+k) convergent vers le MÊME point
focal. Phi global = somme des concentrations. N dans {1,2,4,8}.
Observables : P_final/P_ref, étape de focalisation, phi max.
Question : P_sig(N) ? Zéro verdict.
"""
import json
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "organes"))
import conteneur as C
import condensateur as Q
import porteurs as P

cfg = json.load(open(os.path.join(os.path.dirname(HERE), "univers",
                                  "A.json")))
T = cfg["T"]
MESURE = {1, 4, 8, 12}


def run(n):
    fond_pts = C.fond(seed=cfg["graine_fond"])
    P_ref = C.p_sig(fond_pts)
    caps = []
    for k in range(n):
        bits = Q.charge(cfg["n_bits"], seed=cfg["graine_info"] + k)
        gouttes = Q.injecter(np.zeros((0, 3)), bits, cfg["filet"] * T,
                             seed=cfg["graine_injection"] + k)
        port = P.creer_porteurs(cfg["n_bits"], cfg["n_porteurs"], "I",
                                seed=cfg["graine_porteurs"] + k)
        caps.append((gouttes, port))
    pts, serie, phis, focal = fond_pts.copy(), [], [], None
    for t in range(T):
        for gouttes, port in caps:
            pts = np.vstack(
                [pts, gouttes[t * cfg["filet"]:(t + 1) * cfg["filet"]]])
        d2 = ((pts[:, None, :] - pts[None, :, :]) ** 2).sum(-1)
        voisins = np.argsort(d2, axis=1)[:, 1:4]
        pts = pts + cfg["lissage"] * (pts[voisins].mean(1) - pts)
        phi = 0.0
        for _, port in caps:
            P.transporter(port, cfg["point_focal"], cfg["alpha_transport"])
            phi += P.concentration(port, t + 1)
        phis.append(phi)
        if focal is None and phi >= cfg["phi_c"]:
            focal = t + 1
            pts = np.vstack([pts, C.boucle_focale(cfg["point_focal"])])
        if (t + 1) in MESURE:
            serie.append([t + 1, round(float(C.p_sig(pts) / P_ref), 4)])
    return {"n": n, "P_final": serie[-1][1], "serie": serie,
            "focalisation_etape": focal,
            "phi_max": round(float(max(phis)), 1)}


lignes = []
for n in (1, 2, 4, 8):
    r = run(n)
    lignes.append(r)
    print(f"[c05] n={n} : P_fin={r['P_final']} focal={r['focalisation_etape']} "
          f"phi_max={r['phi_max']}", flush=True)
json.dump({"lignes": lignes},
          open(os.path.join(HERE, "..", "resultats", "c05.json"), "w"),
          indent=1)
print("[c05] archivé.")
