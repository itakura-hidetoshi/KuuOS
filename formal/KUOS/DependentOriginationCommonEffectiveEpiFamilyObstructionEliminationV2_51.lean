import Mathlib.CategoryTheory.EffectiveEpi.Basic
import KUOS.DependentOriginationSeparatingFamilyObstructionEliminationV2_50

namespace KUOS.DependentOriginationCommonEffectiveEpiFamilyObstructionEliminationV2_51

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42
open KUOS.DependentOriginationPointwise2CellRigidityObstructionEliminationV2_47

universe u v uH vH

/-!
# Common effective-epi-family obstruction elimination v2.51

v2.47 reduces the stored-triangle coherence problem to uniqueness of the
component morphisms

```text
F.obj Z ⟶ G.obj Z.
```

v2.49 supplies such uniqueness using one common source object together with an
epimorphism into every `F.obj Z`.  v2.50 supplies a different route using a
globally separating or coseparating object family.

The present file isolates a genuinely family-valued cancellation mechanism
provided directly by Mathlib's `EffectiveEpiFamily` API.

For fixed Cat 1-morphisms `F G : C ⟶ D`, choose one index type `ι` and one
family of probe objects

```text
Q : ι → D
```

that is shared by every component `Z : C`.  For each `Z`, suppose there is a
family

```text
e Z i : Q i ⟶ F.obj Z
```

which is an `EffectiveEpiFamily`.  If in addition every probe hom

```text
Q i ⟶ G.obj Z
```

is a subsingleton, then two maps `F.obj Z ⟶ G.obj Z` agree after
precomposition with every `e Z i`.  `EffectiveEpiFamily.hom_ext` therefore
forces the two maps themselves to agree.

Thus the exact route is

```text
shared effective-epi probe family
  -> pointwise component-hom uniqueness                (v2.47)
  -> exact Cat 2-cell hom uniqueness                    (v2.46)
  -> stored modification naturality
  -> weak universality + coherent route completeness
  -> no local v2.42 E/R obstruction.
```

The probe objects `Q i` are chosen once for the whole pair `F`, `G`; they may
not be chosen independently as `F.obj Z` for each component.  This prevents a
per-component identity-family repackaging of the desired conclusion.

This is an independent sufficient route.  `EffectiveEpiFamily` is stronger
than merely postulating an abstract jointly-epimorphic cancellation law, and a
singleton `EffectiveEpiFamily` corresponds to an effective epimorphism, not to
an arbitrary epimorphism.  Consequently no implication to or from the v2.49
ordinary-epi detector route or the v2.50 separating-family route is asserted.
No existence of such a common family, coherent universal data,
strictification, general higher-localization existence principle, or final
global dependent-origination theorem is proved here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A family of probe objects, common to all source components, which maps
effectively epimorphically onto every `F.obj Z` and has unique maps into every
corresponding `G.obj Z`. -/
def CatHom₂CommonEffectiveEpiFamily
    {C D : Cat.{vH, uH}} (F G : C ⟶ D) : Prop :=
  ∃ (ι : Type uH) (Q : ι → D)
      (e : ∀ Z : C, (i : ι) → Q i ⟶ F.obj Z),
    (∀ Z : C, EffectiveEpiFamily Q (e Z)) ∧
      ∀ (Z : C) (i : ι), Subsingleton (Q i ⟶ G.obj Z)

/-- A common effective-epimorphic probe family forces uniqueness of all
corresponding component morphisms. -/
theorem catHom₂PointwiseSubsingleton_of_commonEffectiveEpiFamily
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hFamily : CatHom₂CommonEffectiveEpiFamily F G) :
    CatHom₂PointwiseSubsingleton F G := by
  rcases hFamily with ⟨ι, Q, e, hEffective, hSub⟩
  intro Z
  letI : EffectiveEpiFamily Q (e Z) := hEffective Z
  constructor
  intro f g
  apply EffectiveEpiFamily.hom_ext Q (e Z) f g
  intro i
  exact (hSub Z i).elim _ _

