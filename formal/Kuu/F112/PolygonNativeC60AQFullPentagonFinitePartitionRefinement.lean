import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteListAppendCoherence

/-!
# F112-P94D3ER — canonical finite AQ rank-partition refinements

EQ proved that splitting the true abelianized C60 AQ character kernel
by any finite list of block ranks agrees exactly with a ONE-STAGE EJ
split after a finite integer-coordinate partition. ER compares ANY
TWO ordered finite block lists with the SAME finite total rank.

The comparison is NOT declared to be the identity on differently
typed coordinate towers. Instead it is an explicit group isomorphism
built by unpartitioning the actual finite integer receiver,
reindexing equal finite ranks, and repartitioning. The genuine
cumulative residual kernel is transported only along equality
of the total rank, preserving its underlying abelianization element.

The independently built EQ sequential normal forms are proved
natural for this explicit canonical comparison, so the comparison
is not postulated from their equality. It preserves every integer
charge at the same finite coordinate and every honest residual
obstruction class. In particular splitting one finite block into
two consecutive blocks anywhere in a finite list changes no
physical finite AQ information.

No permutation of distinct ordered charges, infinite product
surjection/splitting, original noncommutative-kernel abelianity,
19D geometric filler or Gray structure is inferred. Strict Kuu
and independent-Kuu presentation, DS no-go, original 14D--18D
evidence, 107 public roots, pinned Lean/mathlib, same-root,
append-only, and overwrite-forbidden boundaries are maintained.
No new axiom, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

section RankReindex

/-- Canonical reindexing between EQUAL finite integer receivers.
The proof is by equality elimination, not a new choice of charges. -/
def nativeC60ERRankCast {m k : ℕ} (h : m = k) :
    (Fin m → Multiplicative ℤ) ≃* (Fin k → Multiplicative ℤ) := by
  cases h
  exact MulEquiv.refl _

/-- The original finite charge is unchanged by a rank cast. -/
theorem nativeC60ERRankCast_coordinate {m k : ℕ} (h : m = k)
    (v : Fin m → Multiplicative ℤ) (i : Fin m) :
    (nativeC60ERRankCast h v) (Fin.cast h i) = v i := by
  cases h
  rfl

end RankReindex

section GenuineAQRankRefinement

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Rank equality induces a genuine group equivalence between
the two honest cumulative AQ receiver kernels. -/
def nativeC60ERResidualCast (word : List Bool) (start : ℕ)
    {m k : ℕ} (h : m = k) :
    (nativeC60EBAbelianReceiver S F word (start + m)).ker ≃*
      (nativeC60EBAbelianReceiver S F word (start + k)).ker := by
  cases h
  exact MulEquiv.refl _

/-- The residual rank cast does not move even one underlying true
abelianized C60 pentagon obstruction class. -/
theorem nativeC60ERResidualCast_val (word : List Bool)
    (start : ℕ) {m k : ℕ} (h : m = k)
    (z : (nativeC60EBAbelianReceiver S F word (start + m)).ker) :
    (nativeC60ERResidualCast S F word start h z).1 = z.1 := by
  cases h
  rfl

