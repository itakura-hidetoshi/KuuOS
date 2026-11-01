import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5GPointwiseCategoryEquivalenceChange
import Mathlib.CategoryTheory.Whiskering
import Mathlib.CategoryTheory.EqToHom
import Mathlib.Tactic

/-!
F112-P94D3GK5H — genuine pointwise category-equivalence whole
NatIso coherence: local obstruction and pathwise gluing.

GK5G constructs a real whole Mathlib NatIso Phi_t comparing
the transported finite typed tree's evaluation with the
conjugated whole original functor. The arbitrary-path
pseudonaturality square was explicitly left unproved.

This file formalizes the EXACT coherence obstruction:
every actual typed path has the whole NatIso comparison
square if and only if EACH actual basic associator/unitor/
whiskering step does. The theorem is constructive, treating
identity, reverse and concatenation by actual Iso groupoid laws,
and does NOT assume or claim these local obstructions vanish.

Every pointwise change uses a genuine Mathlib category
equivalence e_i : C i ≌ D i; no strictification of its inverse,
no original raw high cells, no arbitrary family identification.
Q_T and P_T are not definitionally identified. Finite indexed
paths only, no global Gray/hyperdescent.

Append-only, root107, Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected #1558 Draft/open/unmerged.
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

section LocalToGlobal
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- Genuine local compatibility for each basic structural rewrite,
including whiskering. This is an explicit PROP obstruction, not a
new axiom: it holds exactly when the two actual whole Mathlib
NatIso pastings agree. -/
def NativeGK5HStepCompatible : Prop :=
  ∀ {i j : I} {a b : NativeGK5DTypedTree C i j}
      (s : NativeGK5DTypedStep C a b),
    nativeGK5DStepIso (nativeGK5GChangeStep e s) ≪≫
      nativeGK5GChangeTreeIso e b =
    nativeGK5GChangeTreeIso e a ≪≫
      nativeGK5GChangeIso e (nativeGK5DStepIso s)

/-- Genuine whole-NatIso compatibility for every proof-relevant
finite rewrite path, not merely equality of its components. -/
def NativeGK5HPathCompatible : Prop :=
  ∀ {i j : I} {a b : NativeGK5DTypedTree C i j}
      (q : NativeGK5DTypedPath C a b),
    nativeGK5DPathIso (nativeGK5GChangePath e q) ≪≫
      nativeGK5GChangeTreeIso e b =
    nativeGK5GChangeTreeIso e a ≪≫
      nativeGK5GChangeIso e (nativeGK5DPathIso q)

/-- The real category-equivalence conjugation action preserves
reversal of whole Mathlib NatIso values. -/
theorem nativeGK5HChangeIso_symm
    {i j : I} {R S : C i ⥤ C j} (α : R ≅ S) :
    nativeGK5GChangeIso e α.symm =
      (nativeGK5GChangeIso e α).symm := by
  rfl

/-- Pointwise conjugation preserves real composition of whole
Mathlib NatIso values as a strict equality of transported
whole NatIso witnesses. -/
theorem nativeGK5HChangeIso_trans
    {i j : I} {R S T : C i ⥤ C j}
    (α : R ≅ S) (β : S ≅ T) :
    nativeGK5GChangeIso e (α ≪≫ β) =
      nativeGK5GChangeIso e α ≪≫ nativeGK5GChangeIso e β := by
  apply Iso.ext
  simp only [nativeGK5GChangeIso, Iso.trans_hom,
    Functor.isoWhiskerLeft_hom, Functor.isoWhiskerRight_hom,
    Functor.whiskerLeft_comp, Functor.whiskerRight_comp]
  rfl

