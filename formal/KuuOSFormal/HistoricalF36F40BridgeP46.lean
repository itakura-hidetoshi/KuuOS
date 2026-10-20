import KuuOSFormal.HistoricalF36F40BridgeP45
import Kuu.F112.KernelEquivalence

/-!
# F112-P46 — actual historical C60 free paths into independent F69

The OLD C60 sixty-dart quiver (F41/F109) has two genuine arrows
for each of the 90 actual truncated-icosahedral edges. The independent
native C60 physical incidence Site is not that old quiver: it has only
dart→edge and edge→polygon arrows, and no dart→dart arrow.

Instead of inventing false incidence arrows, each OLD ORIENTED physical
edge is transported to a genuine *two-leg zigzag*

  old dart a -> native physical edge e <- old dart b,

with a proof of BOTH original/native endpoint correspondences.
The historical reverse edge uses the opposite two-leg traversal, not
an asserted inverse equality in raw Zigzag.

By Mathlib Paths.lift, this genuine quiver map extends to ALL ORIGINAL
Quiver.Path words, preserves original endpoints, identities and arbitrary
composition, and then lands in the actual F69 Gabriel–Zisman localization
by the already verified zigzagLocalizationFunctor. The exact kernel
quotient also receives an honest functor.

The old Gray phase and F42 proof-tree are NOT inferred from equality of
the localized images. This is a global 0/1-source functor, not an F42
2-functor, a proof of source-faithfulness, or a restoration of F54/F55.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000
noncomputable section

/-- The real forward old C60 physical edge does not become a false
dart-to-dart morphism in the original native incidence category:
it is a two-step formally reversible zigzag through its true edge. -/
def historicalNativeEdgeForwardRaw (e : Edge) :
    Zigzag (Site.vertex (edgeEndpoints e).1)
      (Site.vertex (edgeEndpoints e).2) :=
  Zigzag.forward (flag_vertex_edge e false)
    (Zigzag.backward (flag_vertex_edge e true) (.nil _))

/-- The original reverse physical arrow traverses the SAME actual
edge using reversed order of the two real physical dart endpoint legs. -/
def historicalNativeEdgeReverseRaw (e : Edge) :
    Zigzag (Site.vertex (edgeEndpoints e).2)
      (Site.vertex (edgeEndpoints e).1) :=
  Zigzag.forward (flag_vertex_edge e true)
    (Zigzag.backward (flag_vertex_edge e false) (.nil _))

/-- Recover native FIRST dart endpoint of every old physical C60 edge
by the explicit F112 original/native geometric equivalence. -/
theorem historicalOldEdgeFirstDart_native
    (old : TruncatedIcosahedralEdge) :
    dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).1 =
      (edgeEndpoints (edgeEquiv.symm old)).1 := by
  have h := congrArg dartEquiv.symm
    (edgeEndpoints_equiv (edgeEquiv.symm old)).1
  simpa only [edgeEquiv.apply_symm_apply,
    dartEquiv.symm_apply_apply] using h

/-- The corresponding SECOND ordered dart endpoint is also recovered. -/
theorem historicalOldEdgeSecondDart_native
    (old : TruncatedIcosahedralEdge) :
    dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).2 =
      (edgeEndpoints (edgeEquiv.symm old)).2 := by
  have h := congrArg dartEquiv.symm
    (edgeEndpoints_equiv (edgeEquiv.symm old)).2
  simpa only [edgeEquiv.apply_symm_apply,
    dartEquiv.symm_apply_apply] using h

/-- A genuinely typed old FORWARD generator transported to its physical
native two-leg zigzag, including old-to-native endpoint matching. -/
def historicalOldForwardToRaw (old : TruncatedIcosahedralEdge) :
    Zigzag (Site.vertex
      (dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).1))
      (Site.vertex
      (dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).2)) := by
  rw [historicalOldEdgeFirstDart_native,
    historicalOldEdgeSecondDart_native]
  exact historicalNativeEdgeForwardRaw (edgeEquiv.symm old)

/-- The reversed old generator likewise has exactly the reversed
two native dart endpoints and no raw backtrack cancellation. -/
def historicalOldReverseToRaw (old : TruncatedIcosahedralEdge) :
    Zigzag (Site.vertex
      (dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).2))
      (Site.vertex
      (dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).1)) := by
  rw [historicalOldEdgeSecondDart_native,
    historicalOldEdgeFirstDart_native]
  exact historicalNativeEdgeReverseRaw (edgeEquiv.symm old)

/-- Interpret EVERY genuine F41 original oriented C60 quiver arrow.
The original arrow explicitly contains a genuine physical edge code
and BOTH proofs of its old source/target; no arbitrary target is chosen. -/
def historicalOldArrowToRaw {a b : IcosahedralDart} (f : a ⟶ b) :
    Zigzag (Site.vertex (dartEquiv.symm a))
      (Site.vertex (dartEquiv.symm b)) := by
  rcases f with ⟨f, ⟨ha, hb⟩⟩
  subst a
  subst b
  cases f with
  | forward old => exact historicalOldForwardToRaw old
  | reverse old => exact historicalOldReverseToRaw old

/-- True old C60 60-dart/180-oriented-edge quiver prefunctor into
the INDEPENDENT genuine F69 raw zigzag category. -/
def historicalOldQuiverToRaw : IcosahedralDart ⥤q ZigzagSite where
  obj a := ⟨Site.vertex (dartEquiv.symm a)⟩
  map := fun {_ _} f => historicalOldArrowToRaw f

