import KuuOSFormal.HistoricalF36F40BridgeP37
import Mathlib.Tactic.Abel

/-!
# F112-P38 — actual historical F47 to independent native C60 mixed-presentation functor

P36 retained the genuinely original F47 physical edge, its two
different C60 adjacent polygon F42 Type-valued fan/disk atlases, and
the independent original F19/F28/F54/F55 sources and mixed square.
P37 constructed a fully proved additive gauge between all FOUR
original F47 source positions and any separately calibrated native
physical-F42/F55 mixed comparison frame.

P38 now constructs an ACTUAL Mathlib Functor between the two
FOUR-BOUNDARY MIXED PRESENTATION CATEGORIES. It explicitly translates
EVERY original proof-relevant raw mixed 3-arrow constructor into the
corresponding *newly adjoined* native mixed presentation generator,
preserving all four tagged source/target positions and arbitrary
vertical pasting.

The crucial quotient map is NOT postulated. We prove a naturality
identity for the complete (Int×Int)×ZMod2 evaluation of every original
raw mixed 3-proof, using P37's four generator gauge laws, and then
induction on arbitrary raw vertical composition. This proves
well-defined descent through the ORIGINAL F47 full-shadow kernel to
the independent native mixed full-shadow kernel, and hence a genuine
functor with proven identity/composition laws.

This functor compares only the TWO SPECIFIED, freely adjoined mixed
four-boundary PRESENTATION CATEGORIES. It does NOT yet construct a
type-faithful functor on all original/natively independent F42/F55
2-source objects, all original F54 rotation raw witnesses, or
a Gray/Beck-Chevalley 3-equivalence. Crucially, different original
physical C60 edges are NOT claimed to be the chosen north hexagon.
No new axioms, sorry, admit, or Gray import into KuuOSStrict.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156

