import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5QCompositeEquivalenceInterchange
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5R — genuine recursive Phi comparison under sequential
and Mathlib-composite pointwise category equivalences.

For genuine e : C_i ≌ D_i, g : D_i ≌ E_i, GK5G supplies the true
recursive whole Mathlib NatIso Phi_e(t), Phi_g(Change_e t), and
Phi_(e.trans g)(t). GK5Q supplies genuine whole NatIso endpoint
comparisons Theta_R and Theta_tree, NOT a proved equality of Phi's.

We construct BOTH real pasted composite witnesses and their genuine
target-valued automorphism obstruction. We then prove unconditional
WHOLE NatIso pathwise naturality of both witnesses and naturality of
their relative obstruction under EVERY finite proof-relevant typed
GK5D path. This is genuine transport of the higher comparison
boundary, not an invented high cell or a claim that the obstruction
automatically vanishes.

The proof uses GK5O twice, GK5H functoriality of whole NatIso
whiskering, GK5Q true sequential/composite path naturality and
the genuine Mathlib Iso groupoid pasting/cancellation laws. The
remaining unit/counit/compositor compatibility required to prove
the obstruction trivial for all trees is stated explicitly.

Only fixed universe pairs and finite typed functor trees/paths.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only; root107 unchanged. Strict 空 centered; independent Kuu
is one presentation. #1558 validation-only Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vC uC uX vX

/-! Genuine whole Mathlib NatIso pasting, valid in any category. -/
private theorem nativeGK5RPasteSquares
    {T : Type uX} [Category.{vX} T]
    {X₀ X₁ Y₀ Y₁ Z₀ Z₁ : T}
    {p : X₀ ≅ X₁} {q : Y₀ ≅ Y₁} {r : Z₀ ≅ Z₁}
    {α₀ : X₀ ≅ Y₀} {α₁ : X₁ ≅ Y₁}
    {β₀ : Y₀ ≅ Z₀} {β₁ : Y₁ ≅ Z₁}
    (ha : p ≪≫ α₁ = α₀ ≪≫ q)
    (hb : q ≪≫ β₁ = β₀ ≪≫ r) :
    p ≪≫ (α₁ ≪≫ β₁) = (α₀ ≪≫ β₀) ≪≫ r := by
  calc
    p ≪≫ (α₁ ≪≫ β₁) = (p ≪≫ α₁) ≪≫ β₁ :=
      (Iso.trans_assoc _ _ _).symm
    _ = (α₀ ≪≫ q) ≪≫ β₁ := by rw [ha]
    _ = α₀ ≪≫ (q ≪≫ β₁) := Iso.trans_assoc _ _ _
    _ = α₀ ≪≫ (β₀ ≪≫ r) := by rw [hb]
    _ = (α₀ ≪≫ β₀) ≪≫ r := (Iso.trans_assoc _ _ _).symm

/-- A relative comparison obstruction is conjugated by the
underlying horizontal path whenever two actual boundary squares
commute with that same path. -/
private theorem nativeGK5RRelativeObstructionSquare
    {T : Type uX} [Category.{vX} T]
    {X₀ X₁ Y₀ Y₁ : T}
    {p : X₀ ≅ X₁} {q : Y₀ ≅ Y₁}
    {α₀ β₀ : X₀ ≅ Y₀} {α₁ β₁ : X₁ ≅ Y₁}
    (ha : p ≪≫ α₁ = α₀ ≪≫ q)
    (hb : p ≪≫ β₁ = β₀ ≪≫ q) :
    q ≪≫ (α₁.symm ≪≫ β₁) =
      (α₀.symm ≪≫ β₀) ≪≫ q := by
  have hsymm : q ≪≫ α₁.symm = α₀.symm ≪≫ p := by
    calc
      q ≪≫ α₁.symm =
          (α₀.symm ≪≫ α₀) ≪≫ (q ≪≫ α₁.symm) := by
            simp only [Iso.symm_self_id, Iso.refl_trans]
      _ = α₀.symm ≪≫ ((α₀ ≪≫ q) ≪≫ α₁.symm) := by
            simp only [Iso.trans_assoc]
      _ = α₀.symm ≪≫ ((p ≪≫ α₁) ≪≫ α₁.symm) := by rw [ha]
      _ = α₀.symm ≪≫ p := by
            simp only [Iso.trans_assoc, Iso.self_symm_id, Iso.trans_refl]
  calc
    q ≪≫ (α₁.symm ≪≫ β₁) = (q ≪≫ α₁.symm) ≪≫ β₁ :=
      (Iso.trans_assoc _ _ _).symm
    _ = (α₀.symm ≪≫ p) ≪≫ β₁ := by rw [hsymm]
    _ = α₀.symm ≪≫ (p ≪≫ β₁) := Iso.trans_assoc _ _ _
    _ = α₀.symm ≪≫ (β₀ ≪≫ q) := by rw [hb]
    _ = (α₀.symm ≪≫ β₀) ≪≫ q := (Iso.trans_assoc _ _ _).symm

