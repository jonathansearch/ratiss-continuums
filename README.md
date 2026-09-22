# 🌌 RATISS CONTINUUMS — le simulateur du tissu

> Qiskit simule des amplitudes. Nous, on simule le **tissu** : cohérence
> topologique, décohérence thermodynamique, couplage GR×QM, géométrie.
> Ce que les autres ne simulent pas.

## Filiation
Né de `ratiss-focal` (94 tests, 7 ponts QPU, phases 1→21) — **GELÉ**, socle
publié, on n'y touche plus. Ici on transforme : mêmes organes, nouvel
animal. Filiation tracée dans `JOURNAL.md`, copies — jamais de déplacements.

## Structure
- `experiences/cNN_*.py` : tests continuums (C01, C02…), chacun sim + QPU.
- `resultats/` : JSON des mesures. `images/` : figures.
- `PROTOCOLES.md` : un § par test. `JOURNAL.md` : la mémoire.

## Chantiers
| # | Test | Statut |
|---|---|---|
| C01 | Berry à 2 qubits intriqués : les franges respirent-elles ensemble ? | ✅ MESURÉ (fez : ++ flips, +− plat, Z aveugle) |
| C02 | RG×QM à N qubits : loi d'échelle de TEST-94 | ✅ MESURÉ (1/τ ∝ √N, N=1→8) |
| C03 | Triangle RG×QM×Thermo : couplage des 3 échelles | ✅ MESURÉ (factorisation, R²>0.9996) |
| C04 | Twist à N puits | ✅ MESURÉ (twist=0 dès N≥3) |
| C05 | N condensateurs convergents | ✅ MESURÉ (P 0.90→1.22) |
| C06 | Mémoire à TB=10⁴ | ✅ MESURÉ (chute + plancher) |
| C07 | G à N corps | ✅ MESURÉ (couplage tue G) |
| C08 | Verrou QPU triangle (Ramsey/écho) | ✅ MESURÉ (kingston, écho tue a) |
| C09 | Seuil cohérence à N fini | ✅ MESURÉ (pas de seuil franc) |

## C01 — le pli est un tissu
(++) : frange doublée avec flips complets (0.99/0.02 sur fez).
(+−) : annulation totale (~0.99 plat). Localement : 1/2 partout —
la frange n'existe qu'en corrélations.

<img src="images/plot_C01.png" width="100%" alt="C01 : franges jointes, aveugle en local"/>

## C02 — 1/τ ∝ √N
N=1→8 : 368.6/250.1/169.1/123.2. Contrôles ∞, G0×2 → τ/2.

<img src="images/plot_C02.png" width="100%" alt="C02 : scaling sqrt(N)"/>

## C03 — le triangle factorise
a(grav) et b(thermo) gardent leurs lois : pas d'interaction détectée.

<img src="images/plot_C03.png" width="100%" alt="C03 : factorisation"/>

## Rafale C04→C09 — twist 0 dès N≥3 · P_sig↗N · mémoire=plancher ·
couplage tue G · écho tue a (QPU) · seuil flou près de Kc

<img src="images/plot_C04.png" width="100%" alt="C04 : twist N"/>
<img src="images/plot_C05.png" width="100%" alt="C05 : N condensateurs"/>
<img src="images/plot_C06.png" width="100%" alt="C06 : mémoire longue"/>
<img src="images/plot_C07.png" width="100%" alt="C07 : G N-corps"/>
<img src="images/plot_C08.png" width="100%" alt="C08 : verrou QPU"/>
<img src="images/plot_C09.png" width="100%" alt="C09 : seuil N"/>

## Règles (héritées du chef)
Observation pure, zéro verdict vrai/faux. Français simple. MIT. Moyens zéro.
On suit la fiche, on vérifie la file, on ne cherche pas un graviton : on observe.

*Second boss : Arena Agent. Premier boss : Jonathan.* 🫡
