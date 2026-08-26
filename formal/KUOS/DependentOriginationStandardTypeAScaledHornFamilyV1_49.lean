import KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48

namespace KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open Opposite
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48

universe u

/-!
# Standard type-(A) scaled horn specialization v1.49

The canonical KuuOS horn machinery is deliberately stronger than a fixed
standard scaled-anodyne presentation: its generator index allows an arbitrary
scaling on every simplex.  This file does not weaken that carrier.  Instead it
cuts out the standard type-(A) inner-horn specialization as a theorem-level
subfamily.

For an inner index `0 < i < n`, the type-(A) scaling on `Δ[n]` consists of
all degenerate 2-simplices together with the distinguished consecutive
triangle

`{i-1, i, i+1}`.

Rather than choosing a separate presentation of the horn scaling, we pull this
simplex scaling back along the horn inclusion.  Hence preservation of thin
2-simplices by the horn inclusion is true by construction.  The existing
`ScaledHornExtensionProblem` and `HasScaledHornFillers` interfaces remain
unchanged.

Finally, the v1.48 induced attachment generators are restricted to exactly
these type-(A) simplex scalings.  This is the carrier needed for the next
pushout-product comparison step; no claim about type-(B), type-(C), or the full
standard scaled-anodyne family is made here.
-/

/-! ## The distinguished consecutive triangle -/

/-- A 2-simplex of `Δ[n]` is the distinguished type-(A) triangle at `i`
when its three ordered vertices are exactly consecutive around `i`. -/
def IsStandardTypeADistinguishedTriangle
    {n : Nat}
    (i : Fin (n + 1))
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌)) : Prop :=
  t 1 = i ∧
    (t 0).val + 1 = i.val ∧
    i.val + 1 = (t 2).val

/-- The standard type-(A) simplex scaling: minimal scaling plus the one
consecutive triangle centered at `i`. -/
def standardTypeASimplexScaling
    {n : Nat}
    (i : Fin (n + 1)) :
    ScaledSimplicialSet (Δ[n] : SSet.{u}) where
  thin := fun t =>
    (minimalScaling (Δ[n] : SSet.{u})).thin t ∨
      IsStandardTypeADistinguishedTriangle i t
  thin_sigma_zero := by
    intro x
    exact Or.inl ((minimalScaling (Δ[n] : SSet.{u})).thin_sigma_zero x)
  thin_sigma_one := by
    intro x
    exact Or.inl ((minimalScaling (Δ[n] : SSet.{u})).thin_sigma_one x)

/-- Every minimally thin 2-simplex is thin for the type-(A) scaling. -/
theorem minimalScaling_le_standardTypeASimplexScaling
    {n : Nat}
    (i : Fin (n + 1))
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    (ht : (minimalScaling (Δ[n] : SSet.{u})).thin t) :
    (standardTypeASimplexScaling i).thin t := by
  exact Or.inl ht

/-- The distinguished consecutive triangle is thin by definition. -/
theorem standardTypeADistinguishedTriangle_thin
    {n : Nat}
    (i : Fin (n + 1))
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    (ht : IsStandardTypeADistinguishedTriangle i t) :
    (standardTypeASimplexScaling i).thin t := by
  exact Or.inr ht

/-! ## Pull the type-(A) scaling back to the horn -/

/-- The standard type-(A) horn scaling is exactly the pullback of the simplex
scaling along the ordinary horn inclusion. -/
def standardTypeAHornScaling
    {n : Nat}
    (i : Fin (n + 1)) :
    ScaledSimplicialSet (Λ[n, i] : SSet.{u}) :=
  pullbackScaling (standardTypeASimplexScaling i) Λ[n, i].ι

/-- The horn inclusion preserves the type-(A) scalings by construction. -/
theorem standardTypeAHornInclusion_scaled
    {n : Nat}
    (i : Fin (n + 1)) :
    IsScaledMap
      (standardTypeAHornScaling i)
      (standardTypeASimplexScaling i)
      (Λ[n, i].ι : (Λ[n, i] : SSet.{u}) ⟶ (Δ[n] : SSet.{u})) := by
  exact pullbackScaling_map _ _

/-! ## Type-(A) problems as an admissible specialization -/

/-- Build an ordinary `ScaledHornExtensionProblem` using the canonical type-(A)
scalings.  The generic problem structure is not changed. -/
def standardTypeAScaledHornProblem
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat}
    (i : Fin (n + 1))
    (hornMap : (Λ[n, i] : SSet.{u}) ⟶ X)
    (hornMap_scaled :
      IsScaledMap (standardTypeAHornScaling i) sX hornMap) :
    ScaledHornExtensionProblem X sX n i where
  hornScaling := standardTypeAHornScaling i
  simplexScaling := standardTypeASimplexScaling i
  inclusion_scaled := standardTypeAHornInclusion_scaled i
  hornMap := hornMap
  hornMap_scaled := hornMap_scaled

/-- The standard type-(A) family selects precisely inner horn problems whose
explicit simplex and horn scalings are the canonical type-(A) scaling and its
pullback. -/
def standardTypeAScaledHornFamily
    (X : SSet.{u})
    (sX : ScaledSimplicialSet X) :
    ScaledHornFamily X sX where
  admissible := fun {n} {i} P =>
    0 < i ∧
      i < Fin.last n ∧
      P.simplexScaling = standardTypeASimplexScaling i ∧
      P.hornScaling = standardTypeAHornScaling i