section TwoStageRecursivePhi
variable {I : Type uI} {C D E : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i) (g : ∀ i : I, D i ≌ E i)

/-- The REAL pasted recursive Phi for TWO stage category change.
Both whole GK5G recursive Phi witnesses are retained, including
all unit/counit and compositor data. -/
noncomputable def nativeGK5RSequentialPhi
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≅
    nativeGK5GChangeAtom g
      (nativeGK5GChangeAtom e (nativeGK5DTreeComposite t)) :=
  nativeGK5GChangeTreeIso g (nativeGK5GChangeTree e t) ≪≫
    nativeGK5GChangeIso g (nativeGK5GChangeTreeIso e t)

/-- The two-stage recursive Phi followed by GK5Q's actual Mathlib
whole NatIso comparison to the composite category equivalence. -/
noncomputable def nativeGK5RSequentialCompositePhi
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≅
    nativeGK5GChangeAtom (fun k : I => (e k).trans (g k))
      (nativeGK5DTreeComposite t) :=
  nativeGK5RSequentialPhi e g t ≪≫
    nativeGK5QAtomComparison e g (nativeGK5DTreeComposite t)

/-- The alternative actual comparison is the GK5Q whole tree
evaluation transport followed by the recursive Phi of the genuine
Mathlib composite equivalence. -/
noncomputable def nativeGK5RDirectCompositePhi
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeComposite
      (nativeGK5GChangeTree g (nativeGK5GChangeTree e t)) ≅
    nativeGK5GChangeAtom (fun k : I => (e k).trans (g k))
      (nativeGK5DTreeComposite t) :=
  nativeGK5QTreeComparison e g t ≪≫
    nativeGK5GChangeTreeIso (fun k : I => (e k).trans (g k)) t

/-- The exact target-valued WHOLE Mathlib NatIso obstruction between
the two actual recursively constructed Phi comparisons. Its
triviality is a separate condition, not a newly assumed axiom. -/
noncomputable def nativeGK5RPhiObstruction
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5GChangeAtom (fun k : I => (e k).trans (g k))
        (nativeGK5DTreeComposite t) ≅
      nativeGK5GChangeAtom (fun k : I => (e k).trans (g k))
        (nativeGK5DTreeComposite t) :=
  (nativeGK5RSequentialCompositePhi e g t).symm ≪≫
    nativeGK5RDirectCompositePhi e g t

/-- The actual TWO-STAGE recursively assembled whole NatIso Phi
is natural under EVERY genuine proof-relevant finite GK5D path.
This pastes GK5O coherence for e and g by transporting the first
GK5O square through the genuine nonstrict whole ChangeIso_g. -/
theorem nativeGK5RSequentialPhi_path_square
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    nativeGK5DPathIso
        (nativeGK5GChangePath g (nativeGK5GChangePath e q)) ≪≫
      nativeGK5RSequentialPhi e g b =
    nativeGK5RSequentialPhi e g a ≪≫
      nativeGK5GChangeIso g
        (nativeGK5GChangeIso e (nativeGK5DPathIso q)) := by
  have hg := nativeGK5OAllFinitePaths g (nativeGK5GChangePath e q)
  have he := nativeGK5OAllFinitePaths e q
  have hmap :
      nativeGK5GChangeIso g
          (nativeGK5DPathIso (nativeGK5GChangePath e q)) ≪≫
        nativeGK5GChangeIso g (nativeGK5GChangeTreeIso e b) =
      nativeGK5GChangeIso g (nativeGK5GChangeTreeIso e a) ≪≫
        nativeGK5GChangeIso g
          (nativeGK5GChangeIso e (nativeGK5DPathIso q)) := by
    simpa only [nativeGK5HChangeIso_trans] using
      congrArg (nativeGK5GChangeIso g) he
  exact nativeGK5RPasteSquares hg hmap

