import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteListCoordinateNormalization

/-!
# F112-P94D3EQ — strict coherence for arbitrary finite AQ rank-block lists

The preceding files gave TWO INDEPENDENT concrete group equivalences:
(1) sequentially apply the genuine EJ splitting for each block, then
    flatten the resulting typed tower using finite coordinate products;
(2) apply EJ ONCE at the total finite rank, then partition the genuine
    Fin-sum receiver by a recursively defined EK coordinate splitting.

This file compares them by structural induction on an arbitrary
finite list of natural-number block ranks. The induction step reduces
the entire comparison to EM's previously verified equality of the
REAL two-stage and one-stage splits, not to an assumed residual
identification. The final kernel stays the actual C60 AQ abelianized
receiver kernel C_(start + ranks.sum).

All blocks and residual fibers are preserved pointwise, including
empty lists and zero blocks, with no bound on finite list length.
No original noncommutative AQ kernel abelianity, infinite-product
surjection or splitting, Gray category or 19D geometric Type-valued
filler is claimed. Retain strict Kuu, the independent Kuu presentation,
DS complete-evidence no-go, original 14D--18D histories, 107 public
roots, pinned Lean/mathlib, append-only/same-root. No new axiom,
sorry or admit. Copyright Hidetoshi Itakura / 板倉英俊.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

section ArbitraryFiniteListCoherence

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The same explicit partition is applied to both EK diagrams:
their finite first block is left alone, the remaining finite integer
vector is partitioned by the actual recursive Fin split, and the
typed cumulative residual subgroup is unchanged. -/
private def nativeC60EQConsPartitionPost (word : List Bool)
    (start rank : ℕ) (tail : List ℕ) :
    ((Fin rank → Multiplicative ℤ) ×
      ((Fin tail.sum → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F word
          (start + (rank + tail.sum))).ker)) ≃*
      (nativeC60EQChargeTower (rank :: tail) ×
        (nativeC60EBAbelianReceiver S F word
          (start + (rank + tail.sum))).ker) :=
  (MulEquiv.prodCongr
    (MulEquiv.refl (Fin rank → Multiplicative ℤ))
    (MulEquiv.prodCongr
      (nativeC60EQFiniteCoordinatePartition tail)
      (MulEquiv.refl
        ((nativeC60EBAbelianReceiver S F word
          (start + (rank + tail.sum))).ker)))).trans
    (MulEquiv.prodAssoc).symm

