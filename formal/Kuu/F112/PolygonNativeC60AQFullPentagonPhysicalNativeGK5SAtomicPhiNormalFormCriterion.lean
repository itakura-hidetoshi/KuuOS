import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5RRecursivePhiObstruction
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5S — atomic recursive Phi compatibility and a sharp
normal-form criterion for vanishing of the genuine higher comparison obstruction.

GK5R constructs the actual whole Mathlib NatIso obstruction Omega_t between
two non-strict pastings of recursive Phi under genuine pointwise equivalences
e:C≈D and g:D≈E. Its vanishing is invariant under every real finite GK5D
rewrite and depends only on the full ordered dependently typed leaf word.

This new stage proves the ACTUAL atomic Phi comparison equality without
new hypotheses, using authentic iso-whiskering identity laws. It also gives
a logically exact necessary-and-sufficient structural criterion: the whole
Omega vanishes for every finite typed tree if and only if the real unit
and canonical cons-paste recursive comparison squares hold. This reduces
the remaining genuine unit/counit and middle-compositor coherence to a
minimal RIGHT-ASSOCIATED typed word scheme, using GK5R's certified
normalization theorem. It does NOT assume or declare these two remaining
classes automatically coherent.

No strict identification of a chosen quasi-inverse, unit/counit or
binary comparator; no raw F54 cells, Gray or unbounded hyperdescent.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only/same-root107, protected #1558 Draft/open/unmerged.
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

section NormalFormObstructionCriterion
variable {I : Type uI} {C D E : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i) (g : ∀ i : I, D i ≌ E i)

/-- At any genuine Mathlib functor R, the change of an actual
identity whole NatIso is the actual identity NatIso. This is a
genuine whiskering statement, not a strict inverse assertion. -/
theorem nativeGK5SChangeIso_refl
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeIso e (Iso.refl R) =
      Iso.refl (nativeGK5GChangeAtom e R) := by
  change Functor.isoWhiskerLeft (e i).inverse
    (Functor.isoWhiskerRight (Iso.refl R) (e j).functor) = Iso.refl _
  simp only [Functor.isoWhiskerRight_refl, Functor.isoWhiskerLeft_refl]

/-- At an atomic typed tree, both REAL recursive Phi pastings
coincide, with no new unit/compositor premises. The GK5Q structural
comparison is an eqToIso of an associativity proof; the GK5G
tree-Phi at an atom is the real identity NatIso. -/
theorem nativeGK5SAtomPhi_compatible
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5RSequentialCompositePhi e g (.atom R) =
      nativeGK5RDirectCompositePhi e g (.atom R) := by
  have hs :
      nativeGK5RSequentialPhi e g (.atom R) = Iso.refl _ := by
    simp only [nativeGK5RSequentialPhi, nativeGK5GChangeTreeIso,
      nativeGK5GChangeTree, nativeGK5DTreeComposite]
    rw [nativeGK5SChangeIso_refl g (nativeGK5GChangeAtom e R)]
    simp only [Iso.refl_trans]
  have htheta :
      nativeGK5QTreeComparison e g (.atom R) =
        nativeGK5QAtomComparison e g R := by
    rfl
  simp only [nativeGK5RSequentialCompositePhi,
    nativeGK5RDirectCompositePhi, hs, htheta,
    nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
    nativeGK5DTreeComposite, Iso.refl_trans, Iso.trans_refl]

/-- Hence the true target-valued whole NatIso obstruction is
unconditionally trivial on EVERY genuinely typed atomic leaf. -/
theorem nativeGK5SAtomObstruction_refl
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5RPhiObstruction e g (.atom R) = Iso.refl _ :=
  (nativeGK5RPhiObstruction_refl_iff e g (.atom R)).mpr
    (nativeGK5SAtomPhi_compatible e g R)

/-- The EXACT non-strict whole Phi equality on every original
finite heterogeneous typed tree, not merely a conditional
boolean obstruction or a structural eqToIso statement. -/
def NativeGK5SAllTreeCoherent : Prop :=
  ∀ {i j : I} (t : NativeGK5DTypedTree C i j),
    nativeGK5RSequentialCompositePhi e g t =
      nativeGK5RDirectCompositePhi e g t

/-- The genuine unit/counit comparison obligation at each actual
category object. A separate theorem must discharge it; this
declaration does not postulate that its value is true. -/
def NativeGK5SUnitCoherent : Prop :=
  ∀ i : I,
    nativeGK5RSequentialCompositePhi e g (.unit i) =
      nativeGK5RDirectCompositePhi e g (.unit i)

