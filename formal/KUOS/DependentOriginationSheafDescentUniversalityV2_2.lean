import Mathlib
import KUOS.DependentOriginationEffectiveDescentComparisonV2_1

namespace KUOS.DependentOriginationSheafDescentUniversalityV2_2

open CategoryTheory

universe u v uA vA

/-!
# Dependent-origination sheaf-descent universality v2.2

The v2.1 layer rewrites effective contextual descent as bijectivity of one
canonical root-to-compatible-family comparison map.  This file records the
standard categorical universal object that becomes available once a family of
such covers has been promoted to a Grothendieck topology `J` on a site.

For a site `(Site, J)`, Mathlib's sheafification is left adjoint to the fully
faithful inclusion of sheaves into presheaves.  Therefore every map from a
presheaf `P` to a `J`-sheaf factors uniquely through the canonical unit

```text
P -> sheafify J P.
```

Equivalently, for every sheaf `Q`, there is a natural hom-set equivalence

```text
Hom_Sheaf(sheafify(P), Q)
  ≃
Hom_Presheaf(P, forget(Q)).
```

This is an exact universal property for the semantic descent-completion axis.
It is not yet the final KuuOS `DO(C,W,J,H)` theorem.  In particular, a later
bridge must identify KuuOS covariant refinement transport with presheaves on the
opposite refinement site, prove that the generated topology captures the v2.1
comparison maps, and then combine this reflection with presentation
localization `W` and higher coherence `H`.
-/

variable {Site : Type u} [Category.{v} Site]
variable (J : GrothendieckTopology Site)
variable {A : Type uA} [Category.{vA} A]
variable [HasWeakSheafify J A]

/-- The reflective semantic descent completion. -/
noncomputable abbrev descentCompletionFunctor :
    (Siteᵒᵖ ⥤ A) ⥤ Sheaf J A :=
  presheafToSheaf J A

/-- Forget a descent-complete system back to its underlying presheaf. -/
abbrev descentForgetFunctor :
    Sheaf J A ⥤ (Siteᵒᵖ ⥤ A) :=
  sheafToPresheaf J A

/-- Sheafification is left adjoint to the inclusion of descent-complete
systems. -/
noncomputable def descentCompletionAdjunction :
    descentCompletionFunctor (A := A) J ⊣ descentForgetFunctor (A := A) J :=
  sheafificationAdjunction J A

/-- The underlying presheaf of the semantic descent completion of `P`. -/
noncomputable abbrev descentCompletionObj
    (P : Siteᵒᵖ ⥤ A) : Siteᵒᵖ ⥤ A :=
  sheafify J P

/-- The canonical map from a contextual presheaf to its descent completion. -/
noncomputable abbrev descentUnit
    (P : Siteᵒᵖ ⥤ A) :
    P ⟶ descentCompletionObj J P :=
  toSheafify J P

/-- The completed object satisfies the sheaf/descent condition. -/
theorem descentCompletion_isSheaf
    (P : Siteᵒᵖ ⥤ A) :
    Presheaf.IsSheaf J (descentCompletionObj J P) :=
  ((presheafToSheaf J A).obj P).property

/-- The universal mapping property in its clean adjunction form. -/
noncomputable def descentHomEquiv
    (P : Siteᵒᵖ ⥤ A)
    (Q : Sheaf J A) :
    ((descentCompletionFunctor J).obj P ⟶ Q) ≃
      (P ⟶ (descentForgetFunctor J).obj Q) :=
  (descentCompletionAdjunction J).homEquiv P Q

/-- Factor a map from an arbitrary presheaf to any descent-complete presheaf
through the canonical descent completion. -/
noncomputable def descentFactor
    {P Q : Siteᵒᵖ ⥤ A}
    (η : P ⟶ Q)
    (hQ : Presheaf.IsSheaf J Q) :
    descentCompletionObj J P ⟶ Q :=
  sheafifyLift J η hQ

/-- The factor supplied by sheafification really factors the original map. -/
@[reassoc (attr := simp)] theorem descentUnit_factor
    {P Q : Siteᵒᵖ ⥤ A}
    (η : P ⟶ Q)
    (hQ : Presheaf.IsSheaf J Q) :
    descentUnit J P ≫ descentFactor J η hQ = η := by
  exact toSheafify_sheafifyLift J η hQ

/-- Essential uniqueness is strict at the presheaf-map level: every other map
out of the completion with the same factorization equation equals the canonical
factor. -/
theorem descentFactor_unique
    {P Q : Siteᵒᵖ ⥤ A}
    (η : P ⟶ Q)
    (hQ : Presheaf.IsSheaf J Q)
    (γ : descentCompletionObj J P ⟶ Q)
    (hγ : descentUnit J P ≫ γ = η) :
    γ = descentFactor J η hQ := by
  exact sheafifyLift_unique J η hQ γ hγ

/-- The descent-completion unit is natural in the original contextual
presheaf. -/
@[reassoc (attr := simp)] theorem descentUnit_naturality
    {P Q : Siteᵒᵖ ⥤ A}
    (η : P ⟶ Q) :
    η ≫ descentUnit J Q =
      descentUnit J P ≫ sheafifyMap J η := by
  exact toSheafify_naturality J η

/-- A system that already satisfies descent is unchanged by completion up to
canonical natural isomorphism. -/
noncomputable def alreadyDescentCompleteIso
    {P : Siteᵒᵖ ⥤ A}
    (hP : Presheaf.IsSheaf J P) :
    P ≅ descentCompletionObj J P :=
  isoSheafify J hP

/-!
The universal boundary established here is therefore:

```text
arbitrary contextual presheaf P
        |
        | unit
        v
sheafify_J(P)
        |
        | unique factor
        v
any J-descent-complete target Q.
```

The next theorem must be a variance-correct KuuOS bridge:

```text
FunctorialTransportSystem Context
  <-> presheaf on the opposite refinement site
```

followed by identification of the v2.1 effective comparison condition with the
Mathlib sheaf limit condition for a topology generated by the declared
refinement covers.
-/

end KUOS.DependentOriginationSheafDescentUniversalityV2_2
