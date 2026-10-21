import KuuOSFormal.HistoricalF36F40BridgeP48

/-!
# F112-P49 — transport actual old C60 paths inside a real F69 face-star

P46 transported the ACTUAL old C60 Quiver.Path category to genuine F69
zigzag localization. P48 certified exact old/native ordered boundary
geometry and physical incidence. Here a face-localized cone identity is
extended from one physical edge to arbitrary original source paths.

Crucially, the original raw source paths are NEVER declared equal to the
independent source zigzags. The old physical F42 face relators must still
be discharged on their genuine original source boundary paths.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- A physical edge inside a true original polygon induces a compatible
one-step forward old-dart incidence span into the polygon after
localization. This is proved through actual native Site arrows. -/
theorem p49_native_forward_edge_cone (e : Edge) (face : Polygon)
    (he : edgeOnFace e face) :
    zigzagToLocalization (historicalNativeEdgeForwardRaw e) ≫
      siteLocalizationQ.map (homOfLE
        (show Site.vertex (edgeEndpoints e).2 ≤ Site.face face from
          le_trans (flag_vertex_edge e true)
            (show Site.edge e ≤ Site.face face from he))) =
      siteLocalizationQ.map (homOfLE
        (show Site.vertex (edgeEndpoints e).1 ≤ Site.face face from
          le_trans (flag_vertex_edge e false)
            (show Site.edge e ≤ Site.face face from he))) := by
  exact p48_localized_incidence_span_cone
    (flag_vertex_edge e false)
    (flag_vertex_edge e true)
    (show Site.edge e ≤ Site.face face from he)

/-- The actual historically reversed edge runs along the opposite
native dart-edge-dart span, with the same genuine physical face. -/
theorem p49_native_reverse_edge_cone (e : Edge) (face : Polygon)
    (he : edgeOnFace e face) :
    zigzagToLocalization (historicalNativeEdgeReverseRaw e) ≫
      siteLocalizationQ.map (homOfLE
        (show Site.vertex (edgeEndpoints e).1 ≤ Site.face face from
          le_trans (flag_vertex_edge e false)
            (show Site.edge e ≤ Site.face face from he))) =
      siteLocalizationQ.map (homOfLE
        (show Site.vertex (edgeEndpoints e).2 ≤ Site.face face from
          le_trans (flag_vertex_edge e true)
            (show Site.edge e ≤ Site.face face from he))) := by
  exact p48_localized_incidence_span_cone
    (flag_vertex_edge e true)
    (flag_vertex_edge e false)
    (show Site.edge e ≤ Site.face face from he)

/-- Both actual source/target old darts of a historical original
quiver arrow on this physical face are genuine native face sites. -/
theorem p49_old_arrow_endpoints_on_face
    {a b : IcosahedralDart} (f : a ⟶ b) (face : Polygon)
    (he : edgeOnFace (p48_originalArrowNativeEdge f) face) :
    dartOnFace (dartEquiv.symm a) face ∧
      dartOnFace (dartEquiv.symm b) face := by
  rcases f with ⟨oriented, ⟨ha, hb⟩⟩
  subst a
  subst b
  cases oriented with
  | forward old =>
      have hp := edgeFace_endpoints (edgeEquiv.symm old) face he
      constructor
      · change dartOnFace
          (dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).1) face
        rw [historicalOldEdgeFirstDart_native]
        exact hp.1
      · change dartOnFace
          (dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).2) face
        rw [historicalOldEdgeSecondDart_native]
        exact hp.2
  | reverse old =>
      have hp := edgeFace_endpoints (edgeEquiv.symm old) face he
      constructor
      · change dartOnFace
          (dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).2) face
        rw [historicalOldEdgeSecondDart_native]
        exact hp.2
      · change dartOnFace
          (dartEquiv.symm (truncatedIcosahedralEdgeEndpoints old).1) face
        rw [historicalOldEdgeFirstDart_native]
        exact hp.1

