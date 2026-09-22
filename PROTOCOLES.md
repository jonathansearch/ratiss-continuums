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

---
*Exécution : `cd ratiss-continuums && python3 experiences/cNN_*.py`*
*Réel : ajouter `--reel $TOKEN` (clé IBM, jamais commitée).* 🔒
