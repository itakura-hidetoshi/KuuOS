/-
Copyright (c) 2026 Joël Riou. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Joël Riou
-/

import KUOS.PinnedMathlibUnionProdInnerPairingCoreV1_61

/-!
# Pinned-mathlib UnionProd: regularity of the pairing core

Additive reconstruction of the upstream weak-rank argument (2026-06-03,
27e085939a074823b4c553fc5d7543a8ce2708b0), against pinned
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.

This concerns only pairingCore, NOT the full reversed-endpoint pairing,
the complete UnionProd theorem, or the scaled horn descent.
-/

section
universe u
open CategoryTheory MonoidalCategory Simplicial
namespace SSet
namespace prodStdSimplex
open pairingCore

set_option backward.isDefEq.respectTransparency false in
/-- A weak rank function for `pairingCore k n`. -/
noncomputable def weakRankFunction {m : ℕ} (k : Fin (m + 1)) (n : ℕ) :
    (pairingCore.{u} k n).WeakRankFunction ℕ where
  rank s := (finset s.x rfl).card
  lt := by
    intro ⟨s, d, hds, is, hs⟩ ⟨t, d', hdt, it, ht⟩ ⟨h₁, h₂⟩ h₃
    obtain ⟨ds, s, hs₁, hs₂, rfl⟩ := Subcomplex.N.mk_surjective s
    obtain ⟨dt, t, ht₁, ht₂, rfl⟩ := Subcomplex.N.mk_surjective t
    obtain rfl : d = d' := h₃
    obtain rfl : ds = d + 1 := hds
    obtain rfl : dt = d + 1 := hdt
    simp only [ne_eq, pairingCore_ι, Type₁.ext_iff] at h₁
    obtain ⟨f, hf, hδ⟩ := N.le_iff_exists_mono.1 h₂.le
    dsimp at f hf
    obtain ⟨i, rfl⟩ := SimplexCategory.eq_δ_of_mono f
    obtain rfl | rfl := ht.eq_of_isType₂_δ hs.isType₂_δ i (by
      rw [S.ext_iff']
      exact ⟨rfl, hδ.symm⟩)
    · refine (h₁ (hs.δ_injective ht ?_)).elim
      rw [Subcomplex.N.ext_iff, N.ext_iff, S.ext_iff']
      exact ⟨rfl, hδ.symm⟩
    · let Ss := finset (Subcomplex.N.mk s hs₁ hs₂) rfl
      let St := finset (Subcomplex.N.mk t ht₁ ht₂) rfl
      let Sδ := finset hs.δ rfl
      replace hδ (i : Fin (d + 1)) :
          s.1 (is.castSucc.succAbove i) = t.1 (it.succ.succAbove i) :=
        DFunLike.congr_fun (congr_arg Prod.fst hδ.symm) i
      have hSs (i : Fin (d + 1)) : i ∈ Sδ ↔ is.castSucc.succAbove i ∈ Ss := by
        simp [Sδ, Ss, stdSimplex.δ_apply]
      have hSt (i : Fin (d + 1)) : i ∈ Sδ ↔ it.succ.succAbove i ∈ St := by
        simp [Sδ, St, stdSimplex.δ_apply, hδ]
      suffices Ss.card = Sδ.card ∧ St.card = Sδ.card + 1 by grind
      constructor
      · suffices Ss = Finset.image is.castSucc.succAbove Sδ by
          rw [this]
          exact Finset.card_image_of_injective _ Fin.succAbove_right_injective
        ext i
        obtain rfl | ⟨i, rfl⟩ := is.castSucc.eq_self_or_eq_succAbove i
        · have : is.castSucc ∉ Ss := fun h ↦ by
            have : s.1 is.castSucc ≤ k.castSucc := by
              simpa using (hs.simplex_fst_le_castSucc_iff is.castSucc).2 (by simp)
            simp_all [Ss]
          simpa
        · simp [hSs]
      · suffices St = Finset.image it.succ.succAbove Sδ ∪ {it.succ} by
          rw [this, Finset.card_union_of_disjoint (by simp),
            Finset.card_image_of_injective _ Fin.succAbove_right_injective,
            Finset.card_singleton]
        ext i
        obtain rfl | ⟨i, rfl⟩ := it.succ.eq_self_or_eq_succAbove i
        · have : it.succ ∈ St := by
            simpa [St, mem_finset_iff] using ht.simplex_fst_succ
          simp [hSt, this]
        · simp [hSt]

/-! The pinned Rank API lacks the later `PairingCore.WeakRankFunction.isRegular`
lemma. Properness of the core remains an explicit, separate proof obligation. -/

/-- Conditional regularity from the weak rank, without assuming a
nonexistent pinned API or claiming properness of this particular core. -/
theorem pairingCore_isRegular_of_proper {m : ℕ} (k : Fin (m + 1)) (n : ℕ)
    [(pairingCore.{u} k n).IsProper] :
    (pairingCore.{u} k n).IsRegular where
  wf := by
    let h := pairingCore.{u} k n
    have hwf : WellFounded h.pairing.AncestralRel :=
      ((h.weakRankFunctionEquiv ℕ) (weakRankFunction.{u} k n)).wf_ancestralRel
    rw [wellFounded_iff_isEmpty_descending_chain] at hwf ⊢
    exact ⟨fun ⟨f, hf⟩ ↦ hwf.false
      ⟨fun j ↦ h.equivII (f j), fun j ↦
        (h.ancestralRel_iff _ _).1 (hf j)⟩⟩


#print axioms weakRankFunction
#print axioms pairingCore_isRegular_of_proper

end prodStdSimplex
end SSet
end
