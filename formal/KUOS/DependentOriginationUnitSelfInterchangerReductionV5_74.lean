import KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73

namespace KUOS.DependentOriginationUnitSelfInterchangerReductionV5_74

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Unit self-interchanger reduction lemmas v5.74

The v5.73 modification-naturality obstruction should not be discharged by a
single large simplifier call.  This file isolates the three substantive
StrongTrans equations which remain after bicategorical reassociation:

1. eta/eta exchange for the naturality 2-cell eta.naturality(f);
2. composition coherence for f followed by eta_Y;
3. composition coherence for eta_X followed by R.map f.

The identity pseudofunctor's compositor is normalized away explicitly in the
two composition lemmas.  R itself remains fully non-strict: every R.mapComp
and R.map₂ term is retained.

These lemmas are generic in R and eta.  They introduce no new coherence data.
-/

namespace Generic

universe uB vB wB

variable {B : Type uB} [Bicategory.{wB, vB} B]

namespace UnitSelfInterchangerReduction

variable (R : Pseudofunctor B B)
variable (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R)

/-- The forward eta/eta exchange.  This is the generic content of v5.69,
now independent of any biadjunction packaging. -/
theorem selfExchange
    {X Y : B} (f : X ⟶ Y) :
    (Pseudofunctor.id B).map₂ (eta.naturality f).hom ▷
          eta.app (R.obj Y) ≫
        (eta.naturality (eta.app X ≫ R.map f)).hom =
      (eta.naturality
        ((Pseudofunctor.id B).map f ≫ eta.app Y)).hom ≫
        eta.app X ◁ R.map₂ (eta.naturality f).hom :=
  eta.naturality_naturality (eta.naturality f).hom

/-- The inverse eta/eta exchange, in the orientation used by the v5.73
component family. -/
theorem selfExchangeInv
    {X Y : B} (f : X ⟶ Y) :
    (Pseudofunctor.id B).map₂ (eta.naturality f).inv ▷
          eta.app (R.obj Y) ≫
        (eta.naturality
          ((Pseudofunctor.id B).map f ≫ eta.app Y)).hom =
      (eta.naturality (eta.app X ≫ R.map f)).hom ≫
        eta.app X ◁ R.map₂ (eta.naturality f).inv :=
  eta.naturality_naturality (eta.naturality f).inv

/-- Composition coherence on the left composite f ; eta_Y, with the identity
pseudofunctor compositor removed but every R-compositor retained. -/
theorem naturalityComp_f_eta
    {X Y : B} (f : X ⟶ Y) :
    (eta.naturality (f ≫ eta.app Y)).hom ≫
        eta.app X ◁ (R.mapComp f (eta.app Y)).hom =
      (α_ f (eta.app Y) (eta.app (R.obj Y))).hom ≫
        f ◁ (eta.naturality (eta.app Y)).hom ≫
        (α_ f (eta.app Y) (R.map (eta.app Y))).inv ≫
        (eta.naturality f).hom ▷ R.map (eta.app Y) ≫
        (α_ (eta.app X) (R.map f) (R.map (eta.app Y))).hom := by
  have h := eta.naturality_comp f (eta.app Y)
  change
    (eta.naturality (f ≫ eta.app Y)).hom ≫
        eta.app X ◁ (R.mapComp f (eta.app Y)).hom =
      (𝟙 (f ≫ eta.app Y)) ▷ eta.app (R.obj Y) ≫
        (α_ f (eta.app Y) (eta.app (R.obj Y))).hom ≫
        f ◁ (eta.naturality (eta.app Y)).hom ≫
        (α_ f (eta.app Y) (R.map (eta.app Y))).inv ≫
        (eta.naturality f).hom ▷ R.map (eta.app Y) ≫
        (α_ (eta.app X) (R.map f) (R.map (eta.app Y))).hom at h
  rw [Bicategory.id_whiskerRight, Category.id_comp] at h
  exact h

/-- Composition coherence on the right composite eta_X ; R.map f, again
normalizing only the identity pseudofunctor and retaining R.mapComp. -/
theorem naturalityComp_eta_Rmap
    {X Y : B} (f : X ⟶ Y) :
    (eta.naturality (eta.app X ≫ R.map f)).hom ≫
        eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).hom =
      (α_ (eta.app X) (R.map f) (eta.app (R.obj Y))).hom ≫
        eta.app X ◁ (eta.naturality (R.map f)).hom ≫
        (α_ (eta.app X) (eta.app (R.obj X))
          (R.map (R.map f))).inv ≫
        (eta.naturality (eta.app X)).hom ▷ R.map (R.map f) ≫
        (α_ (eta.app X) (R.map (eta.app X))
          (R.map (R.map f))).hom := by
  have h := eta.naturality_comp (eta.app X) (R.map f)
  change
    (eta.naturality (eta.app X ≫ R.map f)).hom ≫
        eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).hom =
      (𝟙 (eta.app X ≫ R.map f)) ▷ eta.app (R.obj Y) ≫
        (α_ (eta.app X) (R.map f) (eta.app (R.obj Y))).hom ≫
        eta.app X ◁ (eta.naturality (R.map f)).hom ≫
        (α_ (eta.app X) (eta.app (R.obj X))
          (R.map (R.map f))).inv ≫
        (eta.naturality (eta.app X)).hom ▷ R.map (R.map f) ≫
        (α_ (eta.app X) (R.map (eta.app X))
          (R.map (R.map f))).hom at h
  rw [Bicategory.id_whiskerRight, Category.id_comp] at h
  exact h

end UnitSelfInterchangerReduction

end Generic

/-!
## Boundary after v5.74

The v5.73 naturality obstruction has now been decomposed into named native
StrongTrans laws.  The next proof may use bicategory coherence only to expose
these three equations, then rewrite once with selfExchangeInv and twice with
the normalized composition lemmas.

This keeps the proof auditable: structural reassociation is separated from
the unique eta/eta exchange.
-/

#print axioms Generic.UnitSelfInterchangerReduction.selfExchange
#print axioms Generic.UnitSelfInterchangerReduction.selfExchangeInv
#print axioms Generic.UnitSelfInterchangerReduction.naturalityComp_f_eta
#print axioms Generic.UnitSelfInterchangerReduction.naturalityComp_eta_Rmap

end

end KUOS.DependentOriginationUnitSelfInterchangerReductionV5_74
