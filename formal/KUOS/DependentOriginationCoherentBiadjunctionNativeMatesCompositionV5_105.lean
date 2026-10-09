import KUOS.DependentOriginationCoherentBiadjunctionNativeMatesV5_104

namespace KUOS.DependentOriginationCoherentBiadjunctionNativeMatesCompositionV5_105

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesV5_104

set_option autoImplicit false
noncomputable section

/-!
# Native mathlib mate composition for unchanged KuuOS actual lifts (v5.105)

v5.104 proved that the ORIGINAL source-unit and target-counit naturality
2-cells have native bicategorical mates and that unmating recovers them.

This file adds:
1. vertical pasting of the original source/target naturality squares,
   matched to vertical pasting of their genuine right mates using
   mathlib's \`Bicategory.mateEquiv_vcomp\`;
2. preservation of the ORIGINAL source and target pseudofunctor
   mapComp comparison cells under this vertical-pasting interface, via
   the unchanged StrongTrans.naturality_comp proofs;
3. a universe-polymorphic horizontal-pasting interface for four actual
   chosen equivalences, using mathlib's \`mateEquiv_hcomp\`.

The F/G, eta/eps, non-strict G.mapComp, object equivalences and
triangulators are not modified. We do not identify the target composite
mate with a raw pasted mate without the necessary mapComp transport.
-/

namespace Generic

universe uB vB wB
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b c d e f : B}
variable {g : a ⟶ d} {h : b ⟶ e} {k : c ⟶ f}

/-- Horizontal mate pasting for four *specified* original adjoint
equivalences; neither side replaces an original adjunction by a strict one. -/
theorem originalEquivalences_mate_hcomp
    (e₁ : Bicategory.Equivalence a b)
    (e₂ : Bicategory.Equivalence d e)
    (e₃ : Bicategory.Equivalence b c)
    (e₄ : Bicategory.Equivalence e f)
    (α : g ≫ e₂.hom ⟶ e₁.hom ≫ h)
    (β : h ≫ e₄.hom ⟶ e₃.hom ≫ k) :
    (Bicategory.mateEquiv
        ((nativeAdjunctionOfEquivalence e₁).comp
          (nativeAdjunctionOfEquivalence e₃))
        ((nativeAdjunctionOfEquivalence e₂).comp
          (nativeAdjunctionOfEquivalence e₄)))
        (Bicategory.leftAdjointSquare.hcomp α β) =
      Bicategory.rightAdjointSquare.hcomp
        (Bicategory.mateEquiv
          (nativeAdjunctionOfEquivalence e₁)
          (nativeAdjunctionOfEquivalence e₂) α)
        (Bicategory.mateEquiv
          (nativeAdjunctionOfEquivalence e₃)
          (nativeAdjunctionOfEquivalence e₄) β) := by
  exact Bicategory.mateEquiv_hcomp
    (nativeAdjunctionOfEquivalence e₁)
    (nativeAdjunctionOfEquivalence e₂)
    (nativeAdjunctionOfEquivalence e₃)
    (nativeAdjunctionOfEquivalence e₄) α β

end Generic

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

section Source

variable {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel}

/-- Vertical composite of two *unchanged* original right mates, retaining
both chosen unit-component right adjuncts and both original R_L.map maps. -/
def actualLiftSourceUnitMateVComp (f : X ⟶ Y) (g : Y ⟶ Z) :
    (actualLiftSourceNativeAdjHom (W := W) A X).r ≫ (f ≫ g) ⟶
      (((actualLiftSourceRoundtrip (W := W) A).map f) ≫
        ((actualLiftSourceRoundtrip (W := W) A).map g)) ≫
          (actualLiftSourceNativeAdjHom (W := W) A Z).r :=
  Bicategory.rightAdjointSquare.vcomp
    (actualLiftSourceUnitRightMate (W := W) A f)
    (actualLiftSourceUnitRightMate (W := W) A g)

