import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5IGeneratorCoherence
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
F112-P94D3GK5J — endpoint-only obstruction for genuine category-equivalence
finite typed rewrite paths.

GK5H proves that the genuine whole-NatIso comparison square for all finite
paths is equivalent to the square for all basic structural generators; GK5I
discharges the three-atomic-leaf associator case unconditionally.

Here we prove a different exact reduction: the truth value of the WHOLE
NatIso square depends only on the fixed source and target typed trees, not on
the proof-relevant rewrite path. We may test the explicit GK5D canonical
normalization-and-reversal path for any identical-typed-leaf endpoints.
Both source and changed path equalities use REAL GK5D Mathlib NatIso
path-independence, not a postulated higher filler. The three-atom
associator certificate thereby extends to EVERY genuine rewrite path with
those endpoints.

This does not assert arbitrary-subtree associators, either unitor or
whiskering generators are automatically coherent. Neither the GK5H local
obstruction nor the global arbitrary-path obstruction is silently erased.

Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only / tighten-only / same-root107. Protected PR #1558 untouched.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vC uC

section EndpointObstruction
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- The actual whole Mathlib NatIso coherence square of one
proof-relevant heterogeneous finite path. -/
def NativeGK5JPathSquare
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (p : NativeGK5DTypedPath C a b) : Prop :=
  nativeGK5DPathIso (nativeGK5GChangePath e p) ≪≫
      nativeGK5GChangeTreeIso e b =
    nativeGK5GChangeTreeIso e a ≪≫
      nativeGK5GChangeIso e (nativeGK5DPathIso p)

/-- Path selection does NOT change the obstruction.
Both sides use GK5D's unconditional proof-relevant path independence,
once in C and independently once in the truly changed category family D. -/
theorem nativeGK5JPathSquare_iff_sameEndpoints
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (p q : NativeGK5DTypedPath C a b) :
    NativeGK5JPathSquare e p ↔ NativeGK5JPathSquare e q := by
  have hC : nativeGK5DPathIso p = nativeGK5DPathIso q :=
    nativeGK5DPath_independent p q
  have hD :
      nativeGK5DPathIso (nativeGK5GChangePath e p) =
        nativeGK5DPathIso (nativeGK5GChangePath e q) :=
    nativeGK5DPath_independent
      (nativeGK5GChangePath e p) (nativeGK5GChangePath e q)
  dsimp [NativeGK5JPathSquare]
  rw [hC, hD]

/-- The canonical obstruction tests exactly one concrete GK5D path
between any two trees with equal ORDERED, dependently typed leaves. -/
def NativeGK5JEndpointCompatible : Prop :=
  ∀ {i j : I} (a b : NativeGK5DTypedTree C i j)
    (h : nativeGK5DTreeLeaves a = nativeGK5DTreeLeaves b),
    NativeGK5JPathSquare e
      (nativeGK5DPathBetweenOfSameLeaves a b h)

/-- Exact reduction from ALL proof-relevant finite paths to the
explicit normalize-and-reverse canonical path of every compatible
typed endpoint pair. No local compatibility hypothesis is assumed. -/
theorem nativeGK5JAllPaths_iff_endpoints :
    NativeGK5HPathCompatible (C := C) (D := D) e ↔
      NativeGK5JEndpointCompatible (C := C) (D := D) e := by
  constructor
  · intro hall i j a b h
    exact hall (nativeGK5DPathBetweenOfSameLeaves a b h)
  · intro hend i j a b p
    have h := nativeGK5DPathLeaves p
    have hcanon : NativeGK5JPathSquare e
        (nativeGK5DPathBetweenOfSameLeaves a b h) :=
      hend a b h
    exact (nativeGK5JPathSquare_iff_sameEndpoints e p
      (nativeGK5DPathBetweenOfSameLeaves a b h)).mpr hcanon

/-- Re-express the GK5H local obstruction criterion without
quantifying over all possible witnesses of each rewrite path.
Canonical endpoint conditions are necessary and sufficient. -/
theorem nativeGK5JEndpoints_iff_localSteps :
    NativeGK5JEndpointCompatible (C := C) (D := D) e ↔
      NativeGK5HStepCompatible (C := C) (D := D) e :=
  (nativeGK5JAllPaths_iff_endpoints (C := C) (D := D) e).symm.trans
    (nativeGK5HAllPaths_iff_localStep (C := C) (D := D) e)

/-- Stronger GK5I corollary: every genuine, possibly redundant,
reversed or concatenated proof-relevant finite typed rewrite path
between the THREE ATOM associator endpoints has the whole
Mathlib NatIso square, without assuming GK5H StepCompatible. -/
theorem nativeGK5JThreeAtoms_allPaths
    {i j k l : I}
    (F : C i ⥤ C j) (G : C j ⥤ C k) (H : C k ⥤ C l)
    (q : NativeGK5DTypedPath C
      (.paste (.paste (.atom F) (.atom G)) (.atom H))
      (.paste (.atom F) (.paste (.atom G) (.atom H)))) :
    NativeGK5JPathSquare e q := by
  let p : NativeGK5DTypedPath C
      (.paste (.paste (.atom F) (.atom G)) (.atom H))
      (.paste (.atom F) (.paste (.atom G) (.atom H))) :=
    .basic (.assoc (.atom F) (.atom G) (.atom H))
  have hp : NativeGK5JPathSquare e p := by
    simpa only [NativeGK5JPathSquare, p,
      nativeGK5DPathIso, nativeGK5GChangePath] using
      (nativeGK5IAssociator_atoms e F G H)
  exact (nativeGK5JPathSquare_iff_sameEndpoints e p q).mp hp

#print axioms nativeGK5JPathSquare_iff_sameEndpoints
#print axioms nativeGK5JAllPaths_iff_endpoints
#print axioms nativeGK5JEndpoints_iff_localSteps
#print axioms nativeGK5JThreeAtoms_allPaths

end EndpointObstruction
end
end Kuu.F112.Physical
