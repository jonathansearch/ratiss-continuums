# 📓 JOURNAL — ratiss-continuums

## 2026-09-22 — Naissance du repo (filiation ratiss-focal gelé à 94/7)
- Ordre chef : nouveau repo, transformation sans toucher au socle.
- Nom tranché : RATISS CONTINUUMS. Premier chantier : C01 Berry 2 qubits
  (piste interdite). Organes portés : boucle fermée v2 (mats méridien-
  équateur-méridien, fuite ~1e-33, γ=−φ/2), motif sim+réel 1 job.

## 2026-09-22 — C01 MESURÉ : les franges respirent ensemble
- Simu : (++) flips 1,0,1,0,1 ; (+−) plat 1.0 ; Z à 1/2 partout.
- Réel ibm_fez (job daper94ak42c73cife9g, 20 circuits) : (++) 0.99/
  0.02/0.99/0.02/0.99, (+−) ~0.99 plat, Z 0.48…0.52. Réel=simu à ~0.01.
- Figure plot_C01. PROTOCOLES C01 scellé. Premier test du repo : le pli
  est un tissu (frange en corrélations, aveugle en local).

## 2026-09-22 — C02 MESURÉ : 1/τ ∝ √N (RG×QM à N qubits)
- N=1/2/4/8 : 368.6/250.1/169.1/123.2 vs 339.6/240.1/169.8/120.1.
  Contrôles ∞, cross G0×2 → τ/2 (84.6/84.9). Loi d'échelle flagship
  du simulateur. Figure plot_C02.

## 2026-09-22 — C03 MESURÉ : le triangle FACTORISE (pas d'interaction)
- C(t)=exp(−a·t²−b·t), R²>0.9996. a(grav) tient à 2/17/2 % (N=1/4/8),
  b(thermo)=κ à 0/12/5 %. Ni a(κ) ni b(G0) : chaque pilier garde sa loi.
  Leçon : 1 graine M=400 = bruit ±50 % → M=2000 × 5 graines. Fig plot_C03.

## 2026-09-22 — Rafale C04→C09 : les 6 chantiers d'un coup (ordre chef)
- C04 twist N : +1/−2/0/0/0/0 (@G0=1) — symétrie≥3 tue le twist, R→0.85.
- C05 N condensateurs : P_fin 0.90→1.22, focal 3→2 — P_sig croît (décroissant).
- C06 mémoire longue : t_half~15 puis plancher — ni expo ni puissance (R²~0).
- C07 G N-corps : couplage érode G 0.13→0.02→0.0 ; N seul = plat.
- C08 verrou QPU (kingston dapfgpgr7bnc73b3brpg) : écho tue a (1.2e−3→~0),
  b persiste — factorisation C03 verrouillée hardware.
- C09 seuil N : K=3 plat (pas de seuil) ; K=0.35 éventail critique flou.
- Organes portés (copies) : conteneur/condensateur/porteurs + A.json.
- Bugs assumés : C07-fig N=1 (barre manquante), C09 indentation K (2 lignes).

## 2026-09-22 — ARCHIVE IBM : C01+C08 rapatriés (resultats/jobs_ibm/)
- Ordre chef : ne rien laisser sur la plateforme. 2 jobs attribués
  (daper94 fez, dapfgpgr kingston), vérifiés bit-identiques. INDEX.json.
  (64 autres jobs → focal, dont Berry v1 redécouvert.)
