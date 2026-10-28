import Kuu.F112.PolygonNativeC60AQFullPentagonArbitraryFiniteBlockTower

/-!
# F112-P94D3EQ — finite-list coordinate normalization for true C60 AQ towers

This continuation constructs a canonical finite tuple partition for
EVERY list of nonnegative block ranks. It is independent of chosen
obstruction-kernel representatives: Fin (ranks.sum) integer charges
are split using the existing EK finite-coordinate group isomorphism.

The genuine recursively split C60 AQ tower is then flattened by
group isomorphisms into a product of the concrete ordered finite
integer-charge tuple and the original cumulative character kernel.
The only reassociation of residual indices is Nat.add_assoc.

The construction does not postulate equality with the one-stage EJ
split: we retain the genuinely separately defined one-stage map for
a subsequent coherence theorem. Neither source noncommutative-kernel
abelianity, infinite product/splitting, Gray nor a geometric 19D
C60 Type-valued filler is introduced. Strict Kuu, independent Kuu
as presentation, DS no-go, all 14D--18D evidence, 107 public roots
and fixed Lean/mathlib are preserved.
No new axioms, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

section FiniteIntegerCoordinateTowers

/-- The ordered, finite integer-coordinate tower with NO artificial
infinite product. The empty tower is the genuine rank-zero integer
receiver, whose unique vector is the group identity. -/
def nativeC60EQChargeTower : List ℕ → Type
  | [] => (Fin 0 → Multiplicative ℤ)
  | rank :: tail =>
      (Fin rank → Multiplicative ℤ) × nativeC60EQChargeTower tail

instance nativeC60EQChargeTowerGroup (ranks : List ℕ) :
    Group (nativeC60EQChargeTower ranks) := by
  induction ranks with
  | nil =>
      change Group (Fin 0 → Multiplicative ℤ)
      infer_instance
  | cons rank tail ih =>
      change Group ((Fin rank → Multiplicative ℤ) ×
        nativeC60EQChargeTower tail)
      letI : Group (nativeC60EQChargeTower tail) := ih
      infer_instance

/-- An independent, canonical finite partition of the complete
rank-sum integer receiver into an arbitrary finite list of blocks.
Every step uses EK's true Fin-coordinate split; the empty case is
literally Fin 0 and includes no selected group representatives. -/
def nativeC60EQFiniteCoordinatePartition :
    (ranks : List ℕ) →
      (Fin ranks.sum → Multiplicative ℤ) ≃*
        nativeC60EQChargeTower ranks
  | [] => MulEquiv.refl (Fin 0 → Multiplicative ℤ)
  | rank :: tail =>
      (nativeC60EKFiniteCoordinateSplit rank tail.sum).trans
        (MulEquiv.prodCongr
          (MulEquiv.refl (Fin rank → Multiplicative ℤ))
          (nativeC60EQFiniteCoordinatePartition tail))

/-- The complete first rank block is recovered literally by the
list partition. This is independent of all kernel splitting data. -/
theorem nativeC60EQFiniteCoordinatePartition_head
    (rank : ℕ) (tail : List ℕ)
    (v : Fin (rank + tail.sum) → Multiplicative ℤ) :
    (nativeC60EQFiniteCoordinatePartition (rank :: tail) v).1 =
      (fun i => v (Fin.castAdd tail.sum i)) := by
  rfl

/-- Finite-coordinate normalization is an honest bijection for
arbitrary list length; this does NOT invoke ℤ^ℕ surjectivity. -/
theorem nativeC60EQFiniteCoordinatePartition_bijective
    (ranks : List ℕ) :
    Function.Bijective (nativeC60EQFiniteCoordinatePartition ranks) :=
  (nativeC60EQFiniteCoordinatePartition ranks).bijective

end FiniteIntegerCoordinateTowers