set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe uP38 vP38 uDP38 vDP38
variable {C : Type uP38} [Category.{vP38} C]
variable {D : Type uDP38} [Category.{vDP38} D]
variable {a b : C} {x y : D} {n n' m m' : Nat}
variable {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- Translate FOUR original mixed F47 source-position tags to the
four DIFFERENT independently presented native mixed C60 positions.
The old F42/F55 type data are retained by the historical index B;
this is a position translation, not a source 2-cell equivalence. -/
def historicalF47BoundaryToNativeMixed
    {B : C60F47SquareFrame α β r s}
    (N : NativeC60PhysicalMixedCalibration) :
    C60F47BoundaryPoint B → NativeC60MixedPoint N
  | .faceBefore => .physicalBefore
  | .faceAfter => .physicalAfter
  | .rotationBefore => .rotationBefore
  | .rotationAfter => .rotationAfter

/-- Translate all SIX freely presented historical F47 raw mixed
constructors, including arbitrary vertical pastes. Physical-face and
native-F55 generator TYPES are never identified; only the explicitly
matched four-boundary formal presentation shapes are translated. -/
def historicalF47MixedRawToNative
    (B : C60F47SquareFrame α β r s)
    (N : NativeC60PhysicalMixedCalibration)
    {X Y : C60F47BoundaryPoint B}
    (f : C60F47PresentedMixedThreeCell B X Y) :
    NativeC60MixedRaw N
      (historicalF47BoundaryToNativeMixed N X)
      (historicalF47BoundaryToNativeMixed N Y) :=
  match f with
  | .ident X => .ident (historicalF47BoundaryToNativeMixed N X)
  | .originalFace => .physicalStep
  | .originalF55 => .rotationStep
  | .compareBefore => .compareBefore
  | .compareAfter => .compareAfter
  | .trans f g =>
      .trans (historicalF47MixedRawToNative B N f)
        (historicalF47MixedRawToNative B N g)

/-- Read a complete historical Gray target element as the SAME
algebraic three-coordinate carrier used by independent Kuu.
This coordinate reading, by itself, is not a comparison functor
between source types. -/
def historicalF47GradeCoordinates (z : GradedThreeCell 0 0) :
    KuuNativeF55Shadow :=
  (z.charge, z.phase)

/-- The actual historical vertical composition is additive on BOTH
integer charges and ZMod2 phase. No grade or raw 3-proof is erased
when establishing this coordinate-level statement. -/
theorem historicalF47GradeCoordinates_add
    (z w : GradedThreeCell 0 0) :
    historicalF47GradeCoordinates (z + w) =
      historicalF47GradeCoordinates z + historicalF47GradeCoordinates w := by
  apply Prod.ext
  · rfl
  · rfl

/-- Extract one of P37's four object-boundary gauge potentials. -/
def HistoricalF47FourBoundaryGauge.at
    {B : C60F47SquareFrame α β r s}
    {N : NativeC60PhysicalMixedCalibration}
    (G : HistoricalF47FourBoundaryGauge B N) :
    C60F47BoundaryPoint B → KuuNativeF55Shadow
  | .faceBefore => G.faceBefore
  | .faceAfter => G.faceAfter
  | .rotationBefore => G.rotationBefore
  | .rotationAfter => G.rotationAfter

/-- Additive cancellation of an intermediate boundary gauge in
arbitrary consecutive vertical pasting. This is the exact algebra
needed for functoriality, not an unproved mixed 3-interchanger. -/
private theorem nativeF47Gauge_vertical
    {u v w x y z p : KuuNativeF55Shadow}
    (hFirst : u + p = w + x)
    (hSecond : v + x = y + z) :
    (u + v) + p = (w + y) + z := by
  calc
    (u + v) + p = (u + p) + v := by abel
    _ = (w + x) + v := by rw [hFirst]
    _ = w + (v + x) := by abel
    _ = w + (y + z) := by rw [hSecond]
    _ = (w + y) + z := by abel

/-- FUNDAMENTAL GAUGE NATURALITY, proved by structural induction
on EVERY original historical F47 mixed raw 3-arrow. The two
physical face/rotation generators, two comparison generators,
identities and arbitrary vertical pastes ALL respect the same
complete-shadow four-boundary transport.

The equality retains old B's original face/F55 boundary types
and native N's independently typed four different boundary tags. -/
theorem historicalF47MixedRawToNative_gauge
    {B : C60F47SquareFrame α β r s}
    {N : NativeC60PhysicalMixedCalibration}
    (G : HistoricalF47FourBoundaryGauge B N)
    {X Y : C60F47BoundaryPoint B}
    (f : C60F47PresentedMixedThreeCell B X Y) :
    (historicalF47MixedRawToNative B N f).toShadow + G.at X =
      historicalF47GradeCoordinates f.toNative + G.at Y := by
  induction f with
  | ident X =>
      rfl
  | originalFace =>
      exact (add_comm N.faceValue G.faceBefore).trans G.face_law.symm
  | originalF55 =>
      exact (add_comm N.rotationValue G.rotationBefore).trans G.rotation_law.symm
  | compareBefore =>
      exact (add_comm N.compareBefore G.faceBefore).trans G.before_law.symm
  | compareAfter =>
      exact (add_comm N.compareAfter G.faceAfter).trans G.after_law.symm
  | trans f g hf hg =>
      simpa only [historicalF47MixedRawToNative,
        NativeC60MixedRaw.toShadow,
        C60F47PresentedMixedThreeCell.toNative,
        historicalF47GradeCoordinates_add] using
        nativeF47Gauge_vertical hf hg

/-- The ACTUAL original full-shadow F47 mixed quotient descends
through the independently defined native full-shadow mixed quotient.
Well-definedness follows from the proven ALL-CONSTRUCTOR gauge
naturality, not from an assumed historical F47/Kuu equivalence. -/
def historicalF47MixedHomToNative
    {B : C60F47SquareFrame α β r s}
    {N : NativeC60PhysicalMixedCalibration}
    (G : HistoricalF47FourBoundaryGauge B N)
    {X Y : C60F47BoundaryPoint B}
    (f : C60F47MixedHom B X Y) :
    NativeC60MixedHom N
      (historicalF47BoundaryToNativeMixed N X)
      (historicalF47BoundaryToNativeMixed N Y) :=
  Quot.liftOn f
    (fun raw => nativeC60MixedOf
      (historicalF47MixedRawToNative B N raw))
    (by
      intro left right heq
      apply Quot.sound
      have hl := historicalF47MixedRawToNative_gauge G left
      have hr := historicalF47MixedRawToNative_gauge G right
      have hcoord := congrArg historicalF47GradeCoordinates heq
      apply add_right_cancel
      calc
        (historicalF47MixedRawToNative B N left).toShadow + G.at X =
            historicalF47GradeCoordinates left.toNative + G.at Y := hl
        _ = historicalF47GradeCoordinates right.toNative + G.at Y := by
          rw [hcoord]
        _ = (historicalF47MixedRawToNative B N right).toShadow + G.at X :=
          hr.symm)

/-- A TRUE Mathlib Functor from the preserved historical original
F47 four-boundary mixed 3-Hom PRESENTATION category into the
independent native C60 physical-F42/F55 four-boundary mixed 3-Hom
presentation category. The source physical edge B and original
typed F42/F55 boundaries are retained in B, and arbitrary vertical
composition is mapped constructor-by-constructor.

No map between arbitrary old/new underlying 2-dimensional proof
sources and no Beck-Chevalley source 3-equivalence is asserted. -/
def historicalF47MixedToNativeFunctor
    {B : C60F47SquareFrame α β r s}
    {N : NativeC60PhysicalMixedCalibration}
    (G : HistoricalF47FourBoundaryGauge B N) :
    C60F47BoundaryPoint B ⥤ NativeC60MixedPoint N where
  obj X := historicalF47BoundaryToNativeMixed N X
  map := fun {_ _} f => historicalF47MixedHomToNative G f
  map_id := by
    intro X
    rfl
  map_comp := by
    intro X Y Z f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    rfl

/-- The mapped actual old quotient arrow obeys the same proved
complete-shadow affine naturality law. It is not merely a
representative-dependent statement about freely generated raw
comparison paths. -/
theorem historicalF47MixedToNativeFunctor_shadow
    {B : C60F47SquareFrame α β r s}
    {N : NativeC60PhysicalMixedCalibration}
    (G : HistoricalF47FourBoundaryGauge B N)
    {X Y : C60F47BoundaryPoint B}
    (f : X ⟶ Y) :
    nativeC60MixedEval
        ((historicalF47MixedToNativeFunctor G).map f) + G.at X =
      historicalF47GradeCoordinates (c60F47MixedEval f) + G.at Y := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact historicalF47MixedRawToNative_gauge G raw

/-- Every original F47 square B and independently calibrated native
mixed comparison N yields this gauge-corrected functor. It is
a presentation-level four-boundary comparison, not the
historical F42/F55 higher-source equivalence. -/
def historicalF47MixedToNativeGivenCalibration
    (B : C60F47SquareFrame α β r s)
    (N : NativeC60PhysicalMixedCalibration)
    (hN : N.Calibrated) :
    C60F47BoundaryPoint B ⥤ NativeC60MixedPoint N :=
  historicalF47MixedToNativeFunctor
    (historicalF47FourBoundaryGauge B N hN)

/-- In particular, the real north C60 native physical/rotation
square gives a fully typed chosen mixed presentation functor from
ANY old calibrated historical F47 frame, with no unjustified
identification of the two frames' physical polygon sites. -/
def historicalF47MixedToNorthNativeFunctor
    (B : C60F47SquareFrame α β r s) :
    C60F47BoundaryPoint B ⥤
      NativeC60MixedPoint northHexagonPhysicalMixedCalibrated :=
  historicalF47MixedToNativeGivenCalibration B
    northHexagonPhysicalMixedCalibrated
    northHexagonPhysicalMixedCalibrated_valid

#print axioms historicalF47BoundaryToNativeMixed
#print axioms historicalF47MixedRawToNative
#print axioms historicalF47GradeCoordinates_add
#print axioms HistoricalF47FourBoundaryGauge.at
#print axioms historicalF47MixedRawToNative_gauge
#print axioms historicalF47MixedHomToNative
#print axioms historicalF47MixedToNativeFunctor
#print axioms historicalF47MixedToNativeFunctor_shadow
#print axioms historicalF47MixedToNativeGivenCalibration
#print axioms historicalF47MixedToNorthNativeFunctor

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
