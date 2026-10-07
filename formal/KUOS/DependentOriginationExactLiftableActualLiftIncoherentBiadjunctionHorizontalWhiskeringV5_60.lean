import KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59

namespace KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionHorizontalWhiskeringV5_60

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleV5_55
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

set_option autoImplicit false

noncomputable section

/-!
# Horizontal whiskering from an incoherent biadjunction datum v5.60

v5.59 packages F, G, eta, eps and the two triangulators, but deliberately does
not add a swallowtail law.

The first prerequisite for writing such a higher-coherence law is to expose
the non-strict horizontal whiskering already proved concretely in v5.53/v5.54:

* precompose eta by G, producing G => G ; (F ; G);
* postcompose eps by G, producing (G ; F) ; G => G;
* compare the two native triple bracketings through the actual mapId/mapComp
  comparators rather than treating them as definitionally equal;
* reassociate only the source coherence of the counit factor;
* vertically compose the two resulting StrongTrans values.

This file generalizes that construction to any
`IncoherentBiadjunctionDatum`.  No new 2-cell or 3-cell is chosen.
In particular, no swallowtail equation is asserted here.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace IncoherentBiadjunctionDatum

variable (D : IncoherentBiadjunctionDatum B C)

/-- The source roundtrip F ; G stored in the unit endpoint. -/
abbrev sourceRoundtrip : Pseudofunctor B B :=
  Pseudofunctor.comp D.base.whitehead.forward D.base.quasiInverse

/-- The target roundtrip G ; F stored in the counit endpoint. -/
abbrev targetRoundtrip : Pseudofunctor C C :=
  Pseudofunctor.comp D.base.quasiInverse D.base.whitehead.forward

/-- Right-associated triple G ; (F ; G). -/
def quasiInverseTripleRight : Pseudofunctor C B :=
  Pseudofunctor.comp D.base.quasiInverse D.sourceRoundtrip

/-- Left-associated triple (G ; F) ; G. -/
def quasiInverseTripleLeft : Pseudofunctor C B :=
  Pseudofunctor.comp D.targetRoundtrip D.base.quasiInverse

/-- Precompose the stored source unit eta by the stored non-strict G.
This is exactly the generic v5.53 construction. -/
def quasiInverseUnitFactor :
    Pseudofunctor.StrongTrans
      D.base.quasiInverse
      D.quasiInverseTripleRight :=
  UnitPrecomposition.strongTrans
    D.base.quasiInverse
    D.base.unit

/-- Postcompose the stored target counit eps by the stored non-strict G.
The source is kept literally left-associated. -/
def quasiInverseCounitFactorLeft :
    Pseudofunctor.StrongTrans
      D.quasiInverseTripleLeft
      D.base.quasiInverse :=
  CounitPostcomposition.strongTrans
    D.base.quasiInverse
    D.base.counit

/-- The identity comparisons of the two native triple bracketings agree as
2-cells after expanding Pseudofunctor.comp. -/
theorem quasiInverseTriple_mapId_hom (Y : C) :
    (D.quasiInverseTripleLeft.mapId Y).hom =
      (D.quasiInverseTripleRight.mapId Y).hom :=
  TripleComparison.mapId_hom
    D.base.quasiInverse
    D.base.whitehead.forward
    D.base.quasiInverse
    Y

/-- The compositor comparisons of the two native triple bracketings agree.
No strict associativity of pseudofunctor composition is assumed. -/
theorem quasiInverseTriple_mapComp_hom
    {X Y Z : C} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (D.quasiInverseTripleLeft.mapComp f g).hom =
      (D.quasiInverseTripleRight.mapComp f g).hom :=
  TripleComparison.mapComp_hom
    D.base.quasiInverse
    D.base.whitehead.forward
    D.base.quasiInverse
    f g

/-- Reassociate only the source coherence of the postcomposed counit factor.
The app, naturality, and naturality_naturality fields are unchanged. -/
def quasiInverseCounitFactor :
    Pseudofunctor.StrongTrans
      D.quasiInverseTripleRight
      D.base.quasiInverse where
  app Y := D.quasiInverseCounitFactorLeft.app Y
  naturality f := D.quasiInverseCounitFactorLeft.naturality f
  naturality_naturality theta :=
    D.quasiInverseCounitFactorLeft.naturality_naturality theta
  naturality_id Y := by
    rw [← D.quasiInverseTriple_mapId_hom Y]
    exact D.quasiInverseCounitFactorLeft.naturality_id Y
  naturality_comp f g := by
    rw [← D.quasiInverseTriple_mapComp_hom f g]
    exact D.quasiInverseCounitFactorLeft.naturality_comp f g

