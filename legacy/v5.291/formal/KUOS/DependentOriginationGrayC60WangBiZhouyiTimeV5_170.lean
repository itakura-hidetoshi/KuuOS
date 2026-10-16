import KUOS.DependentOriginationGrayC60YinYangFourImagesV5_170
import KUOS.DependentOriginationGrayC60LegacyHetuLuoshuV5_170
import Mathlib.Data.Fin.Tuple.Basic

namespace KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60YinYangFourImagesV5_170

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F22 / v5.170 — 王弼『周易略例』: actual C60 oriented 32 faces,
  64 symbolic six-line codes, trigrams, 三才, temporal interpretation

Priority is the original classical Wang Bi texts:
  『明象』: 得意在忘象、得象在忘言.
  『明卦適變通爻』: 夫卦者、時也；爻者、適時之變者也.

FIRST, one constructs a VALID *encoding* of the actual geometric
C60 carrier; only THEN can one ask for a CONTEXTUAL meaning.
The original C60 has 32 polygonal faces (12 pentagons + 20
hexagons), each with two locally chosen orientations/sides.
This gives 64 signed-face codes, not 64 a priori historical
hexagram names or an order of King Wen.

Choosing a chart between actual 32 faces and all five-bit codes
produces an honest bijection:
  original C60 face × orientation ↔ six Yao = (Fin 6 → Bool).
The orientation/surface side is precisely the designated zero-th
binary coordinate of the six-line symbol. This is a CHOICE of
symbolic encoding, not intrinsic physical Yi/Jing morphology.

The six lines split into two 3-line trigrams, and into three
two-line pairs (Earth–Human–Heaven / 三才). A local Yao change
is a genuine involutive state transition. Wang Bi's "hexagram
is a time, Yao changes according to its time" is MODELLED as
a time/context-indexed interpretation function which is not
identified with numerical code by assumption.

Crucially, a change of arbitrary five-bit C60 face chart can be
compensated by transporting the interpretation data: the FINAL
meaning assigned to an original signed face is chart-independent.
This is a constructive, fully typed expression of the principle
that the *象* is a representational instrument, not the *意*
itself. No classical line judgment or hexagram name is invented
by mathematics. The original 60/90/32 C60 chain complex remains
untouched. Twelve branches and 24 solar terms can later enter
only as supplied temporal contexts, not as automatic meanings.
-/

/-- A six-Yao Yin/Yang code. False/true is only a chosen
two-element notation, not an automatic favorable judgment. -/
abbrev WangBiSixYao := Fin 6 → Bool

/-- Eight possible three-Yao patterns, prior to historical
naming conventions. -/
abbrev WangBiThreeYao := Fin 3 → Bool

/-- One actual REAL C60 polygon with one of its two sides or
orientations selected. This is a geometric encoding carrier. -/
abbrev C60WangBiSignedFace :=
  TruncatedIcosahedralSeedFace × Bool

theorem c60WangBiSignedFace_card64 :
    Fintype.card C60WangBiSignedFace = 64 := by
  decide

theorem c60WangBiSixYao_card64 :
    Fintype.card WangBiSixYao = 64 := by
  decide

theorem c60WangBiThreeYao_card8 :
    Fintype.card WangBiThreeYao = 8 := by
  decide

/-- A face chart is an EXPLICIT CHOICE of five bits for each
original 32-face geometry. Wang Bi's reading does not license
declaring such a choice the unique historical卦序. -/
abbrev C60WangBiFaceChart :=
  TruncatedIcosahedralSeedFace ≃ (Fin 5 → Bool)

/-- A genuine finite chart exists because this ACTUAL C60
has precisely 32 physical pentagons/hexagons. Its assignment
to five-bit words is a chosen enumeration, not the King Wen
or Fu Xi hexagram order. -/
noncomputable def c60WangBiFiniteFaceChart :
    C60WangBiFaceChart :=
  Fintype.equivOfCardEq (by decide)

/-- One entirely explicit six-Yao encoding from any supplied
original 32-face chart:
  side bit + five face bits = six Yao.
The first bit always records the chosen side. -/
def c60WangBiSignedFaceHexagramChart
    (chart : C60WangBiFaceChart) :
    C60WangBiSignedFace ≃ WangBiSixYao :=
  ((Equiv.prodComm TruncatedIcosahedralSeedFace Bool).trans
    (Equiv.prodCongr (Equiv.refl Bool) chart)).trans
    (Fin.insertNthEquiv (fun _ : Fin 6 => Bool) 0)

/-- The original side flag appears literally in the first
binary line of this chart, without assuming it is an
actual geometric line on a C60 polygon. -/
theorem c60WangBiSignedFace_sideBit
    (chart : C60WangBiFaceChart)
    (face : TruncatedIcosahedralSeedFace) (side : Bool) :
    (c60WangBiSignedFaceHexagramChart chart (face, side)) 0 = side := by
  simp [c60WangBiSignedFaceHexagramChart, Fin.insertNthEquiv]

