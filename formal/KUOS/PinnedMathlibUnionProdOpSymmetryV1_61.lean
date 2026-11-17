/-
Copyright (c) 2026 Joël Riou. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Joël Riou
-/

import KUOS.PinnedMathlibUnionProdWeakRankV1_61
import Mathlib.AlgebraicTopology.SimplicialSet.AnodyneExtensions.Basic
import Mathlib.AlgebraicTopology.SimplicialSet.SubcomplexOp

/-!
# Additive pinned-mathlib opposite-symmetry prerequisites for UnionProd

Source: Joël Riou, mathlib4 27e085939a074823b4c553fc5d7543a8ce2708b0,
StdSimplex / Monoidal / Horn / Boundary / UnionProd prerequisite lemmas.
The fixed mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6
lacks these names. They are proved here without changing the mathlib pin.
This is a proof port, not an axiom or a substitute for a Lean CI certificate.
-/

universe u

open CategoryTheory MonoidalCategory Simplicial Opposite

namespace SSet

namespace stdSimplex

/-- The canonical reversal of the vertices identifies the opposite simplex. -/
protected def opObjEquiv {n : SimplexCategory} {d : SimplexCategoryᵒᵖ} :
    (stdSimplex.{u}.obj n).op.obj d ≃ (stdSimplex.obj n).obj d :=
  SSet.opObjEquiv.trans (objEquiv.trans
    (SimplexCategory.revEquivalence.fullyFaithfulFunctor.homEquiv.trans objEquiv.symm))

protected lemma opObjEquiv_apply {d n : ℕ} (f : Δ[n].op _⦋d⦌) (i : Fin (d + 1)) :
    stdSimplex.opObjEquiv.{u} f i = (opObjEquiv f i.rev).rev := rfl

lemma opObjEquiv_opObjEquiv_symm_apply {d n : ℕ} (f : (Δ[n] _⦋d⦌))
    (i : Fin (d + 1)) :
    SSet.opObjEquiv (stdSimplex.opObjEquiv.{u}.symm f) i = (f i.rev).rev := rfl

set_option backward.isDefEq.respectTransparency false in
lemma map_rev_map_op_apply {n d d' : ℕ} (f : ⦋d⦌ ⟶ ⦋d'⦌)
    (g : Δ[n] _⦋d'⦌) (i : Fin (d + 1)) :
    dsimp% (show Δ[n] _⦋d⦌ from (Δ[n] : SSet.{u}).map (SimplexCategory.rev.map f).op g : Δ[n] _⦋d⦌) i =
      g (f i.rev).rev := rfl

set_option backward.isDefEq.respectTransparency false in
/-- The opposite of the standard simplex is the same simplex by vertex reversal. -/
@[simps! hom_app_hom_apply inv_app_hom_apply]
def opIso (n : SimplexCategory) :
    (stdSimplex.{u}.obj n).op ≅ stdSimplex.obj n :=
  NatIso.ofComponents (fun d ↦ stdSimplex.opObjEquiv.toIso) (fun {d d'} f ↦ by
    ext g
    refine stdSimplex.ext _ _ (fun i ↦ ?_)
    dsimp
    rw [stdSimplex.opObjEquiv_apply, op_map]
    erw [Equiv.apply_symm_apply]
    dsimp
    rw [map_rev_map_op_apply]
    aesop)

end stdSimplex

/-- The simplicial opposite functor preserves the cartesian monoidal structure. -/
instance : opFunctor.{u}.Monoidal :=
  Functor.CoreMonoidal.toMonoidal
    { εIso := Iso.refl _
      μIso _ _ := Iso.refl _ }

namespace Subcomplex

variable {X Y : SSet.{u}} (S : X.Subcomplex) (T : Y.Subcomplex)

lemma preimage_op_unionProd :
    (unionProd S T).op.preimage (Functor.LaxMonoidal.μ opFunctor _ _) =
      unionProd S.op T.op := rfl

lemma preimage_unionProd {X' Y' : SSet.{u}} (f : X' ⟶ X) (g : Y' ⟶ Y) :
    (unionProd S T).preimage (f ⊗ₘ g) =
      unionProd (S.preimage f) (T.preimage g) := rfl

end Subcomplex

private lemma mem_horn_iff_notMem_range {n d : ℕ} (s : Δ[n] _⦋d⦌)
    (i : Fin (n + 1)) :
    s ∈ (horn.{u} n i).obj _ ↔ ∃ (j : Fin (n + 1)) (_ : j ≠ i), j ∉ Set.range s := by
  simp [horn_eq_iSup]

private lemma mem_boundary_iff_notMem_range {n d : ℕ} (s : Δ[n] _⦋d⦌) :
    s ∈ (boundary n).obj _ ↔ ∃ (j : Fin (n + 1)), j ∉ Set.range s := by
  rw [boundary_eq_iSup]
  simp

lemma op_horn {n : ℕ} (i : Fin (n + 1)) :
    Λ[n, i].op.preimage (stdSimplex.opIso.{u} ⦋n⦌).inv = Λ[n, i.rev] := by
  ext ⟨⟨d⟩⟩ j
  simp only [Subcomplex.preimage_obj, Set.mem_preimage,
    stdSimplex.opIso_inv_app_hom_apply,
    Subcomplex.mem_op_obj_iff, mem_horn_iff_notMem_range, Set.mem_range,
    not_exists, ne_eq, exists_prop, stdSimplex.opObjEquiv_opObjEquiv_symm_apply]
  constructor
  · rintro ⟨k, h₁, h₂⟩
    exact ⟨k.rev, by simpa, fun l hl ↦ by grind [h₂ l.rev]⟩
  · rintro ⟨k, h₁, h₂⟩
    exact ⟨k.rev, by grind⟩

lemma op_boundary (n : ℕ) :
    ∂Δ[n].op.preimage (stdSimplex.opIso.{u} ⦋n⦌).inv = ∂Δ[n] := by
  ext ⟨⟨d⟩⟩ j
  simp only [Subcomplex.preimage_obj, Set.mem_preimage,
    stdSimplex.opIso_inv_app_hom_apply, Subcomplex.mem_op_obj_iff,
    mem_boundary_iff_notMem_range, Set.mem_range,
    stdSimplex.opObjEquiv_opObjEquiv_symm_apply, not_exists]
  constructor
  all_goals
  · rintro ⟨k, hk⟩
    exact ⟨k.rev, fun l _ ↦ hk l.rev (by aesop)⟩

end SSet
