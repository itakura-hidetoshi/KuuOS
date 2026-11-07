import KuuOSFormal.HistoricalNativeF55CommonShadowLEC12
import KuuOSFormal.HistoricalF36F40BridgeP56

/-!
# LEC-13 — original F40 boundary Type ↔ independent F54 and F55 source transport

LEC-12 compares TWO genuinely different historical original and new native
F55 source Types at one explicitly shared signed-charge/phase observation.
It does NOT construct a total original F54 → native F54 equivalence.

This module uses the *actual* original historical Grid.Blocks Type:
  OldBlocks, oldBlocksEquivNative
from retained P4, and the *actual* original F42 quotient-to-localization
functor, F54 transport and nine-constructor F55 transport from P53/P56.

First, old historical F40 Blocks are translated constructor-by-constructor
to independent native Blocks and then mapped to the real F69 localization.
Original intermediate categorical arrows, concatenation and composite
arrows are retained under the explicitly proven P4/P56 operations.

Second, at all four original-F40-typed boundary stages (both Nat depths
arbitrary), build a truly typed independent F54 long-vs-short pentagon
and its two distinct raw F55 histories: the primitive pentagon and
the same primitive followed by a right identity. Map BOTH via the
actual P56 original-F42-to-F69 all-nine-constructor transport.
The mapped source retains raw constructor shape and full chosen
signed two-charge/ZMod2 shadow. The two transported raw witnesses
remain DISTINCT, while their selected shadow readouts are EQUAL.

Hence the original history of even this transported F55 pair CANNOT
be recovered from its lawful selected shadow. This is stronger than
numeric calibration alone, and preserves a real historic F40 boundary.
But the original F54/F55 *history grammar* is not identified with
the native F54/F55 history grammar: its first-stage F40 comparison
and the independently presented native F54 higher source are two
different, explicitly stated steps. No original P77/GK5CG high
coherence, real C60 geometric old/north endpoint identification,
global historic-to-native F55 equivalence or ActOS permission follows.

This source lives ONLY under KuuOSFormal and never enters KuuOSStrict.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
Append-only / tighten-only / overwrite-forbidden / same-root.
-/

namespace KUOS.LivingEngiHistoricalBridge

open CategoryTheory
open Kuu.F112.Physical
open Kuu.LivingEngi
open KUOS.F112ActualHistoricalF36F40BridgeP4
open KUOS.F112ActualHistoricalF36F40BridgeP4.GenuineOriginalC60Geometry.ActualF47
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-! Actual retained original F40 Blocks, not a newly copied grammar. -/

section OriginalF40Boundary

variable {a b c : C60F42FaceRelationPathCategory}

/-- Transport ALL original F40 ordered Blocks to the genuine F69
localization via P4's type equivalence and P53's real F42 quotient. -/
def lec13OldF40BoundaryToF69 (s : OldBlocks a b) :
    KuuNativeBlocks
      (p53_originalF42QuotientToLocalization.obj a)
      (p53_originalF42QuotientToLocalization.obj b) :=
  (oldBlocksToNative s).map p53_originalF42QuotientToLocalization

/-- Even before localization, the complete historical original
Blocks syntax is recoverable EXACTLY from the independent counterpart. -/
theorem lec13OriginalF40_source_exact (s : OldBlocks a b) :
    nativeBlocksToOld (oldBlocksToNative s) = s :=
  nativeBlocksToOld_oldBlocksToNative s

/-- The independent native blocks can similarly be reconstructed
from the original full F40 Blocks without erasing empty subpaths. -/
theorem lec13NativeF40_source_exact (s : KuuNativeBlocks a b) :
    oldBlocksToNative (nativeBlocksToOld s) = s :=
  oldBlocksToNative_nativeBlocksToOld s