/-- Encoding followed by decoding returns the SAME original
signed face; no geometric or historical information is lost
within the SELECTED mathematical coding chart. -/
theorem c60WangBiSignedFace_decode_encode
    (chart : C60WangBiFaceChart)
    (fs : C60WangBiSignedFace) :
    (c60WangBiSignedFaceHexagramChart chart).symm
      (c60WangBiSignedFaceHexagramChart chart fs) = fs :=
  (c60WangBiSignedFaceHexagramChart chart).symm_apply_apply fs

/-- Encoding an arbitrary six-Yao code after decoding it
returns that precise same six-Yao code. -/
theorem c60WangBiSignedFace_encode_decode
    (chart : C60WangBiFaceChart)
    (x : WangBiSixYao) :
    c60WangBiSignedFaceHexagramChart chart
      ((c60WangBiSignedFaceHexagramChart chart).symm x) = x :=
  (c60WangBiSignedFaceHexagramChart chart).apply_symm_apply x

/-- Genuine bottom/top 3+3 Yao decomposition, using the natural
Mathlib equivalence of six functions and two length-three
functions, rather than arbitrary cardinality matching. -/
def c60WangBiTwoTrigrams :
    WangBiSixYao ≃ WangBiThreeYao × WangBiThreeYao :=
  (Fin.appendEquiv 3 3).symm

/-- A six-Yao code is recovered EXACTLY from the two
three-Yao patterns, so neither sub-pattern is discarded. -/
theorem c60WangBiTrigram_reconstruct
    (x : WangBiSixYao) :
    (c60WangBiTwoTrigrams).symm
      (c60WangBiTwoTrigrams x) = x :=
  c60WangBiTwoTrigrams.symm_apply_apply x

/-- The original 三才 (Earth, Human, Heaven) are three pairs
of successive Yao positions, NOT three new geometric C60
poles or a three-element replacement for Yin/Yang. -/
inductive C60WangBiThreePowers
  | earth | human | heaven
  deriving DecidableEq, Repr, Fintype

def c60WangBiPowerIndex : C60WangBiThreePowers → Fin 3
  | .earth => 0
  | .human => 1
  | .heaven => 2

/-- One of the two original Yin/Yang positions within a
Three Powers layer. -/
def c60WangBiThreePowerYaoPosition
    (power : C60WangBiThreePowers) (line : Fin 2) : Fin 6 :=
  ⟨2 * (c60WangBiPowerIndex power).val + line.val, by
    cases power <;> omega⟩

/-- Explicit 3×2≅6 correspondence for all Yao slots:
the three powers partition ALL six line positions exactly. -/
theorem c60WangBiThreePowersYao_bijective :
    Function.Bijective
      (fun ps : C60WangBiThreePowers × Fin 2 =>
        c60WangBiThreePowerYaoPosition ps.1 ps.2) := by
  decide

noncomputable def c60WangBiThreePowersYaoEquiv :
    (C60WangBiThreePowers × Fin 2) ≃ Fin 6 :=
  Equiv.ofBijective
    (fun ps => c60WangBiThreePowerYaoPosition ps.1 ps.2)
    c60WangBiThreePowersYao_bijective

/-- View an original six-Yao symbol as 3×2 Yao coordinates
without losing the order or the Yin/Yang values. -/
def c60WangBiThreePowersSymbol
    (x : WangBiSixYao) :
    C60WangBiThreePowers → Fin 2 → Bool :=
  fun p j => x (c60WangBiThreePowerYaoPosition p j)

/-- The original six-Yao function is fully reconstructible
from its three power-wise two-Yao factors. -/
theorem c60WangBiThreePowersSymbol_reconstruction
    (x : WangBiSixYao) (i : Fin 6) :
    (c60WangBiThreePowersSymbol x
      (c60WangBiThreePowersYaoEquiv.symm i).1
      (c60WangBiThreePowersYaoEquiv.symm i).2) = x i := by
  unfold c60WangBiThreePowersSymbol
  exact congrArg x
    (c60WangBiThreePowersYaoEquiv.apply_symm_apply i)

/-- A genuine change of one selected original Yao position:
the other five positions remain unchanged. Its value is a
state transformation, not an automatic clinical or divinatory
judgment. -/
def c60WangBiChangeYao (x : WangBiSixYao)
    (chosen : Fin 6) : WangBiSixYao :=
  fun i => if i = chosen then !x i else x i

theorem c60WangBiChangeYao_involutive
    (x : WangBiSixYao) (chosen : Fin 6) :
    c60WangBiChangeYao (c60WangBiChangeYao x chosen) chosen = x := by
  funext i
  by_cases h : i = chosen
  · simp [c60WangBiChangeYao, h]
  · simp [c60WangBiChangeYao, h]

theorem c60WangBiChangeYao_selected
    (x : WangBiSixYao) (chosen : Fin 6) :
    (c60WangBiChangeYao x chosen) chosen = !x chosen := by
  simp [c60WangBiChangeYao]

theorem c60WangBiChangeYao_other
    (x : WangBiSixYao) (chosen i : Fin 6) (h : i ≠ chosen) :
    (c60WangBiChangeYao x chosen) i = x i := by
  simp [c60WangBiChangeYao, h]

