import Kuu.F112.PolygonRotationSound

/-!
# F112-E3 / proof-carrying original C60 rotation basepoint transport

Changing from the kth actual polygon dart to the lth is realized by
the ORIGINAL oriented boundary subpath, not by an invented direct
incidence or by changing a Boolean proxy label.

We show functorial identity/composition only in the stated physical
Gabriel-Zisman localization and its exact kernel quotient. We do
not identify distinct unquotiented raw words or assume the historical
F54 original higher composition laws.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000
noncomputable section

/-- The actual contiguous original F69 word from dart k to dart l,
with k <= l and both in the genuine polygon boundary. -/
def polygonRotationTransport (p : Polygon) (k l : Nat)
    (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
    Zigzag (Site.vertex (cyclicBoundaryDart p k))
      (Site.vertex (cyclicBoundaryDart p l)) := by
  have hs : k + (l - k) = l := Nat.add_sub_of_le hkl
  have hbound : k + (l - k) ≤ polygonSideCount p := by
    rw [hs]
    exact hl
  exact changeZigzagTarget
    (congrArg (fun j => Site.vertex (cyclicBoundaryDart p j)) hs)
    (polygonRawSegment p k (l - k) hbound)

/-- Rotation-basepoint transport has two UNCOLLAPSED raw
incidence legs per actual physical boundary edge. -/
theorem polygonRotationTransport_legCount (p : Polygon) (k l : Nat)
    (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
    zigzagLegCount (polygonRotationTransport p k l hkl hl) =
      2 * (l - k) := by
  unfold polygonRotationTransport
  rw [zigzagLegCount_transport]
  exact polygonRawSegment_legCount p k (l - k) (by
    rw [Nat.add_sub_of_le hkl]
    exact hl)

/-- The actual physical boundary transport is localizable to the
same REAL face-cone between its two endpoints. -/
theorem polygonRotationTransport_cone_sound (p : Polygon) (k l : Nat)
    (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
    zigzagToLocalization (polygonRotationTransport p k l hkl hl) =
      zigzagToLocalization
        (polygonConeBetween p k l (Nat.le_trans hkl hl) hl) := by
  have hs : k + (l - k) = l := Nat.add_sub_of_le hkl
  have hb : k + (l - k) ≤ polygonSideCount p :=
    le_trans (le_of_eq hs) hl
  have hc :
      Site.vertex (cyclicBoundaryDart p (k + (l - k))) =
        Site.vertex (cyclicBoundaryDart p l) :=
    congrArg (fun j => Site.vertex (cyclicBoundaryDart p j)) hs
  calc
    zigzagToLocalization (polygonRotationTransport p k l hkl hl) =
        zigzagToLocalization
          (changeZigzagTarget hc (polygonRawSegment p k (l - k) hb)) := by
            rfl
    _ = zigzagToLocalization
          (changeZigzagTarget hc
            (polygonConeBetween p k (k + (l - k))
              (Nat.le_trans hkl hl) hb)) := by
          rw [changeZigzagTarget_localized,
            changeZigzagTarget_localized,
            polygonRawSegment_cone_sound p k
              (Nat.le_trans hkl hl) (l - k) hb]
    _ = zigzagToLocalization
          (polygonConeBetween p k l (Nat.le_trans hkl hl) hl) :=
        congrArg zigzagToLocalization
          (siteSpan_target_cast_eq hc
            (cyclicDart_le_face p k (Nat.le_trans hkl hl))
            (cyclicDart_le_face p (k + (l - k)) hb)
            (cyclicDart_le_face p l hl))

/-- The 0-length rotation is genuinely the local ID; we do not
postulate it as a new law of the raw path constructors. -/
theorem polygonRotationTransport_id_localized (p : Polygon)
    (k : Nat) (hk : k ≤ polygonSideCount p) :
    zigzagToLocalization
      (polygonRotationTransport p k k (Nat.le_refl _) hk) = 𝟙 _ := by
  rw [polygonRotationTransport_cone_sound]
  change
    zigzagToLocalization
      (.forward (cyclicDart_le_face p k hk)
        (.backward (cyclicDart_le_face p k hk) (.nil _))) = 𝟙 _
  exact siteSpan_same_localized (cyclicDart_le_face p k hk)

/-- Two successive REAL boundary basepoint changes agree with
the single longer original boundary change after localization.
This is a proved physical-face telescope, not an axiom of exchange. -/
theorem polygonRotationTransport_comp_localized (p : Polygon)
    (k l m : Nat) (hkl : k ≤ l) (hlm : l ≤ m)
    (hm : m ≤ polygonSideCount p) :
    zigzagToLocalization
      (append
        (polygonRotationTransport p k l hkl (Nat.le_trans hlm hm))
        (polygonRotationTransport p l m hlm hm)) =
      zigzagToLocalization
        (polygonRotationTransport p k m (Nat.le_trans hkl hlm) hm) := by
  rw [zigzagToLocalization_append,
    polygonRotationTransport_cone_sound,
    polygonRotationTransport_cone_sound,
    polygonRotationTransport_cone_sound]
  change
    zigzagToLocalization
      (.forward (cyclicDart_le_face p k (Nat.le_trans hkl (Nat.le_trans hlm hm)))
        (.backward (cyclicDart_le_face p l (Nat.le_trans hlm hm)) (.nil _))) ≫
    zigzagToLocalization
      (.forward (cyclicDart_le_face p l (Nat.le_trans hlm hm))
        (.backward (cyclicDart_le_face p m hm) (.nil _))) =
    zigzagToLocalization
      (.forward (cyclicDart_le_face p k (Nat.le_trans (Nat.le_trans hkl hlm) hm))
        (.backward (cyclicDart_le_face p m hm) (.nil _)))
  simpa only [zigzagToLocalization_append] using
    siteSpan_telescope_localized
      (cyclicDart_le_face p k (Nat.le_trans hkl (Nat.le_trans hlm hm)))
      (cyclicDart_le_face p l (Nat.le_trans hlm hm))
      (cyclicDart_le_face p m hm)

/-- Exact quotient coherence follows from the *proved* original
localization transport composition, not a coarser evaluator. -/
theorem polygonRotationTransport_comp_kernel (p : Polygon)
    (k l m : Nat) (hkl : k ≤ l) (hlm : l ≤ m)
    (hm : m ≤ polygonSideCount p) :
    zigzagKernelQ.map
      (append
        (polygonRotationTransport p k l hkl (Nat.le_trans hlm hm))
        (polygonRotationTransport p l m hlm hm)) =
    zigzagKernelQ.map
      (polygonRotationTransport p k m (Nat.le_trans hkl hlm) hm) :=
  (zigzagKernel_exact _ _).2
    (polygonRotationTransport_comp_localized p k l m hkl hlm hm)

#print axioms polygonRotationTransport
#print axioms polygonRotationTransport_legCount
#print axioms polygonRotationTransport_cone_sound
#print axioms polygonRotationTransport_id_localized
#print axioms polygonRotationTransport_comp_localized
#print axioms polygonRotationTransport_comp_kernel
end
end Kuu.F112.Physical
