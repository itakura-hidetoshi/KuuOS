import KuuOSFormal.HistoricalF36F40BridgeP43

/-!
# F112-P44 — bidirectional historical/native physical flag correspondence

P43 constructs a genuinely geometric, edge-dependent INJECTION
from ORIGINAL F42 face-side choices to actual independent physical
C60 polygon choices, without assuming that their Bool indices agree.

Both genuine adjacent-face fibres have exactly two elements.
Using mathlib's finite-injective-implies-surjective theorem, we
construct the corresponding real EQUIVALENCE on each edge, and then
a full 360-flag EQUIVALENCE which preserves the actual edge and
endpoint slot. The inverse constructs the ORIGINAL genuinely
endpoint-typed contextual F42 witness with full independent Type-valued
fan/disk evidence from ANY native-indexed physical flag.

The two original/new face-side conventions need not be identical.
No old Quiver.Path ≌ new Zigzag source-category equivalence, global
F54/F55 higher-source equivalence, Beck–Chevalley or obstruction
vanishing is claimed. OLD-SIDE only; independent Kuu roots stay clean.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000
noncomputable section

/-- On every actual physical C60 edge, the proven injective historical
side matching exhausts the two independent native side slots. -/
theorem historicalF42NativeSide_surjective (e : Edge) :
    Function.Surjective (historicalF42NativeSide e) :=
  Finite.surjective_of_injective (historicalF42NativeSide_injective e)

/-- Actual old/native adjacency indices are bijective, not definitionally
or postulated to be the identical Bool convention. -/
theorem historicalF42NativeSide_bijective (e : Edge) :
    Function.Bijective (historicalF42NativeSide e) :=
  ⟨historicalF42NativeSide_injective e,
    historicalF42NativeSide_surjective e⟩

/-- True geometric two-face fibre equivalence over EACH one of 90
C60 physical edges; the equivalence comes from P43's real incidence. -/
def historicalF42SideEquiv (e : Edge) : Bool ≃ Bool :=
  Equiv.ofBijective (historicalF42NativeSide e)
    (historicalF42NativeSide_bijective e)

/-- The forward map of the equivalence is exactly the already proved
original-to-native matching, with no coordinate renaming. -/
theorem historicalF42SideEquiv_apply (e : Edge) (side : Bool) :
    historicalF42SideEquiv e side = historicalF42NativeSide e side := rfl

/-- The real historical face-choice slot is recovered from any native
choice. This is a theorem, rather than a chosen second face. -/
theorem historicalF42SideEquiv_rightInverse (e : Edge) (j : Bool) :
    historicalF42NativeSide e ((historicalF42SideEquiv e).symm j) = j := by
  change historicalF42SideEquiv e
    ((historicalF42SideEquiv e).symm j) = j
  exact (historicalF42SideEquiv e).apply_symm_apply j

/-- Backward followed by forward is identity on the ORIGINAL
historical F42 adjacent-face choices. -/
theorem historicalF42SideEquiv_leftInverse (e : Edge) (side : Bool) :
    (historicalF42SideEquiv e).symm (historicalF42NativeSide e side) =
      side := by
  change (historicalF42SideEquiv e).symm (historicalF42SideEquiv e side) =
    side
  exact (historicalF42SideEquiv e).symm_apply_apply side

/-- ANY independent native adjacent polygon is a real original
historical selected C60 polygon on that exact same physical edge.
The unique historical Bool index is obtained by the proved inverse. -/
theorem historicalF42EveryNativeFace_has_actual_original
    (e : Edge) (nativeSide : Bool) :
    polygonEquiv.symm
        (historicalF42EdgeSelectedFace e
          ((historicalF42SideEquiv e).symm nativeSide)) =
      faceAt e nativeSide := by
  calc
    _ = faceAt e
          (historicalF42NativeSide e
            ((historicalF42SideEquiv e).symm nativeSide)) :=
        historicalF42NativeSide_spec e
          ((historicalF42SideEquiv e).symm nativeSide)
    _ = faceAt e nativeSide := by
      rw [historicalF42SideEquiv_rightInverse]

/-- A fully invertible reindexing of the 360 GENUINE C60 flags,
preserving the physical edge and endpoint bit and changing ONLY the
historical/native physical face-side coordinate via its proven
edge-dependent equivalence. -/
def historicalF42PhysicalFlagReindex :
    (Edge × (Bool × Bool)) ≃ (Edge × (Bool × Bool)) where
  toFun t := (t.1, (t.2.1, historicalF42NativeSide t.1 t.2.2))
  invFun t :=
    (t.1, (t.2.1, (historicalF42SideEquiv t.1).symm t.2.2))
  left_inv := by
    rintro ⟨e, ⟨endpointSide, historicalSide⟩⟩
    change
      (e, (endpointSide,
        (historicalF42SideEquiv e).symm
          (historicalF42NativeSide e historicalSide))) =
      (e, (endpointSide, historicalSide))
    simp only [historicalF42SideEquiv_leftInverse]
  right_inv := by
    rintro ⟨e, ⟨endpointSide, nativeSide⟩⟩
    change
      (e, (endpointSide,
        historicalF42NativeSide e
          ((historicalF42SideEquiv e).symm nativeSide))) =
      (e, (endpointSide, nativeSide))
    simp only [historicalF42SideEquiv_rightInverse]

