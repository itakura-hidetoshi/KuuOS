import KuuOSFormal.HistoricalNativeF55CommonShadowLEC12
import KuuOSFormal.HistoricalF36F40BridgeP40

/-!
# LEC-13 — exact old F54/F55 boundary and genuine C60 physical support

LEC-12 proved a genuine common F55 signed/phase readout on retained OLD
and newly independent NATIVE higher proof source Types, without asserting
a faithful raw-source functor or identifying original/new F54 endpoints.

An actual historical C60 F47 calibrated frame has its OWN physical edge,
not determined even by its un-erased OLD F42 and F55 categorical arrows.
P39/P40 prove this with 90 actual physical edges. We now apply those
earlier source-level theorems to the LEC-12 common F55 readout.

Unconditionally: for ANY genuine old typed F47 frame B at original F54
routes r,s, all 90 distinct physical edge supports have exactly the
same OLD F42/F55 source pair AND full signed/phase F55 readout.
Consequently no decoder of the pair PLUS common shadow can recover its
physical C60 support. The FULL support must be explicitly retained.

Conditionally: if the caller supplies an ACTUAL old raw F55 source at
exact F54 endpoints, proof that its old quotient arrow is B.rotationStep,
and a genuine native north C60 F55 raw source with the SAME readout,
we construct NINETY different, typed, calibrated original/native
comparison packets, retaining each true physical support. This does not
pretend that such a matched old F47 frame follows from numeric equality
alone, or supply an old F54 → native F54 source functor.

The 90 physical edges are REAL truncated-icosahedron edges, not Fin 90
proxy sites; the two incident polygonal faces are genuine.

No original source overwrite, no higher original P77/GK5CG comparison
equivalence, no arbitrary Gray/stack descent, no external action authority.
This module belongs only to the mixed KuuOSFormal layer; KuuOSStrict
and the independent Kuu root never import the old KUOS sources.
-/

namespace KUOS.LivingEngiHistoricalBridge

open CategoryTheory
open Kuu.F112.Physical
open Kuu.LivingEngi
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.F112ActualHistoricalF36F40BridgeP4.GenuineOriginalC60Geometry
open KUOS.F112ActualHistoricalF36F40BridgeP4.GenuineOriginalC60Geometry.ActualF47

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- Full chosen signed/phase shadow of the genuinely retained OLD F55
categorical arrow at exact original F54 routes r and s. -/
def lec13HistoricalF47F55Shadow
    (B : C60F47SquareFrame α β r s) :
    HistoricalNativeF55CommonShadow :=
  ((c60F44OriginalF55Eval B.rotationStep).charge,
    (c60F44OriginalF55Eval B.rotationStep).phase)

/-- The un-erased historical F42/F55 two-arrow pair is kept alongside
its separate numerical F55 common-shadow evaluation. Nothing about the
physical support edge follows merely from this selected observer. -/
def lec13HistoricalF47SourceShadow
    (B : C60F47SquareFrame α β r s) :
    ((α ⟶ β) × (r ⟶ s)) × HistoricalNativeF55CommonShadow :=
  (historicalF47ThreeSourcePair B, lec13HistoricalF47F55Shadow B)

/-- Replacing the physical C60 support edge leaves the exact old F55
arrow at the original route boundaries unchanged. -/
theorem lec13_edge_replacement_preserves_original_f55
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    (historicalF47AllEdgeFiberMap B e).1.rotationStep =
      B.rotationStep :=
  historicalF47AllEdgeFiberMap_rotation B e

/-- The same replacement preserves the separately typed original F42
face 3-arrow, not just its number-valued evaluation. -/
theorem lec13_edge_replacement_preserves_original_f42
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    (historicalF47AllEdgeFiberMap B e).1.faceStep = B.faceStep :=
  historicalF47AllEdgeFiberMap_face B e

/-- All ninety genuinely supported frames have EXACTLY the same OLD F55
charge and braided phase, even though the edges themselves differ. -/
theorem lec13_edge_replacement_preserves_common_shadow
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    lec13HistoricalF47F55Shadow
        (historicalF47AllEdgeFiberMap B e).1 =
      lec13HistoricalF47F55Shadow B := by
  rfl