/-- Naturality of the ACTUAL EJ finite split under an equality
of finite receiver ranks, including the full genuine residual. -/
theorem nativeC60ERJ_rankNaturality (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {m k : ℕ} (h : m = k)
    (x : (nativeC60EBAbelianReceiver S F word start).ker) :
    (MulEquiv.prodCongr
      (nativeC60ERRankCast h)
      (nativeC60ERResidualCast S F word start h))
      (nativeC60EJCumulativeDirectProduct S F word r start m x) =
      nativeC60EJCumulativeDirectProduct S F word r start k x := by
  cases h
  rfl

/-- Repartition the entire genuine finite-rank INTEGER receiver
without touching its coordinate values. This is a canonical
rebracketing/grouping, never an arbitrary permutation. -/
def nativeC60ERChargeRepartition (left right : List ℕ)
    (h : left.sum = right.sum) :
    nativeC60EQChargeTower left ≃* nativeC60EQChargeTower right :=
  (nativeC60EQFiniteCoordinatePartition left).symm.trans
    ((nativeC60ERRankCast h).trans
      (nativeC60EQFiniteCoordinatePartition right))

/-- The canonical re-partitioning acts on original finite rank-sum
integer receivers by their unchanged charges. -/
theorem nativeC60ERChargeRepartition_apply (left right : List ℕ)
    (h : left.sum = right.sum)
    (v : Fin left.sum → Multiplicative ℤ) :
    nativeC60ERChargeRepartition left right h
      (nativeC60EQFiniteCoordinatePartition left v) =
    nativeC60EQFiniteCoordinatePartition right (nativeC60ERRankCast h v) := by
  change (nativeC60EQFiniteCoordinatePartition right)
    (nativeC60ERRankCast h
      ((nativeC60EQFiniteCoordinatePartition left).symm
        (nativeC60EQFiniteCoordinatePartition left v))) =
    nativeC60EQFiniteCoordinatePartition right (nativeC60ERRankCast h v)
  rw [MulEquiv.symm_apply_apply]

/-- The complete comparison on finite integer coordinate towers
TIMES the ACTUAL cumulative AQ kernel. No replacement by an
abstract residual factor is allowed. -/
def nativeC60ERCanonicalRepartition (word : List Bool)
    (start : ℕ) (left right : List ℕ)
    (h : left.sum = right.sum) :
    (nativeC60EQChargeTower left ×
      (nativeC60EBAbelianReceiver S F word (start + left.sum)).ker) ≃*
    (nativeC60EQChargeTower right ×
      (nativeC60EBAbelianReceiver S F word (start + right.sum)).ker) :=
  MulEquiv.prodCongr
    (nativeC60ERChargeRepartition left right h)
    (nativeC60ERResidualCast S F word start h)

/-- The ONE-STEP EJ normalization is natural for the explicit
canonical rank-sum re-partitioning, rather than merely abstractly
isomorphic after replacing its codomain. -/
theorem nativeC60EROneStep_naturality (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (left right : List ℕ)
    (h : left.sum = right.sum) :
    (nativeC60EQOneStepNormalForm S F word r start left).trans
      (nativeC60ERCanonicalRepartition S F word start left right h) =
    nativeC60EQOneStepNormalForm S F word r start right := by
  apply MulEquiv.ext
  intro x
  have hc := nativeC60ERJ_rankNaturality S F word r start h x
  have hc1 := congrArg Prod.fst hc
  have hc2 := congrArg Prod.snd hc
  change
    nativeC60ERRankCast h
      (nativeC60EJCumulativeDirectProduct S F word r start left.sum x).1 =
      (nativeC60EJCumulativeDirectProduct S F word r start right.sum x).1
    at hc1
  change
    nativeC60ERResidualCast S F word start h
      (nativeC60EJCumulativeDirectProduct S F word r start left.sum x).2 =
      (nativeC60EJCumulativeDirectProduct S F word r start right.sum x).2
    at hc2
  apply Prod.ext
  · change nativeC60ERChargeRepartition left right h
      (nativeC60EQFiniteCoordinatePartition left
        (nativeC60EJCumulativeDirectProduct S F word r start left.sum x).1) =
      nativeC60EQFiniteCoordinatePartition right
        (nativeC60EJCumulativeDirectProduct S F word r start right.sum x).1
    rw [nativeC60ERChargeRepartition_apply, hc1]
  · change nativeC60ERResidualCast S F word start h
      (nativeC60EJCumulativeDirectProduct S F word r start left.sum x).2 =
      (nativeC60EJCumulativeDirectProduct S F word r start right.sum x).2
    exact hc2

/-- MAIN ER THEOREM: the two INDEPENDENTLY built genuine sequential
EQ decompositions commute with the EXPLICIT re-partitioning on every
C60 AQ kernel element, not only the finite observations. -/
theorem nativeC60ERSequential_naturality (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (left right : List ℕ)
    (h : left.sum = right.sum) :
    (nativeC60EQSequentialNormalForm S F word r start left).trans
      (nativeC60ERCanonicalRepartition S F word start left right h) =
    nativeC60EQSequentialNormalForm S F word r start right := by
  calc
    (nativeC60EQSequentialNormalForm S F word r start left).trans
        (nativeC60ERCanonicalRepartition S F word start left right h) =
      (nativeC60EQOneStepNormalForm S F word r start left).trans
        (nativeC60ERCanonicalRepartition S F word start left right h) := by
          rw [nativeC60EQSequentialNormalForm_eq_oneStep]
    _ = nativeC60EQOneStepNormalForm S F word r start right :=
      nativeC60EROneStep_naturality S F word r start left right h
    _ = nativeC60EQSequentialNormalForm S F word r start right :=
      (nativeC60EQSequentialNormalForm_eq_oneStep S F word r start right).symm

/-- The actual comparison between the independently split true
AQ groups IS the explicit coordinate re-partitioning; the
commutative triangle is not being defined to commute. -/
theorem nativeC60ERSequential_comparison (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (left right : List ℕ)
    (h : left.sum = right.sum) :
    (nativeC60EQSequentialNormalForm S F word r start left).symm.trans
      (nativeC60EQSequentialNormalForm S F word r start right) =
    nativeC60ERCanonicalRepartition S F word start left right h := by
  apply MulEquiv.ext
  intro p
  let eLeft := nativeC60EQSequentialNormalForm S F word r start left
  let eRight := nativeC60EQSequentialNormalForm S F word r start right
  obtain ⟨x, rfl⟩ := eLeft.surjective p
  have hnat := DFunLike.congr_fun
    (nativeC60ERSequential_naturality S F word r start left right h) x
  change (eLeft.symm.trans eRight) (eLeft x) =
    nativeC60ERCanonicalRepartition S F word start left right h (eLeft x)
  calc
    (eLeft.symm.trans eRight) (eLeft x) =
        eRight (eLeft.symm (eLeft x)) := rfl
    _ = eRight x := by rw [MulEquiv.symm_apply_apply]
    _ = nativeC60ERCanonicalRepartition S F word start left right h
          (eLeft x) := hnat.symm

/-- No residual obstruction is lost, identified or twisted by
a change of finite block partition. This is EQUALITY of the
underlying genuine abelianized AQ obstruction class. -/
theorem nativeC60ERRepartition_residual (word : List Bool)
    (start : ℕ) (left right : List ℕ)
    (h : left.sum = right.sum)
    (p : nativeC60EQChargeTower left ×
      (nativeC60EBAbelianReceiver S F word (start + left.sum)).ker) :
    ((nativeC60ERCanonicalRepartition S F word start left right h p).2).1 =
      p.2.1 := by
  exact nativeC60ERResidualCast_val S F word start h p.2

/-- Every observed finite integer charge at its SAME absolute
coordinate is unchanged, even though the block grouping is
different; rank equality only supplies Fin.cast of that index. -/
theorem nativeC60ERRepartition_coordinate (word : List Bool)
    (start : ℕ) (left right : List ℕ)
    (h : left.sum = right.sum)
    (p : nativeC60EQChargeTower left ×
      (nativeC60EBAbelianReceiver S F word (start + left.sum)).ker)
    (i : Fin left.sum) :
    ((nativeC60EQFiniteCoordinatePartition right).symm
      (nativeC60ERCanonicalRepartition S F word start left right h p).1)
        (Fin.cast h i) =
      ((nativeC60EQFiniteCoordinatePartition left).symm p.1) i := by
  have heq := nativeC60ERRankCast_coordinate h
    ((nativeC60EQFiniteCoordinatePartition left).symm p.1) i
  change
    ((nativeC60EQFiniteCoordinatePartition right).symm
      (nativeC60ERChargeRepartition left right h p.1))
        (Fin.cast h i) =
      ((nativeC60EQFiniteCoordinatePartition left).symm p.1) i
  change
    ((nativeC60EQFiniteCoordinatePartition right).symm
      (nativeC60EQFiniteCoordinatePartition right
        (nativeC60ERRankCast h
          ((nativeC60EQFiniteCoordinatePartition left).symm p.1))))
        (Fin.cast h i) =
      ((nativeC60EQFiniteCoordinatePartition left).symm p.1) i
  rw [MulEquiv.symm_apply_apply]
  exact heq

/-- Any adjacent pair of finite integer blocks may be grouped
at an arbitrary front and suffix without changing total rank. -/
theorem nativeC60ERAdjacentSum (front suffix : List ℕ) (a b : ℕ) :
    (front ++ (a + b) :: suffix).sum =
      (front ++ a :: b :: suffix).sum := by
  simp only [List.sum_append, List.sum_cons]
  omega

/-- Genuine AQ splitting along the coarse block (a+b) is explicitly
isomorphic to splitting the consecutive blocks a, then b at ANY
place in the finite list. This re-partitioning is canonical and
preserves all integer-charge and residual coordinates. -/
def nativeC60ERAdjacentRefinement (word : List Bool)
    (start : ℕ) (front suffix : List ℕ) (a b : ℕ) :
    (nativeC60EQChargeTower (front ++ (a + b) :: suffix) ×
      (nativeC60EBAbelianReceiver S F word
        (start + (front ++ (a + b) :: suffix).sum)).ker) ≃*
    (nativeC60EQChargeTower (front ++ a :: b :: suffix) ×
      (nativeC60EBAbelianReceiver S F word
        (start + (front ++ a :: b :: suffix).sum)).ker) :=
  nativeC60ERCanonicalRepartition S F word start
    (front ++ (a + b) :: suffix) (front ++ a :: b :: suffix)
    (nativeC60ERAdjacentSum front suffix a b)

/-- Grouping or refining an adjacent finite rank block anywhere
commutes STRICTLY with the true, separately constructed sequential
C60 AQ decomposition. -/
theorem nativeC60ERAdjacentRefinement_naturality (word : List Bool)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen x y)
    (start : ℕ) (front suffix : List ℕ) (a b : ℕ) :
    (nativeC60EQSequentialNormalForm S F word r start
      (front ++ (a + b) :: suffix)).trans
      (nativeC60ERAdjacentRefinement S F word start front suffix a b) =
      nativeC60EQSequentialNormalForm S F word r start
        (front ++ a :: b :: suffix) :=
  nativeC60ERSequential_naturality S F word r start
    (front ++ (a + b) :: suffix) (front ++ a :: b :: suffix)
    (nativeC60ERAdjacentSum front suffix a b)

end GenuineAQRankRefinement

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

/-- Physical C60 AU dependent 18D evidence inherits canonical
finite block regrouping without a new Type-valued filler. -/
theorem nativeK5ERPhysicalAQ_partition_naturality
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree)
    (start : ℕ) (left right : List ℕ)
    (h : left.sum = right.sum) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let r := nativeC60DYOriginalZigzagGen S F
      (nativeK5CEPhysicalAUGenerator W)
    (nativeC60EQSequentialNormalForm S F
      (nativeK5DOTreeWord tree) r start left).trans
      (nativeC60ERCanonicalRepartition S F
        (nativeK5DOTreeWord tree) start left right h) =
      nativeC60EQSequentialNormalForm S F
        (nativeK5DOTreeWord tree) r start right := by
  dsimp only
  exact nativeC60ERSequential_naturality
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) start left right h

end PhysicalC60AU

#print axioms nativeC60ERRankCast
#print axioms nativeC60ERResidualCast
#print axioms nativeC60ERCanonicalRepartition
#print axioms nativeC60EROneStep_naturality
#print axioms nativeC60ERSequential_naturality
#print axioms nativeC60ERSequential_comparison
#print axioms nativeC60ERRepartition_residual
#print axioms nativeC60ERRepartition_coordinate
#print axioms nativeC60ERAdjacentRefinement_naturality
#print axioms nativeK5ERPhysicalAQ_partition_naturality

end
end Kuu.F112.Physical
