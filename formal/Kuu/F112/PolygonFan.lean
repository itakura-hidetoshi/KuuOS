import Kuu.F112.PolygonRawLoop

/-!
# F112-D1 / independently typed physical polygon fan 2-sources

For EVERY genuine C60 polygon boundary side, the old-edge span
   vertex(d_i) -> edge(e_i) <- vertex(d_(i+1))
is compared to the distinct original-face span
   vertex(d_i) -> face(p) <- vertex(d_(i+1)).
The comparison is grounded in the TWO genuine incidence triangles
through the same edge and original polygon. It is proved sound in the
actual Gabriel-Zisman F69 localization, rather than postulated through
an evaluator.

The Type-valued witness grammar retains identities, inverse, vertical
pasting and both typed contexts as independent raw proof trees. It does
NOT yet include full polygon-disk filling, original F54 rotation paths,
historical F55 3-cells or a strict 3-category.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

/-- In ANY actual incidence poset, refining a two-leg vertex/edge
span through a common upper cell does not change its interpretation
in the real localization. The three original comparability witnesses
are typed before localization; no Gray evaluator is used. -/
theorem siteSpan_localized {s t u v : Site}
    (a : s ≤ u) (b : t ≤ u) (c : u ≤ v) :
    zigzagToLocalization
      (Zigzag.forward a (Zigzag.backward b (.nil t))) =
    zigzagToLocalization
      (Zigzag.forward (le_trans a c)
        (Zigzag.backward (le_trans b c) (.nil t))) := by
  let B : siteLocalizationQ.obj t ≅ siteLocalizationQ.obj u :=
    Localization.Construction.wIso (W := (⊤ : MorphismProperty Site))
      (homOfLE b) (by trivial)
  let D : siteLocalizationQ.obj t ≅ siteLocalizationQ.obj v :=
    Localization.Construction.wIso (W := (⊤ : MorphismProperty Site))
      (homOfLE (le_trans b c)) (by trivial)
  have hb : D.hom = B.hom ≫ siteLocalizationQ.map (homOfLE c) := by
    change siteLocalizationQ.map (homOfLE (le_trans b c)) =
      siteLocalizationQ.map (homOfLE b) ≫ siteLocalizationQ.map (homOfLE c)
    rw [← siteLocalizationQ.map_comp]
    exact congrArg siteLocalizationQ.map (Subsingleton.elim _ _)
  have ha :
      siteLocalizationQ.map (homOfLE (le_trans a c)) =
        siteLocalizationQ.map (homOfLE a) ≫ siteLocalizationQ.map (homOfLE c) := by
    rw [← siteLocalizationQ.map_comp]
    exact congrArg siteLocalizationQ.map (Subsingleton.elim _ _)
  change siteLocalizationQ.map (homOfLE a) ≫ (B.inv ≫ 𝟙 _) =
    siteLocalizationQ.map (homOfLE (le_trans a c)) ≫ (D.inv ≫ 𝟙 _)
  simp only [Category.comp_id]
  rw [← cancel_mono D.hom]
  calc
    (siteLocalizationQ.map (homOfLE a) ≫ B.inv) ≫ D.hom =
        (siteLocalizationQ.map (homOfLE a) ≫ B.inv) ≫
          (B.hom ≫ siteLocalizationQ.map (homOfLE c)) := by rw [hb]
    _ = siteLocalizationQ.map (homOfLE a) ≫ siteLocalizationQ.map (homOfLE c) := by
      simp only [Category.assoc, B.inv_hom_id, Category.id_comp]
    _ = siteLocalizationQ.map (homOfLE (le_trans a c)) := ha.symm
    _ = (siteLocalizationQ.map (homOfLE (le_trans a c)) ≫ D.inv) ≫ D.hom := by
      rw [Category.assoc, D.inv_hom_id, Category.comp_id]