/-- Even the combined un-erased OLD F42/F55 source pair PLUS the full
signed/phase common shadow is independent of the physical support edge.
This is substantially richer than a Bool or numerical-only proxy. -/
theorem lec13_edge_replacement_preserves_source_and_shadow
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    lec13HistoricalF47SourceShadow
        (historicalF47AllEdgeFiberMap B e).1 =
      lec13HistoricalF47SourceShadow B := by
  rfl

/-- Every actual C60 geometric support is exactly recovered from the
retained source F47 FRAME itself, not from its source/shadow projection. -/
theorem lec13_edge_replacement_support_exact
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    frameKuuEdge (historicalF47AllEdgeFiberMap B e).1 = e :=
  historicalF47AllEdgeFiberMap_support B e

/-- The stored physical edge also determines an ACTUAL pair of distinct
incident pentagonal/hexagonal C60 faces with authentic incidences. -/
theorem lec13_edge_replacement_two_real_faces
    (B : C60F47SquareFrame α β r s) (e : Edge) :
    let P := historicalF47TwoFaceNativeAtlas
      (historicalF47AllEdgeFiberMap B e).1
    P.edge = e ∧
      P.edge ∈ polygonBoundaryEdges P.firstFace ∧
      P.edge ∈ polygonBoundaryEdges P.secondFace ∧
      P.firstFace ≠ P.secondFace :=
  historicalF47AllEdgeFiberMap_twoFace_geometry B e

/-- The old complete two-source-plus-shadow observation is
NONINJECTIVE on the genuine 90-edge carrier. -/
theorem lec13_original_source_shadow_not_injective_on_edges
    (B : C60F47SquareFrame α β r s) :
    ¬ Function.Injective
      (fun e : Edge =>
        lec13HistoricalF47SourceShadow
          (historicalF47AllEdgeFiberMap B e).1) := by
  intro hInjective
  apply northOriginalCross_ne_around
  apply hInjective
  rw [lec13_edge_replacement_preserves_source_and_shadow,
      lec13_edge_replacement_preserves_source_and_shadow]

/-- Even knowing the entire original F42/F55 arrow pair and the chosen
complete F55 signed/phase shadow cannot recover ALL old C60 physical
edge supports. This is a true 90-edge obstruction, not missing evidence. -/
theorem lec13_no_support_decoder_from_original_source_shadow
    (B : C60F47SquareFrame α β r s) :
    ¬ ∃ recover :
        (((α ⟶ β) × (r ⟶ s)) × HistoricalNativeF55CommonShadow) → Edge,
      ∀ e : Edge,
        recover (lec13HistoricalF47SourceShadow
          (historicalF47AllEdgeFiberMap B e).1) = e := by
  rintro ⟨recover, hrecover⟩
  have hInjective : Function.Injective
      (fun e : Edge =>
        lec13HistoricalF47SourceShadow
          (historicalF47AllEdgeFiberMap B e).1) := by
    intro e f heq
    calc
      e = recover (lec13HistoricalF47SourceShadow
        (historicalF47AllEdgeFiberMap B e).1) := (hrecover e).symm
      _ = recover (lec13HistoricalF47SourceShadow
        (historicalF47AllEdgeFiberMap B f).1) := congrArg recover heq
      _ = f := hrecover f
  exact lec13_original_source_shadow_not_injective_on_edges B hInjective

/-- The exact ninety-way lower bound remains true with complete OLD F42,
OLD F54/F55 and chosen full F55 signed/phase shadow retained. -/
theorem lec13_ninety_real_edges_same_historical_source_shadow
    (B : C60F47SquareFrame α β r s) :
    Fintype.card Edge = 90 ∧
      Function.Injective (historicalF47AllEdgeFiberMap B) ∧
      (∀ e : Edge,
        lec13HistoricalF47SourceShadow
          (historicalF47AllEdgeFiberMap B e).1 =
          lec13HistoricalF47SourceShadow B) := by
  refine ⟨historicalF47PhysicalSupport_cardinality,
    historicalF47AllEdgeFiberMap_injective B, ?_⟩
  intro e
  exact lec13_edge_replacement_preserves_source_and_shadow B e

