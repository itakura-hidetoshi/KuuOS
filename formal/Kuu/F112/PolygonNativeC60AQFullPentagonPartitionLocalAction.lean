import Kuu.F112.PolygonNativeC60AQFullPentagonPartitionLocalPaths

/-!
# F112-P94D3ET — genuine C60 AQ actions of locally generated paths

A Type-valued local path uses only adjacent split/merge or rank-zero
insert/delete moves (ET). Its finite ES interpretation is EVALUATED by
the genuine ER group equivalences on the actual finite integer receiver
and the residual subgroup of the original C60 AQ abelianized kernel.

The action is proved equal to the canonical ER endpoint comparison, for
ANY locally generated path. A constructive local path exists for every
equal-total-rank pair; it has that canonical action. Local composition,
reversal, all observed coordinates, residual values, finite path
independence and closed-loop identity follow from previously verified
ER/ES theorems. These are equalities of actions, NOT equalities of
different Type-valued local histories or original high-dimensional cells.

No arbitrary equal-rank generator is added to the ET local syntax.
No claim of infinite splitting, free abelian source, full 19D geometric
filling or Gray structure. Preserve strict Kuu, independent Kuu as a
presentation, DS no-go, 14D--18D evidence and the 107 published roots.
No new axiom, sorry or admit. Pinned Lean/mathlib; append-only/same-root.
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

