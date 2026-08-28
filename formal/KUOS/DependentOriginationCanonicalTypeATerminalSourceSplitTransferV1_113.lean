import KUOS.DependentOriginationCanonicalTypeAHigherLowerCylinderRetractObstructionV1_112

namespace KUOS.DependentOriginationCanonicalTypeATerminalSourceSplitTransferV1_113

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationCanonicalTypeATwoStaircaseRetractV1_110
open KUOS.DependentOriginationCanonicalTypeAHigherLowerCylinderRetractObstructionV1_112

universe u

noncomputable section

/-!
# Terminal source-split transfer for standard type-(A) horns v1.113

Version v1.112 proves that in every type-(A) simplex dimension at least three
there is no *full* scaled target retract through one lower canonical cylinder.
That obstruction is decisive for presentation-level arrow retracts, but it is
strictly stronger than what terminal horn filling requires.

For a terminal lifting problem one never has to map the intermediate target
back to the original simplex.  It is enough to have a commutative morphism of
arrows

```text
A --a--> C
|        |
j        k
v        v
B --s--> D
```

whose source component `a` is split by some `q : C -> A`.  If `k` has RLP
against the terminal map of `X`, then an extension of `q >> f : C -> X` along
`k`, restricted along `s`, extends any `f : A -> X` along `j`.

Thus only a *source split* is needed.  No target retraction `D -> B` occurs.
This is exactly the asymmetry needed after v1.112: higher type-(A) terminal
fibrancy can still be proved by a multi-cell prism source construction even
though a presentation-level one-cylinder retract is impossible.

The file packages this generic transfer, specializes it to the canonical
KuuOS generated left class, verifies that the already-completed degree-two
staircase retract supplies the source-split seed, and isolates the remaining
higher-dimensional geometry in one positive certificate.
-/

/-! ## Generic one-sided arrow data -/

/-- A morphism `j` is terminal-source-split through `k` when it maps
commutatively into `k` and the source component has a retraction.

There is deliberately no retraction on the target component. -/
structure TerminalSourceSplitTransferData
    {A B C D : ScaledSSet.{u}}
    (j : A ⟶ B)
    (k : C ⟶ D) where
  sourceInto : A ⟶ C
  targetInto : B ⟶ D
  square : sourceInto ≫ k = j ≫ targetInto
  sourceRetraction : C ⟶ A
  source_retract : sourceInto ≫ sourceRetraction = 𝟙 A

/-- Terminal RLP transfers across source-split arrow data.

This is weaker than the usual arrow-retract lemma: the target component need
not split because every bottom map in a terminal lifting square is unique. -/
theorem hasLiftingProperty_toPoint_of_terminalSourceSplit
    {A B C D X : ScaledSSet.{u}}
    {j : A ⟶ B}
    {k : C ⟶ D}
    (T : TerminalSourceSplitTransferData j k)
    (hk : HasLiftingProperty k (ScaledSSet.toPoint X)) :
    HasLiftingProperty j (ScaledSSet.toPoint X) := by
  rw [ScaledSSet.hasLiftingProperty_toPoint_iff] at hk ⊢
  intro f
  rcases hk (T.sourceRetraction ≫ f) with ⟨l, hl⟩
  refine ⟨T.targetInto ≫ l, ?_⟩
  calc
    j ≫ (T.targetInto ≫ l)
        = (j ≫ T.targetInto) ≫ l := by simp
    _ = (T.sourceInto ≫ k) ≫ l := by rw [← T.square]
    _ = T.sourceInto ≫ (k ≫ l) := by simp
    _ = T.sourceInto ≫ (T.sourceRetraction ≫ f) := by rw [hl]
    _ = (T.sourceInto ≫ T.sourceRetraction) ≫ f := by simp
    _ = (𝟙 A) ≫ f := by rw [T.source_retract]
    _ = f := by simp

/-! ## Membership-level source-split realization -/

/-- A morphism admits a terminal source-split realization through a morphism
belonging to `L`. -/
def HasTerminalSourceSplitThrough
    {A B : ScaledSSet.{u}}
    (j : A ⟶ B)
    (L : MorphismProperty (ScaledSSet.{u})) : Prop :=
  ∃ (C D : ScaledSSet.{u}) (k : C ⟶ D),
    L k ∧ Nonempty (TerminalSourceSplitTransferData j k)

/-- RLP against every map in `L` implies terminal RLP against every map which
is source-split through one member of `L`. -/
theorem hasLiftingProperty_toPoint_of_sourceSplitThrough
    {A B X : ScaledSSet.{u}}
    {j : A ⟶ B}
    {L : MorphismProperty (ScaledSSet.{u})}
    (hgeom : HasTerminalSourceSplitThrough j L)
    (hX : L.rlp (ScaledSSet.toPoint X)) :
    HasLiftingProperty j (ScaledSSet.toPoint X) := by
  rcases hgeom with ⟨C, D, k, hk, ⟨T⟩⟩
  exact hasLiftingProperty_toPoint_of_terminalSourceSplit T (hX k hk)

