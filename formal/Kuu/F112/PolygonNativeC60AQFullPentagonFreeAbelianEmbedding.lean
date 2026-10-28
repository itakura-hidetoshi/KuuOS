import Kuu.F112.PolygonNativeC60AQFullPentagonNonFiniteGeneration
import Mathlib.Algebra.FreeAbelianGroup.Finsupp
import Mathlib.Algebra.Group.TypeTags.Hom

/-!
# F112-P94D3ED — countably generated free abelian subgroup of the actual AQ kernel abelianization

EA constructs ACTUAL, complete Type-valued contextual 18D pentagon
defects indexed by natural-number finite AQ tags. The pairwise
orthogonal integer characters vanish on the transported original
pentagon normal closure. EB embeds these defects in the exact kernel
of the image-to-full comparison and proves integer character
Kronecker evaluation.

ED constructs the canonical finite-support integer sum of the
ABELIANIZED contextual defects:
  (ℕ →₀ ℤ) →+ Additive (Abelianization (ker π_w)).
The construction uses the pinned mathlib free abelian group and its
true isomorphism with finitely supported integer functions.

Every coordinate receiver χ_i induces a Z-valued additive
homomorphism from the actual abelianization. Its value on the
j-th genuine Type-valued defect is the Kronecker delta.
The coordinate receiver composed with the finite-support map
recovers the original integer coefficient at every index.
Consequently, the map is injective: the abelianization CONTAINS an
actual countably generated free abelian subgroup.

The embedding is into the abelianization, not an unjustified
homomorphism from an abelian group into the original noncommutative
kernel. The free-abelian subgroup is not claimed to equal the whole
abelianization, nor is any geometric C60 19D filler produced.
Strict Kuu, independent Kuu as a presentation, prior 14D--18D
Type-valued proof histories, DS no-go, 107 public roots, fixed
Lean/mathlib, no-Gray and append-only rules are retained.
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

