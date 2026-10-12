import KUOS.DependentOriginationGrayC60F55TwoContextPhysicalV5_208
import KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200

namespace KUOS.DependentOriginationGrayC60F55DirectCompositeContextV5_209

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208
open KUOS.DependentOriginationGrayC60F55TwoContextPhysicalV5_208
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.209 / F59-F60-A: direct ORIGINAL F42 path and F54 tree compositions

Unlike v5.208, compare a genuinely DIRECT source construction with
two sequential source contexts. The old F42 paths are concatenated
by Quiver.Path.comp (with explicit comp_assoc reindexing). The old
F54/F55 contexts are combined as an ACTUAL original binary .node,
rather than identified with a distinct raw bracket-tree word.
The old exact-depth F44 reassociation theorem supplies the explicit
two Nat.add_assoc transports.

Original F42 face 2-cell terms and F54 route terms are NOT equated
across distinct raw presentations. Instead the direct and nested
presentations are compared in the source F47 full-native-kernel
mixed four-boundary 3-Hom category, retaining full Gray charge/phase.
-/

/-! ## I. Genuine F42 original source paths and F54 rebracketing -/

/-- Direct original F42 path concatenation, then explicit dependent
reindexing to the endpoints of TWO left original path whiskerings.
The result is still a proof-relevant original F42 source 2-cell. -/
def c60F60LeftDirectPathFace
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path c d}
    (prior : Quiver.Path b c) (outer : Quiver.Path a b)
    (α : C60F42PresentedFaceCell p q) :
    C60F42PresentedFaceCell
      (outer.comp (prior.comp p)) (outer.comp (prior.comp q)) :=
  c60F52ReindexFace
    (Quiver.Path.comp_assoc outer prior p)
    (Quiver.Path.comp_assoc outer prior q)
    ((c60F45LeftWhiskerFunctor (outer.comp prior)).obj α)

/-- The direct-composite original F42 witness and the nested original
F42 witness have the same original face degree; this theorem does NOT
identify the two raw original 2-cell proof terms. -/
theorem c60F60LeftDirectPathFace_degree
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path c d}
    (prior : Quiver.Path b c) (outer : Quiver.Path a b)
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree (c60F60LeftDirectPathFace prior outer α) =
    c60F43FaceDegree
      ((c60F45LeftWhiskerFunctor outer).obj
        ((c60F45LeftWhiskerFunctor prior).obj α)) := by
  simp only [c60F60LeftDirectPathFace,
    c60F52ReindexFace_degree, c60F45LeftWhiskerFaceDegree]

/-- The opposite genuine ORIGINAL F42 suffix composition. Direct
right whiskering has different path parentheses, so we use BOTH
exact opposite-direction comp_assoc casts rather than conflating. -/
def c60F60RightDirectPathFace
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c) (outer : Quiver.Path c d)
    (α : C60F42PresentedFaceCell p q) :
    C60F42PresentedFaceCell
      ((p.comp suffix).comp outer) ((q.comp suffix).comp outer) :=
  c60F52ReindexFace
    (Quiver.Path.comp_assoc p suffix outer).symm
    (Quiver.Path.comp_assoc q suffix outer).symm
    ((c60F45RightWhiskerFunctor (suffix.comp outer)).obj α)

theorem c60F60RightDirectPathFace_degree
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c) (outer : Quiver.Path c d)
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree (c60F60RightDirectPathFace suffix outer α) =
    c60F43FaceDegree
      ((c60F45RightWhiskerFunctor outer).obj
        ((c60F45RightWhiskerFunctor suffix).obj α)) := by
  simp only [c60F60RightDirectPathFace,
    c60F52ReindexFace_degree, c60F45RightWhiskerFaceDegree]

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Directly regrouping three ORIGINAL F54/F55 bracket trees changes
TWO exact natural-number depth indices. The F44 source exchange class
agrees after both casts, not by asserting raw tree-term equality. -/
theorem c60F60OriginalF54ThreeTreeReassociation
    {a b : D} {x y : E}
    {n₀ n₁ n₂ m₀ m₁ m₂ : Nat}
    {ma mb mc md : Blocks a b} {pa pb pc pd : Blocks x y}
    (first : OriginalF45BracketTree n₀ m₀ ma pa mb pb)
    (second : OriginalF45BracketTree n₁ m₁ mb pb mc pc)
    (third : OriginalF45BracketTree n₂ m₂ mc pc md pd) :
    (OriginalF45BracketTree.castDepths
      (Nat.add_assoc n₀ n₁ n₂) (Nat.add_assoc m₀ m₁ m₂)
      (OriginalF45BracketTree.node
        (OriginalF45BracketTree.node first second) third)).toExchangeClass =
    (OriginalF45BracketTree.node first
      (OriginalF45BracketTree.node second third)).toExchangeClass :=
  OriginalF45BracketTree.reassociate first second third

/-! ## II. LEFT: direct original composite vs genuine two-stage source -/

section OriginalLeftDirectComposite
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable (B : C60F47SquareFrame α β r s)

/-- Actual DIRECT original F42 concatenated path and ORIGINAL F54
binary node as a single new contextual source F47 square. -/
def c60F60LeftDirectFrame
    {u z : IcosahedralDart}
    (prior : Quiver.Path u v) (outer : Quiver.Path z u)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :=
  c60F47WhiskerLeft B (outer.comp prior)
    (OriginalF45BracketTree.node later₁ later₂)

/-- The other presentation retains BOTH nested original context
constructors and their independently typed intermediate F54 trees. -/
def c60F60LeftNestedFrame
    {u z : IcosahedralDart}
    (prior : Quiver.Path u v) (outer : Quiver.Path z u)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :=
  c60F47WhiskerLeft (c60F47WhiskerLeft B prior later₁) outer later₂