/-- Abbreviation for source-split realization through the canonical generated
left class. -/
def IsCanonicalTerminalSourceSplit
    {A B : ScaledSSet.{u}}
    (j : A ⟶ B) : Prop :=
  HasTerminalSourceSplitThrough j
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))

/-- A canonical-generated right terminal map therefore lifts against any
source-split canonical realization. -/
theorem canonicalGeneratedRight_hasLiftingProperty_toPoint_of_sourceSplit
    {A B X : ScaledSSet.{u}}
    {j : A ⟶ B}
    (hgeom : IsCanonicalTerminalSourceSplit j)
    (hX :
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})).rlp
        (ScaledSSet.toPoint X)) :
    HasLiftingProperty j (ScaledSSet.toPoint X) :=
  hasLiftingProperty_toPoint_of_sourceSplitThrough hgeom hX

/-! ## Standard type-(A) terminal source-split certificate -/

/-- Object-level standard type-(A) terminal RLP for a scaled simplicial set. -/
def HasStandardTypeATerminalRLP (X : ScaledSSet.{u}) : Prop :=
  ∀ g : StandardTypeAHornGeneratorIndex,
    HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom g)
      (ScaledSSet.toPoint X)

/-- The exact remaining geometry needed to transfer canonical attachment
fibrancy to all standard type-(A) terminal horn fillers.

Unlike the v1.79 presentation comparison, this asks only for source-split
realizations, not canonical left-class membership of the standard horn itself. -/
structure StandardTypeATerminalSourceSplitCanonicalCertificate : Prop where
  sourceSplit :
    ∀ g : StandardTypeAHornGeneratorIndex,
      IsCanonicalTerminalSourceSplit
        (standardTypeAScaledHornGeneratorHom g)

namespace StandardTypeATerminalSourceSplitCanonicalCertificate

/-- A source-split certificate transfers the complete canonical generated
terminal right class to standard type-(A) terminal RLP. -/
theorem canonicalGeneratedRight_hasStandardTypeATerminalRLP
    (K : StandardTypeATerminalSourceSplitCanonicalCertificate.{u})
    {X : ScaledSSet.{u}}
    (hX :
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})).rlp
        (ScaledSSet.toPoint X)) :
    HasStandardTypeATerminalRLP X := by
  intro g
  exact
    canonicalGeneratedRight_hasLiftingProperty_toPoint_of_sourceSplit
      (K.sourceSplit g) hX

/-- The same result from the literal canonical attachment-fibrancy predicate,
using equality of generator RLP and generated RLP. -/
theorem attachmentFibrant_hasStandardTypeATerminalRLP
    (K : StandardTypeATerminalSourceSplitCanonicalCertificate.{u})
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X) :
    HasStandardTypeATerminalRLP X := by
  apply K.canonicalGeneratedRight_hasStandardTypeATerminalRLP
  rw [canonicalGeneratedScaledAnodyne_rlp]
  exact hX

/-- Extension form: every scaled standard type-(A) horn map extends to the
scaled simplex under attachment fibrancy and the source-split geometry. -/
theorem attachmentFibrant_standardTypeAHornExtension
    (K : StandardTypeATerminalSourceSplitCanonicalCertificate.{u})
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X)
    (g : StandardTypeAHornGeneratorIndex)
    (f : standardTypeAScaledHorn g ⟶ X) :
    ∃ l : standardTypeAScaledSimplex g ⟶ X,
      standardTypeAScaledHornGeneratorHom g ≫ l = f := by
  apply
    (ScaledSSet.hasLiftingProperty_toPoint_iff
      (standardTypeAScaledHornGeneratorHom g)).1
  exact K.attachmentFibrant_hasStandardTypeATerminalRLP hX g

end StandardTypeATerminalSourceSplitCanonicalCertificate

/-! ## Degree-two seed from the existing full staircase retract -/

