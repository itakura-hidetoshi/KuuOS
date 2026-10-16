import KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205

namespace KUOS.DependentOriginationGrayC60F55CrossRotationCocycleV5_206

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.206 / F59-F57-A: independent ORIGINAL F42/F54 cross-rotation
# full/faithful 3-Hom transport and three-chart typed cocycle

The v5.205 F56 context functor goes between independent original F42
physical source face paths AND independent original F54 bracket-tree
rotation route types, provided one ACTUAL C60 edge and the complete
original face and F55 Int×Int plus ZMod2 native source images agree.
Its faithfulness was proved, but not general fullness, two-sided
cancellation or three-chart NatIso with changing ORIGINAL F54 types.

This module:
  * proves FULLNESS for every original F47 mixed boundary 3-Hom,
    genuinely constructing a raw F47 witness as preimage;
  * proves four-source-boundary position bijection, full faithfulness;
  * proves actual two-sided, three-chart source 3-Hom cocycle
    and associated Mathlib NATURAL ISOMORPHISMS with three independently
    typed original F54 rotation path domains/codomains;
  * uses FULL native hom-set equality after dependent F47 quotient,
    never declares original F42 proof terms or F54 routes equal.

The cocycle holds IN THE EXPLICITLY ADJOINED F47 MIXED CATEGORY ONLY,
with all original types retained. The new Delta=(0,1;0) does NOT
belong to the nine original F55 generators; signed north-pentagon
curvature and global descent obstructions remain nonzero.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GenuineThreeIndependentOriginalFrames
variable {a b : D} {x y : E}

variable {n₀ n₀' m₀ m₀' n₁ n₁' m₁ m₁' n₂ n₂' m₂ m₂' : Nat}
variable {ma₀ mb₀ ma₁ mb₁ ma₂ mb₂ : Blocks a b}
variable {pa₀ pb₀ pa₁ pb₁ pa₂ pb₂ : Blocks x y}

variable {first₀ : OriginalF45BracketTree n₀ m₀ ma₀ pa₀ mb₀ pb₀}
variable {last₀ : OriginalF45BracketTree n₀' m₀' ma₀ pa₀ mb₀ pb₀}
variable {first₁ : OriginalF45BracketTree n₁ m₁ ma₁ pa₁ mb₁ pb₁}
variable {last₁ : OriginalF45BracketTree n₁' m₁' ma₁ pa₁ mb₁ pb₁}
variable {first₂ : OriginalF45BracketTree n₂ m₂ ma₂ pa₂ mb₂ pb₂}
variable {last₂ : OriginalF45BracketTree n₂' m₂' ma₂ pa₂ mb₂ pb₂}
variable {r₀ s₀ : OriginalF45BracketTree.DepthRotationRoute first₀ last₀}
variable {r₁ s₁ : OriginalF45BracketTree.DepthRotationRoute first₁ last₁}
variable {r₂ s₂ : OriginalF45BracketTree.DepthRotationRoute first₂ last₂}

variable {v₀ w₀ v₁ w₁ v₂ w₂ : IcosahedralDart}
variable {p₀ q₀ : Quiver.Path v₀ w₀}
variable {p₁ q₁ : Quiver.Path v₁ w₁}
variable {p₂ q₂ : Quiver.Path v₂ w₂}
variable {α₀ β₀ : C60F42PresentedFaceCell p₀ q₀}
variable {α₁ β₁ : C60F42PresentedFaceCell p₁ q₁}
variable {α₂ β₂ : C60F42PresentedFaceCell p₂ q₂}

variable (B₀ : C60F47SquareFrame α₀ β₀ r₀ s₀)
variable (B₁ : C60F47SquareFrame α₁ β₁ r₁ s₁)
variable (B₂ : C60F47SquareFrame α₂ β₂ r₂ s₂)

/-- A source 3-Hom cast justified by inspection of one of the
FOUR tagged original boundary positions, not by equating F42/F54
raw source objects. -/
def c60F57ContextRoundTripHomCast
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    c60F56ContextMixedPoint B₁ B₀
      (c60F56ContextMixedPoint B₀ B₁ X) ⟶
    c60F56ContextMixedPoint B₁ B₀
      (c60F56ContextMixedPoint B₀ B₁ Y) := by
  cases X <;> cases Y
  all_goals exact f

def c60F57ContextThreeChartHomCast
    {X Y : C60F47BoundaryPoint B₀}
    (f : c60F56ContextMixedPoint B₀ B₂ X ⟶
      c60F56ContextMixedPoint B₀ B₂ Y) :
    c60F56ContextMixedPoint B₁ B₂
      (c60F56ContextMixedPoint B₀ B₁ X) ⟶
    c60F56ContextMixedPoint B₁ B₂
      (c60F56ContextMixedPoint B₀ B₁ Y) := by
  cases X <;> cases Y
  all_goals exact f

