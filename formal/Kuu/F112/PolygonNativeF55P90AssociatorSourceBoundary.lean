import Kuu.F112.PolygonNativeF55P89StrictHorizontalCategory
import Mathlib.Tactic

/-!
# F112-P90A — genuine F54 reassociation is not literal F45 tree equality

P89 proves a true same-presentation P89×P89→P89 horizontal operation
and strict horizontal-vertical interchange, but the former output
is indexed by the ORIGINAL F54 tree binary bracketing.

Before asserting a horizontal associativity equation across THREE
factors, we must distinguish:
  (1) the source tree ((a·b)·c);
  (2) the source tree (a·(b·c));
  (3) the authentic F54 Type-valued associator ROUTE between them;
  (4) an equality of raw source trees (which is FALSE after the two
      independent Nat.add_assoc casts are made explicit).

We prove a NEW independent left-root-node invariant for every native
F45 tree and show a uniform non-equality of the two typed bracketings
at arbitrary six Nat depths and arbitrary F19/F28 Blocks histories.
Meanwhile the genuine native F54 associator has one real rotation and
preserves full ordered physical sectors.

This is a typed obstruction to treating P89's horizontal operation
as trivially strictly associative across F54 bracketing. It is NOT
a no-go for a separate comparison presentation or a proof of all
local strict 3-category axioms. The original route and odd C60 phase
remain intact. No Gray, sorry/admit, new axioms or root removal.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Actual number of internal F45 tree nodes, independent of
raw F54 route count and independent of any numerical F55 shadow. -/
def KuuNativeF45Tree.p90InternalNodes
    {p : Polygon} {a b : D} {x y : E}
    {n m : Nat} {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y} :
    KuuNativeF45Tree p n m ma pa mb pb → Nat
  | .refl _ _ _ => 0
  | .leaf _ _ _ _ => 0
  | .node first second =>
      first.p90InternalNodes + second.p90InternalNodes + 1

/-- Internal node count on the LEFT immediate subtree of the root.
The two 3-factor bracketings have different values for all typed
input trees, even when their ordered physical sectors coincide. -/
def KuuNativeF45Tree.p90LeftRootNodes
    {p : Polygon} {a b : D} {x y : E}
    {n m : Nat} {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y} :
    KuuNativeF45Tree p n m ma pa mb pb → Nat
  | .refl _ _ _ => 0
  | .leaf _ _ _ _ => 0
  | .node first _ => first.p90InternalNodes

/-- Both explicit original-F19/F28 Nat-index casts preserve the
left-root constructor shape and its independent subtree invariant. -/
theorem KuuNativeF45Tree.p90LeftRootNodes_castDepths
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (hn : n = n') (hm : m = m')
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (KuuNativeF45Tree.castDepths hn hm tree).p90LeftRootNodes =
      tree.p90LeftRootNodes := by
  cases hn
  cases hm
  rfl

/-- Genuine typed ORIGINAL F54 associativity has unequal source
TREES: a selected source-level invariant sees the difference even
after the two Nat.add_assoc dependent casts, at arbitrary depths.
A transported associator ROUTE is not literal tree equality. -/
theorem nativeF54P90_assoc_cast_source_ne
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (second : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (third : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    KuuNativeF45Tree.castDepths
      (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node first second) third) ≠
      KuuNativeF45Tree.node first
        (KuuNativeF45Tree.node second third) := by
  intro heq
  have h := congrArg KuuNativeF45Tree.p90LeftRootNodes heq
  simp only [KuuNativeF45Tree.p90LeftRootNodes_castDepths,
    KuuNativeF45Tree.p90LeftRootNodes,
    KuuNativeF45Tree.p90InternalNodes] at h
  omega

/-- Full original ordered physical sector projection identifies
the two bracketed presentations, although the actual source trees
cannot be equal. This is a concrete nonfaithful source readout. -/
theorem nativeF54P90_assoc_sectors_eq_and_source_ne
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (second : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (third : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.castDepths
      (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node first second) third)).sectors =
      (KuuNativeF45Tree.node first
        (KuuNativeF45Tree.node second third)).sectors ∧
    KuuNativeF45Tree.castDepths
      (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node first second) third) ≠
      KuuNativeF45Tree.node first
        (KuuNativeF45Tree.node second third) := by
  constructor
  · rw [KuuNativeF45Tree.sectors_castDepths]
    change (first.sectors ++ second.sectors) ++ third.sectors =
      first.sectors ++ (second.sectors ++ third.sectors)
    exact List.append_assoc _ _ _
  · exact nativeF54P90_assoc_cast_source_ne first second third

/-- The F54 associator between the original bracketings is an
ACTUAL Type-valued route with precisely one genuine primitive
rotation. The sector coincidence is not used to fabricate it. -/
theorem nativeF54P90_assoc_actual_route_and_count
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (second : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (third : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    ∃ route : KuuNativeF45Tree.DepthRotationRoute p
        (KuuNativeF45Tree.node
          (KuuNativeF45Tree.node first second) third)
        (KuuNativeF45Tree.node first
          (KuuNativeF45Tree.node second third)),
      route.rotationCount = 1 ∧
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node first second) third).sectors =
        (KuuNativeF45Tree.node first
          (KuuNativeF45Tree.node second third)).sectors := by
  refine ⟨KuuNativeF45Tree.DepthRotationRoute.assoc first second third, ?_, ?_⟩
  · exact KuuNativeF45Tree.DepthRotationRoute.assoc_rotationCount first second third
  · exact (KuuNativeF45Tree.DepthRotationRoute.assoc first second third).sectors_eq

/-- Physical north C60 pentagon: all THREE nontrivial F45 sectors
are present with their independently typed F19 and F28 histories.
The two parenthesized tree presentations really differ. -/
theorem northNativeF54P90_assoc_cast_source_ne :
    KuuNativeF45Tree.castDepths
      (Nat.add_assoc 1 1 1) (Nat.add_assoc 1 1 1)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node
          northNativeF45FirstStage northNativeF45SecondStage)
        northNativeF45ThirdStage) ≠
    KuuNativeF45Tree.node northNativeF45FirstStage
      (KuuNativeF45Tree.node
        northNativeF45SecondStage northNativeF45ThirdStage) := by
  exact nativeF54P90_assoc_cast_source_ne
    northNativeF45FirstStage northNativeF45SecondStage northNativeF45ThirdStage

#print axioms KuuNativeF45Tree.p90InternalNodes
#print axioms KuuNativeF45Tree.p90LeftRootNodes
#print axioms KuuNativeF45Tree.p90LeftRootNodes_castDepths
#print axioms nativeF54P90_assoc_cast_source_ne
#print axioms nativeF54P90_assoc_sectors_eq_and_source_ne
#print axioms nativeF54P90_assoc_actual_route_and_count
#print axioms northNativeF54P90_assoc_cast_source_ne

end
end Kuu.F112.Physical
