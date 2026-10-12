import KUOS.DependentOriginationGrayC60F55MixedDescentObstructionV5_204

namespace KUOS.DependentOriginationGrayC60F55MixedCocycleV5_205

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
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60MixedComparisonObstructionV5_196
open KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
open KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204
open KUOS.DependentOriginationGrayC60F55MixedDescentObstructionV5_204
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.205 / F59-F56-A: genuinely typed mixed-source Čech-style cocycle

The v5.204 FULL/FAITHFUL F47 3-Hom transport is now shown to
satisfy strict identity, inversion, and *three-presentation*
composition on all original SOURCE categorical 3-arrows,
not just on full-native Gray values.

Every original F42 face-2-cell witness and original F54
rotation-path witness remains in its OWN separately typed
F47 source frame; the four distinct tagged boundary positions
are preserved. A "third presentation" is an additional
admissible local comparison frame with matched original
F55 routes, NOT a falsely manufactured third polygon
incident to one physical C60 edge (there are only two).

Equations hold in the explicitly specified F47 full-native
kernel 3-Hom quotient. Nonzero north-F55 curvature and the
original nine-generator nonlift of the ADJOINED correction
Delta=(0,1;0) continue to obstruct unqualified physical
global descent.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GeneralThreeLocalFrames
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v₀ w₀ v₁ w₁ v₂ w₂ : IcosahedralDart}
variable {p₀ q₀ : Quiver.Path v₀ w₀}
variable {p₁ q₁ : Quiver.Path v₁ w₁}
variable {p₂ q₂ : Quiver.Path v₂ w₂}
variable {α₀ β₀ : C60F42PresentedFaceCell p₀ q₀}
variable {α₁ β₁ : C60F42PresentedFaceCell p₁ q₁}
variable {α₂ β₂ : C60F42PresentedFaceCell p₂ q₂}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

variable (B₀ : C60F47SquareFrame α₀ β₀ r s)
variable (B₁ : C60F47SquareFrame α₁ β₁ r s)
variable (B₂ : C60F47SquareFrame α₂ β₂ r s)

/-- Identity presentation change fixes EVERY source mixed
3-arrow, with all four original tagged boundaries. -/
theorem c60F56MixedTransport_id_map
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    (c60F48MixedBoundaryTransportFunctor B₀ B₀ rfl rfl).map f = f := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful B₀
    exact c60F48MixedBoundaryTransportFunctor_fullNative
      B₀ B₀ rfl rfl f

/-- Complete two-sided cancellation. A transport from one
original local mixed four-boundary presentation to a second
one and back is the ACTUAL identity on all parallel source
3-Hom arrows, not only on their native Gray evaluations. -/
theorem c60F56MixedTransport_roundTrip_map
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    (c60F48MixedBoundaryTransportFunctor
      B₁ B₀ hface.symm hrotation.symm).map
      ((c60F48MixedBoundaryTransportFunctor
        B₀ B₁ hface hrotation).map f) = f := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful B₀
    calc
      c60F47MixedEval
          ((c60F48MixedBoundaryTransportFunctor
            B₁ B₀ hface.symm hrotation.symm).map
            ((c60F48MixedBoundaryTransportFunctor
              B₀ B₁ hface hrotation).map f)) =
        c60F47MixedEval
          ((c60F48MixedBoundaryTransportFunctor
            B₀ B₁ hface hrotation).map f) :=
        c60F48MixedBoundaryTransportFunctor_fullNative
          B₁ B₀ hface.symm hrotation.symm _
      _ = c60F47MixedEval f :=
        c60F48MixedBoundaryTransportFunctor_fullNative
          B₀ B₁ hface hrotation f