/-- The FOUR source boundary positions remain in bijection even
though their underlying original F42 and F54/F55 route types are
INDEPENDENT and may differ between the two frames. -/
theorem c60F57CrossOriginalContext_objects_bijective :
    Function.Bijective (c60F56ContextMixedPoint B₀ B₁) := by
  constructor
  · intro X Y h
    cases X <;> cases Y <;>
      simp_all [c60F56ContextMixedPoint]
  · intro Y
    cases Y with
    | faceBefore => exact ⟨.faceBefore, rfl⟩
    | faceAfter => exact ⟨.faceAfter, rfl⟩
    | rotationBefore => exact ⟨.rotationBefore, rfl⟩
    | rotationAfter => exact ⟨.rotationAfter, rfl⟩

/-- NEW FULLNESS of the F56 cross-ORIGINAL-rotation context functor.
The preimage is an explicit genuine RAW F47 word, independently
reindexed BACK from B₁ to B₀ on all four proof-relevant boundaries.
The proof uses all native integer and parity coordinates in the
F47 kernel quotient, not an untyped abstract grade equivalence. -/
theorem c60F57CrossOriginalContext_full
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀}
    (g : (c60F56ContextMixedFunctor
      B₀ B₁ hedge hface hrotation).obj X ⟶
      (c60F56ContextMixedFunctor
        B₀ B₁ hedge hface hrotation).obj Y) :
    ∃ f : X ⟶ Y,
      (c60F56ContextMixedFunctor
        B₀ B₁ hedge hface hrotation).map f = g := by
  cases X <;> cases Y
  all_goals
    refine Quot.inductionOn g (fun raw => ?_)
    refine ⟨c60F47MixedOf (c60F56ContextMixedRaw B₁ B₀ raw), ?_⟩
    apply c60F47MixedGrayFunctor_faithful B₁
    change (c60F56ContextMixedRaw B₀ B₁
      (c60F56ContextMixedRaw B₁ B₀ raw)).toNative = raw.toNative
    calc
      _ = (c60F56ContextMixedRaw B₁ B₀ raw).toNative :=
        c60F56ContextMixedRaw_native B₀ B₁ hface hrotation _
      _ = raw.toNative :=
        c60F56ContextMixedRaw_native B₁ B₀
          hface.symm hrotation.symm raw

theorem c60F57CrossOriginalContext_hom_bijective
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀} :
    Function.Bijective
      (fun (f : X ⟶ Y) =>
        (c60F56ContextMixedFunctor
          B₀ B₁ hedge hface hrotation).map f) := by
  constructor
  · intro f g h
    exact c60F56ContextMixedFunctor_faithful
      B₀ B₁ hedge hface hrotation h
  · intro g
    exact c60F57CrossOriginalContext_full
      B₀ B₁ hedge hface hrotation g

/-- Two different genuinely TYPED original rotation/face
presentation transports are inverse on EVERY source mixed F47
3-arrow once the original full-native data match. -/
theorem c60F57CrossOriginalContext_roundTrip_map
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    (c60F56ContextMixedFunctor
      B₁ B₀ hedge.symm hface.symm hrotation.symm).map
      ((c60F56ContextMixedFunctor
        B₀ B₁ hedge hface hrotation).map f) =
      c60F57ContextRoundTripHomCast B₀ B₁ f := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful B₀
    calc
      c60F47MixedEval
        ((c60F56ContextMixedFunctor
          B₁ B₀ hedge.symm hface.symm hrotation.symm).map
          ((c60F56ContextMixedFunctor
            B₀ B₁ hedge hface hrotation).map f)) =
        c60F47MixedEval
          ((c60F56ContextMixedFunctor
            B₀ B₁ hedge hface hrotation).map f) :=
        c60F56ContextMixedFunctor_fullNative
          B₁ B₀ hedge.symm hface.symm hrotation.symm _
      _ = c60F47MixedEval f :=
        c60F56ContextMixedFunctor_fullNative
          B₀ B₁ hedge hface hrotation f

