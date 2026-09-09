import KUOS.DependentOriginationComparisonAutomorphismSectionsV2_28

namespace KUOS.DependentOriginationPointwiseExtensionObstructionV2_29

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStoredTriangleCorrectionTorsorV2_27
open KUOS.DependentOriginationComparisonAutomorphismSectionsV2_28

universe u v uH vH

/-!
# Pointwise extension obstruction v2.29

The v2.28 layer proved that pointwise automorphism rigidity implies target
modification rigidity, while deliberately not claiming the converse.  The
reason is now isolated exactly.

A nontrivial automorphism of one objectwise comparison functor is only local
data.  To produce a nontrivial modification it must extend to a coherent
section satisfying the StrongTrans modification naturality equation.  This
file packages that extension problem without adding any existence axiom.

The exact local picture is:

```text
nontrivial coherent section
  <->
nontrivial pointwise automorphism witness admitting a coherent extension.
```

Therefore:

```text
pointwise non-rigidity + target rigidity
  <->
there exists pointwise nontriviality, but every such witness is blocked
from extending coherently.
```

An explicit extension property closes the one-way implication from v2.28 and
gives equivalence between pointwise rigidity and target modification rigidity.
The extension property itself remains an explicit proposition, not an axiom or
an unconditional theorem.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A concrete nonidentity self-isomorphism of one objectwise comparison
functor.  It is local data only; no coherence is included. -/
structure FactorComparisonPointwiseAutomorphismWitness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) where
  object : Context
  automorphism :
    H.comparison.app (.mk object) ≅ H.comparison.app (.mk object)
  nontrivial : automorphism ≠ Iso.refl _

/-- A chosen pointwise witness admits a coherent extension when it occurs as
one component of a v2.28 coherent automorphism section. -/
def FactorComparisonPointwiseAutomorphismWitness.HasCoherentExtension
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H) : Prop :=
  ∃ P : FactorComparisonAutomorphismSection (W := W) H,
    P.component q.object = q.automorphism

/-- If a nontrivial pointwise witness is realized by a coherent section, that
section cannot be the identity section. -/
theorem section_ne_identity_of_pointwiseWitness_extension
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H)
    (P : FactorComparisonAutomorphismSection (W := W) H)
    (hComponent : P.component q.object = q.automorphism) :
    P ≠ identityFactorComparisonAutomorphismSection (W := W) H := by
  intro hEq
  have hAt := congrArg
    (fun Q : FactorComparisonAutomorphismSection (W := W) H =>
      Q.component q.object) hEq
  apply q.nontrivial
  calc
    q.automorphism = P.component q.object := hComponent.symm
    _ = (identityFactorComparisonAutomorphismSection (W := W) H).component q.object := hAt
    _ = Iso.refl _ :=
      identityFactorComparisonAutomorphismSection_component
        (W := W) H q.object

/-- Any coherent extension of a nontrivial pointwise witness gives a nontrivial
coherent section. -/
theorem hasNontrivialSection_of_pointwiseWitness_extension
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H)
    (hExtension : q.HasCoherentExtension (W := W)) :
    HasNontrivialFactorComparisonAutomorphismSection (W := W) H := by
  rcases hExtension with ⟨P, hComponent⟩
  exact ⟨P,
    section_ne_identity_of_pointwiseWitness_extension
      (W := W) q P hComponent⟩

/-- Exact bridge: a nonidentity coherent section exists exactly when some
nontrivial pointwise witness extends coherently. -/
theorem hasNontrivialSection_iff_exists_extendablePointwiseWitness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    HasNontrivialFactorComparisonAutomorphismSection (W := W) H ↔
      ∃ q : FactorComparisonPointwiseAutomorphismWitness (W := W) H,
        q.HasCoherentExtension (W := W) := by
  classical
  constructor
  · rintro ⟨P, hP⟩
    have hObject : ∃ X : Context, P.component X ≠ Iso.refl _ := by
      by_contra hNoObject
      apply hP
      ext X
      have hX : P.component X = Iso.refl _ := by
        by_contra hXne
        exact hNoObject ⟨X, hXne⟩
      calc
        P.component X = Iso.refl _ := hX
        _ = (identityFactorComparisonAutomorphismSection (W := W) H).component X :=
          (identityFactorComparisonAutomorphismSection_component
            (W := W) H X).symm
    rcases hObject with ⟨X, hX⟩
    let q : FactorComparisonPointwiseAutomorphismWitness (W := W) H := {
      object := X
      automorphism := P.component X
      nontrivial := hX
    }
    refine ⟨q, ?_⟩
    exact ⟨P, rfl⟩
  · rintro ⟨q, hExtension⟩
    exact hasNontrivialSection_of_pointwiseWitness_extension
      (W := W) q hExtension

