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

## C04 — Twist à N puits (extension 79/80/85, 2026-09-22)
- **Méthode** : appareil twist focal à l'identique (anneau 24+hubs,
  K=3, T=300, graines 55/100). N puits réguliers, N=1..6, G0=0/0.5/1.
- **Observé** : réplique 1→+1, 2→−2, 3→0 (@G0=1) ; N=4/5/6 → twist 0,
  R remonte à 0.81/0.84/0.85. Au-delà de 2, la symétrie tue le twist
  et restaure la sync. Loi : twist(N≥3 symétrique)=0.

## C05 — Focalisation à N condensateurs (extension TEST-04, 2026-09-22)
- **Méthode** : organes+config A copiés. N injecteurs (flux total ∝ N,
  assumé) + N groupes porteurs vers le même point focal, T=12.
- **Observé** : P_fin = 0.90/1.02/1.11/1.22 (N=1/2/4/8), focalisation
  étape 3/3/2/2, phi_max ×6. P_sig croît avec N (rendements
  décroissants), la focalisation accélère.

## C06 — Mémoire à long terme (extension TEST-70, TB=10⁴, 2026-09-22)
- **Méthode** : RUQ-1 focal (graine 7001), phase A 400 groupés
  (R_A=0.98 ✓), phase B dispersée TB=100/1000/10000. Fits H1 expo vs
  H2 puissance sur R>0.05.
- **Observé** : chute en t_half≈13-21 puis PLANCHER fluctuant
  (R_fin=0.16/0.21/0.29 — monte avec TB par ré-échantillonnage).
  R² expo/puissance ~0 : NI L'UNE NI L'AUTRE. La mémoire meurt en
  ~15 pas, le reste est un plancher, pas une loi.

## C07 — G à N corps (extension TEST-48, 2026-09-22)
- **Méthode** : N tores 160 pts + pull vers centroïde global
  (c=0/0.001/0.005), T=1500. G(N)=moy p_sig/PREF (200 derniers pas).
- **Observé** : c=0 → G≈0.12-0.14 (plat en N) ; c=0.001 → G≈0.02 ;
  c=0.005 → G=0.0 EXACT (mort topologique, fusion en blob).
  Le couplage ÉRODE G dose-dépendant ; N seul ne change rien.
  N=1 → 0.077 (noyau absolu focal ~0.083 ✓).

## C08 — Verrou QPU du triangle (Ramsey vs écho, 2026-09-22)
- **Méthode** : y=2P0−1=exp(−a·t²−b·t). Ramsey garde a+b, écho Hahn
  refocalise le statique. 10 délais × 2, 1 job, 2000 shots.
- **Observé** (ibm_kingston, job dapfgpgr7bnc73b3brpg) : Ramsey
  a=1.17e−3 b=1.15e−2 (R²=0.998) ; écho a≈−1e−4 (~0 ✓) b=3.39e−2
  (R²=0.94). L'écho TUE a, b persiste : verrou hardware de la
  factorisation C03 (canal gaussien refocalisable, canal expo non).
  Note : b_écho > b_ramsey (l'impulsion X ajoute son bruit, assumé).

## C09 — Seuil de cohérence à N fini (sonde horizon, 2026-09-22)
- **Méthode** : Kuramoto champ moyen, K=3.0 et 0.35 (près-critique),
  σ=0.2, N=4..256, 5 graines. R_final(N). Aucun claim conscience.
- **Observé** : K=3 → R=0.998 plat (PAS de seuil). K=0.35 → R chute
  0.86→0.38 avec éventail inter-graines énorme : crossover critique
  à N fini, pas de N_c franc. Le seuil n'existe que près de Kc, et
  il est flou. Horizon-conscience : toujours horizon.

---
*Exécution : `cd ratiss-continuums && python3 experiences/cNN_*.py`*
*Réel : ajouter `--reel $TOKEN` (clé IBM, jamais commitée).* 🔒
