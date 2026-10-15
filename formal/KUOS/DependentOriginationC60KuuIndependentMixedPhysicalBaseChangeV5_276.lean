import KUOS.DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275
import KUOS.DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207

namespace KUOS.DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206
open KUOS.DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.276 / F112 fourth stage — actual physical source mixed base change

F112/v5.275 produces a genuine ORIGINAL F42/F54/F55 four-boundary
F47 mixed source frame for any two independently chosen odd-degree
polygon face cells at the actual two DIFFERENT physical face sites
adjacent to an original C60 edge.

Here the two source presentations may use DIFFERENT genuine C60
path contexts and DIFFERENT original F42 face witnesses.
Their physical edges are required to be the SAME actual physical edge:
this is an explicit geometrical incidence check, not a fabricated
canonical comparison between unrelated physical patches.

Prove the previously CONDITIONAL F56/F58 full-native comparisons
on ACTUAL INDEPENDENT F42 source face pairs:
  1. Both original F43/F44 face native images agree by the
     proved odd/odd F112 exchange, and both original F54/F55
     square images agree on the very same physical edge.
  2. Obtain an actual original-boundary-typed F47 Mathlib
     source functor between independent face presentations,
     faithful on all source 3-Homs and preserving EVERY native
     Int×Int charge and independent ZMod 2 phase.
  3. The change functors obey arbitrary triple-comparison
     Čech cocycle coherence on ALL F47 source Homs, not just
     equality of observer charges or one chosen mixed arrow.
  4. For TWO independently typed ORIGINAL C60 prior/suffix
     paths and the old independent F54/F55 bracket contexts,
     obtain actual LEFT/RIGHT F58 Beck–Chevalley natural
     isomorphisms between the distinct original F47 sources.
  5. Their transported mixed source squares still commute,
     but NO old original F55 nine-constructor cell can
     replace the required adjoined mixed comparison, including
     after these correctly typed original source contexts.
  6. Specialize to any three independent odd-degree original
     face labels on each of the ninety actual physical edges.

BOUNDARY: This transports between presentations of the SAME
actual C60 physical edge, not automatically between two
different physical edges on an overlap. It is not a topology
or globally effective original F42/F54/F55 three-descent.
Original F110 phase loss and F68 north signed charge -5 remain.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section IndependentPhysicalOriginalContexts
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

/-- A named actual full ORIGINAL F47 frame makes path- and
rotation-dependent types explicit in all the following comparisons. -/
abbrev c60F112MixedPhysicalFrame {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n)
    (P : C60F112IndependentOddFacePair C i) :=
  c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P

/-- For ANY two genuinely source-typed odd F42 site pairs, the
F43/F44 original face exchange has the SAME complete original
Gray image. Not just their F77 quotient images: exchange phase
remains ONE before any physical source change functor. -/
theorem c60F112MixedPhysicalFace_native_eq {n : Nat}
    (C₀ C₁ : C60F108BothFaceContexts n) (i : Fin n)
    (P₀ : C60F112IndependentOddFacePair C₀ i)
    (P₁ : C60F112IndependentOddFacePair C₁ i) :
    c60F44FaceThreeEval
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀).faceStep =
    c60F44FaceThreeEval
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁).faceStep := by
  calc
    _ = c60F51Eval (c60F112IndependentPairExchangeHom C₀ i P₀) :=
      c60F112IndependentFaceMixedFrame_face_native
        t₁ t₂ left right C₀ i P₀
    _ = (c60F77PhaseGenerator GrayGrade.unit :
          GrayGrade.unit ⟶ GrayGrade.unit) :=
      c60F112IndependentPair_nativePhaseGenerator C₀ i P₀
    _ = c60F51Eval (c60F112IndependentPairExchangeHom C₁ i P₁) :=
      (c60F112IndependentPair_nativePhaseGenerator C₁ i P₁).symm
    _ = _ :=
      (c60F112IndependentFaceMixedFrame_face_native
        t₁ t₂ left right C₁ i P₁).symm

