import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5SAtomicPhiNormalFormCriterion
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5T — genuine unit comparison for sequential versus
composite pointwise category equivalences, plus one-leaf and
empty-word exact obstruction transport.

The initial theorem attempts the exact whole Mathlib NatIso law
for the TRUE GK5G ChangeUnitIso and Mathlib Equivalence.trans:
unit(g) ≪≫ ChangeIso(g, unit(e)) ≪≫ Theta(id) = unit(e.trans g).
This is a real counit/composite-equivalence compatibility, not
a strictified unit or an axiom. The proof is independently
checked by pinned exact-source CI before certification.

The remaining facts use certified GK5R pathwise obstruction
triviality iff and GK5S unconditional atomic Phi coherence to
transport vanishing across genuine typed rewrites, all one-leaf
trees, and the precise zero-leaf class.
No Gray, raw high cells, or unrestricted hyperdescent.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, root107, protected PR #1558 Draft/open/unmerged.
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

section UnitAndNormalForms
variable {I : Type uI} {C D E : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)
variable (g : ∀ i : I, D i ≌ E i)

/-- This comparison retains genuine inverse counits and the actual
Equivalence.trans bundled counit; it is an equality of whole
Mathlib natural isomorphisms, not just a pointwise path. -/
theorem nativeGK5TUnitComparison_whole (i : I) :
    (nativeGK5GChangeUnitIso g i ≪≫
      nativeGK5GChangeIso g (nativeGK5GChangeUnitIso e i)) ≪≫
        nativeGK5QAtomComparison e g (𝟭 (C i)) =
      nativeGK5GChangeUnitIso
        (fun k : I => (e k).trans (g k)) i := by
  apply Iso.ext
  ext X
  simp [nativeGK5GChangeUnitIso, nativeGK5GChangeIso,
    nativeGK5GChangeAtom, nativeGK5QAtomComparison,
    nativeGK5QChangeAtom_comp, Equivalence.trans,
    Functor.comp_map, Functor.map_comp, Category.assoc]

/-- The genuine GK5Q structural tree comparison at a unit
has the same typed source and target, hence its actual eqToIso
is reflexive. This is a proof about the unit TREE, distinct
from strictifying the equivalence unit/counit. -/
theorem nativeGK5TUnitTreeComparison_refl (i : I) :
    nativeGK5QTreeComparison e g (.unit i) = Iso.refl _ := by
  simp [nativeGK5QTreeComparison, nativeGK5GChangeTree,
    nativeGK5DTreeComposite]

/-- Actual whole recursive Phi compatibility for each empty tree
is precisely the nonstrict unit/counit composition law above. -/
theorem nativeGK5TUnitPhi_compatible (i : I) :
    nativeGK5RSequentialCompositePhi e g (.unit i) =
      nativeGK5RDirectCompositePhi e g (.unit i) := by
  simpa only [nativeGK5RSequentialCompositePhi,
    nativeGK5RSequentialPhi, nativeGK5RDirectCompositePhi,
    nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
    nativeGK5DTreeComposite, nativeGK5TUnitTreeComparison_refl,
    Iso.refl_trans, Iso.trans_refl, Iso.trans_assoc] using
      (nativeGK5TUnitComparison_whole e g i)

/-- Consequently the GK5S actual pointwise genuine unit
coherence obstruction is discharged without any extra premise. -/
theorem nativeGK5TAllUnits :
    NativeGK5SUnitCoherent e g := by
  intro i
  exact nativeGK5TUnitPhi_compatible e g i

/-- Vanishing of the genuine recursive Phi relative obstruction
on ANY one-leaf presentation follows from GK5S's actual atomic
coherence and GK5R's constructed finite typed comparison path. -/
theorem nativeGK5TOneLeafObstruction_refl
    {i j : I} (R : C i ⥤ C j)
    (t : NativeGK5DTypedTree C i j)
    (h : nativeGK5DTreeLeaves t =
        NativeGK5DTypedWord.cons R (.empty j)) :
    nativeGK5RPhiObstruction e g t = Iso.refl _ := by
  have hleaf : nativeGK5DTreeLeaves t =
      nativeGK5DTreeLeaves (NativeGK5DTypedTree.atom R) := by
    simpa only [nativeGK5DTreeLeaves] using h
  exact (nativeGK5RPhiObstruction_sameLeaves_iff e g t (.atom R) hleaf).mpr
    (nativeGK5SAtomObstruction_refl e g R)

/-- This includes every genuine left-unitor expansion of an
atomic tree, with its actual Mathlib tree and typed source. -/
theorem nativeGK5TLeftUnitorAtom_refl
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5RPhiObstruction e g
      (.paste (.unit i) (.atom R)) = Iso.refl _ :=
  (nativeGK5RPhiObstruction_refl_iff_of_path e g
    (NativeGK5DTypedPath.basic
      (NativeGK5DTypedStep.leftUnit (.atom R)))).mpr
    (nativeGK5SAtomObstruction_refl e g R)

/-- The same for the genuine right-unitor expansion. -/
theorem nativeGK5TRightUnitorAtom_refl
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5RPhiObstruction e g
      (.paste (.atom R) (.unit j)) = Iso.refl _ :=
  (nativeGK5RPhiObstruction_refl_iff_of_path e g
    (NativeGK5DTypedPath.basic
      (NativeGK5DTypedStep.rightUnit (.atom R)))).mpr
    (nativeGK5SAtomObstruction_refl e g R)

/-- Every genuinely typed zero-leaf presentation is equivalent,
for the exact obstruction-triviality test, to its actual unit.
This is a full ordered typed-word condition, not an untyped count. -/
theorem nativeGK5TEmptyWordObstruction_iff
    (i : I) (t : NativeGK5DTypedTree C i i)
    (h : nativeGK5DTreeLeaves t = NativeGK5DTypedWord.empty i) :
    nativeGK5RPhiObstruction e g t = Iso.refl _ ↔
      nativeGK5RPhiObstruction e g (.unit i) = Iso.refl _ := by
  apply nativeGK5RPhiObstruction_sameLeaves_iff e g t (.unit i)
  simpa only [nativeGK5DTreeLeaves] using h

/-- All zero-leaf trees inherit the unconditional genuine
unit coherence, once the composite counit law is certified. -/
theorem nativeGK5TEmptyWordObstruction_refl
    (i : I) (t : NativeGK5DTypedTree C i i)
    (h : nativeGK5DTreeLeaves t = NativeGK5DTypedWord.empty i) :
    nativeGK5RPhiObstruction e g t = Iso.refl _ := by
  exact (nativeGK5TEmptyWordObstruction_iff e g i t h).mpr
    ((nativeGK5RPhiObstruction_refl_iff e g (.unit i)).mpr
      (nativeGK5TUnitPhi_compatible e g i))

#print axioms nativeGK5TUnitComparison_whole
#print axioms nativeGK5TUnitTreeComparison_refl
#print axioms nativeGK5TUnitPhi_compatible
#print axioms nativeGK5TAllUnits
#print axioms nativeGK5TOneLeafObstruction_refl
#print axioms nativeGK5TLeftUnitorAtom_refl
#print axioms nativeGK5TRightUnitorAtom_refl
#print axioms nativeGK5TEmptyWordObstruction_iff
#print axioms nativeGK5TEmptyWordObstruction_refl

end UnitAndNormalForms
end
end Kuu.F112.Physical