/-- The actual C60 two-sided representation flips its side
but does not change the underlying original 32-face object. -/
def c60WangBiFlipFaceSide :
    C60WangBiSignedFace → C60WangBiSignedFace
  | (face, side) => (face, !side)

theorem c60WangBiFlipFaceSide_involutive :
    Function.Involutive c60WangBiFlipFaceSide := by
  intro fs
  rcases fs with ⟨face, side⟩
  cases side <;> rfl

/-- The first Yao of the associated six-line symbol reverses
when the same REAL C60 face is viewed from its opposite side. -/
theorem c60WangBiSideFlip_firstYao
    (chart : C60WangBiFaceChart)
    (fs : C60WangBiSignedFace) :
    (c60WangBiSignedFaceHexagramChart chart
      (c60WangBiFlipFaceSide fs)) 0 =
        !((c60WangBiSignedFaceHexagramChart chart fs) 0) := by
  rcases fs with ⟨face, side⟩
  simp only [c60WangBiFlipFaceSide]
  rw [c60WangBiSignedFace_sideBit,
    c60WangBiSignedFace_sideBit]

/-- An arbitrary change of face-chart induces a fully
reversible, constructive permutation of all 64 six-Yao
symbols. No one C60 face enumeration is imposed as a
final cosmic sequence. -/
def c60WangBiChangeHexagramChart
    (fromChart toChart : C60WangBiFaceChart) :
    WangBiSixYao ≃ WangBiSixYao :=
  (c60WangBiSignedFaceHexagramChart fromChart).symm.trans
    (c60WangBiSignedFaceHexagramChart toChart)

theorem c60WangBiChartChange_compose
    (a b c : C60WangBiFaceChart) (x : WangBiSixYao) :
    c60WangBiChangeHexagramChart b c
      (c60WangBiChangeHexagramChart a b x) =
    c60WangBiChangeHexagramChart a c x := by
  simp [c60WangBiChangeHexagramChart]

/-- 王弼's SYMBOL / TIME / MEANING distinction is made a
proper typed interface. An actual semantic reading must be
supplied with both its historical situation and its
interpretive authority; bare cardinality cannot create it. -/
structure WangBiTemporalReading (Time Meaning : Type*) where
  interpret : WangBiSixYao → Time → Meaning

/-- An interpretation of one original signed C60 face at a
time/context, through an explicitly supplied 64-code chart. -/
def c60WangBiReadSignedFace
    {Time Meaning : Type*}
    (chart : C60WangBiFaceChart)
    (reading : WangBiTemporalReading Time Meaning)
    (fs : C60WangBiSignedFace) (time : Time) : Meaning :=
  reading.interpret (c60WangBiSignedFaceHexagramChart chart fs) time

/-- Correctly transfer ANY time-dependent reading when the
Wuxing/symbol chart changes. This is a constructive form of
not privileging *象* over *意*: original face meanings can
remain coherent under re-encoding, while the actual source
face and the original time/context are not discarded. -/
def c60WangBiTransportReading
    {Time Meaning : Type*}
    (fromChart toChart : C60WangBiFaceChart)
    (reading : WangBiTemporalReading Time Meaning) :
    WangBiTemporalReading Time Meaning where
  interpret := fun code time =>
    reading.interpret
      (c60WangBiChangeHexagramChart toChart fromChart code)
      time

/-- Meaning-preserving chart transport, for every original
C60 face, both of its sides and all supplied time contexts.
This is the actual categorical-style commuting diagram
analogous to Wang Bi's "symbol makes meaning visible". -/
theorem c60WangBiRead_commutes_with_chart_transport
    {Time Meaning : Type*}
    (fromChart toChart : C60WangBiFaceChart)
    (reading : WangBiTemporalReading Time Meaning)
    (fs : C60WangBiSignedFace) (time : Time) :
    c60WangBiReadSignedFace toChart
      (c60WangBiTransportReading fromChart toChart reading)
      fs time =
    c60WangBiReadSignedFace fromChart reading fs time := by
  simp [c60WangBiReadSignedFace,
    c60WangBiTransportReading,
    c60WangBiChangeHexagramChart]

#print axioms c60WangBiSignedFace_card64
#print axioms c60WangBiSixYao_card64
#print axioms c60WangBiThreeYao_card8
#print axioms c60WangBiFiniteFaceChart
#print axioms c60WangBiSignedFace_sideBit
#print axioms c60WangBiSignedFace_decode_encode
#print axioms c60WangBiSignedFace_encode_decode
#print axioms c60WangBiTrigram_reconstruct
#print axioms c60WangBiThreePowersYao_bijective
#print axioms c60WangBiThreePowersSymbol_reconstruction
#print axioms c60WangBiChangeYao_involutive
#print axioms c60WangBiChangeYao_selected
#print axioms c60WangBiChangeYao_other
#print axioms c60WangBiFlipFaceSide_involutive
#print axioms c60WangBiSideFlip_firstYao
#print axioms c60WangBiChartChange_compose
#print axioms c60WangBiRead_commutes_with_chart_transport

end
end KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
