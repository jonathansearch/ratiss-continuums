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

## Règles (héritées du chef)
Observation pure, zéro verdict vrai/faux. Français simple. MIT. Moyens zéro.
On suit la fiche, on vérifie la file, on ne cherche pas un graviton : on observe.

*Second boss : Arena Agent. Premier boss : Jonathan.* 🫡