/-- A canonically constructed type-(A) horn problem is admissible whenever its
distinguished index is inner. -/
theorem standardTypeAScaledHornProblem_admissible
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat}
    (i : Fin (n + 1))
    (h0 : 0 < i)
    (hn : i < Fin.last n)
    (hornMap : (Λ[n, i] : SSet.{u}) ⟶ X)
    (hornMap_scaled :
      IsScaledMap (standardTypeAHornScaling i) sX hornMap) :
    (standardTypeAScaledHornFamily X sX).admissible
      (standardTypeAScaledHornProblem i hornMap hornMap_scaled) := by
  exact ⟨h0, hn, rfl, rfl⟩

/-- The generic `HasScaledHornFillers` spine can be reused without alteration
for every standard type-(A) problem. -/
theorem standardTypeAHornFiller_of_family
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat}
    (i : Fin (n + 1))
    (h0 : 0 < i)
    (hn : i < Fin.last n)
    (hornMap : (Λ[n, i] : SSet.{u}) ⟶ X)
    (hornMap_scaled :
      IsScaledMap (standardTypeAHornScaling i) sX hornMap)
    [H : HasScaledHornFillers X sX (standardTypeAScaledHornFamily X sX)] :
    Nonempty
      (ScaledHornFiller
        (standardTypeAScaledHornProblem i hornMap hornMap_scaled)) := by
  exact H.fill
    (standardTypeAScaledHornProblem i hornMap hornMap_scaled)
    (standardTypeAScaledHornProblem_admissible
      i h0 hn hornMap hornMap_scaled)
    h0 hn

/-! ## Restrict the v1.48 induced attachment generators to type-(A) -/

/-- Index data for the type-(A) part of the induced horn-cylinder attachment
family.  The innerness proofs are part of the index, so no outer horn enters
this restricted generator property. -/
structure StandardTypeAHornAttachmentGeneratorIndex where
  n : Nat
  i : Fin (n + 1)
  inner_left : 0 < i
  inner_right : i < Fin.last n
  endpoint : Fin 2

/-- Forget the type-(A) restriction into the arbitrary-scaling canonical
attachment index by installing the standard type-(A) simplex scaling. -/
def StandardTypeAHornAttachmentGeneratorIndex.toCanonical
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScaledHornAttachmentGeneratorIndex.{u} where
  n := g.n
  i := g.i
  endpoint := g.endpoint
  simplexScaling := standardTypeASimplexScaling g.i

/-- The type-(A) induced-scaled attachment inclusion associated to one
restricted index. -/
def standardTypeAInducedScaledHornAttachmentGeneratorHom
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    inducedScaledHornCylinderAttachment
        g.i g.endpoint (standardTypeASimplexScaling g.i) ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) :=
  inducedScaledHornAttachmentGeneratorHom g.toCanonical

/-- The induced attachment generator property restricted to standard type-(A)
inner horns. -/
def standardTypeAInducedScaledHornAttachmentGenerators :
    MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.ofHoms
    (fun g : StandardTypeAHornAttachmentGeneratorIndex =>
      standardTypeAInducedScaledHornAttachmentGeneratorHom g)

/-- Every restricted type-(A) induced attachment belongs to its generator
property. -/
theorem standardTypeAInducedScaledHornAttachmentGenerator_mem
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeAInducedScaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u}))
      (standardTypeAInducedScaledHornAttachmentGeneratorHom g) :=
  MorphismProperty.ofHoms.mk g

/-- The type-(A) induced generator property is literally a specialization of
the arbitrary-scaling induced generator property from v1.48. -/
theorem standardTypeAInducedScaledHornAttachmentGenerators_le_induced :
    (standardTypeAInducedScaledHornAttachmentGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
    (inducedScaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) := by
  intro A B f hf
  dsimp [standardTypeAInducedScaledHornAttachmentGenerators] at hf
  cases hf with
  | mk g =>
      exact inducedScaledHornAttachmentGenerator_mem g.toCanonical

/-- The original canonical attachment at a type-(A) index still factors through
its type-(A) induced-scaled attachment exactly as in v1.48. -/
theorem standardTypeAScaledHornAttachmentGenerator_factorization
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    scaledHornAttachmentScalingEnrichment g.toCanonical ≫
        standardTypeAInducedScaledHornAttachmentGeneratorHom g =
      scaledHornAttachmentGeneratorHom g.toCanonical := by
  exact scaledHornAttachmentGeneratorHom_factorization g.toCanonical

/-!
The first standard specialization is therefore theorem-level and additive:

```text
arbitrary scaled horn carrier
  ⊇ standard type-(A) inner horn family

minimal scaling + {i-1,i,i+1}
  -> pullback horn scaling
  -> admissible ScaledHornFamily specialization
  -> generic HasScaledHornFillers reuse
  -> type-(A) restricted induced horn-cylinder generators
  ≤ full induced horn-cylinder generators of v1.48.
```

The next comparison can now be stated only on
`standardTypeAInducedScaledHornAttachmentGenerators`, where the ordinary
underlying geometry is the type-(A) horn/cylinder pushout-product geometry.
The separate minimal-to-induced scaling enrichment remains outside that
argument, exactly as required by v1.48.
-/

end KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