/-- Positive pointwise non-rigidity: there exists some nontrivial local
self-isomorphism, without assuming it extends coherently. -/
def HasNontrivialFactorComparisonPointwiseAutomorphism
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) : Prop :=
  Nonempty (FactorComparisonPointwiseAutomorphismWitness (W := W) H)

/-- Since identity exists objectwise, failure of v2.28 pointwise rigidity is
exactly existence of a nontrivial pointwise automorphism witness. -/
theorem not_pointwiseAutomorphismRigidity_iff_hasNontrivialPointwiseAutomorphism
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    (¬ FactorComparisonPointwiseAutomorphismRigidity (W := W) H) ↔
      HasNontrivialFactorComparisonPointwiseAutomorphism (W := W) H := by
  classical
  constructor
  · intro hNotRigid
    by_contra hNoWitness
    apply hNotRigid
    intro X
    constructor
    intro g h
    have hg : g = Iso.refl _ := by
      by_contra hgNe
      exact hNoWitness ⟨{
        object := X
        automorphism := g
        nontrivial := hgNe
      }⟩
    have hh : h = Iso.refl _ := by
      by_contra hhNe
      exact hNoWitness ⟨{
        object := X
        automorphism := h
        nontrivial := hhNe
      }⟩
    exact hg.trans hh.symm
  · rintro ⟨q⟩ hRigid
    exact q.nontrivial
      (@Subsingleton.elim _ (hRigid q.object)
        q.automorphism (Iso.refl _))

/-- Exact target non-rigidity normal form in terms of extendable pointwise
witnesses. -/
theorem not_targetAutomorphismRigidity_iff_exists_extendablePointwiseWitness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    (¬ Subsingleton (H.comparison ≅ H.comparison)) ↔
      ∃ q : FactorComparisonPointwiseAutomorphismWitness (W := W) H,
        q.HasCoherentExtension (W := W) := by
  calc
    (¬ Subsingleton (H.comparison ≅ H.comparison)) ↔
        HasNontrivialFactorComparisonAutomorphismSection (W := W) H :=
      not_subsingleton_factorComparisonAutomorphismIso_iff_nontrivialSection
        (W := W) H
    _ ↔ ∃ q : FactorComparisonPointwiseAutomorphismWitness (W := W) H,
          q.HasCoherentExtension (W := W) :=
      hasNontrivialSection_iff_exists_extendablePointwiseWitness
        (W := W) H

/-- The precise residual gap left by v2.28: local nontrivial automorphisms exist,
but no nontrivial pointwise witness extends to a coherent section. -/
def FactorComparisonCoherenceExtensionObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) : Prop :=
  HasNontrivialFactorComparisonPointwiseAutomorphism (W := W) H ∧
    ∀ q : FactorComparisonPointwiseAutomorphismWitness (W := W) H,
      ¬ q.HasCoherentExtension (W := W)

/-- Exact characterization of the v2.28 one-way gap: pointwise non-rigidity can
coexist with target rigidity precisely when coherence blocks every nontrivial
pointwise witness from extending. -/
theorem coherenceExtensionObstruction_iff_pointwiseNonrigid_and_targetRigid
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    FactorComparisonCoherenceExtensionObstruction (W := W) H ↔
      (¬ FactorComparisonPointwiseAutomorphismRigidity (W := W) H) ∧
        Subsingleton (H.comparison ≅ H.comparison) := by
  classical
  constructor
  · rintro ⟨hPointwise, hNoExtension⟩
    refine ⟨
      (not_pointwiseAutomorphismRigidity_iff_hasNontrivialPointwiseAutomorphism
        (W := W) H).mpr hPointwise,
      ?_⟩
    by_contra hTargetNotRigid
    rcases
      (not_targetAutomorphismRigidity_iff_exists_extendablePointwiseWitness
        (W := W) H).mp hTargetNotRigid with ⟨q, hExtension⟩
    exact hNoExtension q hExtension
  · rintro ⟨hPointwiseNotRigid, hTargetRigid⟩
    refine ⟨
      (not_pointwiseAutomorphismRigidity_iff_hasNontrivialPointwiseAutomorphism
        (W := W) H).mp hPointwiseNotRigid,
      ?_⟩
    intro q hExtension
    have hTargetNotRigid : ¬ Subsingleton (H.comparison ≅ H.comparison) :=
      (not_targetAutomorphismRigidity_iff_exists_extendablePointwiseWitness
        (W := W) H).mpr ⟨q, hExtension⟩
    exact hTargetNotRigid hTargetRigid

/-- A strong extension property: every nontrivial pointwise automorphism witness
extends to a coherent section.  This is an explicit proposition and is not
asserted unconditionally. -/
def FactorComparisonPointwiseAutomorphismExtensionProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) : Prop :=
  ∀ q : FactorComparisonPointwiseAutomorphismWitness (W := W) H,
    q.HasCoherentExtension (W := W)