/-- The actual original F54/F55 rotation square on one TRUE
physical C60 edge is the same original source arrow, regardless
of the two independent F42 chosen face paths. -/
theorem c60F112MixedPhysicalRotation_native_eq {n : Nat}
    (C₀ C₁ : C60F108BothFaceContexts n) (i : Fin n)
    (P₀ : C60F112IndependentOddFacePair C₀ i)
    (P₁ : C60F112IndependentOddFacePair C₁ i)
    (hedge : C₀.edge i = C₁.edge i) :
    c60F44OriginalF55Eval
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀).rotationStep =
    c60F44OriginalF55Eval
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁).rotationStep := by
  change c60F44OriginalF55Eval
      (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right (C₀.edge i)) =
    c60F44OriginalF55Eval
      (c60F46PhysicalFlagOriginalF55Arrow t₁ t₂ left right (C₁.edge i))
  rw [hedge]

/-- An ACTUAL full original F47 source change, induced by TWO
independent original F42 face-site pairs and separately typed
genuine original C60 paths. All F56 requirements are now proved
from actual physical source cells, not supplied compatibility. -/
def c60F112MixedPhysicalSourceChange {n : Nat}
    (C₀ C₁ : C60F108BothFaceContexts n) (i : Fin n)
    (P₀ : C60F112IndependentOddFacePair C₀ i)
    (P₁ : C60F112IndependentOddFacePair C₁ i)
    (hedge : C₀.edge i = C₁.edge i) :
    C60F47BoundaryPoint
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀) ⥤
    C60F47BoundaryPoint
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁) :=
  c60F56ContextMixedFunctor
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁)
    (by
      change C₀.edge i = C₁.edge i
      exact hedge)
    (c60F112MixedPhysicalFace_native_eq t₁ t₂ left right C₀ C₁ i P₀ P₁)
    (c60F112MixedPhysicalRotation_native_eq
      t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge)

/-- Source change preserves all full native F47 mixed arrows:
both independent integer charges AND the original nonzero
exchange phase, even when chosen F42 paths are different. -/
theorem c60F112MixedPhysicalSourceChange_native {n : Nat}
    (C₀ C₁ : C60F108BothFaceContexts n) (i : Fin n)
    (P₀ : C60F112IndependentOddFacePair C₀ i)
    (P₁ : C60F112IndependentOddFacePair C₁ i)
    (hedge : C₀.edge i = C₁.edge i)
    {X Y : C60F47BoundaryPoint
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)}
    (f : X ⟶ Y) :
    c60F47MixedEval
      ((c60F112MixedPhysicalSourceChange
        t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge).map f) =
      c60F47MixedEval f :=
  c60F56ContextMixedFunctor_fullNative
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁)
    (by change C₀.edge i = C₁.edge i; exact hedge)
    (c60F112MixedPhysicalFace_native_eq t₁ t₂ left right C₀ C₁ i P₀ P₁)
    (c60F112MixedPhysicalRotation_native_eq
      t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge) f

/-- Faithful on ALL original F47 3-Homs, rather than only the
canonical mixed comparison square. -/
theorem c60F112MixedPhysicalSourceChange_faithful {n : Nat}
    (C₀ C₁ : C60F108BothFaceContexts n) (i : Fin n)
    (P₀ : C60F112IndependentOddFacePair C₀ i)
    (P₁ : C60F112IndependentOddFacePair C₁ i)
    (hedge : C₀.edge i = C₁.edge i)
    {X Y : C60F47BoundaryPoint
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)}
    {f g : X ⟶ Y}
    (h : (c60F112MixedPhysicalSourceChange
      t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge).map f =
      (c60F112MixedPhysicalSourceChange
        t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge).map g) : f = g := by
  apply c60F47MixedGrayFunctor_faithful
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
  have hh := congrArg (fun z => c60F47MixedEval z) h
  change c60F47MixedEval
      ((c60F112MixedPhysicalSourceChange
        t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge).map f) =
    c60F47MixedEval
      ((c60F112MixedPhysicalSourceChange
        t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge).map g) at hh
  rw [c60F112MixedPhysicalSourceChange_native,
    c60F112MixedPhysicalSourceChange_native] at hh
  exact hh