/-- The actual historical original F40 composite Hom is mapped into
F69 as a category Functor Hom, not just an integer charge statistic. -/
theorem lec13OldF40BoundaryToF69_composite
    (s : OldBlocks a b) :
    (lec13OldF40BoundaryToF69 s).composite =
      p53_originalF42QuotientToLocalization.map s.composite := by
  change ((oldBlocksToNative s).map
    p53_originalF42QuotientToLocalization).composite =
      p53_originalF42QuotientToLocalization.map s.composite
  rw [KuuNativeBlocks.composite_map, oldBlocksToNative_composite]

/-- The genuine complete original F40 segmented concatenation
commutes with historical F42-to-native-F69 localization. -/
theorem lec13OldF40BoundaryToF69_append
    (s : OldBlocks a b) (t : OldBlocks b c) :
    lec13OldF40BoundaryToF69 (s.append t) =
      (lec13OldF40BoundaryToF69 s).append
        (lec13OldF40BoundaryToF69 t) := by
  change (oldBlocksToNative (s.append t)).map
      p53_originalF42QuotientToLocalization =
    ((oldBlocksToNative s).map p53_originalF42QuotientToLocalization).append
      ((oldBlocksToNative t).map p53_originalF42QuotientToLocalization)
  rw [oldBlocksToNative_append, KuuNativeBlocks.map_append]

/-- Every original historic two-axis F40 boundary is transported
independently, retaining its explicitly distinct categorical axes. -/
theorem lec13OriginalF40_twoAxes_exact
    {x y : C60F42FaceRelationPathCategory}
    (sourceTarget : OldBlocks a b) (phaseTarget : OldBlocks x y) :
    nativeBlocksToOld (oldBlocksToNative sourceTarget) = sourceTarget ∧
      nativeBlocksToOld (oldBlocksToNative phaseTarget) = phaseTarget :=
  ⟨lec13OriginalF40_source_exact sourceTarget,
    lec13OriginalF40_source_exact phaseTarget⟩

end OriginalF40Boundary

/-! Original F40 boundaries produce *independent* F54 higher-source
trees over the ACTUAL historical F42 category. P56 then transports the
entire tree to independent F69 via the genuine original quotient. -/

section FourStageOriginalF40Boundary

variable (p : Polygon)
variable {a b x y : C60F42FaceRelationPathCategory}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : OldBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : OldBlocks x y}
variable
  (t₁ : KuuNativeF45Tree p n₁ m₁
    (oldBlocksToNative p₀) (oldBlocksToNative q₀)
    (oldBlocksToNative p₁) (oldBlocksToNative q₁))
  (t₂ : KuuNativeF45Tree p n₂ m₂
    (oldBlocksToNative p₁) (oldBlocksToNative q₁)
    (oldBlocksToNative p₂) (oldBlocksToNative q₂))
  (t₃ : KuuNativeF45Tree p n₃ m₃
    (oldBlocksToNative p₂) (oldBlocksToNative q₂)
    (oldBlocksToNative p₃) (oldBlocksToNative q₃))
  (t₄ : KuuNativeF45Tree p n₄ m₄
    (oldBlocksToNative p₃) (oldBlocksToNative q₃)
    (oldBlocksToNative p₄) (oldBlocksToNative q₄))

/-- Exactly the genuinely typed independent F54 pair over converted
HISTORICAL original F40 Blocks, with arbitrary two-Nat-stage depths. -/
abbrev LEC13OldF40NativeF55Raw :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄)

/-- The genuine free F55 pentagon generator on the actually converted
historic F40 boundary. No shadow equality generates this source cell. -/
def lec13OldF40NativePentagon :
    LEC13OldF40NativeF55Raw p t₁ t₂ t₃ t₄ :=
  .pentagon t₁ t₂ t₃ t₄

/-- A distinct original-F40-based F55 Type-value with a pasted unit,
retained in the raw source before any quotient is applied. -/
def lec13OldF40NativePentagonWithUnit :
    LEC13OldF40NativeF55Raw p t₁ t₂ t₃ t₄ :=
  .trans (lec13OldF40NativePentagon p t₁ t₂ t₃ t₄)
    (.ident (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄))