/-- Under the explicit extension property, pointwise non-rigidity forces target
modification non-rigidity. -/
theorem not_targetRigidity_of_not_pointwiseRigidity_and_extensionProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R)
    (hPointwiseNotRigid :
      ¬ FactorComparisonPointwiseAutomorphismRigidity (W := W) H)
    (hExtension : FactorComparisonPointwiseAutomorphismExtensionProperty
      (W := W) H) :
    ¬ Subsingleton (H.comparison ≅ H.comparison) := by
  rcases
    (not_pointwiseAutomorphismRigidity_iff_hasNontrivialPointwiseAutomorphism
      (W := W) H).mp hPointwiseNotRigid with ⟨q⟩
  exact
    (not_targetAutomorphismRigidity_iff_exists_extendablePointwiseWitness
      (W := W) H).mpr ⟨q, hExtension q⟩

/-- The extension property closes the local v2.28 gap exactly. -/
theorem pointwiseRigidity_iff_targetRigidity_of_extensionProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R)
    (hExtension : FactorComparisonPointwiseAutomorphismExtensionProperty
      (W := W) H) :
    FactorComparisonPointwiseAutomorphismRigidity (W := W) H ↔
      Subsingleton (H.comparison ≅ H.comparison) := by
  classical
  constructor
  · intro hPointwise
    exact subsingleton_factorComparisonAutomorphismIso_of_pointwiseRigidity
      W H hPointwise
  · intro hTarget
    by_contra hPointwiseNotRigid
    exact
      (not_targetRigidity_of_not_pointwiseRigidity_and_extensionProperty
        (W := W) H hPointwiseNotRigid hExtension) hTarget

/-- Uniform extension property over every factor morphism into one coherent
universal datum. -/
def HigherFactorComparisonPointwiseAutomorphismExtensionProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (_alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    FactorComparisonPointwiseAutomorphismExtensionProperty (W := W) H

/-- Under uniform extension, the v2.28 uniform pointwise criterion is not merely
sufficient but equivalent to target modification rigidity. -/
theorem higherPointwiseRigidity_iff_targetRigidity_of_extensionProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hExtension : HigherFactorComparisonPointwiseAutomorphismExtensionProperty
      (W := W) U) :
    HigherFactorComparisonPointwiseAutomorphismRigidity (W := W) U ↔
      HigherFactorComparisonAutomorphismRigidity (W := W) U := by
  classical
  constructor
  · exact higherFactorComparisonRigidity_of_pointwiseRigidity W U
  · intro hTarget H alpha
    exact
      (pointwiseRigidity_iff_targetRigidity_of_extensionProperty
        (W := W) H (hExtension H alpha)).mpr (hTarget H alpha)

/-- Uniformly witnessed coherence-extension obstruction: some factor has local
pointwise non-rigidity while every nontrivial witness there is coherence-blocked. -/
def HigherFactorComparisonCoherenceExtensionObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    FactorComparisonCoherenceExtensionObstruction (W := W) H

/-- If target modification rigidity already holds uniformly, then failure of
uniform pointwise rigidity is exactly the existence of a coherence-extension
obstruction at some factor. -/
theorem higherCoherenceExtensionObstruction_iff_not_pointwiseRigidity_of_targetRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hTarget : HigherFactorComparisonAutomorphismRigidity (W := W) U) :
    HigherFactorComparisonCoherenceExtensionObstruction (W := W) U ↔
      ¬ HigherFactorComparisonPointwiseAutomorphismRigidity (W := W) U := by
  classical
  constructor
  · rintro ⟨H, alpha, hObstruction⟩ hPointwise
    have hLocalPointwise := hPointwise H alpha
    exact
      ((coherenceExtensionObstruction_iff_pointwiseNonrigid_and_targetRigid
        (W := W) H).mp hObstruction).1 hLocalPointwise
  · intro hPointwiseNotRigid
    by_contra hNoObstruction
    apply hPointwiseNotRigid
    intro H alpha
    by_contra hLocalNotRigid
    have hLocalObstruction :
        FactorComparisonCoherenceExtensionObstruction (W := W) H :=
      (coherenceExtensionObstruction_iff_pointwiseNonrigid_and_targetRigid
        (W := W) H).mpr ⟨hLocalNotRigid, hTarget H alpha⟩
    exact hNoObstruction ⟨H, alpha, hLocalObstruction⟩

/-!
The remaining local gap after v2.28 is now exact:

```text
not pointwise rigid
  <->
there exists a nontrivial objectwise automorphism witness

not target rigid
  <->
there exists such a witness that extends coherently.
```

Hence target rigidity together with pointwise non-rigidity is not mysterious;
it is exactly the situation where nontrivial local automorphisms exist but all
of them fail the coherent extension problem.

No coherent extension property is proved in general here.  In particular this
file does not prove pointwise rigidity from target rigidity, does not prove
correction existence, and does not prove the general weak higher-localization
universal principle.
-/

end KUOS.DependentOriginationPointwiseExtensionObstructionV2_29