/-- The original four-boundary F47 mixed square is transported
as a SOURCE CATEGORY arrow. Native comparison after transport
is not presented as equality of unrelated raw F42 witnesses. -/
theorem c60F112MixedPhysicalSourceChange_square {n : Nat}
    (C₀ C₁ : C60F108BothFaceContexts n) (i : Fin n)
    (P₀ : C60F112IndependentOddFacePair C₀ i)
    (P₁ : C60F112IndependentOddFacePair C₁ i)
    (hedge : C₀.edge i = C₁.edge i) :
    (c60F112MixedPhysicalSourceChange
      t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge).map
      (c60F47FaceArrow
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀) ≫
       c60F47CompareAfter
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)) =
      c60F47FaceArrow
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁) ≫
      c60F47CompareAfter
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁) :=
  c60F56ContextMixedFunctor_square
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁)
    (by change C₀.edge i = C₁.edge i; exact hedge)
    (c60F112MixedPhysicalFace_native_eq t₁ t₂ left right C₀ C₁ i P₀ P₁)
    (c60F112MixedPhysicalRotation_native_eq
      t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge)

/-- An actual THREE-PRESENTATION Čech cocycle at one real
physical C60 edge: any two successive independent raw F42
source changes act like direct source change ON EVERY F47 HOM,
not merely on the charge-only F77 observer. -/
theorem c60F112MixedPhysicalThreeChanges_cocycle {n : Nat}
    (C₀ C₁ C₂ : C60F108BothFaceContexts n) (i : Fin n)
    (P₀ : C60F112IndependentOddFacePair C₀ i)
    (P₁ : C60F112IndependentOddFacePair C₁ i)
    (P₂ : C60F112IndependentOddFacePair C₂ i)
    (h₀₁ : C₀.edge i = C₁.edge i)
    (h₁₂ : C₁.edge i = C₂.edge i)
    {X Y : C60F47BoundaryPoint
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)}
    (f : X ⟶ Y) :
    ((c60F112MixedPhysicalSourceChange
      t₁ t₂ left right C₀ C₁ i P₀ P₁ h₀₁) ⋙
      (c60F112MixedPhysicalSourceChange
        t₁ t₂ left right C₁ C₂ i P₁ P₂ h₁₂)).map f =
    (c60F112MixedPhysicalSourceChange
      t₁ t₂ left right C₀ C₂ i P₀ P₂ (h₀₁.trans h₁₂)).map f := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₂ i P₂)
    change c60F47MixedEval
        ((c60F112MixedPhysicalSourceChange
          t₁ t₂ left right C₁ C₂ i P₁ P₂ h₁₂).map
          ((c60F112MixedPhysicalSourceChange
            t₁ t₂ left right C₀ C₁ i P₀ P₁ h₀₁).map f)) =
      c60F47MixedEval
        ((c60F112MixedPhysicalSourceChange
          t₁ t₂ left right C₀ C₂ i P₀ P₂ (h₀₁.trans h₁₂)).map f)
    rw [c60F112MixedPhysicalSourceChange_native,
      c60F112MixedPhysicalSourceChange_native,
      c60F112MixedPhysicalSourceChange_native]

/-! ## Source-level Beck–Chevalley with genuinely distinct C60 contexts -/

/-- LEFT Beck–Chevalley NATURAL ISO after two genuinely
independent original C60 physical paths, with an old
independent F54 later bracket tree. This is a source-level
NatIso for ACTUAL odd F42 cells and TRUE physical F55 square. -/
def c60F112MixedPhysicalLeftBeckChevalley {n : Nat}
    (C₀ C₁ : C60F108BothFaceContexts n) (i : Fin n)
    (P₀ : C60F112IndependentOddFacePair C₀ i)
    (P₁ : C60F112IndependentOddFacePair C₁ i)
    (hedge : C₀.edge i = C₁.edge i)
    {u₀ u₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ (truncatedIcosahedralEdgeEndpoints (C₀.edge i)).1)
    (prior₁ : Quiver.Path u₁ (truncatedIcosahedralEdgeEndpoints (C₁.edge i)).1)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l p₂ q₂ mc pc) :
    (c60F56OriginalLeftMixedContextFunctor
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
      prior₀ later) ⋙
      (c60F58LeftAfterFaceChoice
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁)
        (by change C₀.edge i = C₁.edge i; exact hedge)
        (c60F112MixedPhysicalFace_native_eq
          t₁ t₂ left right C₀ C₁ i P₀ P₁)
        (c60F112MixedPhysicalRotation_native_eq
          t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge)
        prior₀ prior₁ later) ≅
    (c60F112MixedPhysicalSourceChange
      t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge) ⋙
      (c60F56OriginalLeftMixedContextFunctor
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁)
        prior₁ later) :=
  c60F58LeftFaceContext_NatIso
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁)
    (by change C₀.edge i = C₁.edge i; exact hedge)
    (c60F112MixedPhysicalFace_native_eq t₁ t₂ left right C₀ C₁ i P₀ P₁)
    (c60F112MixedPhysicalRotation_native_eq
      t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge)
    prior₀ prior₁ later

