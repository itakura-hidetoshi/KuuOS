import Kuu.F112.PolygonNativeC60AQFullPentagonFinitePartitionRefinement

/-!
# F112-P94D3ES — coherent groupoid of genuine finite C60 AQ partitions

ER constructs an EXPLICIT group equivalence between finite ordered
integer-block lists whose total finite rank is equal. Its construction
unpartitions genuine Fin coordinates, transports their equal rank,
and repartitions without moving the actual C60 AQ residual class.
EQ proves its naturality for independently constructed finite
sequential EJ splittings of the true abelianized obstruction kernel.

ES proves that these concrete maps satisfy groupoid composition,
identity and inverse laws, not merely an abstract groupoid inferred
from the existence of equivalences. All three claims use ER's
verified sequential naturality, so the change of presentation is
independent of intermediate rank partitions.

Every integer charge remains at its original absolute finite
coordinate and the terminal residual remains an actual subgroup of
the abelianization of the ORIGINAL noncommutative C60 AQ kernel.
No infinite-rank split, infinite-product surjectivity, unproved 19D
Type-valued geometric filler, Gray structure, or claim that the
original source kernel is abelian/free is introduced.
Preserve strict Kuu, independent Kuu as a presentation, DS no-go,
14D--18D original Type-valued evidence, 107 public roots, pinned
Lean/mathlib, append-only/same-root/overwrite-forbidden policy.
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

universe u

section FiniteAQPartitionGroupoid

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The EXPLICIT ER canonical comparison is the identity when the
source and target finite block lists coincide. This is proved from
the actual EQ sequential EJ splitting, not postulated as a unit. -/
theorem nativeC60ESCanonicalRepartition_refl (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (xs : List ℕ) :
    nativeC60ERCanonicalRepartition S F word start xs xs rfl =
      MulEquiv.refl
        (nativeC60EQChargeTower xs ×
          (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker) := by
  rw [← nativeC60ERSequential_comparison S F word r start xs xs rfl]
  apply MulEquiv.ext
  intro p
  change
    nativeC60EQSequentialNormalForm S F word r start xs
      ((nativeC60EQSequentialNormalForm S F word r start xs).symm p) = p
  exact (nativeC60EQSequentialNormalForm S F word r start xs).apply_symm_apply p

/-- Composition of TWO ACTUAL canonical ER changes of finite
partitions is the SINGLE canonical comparison of their endpoints.
The intermediate partition neither changes the integer receiver
nor twists any genuine cumulative residual obstruction class. -/
theorem nativeC60ESCanonicalRepartition_comp (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (xs ys zs : List ℕ)
    (hxy : xs.sum = ys.sum) (hyz : ys.sum = zs.sum) :
    (nativeC60ERCanonicalRepartition S F word start xs ys hxy).trans
      (nativeC60ERCanonicalRepartition S F word start ys zs hyz) =
    nativeC60ERCanonicalRepartition S F word start xs zs
      (hxy.trans hyz) := by
  apply MulEquiv.ext
  intro p
  let ex := nativeC60EQSequentialNormalForm S F word r start xs
  obtain ⟨x, rfl⟩ := ex.surjective p
  have hfirst := DFunLike.congr_fun
    (nativeC60ERSequential_naturality S F word r start xs ys hxy) x
  have hsecond := DFunLike.congr_fun
    (nativeC60ERSequential_naturality S F word r start ys zs hyz) x
  have hdirect := DFunLike.congr_fun
    (nativeC60ERSequential_naturality S F word r start xs zs
      (hxy.trans hyz)) x
  change nativeC60ERCanonicalRepartition S F word start xs ys hxy
    (ex x) = nativeC60EQSequentialNormalForm S F word r start ys x
    at hfirst
  change nativeC60ERCanonicalRepartition S F word start ys zs hyz
    (nativeC60EQSequentialNormalForm S F word r start ys x) =
      nativeC60EQSequentialNormalForm S F word r start zs x
    at hsecond
  change nativeC60ERCanonicalRepartition S F word start xs zs
    (hxy.trans hyz) (ex x) =
      nativeC60EQSequentialNormalForm S F word r start zs x
    at hdirect
  change nativeC60ERCanonicalRepartition S F word start ys zs hyz
      (nativeC60ERCanonicalRepartition S F word start xs ys hxy
        (ex x)) =
    nativeC60ERCanonicalRepartition S F word start xs zs
      (hxy.trans hyz) (ex x)
  rw [hfirst, hsecond, hdirect]

/-- The inverse of the genuine ER finite partition comparison is
exactly the canonical comparison with REVERSED finite rank equality.
This is an equality of group isomorphisms, not just of underlying
bijections. -/
theorem nativeC60ESCanonicalRepartition_symm (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (xs ys : List ℕ)
    (hxy : xs.sum = ys.sum) :
    (nativeC60ERCanonicalRepartition S F word start xs ys hxy).symm =
      nativeC60ERCanonicalRepartition S F word start ys xs hxy.symm := by
  apply MulEquiv.ext
  intro p
  let ey := nativeC60EQSequentialNormalForm S F word r start ys
  obtain ⟨x, rfl⟩ := ey.surjective p
  have hforward := DFunLike.congr_fun
    (nativeC60ERSequential_naturality S F word r start xs ys hxy) x
  have hreverse := DFunLike.congr_fun
    (nativeC60ERSequential_naturality S F word r start ys xs hxy.symm) x
  change nativeC60ERCanonicalRepartition S F word start xs ys hxy
      (nativeC60EQSequentialNormalForm S F word r start xs x) = ey x
    at hforward
  change nativeC60ERCanonicalRepartition S F word start ys xs hxy.symm
      (ey x) = nativeC60EQSequentialNormalForm S F word r start xs x
    at hreverse
  change (nativeC60ERCanonicalRepartition S F word start xs ys hxy).symm
    (ey x) =
    nativeC60ERCanonicalRepartition S F word start ys xs hxy.symm (ey x)
  rw [hreverse, ← hforward]
  exact (nativeC60ERCanonicalRepartition S F word start xs ys hxy).symm_apply_apply
    (nativeC60EQSequentialNormalForm S F word r start xs x)

/-- Any two different intermediate partitions with the SAME
finite total rank give literally the SAME canonical endpoint
comparison. This is the elementary diamond for finite AQ
repartitioning: neither path may introduce a residual holonomy. -/
theorem nativeC60ESCanonicalRepartition_diamond (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (xs mid₁ mid₂ zs : List ℕ)
    (h1 : xs.sum = mid₁.sum) (h2 : mid₁.sum = zs.sum)
    (h3 : xs.sum = mid₂.sum) (h4 : mid₂.sum = zs.sum) :
    (nativeC60ERCanonicalRepartition S F word start xs mid₁ h1).trans
      (nativeC60ERCanonicalRepartition S F word start mid₁ zs h2) =
    (nativeC60ERCanonicalRepartition S F word start xs mid₂ h3).trans
      (nativeC60ERCanonicalRepartition S F word start mid₂ zs h4) := by
  rw [nativeC60ESCanonicalRepartition_comp S F word r start xs mid₁ zs h1 h2]
  rw [nativeC60ESCanonicalRepartition_comp S F word r start xs mid₂ zs h3 h4]

end FiniteAQPartitionGroupoid

#print axioms nativeC60ESCanonicalRepartition_refl
#print axioms nativeC60ESCanonicalRepartition_comp
#print axioms nativeC60ESCanonicalRepartition_symm
#print axioms nativeC60ESCanonicalRepartition_diamond

end
end Kuu.F112.Physical
