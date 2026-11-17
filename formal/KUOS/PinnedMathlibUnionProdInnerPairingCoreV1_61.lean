import KUOS.PinnedMathlibUnionProdProofPortV1_61

/-!
# Pinned UnionProd inner pairing-core witness

This additive module isolates the inner-horn index condition actually used
by the type-(A) boundary-prism construction. It does not assume the
not-yet-certified regularity of the complete UnionProd pairing.
The argument is adapted from the upstream UnionProd proof and keeps
the pinned mathlib and the previously proved pairing core unchanged.
-/

namespace SSet
namespace prodStdSimplex

open pairingCore

universe u

instance {m : ℕ} (k : Fin m) (n : ℕ) :
    (pairingCore.{u} k.succ n).IsInner where
  ne_zero (s : Type₁ k.succ n) h := by
    have hi : s.index = 0 := by
      rwa [← Fin.castSucc_eq_zero_iff]
    have hs : IsIndex s.x s.hd (Fin.succ 0) := by
      simpa [hi] using s.isIndex
    obtain ⟨i, hi0⟩ := mem_range_left s.x s.hd 0
      (fun h => by simp [Fin.ext_iff] at h)
    have h₁ := hs.simplex_fst_castSucc
    dsimp only [Fin.castSucc_zero] at h₁
    have hle : (k.succ.castSucc : Fin (m + 2)) ≤ 0 := by
      calc
        k.succ.castSucc = (s.x.cast s.hd).simplex.1 0 := h₁.symm
        _ ≤ (s.x.cast s.hd).simplex.1 i :=
          stdSimplex.monotone_apply (s.x.cast s.hd).simplex.1 i.zero_le
        _ = 0 := hi0
    have hval : (k.succ.castSucc : Fin (m + 2)).val = k.val + 1 := rfl
    have hleVal : (k.succ.castSucc : Fin (m + 2)).val ≤ 0 := hle
    omega
  ne_last x := by
    dsimp [pairingCore]
    simp

end prodStdSimplex
end SSet