/-- RIGHT Beck–Chevalley NATURAL ISO after two genuinely
independent physical suffix paths and an ORIGINAL F54 earlier
bracket tree. No raw original F42/F54 endpoints are equalized. -/
def c60F112MixedPhysicalRightBeckChevalley {n : Nat}
    (C₀ C₁ : C60F108BothFaceContexts n) (i : Fin n)
    (P₀ : C60F112IndependentOddFacePair C₀ i)
    (P₁ : C60F112IndependentOddFacePair C₁ i)
    (hedge : C₀.edge i = C₁.edge i)
    {u₀ u₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path
      (truncatedIcosahedralEdgeEndpoints (C₀.edge i)).2 u₀)
    (suffix₁ : Quiver.Path
      (truncatedIcosahedralEdgeEndpoints (C₁.edge i)).2 u₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc p₀ q₀) :
    (c60F56OriginalRightMixedContextFunctor
      (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
      suffix₀ earlier) ⋙
      (c60F58RightAfterFaceChoice
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁)
        (by change C₀.edge i = C₁.edge i; exact hedge)
        (c60F112MixedPhysicalFace_native_eq
          t₁ t₂ left right C₀ C₁ i P₀ P₁)
        (c60F112MixedPhysicalRotation_native_eq
          t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge)
        suffix₀ suffix₁ earlier) ≅
    (c60F112MixedPhysicalSourceChange
      t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge) ⋙
      (c60F56OriginalRightMixedContextFunctor
        (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁)
        suffix₁ earlier) :=
  c60F58RightFaceContext_NatIso
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₀ i P₀)
    (c60F112MixedPhysicalFrame t₁ t₂ left right C₁ i P₁)
    (by change C₀.edge i = C₁.edge i; exact hedge)
    (c60F112MixedPhysicalFace_native_eq t₁ t₂ left right C₀ C₁ i P₀ P₁)
    (c60F112MixedPhysicalRotation_native_eq
      t₁ t₂ left right C₀ C₁ i P₀ P₁ hedge)
    suffix₀ suffix₁ earlier

/-- The original nine-generator F55 NO-LIFT obstruction persists
after the real C60 LEFT path and independently typed original
F54 tree context for an arbitrary independent odd F42 pair. -/
theorem c60F112MixedPhysicalLeft_noOriginalF55Lift {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n)
    (P : C60F112IndependentOddFacePair C i)
    {u : IcosahedralDart}
    (prior : Quiver.Path u (truncatedIcosahedralEdgeEndpoints (C.edge i)).1)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l p₂ q₂ mc pc) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        ((c60F45F55LeftContextFunctor later).obj
          (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right))
        ((c60F45F55LeftContextFunctor later).obj
          (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)),
      c60F44FaceThreeEval
        (c60F47WhiskerLeft
          (c60F112MixedPhysicalFrame t₁ t₂ left right C i P)
          prior later).faceStep +
        c60F55SourceNative cell =
      c60F44OriginalF55Eval
        (c60F47WhiskerLeft
          (c60F112MixedPhysicalFrame t₁ t₂ left right C i P)
          prior later).rotationStep :=
  c60F57OriginalLeftContext_noOriginalF55Lift
    (c60F112MixedPhysicalFrame t₁ t₂ left right C i P)
    prior later

