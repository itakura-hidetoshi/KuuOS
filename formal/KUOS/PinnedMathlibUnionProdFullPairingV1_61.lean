/-
Copyright (c) 2026 Joël Riou. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Joël Riou
-/

import KUOS.PinnedMathlibUnionProdOpSymmetryV1_61

/-!
# Complete combinatorial UnionProd pairing at the fixed mathlib pin

Additive port of the terminal part of Joël Riou's UnionProd proof
(mathlib4 commit 27e085939a074823b4c553fc5d7543a8ce2708b0).
The existing locally proved pairingCore, weak rank, regularity and innerness
are reused unchanged. The last-index case is obtained by the now-explicit
opposite simplex isomorphism, never by an unproved API assumption.
The ordinary simplicial anodyne conclusion is kept distinct from scaled
horn descent, which is NOT proved by this file.
-/

universe u
open CategoryTheory MonoidalCategory Simplicial

namespace SSet
namespace prodStdSimplex

set_option backward.isDefEq.respectTransparency false in
/-- The full regular pairing for a horn-boundary union product, including the
last vertex (handled by reversal). -/
noncomputable def pairing {m : ℕ} (k : Fin (m + 2)) (n : ℕ) :
    (Subcomplex.unionProd.{u} Λ[m + 1, k] ∂Δ[n]).Pairing :=
  if hk : k = Fin.last (m + 1) then
    (pairingCore (0 : Fin (m + 1)) n).pairing.op.ofIso
      (((stdSimplex.opIso _).symm ⊗ᵢ (stdSimplex.opIso _).symm) ≪≫
        Functor.Monoidal.μIso opFunctor _ _) (by
          dsimp
          rw [hk, Subcomplex.preimage_comp,
            Subcomplex.preimage_op_unionProd,
            Subcomplex.preimage_unionProd,
            op_boundary, op_horn, Fin.rev_zero])
  else
    (pairingCore.{u} (k.castPred hk) n).pairing

lemma pairing_castSucc {m : ℕ} (k : Fin (m + 1)) (n : ℕ) :
    pairing.{u} k.castSucc n = (pairingCore.{u} k n).pairing :=
  dif_neg (by grind)

instance {m : ℕ} (k : Fin (m + 2)) (n : ℕ) :
    (pairing.{u} k n).IsRegular := by
  by_cases! hk : k = Fin.last (m + 1)
  · subst hk
    dsimp only [pairing]
    rw [dif_pos rfl]
    infer_instance
  · obtain ⟨k, rfl⟩ := Fin.eq_castSucc_of_ne_last hk
    rw [pairing_castSucc]
    infer_instance

instance {m : ℕ} (k : Fin m) (n : ℕ) :
    (pairing.{u} k.castSucc.succ n).IsInner := by
  simp only [← Fin.castSucc_succ, pairing_castSucc]
  infer_instance

/-- All horn-by-boundary union products are strong anodyne inclusions. -/
theorem unionProd_strongAnodyne {m : ℕ} (k : Fin (m + 2)) (n : ℕ) :
    strongAnodyneExtensions
      (Subcomplex.unionProd.{u} Λ[m + 1, k] ∂Δ[n]).ι :=
  (pairing.{u} k n).strongAnodyneExtensions

/-- The ordinary simplicial horn-by-boundary union product is anodyne. -/
theorem unionProd_anodyne {m : ℕ} (k : Fin (m + 2)) (n : ℕ) :
    anodyneExtensions
      (Subcomplex.unionProd.{u} Λ[m + 1, k] ∂Δ[n]).ι :=
  (pairing.{u} k n).anodyneExtensions

#print axioms unionProd_strongAnodyne
#print axioms unionProd_anodyne

end prodStdSimplex
end SSet