/-- Full native \`mateEquiv_vcomp\` specialized to two distinct source
1-cells of the original actual-lift bicategory. -/
theorem actualLiftSourceUnitMateVComp_eq
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (Bicategory.mateEquiv
        (actualLiftSourceNativeAdjHom (W := W) A X).adj
        (actualLiftSourceNativeAdjHom (W := W) A Z).adj)
        (Bicategory.leftAdjointSquare.vcomp
          ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom
          ((actualLiftSourceRoundtripUnit (W := W) A).naturality g).hom) =
      actualLiftSourceUnitMateVComp (W := W) A f g := by
  exact Bicategory.mateEquiv_vcomp
    (actualLiftSourceNativeAdjHom (W := W) A X).adj
    (actualLiftSourceNativeAdjHom (W := W) A Y).adj
    (actualLiftSourceNativeAdjHom (W := W) A Z).adj
    ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom
    ((actualLiftSourceRoundtripUnit (W := W) A).naturality g).hom

/-- Native source \`naturality_comp\` equals the genuine mathlib left
square paste AFTER transporting along the original R_L.mapComp hom.
This is the key non-strict comparison, not a fictitious strict R_L. -/
theorem actualLiftSourceUnitNativeComp_eq_leftPaste
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((actualLiftSourceRoundtripUnit (W := W) A).naturality (f ≫ g)).hom ≫
        (actualLiftSourceRoundtripUnit (W := W) A).app X ◁
          ((actualLiftSourceRoundtrip (W := W) A).mapComp f g).hom =
      Bicategory.leftAdjointSquare.vcomp
        ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom
        ((actualLiftSourceRoundtripUnit (W := W) A).naturality g).hom := by
  have hIdComp :
      ((Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel)).mapComp f g).hom =
        𝟙 (f ≫ g) := rfl
  have hIdMapF :
      (Pseudofunctor.id
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)).map f = f := rfl
  have hIdMapG :
      (Pseudofunctor.id
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)).map g = g := rfl
  have hNative := (actualLiftSourceRoundtripUnit (W := W) A).naturality_comp f g
  rw [hIdComp] at hNative
  simpa only [hIdMapF, hIdMapG, Bicategory.id_whiskerRight,
    Category.id_comp, Bicategory.leftAdjointSquare.vcomp] using hNative

/-- The original source compositor-corrected naturality for f;g is
exactly the native VComp of the two original right mates. -/
theorem actualLiftSourceUnitMateComp_native
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (Bicategory.mateEquiv
        (actualLiftSourceNativeAdjHom (W := W) A X).adj
        (actualLiftSourceNativeAdjHom (W := W) A Z).adj)
        (((actualLiftSourceRoundtripUnit (W := W) A).naturality (f ≫ g)).hom ≫
          (actualLiftSourceRoundtripUnit (W := W) A).app X ◁
            ((actualLiftSourceRoundtrip (W := W) A).mapComp f g).hom) =
      actualLiftSourceUnitMateVComp (W := W) A f g := by
  exact
    (congrArg
      (Bicategory.mateEquiv
        (actualLiftSourceNativeAdjHom (W := W) A X).adj
        (actualLiftSourceNativeAdjHom (W := W) A Z).adj)
      (actualLiftSourceUnitNativeComp_eq_leftPaste (W := W) A f g)).trans
      (actualLiftSourceUnitMateVComp_eq (W := W) A f g)

end Source

section Target

variable {X Y Z : ActualLiftTarget.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel}

/-- Right-mate vertical paste of two unchanged target counit
naturality squares, with the actual G;F maps. -/
def actualLiftTargetCounitMateVComp (f : X ⟶ Y) (g : Y ⟶ Z) :
    (actualLiftTargetNativeAdjHom (W := W) A X).r ≫
        (((actualLiftTargetRoundtrip (W := W) A).map f) ≫
          ((actualLiftTargetRoundtrip (W := W) A).map g)) ⟶
      (f ≫ g) ≫ (actualLiftTargetNativeAdjHom (W := W) A Z).r :=
  Bicategory.rightAdjointSquare.vcomp
    (actualLiftTargetCounitRightMate (W := W) A f)
    (actualLiftTargetCounitRightMate (W := W) A g)

/-- Target mate pastes are native to mathlib's bicategory of adjuncts. -/
theorem actualLiftTargetCounitMateVComp_eq
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (Bicategory.mateEquiv
        (actualLiftTargetNativeAdjHom (W := W) A X).adj
        (actualLiftTargetNativeAdjHom (W := W) A Z).adj)
        (Bicategory.leftAdjointSquare.vcomp
          ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom
          ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom) =
      actualLiftTargetCounitMateVComp (W := W) A f g := by
  exact Bicategory.mateEquiv_vcomp
    (actualLiftTargetNativeAdjHom (W := W) A X).adj
    (actualLiftTargetNativeAdjHom (W := W) A Y).adj
    (actualLiftTargetNativeAdjHom (W := W) A Z).adj
    ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom
    ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom

/-- Target \`naturality_comp\` exposes the actual non-strict R_E.mapComp
factor before the two original naturality squares are pasted.  The
target identity pseudofunctor's compositor remains its literal identity. -/
theorem actualLiftTargetCounitNativeComp_eq_leftPaste
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((actualLiftTargetRoundtripCounit (W := W) A).naturality (f ≫ g)).hom ≫
      (actualLiftTargetRoundtripCounit (W := W) A).app X ◁ 𝟙 (f ≫ g) =
      ((actualLiftTargetRoundtrip (W := W) A).mapComp f g).hom ▷
        (actualLiftTargetRoundtripCounit (W := W) A).app Z ≫
          Bicategory.leftAdjointSquare.vcomp
            ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom
            ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom := by
  simpa only [Bicategory.leftAdjointSquare.vcomp] using
    (actualLiftTargetRoundtripCounit (W := W) A).naturality_comp f g

/-- Mating the original target counit's entire composer-corrected
natComp equality, without asserting that the mapComp correction is absent.
The bare VComp of mates is separately given by the theorem above. -/
theorem actualLiftTargetCounitMateComp_native
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (Bicategory.mateEquiv
      (actualLiftTargetNativeAdjHom (W := W) A X).adj
      (actualLiftTargetNativeAdjHom (W := W) A Z).adj)
      (((actualLiftTargetRoundtripCounit (W := W) A).naturality (f ≫ g)).hom ≫
        (actualLiftTargetRoundtripCounit (W := W) A).app X ◁ 𝟙 (f ≫ g)) =
    (Bicategory.mateEquiv
      (actualLiftTargetNativeAdjHom (W := W) A X).adj
      (actualLiftTargetNativeAdjHom (W := W) A Z).adj)
      (((actualLiftTargetRoundtrip (W := W) A).mapComp f g).hom ▷
        (actualLiftTargetRoundtripCounit (W := W) A).app Z ≫
          Bicategory.leftAdjointSquare.vcomp
            ((actualLiftTargetRoundtripCounit (W := W) A).naturality f).hom
            ((actualLiftTargetRoundtripCounit (W := W) A).naturality g).hom) := by
  exact congrArg _ (actualLiftTargetCounitNativeComp_eq_leftPaste (W := W) A f g)

end Target

#print axioms Generic.originalEquivalences_mate_hcomp
#print axioms actualLiftSourceUnitMateVComp
#print axioms actualLiftSourceUnitMateVComp_eq
#print axioms actualLiftSourceUnitNativeComp_eq_leftPaste
#print axioms actualLiftSourceUnitMateComp_native
#print axioms actualLiftTargetCounitMateVComp
#print axioms actualLiftTargetCounitMateVComp_eq
#print axioms actualLiftTargetCounitNativeComp_eq_leftPaste
#print axioms actualLiftTargetCounitMateComp_native

end

end KUOS.DependentOriginationCoherentBiadjunctionNativeMatesCompositionV5_105