/-- For every raw base arrow, the exact pair of Cat 1-morphisms occurring in
the v2.23 stored-triangle naturality square admits a common effective-epi
probe family. -/
def StoredV2_18NaturalityCommonEffectiveEpiFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    CatHom₂CommonEffectiveEpiFamily
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc ≫
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).app (.mk Y))
      (H.comparison.app (.mk X) ≫ R.map f.toLoc)

/-- Common effective-epi-family rigidity supplies the exact v2.47
component-hom subsingleton condition for a stored naturality square. -/
theorem storedV2_18NaturalityComponentHomSubsingleton_of_commonEffectiveEpiFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hFamily : StoredV2_18NaturalityCommonEffectiveEpiFamily
      (W := W) alpha) :
    StoredV2_18NaturalityComponentHomSubsingleton (W := W) alpha := by
  intro X Y f
  exact catHom₂PointwiseSubsingleton_of_commonEffectiveEpiFamily
    _ _ (hFamily f)

/-- Uniform common effective-epi-family rigidity for every v2.18 factor into
one coherent chosen carrier. -/
def HigherStoredV2_18NaturalityCommonEffectiveEpiFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalityCommonEffectiveEpiFamily (W := W) alpha

/-- Uniform common effective-epi-family rigidity implies the uniform v2.47
pointwise criterion. -/
theorem higherStoredV2_18NaturalityComponentHomSubsingleton_of_commonEffectiveEpiFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalityCommonEffectiveEpiFamily
      (W := W) U) :
    HigherStoredV2_18NaturalityComponentHomSubsingleton (W := W) U := by
  intro H alpha
  exact
    storedV2_18NaturalityComponentHomSubsingleton_of_commonEffectiveEpiFamily
      (W := W) alpha (hFamily H alpha)

/-- Coherent universal data plus uniform common effective-epi-family rigidity
give the v2.18 weak universal property on the same chosen carrier. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_commonEffectiveEpiFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalityCommonEffectiveEpiFamily
      (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R :=
  hasWeakHigherLocalizationUniversalProperty_of_pointwise2CellRigidity
    (W := W) U
      (higherStoredV2_18NaturalityComponentHomSubsingleton_of_commonEffectiveEpiFamily
        (W := W) U hFamily)

/-- The coherent Stage III route obstruction disappears under the same common
effective-epi-family condition. -/
theorem higherCoherentRouteCompleteness_of_commonEffectiveEpiFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalityCommonEffectiveEpiFamily
      (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  higherCoherentRouteCompleteness_of_pointwise2CellRigidity
    (W := W) U
      (higherStoredV2_18NaturalityComponentHomSubsingleton_of_commonEffectiveEpiFamily
        (W := W) U hFamily)

/-- Common effective-epi-family rigidity gives the aligned state in the v2.42
local classification. -/
theorem higherWeakCoherentAlignment_of_commonEffectiveEpiFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalityCommonEffectiveEpiFamily
      (W := W) U) :
    HigherWeakCoherentAlignment (W := W) U :=
  ⟨hasWeakHigherLocalizationUniversalProperty_of_commonEffectiveEpiFamily
      (W := W) U hFamily,
    higherCoherentRouteCompleteness_of_commonEffectiveEpiFamily
      (W := W) U hFamily⟩

/-- Exact local E/R obstruction elimination under a common effective-epi probe
family. -/
theorem no_twoAxisObstruction_of_commonEffectiveEpiFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalityCommonEffectiveEpiFamily
      (W := W) U) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  (higherWeakCoherentAlignment_iff_no_twoAxisObstruction
    (W := W) U).mp
      (higherWeakCoherentAlignment_of_commonEffectiveEpiFamily
        (W := W) U hFamily)

end KUOS.DependentOriginationCommonEffectiveEpiFamilyObstructionEliminationV2_51