/-- Genuine three-chart source-categorical cocycle on arbitrary
mixed 3-Hom, with SEPARATE original F42 and F54 route types
for all THREE charts. All transitions act at the same actual
physical C60 edge and preserve the full native F43/F55 images. -/
theorem c60F57CrossOriginalContext_threeChart_map
    (hedge₀₁ : B₀.edge = B₁.edge)
    (hedge₁₂ : B₁.edge = B₂.edge)
    (hface₀₁ : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot₀₁ : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    (hface₁₂ : c60F44FaceThreeEval B₁.faceStep =
      c60F44FaceThreeEval B₂.faceStep)
    (hrot₁₂ : c60F44OriginalF55Eval B₁.rotationStep =
      c60F44OriginalF55Eval B₂.rotationStep)
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    (c60F56ContextMixedFunctor
      B₁ B₂ hedge₁₂ hface₁₂ hrot₁₂).map
      ((c60F56ContextMixedFunctor
        B₀ B₁ hedge₀₁ hface₀₁ hrot₀₁).map f) =
    c60F57ContextThreeChartHomCast B₀ B₁ B₂
      ((c60F56ContextMixedFunctor B₀ B₂
        (hedge₀₁.trans hedge₁₂)
        (hface₀₁.trans hface₁₂)
        (hrot₀₁.trans hrot₁₂)).map f) := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful B₂
    calc
      c60F47MixedEval
        ((c60F56ContextMixedFunctor
          B₁ B₂ hedge₁₂ hface₁₂ hrot₁₂).map
          ((c60F56ContextMixedFunctor
            B₀ B₁ hedge₀₁ hface₀₁ hrot₀₁).map f)) =
        c60F47MixedEval
          ((c60F56ContextMixedFunctor
            B₀ B₁ hedge₀₁ hface₀₁ hrot₀₁).map f) :=
        c60F56ContextMixedFunctor_fullNative
          B₁ B₂ hedge₁₂ hface₁₂ hrot₁₂ _
      _ = c60F47MixedEval f :=
        c60F56ContextMixedFunctor_fullNative
          B₀ B₁ hedge₀₁ hface₀₁ hrot₀₁ f
      _ = c60F47MixedEval
        ((c60F56ContextMixedFunctor B₀ B₂
          (hedge₀₁.trans hedge₁₂)
          (hface₀₁.trans hface₁₂)
          (hrot₀₁.trans hrot₁₂)).map f) :=
        (c60F56ContextMixedFunctor_fullNative B₀ B₂
          (hedge₀₁.trans hedge₁₂)
          (hface₀₁.trans hface₁₂)
          (hrot₀₁.trans hrot₁₂) f).symm

/-- A Mathlib natural isomorphism for THREE distinct original
F42 and F54/F55 typed contexts. Unlike F56-A, the source
rotation-route trees are NOT fixed across the three charts. -/
def c60F57CrossOriginalContext_threeChartNatIso
    (hedge₀₁ : B₀.edge = B₁.edge)
    (hedge₁₂ : B₁.edge = B₂.edge)
    (hface₀₁ : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot₀₁ : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    (hface₁₂ : c60F44FaceThreeEval B₁.faceStep =
      c60F44FaceThreeEval B₂.faceStep)
    (hrot₁₂ : c60F44OriginalF55Eval B₁.rotationStep =
      c60F44OriginalF55Eval B₂.rotationStep) :
    (c60F56ContextMixedFunctor
      B₀ B₁ hedge₀₁ hface₀₁ hrot₀₁) ⋙
      (c60F56ContextMixedFunctor
        B₁ B₂ hedge₁₂ hface₁₂ hrot₁₂) ≅
    c60F56ContextMixedFunctor B₀ B₂
      (hedge₀₁.trans hedge₁₂)
      (hface₀₁.trans hface₁₂)
      (hrot₀₁.trans hrot₁₂) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        calc
          _ = (c60F56ContextMixedFunctor
            B₁ B₂ hedge₁₂ hface₁₂ hrot₁₂).map
              ((c60F56ContextMixedFunctor
                B₀ B₁ hedge₀₁ hface₀₁ hrot₀₁).map f) :=
            Category.comp_id _
          _ = c60F57ContextThreeChartHomCast B₀ B₁ B₂
            ((c60F56ContextMixedFunctor B₀ B₂
              (hedge₀₁.trans hedge₁₂)
              (hface₀₁.trans hface₁₂)
              (hrot₀₁.trans hrot₁₂)).map f) :=
            c60F57CrossOriginalContext_threeChart_map
              B₀ B₁ B₂ hedge₀₁ hedge₁₂
              hface₀₁ hrot₀₁ hface₁₂ hrot₁₂ f
          _ = _ := (Category.id_comp _).symm)

/-- Two original source systems can change independently and
still have a categorical NATURAL round-trip isomorphism, not
merely target Gray equality or an unproven original F54
source identification. -/
def c60F57CrossOriginalContext_roundTripNatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep) :
    (c60F56ContextMixedFunctor
      B₀ B₁ hedge hface hrotation) ⋙
      (c60F56ContextMixedFunctor
        B₁ B₀ hedge.symm hface.symm hrotation.symm) ≅
    𝟭 (C60F47BoundaryPoint B₀) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        calc
          _ = (c60F56ContextMixedFunctor
            B₁ B₀ hedge.symm hface.symm hrotation.symm).map
              ((c60F56ContextMixedFunctor
                B₀ B₁ hedge hface hrotation).map f) :=
            Category.comp_id _
          _ = c60F57ContextRoundTripHomCast B₀ B₁ f :=
            c60F57CrossOriginalContext_roundTrip_map
              B₀ B₁ hedge hface hrotation f
          _ = _ := (Category.id_comp _).symm)

end GenuineThreeIndependentOriginalFrames

#print axioms c60F57ContextRoundTripHomCast
#print axioms c60F57ContextThreeChartHomCast
#print axioms c60F57CrossOriginalContext_objects_bijective
#print axioms c60F57CrossOriginalContext_full
#print axioms c60F57CrossOriginalContext_hom_bijective
#print axioms c60F57CrossOriginalContext_roundTrip_map
#print axioms c60F57CrossOriginalContext_threeChart_map
#print axioms c60F57CrossOriginalContext_threeChartNatIso
#print axioms c60F57CrossOriginalContext_roundTripNatIso

end
end KUOS.DependentOriginationGrayC60F55CrossRotationCocycleV5_206