/-- The direct original source F42/F54 construction and nested source
construction have a genuine FULL native F47 transport, with all four
mixed boundary tags retained. No source F42 or F54 raw word is equated. -/
def c60F60LeftDirectToNested
    {u z : IcosahedralDart}
    (prior : Quiver.Path u v) (outer : Quiver.Path z u)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :
    C60F47BoundaryPoint (c60F60LeftDirectFrame B prior outer later₁ later₂) ⥤
      C60F47BoundaryPoint (c60F60LeftNestedFrame B prior outer later₁ later₂) :=
  c60F56ContextMixedFunctor
    (c60F60LeftDirectFrame B prior outer later₁ later₂)
    (c60F60LeftNestedFrame B prior outer later₁ later₂)
    (by rfl)
    (by
      calc
        c60F44FaceThreeEval
            (c60F60LeftDirectFrame B prior outer later₁ later₂).faceStep =
          c60F44FaceThreeEval B.faceStep :=
            c60F45LeftWhiskerGrayMap (outer.comp prior) B.faceStep
        _ = c60F44FaceThreeEval
            (c60F47WhiskerLeft B prior later₁).faceStep :=
              (c60F45LeftWhiskerGrayMap prior B.faceStep).symm
        _ = c60F44FaceThreeEval
            (c60F60LeftNestedFrame B prior outer later₁ later₂).faceStep :=
              (c60F45LeftWhiskerGrayMap outer
                (c60F47WhiskerLeft B prior later₁).faceStep).symm)
    (by
      calc
        c60F44OriginalF55Eval
            (c60F60LeftDirectFrame B prior outer later₁ later₂).rotationStep =
          c60F44OriginalF55Eval B.rotationStep :=
            c60F45F55LeftContextGrayMap
              (OriginalF45BracketTree.node later₁ later₂) B.rotationStep
        _ = c60F44OriginalF55Eval
            (c60F47WhiskerLeft B prior later₁).rotationStep :=
              (c60F45F55LeftContextGrayMap later₁ B.rotationStep).symm
        _ = c60F44OriginalF55Eval
            (c60F60LeftNestedFrame B prior outer later₁ later₂).rotationStep :=
              (c60F45F55LeftContextGrayMap later₂
                (c60F47WhiskerLeft B prior later₁).rotationStep).symm)

/-- The actual direct original one-step F42 path and F54 tree route
and the original two successive whiskerings produce SAME F47 source
3-Hom morphisms after the only justified final typed transport. -/
theorem c60F60LeftDirectVsNested_map
    {u z : IcosahedralDart}
    (prior : Quiver.Path u v) (outer : Quiver.Path z u)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd)
    {X Y : C60F47BoundaryPoint B} (f : X ⟶ Y) :
    ((c60F56OriginalLeftMixedContextFunctor B (outer.comp prior)
        (OriginalF45BracketTree.node later₁ later₂)) ⋙
      (c60F60LeftDirectToNested B prior outer later₁ later₂)).map f =
    ((c60F56OriginalLeftMixedContextFunctor B prior later₁) ⋙
      (c60F56OriginalLeftMixedContextFunctor
        (c60F47WhiskerLeft B prior later₁) outer later₂)).map f := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful
      (c60F60LeftNestedFrame B prior outer later₁ later₂)
    simp only [Functor.comp_map, c60F60LeftDirectToNested,
      c60F56OriginalLeftMixedContextFunctor,
      c60F56ContextMixedFunctor_fullNative]

/-- Mathlib source-level natural isomorphism identifying the direct
ORIGINAL F42 path-concatenated/F54 tree-node route with the earlier
proved two-stage contextual transport, after genuinely typed final
F47 mixed-source comparison, on all four original boundary tags. -/
def c60F60LeftDirectVsNestedNatIso
    {u z : IcosahedralDart}
    (prior : Quiver.Path u v) (outer : Quiver.Path z u)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ mb pb mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :
    (c60F56OriginalLeftMixedContextFunctor B (outer.comp prior)
        (OriginalF45BracketTree.node later₁ later₂)) ⋙
      (c60F60LeftDirectToNested B prior outer later₁ later₂) ≅
    (c60F56OriginalLeftMixedContextFunctor B prior later₁) ⋙
      (c60F56OriginalLeftMixedContextFunctor
        (c60F47WhiskerLeft B prior later₁) outer later₂) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        calc
          _ = ((c60F56OriginalLeftMixedContextFunctor B
                (outer.comp prior)
                (OriginalF45BracketTree.node later₁ later₂)) ⋙
              (c60F60LeftDirectToNested B prior outer later₁ later₂)).map f :=
                Category.comp_id _
          _ = ((c60F56OriginalLeftMixedContextFunctor B prior later₁) ⋙
              (c60F56OriginalLeftMixedContextFunctor
                (c60F47WhiskerLeft B prior later₁) outer later₂)).map f :=
                c60F60LeftDirectVsNested_map B prior outer later₁ later₂ f
          _ = _ := (Category.id_comp _).symm)

end OriginalLeftDirectComposite

#print axioms c60F60LeftDirectPathFace
#print axioms c60F60LeftDirectPathFace_degree
#print axioms c60F60RightDirectPathFace
#print axioms c60F60RightDirectPathFace_degree
#print axioms c60F60OriginalF54ThreeTreeReassociation
#print axioms c60F60LeftDirectFrame
#print axioms c60F60LeftNestedFrame
#print axioms c60F60LeftDirectToNested
#print axioms c60F60LeftDirectVsNested_map
#print axioms c60F60LeftDirectVsNestedNatIso

end
end KUOS.DependentOriginationGrayC60F55DirectCompositeContextV5_209