/-- The COMPLETE three-presentation cocycle on actual typed
F47 source-category arrows: direct mixed boundary transport
equals the two-step transport through ANY additional admissible
F47 local frame, provided genuine face/F55 native equality
has been proved at each transition. -/
theorem c60F56MixedTransport_threeFrame_cocycle_map
    (hface₀₁ : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot₀₁ : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    (hface₁₂ : c60F44FaceThreeEval B₁.faceStep =
      c60F44FaceThreeEval B₂.faceStep)
    (hrot₁₂ : c60F44OriginalF55Eval B₁.rotationStep =
      c60F44OriginalF55Eval B₂.rotationStep)
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    (c60F48MixedBoundaryTransportFunctor B₁ B₂ hface₁₂ hrot₁₂).map
      ((c60F48MixedBoundaryTransportFunctor
        B₀ B₁ hface₀₁ hrot₀₁).map f) =
    (c60F48MixedBoundaryTransportFunctor B₀ B₂
      (hface₀₁.trans hface₁₂)
      (hrot₀₁.trans hrot₁₂)).map f := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful B₂
    calc
      c60F47MixedEval
          ((c60F48MixedBoundaryTransportFunctor
            B₁ B₂ hface₁₂ hrot₁₂).map
            ((c60F48MixedBoundaryTransportFunctor
              B₀ B₁ hface₀₁ hrot₀₁).map f)) =
        c60F47MixedEval
          ((c60F48MixedBoundaryTransportFunctor
            B₀ B₁ hface₀₁ hrot₀₁).map f) :=
        c60F48MixedBoundaryTransportFunctor_fullNative
          B₁ B₂ hface₁₂ hrot₁₂ _
      _ = c60F47MixedEval f :=
        c60F48MixedBoundaryTransportFunctor_fullNative
          B₀ B₁ hface₀₁ hrot₀₁ f
      _ = c60F47MixedEval
          ((c60F48MixedBoundaryTransportFunctor B₀ B₂
            (hface₀₁.trans hface₁₂)
            (hrot₀₁.trans hrot₁₂)).map f) :=
        (c60F48MixedBoundaryTransportFunctor_fullNative B₀ B₂
          (hface₀₁.trans hface₁₂)
          (hrot₀₁.trans hrot₁₂) f).symm

/-- Genuine Mathlib natural isomorphism expressing the
three-frame transition cocycle, with object components the
identity isomorphisms of the EXACT FOUR mixed source boundary
slots. Every naturality square is proved from source-category
cocycle equality on all proof-relevant mixed 3-Hom arrows. -/
def c60F56MixedTransport_threeFrameNatIso
    (hface₀₁ : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot₀₁ : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    (hface₁₂ : c60F44FaceThreeEval B₁.faceStep =
      c60F44FaceThreeEval B₂.faceStep)
    (hrot₁₂ : c60F44OriginalF55Eval B₁.rotationStep =
      c60F44OriginalF55Eval B₂.rotationStep) :
    (c60F48MixedBoundaryTransportFunctor
      B₀ B₁ hface₀₁ hrot₀₁) ⋙
      (c60F48MixedBoundaryTransportFunctor
        B₁ B₂ hface₁₂ hrot₁₂) ≅
    c60F48MixedBoundaryTransportFunctor B₀ B₂
      (hface₀₁.trans hface₁₂)
      (hrot₀₁.trans hrot₁₂) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        simp only [Functor.comp_map, Iso.refl_hom,
          Category.comp_id, Category.id_comp]
        exact c60F56MixedTransport_threeFrame_cocycle_map
          B₀ B₁ B₂ hface₀₁ hrot₀₁ hface₁₂ hrot₁₂ f)

/-- Actual roundtrip is a natural isomorphism to the IDENTITY
of the original F47 mixed source category, with no loss of
the proof-relevant F42 face and F54 rotation boundary tags. -/
def c60F56MixedTransport_roundTripNatIso
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep) :
    (c60F48MixedBoundaryTransportFunctor
      B₀ B₁ hface hrotation) ⋙
      (c60F48MixedBoundaryTransportFunctor
        B₁ B₀ hface.symm hrotation.symm) ≅
    𝟭 (C60F47BoundaryPoint B₀) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        simp only [Functor.comp_map, Functor.id_map,
          Iso.refl_hom, Category.comp_id, Category.id_comp]
        exact c60F56MixedTransport_roundTrip_map
          B₀ B₁ hface hrotation f)

end GeneralThreeLocalFrames

section ActualNinetyEdgeCocycle

variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- Physical BOTH-FACE reverse transport cancels the actual
F48 forward functor on every original F47 four-boundary
mixed source 3-Hom, over all NINETY genuine C60 edges. -/
theorem c60F56EveryActualEdgeFaceChange_roundTrip
    (edge : TruncatedIcosahedralEdge)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)}
    (f : X ⟶ Y) :
    (c60F55ActualEdgeFaceChoiceReverseFunctor
      t₁ t₂ left right edge).map
        ((c60F48ActualEdgeFaceChoiceFunctor
          t₁ t₂ left right edge).map f) = f := by
  exact c60F56MixedTransport_roundTrip_map
    (c60F48EveryRealEdgeMixedFrame
      t₁ t₂ left right edge false)
    (c60F48EveryRealEdgeMixedFrame
      t₁ t₂ left right edge true)
    (by rw [c60F48EveryRealEdgeFaceStep_native,
      c60F48EveryRealEdgeFaceStep_native])
    (by rfl) f

#print axioms c60F56MixedTransport_id_map
#print axioms c60F56MixedTransport_roundTrip_map
#print axioms c60F56MixedTransport_threeFrame_cocycle_map
#print axioms c60F56MixedTransport_threeFrameNatIso
#print axioms c60F56MixedTransport_roundTripNatIso
#print axioms c60F56EveryActualEdgeFaceChange_roundTrip

end ActualNinetyEdgeCocycle
end
end KUOS.DependentOriginationGrayC60F55MixedCocycleV5_205