/-- One genuinely typed OLD original quiver arrow transports its
native face spokes compatibly after localization, with either old
orientation. No fake dart-to-dart arrow is added to Site. -/
theorem p49_old_arrow_localized_cone
    {a b : IcosahedralDart} (f : a ⟶ b) (face : Polygon)
    (he : edgeOnFace (p48_originalArrowNativeEdge f) face)
    (ha : Site.vertex (dartEquiv.symm a) ≤ Site.face face)
    (hb : Site.vertex (dartEquiv.symm b) ≤ Site.face face) :
    historicalOldPathsToLocalization.map f.toPath ≫
      siteLocalizationQ.map (homOfLE hb) =
        siteLocalizationQ.map (homOfLE ha) := by
  rcases f with ⟨oriented, ⟨hsource, htarget⟩⟩
  subst a
  subst b
  cases oriented with
  | forward old =>
      have hnative :=
        p49_native_forward_edge_cone (edgeEquiv.symm old) face he
      change zigzagToLocalization (historicalOldForwardToRaw old) ≫
        siteLocalizationQ.map (homOfLE hb) =
          siteLocalizationQ.map (homOfLE ha)
      cases old with
      | cross oe =>
          cases oe <;>
            simpa [historicalOldForwardToRaw,
              historicalNativeEdgeForwardRaw,
              historicalOldEdgeFirstDart_native,
              historicalOldEdgeSecondDart_native] using hnative
      | around ae =>
          rcases ae with ⟨v, s⟩
          cases v <;> cases s <;>
            simpa [historicalOldForwardToRaw,
              historicalNativeEdgeForwardRaw,
              historicalOldEdgeFirstDart_native,
              historicalOldEdgeSecondDart_native] using hnative
  | reverse old =>
      have hnative :=
        p49_native_reverse_edge_cone (edgeEquiv.symm old) face he
      change zigzagToLocalization (historicalOldReverseToRaw old) ≫
        siteLocalizationQ.map (homOfLE hb) =
          siteLocalizationQ.map (homOfLE ha)
      cases old with
      | cross oe =>
          cases oe <;>
            simpa [historicalOldReverseToRaw,
              historicalNativeEdgeReverseRaw,
              historicalOldEdgeFirstDart_native,
              historicalOldEdgeSecondDart_native] using hnative
      | around ae =>
          rcases ae with ⟨v, s⟩
          cases v <;> cases s <;>
            simpa [historicalOldReverseToRaw,
              historicalNativeEdgeReverseRaw,
              historicalOldEdgeFirstDart_native,
              historicalOldEdgeSecondDart_native] using hnative

/-- The EXISTING P48 old source path incidence certificate is stable
under full nontrivial old Quiver.Path composition, not just one edge. -/
theorem p49_old_path_incidence_comp {a b c : IcosahedralDart}
    (face : Polygon)
    (p : Quiver.Path a b) (q : Quiver.Path b c) :
    p48_originalPathWithinPolygon face (p.comp q) =
      (p48_originalPathWithinPolygon face p &&
        p48_originalPathWithinPolygon face q) := by
  induction q with
  | nil =>
      simp only [Quiver.Path.comp_nil, p48_originalPathWithinPolygon,
        Bool.and_true]
  | cons q f ih =>
      rw [Quiver.Path.comp_cons]
      simpa only [p48_originalPathWithinPolygon, Bool.and_assoc] using
        congrArg (fun x : Bool =>
          x && decide (edgeOnFace (p48_originalArrowNativeEdge f) face)) ih

/-- An original path with actual real polygon boundary incidences
is compatible with the polygon's physical spokes after localization.
The source is the real Quiver.Path, not a replacement raw word. -/
theorem p49_old_path_localized_cone :
    ∀ {a b : IcosahedralDart} (p : Quiver.Path a b)
      (face : Polygon),
      p48_originalPathWithinPolygon face p = true →
      (ha : Site.vertex (dartEquiv.symm a) ≤ Site.face face) →
      (hb : Site.vertex (dartEquiv.symm b) ≤ Site.face face) →
      historicalOldPathsToLocalization.map p ≫
        siteLocalizationQ.map (homOfLE hb) =
          siteLocalizationQ.map (homOfLE ha) := by
  intro a b p
  induction p with
  | nil =>
      intro face hp ha hb
      change zigzagLocalizationFunctor.map
          (𝟙 (historicalOldQuiverToRaw.obj _)) ≫
          siteLocalizationQ.map (homOfLE hb) =
            siteLocalizationQ.map (homOfLE ha)
      rw [zigzagLocalizationFunctor.map_id, Category.id_comp]
      exact congrArg siteLocalizationQ.map (Subsingleton.elim _ _)
  | cons p f ih =>
      intro face hp ha hb
      have hsplit :
          p48_originalPathWithinPolygon face p = true ∧
            decide (edgeOnFace (p48_originalArrowNativeEdge f) face) = true := by
        simpa only [p48_originalPathWithinPolygon,
          Bool.and_eq_true] using hp
      have he : edgeOnFace (p48_originalArrowNativeEdge f) face :=
        of_decide_eq_true hsplit.2
      have hc : Site.vertex (dartEquiv.symm _) ≤ Site.face face :=
        (p49_old_arrow_endpoints_on_face f face he).1
      have h1 := ih face hsplit.1 ha hc
      have h2 := p49_old_arrow_localized_cone f face he hc hb
      rw [← Quiver.Path.comp_toPath_eq_cons,
        historicalOldPaths_localized_comp, Category.assoc, h2]
      exact h1

#print axioms p49_native_forward_edge_cone
#print axioms p49_native_reverse_edge_cone
#print axioms p49_old_arrow_endpoints_on_face
#print axioms p49_old_arrow_localized_cone
#print axioms p49_old_path_incidence_comp
#print axioms p49_old_path_localized_cone

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
