import Kuu.F112.PolygonNativeC60AQFullPentagonPartitionGroupoid

/-!
# F112-P94D3ES — arbitrary finite paths of genuine AQ rank repartitionings

ER constructs a canonical equivalence between ANY two finite ordered
rank partitions with equal total rank, without losing any original
finite C60 AQ integer charge or the underlying residual obstruction.
ES proves its strict groupoid identity, composition and inverse laws.

Here a Type-valued finite PATH records an arbitrary finite sequence
of compatible rank repartitioning steps. The path is not a new
higher-dimensional C60 geometric filling: every step is the
previously verified ER equality-of-total-rank coordinate change.
Its composite is independently defined by recursion, and then
proved equal to the SINGLE endpoint canonical comparison using
the verified ES composition law. Thus any TWO paths with the same
endpoints have identical group isomorphisms and identical effects
on all integer coordinates and the actual residual subgroup.

The original noncommutative C60 AQ obstruction kernel is never
declared abelian or free; no infinite-rank splitting or full
infinite-product surjection, geometric 19D filler, or Gray category.
Retain strict Kuu and independent Kuu presentation, historical
DS no-go and 14D--18D Type-valued evidence, all 107 public roots,
pinned Lean/mathlib, same-root and append-only. No axiom, sorry or admit.
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

/-- Genuine ordered finite AQ rank-partition paths. A step is
admissible ONLY with a proof that the finite total integer rank
is preserved, and the path is truly finite by inductive syntax. -/
inductive NativeC60ESPartitionPath : List ℕ → List ℕ → Type where
  | refl (xs : List ℕ) : NativeC60ESPartitionPath xs xs
  | step {xs ys zs : List ℕ} (h : xs.sum = ys.sum)
      (tail : NativeC60ESPartitionPath ys zs) :
      NativeC60ESPartitionPath xs zs

/-- Every genuinely finite repartition path preserves exactly the
original total finite receiver rank, without any completion axiom. -/
def nativeC60ESPathRankEq {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) : xs.sum = ys.sum := by
  induction p with
  | refl _ => rfl
  | step h tail ih => exact h.trans ih

section ActualAQPathAction

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Independently compose the ACTUAL finite C60 AQ repartition
group equivalences along a Type-valued finite partition path.
The final factor at every vertex is the true cumulative kernel
of the original abelianized noncommutative AQ obstruction. -/
def nativeC60ESPathEquiv (word : List Bool) (start : ℕ)
    {xs ys : List ℕ} (p : NativeC60ESPartitionPath xs ys) :
    (nativeC60EQChargeTower xs ×
      (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker) ≃*
    (nativeC60EQChargeTower ys ×
      (nativeC60EBAbelianReceiver S F word (start + ys.sum)).ker) := by
  induction p with
  | refl _ =>
      exact MulEquiv.refl _
  | step h tail ih =>
      exact (nativeC60ERCanonicalRepartition S F word start _ _ h).trans ih

/-- Every finite path of actual AQ repartitionings reduces to the
ONE canonical endpoint ER map. The essential induction uses ES's
proved composition law, never an assumed equality of residuals. -/
theorem nativeC60ESPathEquiv_eq_canonical (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    nativeC60ESPathEquiv S F word start p =
      nativeC60ERCanonicalRepartition S F word start xs ys
        (nativeC60ESPathRankEq p) := by
  induction p with
  | refl xs =>
      exact (nativeC60ESCanonicalRepartition_refl S F word r start xs).symm
  | step h tail ih =>
      change
        (nativeC60ERCanonicalRepartition S F word start _ _ h).trans
          (nativeC60ESPathEquiv S F word start tail) =
        nativeC60ERCanonicalRepartition S F word start _ _
          (h.trans (nativeC60ESPathRankEq tail))
      rw [ih]
      exact nativeC60ESCanonicalRepartition_comp S F word r start _ _ _
        h (nativeC60ESPathRankEq tail)

/-- The path action commutes with the independently defined true
sequential EQ splitting, for any finite path and any physical
original abelianized AQ comparison-kernel element. -/
theorem nativeC60ESPathEquiv_natural (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    (nativeC60EQSequentialNormalForm S F word r start xs).trans
      (nativeC60ESPathEquiv S F word start p) =
    nativeC60EQSequentialNormalForm S F word r start ys := by
  rw [nativeC60ESPathEquiv_eq_canonical S F word r start p]
  exact nativeC60ERSequential_naturality S F word r start xs ys
    (nativeC60ESPathRankEq p)

/-- MAIN ES FINITE-PATH INDEPENDENCE: any TWO actual finite
repartition paths between the same ordered rank partitions give
literally equal group isomorphisms on all receiver coordinates
and their genuine final C60 AQ residual-kernel elements. -/
theorem nativeC60ESPathEquiv_independent (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p q : NativeC60ESPartitionPath xs ys) :
    nativeC60ESPathEquiv S F word start p =
      nativeC60ESPathEquiv S F word start q := by
  rw [nativeC60ESPathEquiv_eq_canonical S F word r start p,
      nativeC60ESPathEquiv_eq_canonical S F word r start q]
  have h : nativeC60ESPathRankEq p = nativeC60ESPathRankEq q :=
    Subsingleton.elim _ _
  rw [h]

/-- Every closed finite repartition loop has identity monodromy,
even on the residual subgroup: there is no hidden residual
holonomy generated by finite AQ rebracketings. -/
theorem nativeC60ESPathEquiv_loop_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (xs : List ℕ)
    (p : NativeC60ESPartitionPath xs xs) :
    nativeC60ESPathEquiv S F word start p =
      MulEquiv.refl
        (nativeC60EQChargeTower xs ×
          (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker) := by
  rw [nativeC60ESPathEquiv_eq_canonical S F word r start p]
  have h : nativeC60ESPathRankEq p = rfl :=
    Subsingleton.elim _ _
  rw [h]
  exact nativeC60ESCanonicalRepartition_refl S F word r start xs

/-- Each finite path preserves an ACTUAL residual C60 AQ kernel
element, not just the finite integer receiver coordinates. -/
theorem nativeC60ESPathEquiv_residual (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys)
    (z : nativeC60EQChargeTower xs ×
      (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker) :
    ((nativeC60ESPathEquiv S F word start p z).2).1 = z.2.1 := by
  rw [nativeC60ESPathEquiv_eq_canonical S F word r start p]
  exact nativeC60ERRepartition_residual S F word start xs ys
    (nativeC60ESPathRankEq p) z

end ActualAQPathAction

#print axioms nativeC60ESPathRankEq
#print axioms nativeC60ESPathEquiv
#print axioms nativeC60ESPathEquiv_eq_canonical
#print axioms nativeC60ESPathEquiv_natural
#print axioms nativeC60ESPathEquiv_independent
#print axioms nativeC60ESPathEquiv_loop_id
#print axioms nativeC60ESPathEquiv_residual

end
end Kuu.F112.Physical