section CountableFreeAbelianContextObstructions

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A true dependent 18D contextual pentagon defect at index j,
projected from the original NONCOMMUTATIVE kernel into its
actual group abelianization. -/
def nativeC60EDAbelianizedDefect (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (j : ℕ) :
    Additive (Abelianization ((nativeC60DZImageToFull S F word).ker)) :=
  Additive.ofMul (Abelianization.of
    (nativeC60EBKernelGenerator S F word j r))

/-- An EA integer character restricted to the actual kernel factors
uniquely through its true abelianization, then changes multiplicative
notation back into an additive integer charge. -/
def nativeC60EDAbelianizedCoordinate (word : List Bool) (i : ℕ) :
    Additive (Abelianization ((nativeC60DZImageToFull S F word).ker)) →+ ℤ :=
  (Abelianization.lift
    (nativeC60EBKernelCharacter S F word i)).toAdditiveLeft

/-- The normalized Kronecker evaluation is EXACTLY an integer.
No quotient or commutativity of the original kernel is assumed. -/
theorem nativeC60EDAbelianizedCoordinate_defect (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (i j : ℕ) :
    nativeC60EDAbelianizedCoordinate S F word i
      (nativeC60EDAbelianizedDefect S F word r j) =
      (if i = j then (1 : ℤ) else 0) := by
  change Multiplicative.toAdd
    ((Abelianization.lift (nativeC60EBKernelCharacter S F word i))
      (Abelianization.of
        (nativeC60EBKernelGenerator S F word j r))) =
      (if i = j then (1 : ℤ) else 0)
  rw [Abelianization.lift_apply_of,
    nativeC60EBKernelCharacter_generator S F word r i j]
  split_ifs <;> rfl

/-- Universal additive extension of the genuine context-indexed
abelianized defects, before choosing their finite-support model. -/
def nativeC60EDFreeAbelianLift (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    FreeAbelianGroup ℕ →+
      Additive (Abelianization ((nativeC60DZImageToFull S F word).ker)) :=
  FreeAbelianGroup.lift (nativeC60EDAbelianizedDefect S F word r)

/-- The genuinely finitely supported integer-to-abelianization map.
The domain is the algebraic direct sum, not the full product ℤ^ℕ. -/
def nativeC60EDFiniteSupportEmbedding (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    (ℕ →₀ ℤ) →+
      Additive (Abelianization ((nativeC60DZImageToFull S F word).ker)) :=
  (nativeC60EDFreeAbelianLift S F word r).comp
    Finsupp.toFreeAbelianGroup

/-- On the universal free abelian presentation, every genuine
C60 charge equals the corresponding finite integer coefficient. -/
theorem nativeC60EDCoordinate_freeAbelian (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (i : ℕ) (v : FreeAbelianGroup ℕ) :
    nativeC60EDAbelianizedCoordinate S F word i
      (nativeC60EDFreeAbelianLift S F word r v) =
      FreeAbelianGroup.coeff i v := by
  have hhom :
      (nativeC60EDAbelianizedCoordinate S F word i).comp
        (nativeC60EDFreeAbelianLift S F word r) =
      FreeAbelianGroup.coeff i := by
    apply FreeAbelianGroup.lift_ext
    intro j
    rw [AddMonoidHom.comp_apply]
    change nativeC60EDAbelianizedCoordinate S F word i
      (nativeC60EDAbelianizedDefect S F word r j) =
      FreeAbelianGroup.coeff i (FreeAbelianGroup.of j)
    rw [nativeC60EDAbelianizedCoordinate_defect S F word r i j]
    rw [FreeAbelianGroup.coeff, AddMonoidHom.comp_apply,
      FreeAbelianGroup.toFinsupp_of]
    change (if i = j then (1 : ℤ) else 0) =
      (Finsupp.single j (1 : ℤ)) i
    by_cases h : i = j
    · subst j
      simp
    · have hji : j ≠ i := Ne.symm h
      simp [h, hji]
  exact DFunLike.congr_fun hhom v

/-- Exact recovery of every finite-support integer coefficient
from the fully Type-valued pentagon obstruction in the abelianization. -/
theorem nativeC60EDCoordinate_finiteSupport (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (v : ℕ →₀ ℤ) (i : ℕ) :
    nativeC60EDAbelianizedCoordinate S F word i
      (nativeC60EDFiniteSupportEmbedding S F word r v) = v i := by
  change nativeC60EDAbelianizedCoordinate S F word i
      (nativeC60EDFreeAbelianLift S F word r
        (Finsupp.toFreeAbelianGroup v)) = v i
  rw [nativeC60EDCoordinate_freeAbelian S F word r i]
  change (FreeAbelianGroup.toFinsupp (Finsupp.toFreeAbelianGroup v)) i = v i
  rw [FreeAbelianGroup.toFinsupp_toFreeAbelianGroup]

/-- The full product ℤ^ℕ is only an OBSERVATION receiver. This
homomorphism does NOT assert the obstruction subgroup surjects onto
that full infinite product. -/
def nativeC60EDAllCoordinates (word : List Bool) :
    Additive (Abelianization ((nativeC60DZImageToFull S F word).ker)) →+
      (ℕ → ℤ) where
  toFun x i := nativeC60EDAbelianizedCoordinate S F word i x
  map_zero' := by
    funext i
    exact map_zero (nativeC60EDAbelianizedCoordinate S F word i)
  map_add' x y := by
    funext i
    exact map_add (nativeC60EDAbelianizedCoordinate S F word i) x y

/-- The infinite product of characters recovers the embedded
FINITE-support coefficients pointwise; no image-completion is assumed. -/
theorem nativeC60EDAllCoordinates_finiteSupport (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (v : ℕ →₀ ℤ) :
    nativeC60EDAllCoordinates S F word
      (nativeC60EDFiniteSupportEmbedding S F word r v) =
        (fun i : ℕ => v i) := by
  funext i
  exact nativeC60EDCoordinate_finiteSupport S F word r v i

/-- MAIN ED RESULT: an actual countable free abelian direct sum
embeds in the ABELIANIZATION of the genuine noncommutative C60 AQ
quotient kernel. The left inverse is the family of EA integer
characters, which detects EVERY finite-support coordinate. -/
theorem nativeC60EDFiniteSupportEmbedding_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    Function.Injective (nativeC60EDFiniteSupportEmbedding S F word r) := by
  intro v w heq
  apply Finsupp.ext
  intro i
  have h := congrArg (nativeC60EDAbelianizedCoordinate S F word i) heq
  rw [nativeC60EDCoordinate_finiteSupport S F word r v i,
    nativeC60EDCoordinate_finiteSupport S F word r w i] at h
  exact h

/-- The equivalent universal FreeAbelianGroup formulation is also
injective. This is NOT a claim that the entire kernel is free. -/
theorem nativeC60EDFreeAbelianLift_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    Function.Injective (nativeC60EDFreeAbelianLift S F word r) := by
  intro v w heq
  apply (FreeAbelianGroup.equivFinsupp ℕ).injective
  apply Finsupp.ext
  intro i
  have h := congrArg (nativeC60EDAbelianizedCoordinate S F word i) heq
  rw [nativeC60EDCoordinate_freeAbelian S F word r i v,
    nativeC60EDCoordinate_freeAbelian S F word r i w] at h
  exact h

end CountableFreeAbelianContextObstructions

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

/-- The ACTUAL physical C60 AU 16D zigzag supplies the dependent
18D generator used to inject a countably generated free abelian
subgroup into the genuine AQ kernel abelianization. -/
theorem nativeK5EDPhysicalAQ_freeAbelianEmbedding_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    Function.Injective
      (nativeC60EDFiniteSupportEmbedding S F
        (nativeK5DOTreeWord tree)
        (nativeC60DYOriginalZigzagGen S F
          (nativeK5CEPhysicalAUGenerator W))) := by
  dsimp only
  exact nativeC60EDFiniteSupportEmbedding_injective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W))

end PhysicalC60AU

#print axioms nativeC60EDAbelianizedDefect
#print axioms nativeC60EDAbelianizedCoordinate
#print axioms nativeC60EDAbelianizedCoordinate_defect
#print axioms nativeC60EDFreeAbelianLift
#print axioms nativeC60EDFiniteSupportEmbedding
#print axioms nativeC60EDCoordinate_freeAbelian
#print axioms nativeC60EDCoordinate_finiteSupport
#print axioms nativeC60EDAllCoordinates
#print axioms nativeC60EDAllCoordinates_finiteSupport
#print axioms nativeC60EDFiniteSupportEmbedding_injective
#print axioms nativeC60EDFreeAbelianLift_injective
#print axioms nativeK5EDPhysicalAQ_freeAbelianEmbedding_injective

end
end Kuu.F112.Physical