/-- Forget the unnecessary target retraction from the v1.110 degree-two arrow
retract.  The remaining source split is exactly the data needed for terminal
lifting transfer. -/
def standardTypeATwoTerminalSourceSplit :
    TerminalSourceSplitTransferData
      (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex)
      (scaledHornAttachmentGeneratorHom typeATwoStaircaseCanonicalIndex) where
  sourceInto := typeATwoSourceToCanonicalSource
  targetInto := typeATwoTargetToCanonicalTarget
  square := by
    apply ScaledSSet.ScaledMap.ext
    change
      (Λ[2, (1 : Fin 3)].ι :
          (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) ≫
        typeATwoLowerRightStaircaseSection =
      typeATwoHornIntoCanonicalAttachmentMap ≫
        (hornCylinderAttachment 1 (1 : Fin 2) 0).ι
    exact typeATwoHornIntoCanonicalAttachmentMap_ι.symm
  sourceRetraction := typeATwoCanonicalSourceToSource
  source_retract := typeATwoSource_retract

/-- Hence the unique degree-two type-(A) horn has a terminal source-split
realization through a literal canonical attachment. -/
theorem standardTypeATwo_isCanonicalTerminalSourceSplit :
    IsCanonicalTerminalSourceSplit
      (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex) := by
  refine ⟨
    minimallyScaledHornCylinderAttachment 1 (1 : Fin 2) 0,
    scaledSimplexCylinder (minimalScaling (Δ[1] : SSet.{u})),
    scaledHornAttachmentGeneratorHom typeATwoStaircaseCanonicalIndex,
    ?_, ⟨standardTypeATwoTerminalSourceSplit⟩⟩
  exact scaledHornAttachmentGenerators_le_generated _
    (scaledHornAttachmentGenerator_mem typeATwoStaircaseCanonicalIndex)

/-- Every literal degree-two type-(A) generator has the preceding source-split
realization. -/
theorem standardTypeA_dim_two_isCanonicalTerminalSourceSplit
    (g : StandardTypeAHornGeneratorIndex)
    (hn : g.n = 2) :
    IsCanonicalTerminalSourceSplit
      (standardTypeAScaledHornGeneratorHom g) := by
  rw [standardTypeAHornGeneratorIndex_eq_two g hn]
  exact standardTypeATwo_isCanonicalTerminalSourceSplit

/-! ## Post-two terminal source-split frontier -/

/-- After the degree-two seed, only source-split realizations for dimensions
at least three remain in the object-level type-(A) terminal problem. -/
structure StandardTypeAPostTwoTerminalSourceSplitCore : Prop where
  higher :
    ∀ g : StandardTypeAHornGeneratorIndex,
      3 ≤ g.n →
        IsCanonicalTerminalSourceSplit
          (standardTypeAScaledHornGeneratorHom g)

namespace StandardTypeAPostTwoTerminalSourceSplitCore

/-- The post-two higher source-split core supplies the source-split geometry in
all type-(A) dimensions. -/
theorem all
    (K : StandardTypeAPostTwoTerminalSourceSplitCore.{u})
    (g : StandardTypeAHornGeneratorIndex) :
    IsCanonicalTerminalSourceSplit
      (standardTypeAScaledHornGeneratorHom g) := by
  have hge2 : 2 ≤ g.n := by
    have hleft := g.inner_left
    have hright := g.inner_right
    change 0 < g.i.val at hleft
    change g.i.val < g.n at hright
    omega
  by_cases htwo : g.n = 2
  · exact standardTypeA_dim_two_isCanonicalTerminalSourceSplit g htwo
  · exact K.higher g (by omega)

/-- Package the post-two core as the complete terminal source-split
certificate. -/
def toCertificate
    (K : StandardTypeAPostTwoTerminalSourceSplitCore.{u}) :
    StandardTypeATerminalSourceSplitCanonicalCertificate.{u} where
  sourceSplit := K.all

/-- Therefore the remaining higher source-side prism geometry alone is enough
to make every canonical attachment-fibrant object standard type-(A)
terminal-fibrant. -/
theorem attachmentFibrant_hasStandardTypeATerminalRLP
    (K : StandardTypeAPostTwoTerminalSourceSplitCore.{u})
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X) :
    HasStandardTypeATerminalRLP X :=
  K.toCertificate.attachmentFibrant_hasStandardTypeATerminalRLP hX

end StandardTypeAPostTwoTerminalSourceSplitCore

/-!
The PlanOS frontier after v1.113 is intentionally asymmetric:

```text
presentation-level reverse comparison:
  standard type-A horn ∈ canonicalGenerated
  requires a full left-class argument and remains blocked by v1.112
  for any one-lower-cylinder target retract in dimensions >= 3.

object-level terminal type-A fibrancy:
  only source-split transfer is required;
  no cylinder -> simplex target retraction is needed.
```

The exact positive higher-dimensional target is therefore now

```text
for every type-A g with g.n >= 3,
construct a canonical-generated map k and
TerminalSourceSplitTransferData (standardTypeAScaledHornGeneratorHom g) k.
```

A multi-cell prism construction may satisfy this even though no single lower
cylinder can be a full arrow retract.  This is the source-side geometry to be
built next; no higher type-A canonical membership is assumed in the interface.
-/

end KUOS.DependentOriginationCanonicalTypeATerminalSourceSplitTransferV1_113