/-- A formal groupoid identity: an actual whole NatIso square
remains commutative when both path Iso witnesses are inverted. -/
private theorem nativeGK5HReverseSquare
    {A B : Type uC} [Category.{vC} A] [Category.{vC} B]
    {L₀ L₁ R₀ R₁ : A ⥤ B}
    (P : L₀ ≅ L₁) (Q : R₀ ≅ R₁)
    (φ₀ : L₀ ≅ R₀) (φ₁ : L₁ ≅ R₁)
    (h : P ≪≫ φ₁ = φ₀ ≪≫ Q) :
    P.symm ≪≫ φ₀ = φ₁ ≪≫ Q.symm := by
  have h' : φ₀ = (P ≪≫ φ₁) ≪≫ Q.symm := by
    calc
      φ₀ = (φ₀ ≪≫ Q) ≪≫ Q.symm := by simp
      _ = (P ≪≫ φ₁) ≪≫ Q.symm := by rw [h]
  calc
    P.symm ≪≫ φ₀ =
      P.symm ≪≫ ((P ≪≫ φ₁) ≪≫ Q.symm) := by rw [h']
    _ = φ₁ ≪≫ Q.symm := by simp [Iso.trans_assoc]

/-- The non-vacuous finite-path GLUING implication:
all actual typed paths are coherent whenever ALL local
basic steps have the real whole NatIso square.
This proves no unjustified automatic local coherence. -/
theorem nativeGK5HLocalStep_implies_allPaths
    (hlocal : NativeGK5HStepCompatible (C := C) (D := D) e) :
    NativeGK5HPathCompatible (C := C) (D := D) e := by
  intro i j a b q
  induction q with
  | refl a =>
      simp only [nativeGK5DPathIso, nativeGK5GChangePath,
        nativeGK5GChangeIso, Functor.isoWhiskerRight_refl,
        Functor.isoWhiskerLeft_refl, Iso.refl_trans]
      exact (Iso.trans_refl (nativeGK5GChangeTreeIso e a)).symm
  | basic s =>
      simpa only [nativeGK5DPathIso, nativeGK5GChangePath] using
        hlocal s
  | reverse q ih =>
      simpa only [nativeGK5DPathIso, nativeGK5GChangePath,
        nativeGK5HChangeIso_symm] using
        (nativeGK5HReverseSquare (A := D i) (B := D j)
          (nativeGK5DPathIso (nativeGK5GChangePath e q))
          (nativeGK5GChangeIso e (nativeGK5DPathIso q))
          (nativeGK5GChangeTreeIso e _)
          (nativeGK5GChangeTreeIso e _) ih)
  | trans q r ihq ihr =>
      simpa only [nativeGK5DPathIso, nativeGK5GChangePath,
        nativeGK5HChangeIso_trans, Iso.trans_assoc] using
        (show
          (nativeGK5DPathIso (nativeGK5GChangePath e q) ≪≫
              nativeGK5DPathIso (nativeGK5GChangePath e r)) ≪≫
              nativeGK5GChangeTreeIso e _ =
            nativeGK5GChangeTreeIso e _ ≪≫
              (nativeGK5GChangeIso e (nativeGK5DPathIso q) ≪≫
                nativeGK5GChangeIso e (nativeGK5DPathIso r)) from
          calc
            _ = nativeGK5DPathIso (nativeGK5GChangePath e q) ≪≫
                (nativeGK5DPathIso (nativeGK5GChangePath e r) ≪≫
                  nativeGK5GChangeTreeIso e _) := by simp [Iso.trans_assoc]
            _ = nativeGK5DPathIso (nativeGK5GChangePath e q) ≪≫
                (nativeGK5GChangeTreeIso e _ ≪≫
                  nativeGK5GChangeIso e (nativeGK5DPathIso r)) := by rw [ihr]
            _ = (nativeGK5DPathIso (nativeGK5GChangePath e q) ≪≫
                  nativeGK5GChangeTreeIso e _) ≪≫
                  nativeGK5GChangeIso e (nativeGK5DPathIso r) := by
                    simp [Iso.trans_assoc]
            _ = (nativeGK5GChangeTreeIso e _ ≪≫
                  nativeGK5GChangeIso e (nativeGK5DPathIso q)) ≪≫
                  nativeGK5GChangeIso e (nativeGK5DPathIso r) := by rw [ihq]
            _ = _ := by simp [Iso.trans_assoc])

/-- Every full-path square necessarily contains the basic-step
squares: this is the precise local obstruction converse. -/
theorem nativeGK5HAllPaths_implies_localStep
    (hall : NativeGK5HPathCompatible (C := C) (D := D) e) :
    NativeGK5HStepCompatible (C := C) (D := D) e := by
  intro i j a b s
  simpa only [nativeGK5DPathIso, nativeGK5GChangePath] using
    (hall (NativeGK5DTypedPath.basic s))

/-- EXACT LOCAL-TO-GLOBAL OBSTRUCTION CRITERION. The arbitrary
finite rewrite path whole NatIso comparison is coherent IFF
each genuine associator/unitor/whiskering generator passes
its real whole NatIso square. No Gray filler is added. -/
theorem nativeGK5HAllPaths_iff_localStep :
    NativeGK5HPathCompatible (C := C) (D := D) e ↔
      NativeGK5HStepCompatible (C := C) (D := D) e :=
  ⟨nativeGK5HAllPaths_implies_localStep e,
    nativeGK5HLocalStep_implies_allPaths e⟩

/-- A specific actual GK5D normalization route inherits the
whole NatIso pseudonaturality square under the exact local
coherence hypothesis; no path existence assumption is needed. -/
theorem nativeGK5HNormalizePath_square
    (hlocal : NativeGK5HStepCompatible (C := C) (D := D) e)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DPathIso
        (nativeGK5GChangePath e (nativeGK5DNormalizePath t)) ≪≫
      nativeGK5GChangeTreeIso e
        (nativeGK5DTreeOfWord (nativeGK5DTreeLeaves t)) =
    nativeGK5GChangeTreeIso e t ≪≫
      nativeGK5GChangeIso e
        (nativeGK5DPathIso (nativeGK5DNormalizePath t)) :=
  nativeGK5HLocalStep_implies_allPaths e hlocal
    (nativeGK5DNormalizePath t)

#print axioms nativeGK5HChangeIso_symm
#print axioms nativeGK5HChangeIso_trans
#print axioms nativeGK5HLocalStep_implies_allPaths
#print axioms nativeGK5HAllPaths_implies_localStep
#print axioms nativeGK5HAllPaths_iff_localStep
#print axioms nativeGK5HNormalizePath_square

end LocalToGlobal
end
end Kuu.F112.Physical