/-- MAIN EQ FINITE-LIST COHERENCE: the SEQUENTIALLY split genuine
AQ kernel at arbitrary finite block ranks and the ONE-STEP split
at the total rank have exactly identical true integer coordinates
and residual elements after the independent canonical Fin partition.
No comparison map is postulated as an identity. -/
theorem nativeC60EQSequentialNormalForm_eq_oneStep (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (ranks : List ℕ) :
    nativeC60EQSequentialNormalForm S F word r start ranks =
      nativeC60EQOneStepNormalForm S F word r start ranks := by
  induction ranks generalizing start with
  | nil =>
      apply MulEquiv.ext
      intro x
      rfl
  | cons rank tail ih =>
      apply MulEquiv.ext
      intro x
      let e := nativeC60EJCumulativeDirectProduct S F word r start rank
      let a0 := (e x).1
      let y := (e x).2
      let cast := nativeC60EQResidualRankAssoc S F word start rank tail.sum
      let post := nativeC60EQConsPartitionPost S F word start rank tail
      have htail :
          nativeC60EQSequentialNormalForm S F word r
            (start + rank) tail y =
          nativeC60EQOneStepNormalForm S F word r
            (start + rank) tail y :=
        DFunLike.congr_fun (ih (start + rank)) y
      have hEM :=
        nativeC60EMTwoStage_eq_OneStage
          S F word r start rank tail.sum x
      have hbase :
          nativeC60EQSequentialNormalForm S F word r
            start (rank :: tail) x =
          ((a0,
              (nativeC60EQOneStepNormalForm S F word r
                (start + rank) tail y).1),
             cast ((nativeC60EQOneStepNormalForm S F word r
                (start + rank) tail y).2)) := by
        calc
          nativeC60EQSequentialNormalForm S F word r start (rank :: tail) x =
              ((a0,
                (nativeC60EQSequentialNormalForm S F word r
                  (start + rank) tail y).1),
               cast ((nativeC60EQSequentialNormalForm S F word r
                  (start + rank) tail y).2)) := by rfl
          _ = ((a0,
                (nativeC60EQOneStepNormalForm S F word r
                  (start + rank) tail y).1),
               cast ((nativeC60EQOneStepNormalForm S F word r
                  (start + rank) tail y).2)) := by rw [htail]
      have hpost :
          ((a0,
              (nativeC60EQOneStepNormalForm S F word r
                (start + rank) tail y).1),
             cast ((nativeC60EQOneStepNormalForm S F word r
                (start + rank) tail y).2)) =
          post (nativeC60EKTwoStage S F word r start rank tail.sum x) := by
        rfl
      have hlast :
          post (nativeC60EKOneStage S F word r start rank tail.sum x) =
            nativeC60EQOneStepNormalForm S F word r start (rank :: tail) x := by
        rfl
      exact hbase.trans (hpost.trans ((congrArg post hEM).trans hlast))

/-- Every arbitrary FINITE decomposition comparison is literally
the identity group equivalence on the full finite integer coordinate
tower TIMES THE ACTUAL cumulative AQ residual subgroup. -/
theorem nativeC60EQFiniteListComparison_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (ranks : List ℕ) :
    (nativeC60EQOneStepNormalForm S F word r start ranks).symm.trans
      (nativeC60EQSequentialNormalForm S F word r start ranks) =
      MulEquiv.refl
        (nativeC60EQChargeTower ranks ×
          (nativeC60EBAbelianReceiver S F word
            (start + ranks.sum)).ker) := by
  apply MulEquiv.ext
  intro p
  change nativeC60EQSequentialNormalForm S F word r start ranks
      ((nativeC60EQOneStepNormalForm S F word r start ranks).symm p) = p
  rw [nativeC60EQSequentialNormalForm_eq_oneStep]
  exact MulEquiv.apply_symm_apply
    (nativeC60EQOneStepNormalForm S F word r start ranks) p

/-- There is no remaining residual fiber automorphism after any
finite number of actual AQ deletions: the group element itself is
unchanged, not only its observed integer charges. -/
theorem nativeC60EQFiniteListResidual_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (ranks : List ℕ)
    (v : nativeC60EQChargeTower ranks)
    (z : (nativeC60EBAbelianReceiver S F word
      (start + ranks.sum)).ker) :
    (((nativeC60EQOneStepNormalForm S F word r start ranks).symm.trans
      (nativeC60EQSequentialNormalForm S F word r start ranks))
        (v, z)).2 = z := by
  rw [nativeC60EQFiniteListComparison_id]
  rfl

end ArbitraryFiniteListCoherence

section PhysicalC60AU

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- True physical dependent C60 AU evidence provides the strict
arbitrary-finite-block comparison, preserving every genuine
integer coordinate and residual obstruction class. -/
theorem nativeK5EQPhysicalAQ_finiteListCoherence_id
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree)
    (start : ℕ) (ranks : List ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let r := nativeC60DYOriginalZigzagGen S F
      (nativeK5CEPhysicalAUGenerator W)
    (nativeC60EQOneStepNormalForm S F
      (nativeK5DOTreeWord tree) r start ranks).symm.trans
      (nativeC60EQSequentialNormalForm S F
        (nativeK5DOTreeWord tree) r start ranks) =
      MulEquiv.refl
        (nativeC60EQChargeTower ranks ×
          (nativeC60EBAbelianReceiver S F
            (nativeK5DOTreeWord tree) (start + ranks.sum)).ker) := by
  dsimp only
  exact nativeC60EQFiniteListComparison_id
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) start ranks

end PhysicalC60AU

#print axioms nativeC60EQSequentialNormalForm_eq_oneStep
#print axioms nativeC60EQFiniteListComparison_id
#print axioms nativeC60EQFiniteListResidual_id
#print axioms nativeK5EQPhysicalAQ_finiteListCoherence_id

end
end Kuu.F112.Physical