/-- Both genuinely typed original-F40-based pentagon histories differ
as raw F55 proof trees, even though both represent a lawful pentagon. -/
theorem lec13OldF40NativePentagon_raw_distinct :
    lec13OldF40NativePentagon p t₁ t₂ t₃ t₄ ≠
      lec13OldF40NativePentagonWithUnit p t₁ t₂ t₃ t₄ := by
  intro h
  have hs := congrArg
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag h
  change (1 : Nat) = 4 at hs
  exact (by decide : (1 : Nat) ≠ 4) hs

/-- Actual P56 full F55 constructor transport to F69, on BOTH
old F42 categorical axes. This is an actual raw Type value. -/
def lec13OldF40NativePentagonAtF69 :=
  p56_originalF42QuotientAllNineF55RawToF69
    (lec13OldF40NativePentagon p t₁ t₂ t₃ t₄)

/-- Preserve the distinct history with its original right-unit
constructor under the same F54/F55 source/target functor transport. -/
def lec13OldF40NativePentagonWithUnitAtF69 :=
  p56_originalF42QuotientAllNineF55RawToF69
    (lec13OldF40NativePentagonWithUnit p t₁ t₂ t₃ t₄)

/-- The actual mapped F69 pentagon still has the genuine primitive
source constructor shape (not an equality fabricated from a quotient). -/
theorem lec13OldF40NativePentagonAtF69_shape :
    (lec13OldF40NativePentagonAtF69 p t₁ t₂ t₃ t₄).shapeTag = 1 := by
  rw [lec13OldF40NativePentagonAtF69,
    p56_originalF42QuotientAllNineF55_shapeTag]
  rfl

/-- The original right unit still appears as a different structural
constructor after actual P56 full raw-typed F55 transport. -/
theorem lec13OldF40NativePentagonWithUnitAtF69_shape :
    (lec13OldF40NativePentagonWithUnitAtF69 p t₁ t₂ t₃ t₄).shapeTag = 4 := by
  rw [lec13OldF40NativePentagonWithUnitAtF69,
    p56_originalF42QuotientAllNineF55_shapeTag]
  rfl

/-- Localizing the ORIGINAL F42 category does not erase the two
distinct F55 raw proof histories on the historically converted F40. -/
theorem lec13OldF40NativePentagonAtF69_raw_distinct :
    lec13OldF40NativePentagonAtF69 p t₁ t₂ t₃ t₄ ≠
      lec13OldF40NativePentagonWithUnitAtF69 p t₁ t₂ t₃ t₄ := by
  intro h
  have hs := congrArg
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag h
  have ha := lec13OldF40NativePentagonAtF69_shape p t₁ t₂ t₃ t₄
  have hb := lec13OldF40NativePentagonWithUnitAtF69_shape p t₁ t₂ t₃ t₄
  exact (by decide : (1 : Nat) ≠ 4) (ha.symm.trans (hs.trans hb))

/-- The calibrated two signed F55 charges and chosen exchange phase
are preserved for the transported ORIGINAL-F40-based pentagon. -/
theorem lec13OldF40NativePentagonAtF69_shadow :
    (lec13OldF40NativePentagonAtF69 p t₁ t₂ t₃ t₄).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := by
  rw [lec13OldF40NativePentagonAtF69,
    p56_originalF42QuotientAllNineF55_shadow]
  rfl

/-- The primitive and right-unit source histories have the SAME
chosen signed-charge/phase readout, even though they remain raw-distinct. -/
theorem lec13OldF40NativePentagonWithUnitAtF69_shadow :
    (lec13OldF40NativePentagonWithUnitAtF69 p t₁ t₂ t₃ t₄).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := by
  rw [lec13OldF40NativePentagonWithUnitAtF69,
    p56_originalF42QuotientAllNineF55_shadow]
  change ((((1 : Int), (0 : Int)), (0 : ZMod 2)) : KuuNativeF55Shadow) +
      (0 : KuuNativeF55Shadow) =
    (((1 : Int), (0 : Int)), (0 : ZMod 2))
  exact add_zero _

