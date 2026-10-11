import KUOS.DependentOriginationGrayC60LegacyWuxingGlobalTransportV5_170
import KUOS.Architecture.QiProcessTensorLocalRealYinYangGeometryV2_4
import KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154

namespace KUOS.DependentOriginationGrayC60YinYangFourImagesV5_170

open KUOS.Architecture
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 3000000
noncomputable section

/-!
# F59-F22 — Yin-Yang polar axis, complex local-real structure and 四象

Per the original KuuOS Qi v2.3/v2.4 specifications:
  陰陽 is a LOCAL REAL POLARITY FRAME, not fixed substances.
  It is not a claim that Yin = imaginary part, Yang = real part.
  Five phases are FUNCTIONAL DIFFERENTIATION within the YinYang flow.

Original C60 has two privileged original ICOSAHEDRAL poles,
North and South. These poles are centers of real PENTAGON FACES
in truncated C60, not themselves added C60 surface dart vertices.

A chosen frame identifies the poles with conjugations κ or −κ
on the complex analytic carrier. Reversing the frame exchanges
the two choices. Thus the poles express a relational axis, not
fixed intrinsic North=Yang or South=Yin essences.

The Four Images (四象) are two successive local YinYang distinctions,
realized on EACH of the 90 already constructed K2,2 four-flag
incidence squares. Four Image labels require a local choice of
vertex/face order; the C60 underlying surface still has NO square
polygonal face. All statements are mathematical structural
constructions, not physiological or thermodynamic measurements.
-/

/-- Geometric polar pentagon labels of the ACTUAL original C60. -/
inductive C60PolarEnd | north | south
  deriving DecidableEq, Repr, Fintype

def c60PolarOpposite : C60PolarEnd → C60PolarEnd
  | .north => .south
  | .south => .north

theorem c60PolarOpposite_involutive :
    Function.Involutive c60PolarOpposite := by
  intro p
  cases p <;> rfl

/-- The two original icosahedral poles are centers of two
different REAL C60 five-edge faces. -/
def c60PolarPentagon : C60PolarEnd → TruncatedIcosahedralSeedFace
  | .north => .aroundVertex .north
  | .south => .aroundVertex .south

theorem c60PolarPentagons_distinct :
    c60PolarPentagon .north ≠ c60PolarPentagon .south := by decide

/-- κ₊(z)=conj(z), κ₋(z)=−conj(z), chosen relationally
at the two real poles. In particular this is NOT z↦±z
and does not assert poles have absolute intrinsic polarity. -/
def c60PolarComplexConjugation
    (chart : Bool) (pole : C60PolarEnd) (z : ℂ) : ℂ :=
  if chart == (pole == .north) then Complex.conj z
  else -Complex.conj z

/-- Both local complex conjugations square to identity;
a polar frame can be reversed without altering involutivity. -/
theorem c60PolarComplexConjugation_involutive
    (chart : Bool) (pole : C60PolarEnd) :
    Function.Involutive (c60PolarComplexConjugation chart pole) := by
  intro z
  cases chart <;> cases pole <;>
    simp [c60PolarComplexConjugation, Complex.ext_iff]

/-- The exact ORIGINAL KuuOS v2.4 LocalRealFrame interface,
now instantiated on the physical north/south C60 pentagons
with an honest complex conjugate-involutive structure. -/
def c60PolarLocalRealFrame
    (chart : Bool) (pole : C60PolarEnd) : LocalRealFrame ℂ where
  conjugation := c60PolarComplexConjugation chart pole
  involutive := c60PolarComplexConjugation_involutive chart pole

/-- Flipping the chosen C60 pole swaps local complex real
structures by a MINUS SIGN. This is a comparison between
frames, not a fixed intrinsic Yin/Yang material assignment. -/
theorem c60PolarFlip_changesConjugation
    (chart : Bool) (pole : C60PolarEnd) (z : ℂ) :
    c60PolarComplexConjugation chart (c60PolarOpposite pole) z =
      -c60PolarComplexConjugation chart pole z := by
  cases chart <;> cases pole <;>
    simp [c60PolarComplexConjugation, c60PolarOpposite]

/-- Original KuuOS v2.4 Yang/Yin ±1 projection formula
relative to the CHOSEN local real involution. -/
def c60PolarYangProjection
    (chart : Bool) (pole : C60PolarEnd) (z : ℂ) : ℂ :=
  (z + c60PolarComplexConjugation chart pole z) / 2