/-- Enriching the original observation by retaining its actual C60
physical Edge makes the ninety distinct authentic frame witnesses
injectively observable (but does not synthesize missing old/new
F54 endpoint comparison or higher 3-/4-cell transport). -/
def lec13SupportedSourceShadow
    (B : C60F47SquareFrame α β r s) :
    (((α ⟶ β) × (r ⟶ s)) × HistoricalNativeF55CommonShadow) × Edge :=
  (lec13HistoricalF47SourceShadow B, frameKuuEdge B)

/-- The extra Edge is recovered as data, not guessed from a quotient. -/
theorem lec13_supported_source_shadow_edge_exact
    (B : C60F47SquareFrame α β r s) :
    (lec13SupportedSourceShadow B).2 = frameKuuEdge B := rfl

/-- With the actual supported Edge field, all ninety frame variants
can be distinguished even though their source/shadow parts coincide. -/
theorem lec13_supported_source_shadow_injective_on_edges
    (B : C60F47SquareFrame α β r s) :
    Function.Injective (fun e : Edge =>
      lec13SupportedSourceShadow (historicalF47AllEdgeFiberMap B e).1) := by
  intro e f h
  have hedge := congrArg
    (fun z : (((α ⟶ β) × (r ⟶ s)) ×
      HistoricalNativeF55CommonShadow) × Edge => z.2) h
  simpa only [lec13SupportedSourceShadow,
    historicalF47AllEdgeFiberMap_support] using hedge

/-- A genuine conditional historical/original-to-independent/native
calibration packet. It requires an ACTUAL original raw F55 3-cell at
exact old F54 source/target routes; an exact old quotient arrow witness;
and a genuinely independent native north C60 F55 raw source with
a PROVED common numerical shadow. These are not manufactured from
the old F47 categorical arrow or from a number. -/
structure LEC13OriginalNativeCalibration
    (B : C60F47SquareFrame α β r s) where
  historicalRaw : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s
  independentRaw : NorthNativeF55Raw
  historicalArrowExact : c60F44OriginalF55Of historicalRaw = B.rotationStep
  commonShadowExact :
    historicalF55CommonReadout historicalRaw =
      nativeNorthF55CommonReadout independentRaw

/-- Under this explicitly supplied actual typed old/native comparison,
the old frame's categorical F55 signed/phase readout agrees with that
genuine independent native raw source. -/
theorem lec13_calibrated_frame_matches_native
    (B : C60F47SquareFrame α β r s)
    (C : LEC13OriginalNativeCalibration B) :
    lec13HistoricalF47F55Shadow B =
      nativeNorthF55CommonReadout C.independentRaw := by
  change
    ((c60F44OriginalF55Eval B.rotationStep).charge,
      (c60F44OriginalF55Eval B.rotationStep).phase) =
      nativeNorthF55CommonReadout C.independentRaw
  rw [← C.historicalArrowExact, c60F44OriginalF55Eval_of]
  exact C.commonShadowExact

/-- The exact source/target, support and native readout remain
distinct fields: no older raw three-cell is reconstructed from a
numerical shadow, no physical Edge is inferred from two source arrows. -/
structure LEC13SupportedOriginalNative
    (B : C60F47SquareFrame α β r s)
    (C : LEC13OriginalNativeCalibration B) where
  originalFrame : HistoricalF47ThreeSourceFiber B
  physicalEdge : Edge
  supportExact : frameKuuEdge originalFrame.1 = physicalEdge
  historicalRawArrowExact :
    c60F44OriginalF55Of C.historicalRaw = originalFrame.1.rotationStep
  nativeShadowExact :
    lec13HistoricalF47F55Shadow originalFrame.1 =
      nativeNorthF55CommonReadout C.independentRaw

