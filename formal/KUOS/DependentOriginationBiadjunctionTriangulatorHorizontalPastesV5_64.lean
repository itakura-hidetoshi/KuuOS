import KUOS.DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63

namespace KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58.Generic
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59
open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationStrongTransModificationPrecompositionV5_61
open KUOS.DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63

set_option autoImplicit false

noncomputable section

/-!
# Modification-level horizontal pastes for biadjunction triangulators v5.64

v5.61 and v5.63 show that a functor-bicategory triangulator is preserved by
arbitrary pseudofunctor precomposition and postcomposition.  The latter keeps
the non-strict identity comparison explicitly through the postcomposing
pseudofunctor's mapId cell.

For an incoherent biadjunction datum

  F : B -> C,
  G : C -> B,

there are therefore two canonically contracted triangle StrongTrans values on
each roundtrip pseudofunctor:

* on F ; G, postcompose the forward triangulator by G, or precompose the
  reverse triangulator by F;
* on G ; F, precompose the forward triangulator by G, or postcompose the
  reverse triangulator by F.

This file vertically pastes the two stored contractions through the common
native identity StrongTrans.  The result is an invertible modification
comparing the two horizontally whiskered triangle representatives on each
roundtrip.

No swallowtail equation is asserted.  These pastes are only the typed
modification-level interface on which the later swallowtail predicates can be
stated.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace IncoherentBiadjunctionDatum

variable (D : IncoherentBiadjunctionDatum B C)

/-- The source roundtrip F ; G. -/
abbrev sourceRoundtrip : Pseudofunctor B B :=
  Pseudofunctor.comp D.base.whitehead.forward D.base.quasiInverse

/-- The target roundtrip G ; F. -/
abbrev targetRoundtrip : Pseudofunctor C C :=
  Pseudofunctor.comp D.base.quasiInverse D.base.whitehead.forward

/-! The StrongTrans hom categories are scoped instances in Mathlib.  At this
generic two-bicategory boundary the universe carried by `Category` is not an
output parameter, so elaborating `Iso.trans` cannot reliably reconstruct it
from the endpoints alone.  Bind the exact native hom categories explicitly,
as in v5.61 and v5.63. -/

local instance sourceRoundtripStrongTransHomCategory :
    Category
      (Pseudofunctor.StrongTrans (sourceRoundtrip D) (sourceRoundtrip D)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := sourceRoundtrip D) (G := sourceRoundtrip D)

local instance targetRoundtripStrongTransHomCategory :
    Category
      (Pseudofunctor.StrongTrans (targetRoundtrip D) (targetRoundtrip D)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := C) (C := C)
    (F := targetRoundtrip D) (G := targetRoundtrip D)

/-- Forward triangulator horizontally whiskered on the right by G.
The v5.63 postcomposition construction retains G.mapId in the contraction. -/
def sourceForwardTriangulator :
    FunctorBicategoryTriangulator (sourceRoundtrip D) :=
  StrongTransPostcomposition.triangulator
    D.base.whitehead.forward
    D.base.quasiInverse
    D.triangulators.forward

/-- Reverse triangulator horizontally whiskered on the left by F.
Precomposition preserves the identity StrongTrans definitionally. -/
def sourceReverseTriangulator :
    FunctorBicategoryTriangulator (sourceRoundtrip D) :=
  StrongTransPrecomposition.triangulator
    D.base.whitehead.forward
    D.triangulators.reverse

/-- Forward triangulator horizontally whiskered on the left by G. -/
def targetForwardTriangulator :
    FunctorBicategoryTriangulator (targetRoundtrip D) :=
  StrongTransPrecomposition.triangulator
    D.base.quasiInverse
    D.triangulators.forward

/-- Reverse triangulator horizontally whiskered on the right by F.
The v5.63 postcomposition construction retains F.mapId in the contraction. -/
def targetReverseTriangulator :
    FunctorBicategoryTriangulator (targetRoundtrip D) :=
  StrongTransPostcomposition.triangulator
    D.base.quasiInverse
    D.base.whitehead.forward
    D.triangulators.reverse

/-- Source-side horizontal paste.