def c60PolarYinProjection
    (chart : Bool) (pole : C60PolarEnd) (z : ℂ) : ℂ :=
  (z - c60PolarComplexConjugation chart pole z) / 2

theorem c60PolarProjections_reconstruct
    (chart : Bool) (pole : C60PolarEnd) (z : ℂ) :
    c60PolarYangProjection chart pole z +
      c60PolarYinProjection chart pole z = z := by
  unfold c60PolarYangProjection c60PolarYinProjection
  ring

/-- Swap North/South and the two original Yin/Yang projector
roles EXCHANGE, without asserting any pole is forever Yin or Yang. -/
theorem c60PolarFlip_exchangesProjections
    (chart : Bool) (pole : C60PolarEnd) (z : ℂ) :
    c60PolarYangProjection chart (c60PolarOpposite pole) z =
      c60PolarYinProjection chart pole z := by
  rw [c60PolarYangProjection, c60PolarYinProjection,
    c60PolarFlip_changesConjugation]
  ring

theorem c60PolarFlip_exchangesOtherProjection
    (chart : Bool) (pole : C60PolarEnd) (z : ℂ) :
    c60PolarYinProjection chart (c60PolarOpposite pole) z =
      c60PolarYangProjection chart pole z := by
  rw [c60PolarYinProjection, c60PolarYangProjection,
    c60PolarFlip_changesConjugation]
  ring

/-- 四象: the two-step differentiation of a local Yin/Yang
distinction, one bit for source endpoint, one for incident face. -/
inductive C60FourImage
  | taiyin | shaoyin | shaoyang | taiyang
  deriving DecidableEq, Repr, Fintype

def c60FourImageOfFlags : Bool × Bool → C60FourImage
  | (false,false) => .taiyin
  | (false,true)  => .shaoyin
  | (true,false)  => .shaoyang
  | (true,true)   => .taiyang

theorem c60FourImageOfFlags_bijective :
    Function.Bijective c60FourImageOfFlags := by decide

/-- Four Images are not free-floating names: each of the
ninety genuine original C60 edge/face INCIDENCE SQUARES
realizes all four flag combinations on true original faces. -/
def c60FourImageActualFlag
    {e : TruncatedIcosahedralEdge}
    (square : TruncatedEdgeFlagSquare e)
    (image : C60FourImage) :
    IcosahedralDart × TruncatedIcosahedralSeedFace :=
  let corners : Bool × Bool :=
    (Equiv.ofBijective c60FourImageOfFlags
      c60FourImageOfFlags_bijective).symm image
  (square.vertex corners.1, square.face corners.2)

/-- Every actual four-image flag is a valid C60 vertex-face
incidence; the corresponding square was constructed at a real
90-edge and contains two distinct endpoints and two faces. -/
theorem c60FourImageActualFlag_incident
    {e : TruncatedIcosahedralEdge}
    (square : TruncatedEdgeFlagSquare e)
    (image : C60FourImage) :
    truncatedDartOnSeedFace
      (c60FourImageActualFlag square image).1
      (c60FourImageActualFlag square image).2 := by
  exact square.corner_incident _ _

/-- The four Image combinations correspond bijectively to
the four REAL flags of every original edge incidence square. -/
theorem c60FourImageActualFlag_injective
    {e : TruncatedIcosahedralEdge}
    (square : TruncatedEdgeFlagSquare e) :
    Function.Injective (c60FourImageActualFlag square) := by
  intro a b h
  have hinj := square.corner_injective
  exact (Equiv.ofBijective c60FourImageOfFlags
    c60FourImageOfFlags_bijective).symm.injective (hinj h)

theorem c60FourImage_card :
    Fintype.card C60FourImage = 4 := by decide

#print axioms c60PolarOpposite_involutive
#print axioms c60PolarPentagons_distinct
#print axioms c60PolarComplexConjugation_involutive
#print axioms c60PolarFlip_changesConjugation
#print axioms c60PolarProjections_reconstruct
#print axioms c60PolarFlip_exchangesProjections
#print axioms c60PolarFlip_exchangesOtherProjection
#print axioms c60FourImageOfFlags_bijective
#print axioms c60FourImageActualFlag_incident
#print axioms c60FourImageActualFlag_injective
#print axioms c60FourImage_card

end
end KUOS.DependentOriginationGrayC60YinYangFourImagesV5_170