/-- Same exact original F55 no-lift after a real physical
RIGHT suffix and independent original F54 earlier tree. -/
theorem c60F112MixedPhysicalRight_noOriginalF55Lift {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n)
    (P : C60F112IndependentOddFacePair C i)
    {u : IcosahedralDart}
    (suffix : Quiver.Path (truncatedIcosahedralEdgeEndpoints (C.edge i)).2 u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc p₀ q₀) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        ((c60F45F55RightContextFunctor earlier).obj
          (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right))
        ((c60F45F55RightContextFunctor earlier).obj
          (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)),
      c60F44FaceThreeEval
        (c60F47WhiskerRight
          (c60F112MixedPhysicalFrame t₁ t₂ left right C i P)
          suffix earlier).faceStep +
        c60F55SourceNative cell =
      c60F44OriginalF55Eval
        (c60F47WhiskerRight
          (c60F112MixedPhysicalFrame t₁ t₂ left right C i P)
          suffix earlier).rotationStep :=
  c60F57OriginalRightContext_noOriginalF55Lift
    (c60F112MixedPhysicalFrame t₁ t₂ left right C i P)
    suffix earlier

/-! ## Canonical genuine ninety-edge source family -/

/-- All 90 actual C60 edges admit independent raw F42-label
changes whose F47 source functors preserve full charge/phase. -/
def c60F112AllNinetyMixedPhysicalChange
    (i : Fin (Fintype.card TruncatedIcosahedralEdge))
    (P₀ P₁ : C60F112IndependentOddFacePair
      c60F108AllNinetyBothFaces i) :
    C60F47BoundaryPoint
      (c60F112MixedPhysicalFrame t₁ t₂ left right
        c60F108AllNinetyBothFaces i P₀) ⥤
    C60F47BoundaryPoint
      (c60F112MixedPhysicalFrame t₁ t₂ left right
        c60F108AllNinetyBothFaces i P₁) :=
  c60F112MixedPhysicalSourceChange
    t₁ t₂ left right
    c60F108AllNinetyBothFaces c60F108AllNinetyBothFaces
    i P₀ P₁ rfl

/-- True all-ninety three-choice higher coherence for ALL
mixed F47 Homs, including original F43, original F55 and
the NEW compare-before/after arrows; never quotient to F77. -/
theorem c60F112AllNinetyMixedPhysicalCech_cocycle
    (i : Fin (Fintype.card TruncatedIcosahedralEdge))
    (P₀ P₁ P₂ : C60F112IndependentOddFacePair
      c60F108AllNinetyBothFaces i)
    {X Y : C60F47BoundaryPoint
      (c60F112MixedPhysicalFrame t₁ t₂ left right
        c60F108AllNinetyBothFaces i P₀)}
    (f : X ⟶ Y) :
    ((c60F112AllNinetyMixedPhysicalChange
      t₁ t₂ left right i P₀ P₁) ⋙
      (c60F112AllNinetyMixedPhysicalChange
        t₁ t₂ left right i P₁ P₂)).map f =
    (c60F112AllNinetyMixedPhysicalChange
      t₁ t₂ left right i P₀ P₂).map f :=
  c60F112MixedPhysicalThreeChanges_cocycle
    t₁ t₂ left right
    c60F108AllNinetyBothFaces c60F108AllNinetyBothFaces
    c60F108AllNinetyBothFaces
    i P₀ P₁ P₂ rfl rfl f

#print axioms c60F112MixedPhysicalFace_native_eq
#print axioms c60F112MixedPhysicalRotation_native_eq
#print axioms c60F112MixedPhysicalSourceChange
#print axioms c60F112MixedPhysicalSourceChange_native
#print axioms c60F112MixedPhysicalSourceChange_faithful
#print axioms c60F112MixedPhysicalSourceChange_square
#print axioms c60F112MixedPhysicalThreeChanges_cocycle
#print axioms c60F112MixedPhysicalLeftBeckChevalley
#print axioms c60F112MixedPhysicalRightBeckChevalley
#print axioms c60F112MixedPhysicalLeft_noOriginalF55Lift
#print axioms c60F112MixedPhysicalRight_noOriginalF55Lift
#print axioms c60F112AllNinetyMixedPhysicalChange
#print axioms c60F112AllNinetyMixedPhysicalCech_cocycle

end IndependentPhysicalOriginalContexts
end
end KUOS.DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276