/-- Under a TRUE supplied original/native calibration packet, every
actual C60 edge gives a genuinely typed supported comparison packet.
This is *conditional*: nothing here assumes every old F47 frame has
a raw old/native match, which is a separate lifting obligation. -/
def lec13SupportedOriginalNativeAt
    (B : C60F47SquareFrame α β r s)
    (C : LEC13OriginalNativeCalibration B)
    (e : Edge) : LEC13SupportedOriginalNative B C where
  originalFrame := historicalF47AllEdgeFiberMap B e
  physicalEdge := e
  supportExact := historicalF47AllEdgeFiberMap_support B e
  historicalRawArrowExact := by
    simpa only [historicalF47AllEdgeFiberMap_rotation] using
      C.historicalArrowExact
  nativeShadowExact := by
    calc
      lec13HistoricalF47F55Shadow
        (historicalF47AllEdgeFiberMap B e).1 =
          lec13HistoricalF47F55Shadow B :=
        lec13_edge_replacement_preserves_common_shadow B e
      _ = nativeNorthF55CommonReadout C.independentRaw :=
        lec13_calibrated_frame_matches_native B C

/-- The 90 genuine physical-edge choices are distinct even after
retaining the old typed raw proof, the independent native typed raw
proof, the original F42/F55 arrow pair and calibrated common readout. -/
theorem lec13_supported_original_native_injective
    (B : C60F47SquareFrame α β r s)
    (C : LEC13OriginalNativeCalibration B) :
    Function.Injective (lec13SupportedOriginalNativeAt B C) := by
  intro e f h
  exact congrArg (fun W : LEC13SupportedOriginalNative B C =>
    W.physicalEdge) h

/-- The TRUE size of a fiber of supported, same-source,
same-shadow old/native comparison witnesses is at least 90
whenever the original/native calibration itself is supplied. -/
theorem lec13_matched_native_has_ninety_real_supports
    (B : C60F47SquareFrame α β r s)
    (C : LEC13OriginalNativeCalibration B) :
    Fintype.card Edge = 90 ∧
      Function.Injective (lec13SupportedOriginalNativeAt B C) :=
  ⟨historicalF47PhysicalSupport_cardinality,
    lec13_supported_original_native_injective B C⟩

/-- Even with a genuine user-supplied OLD raw F55 source and independent
native raw F55 witness aligned by the actual common shadow, the same
historical source/shadow cannot determine the physical C60 support
edge. Matching source Types does not excuse discarding geometry. -/
theorem lec13_native_matched_source_shadow_no_support_decoder
    (B : C60F47SquareFrame α β r s)
    (C : LEC13OriginalNativeCalibration B) :
    ¬ ∃ recover :
        ((((α ⟶ β) × (r ⟶ s)) × HistoricalNativeF55CommonShadow) ×
          NorthNativeF55Raw) → Edge,
      ∀ e : Edge,
        recover
          (lec13HistoricalF47SourceShadow
            (lec13SupportedOriginalNativeAt B C e).originalFrame.1,
            C.independentRaw) = e := by
  rintro ⟨recover, hrecover⟩
  apply lec13_no_support_decoder_from_original_source_shadow B
  refine ⟨fun z => recover (z, C.independentRaw), ?_⟩
  intro e
  exact hrecover e

#print axioms lec13_edge_replacement_preserves_original_f55
#print axioms lec13_edge_replacement_preserves_original_f42
#print axioms lec13_edge_replacement_preserves_common_shadow
#print axioms lec13_edge_replacement_preserves_source_and_shadow
#print axioms lec13_edge_replacement_support_exact
#print axioms lec13_edge_replacement_two_real_faces
#print axioms lec13_original_source_shadow_not_injective_on_edges
#print axioms lec13_no_support_decoder_from_original_source_shadow
#print axioms lec13_ninety_real_edges_same_historical_source_shadow
#print axioms lec13_supported_source_shadow_edge_exact
#print axioms lec13_supported_source_shadow_injective_on_edges
#print axioms lec13_calibrated_frame_matches_native
#print axioms lec13SupportedOriginalNativeAt
#print axioms lec13_supported_original_native_injective
#print axioms lec13_matched_native_has_ninety_real_supports
#print axioms lec13_native_matched_source_shadow_no_support_decoder

end
end KUOS.LivingEngiHistoricalBridge
