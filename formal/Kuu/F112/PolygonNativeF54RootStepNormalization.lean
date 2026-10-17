import Kuu.F112.PolygonNativeF54PackedRootNaturality

/-!
# F112-E7Q5-F4-J — one SAME-TYPE witness comparison suffices for all F55 descent

The independent F4-I proof now transports the true double Nat.cast
root F54 source as a proof-relevant Sigma intermediate packet, with
its original categorical Blocks and oriented F54 rotation witness.
That gives unconditional exact factorization of the mapped source
route for arbitrary six symbolic Nat depths.

The ONE remaining obstacle is no longer equality of a compound,
dependently indexed F54 route: it is equality of two ACTUAL
LocalRotation witnesses of the SAME genuine F45 source and target
type, after explicitly transporting the original root witness.

We package that single proof obligation as a structure (NOT a Lean
axiom or an asserted inhabitant). Given it, the complete original
F54 root strict naturality follows by ordinary equality rewriting
inside the verified Sigma packet. Existing F4-H then gives both
full F54 pentagon naturality equations, F4-B constructs the free F55
pentagon 3-cell and F4-F3 gives the faithful chosen quotient functor.

Historical KUOS/Gray source equivalence and F59/F68/F77 obstruction
transfer remain separate and unproved.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC uD vD
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

/-- THE precise remaining proof-relevant NORMALIZATION QUESTION.
The two terms have the very SAME dependent F45 input tree and F54
output tree, so the comparison is ordinary Eq rather than arbitrary
HEq or equality between numerical shadow images. -/
structure KuuNativeF54RootStepNormalization
    (F : A ⥤ C) (G : B ⥤ D) where
  step :
    ∀ (p : Polygon) {a b : A} {x y : B}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
      (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
      (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
      (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃),
      nativePackedRootMappedRotation F G t₁ t₂ t₃ =
        KuuNativeF45Tree.LocalRotation.assoc
          (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G)

/-- From SAME-TYPE witness normalization, prove actual original
F54 root strict naturality for ANY SIX symbolic Nat depth indices.
The only nontrivial middle expression is the already verified F4-I
type-packed route, not an ill-typed detached F45 Eq.rec rewrite. -/
def KuuNativeF54RootStepNormalization.toRootComparison
    (F : A ⥤ C) (G : B ⥤ D)
    (h : KuuNativeF54RootStepNormalization F G) :
    KuuNativeF54RootAssocComparison F G where
  root := fun p {_a _b} {_x _y}
    {_n₁ _n₂ _n₃ _m₁ _m₂ _m₃}
    {_p₀ _p₁ _p₂ _p₃} {_q₀ _q₁ _q₂ _q₃}
    t₁ t₂ t₃ => by
      rw [nativeGeneralRootAssoc_mapAxes_packed F G t₁ t₂ t₃]
      rw [h.step p t₁ t₂ t₃]
      rfl

/-- As a consequence, one matched local-rotation proof induces
BOTH globally indexed F54 3/2 pentagon boundary equations, without
introducing another independent assumption for either route. -/
def KuuNativeF54RootStepNormalization.toBoundary
    (F : A ⥤ C) (G : B ⥤ D)
    (h : KuuNativeF54RootStepNormalization F G) :
    KuuNativeF55PentagonBoundaryComparison F G :=
  (h.toRootComparison F G).toBoundary F G

/-- Therefore the actual Mathlib third-level functor on the
independent chosen full-shadow F55 quotient is obtained from the ONE
proof-relevant local normalized witness, not a Gray exchange axiom. -/
def nativeF55ThreeFunctorOfRootStepNormalization
    (F : A ⥤ C) (G : B ⥤ D)
    (h : KuuNativeF54RootStepNormalization F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    (KuuNativeF45Tree.DepthRotationRoute p first last) ⥤
      (KuuNativeF45Tree.DepthRotationRoute p
        (first.mapAxes F G) (last.mapAxes F G)) :=
  nativeF55ThreeFunctorOfRootAssoc F G (h.toRootComparison F G) first last

#print axioms KuuNativeF54RootStepNormalization
#print axioms KuuNativeF54RootStepNormalization.toRootComparison
#print axioms KuuNativeF54RootStepNormalization.toBoundary
#print axioms nativeF55ThreeFunctorOfRootStepNormalization
end
end Kuu.F112.Physical