/-- The reverse triangle obtained from the two native horizontal-whiskering
factors.  This is still only a StrongTrans; its contraction is stored
separately in v5.59's reverse triangulator. -/
def quasiInverseTriangle :
    Pseudofunctor.StrongTrans
      D.base.quasiInverse
      D.base.quasiInverse :=
  Pseudofunctor.StrongTrans.vcomp
    D.quasiInverseUnitFactor
    D.quasiInverseCounitFactor

@[simp] theorem quasiInverseUnitFactor_app (Y : C) :
    D.quasiInverseUnitFactor.app Y =
      D.base.unit.app (D.base.quasiInverse.obj Y) :=
  rfl

@[simp] theorem quasiInverseCounitFactorLeft_app (Y : C) :
    D.quasiInverseCounitFactorLeft.app Y =
      D.base.quasiInverse.map (D.base.counit.app Y) :=
  rfl

@[simp] theorem quasiInverseCounitFactor_app (Y : C) :
    D.quasiInverseCounitFactor.app Y =
      D.base.quasiInverse.map (D.base.counit.app Y) :=
  rfl

@[simp] theorem quasiInverseTriangle_app (Y : C) :
    D.quasiInverseTriangle.app Y =
      D.base.unit.app (D.base.quasiInverse.obj Y) ≫
        D.base.quasiInverse.map (D.base.counit.app Y) :=
  rfl

end IncoherentBiadjunctionDatum

end Generic

open Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Typed abbreviation for the v5.59 actual-lift datum. -/
abbrev actualLiftBiadjunctionDatum :=
  exactLiftableActualLiftIncoherentBiadjunctionDatum
    (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)

/-! ## Whole-record regressions to the already-proved v5.53--v5.55 data -/

@[simp] theorem actualLiftBiadjunctionDatum_quasiInverseTripleRight :
    (actualLiftBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).quasiInverseTripleRight =
      actualLiftQuasiInverseTriple
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem actualLiftBiadjunctionDatum_quasiInverseTripleLeft :
    (actualLiftBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).quasiInverseTripleLeft =
      actualLiftQuasiInverseCounitTriple
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem actualLiftBiadjunctionDatum_quasiInverseUnitFactor :
    (actualLiftBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).quasiInverseUnitFactor =
      actualLiftQuasiInverseRestrictedSourceUnit
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem actualLiftBiadjunctionDatum_quasiInverseCounitFactorLeft :
    (actualLiftBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).quasiInverseCounitFactorLeft =
      actualLiftQuasiInverseRestrictedTargetCounit
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem actualLiftBiadjunctionDatum_quasiInverseCounitFactor :
    (actualLiftBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).quasiInverseCounitFactor =
      actualLiftQuasiInverseRestrictedTargetCounitReassociated
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

@[simp] theorem actualLiftBiadjunctionDatum_quasiInverseTriangle :
    (actualLiftBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).quasiInverseTriangle =
      actualLiftQuasiInverseTriangle
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel) :=
  rfl

/-- The generic v5.60 reverse triangle is exactly the triangle stored by the
v5.59 reverse triangulator. -/
@[simp] theorem actualLiftBiadjunctionDatum_quasiInverseTriangle_eq_stored :
    (actualLiftBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).quasiInverseTriangle =
      (actualLiftBiadjunctionDatum
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).triangulators.reverse.triangle :=
  rfl

/-!
## Boundary after v5.60

For an arbitrary incoherent biadjunction datum, the reverse triangle now has a
fully generic non-strict construction from eta and eps:

  G
    -> G ; (F ; G)
    -> G.

The second arrow is obtained from the native left-associated postcomposition
(G ; F) ; G -> G only by the proved mapId/mapComp comparison of the two triple
bracketings.

Thus the StrongTrans-level horizontal whiskering needed by the reverse
triangle is no longer actual-lift-specific.  The next higher-coherence step is
modification-level whiskering of the stored triangulator contractions; no
such 3-cell operation is claimed in this file.
-/

#print axioms Generic.IncoherentBiadjunctionDatum.quasiInverseUnitFactor
#print axioms Generic.IncoherentBiadjunctionDatum.quasiInverseCounitFactorLeft
#print axioms Generic.IncoherentBiadjunctionDatum.quasiInverseTriple_mapId_hom
#print axioms Generic.IncoherentBiadjunctionDatum.quasiInverseTriple_mapComp_hom
#print axioms Generic.IncoherentBiadjunctionDatum.quasiInverseCounitFactor
#print axioms Generic.IncoherentBiadjunctionDatum.quasiInverseTriangle
#print axioms actualLiftBiadjunctionDatum_quasiInverseTriangle

end

end KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionHorizontalWhiskeringV5_60
