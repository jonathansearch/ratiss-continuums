# 📜 PROTOCOLES — ratiss-continuums

## C01 — Berry à 2 qubits intriqués (piste interdite, 2026-09-22)
- **Méthode** : paire de Bell + boucle fermée v2 sur chaque qubit
  (méridien-équateur-méridien, fuite ~1e-33, γ=−φ/2), orientations
  (++) ou (+−). Lectures Bell (CNOT+H) et Z directe. 5 φ × 2 ori ×
  2 lectures = 20 circuits, 4000 shots, sim + 1 job QPU.
- **Observé** : Bell (++) : P(00) = 1,0,1,0,1 (simu) / 0.99,0.02,
  0.99,0.02,0.99 (ibm_fez, job daper94ak42c73cife9g) — frange DOUBLÉE,
  flips complets. Bell (+−) : 1.0 partout (simu) / ~0.99 (réel) —
  ANNULATION. Z : marginales 0.48…0.52 partout — aveugle en local.
  La frange n'existe qu'en corrélations : les deux qubits respirent
  ensemble. Le pli est un tissu.

## C02 — RG×QM à N qubits (loi d'échelle TEST-94, 2026-09-22)
- **Méthode** : superposition à N qubits, branche A (tous à r0) vs B
  (tous à r0+dh). Fréquences internes indépendantes w_j ~ N(1, sw).
  Φ(t)=(Σw_j)·Δf·t intégrée pas à pas, M=400, T=1000.
- **Observé** : τ_N = √2/(Δf·sw·√N) : N=1→368.6 (339.6), 2→250.1
  (240.1), 4→169.1 (169.8), 8→123.2 (120.1). Contrôles N=8 :
  dh/G0/sw=0 → ∞. Cross N=4 G0=0.2 → 84.6 (84.9, τ divisé par 2).
  Loi : 1/τ ∝ √N — la décohérence gravitationnelle accélère avec N.

## C03 — Triangle RG×QM×Thermo (couplage des 3 échelles, 2026-09-22)
- **Méthode** : base C02 + flux entropique ETH (Wiener par branche,
  variance 2κ·dt — "pas de flux, pas de temps"). C(t)=exp(−a·t²−b·t),
  fit 2-paramètres, M=2000, moyenne 5 graines (1 graine = bruit ±50 %,
  assumé puis corrigé).
- **Observé** : R²>0.9996 partout. a (grav) : N=1/4/8 à 2/17/2 % ;
  b (thermo) : κ à 0/12/5 %. a ne bouge pas avec κ, b ne bouge pas
  avec G0 (au résidu d'ajustement ~15 % près à N=4). VERDICT BENCH :
  les trois échelles FACTORISENT — chaque pilier garde sa loi, pas
  d'interaction détectée. Contrôles : G0/sw=0 → a=0, b=κ ; κ=0 → b=0.

---
*Exécution : `cd ratiss-continuums && python3 experiences/cNN_*.py`*
*Réel : ajouter `--reel $TOKEN` (clé IBM, jamais commitée).* 🔒