/-- The 360-flag equivalence cannot alter the physical edge or
the selected genuine endpoint. No artificial Fin 360 labels. -/
theorem historicalF42PhysicalFlagReindex_preserves_edge_endpoint
    (t : Edge × (Bool × Bool)) :
    (historicalF42PhysicalFlagReindex t).1 = t.1 ∧
    (historicalF42PhysicalFlagReindex t).2.1 = t.2.1 :=
  ⟨rfl, rfl⟩

/-- Canonical proof-relevant ORIGINAL contextual face source attached
directly to the NATIVE two-side index of any physical C60 flag. -/
def historicalF42NativeIndexedFlag
    (e : Edge) (endpointSide nativeSide : Bool) :
    HistoricalF42ActualNativeFlag e endpointSide
      ((historicalF42SideEquiv e).symm nativeSide) :=
  historicalF42ActualNativeFlag e endpointSide
    ((historicalF42SideEquiv e).symm nativeSide)

/-- In the native-indexed packet, the original F42 source's native
polygon really equals the independently requested polygon. -/
theorem historicalF42NativeIndexedFlag_face
    (e : Edge) (endpointSide nativeSide : Bool) :
    (historicalF42NativeIndexedFlag e endpointSide nativeSide).physical.nativeFace =
      faceAt e nativeSide := by
  calc
    _ = faceAt e
          (historicalF42NativeSide e
            ((historicalF42SideEquiv e).symm nativeSide)) :=
        historicalF42Flag_native_face_matches e endpointSide
          ((historicalF42SideEquiv e).symm nativeSide)
    _ = faceAt e nativeSide := by
      rw [historicalF42SideEquiv_rightInverse]

/-- The native-indexed original F42 source carries exactly the
independently requested two-arrow genuine C60 incidence flag. -/
theorem historicalF42NativeIndexedFlag_triangle
    (e : Edge) (endpointSide nativeSide : Bool) :
    (historicalF42NativeIndexedFlag e endpointSide nativeSide).nativeFlag =
      flagTriangle e endpointSide nativeSide := by
  calc
    _ = flagTriangle e endpointSide
          (historicalF42NativeSide e
            ((historicalF42SideEquiv e).symm nativeSide)) :=
        (historicalF42NativeIndexedFlag e endpointSide nativeSide).nativeFlag_exact
    _ = flagTriangle e endpointSide nativeSide := by
      rw [historicalF42SideEquiv_rightInverse]

/-- The original complete ordered 5/6-edge word is not lost when
reindexing from the native polygon back to the historical F42 cell. -/
theorem historicalF42NativeIndexedFlag_original_word
    (e : Edge) (endpointSide nativeSide : Bool) :
    (historicalF42NativeIndexedFlag e endpointSide nativeSide).originalF42.originalWords =
      [kernelC60FullFaceBoundaryEdges
        (historicalF42EdgeSelectedFace e
          ((historicalF42SideEquiv e).symm nativeSide))] :=
  (historicalF42Flag_original_source_and_word e endpointSide
    ((historicalF42SideEquiv e).symm nativeSide)).2

/-- ALL 360 genuine native-indexed vertex-edge-face flags have
a direct canonical ORIGINAL proof-relevant contextual F42 source and
the EXACT actual native incidence two-simplex, with no arbitrary
postulated match or new axiom. -/
theorem historicalF42All360_native_indexed_original_sources :
    Fintype.card (Edge × (Bool × Bool)) = 360 ∧
    (∀ t : Edge × (Bool × Bool),
      (historicalF42NativeIndexedFlag t.1 t.2.1 t.2.2).nativeFlag =
        flagTriangle t.1 t.2.1 t.2.2) :=
  ⟨flag_card, fun t =>
    historicalF42NativeIndexedFlag_triangle t.1 t.2.1 t.2.2⟩

#print axioms historicalF42NativeSide_surjective
#print axioms historicalF42NativeSide_bijective
#print axioms historicalF42SideEquiv
#print axioms historicalF42SideEquiv_apply
#print axioms historicalF42SideEquiv_rightInverse
#print axioms historicalF42SideEquiv_leftInverse
#print axioms historicalF42EveryNativeFace_has_actual_original
#print axioms historicalF42PhysicalFlagReindex
#print axioms historicalF42PhysicalFlagReindex_preserves_edge_endpoint
#print axioms historicalF42NativeIndexedFlag
#print axioms historicalF42NativeIndexedFlag_face
#print axioms historicalF42NativeIndexedFlag_triangle
#print axioms historicalF42NativeIndexedFlag_original_word
#print axioms historicalF42All360_native_indexed_original_sources

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
