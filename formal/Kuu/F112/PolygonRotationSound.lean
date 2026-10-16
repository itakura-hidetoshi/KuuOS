import Kuu.F112.PolygonRotation

/-!
# F112-E2 / genuine cyclic rotation soundness and Type-valued 2-sources

For every actual C60 pentagon/hexagon and each certified cyclic base
dart, its raw rotated boundary word localizes to the identity. The proof
is NOT an observation axiom: it is derived by real original Site arrows
to the same physical polygon, a dependent arbitrary-length segment
induction and the localization inverse/face-spoke telescope.

The raw ten-or-twelve-leg rotated path is distinct from nil. Rotation proof
terms remain Type-valued and support inverse, composition, and typed
contexts. The historical original F54 and F55 3-cell presentations,
interchange and phase/charge obstructions are not silently imported.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000
noncomputable section

/-- The original geometric cone from any certified boundary dart to
any other through the SAME real polygon site. -/
def polygonConeBetween (p : Polygon) (start stop : Nat)
    (hs : start ≤ polygonSideCount p) (ht : stop ≤ polygonSideCount p) :
    Zigzag (Site.vertex (cyclicBoundaryDart p start))
      (Site.vertex (cyclicBoundaryDart p stop)) :=
  .forward (cyclicDart_le_face p start hs)
    (.backward (cyclicDart_le_face p stop ht) (.nil _))