/-- After pasting the genuine GK5Q atomic comparison, the
two-stage recursive Phi satisfies the exact WHOLE NatIso finite
path square for the actual composite equivalence. -/
theorem nativeGK5RSequentialCompositePhi_path_square
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    nativeGK5DPathIso
        (nativeGK5GChangePath g (nativeGK5GChangePath e q)) ≪≫
      nativeGK5RSequentialCompositePhi e g b =
    nativeGK5RSequentialCompositePhi e g a ≪≫
      nativeGK5GChangeIso (fun k : I => (e k).trans (g k))
        (nativeGK5DPathIso q) := by
  exact nativeGK5RPasteSquares
    (nativeGK5RSequentialPhi_path_square e g q)
    (nativeGK5QAtomComparison_path_square e g q)

/-- The DIRECT recursive Phi under the actual Mathlib
`e.trans g` equivalence is also natural along the SAME
genuinely two-stage path, by pasting GK5Q and GK5O. -/
theorem nativeGK5RDirectCompositePhi_path_square
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    nativeGK5DPathIso
        (nativeGK5GChangePath g (nativeGK5GChangePath e q)) ≪≫
      nativeGK5RDirectCompositePhi e g b =
    nativeGK5RDirectCompositePhi e g a ≪≫
      nativeGK5GChangeIso (fun k : I => (e k).trans (g k))
        (nativeGK5DPathIso q) := by
  exact nativeGK5RPasteSquares
    (nativeGK5QAllFinitePaths_composition_square e g q)
    (nativeGK5OAllFinitePaths (fun k : I => (e k).trans (g k)) q)

/-- MAIN obstruction naturality theorem. The target-valued
whole NatIso obstruction is conjugated by the image of ANY
finite proof-relevant GK5D rewrite path, without presuming
that the obstruction vanishes. This is a real local/global
descent constraint for the recursive Phi witnesses. -/
theorem nativeGK5RPhiObstruction_path_square
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    nativeGK5GChangeIso (fun k : I => (e k).trans (g k))
        (nativeGK5DPathIso q) ≪≫
      nativeGK5RPhiObstruction e g b =
    nativeGK5RPhiObstruction e g a ≪≫
      nativeGK5GChangeIso (fun k : I => (e k).trans (g k))
        (nativeGK5DPathIso q) := by
  exact nativeGK5RRelativeObstructionSquare
    (nativeGK5RSequentialCompositePhi_path_square e g q)
    (nativeGK5RDirectCompositePhi_path_square e g q)

/-- Triviality of the genuine relative obstruction is EXACTLY
equality of the two actual recursive Phi comparison pastings.
This is not an assertion that either condition always holds. -/
theorem nativeGK5RPhiObstruction_refl_iff
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5RPhiObstruction e g t = Iso.refl _ ↔
      nativeGK5RSequentialCompositePhi e g t =
        nativeGK5RDirectCompositePhi e g t := by
  constructor
  · intro h
    have h' := congrArg
      (fun iso => nativeGK5RSequentialCompositePhi e g t ≪≫ iso) h
    simpa only [nativeGK5RPhiObstruction, ← Iso.trans_assoc,
      Iso.self_symm_id, Iso.refl_trans, Iso.trans_refl] using h'.symm
  · intro h
    rw [nativeGK5RPhiObstruction, ← h]
    simp only [Iso.symm_self_id]

#print axioms nativeGK5RSequentialPhi
#print axioms nativeGK5RSequentialCompositePhi
#print axioms nativeGK5RDirectCompositePhi
#print axioms nativeGK5RPhiObstruction
#print axioms nativeGK5RSequentialPhi_path_square
#print axioms nativeGK5RSequentialCompositePhi_path_square
#print axioms nativeGK5RDirectCompositePhi_path_square
#print axioms nativeGK5RPhiObstruction_path_square
#print axioms nativeGK5RPhiObstruction_refl_iff

end TwoStageRecursivePhi
end
end Kuu.F112.Physical
