import KUOS.DependentOriginationGrayC60F55DirectCompositeContextV5_209

namespace KUOS.DependentOriginationGrayC60F55DirectCompositePhysicalV5_209

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206
open KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207
open KUOS.DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208
open KUOS.DependentOriginationGrayC60F55TwoContextPhysicalV5_208
open KUOS.DependentOriginationGrayC60F55DirectCompositeContextV5_209
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.209 / F59-F60-B: direct right context, actual C60 physical edges

Left and right original F42 path concatenation is not an equality
of two distinct original proof-term syntaxes. The F54 source tree
uses its actual .node constructor, also not erased by rebracketing.
The source comparison is a FOUR-TAG Mathlib NatIso in the explicitly
ADJOINED F47 full-native-kernel 3-Hom quotient, not an unconditional
globally glued raw source Gray-3 category.

All statements below specialize to the genuine 90 C60 physical edges,
their two truly incident polygonal faces and independent loop bases;
old original nine-constructor F55 no-lift persists after the DIRECT
single-composite original context as well as v5.208's nested context.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalRightDirectComposite

variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable (B : C60F47SquareFrame α β r s)

/-- One ORIGINAL F42 suffix concatenation and genuinely original F54
tree node, in contrast to two successive independently typed steps. -/
def c60F60RightDirectFrame
    {u z : IcosahedralDart}
    (suffix : Quiver.Path w u) (outer : Quiver.Path u z)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :=
  c60F47WhiskerRight B (suffix.comp outer)
    (OriginalF45BracketTree.node earlier₂ earlier₁)

/-- Two independent original F42 suffixes and F54 earlier-tree
whiskerings, with the actual intermediate source boundaries. -/
def c60F60RightNestedFrame
    {u z : IcosahedralDart}
    (suffix : Quiver.Path w u) (outer : Quiver.Path u z)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :=
  c60F47WhiskerRight
    (c60F47WhiskerRight B suffix earlier₁) outer earlier₂

/-- Legitimate F47 source four-boundary transport between DIRECT
original F42/F54 composition and the nested two-stage expression:
original F43 and original F55 full Gray images are retained. -/
def c60F60RightDirectToNested
    {u z : IcosahedralDart}
    (suffix : Quiver.Path w u) (outer : Quiver.Path u z)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    C60F47BoundaryPoint
        (c60F60RightDirectFrame B suffix outer earlier₁ earlier₂) ⥤
      C60F47BoundaryPoint
        (c60F60RightNestedFrame B suffix outer earlier₁ earlier₂) :=
  c60F56ContextMixedFunctor
    (c60F60RightDirectFrame B suffix outer earlier₁ earlier₂)
    (c60F60RightNestedFrame B suffix outer earlier₁ earlier₂)
    (by rfl)
    (by
      calc
        c60F44FaceThreeEval
            (c60F60RightDirectFrame B suffix outer earlier₁ earlier₂).faceStep =
          c60F44FaceThreeEval B.faceStep :=
            c60F45RightWhiskerGrayMap (suffix.comp outer) B.faceStep
        _ = c60F44FaceThreeEval
            (c60F47WhiskerRight B suffix earlier₁).faceStep :=
              (c60F45RightWhiskerGrayMap suffix B.faceStep).symm
        _ = c60F44FaceThreeEval
            (c60F60RightNestedFrame B suffix outer earlier₁ earlier₂).faceStep :=
              (c60F45RightWhiskerGrayMap outer
                (c60F47WhiskerRight B suffix earlier₁).faceStep).symm)
    (by
      calc
        c60F44OriginalF55Eval
            (c60F60RightDirectFrame B suffix outer earlier₁ earlier₂).rotationStep =
          c60F44OriginalF55Eval B.rotationStep :=
            c60F45F55RightContextGrayMap
              (OriginalF45BracketTree.node earlier₂ earlier₁) B.rotationStep
        _ = c60F44OriginalF55Eval
            (c60F47WhiskerRight B suffix earlier₁).rotationStep :=
              (c60F45F55RightContextGrayMap earlier₁ B.rotationStep).symm
        _ = c60F44OriginalF55Eval
            (c60F60RightNestedFrame B suffix outer earlier₁ earlier₂).rotationStep :=
              (c60F45F55RightContextGrayMap earlier₂
                (c60F47WhiskerRight B suffix earlier₁).rotationStep).symm)