/-- The genuinely typed RIGHT-ASSOCIATED cons-paste comparison
obligation. It tests only `paste (atom R) (TreeOfWord w)`, not
all arbitrary binary trees; its premise is exactly the
already-checked recursive comparison for the tail word. -/
def NativeGK5SConsCoherent : Prop :=
  ∀ {i j k : I} (R : C i ⥤ C j)
      (w : NativeGK5DTypedWord C j k),
    nativeGK5RSequentialCompositePhi e g (nativeGK5DTreeOfWord w) =
      nativeGK5RDirectCompositePhi e g (nativeGK5DTreeOfWord w) →
    nativeGK5RSequentialCompositePhi e g
        (.paste (.atom R) (nativeGK5DTreeOfWord w)) =
      nativeGK5RDirectCompositePhi e g
        (.paste (.atom R) (nativeGK5DTreeOfWord w))

/-- Unit and canonical cons-paste compatibility constructively
induce whole recursive Phi comparison on every dependent typed
right-associated word. No faithfulness or strict inverse premise. -/
theorem nativeGK5SNormalWords_of_unit_cons
    (hu : NativeGK5SUnitCoherent e g)
    (hc : NativeGK5SConsCoherent e g) :
    ∀ {i j : I} (w : NativeGK5DTypedWord C i j),
      nativeGK5RSequentialCompositePhi e g (nativeGK5DTreeOfWord w) =
        nativeGK5RDirectCompositePhi e g (nativeGK5DTreeOfWord w)
  | _, _, .empty i => hu i
  | _, _, .cons R w =>
      hc R w (nativeGK5SNormalWords_of_unit_cons hu hc w)

/-- GK5R's actual pathwise obstruction normal-form equivalence
extends the proved unit+canonical-cons cases to the true recursive
Phi comparison equality for EVERY proof-relevant finite typed
binary tree. -/
theorem nativeGK5SAllTrees_of_unit_cons
    (hu : NativeGK5SUnitCoherent e g)
    (hc : NativeGK5SConsCoherent e g) :
    NativeGK5SAllTreeCoherent e g := by
  intro i j t
  have hn :
      nativeGK5RPhiObstruction e g
          (nativeGK5DTreeOfWord (nativeGK5DTreeLeaves t)) = Iso.refl _ :=
    (nativeGK5RPhiObstruction_refl_iff e g
      (nativeGK5DTreeOfWord (nativeGK5DTreeLeaves t))).mpr
        (nativeGK5SNormalWords_of_unit_cons e g hu hc
          (nativeGK5DTreeLeaves t))
  exact (nativeGK5RPhiObstruction_refl_iff e g t).mp
    ((nativeGK5RPhiObstruction_normalization_iff e g t).mpr hn)

/-- EXACT finite typed recursive Phi composition-coherence criterion.
All trees are genuinely coherent if and only if the unit comparison
and the canonical right-associated cons comparison propagation hold.
No unproved vanishing is asserted or used in either direction. -/
theorem nativeGK5SAllTrees_iff_unit_cons :
    NativeGK5SAllTreeCoherent e g ↔
      NativeGK5SUnitCoherent e g ∧ NativeGK5SConsCoherent e g := by
  constructor
  · intro hall
    constructor
    · intro i
      exact hall (.unit i)
    · intro i j k R w _
      exact hall (.paste (.atom R) (nativeGK5DTreeOfWord w))
  · rintro ⟨hu, hc⟩
    exact nativeGK5SAllTrees_of_unit_cons e g hu hc

/-- The exact same criterion expressed as the universal vanishing
of the REAL target-valued whole NatIso obstruction, rather than
as equality of its two nonstrict recursive Phi presentations. -/
theorem nativeGK5SAllObstructions_iff_unit_cons :
    (∀ {i j : I} (t : NativeGK5DTypedTree C i j),
      nativeGK5RPhiObstruction e g t = Iso.refl _) ↔
      NativeGK5SUnitCoherent e g ∧ NativeGK5SConsCoherent e g := by
  rw [← nativeGK5SAllTrees_iff_unit_cons]
  constructor
  · intro h i j t
    exact (nativeGK5RPhiObstruction_refl_iff e g t).mp (h t)
  · intro h i j t
    exact (nativeGK5RPhiObstruction_refl_iff e g t).mpr (h t)

#print axioms nativeGK5SChangeIso_refl
#print axioms nativeGK5SAtomPhi_compatible
#print axioms nativeGK5SAtomObstruction_refl
#print axioms NativeGK5SAllTreeCoherent
#print axioms NativeGK5SUnitCoherent
#print axioms NativeGK5SConsCoherent
#print axioms nativeGK5SNormalWords_of_unit_cons
#print axioms nativeGK5SAllTrees_of_unit_cons
#print axioms nativeGK5SAllTrees_iff_unit_cons
#print axioms nativeGK5SAllObstructions_iff_unit_cons

end NormalFormObstructionCriterion
end
end Kuu.F112.Physical