/-- Mathlib's free-path universal property transports ARBITRARILY long
original genuine C60 Quiver.Path words with their actual endpoints. -/
def historicalOldPathsToRaw : Paths IcosahedralDart ⥤ ZigzagSite :=
  Paths.lift historicalOldQuiverToRaw

/-- The global old Quiver.Path interpretation in genuine independent
F69 Gabriel–Zisman physical localization, not in original Site. -/
def historicalOldPathsToLocalization :
    Paths IcosahedralDart ⥤ PhysicalLocalization :=
  historicalOldPathsToRaw ⋙ zigzagLocalizationFunctor

/-- The same old genuine path source has an actual functor into
the exactly verified F69 localization-kernel quotient. -/
def historicalOldPathsToKernel :
    Paths IcosahedralDart ⥤ ZigzagKernelQuotient :=
  historicalOldPathsToRaw ⋙ zigzagKernelQ

/-- An original OLD path and its translated native raw zigzag carry
the SAME actual independently transported vertex endpoints. -/
theorem historicalOldPaths_source_target (a : IcosahedralDart) :
    (historicalOldPathsToRaw.obj (a : Paths IcosahedralDart)).site =
      Site.vertex (dartEquiv.symm a) := rfl

/-- No original source dart is collapsed to another independent native
site by the new global path transport. -/
theorem historicalOldPaths_objects_injective :
    Function.Injective historicalOldPathsToRaw.obj := by
  intro a b h
  have hs := congrArg ZigzagSite.site h
  change Site.vertex (dartEquiv.symm a) =
    Site.vertex (dartEquiv.symm b) at hs
  exact dartEquiv.symm.injective (Site.vertex.inj hs)

/-- Original OLD free paths have exactly functorial composition in the
native raw zigzag category; no raw inverse relation is postulated. -/
theorem historicalOldPaths_raw_comp
    {a b c : IcosahedralDart}
    (p : Quiver.Path a b) (q : Quiver.Path b c) :
    historicalOldPathsToRaw.map (p.comp q) =
      append (historicalOldPathsToRaw.map p)
        (historicalOldPathsToRaw.map q) :=
  historicalOldPathsToRaw.map_comp p q

/-- The same actual OLD path composition respects all native F69
localized incidence relations through the honest Mathlib functor. -/
theorem historicalOldPaths_localized_comp
    {a b c : IcosahedralDart}
    (p : Quiver.Path a b) (q : Quiver.Path b c) :
    historicalOldPathsToLocalization.map (p.comp q) =
      historicalOldPathsToLocalization.map p ≫
        historicalOldPathsToLocalization.map q :=
  historicalOldPathsToLocalization.map_comp p q

/-- The raw and localized old-path maps agree on EVERY path by
the exact F69 zigzag localization, not merely on chosen endpoints. -/
theorem historicalOldPaths_localized_factor
    {a b : IcosahedralDart} (p : Quiver.Path a b) :
    historicalOldPathsToLocalization.map p =
      zigzagToLocalization (historicalOldPathsToRaw.map p) := rfl

/-- The image of the F109 already constructed genuine original
source path exists for EVERY PAIR of actual C60 darts. -/
theorem historicalF109AllDarts_native_raw_nonempty
    (a b : IcosahedralDart) :
    Nonempty (Zigzag (Site.vertex (dartEquiv.symm a))
        (Site.vertex (dartEquiv.symm b))) :=
  ⟨historicalOldPathsToRaw.map (c60F109EveryDartToDart a b)⟩

/-- Original F109 genuine two-endpoint paths retain their exact native
localization arrow; this does not assert any equivalence of raw words. -/
theorem historicalF109AllDarts_native_localization_nonempty
    (a b : IcosahedralDart) :
    Nonempty
      (siteLocalizationQ.obj (Site.vertex (dartEquiv.symm a)) ⟶
        siteLocalizationQ.obj (Site.vertex (dartEquiv.symm b))) :=
  ⟨historicalOldPathsToLocalization.map
    (c60F109EveryDartToDart a b)⟩

/-- A two-leg genuine physical old-edge excursion never becomes raw nil;
a relation may appear only after the specified localization. -/
theorem historicalNativeForwardReverse_raw_ne_nil (e : Edge) :
    append (historicalNativeEdgeForwardRaw e)
      (historicalNativeEdgeReverseRaw e) ≠
        Zigzag.nil (Site.vertex (edgeEndpoints e).1) := by
  intro h
  cases h

#print axioms historicalNativeEdgeForwardRaw
#print axioms historicalNativeEdgeReverseRaw
#print axioms historicalOldEdgeFirstDart_native
#print axioms historicalOldEdgeSecondDart_native
#print axioms historicalOldForwardToRaw
#print axioms historicalOldReverseToRaw
#print axioms historicalOldArrowToRaw
#print axioms historicalOldQuiverToRaw
#print axioms historicalOldPathsToRaw
#print axioms historicalOldPathsToLocalization
#print axioms historicalOldPathsToKernel
#print axioms historicalOldPaths_source_target
#print axioms historicalOldPaths_objects_injective
#print axioms historicalOldPaths_raw_comp
#print axioms historicalOldPaths_localized_comp
#print axioms historicalOldPaths_localized_factor
#print axioms historicalF109AllDarts_native_raw_nonempty
#print axioms historicalF109AllDarts_native_localization_nonempty
#print axioms historicalNativeForwardReverse_raw_ne_nil

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