Both whiskered triangles contract to the same native identity StrongTrans on
F ; G.  Compose the forward contraction with the inverse reverse contraction
to compare the triangle representatives themselves. -/
def sourceHorizontalPaste :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans (sourceRoundtrip D) (sourceRoundtrip D))
      (Pseudofunctor.StrongTrans.homCategory
        (B := B) (C := B)
        (F := sourceRoundtrip D) (G := sourceRoundtrip D))
      (sourceForwardTriangulator D).triangle
      (sourceReverseTriangulator D).triangle :=
  (sourceForwardTriangulator D).contraction ≪≫
    (sourceReverseTriangulator D).contraction.symm

/-- Target-side horizontal paste, obtained through the common native identity
StrongTrans on G ; F. -/
def targetHorizontalPaste :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans (targetRoundtrip D) (targetRoundtrip D))
      (Pseudofunctor.StrongTrans.homCategory
        (B := C) (C := C)
        (F := targetRoundtrip D) (G := targetRoundtrip D))
      (targetForwardTriangulator D).triangle
      (targetReverseTriangulator D).triangle :=
  (targetForwardTriangulator D).contraction ≪≫
    (targetReverseTriangulator D).contraction.symm

@[simp] theorem sourceForwardTriangulator_triangle :
    (sourceForwardTriangulator D).triangle =
      KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62.StrongTransPostcomposition.strongTrans
        D.base.quasiInverse
        D.triangulators.forward.triangle :=
  rfl

@[simp] theorem sourceReverseTriangulator_triangle :
    (sourceReverseTriangulator D).triangle =
      StrongTransPrecomposition.strongTrans
        D.base.whitehead.forward
        D.triangulators.reverse.triangle :=
  rfl

@[simp] theorem targetForwardTriangulator_triangle :
    (targetForwardTriangulator D).triangle =
      StrongTransPrecomposition.strongTrans
        D.base.quasiInverse
        D.triangulators.forward.triangle :=
  rfl

@[simp] theorem targetReverseTriangulator_triangle :
    (targetReverseTriangulator D).triangle =
      KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62.StrongTransPostcomposition.strongTrans
        D.base.whitehead.forward
        D.triangulators.reverse.triangle :=
  rfl

@[simp] theorem sourceHorizontalPaste_hom :
    (sourceHorizontalPaste D).hom =
      (sourceForwardTriangulator D).contraction.hom ≫
        (sourceReverseTriangulator D).contraction.inv :=
  rfl

@[simp] theorem targetHorizontalPaste_hom :
    (targetHorizontalPaste D).hom =
      (targetForwardTriangulator D).contraction.hom ≫
        (targetReverseTriangulator D).contraction.inv :=
  rfl

end IncoherentBiadjunctionDatum

end Generic

open Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The source-side generic horizontal paste specialized to the unchanged
actual-lift incoherent biadjunction datum. -/
def actualLiftSourceHorizontalPaste :=
  Generic.IncoherentBiadjunctionDatum.sourceHorizontalPaste
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The target-side generic horizontal paste specialized to the unchanged
actual-lift incoherent biadjunction datum. -/
def actualLiftTargetHorizontalPaste :=
  Generic.IncoherentBiadjunctionDatum.targetHorizontalPaste
    (exactLiftableActualLiftIncoherentBiadjunctionDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-!
## Boundary after v5.64

The two triangle contractions can now be horizontally whiskered in both
directions and vertically pasted at modification level without re-choosing
F, G, eta, eps, or either triangulator.

The postcomposition halves keep their canonical mapId correction from v5.63;
the precomposition halves use the definitional identity preservation proved
in v5.61.  Thus the resulting source and target paste isomorphisms retain the
non-strict pseudofunctor coherence rather than silently strictifying it.

What is still absent is exactly the next datum: a typed swallowtail equation
identifying the appropriate paste built from eta/eps, associators/unitors, and
these contraction modifications.  No coherent biadjunction is claimed here.
-/

#print axioms Generic.IncoherentBiadjunctionDatum.sourceForwardTriangulator
#print axioms Generic.IncoherentBiadjunctionDatum.sourceReverseTriangulator
#print axioms Generic.IncoherentBiadjunctionDatum.targetForwardTriangulator
#print axioms Generic.IncoherentBiadjunctionDatum.targetReverseTriangulator
#print axioms Generic.IncoherentBiadjunctionDatum.sourceHorizontalPaste
#print axioms Generic.IncoherentBiadjunctionDatum.targetHorizontalPaste
#print axioms actualLiftSourceHorizontalPaste
#print axioms actualLiftTargetHorizontalPaste

end

end KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64