/-- Exact observed collision of two DIFFERENT F69-transported
Type-valued source histories, without erasing their raw terms. -/
theorem lec13OldF40NativePentagonAtF69_shadow_collision :
    (lec13OldF40NativePentagonAtF69 p t₁ t₂ t₃ t₄).nativeShadow =
      (lec13OldF40NativePentagonWithUnitAtF69 p t₁ t₂ t₃ t₄).nativeShadow :=
  (lec13OldF40NativePentagonAtF69_shadow p t₁ t₂ t₃ t₄).trans
    (lec13OldF40NativePentagonWithUnitAtF69_shadow p t₁ t₂ t₃ t₄).symm

/-- Even after actual historical F40 and F42-to-F69 higher-source
transport, the selected numerical shadow CANNOT reconstruct every
original raw proof history. This is a concrete F55 collision. -/
theorem lec13OldF40NativePentagonAtF69_no_shadow_retraction :
    ¬ ∃ recover :
        KuuNativeF55Shadow →
          KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
            ((KuuNativeF45Tree.DepthRotationRoute.pentagonLong
              t₁ t₂ t₃ t₄).mapAxes
                p53_originalF42QuotientToLocalization
                p53_originalF42QuotientToLocalization)
            ((KuuNativeF45Tree.DepthRotationRoute.pentagonShort
              t₁ t₂ t₃ t₄).mapAxes
                p53_originalF42QuotientToLocalization
                p53_originalF42QuotientToLocalization),
        ∀ c, recover c.nativeShadow = c := by
  rintro ⟨recover, hrec⟩
  have heq := congrArg recover
    (lec13OldF40NativePentagonAtF69_shadow_collision p t₁ t₂ t₃ t₄)
  exact lec13OldF40NativePentagonAtF69_raw_distinct p t₁ t₂ t₃ t₄
    ((hrec _).symm.trans (heq.trans (hrec _)))

/-- Third-level old-F42/F69 path category source functor has an
actual faithful chosen-quotient Hom mapping; this is NOT raw source
faithfulness and does not invert the selected full shadow quotient. -/
theorem lec13OldF40NativeF55_selectedFunctor_faithful
    {f g :
      (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄) ⟶
      (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄)}
    (heq :
      (p56_originalF42QuotientF55ThreeFunctor
        (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
        (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄)).map f =
      (p56_originalF42QuotientF55ThreeFunctor
        (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
        (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄)).map g) :
    f = g :=
  p56_originalF42QuotientF55ThreeFunctor_faithful
    (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
    (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄) heq

#print axioms lec13OriginalF40_source_exact
#print axioms lec13NativeF40_source_exact
#print axioms lec13OldF40BoundaryToF69_composite
#print axioms lec13OldF40BoundaryToF69_append
#print axioms lec13OriginalF40_twoAxes_exact
#print axioms lec13OldF40NativePentagon_raw_distinct
#print axioms lec13OldF40NativePentagonAtF69_shape
#print axioms lec13OldF40NativePentagonWithUnitAtF69_shape
#print axioms lec13OldF40NativePentagonAtF69_raw_distinct
#print axioms lec13OldF40NativePentagonAtF69_shadow
#print axioms lec13OldF40NativePentagonWithUnitAtF69_shadow
#print axioms lec13OldF40NativePentagonAtF69_shadow_collision
#print axioms lec13OldF40NativePentagonAtF69_no_shadow_retraction
#print axioms lec13OldF40NativeF55_selectedFunctor_faithful

end FourStageOriginalF40Boundary

end
end KUOS.LivingEngiHistoricalBridge