/-- ALL real physical subsegments, not only those starting at dart zero,
are sound with respect to their original polygon face-cone in the
genuine F69 localization. -/
theorem polygonRawSegment_cone_sound (p : Polygon) (start : Nat)
    (hs : start ≤ polygonSideCount p) :
    ∀ (k : Nat) (hsk : start + k ≤ polygonSideCount p),
      zigzagToLocalization (polygonRawSegment p start k hsk) =
        zigzagToLocalization
          (polygonConeBetween p start (start + k) hs hsk) := by
  intro k
  induction k with
  | zero =>
      intro hsk
      have hproof :
          cyclicDart_le_face p start hsk =
            cyclicDart_le_face p start hs := Subsingleton.elim _ _
      change (𝟙 _) =
        zigzagToLocalization
          (.forward (cyclicDart_le_face p start hs)
            (.backward (cyclicDart_le_face p start hsk) (.nil _)))
      rw [hproof]
      exact (siteSpan_same_localized (cyclicDart_le_face p start hs)).symm
  | succ k ih =>
      intro hsk
      have hlt : start + k < polygonSideCount p :=
        Nat.lt_of_succ_le hsk
      have hk' : start + k ≤ polygonSideCount p := Nat.le_of_lt hlt
      have hn : polygonSideCount p ≤ 6 := by
        cases p <;> simp [polygonSideCount]
      let i : Fin 6 := ⟨start + k, Nat.lt_of_lt_of_le hlt hn⟩
      have hi : i.val < polygonSideCount p := hlt
      change
        zigzagToLocalization
          (append (polygonRawSegment p start k hk') (polygonRawSide p i hi)) =
        zigzagToLocalization
          (polygonConeBetween p start (start + (k + 1)) hs hsk)
      rw [zigzagToLocalization_append, ih hk',
        polygonFanSector_localized p i hi,
        polygonConeRawSide_eq_span p i hi]
      change
        zigzagToLocalization
          (.forward (cyclicDart_le_face p start hs)
            (.backward (cyclicDart_le_face p (start + k) hk') (.nil _))) ≫
        zigzagToLocalization
          (.forward (cyclicDart_le_face p (start + k) hk')
            (.backward (cyclicDart_le_face p (start + (k + 1)) hsk) (.nil _))) =
        zigzagToLocalization
          (.forward (cyclicDart_le_face p start hs)
            (.backward (cyclicDart_le_face p (start + (k + 1)) hsk) (.nil _)))
      simpa only [zigzagToLocalization_append] using
        siteSpan_telescope_localized
          (cyclicDart_le_face p start hs)
          (cyclicDart_le_face p (start + k) hk')
          (cyclicDart_le_face p (start + (k + 1)) hsk)

/-- A typed target site renaming of a real two-arrow face-cone
produces EXACTLY the corresponding real face-cone word; no quotient
and no equality of distinct original sites is postulated. -/
theorem siteSpan_target_cast_eq {s t u v : Site}
    (ht : t = u) (a : s ≤ v) (b : t ≤ v) (c : u ≤ v) :
    changeZigzagTarget ht
      (Zigzag.forward a (Zigzag.backward b (.nil t))) =
      Zigzag.forward a (Zigzag.backward c (.nil u)) := by
  cases ht
  rfl

/-- After traversing the actual suffix, its endpoint is the original
first dart, so its localized image is the same real face-cone
from the rotated basepoint to that first dart. -/
theorem polygonRotationTail_cone_sound (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    zigzagToLocalization (polygonRotationTail p k hk) =
      zigzagToLocalization
        (polygonConeBetween p k 0 hk (Nat.zero_le _)) := by
  have hsum : k + (polygonSideCount p - k) = polygonSideCount p :=
    Nat.add_sub_of_le hk
  have hbound : k + (polygonSideCount p - k) ≤ polygonSideCount p :=
    le_of_eq hsum
  have hclose :
      Site.vertex (cyclicBoundaryDart p (k + (polygonSideCount p - k))) =
        Site.vertex (cyclicBoundaryDart p 0) :=
    congrArg Site.vertex
      ((congrArg (cyclicBoundaryDart p) hsum).trans (cyclicBoundary_closed p))
  calc
    zigzagToLocalization (polygonRotationTail p k hk) =
      zigzagToLocalization
        (changeZigzagTarget hclose
          (polygonRawSegment p k (polygonSideCount p - k) hbound)) := by
        rfl
    _ = zigzagToLocalization
          (changeZigzagTarget hclose
            (polygonConeBetween p k (k + (polygonSideCount p - k)) hk hbound)) := by
          rw [changeZigzagTarget_localized,
            changeZigzagTarget_localized,
            polygonRawSegment_cone_sound p k hk
              (polygonSideCount p - k) hbound]
    _ = zigzagToLocalization
          (polygonConeBetween p k 0 hk (Nat.zero_le _)) :=
      congrArg zigzagToLocalization
        (siteSpan_target_cast_eq hclose
          (cyclicDart_le_face p k hk)
          (cyclicDart_le_face p (k + (polygonSideCount p - k)) hbound)
          (cyclicDart_le_face p 0 (Nat.zero_le _)))

/-- A genuine cyclic rotation of the original five/six-edge boundary
is an IDENTITY only AFTER the actual F69 localization. -/
theorem polygonRotatedRawLoop_localized_id (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    zigzagToLocalization (polygonRotatedRawLoop p k hk) = 𝟙 _ := by
  unfold polygonRotatedRawLoop
  rw [zigzagToLocalization_append]
  rw [polygonRotationTail_cone_sound p k hk,
      polygonRawPrefix_cone_sound p k hk]
  let a := cyclicDart_le_face p k hk
  let b := cyclicDart_le_face p 0 (Nat.zero_le _)
  change
    zigzagToLocalization
        (.forward a (.backward b (.nil _))) ≫
      zigzagToLocalization
        (.forward b (.backward a (.nil _))) = 𝟙 _
  calc
    _ = zigzagToLocalization
          (append
            (.forward a (.backward b (.nil _)))
            (.forward b (.backward a (.nil _)))) :=
      (zigzagToLocalization_append _ _).symm
    _ = zigzagToLocalization
          (.forward a (.backward a (.nil _))) :=
      siteSpan_telescope_localized a b a
    _ = 𝟙 _ := siteSpan_same_localized a

/-- Exact source kernel quotient agrees with that proven
localization cancellation and DOES NOT identify unquotiented words. -/
theorem polygonRotatedRawLoop_kernel_id (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    zigzagKernelQ.map (polygonRotatedRawLoop p k hk) =
      zigzagKernelQ.map
        (Zigzag.nil (Site.vertex (cyclicBoundaryDart p k))) := by
  apply (zigzagKernel_exact _ _).2
  simpa only [zigzagToLocalization] using
    polygonRotatedRawLoop_localized_id p k hk

/-- NEW, freely presented Type-valued cyclic rotation 2-source;
each actual basepoint is correctly typed in both boundaries. -/
inductive PolygonRotationRewrite :
    {s t : Site} → Zigzag s t → Zigzag s t → Type where
  | ident {s t : Site} (q : Zigzag s t) : PolygonRotationRewrite q q
  | physicalRotation (p : Polygon) (k : Nat)
      (hk : k ≤ polygonSideCount p) :
      PolygonRotationRewrite (polygonRotatedRawLoop p k hk)
        (Zigzag.nil (Site.vertex (cyclicBoundaryDart p k)))
  | inverse {s t : Site} {q r : Zigzag s t}
      (c : PolygonRotationRewrite q r) : PolygonRotationRewrite r q
  | vertical {s t : Site} {q r u : Zigzag s t}
      (c : PolygonRotationRewrite q r)
      (d : PolygonRotationRewrite r u) : PolygonRotationRewrite q u
  | leftContext {r s t : Site} (h : Zigzag r s)
      {q u : Zigzag s t} (c : PolygonRotationRewrite q u) :
      PolygonRotationRewrite (append h q) (append h u)
  | rightContext {r s t : Site}
      {q u : Zigzag r s} (c : PolygonRotationRewrite q u) (h : Zigzag s t) :
      PolygonRotationRewrite (append q h) (append u h)

/-- The free raw higher source is interpreted soundly in the EXACT
physical localization by induction, not by a stipulated evaluator. -/
theorem PolygonRotationRewrite.localized_sound
    {s t : Site} {q r : Zigzag s t} (c : PolygonRotationRewrite q r) :
    zigzagToLocalization q = zigzagToLocalization r := by
  induction c with
  | ident q => rfl
  | physicalRotation p k hk =>
      simpa only [zigzagToLocalization] using
        polygonRotatedRawLoop_localized_id p k hk
  | inverse c ih => exact ih.symm
  | vertical c d ihc ihd => exact ihc.trans ihd
  | leftContext h c ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => zigzagToLocalization h ≫ x) ih
  | rightContext c h ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => x ≫ zigzagToLocalization h) ih

theorem PolygonRotationRewrite.kernel_sound
    {s t : Site} {q r : Zigzag s t} (c : PolygonRotationRewrite q r) :
    zigzagKernelQ.map q = zigzagKernelQ.map r :=
  (zigzagKernel_exact q r).2 c.localized_sound

def polygonRotationWitness (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    PolygonRotationRewrite (polygonRotatedRawLoop p k hk)
      (Zigzag.nil (Site.vertex (cyclicBoundaryDart p k))) :=
  .physicalRotation p k hk

def polygonRotationWitnessWithUnit (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    PolygonRotationRewrite (polygonRotatedRawLoop p k hk)
      (Zigzag.nil (Site.vertex (cyclicBoundaryDart p k))) :=
  .vertical (.ident (polygonRotatedRawLoop p k hk))
    (.physicalRotation p k hk)

/-- Original higher proof trees are distinguishable even if their
image in the exact localization kernel is the same equality. -/
theorem polygonRotationWitness_ne_withUnit (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    polygonRotationWitness p k hk ≠
      polygonRotationWitnessWithUnit p k hk := by
  intro h
  cases h

#print axioms polygonRawSegment_cone_sound
#print axioms siteSpan_target_cast_eq
#print axioms polygonRotationTail_cone_sound
#print axioms polygonRotatedRawLoop_localized_id
#print axioms polygonRotatedRawLoop_kernel_id
#print axioms PolygonRotationRewrite.localized_sound
#print axioms PolygonRotationRewrite.kernel_sound
#print axioms polygonRotationWitness_ne_withUnit
end
end Kuu.F112.Physical