/-- The genuine face cone span, using the actual same physical polygon
for BOTH end vertices. Its source differs syntactically from the edge
span even though both become equal only in the explicit localization. -/
def polygonConeRawSide (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    Zigzag (Site.vertex (cyclicBoundaryDart p i.val))
      (Site.vertex (cyclicBoundaryDart p (i.val + 1))) :=
  let e := cyclicBoundaryEdge p i.val
  let v := cyclicBoundaryDart p i.val
  let w := cyclicBoundaryDart p (i.val + 1)
  let h := cyclicBoundarySide_real p i hi
  .forward (le_trans (edgeJoins_start e v w h.1) h.2.1)
    (.backward (le_trans (edgeJoins_finish e v w h.1) h.2.1) (.nil _))

/-- A real physical fan sector: equality of localized edge-span and
face-span is proved from the ORIGINAL poset triangles, not inserted as
an arbitrary congruence. -/
theorem polygonFanSector_localized (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    zigzagToLocalization (polygonRawSide p i hi) =
      zigzagToLocalization (polygonConeRawSide p i hi) := by
  let e := cyclicBoundaryEdge p i.val
  let v := cyclicBoundaryDart p i.val
  let w := cyclicBoundaryDart p (i.val + 1)
  have h := cyclicBoundarySide_real p i hi
  change
    zigzagToLocalization
      (.forward (edgeJoins_start e v w h.1)
        (.backward (edgeJoins_finish e v w h.1) (.nil _))) =
    zigzagToLocalization
      (.forward (le_trans (edgeJoins_start e v w h.1) h.2.1)
        (.backward (le_trans (edgeJoins_finish e v w h.1) h.2.1) (.nil _)))
  exact siteSpan_localized (edgeJoins_start e v w h.1)
    (edgeJoins_finish e v w h.1) h.2.1

/-- The exact proven kernel, not a newly guessed equivalence. -/
theorem polygonFanSector_kernel (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    zigzagKernelQ.map (polygonRawSide p i hi) =
      zigzagKernelQ.map (polygonConeRawSide p i hi) :=
  (zigzagKernel_exact _ _).2 (polygonFanSector_localized p i hi)

/-- NEW proof-relevant physical F42 fan syntax, distinguished from the
old F42 fully glued polygon disk. Endpoints and whiskering are typed. -/
inductive PolygonFanRewrite :
    {s t : Site} → Zigzag s t → Zigzag s t → Type where
  | ident {s t : Site} (q : Zigzag s t) : PolygonFanRewrite q q
  | sector (p : Polygon) (i : Fin 6) (hi : i.val < polygonSideCount p) :
      PolygonFanRewrite (polygonRawSide p i hi) (polygonConeRawSide p i hi)
  | inverse {s t : Site} {q r : Zigzag s t}
      (z : PolygonFanRewrite q r) : PolygonFanRewrite r q
  | vertical {s t : Site} {q r u : Zigzag s t}
      (z : PolygonFanRewrite q r) (w : PolygonFanRewrite r u) :
      PolygonFanRewrite q u
  | leftContext {r s t : Site} (h : Zigzag r s)
      {q u : Zigzag s t} (z : PolygonFanRewrite q u) :
      PolygonFanRewrite (append h q) (append h u)
  | rightContext {r s t : Site}
      {q u : Zigzag r s} (z : PolygonFanRewrite q u) (h : Zigzag s t) :
      PolygonFanRewrite (append q h) (append u h)

/-- By structural recursion on the actual Type-valued 2-cell source,
all generated pastings are sound in the original F69 localization. -/
theorem PolygonFanRewrite.localized_sound
    {s t : Site} {q r : Zigzag s t} (z : PolygonFanRewrite q r) :
    zigzagToLocalization q = zigzagToLocalization r := by
  induction z with
  | ident q => rfl
  | sector p i hi => exact polygonFanSector_localized p i hi
  | inverse z ih => exact ih.symm
  | vertical z w ihz ihw => exact ihz.trans ihw
  | leftContext h z ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => zigzagToLocalization h ≫ x) ih
  | rightContext z h ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => x ≫ zigzagToLocalization h) ih

theorem PolygonFanRewrite.kernel_sound
    {s t : Site} {q r : Zigzag s t} (z : PolygonFanRewrite q r) :
    zigzagKernelQ.map q = zigzagKernelQ.map r :=
  (zigzagKernel_exact q r).2 z.localized_sound

/-- Canonical physical face-sector proof term (not just the proposition
that its two raw words become equal). -/
def polygonFanSector (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    PolygonFanRewrite (polygonRawSide p i hi) (polygonConeRawSide p i hi) :=
  .sector p i hi

def polygonFanSectorWithUnit (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    PolygonFanRewrite (polygonRawSide p i hi) (polygonConeRawSide p i hi) :=
  .vertical (.ident (polygonRawSide p i hi)) (.sector p i hi)

/-- Proof relevance is kept: direct and unit-prefixed 2-source trees are
not definitionally or propositionally identified. -/
theorem polygonFanSector_ne_withUnit (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    polygonFanSector p i hi ≠ polygonFanSectorWithUnit p i hi := by
  intro h
  cases h

#print axioms siteSpan_localized
#print axioms polygonConeRawSide
#print axioms polygonFanSector_localized
#print axioms polygonFanSector_kernel
#print axioms PolygonFanRewrite.localized_sound
#print axioms PolygonFanRewrite.kernel_sound
#print axioms polygonFanSector_ne_withUnit
end
end Kuu.F112.Physical