section FiniteAQLocalPathAction

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Evaluate a finite path of ONLY local moves using the actual
ES recursive composite of true ER receiver/residual group maps. -/
def nativeC60ETLocalPathEquiv (word : List Bool) (start : ℕ)
    {xs ys : List ℕ} (p : NativeC60ETLocalPath xs ys) :
    (nativeC60EQChargeTower xs ×
      (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker) ≃*
    (nativeC60EQChargeTower ys ×
      (nativeC60EBAbelianReceiver S F word (start + ys.sum)).ker) :=
  nativeC60ESPathEquiv S F word start (nativeC60ETLocalToES p)

/-- MAIN ET THEOREM: every finite local history has precisely the
verified ER canonical endpoint action on both genuine integer receiver
coordinates and the original residual AQ obstruction class. -/
theorem nativeC60ETLocalPathEquiv_canonical (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ETLocalPath xs ys) :
    nativeC60ETLocalPathEquiv S F word start p =
      nativeC60ERCanonicalRepartition S F word start xs ys
        (nativeC60ETLocalPath_rankEq p) := by
  exact nativeC60ESPathEquiv_eq_canonical S F word r start
    (nativeC60ETLocalToES p)

/-- The locally generated action commutes with the independently
constructed actual sequential EJ decomposition of the C60 AQ kernel. -/
theorem nativeC60ETLocalPathEquiv_natural (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ETLocalPath xs ys) :
    (nativeC60EQSequentialNormalForm S F word r start xs).trans
      (nativeC60ETLocalPathEquiv S F word start p) =
    nativeC60EQSequentialNormalForm S F word r start ys := by
  exact nativeC60ESPathEquiv_natural S F word r start
    (nativeC60ETLocalToES p)

/-- Finite concatenation of local paths evaluates to composition of
their genuine C60 AQ group equivalences. -/
theorem nativeC60ETLocalPathEquiv_trans (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys zs : List ℕ}
    (p : NativeC60ETLocalPath xs ys)
    (q : NativeC60ETLocalPath ys zs) :
    nativeC60ETLocalPathEquiv S F word start
        (nativeC60ETLocalPath_trans p q) =
      (nativeC60ETLocalPathEquiv S F word start p).trans
        (nativeC60ETLocalPathEquiv S F word start q) := by
  calc
    nativeC60ETLocalPathEquiv S F word start
        (nativeC60ETLocalPath_trans p q) =
      nativeC60ERCanonicalRepartition S F word start xs zs
        (nativeC60ETLocalPath_rankEq (nativeC60ETLocalPath_trans p q)) :=
          nativeC60ETLocalPathEquiv_canonical S F word r start
            (nativeC60ETLocalPath_trans p q)
    _ = (nativeC60ERCanonicalRepartition S F word start xs ys
          (nativeC60ETLocalPath_rankEq p)).trans
        (nativeC60ERCanonicalRepartition S F word start ys zs
          (nativeC60ETLocalPath_rankEq q)) := by
            exact (nativeC60ESCanonicalRepartition_comp S F word r
              start xs ys zs (nativeC60ETLocalPath_rankEq p)
              (nativeC60ETLocalPath_rankEq q)).symm
    _ = (nativeC60ETLocalPathEquiv S F word start p).trans
          (nativeC60ETLocalPathEquiv S F word start q) := by
            rw [nativeC60ETLocalPathEquiv_canonical S F word r start p,
              nativeC60ETLocalPathEquiv_canonical S F word r start q]

/-- Reversing a finite local history reverses its genuine action,
without asserting that the underlying history itself is identified. -/
theorem nativeC60ETLocalPathEquiv_reverse (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ETLocalPath xs ys) :
    nativeC60ETLocalPathEquiv S F word start
        (nativeC60ETLocalPath_reverse p) =
      (nativeC60ETLocalPathEquiv S F word start p).symm := by
  calc
    nativeC60ETLocalPathEquiv S F word start
        (nativeC60ETLocalPath_reverse p) =
      nativeC60ERCanonicalRepartition S F word start ys xs
        (nativeC60ETLocalPath_rankEq (nativeC60ETLocalPath_reverse p)) :=
          nativeC60ETLocalPathEquiv_canonical S F word r start
            (nativeC60ETLocalPath_reverse p)
    _ = (nativeC60ERCanonicalRepartition S F word start xs ys
          (nativeC60ETLocalPath_rankEq p)).symm := by
            exact (nativeC60ESCanonicalRepartition_symm S F word r
              start xs ys (nativeC60ETLocalPath_rankEq p)).symm
    _ = (nativeC60ETLocalPathEquiv S F word start p).symm := by
          rw [nativeC60ETLocalPathEquiv_canonical S F word r start p]

/-- Every locally generated path preserves the ORIGINAL residual C60
AQ abelianized kernel element, not only a replacement abstract factor. -/
theorem nativeC60ETLocalPathEquiv_residual (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ETLocalPath xs ys)
    (z : nativeC60EQChargeTower xs ×
      (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker) :
    ((nativeC60ETLocalPathEquiv S F word start p z).2).1 =
      z.2.1 := by
  exact nativeC60ESPathEquiv_residual S F word r start
    (nativeC60ETLocalToES p) z

/-- Every locally generated path also preserves each absolute finite
integer receiver coordinate (no charge permutation). -/
theorem nativeC60ETLocalPathEquiv_coordinate (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ETLocalPath xs ys)
    (z : nativeC60EQChargeTower xs ×
      (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker)
    (i : Fin xs.sum) :
    ((nativeC60EQFiniteCoordinatePartition ys).symm
      (nativeC60ETLocalPathEquiv S F word start p z).1)
        (Fin.cast (nativeC60ETLocalPath_rankEq p) i) =
    ((nativeC60EQFiniteCoordinatePartition xs).symm z.1) i := by
  rw [nativeC60ETLocalPathEquiv_canonical S F word r start p]
  exact nativeC60ERRepartition_coordinate S F word start xs ys
    (nativeC60ETLocalPath_rankEq p) z i

/-- Two LOCAL histories between the same endpoints have the SAME
action; their Type-valued histories themselves remain distinct. -/
theorem nativeC60ETLocalPathEquiv_independent (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p q : NativeC60ETLocalPath xs ys) :
    nativeC60ETLocalPathEquiv S F word start p =
      nativeC60ETLocalPathEquiv S F word start q := by
  exact nativeC60ESPathEquiv_independent S F word r start
    (nativeC60ETLocalToES p) (nativeC60ETLocalToES q)

/-- Every finite local closed path acts as the IDENTITY, including
on the genuine residual kernel. No finite rank-repartition holonomy. -/
theorem nativeC60ETLocalPathEquiv_loop_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (xs : List ℕ)
    (p : NativeC60ETLocalPath xs xs) :
    nativeC60ETLocalPathEquiv S F word start p =
      MulEquiv.refl
        (nativeC60EQChargeTower xs ×
          (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker) := by
  exact nativeC60ESPathEquiv_loop_id S F word r start xs
    (nativeC60ETLocalToES p)

/-- The CONSTRUCTED local path between any two equal-rank partitions
evaluates to the original ER canonical comparison, even for [] and [0]. -/
theorem nativeC60ETLocalConnect_canonical (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (xs ys : List ℕ) (h : xs.sum = ys.sum) :
    nativeC60ETLocalPathEquiv S F word start
        (nativeC60ETLocalConnect xs ys h) =
      nativeC60ERCanonicalRepartition S F word start xs ys h := by
  exact nativeC60ETLocalPathEquiv_canonical S F word r start
    (nativeC60ETLocalConnect xs ys h)

/-- Local GENERATION of every ER canonical repartitioning: a genuine
finite local path and an equality of its physical AQ action to ER. -/
theorem nativeC60ETCanonical_hasLocalPath (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (xs ys : List ℕ) (h : xs.sum = ys.sum) :
    ∃ p : NativeC60ETLocalPath xs ys,
      nativeC60ETLocalPathEquiv S F word start p =
        nativeC60ERCanonicalRepartition S F word start xs ys h :=
  ⟨nativeC60ETLocalConnect xs ys h,
    nativeC60ETLocalConnect_canonical S F word r start xs ys h⟩

end FiniteAQLocalPathAction

#print axioms nativeC60ETLocalPathEquiv
#print axioms nativeC60ETLocalPathEquiv_canonical
#print axioms nativeC60ETLocalPathEquiv_natural
#print axioms nativeC60ETLocalPathEquiv_trans
#print axioms nativeC60ETLocalPathEquiv_reverse
#print axioms nativeC60ETLocalPathEquiv_residual
#print axioms nativeC60ETLocalPathEquiv_coordinate
#print axioms nativeC60ETLocalPathEquiv_independent
#print axioms nativeC60ETLocalPathEquiv_loop_id
#print axioms nativeC60ETCanonical_hasLocalPath

end
end Kuu.F112.Physical
