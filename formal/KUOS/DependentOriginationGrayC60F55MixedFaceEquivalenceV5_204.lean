import KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
import KUOS.DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203

namespace KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204

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
open KUOS.DependentOriginationGrayC60OriginalF43F55MixedBridgeV5_203
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F55-A / v5.204: full mixed-boundary presentation transport

F48 proved one-way FAITHFUL transport between different four-boundary
F47 source categories for the two original incident C60 polygons.
Here we prove the missing FULLNESS and OBJECT BIJECTIVITY, using the
ACTUAL raw F47 mixed constructor presentation and its full-native
Int×Int and ZMod2 kernel. Both directions are genuine source
category functors; not just matched Gray grades.

The physical source F42 polygon path/2-cell terms of each real face
REMAIN DISTINCT. This transport is between the explicitly ADJOINED
F47 four-boundary mixed comparison categories, not an identification
of original unquotiented F42 or F54/F55 terms, and not yet global
geometric descent in the presence of F55 nonzero signed curvature.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GeneralMixedTransport

variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w v' w' : IcosahedralDart}
variable {p q : Quiver.Path v w} {p' q' : Quiver.Path v' w'}
variable {α β : C60F42PresentedFaceCell p q}
variable {α' β' : C60F42PresentedFaceCell p' q'}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

variable (B₀ : C60F47SquareFrame α β r s)
  (B₁ : C60F47SquareFrame α' β' r s)

/-- Every FOUR ORIGINAL boundary tags (the two F42 face slots
and two independently typed F54 rotation slots) has an inverse
image in the other original F47 mixed presentation. -/
theorem c60F55MixedChangePoint_bijective :
    Function.Bijective (c60F48ChangeMixedBoundaryPoint B₀ B₁) := by
  constructor
  · intro X Y h
    cases X <;> cases Y <;>
      simp_all [c60F48ChangeMixedBoundaryPoint]
  · intro Z
    cases Z with
    | faceBefore => exact ⟨.faceBefore, rfl⟩
    | faceAfter => exact ⟨.faceAfter, rfl⟩
    | rotationBefore => exact ⟨.rotationBefore, rfl⟩
    | rotationAfter => exact ⟨.rotationAfter, rfl⟩

/-- Every actual morphism in the OTHER F47 four-boundary source
category has a raw preimage in the first, preserving the same
complete native integer pair and independent exchange phase.
Fullness is proved on all parallel typed boundary pairs, rather
than asserting that original F42 and F54 routes are equal. -/
theorem c60F55MixedTransport_full
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀}
    (g :
      (c60F48MixedBoundaryTransportFunctor B₀ B₁ hface hrotation).obj X ⟶
      (c60F48MixedBoundaryTransportFunctor B₀ B₁ hface hrotation).obj Y) :
    ∃ f : X ⟶ Y,
      (c60F48MixedBoundaryTransportFunctor B₀ B₁ hface hrotation).map f = g := by
  cases X <;> cases Y
  all_goals
    refine Quot.inductionOn g (fun raw => ?_)
    refine ⟨c60F47MixedOf (c60F48ChangeMixedRaw B₁ B₀ raw), ?_⟩
    apply c60F47MixedGrayFunctor_faithful B₁
    change (c60F48ChangeMixedRaw B₀ B₁
      (c60F48ChangeMixedRaw B₁ B₀ raw)).toNative = raw.toNative
    calc
      _ = (c60F48ChangeMixedRaw B₁ B₀ raw).toNative :=
        c60F48ChangeMixedRaw_native B₀ B₁ hface hrotation _
      _ = raw.toNative :=
        c60F48ChangeMixedRaw_native B₁ B₀
          hface.symm hrotation.symm raw