/-- Dependent four-tag Hom cast from the genuine two-stage
original RIGHT F42/F54 context to the original direct-context
comparison after final F47 presentation transport. -/
def c60F60RightDirectVsNestedHomCast
    {u z : IcosahedralDart}
    (suffix : Quiver.Path w u) (outer : Quiver.Path u z)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc)
    {X Y : C60F47BoundaryPoint B}
    (g :
      ((c60F56OriginalRightMixedContextFunctor B suffix earlier₁) ⋙
        (c60F56OriginalRightMixedContextFunctor
          (c60F47WhiskerRight B suffix earlier₁) outer earlier₂)).obj X ⟶
      ((c60F56OriginalRightMixedContextFunctor B suffix earlier₁) ⋙
        (c60F56OriginalRightMixedContextFunctor
          (c60F47WhiskerRight B suffix earlier₁) outer earlier₂)).obj Y) :
    ((c60F56OriginalRightMixedContextFunctor B (suffix.comp outer)
        (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
      (c60F60RightDirectToNested B suffix outer earlier₁ earlier₂)).obj X ⟶
    ((c60F56OriginalRightMixedContextFunctor B (suffix.comp outer)
        (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
      (c60F60RightDirectToNested B suffix outer earlier₁ earlier₂)).obj Y := by
  cases X <;> cases Y
  all_goals exact g

/-- Both genuine right source contextualizations agree on EVERY F47
source 3-Hom morphism after the justified final mixed source transport. -/
theorem c60F60RightDirectVsNested_map
    {u z : IcosahedralDart}
    (suffix : Quiver.Path w u) (outer : Quiver.Path u z)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc)
    {X Y : C60F47BoundaryPoint B} (f : X ⟶ Y) :
    ((c60F56OriginalRightMixedContextFunctor B (suffix.comp outer)
        (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
      (c60F60RightDirectToNested B suffix outer earlier₁ earlier₂)).map f =
    c60F60RightDirectVsNestedHomCast B suffix outer earlier₁ earlier₂
      (((c60F56OriginalRightMixedContextFunctor B suffix earlier₁) ⋙
        (c60F56OriginalRightMixedContextFunctor
          (c60F47WhiskerRight B suffix earlier₁) outer earlier₂)).map f) := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful
      (c60F60RightNestedFrame B suffix outer earlier₁ earlier₂)
    simp only [Functor.comp_map, c60F60RightDirectToNested,
      c60F56OriginalRightMixedContextFunctor,
      c60F56ContextMixedFunctor_fullNative]

/-- Honest original-right direct-vs-nested Mathlib source natural
isomorphism, without identifying raw F42 two-cells or F54 tree words. -/
def c60F60RightDirectVsNestedNatIso
    {u z : IcosahedralDart}
    (suffix : Quiver.Path w u) (outer : Quiver.Path u z)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    (c60F56OriginalRightMixedContextFunctor B (suffix.comp outer)
        (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
      (c60F60RightDirectToNested B suffix outer earlier₁ earlier₂) ≅
    (c60F56OriginalRightMixedContextFunctor B suffix earlier₁) ⋙
      (c60F56OriginalRightMixedContextFunctor
        (c60F47WhiskerRight B suffix earlier₁) outer earlier₂) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        calc
          _ = ((c60F56OriginalRightMixedContextFunctor B
                (suffix.comp outer)
                (OriginalF45BracketTree.node earlier₂ earlier₁)) ⋙
              (c60F60RightDirectToNested B suffix outer earlier₁ earlier₂)).map f :=
                Category.comp_id _
          _ = c60F60RightDirectVsNestedHomCast B suffix outer earlier₁ earlier₂
              (((c60F56OriginalRightMixedContextFunctor B suffix earlier₁) ⋙
                (c60F56OriginalRightMixedContextFunctor
                  (c60F47WhiskerRight B suffix earlier₁) outer earlier₂)).map f) :=
                c60F60RightDirectVsNested_map B suffix outer earlier₁ earlier₂ f
          _ = _ := (Category.id_comp _).symm)

end OriginalRightDirectComposite

section ActualPhysicalDirectComposite

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

/-- A source-level direct-vs-two-step LEFT NatIso for EACH genuine
C60 physical edge and EACH one of its two incident polygonal faces. -/
def c60F60PhysicalLeftDirectVsNestedNatIso
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {u z : IcosahedralDart}
    (prior : Quiver.Path u (c60F58OriginalPhysicalFaceBase edge side))
    (outer : Quiver.Path z u)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ p₂ q₂ mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :=
  c60F60LeftDirectVsNestedNatIso
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
    prior outer later₁ later₂

/-- A source-level direct-vs-two-step RIGHT NatIso for EACH actual
physical edge and its true original adjacent polygon base dart. -/
def c60F60PhysicalRightDirectVsNestedNatIso
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {u z : IcosahedralDart}
    (suffix : Quiver.Path (c60F58OriginalPhysicalFaceBase edge side) u)
    (outer : Quiver.Path u z)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc p₀ q₀)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :=
  c60F60RightDirectVsNestedNatIso
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
    suffix outer earlier₁ earlier₂

/-- At all ninety C60 physical edges and BOTH originally distinct
adjacent polygon faces, no direct original F42-path-concatenated and
F54-bracket-node context can lift ADJOINED Delta into OLD F55. -/
theorem c60F60PhysicalLeftDirect_noOriginalF55Delta
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {u z : IcosahedralDart}
    (prior : Quiver.Path u (c60F58OriginalPhysicalFaceBase edge side))
    (outer : Quiver.Path z u)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ p₂ q₂ mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55LeftContextFunctor
        (OriginalF45BracketTree.node later₁ later₂)).obj
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right))
      ((c60F45F55LeftContextFunctor
        (OriginalF45BracketTree.node later₁ later₂)).obj
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)),
      c60F44FaceThreeEval
        (c60F60LeftDirectFrame
          (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
          prior outer later₁ later₂).faceStep +
        c60F55SourceNative cell =
      c60F44OriginalF55Eval
        (c60F60LeftDirectFrame
          (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
          prior outer later₁ later₂).rotationStep :=
  c60F57OriginalLeftContext_noOriginalF55Lift
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
    (outer.comp prior) (OriginalF45BracketTree.node later₁ later₂)

/-- The SAME old-nine F55 obstruction holds under original RIGHT
single-composite suffix path and original directly composed F54 trees. -/
theorem c60F60PhysicalRightDirect_noOriginalF55Delta
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {u z : IcosahedralDart}
    (suffix : Quiver.Path (c60F58OriginalPhysicalFaceBase edge side) u)
    (outer : Quiver.Path u z)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc p₀ q₀)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55RightContextFunctor
        (OriginalF45BracketTree.node earlier₂ earlier₁)).obj
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right))
      ((c60F45F55RightContextFunctor
        (OriginalF45BracketTree.node earlier₂ earlier₁)).obj
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)),
      c60F44FaceThreeEval
        (c60F60RightDirectFrame
          (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
          suffix outer earlier₁ earlier₂).faceStep +
        c60F55SourceNative cell =
      c60F44OriginalF55Eval
        (c60F60RightDirectFrame
          (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
          suffix outer earlier₁ earlier₂).rotationStep :=
  c60F57OriginalRightContext_noOriginalF55Lift
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
    (suffix.comp outer) (OriginalF45BracketTree.node earlier₂ earlier₁)

end ActualPhysicalDirectComposite

#print axioms c60F60RightDirectFrame
#print axioms c60F60RightNestedFrame
#print axioms c60F60RightDirectToNested
#print axioms c60F60RightDirectVsNestedHomCast
#print axioms c60F60RightDirectVsNested_map
#print axioms c60F60RightDirectVsNestedNatIso
#print axioms c60F60PhysicalLeftDirectVsNestedNatIso
#print axioms c60F60PhysicalRightDirectVsNestedNatIso
#print axioms c60F60PhysicalLeftDirect_noOriginalF55Delta
#print axioms c60F60PhysicalRightDirect_noOriginalF55Delta

end
end KUOS.DependentOriginationGrayC60F55DirectCompositePhysicalV5_209