section GenuineAQFiniteListNormalization

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Rank reassociation transported within the same genuine
C60 AQ kernel family. There is no quotient identification. -/
def nativeC60EQResidualRankAssoc (word : List Bool)
    (start rank tailSum : ℕ) :
    (nativeC60EBAbelianReceiver S F word ((start + rank) + tailSum)).ker ≃*
      (nativeC60EBAbelianReceiver S F word
        (start + (rank + tailSum))).ker := by
  rw [← Nat.add_assoc start rank tailSum]

/-- Flatten the ACTUAL recursively constructed EJ finite list
tower to an explicitly ordered, finite integer-coordinate group
and the honest final residual subgroup. This map is constructed
independently of the one-stage receiver below. -/
def nativeC60EQFlattenTower (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) :
    (ranks : List ℕ) →
      nativeC60EQBlocks S F word start ranks ≃*
        nativeC60EQChargeTower ranks ×
          (nativeC60EBAbelianReceiver S F word
            (start + ranks.sum)).ker
  | [] => nativeC60EJCumulativeDirectProduct S F word r start 0
  | rank :: tail =>
      ((MulEquiv.prodCongr
          (MulEquiv.refl (Fin rank → Multiplicative ℤ))
          (nativeC60EQFlattenTower word r (start + rank) tail)).trans
        (MulEquiv.prodAssoc).symm).trans
        (MulEquiv.prodCongr
          (MulEquiv.refl (nativeC60EQChargeTower (rank :: tail)))
          (nativeC60EQResidualRankAssoc S F word start rank tail.sum))

/-- Fully normalized, genuine FINITE LIST sequential splitting.
The first map iterates the actual EJ group splittings. The second
independently flattens the resulting nested finite block tower. -/
def nativeC60EQSequentialNormalForm (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (ranks : List ℕ) :
    (nativeC60EBAbelianReceiver S F word start).ker ≃*
      nativeC60EQChargeTower ranks ×
        (nativeC60EBAbelianReceiver S F word
          (start + ranks.sum)).ker :=
  (nativeC60EQIteratedDirectProduct S F word r start ranks).trans
    (nativeC60EQFlattenTower S F word r start ranks)

/-- The independent ONE-STEP canonical split deletes exactly
ranks.sum actual AQ charges by EJ, then uses the independently
constructed rank-list integer partition. It has precisely the
same domain and codomain as the sequential construction. -/
def nativeC60EQOneStepNormalForm (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (ranks : List ℕ) :
    (nativeC60EBAbelianReceiver S F word start).ker ≃*
      nativeC60EQChargeTower ranks ×
        (nativeC60EBAbelianReceiver S F word
          (start + ranks.sum)).ker :=
  (nativeC60EJCumulativeDirectProduct S F word r start ranks.sum).trans
    (MulEquiv.prodCongr
      (nativeC60EQFiniteCoordinatePartition ranks)
      (MulEquiv.refl
        ((nativeC60EBAbelianReceiver S F word
          (start + ranks.sum)).ker)))

/-- The one-stage normal form has the genuine, unchanged cumulative
AQ residual as its second coordinate. No artificial fiber is added. -/
theorem nativeC60EQOneStepNormalForm_residual (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (ranks : List ℕ)
    (x : (nativeC60EBAbelianReceiver S F word start).ker) :
    (nativeC60EQOneStepNormalForm S F word r start ranks x).2 =
      (nativeC60EJCumulativeDirectProduct
        S F word r start ranks.sum x).2 := by
  rfl

end GenuineAQFiniteListNormalization

#print axioms nativeC60EQChargeTower
#print axioms nativeC60EQFiniteCoordinatePartition
#print axioms nativeC60EQFiniteCoordinatePartition_head
#print axioms nativeC60EQFlattenTower
#print axioms nativeC60EQSequentialNormalForm
#print axioms nativeC60EQOneStepNormalForm
#print axioms nativeC60EQOneStepNormalForm_residual

end
end Kuu.F112.Physical