/-- Fullness and the older F48 FAITHFULNESS together mean
bijection on EVERY typed F47 three-Hom, not just the image of
one preferred face/F55 square. The tags remain unchanged. -/
theorem c60F55MixedTransport_hom_bijective
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrotation : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {X Y : C60F47BoundaryPoint B₀} :
    Function.Bijective
      (fun (f : X ⟶ Y) =>
        (c60F48MixedBoundaryTransportFunctor
          B₀ B₁ hface hrotation).map f) := by
  constructor
  · intro f g h
    exact c60F48MixedBoundaryTransportFunctor_faithful
      B₀ B₁ hface hrotation h
  · intro g
    exact c60F55MixedTransport_full B₀ B₁ hface hrotation g

end GeneralMixedTransport

section EveryPhysicalEdge

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

/-- Reverse real-face-choice FUNCTOR: from the genuine second
C60 incident polygon's F47 mixed four-boundary source to the
FIRST, keeping the SAME original F54/F55 route-square 3-cell. -/
def c60F55ActualEdgeFaceChoiceReverseFunctor
    (edge : TruncatedIcosahedralEdge) :
    C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true) ⥤
    C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false) :=
  c60F48MixedBoundaryTransportFunctor
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)
    (by rw [c60F48EveryRealEdgeFaceStep_native,
      c60F48EveryRealEdgeFaceStep_native])
    (by rfl)

/-- The forward physically selected face-choice functor is both
FULL and FAITHFUL and bijective on the FOUR original boundary
POSITIONS. Its domain and codomain original F42 polygon paths
remain differently indexed. -/
theorem c60F55ActualEdgeFaceChoice_isFullyFaithful
    (edge : TruncatedIcosahedralEdge)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)} :
    Function.Bijective
      (fun (f : X ⟶ Y) =>
        (c60F48ActualEdgeFaceChoiceFunctor t₁ t₂ left right edge).map f) := by
  exact c60F55MixedTransport_hom_bijective
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)
    (by rw [c60F48EveryRealEdgeFaceStep_native,
      c60F48EveryRealEdgeFaceStep_native])
    (by rfl)

/-- The reverse physical face-change preserves every raw mixed
comparison and its complete native Gray image. In particular
the actual 2-path/F55 comparison square transports backwards. -/
theorem c60F55ActualEdgeFaceChoiceReverse_square
    (edge : TruncatedIcosahedralEdge) :
    (c60F55ActualEdgeFaceChoiceReverseFunctor
      t₁ t₂ left right edge).map
      (c60F47FaceArrow
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true) ≫
       c60F47CompareAfter
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)) =
      c60F47FaceArrow
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false) ≫
      c60F47CompareAfter
        (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false) := by
  apply Quot.sound
  rfl

/-- The reverse direction also has complete native-faithful
and FULL morphism action on every actual four-boundary hom. -/
theorem c60F55ActualEdgeFaceChoiceReverse_isFullyFaithful
    (edge : TruncatedIcosahedralEdge)
    {X Y : C60F47BoundaryPoint
      (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)} :
    Function.Bijective
      (fun (f : X ⟶ Y) =>
        (c60F55ActualEdgeFaceChoiceReverseFunctor
          t₁ t₂ left right edge).map f) := by
  exact c60F55MixedTransport_hom_bijective
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge true)
    (c60F48EveryRealEdgeMixedFrame t₁ t₂ left right edge false)
    (by rw [c60F48EveryRealEdgeFaceStep_native,
      c60F48EveryRealEdgeFaceStep_native])
    (by rfl)

end EveryPhysicalEdge

#print axioms c60F55MixedChangePoint_bijective
#print axioms c60F55MixedTransport_full
#print axioms c60F55MixedTransport_hom_bijective
#print axioms c60F55ActualEdgeFaceChoiceReverseFunctor
#print axioms c60F55ActualEdgeFaceChoice_isFullyFaithful
#print axioms c60F55ActualEdgeFaceChoiceReverse_square
#print axioms c60F55ActualEdgeFaceChoiceReverse_isFullyFaithful

end
end KUOS.DependentOriginationGrayC60F55MixedFaceEquivalenceV5_204
