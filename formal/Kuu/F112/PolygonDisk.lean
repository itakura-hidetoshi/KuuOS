import Kuu.F112.PolygonFan

/-!
# F112-D2 / polygon fan telescoping and genuine localized disk soundness

The independent proof-relevant sector source of F112-D1 is extended
over the entire REAL five/six-sided C60 polygon boundary. A common
physical face provides a genuine incidence spoke for every cyclic dart.
The comparison of adjacent spans telescopes in the Gabriel-Zisman
localization, proving that the WHOLE 10/12-leg raw loop localizes to id.

A NEW Type-valued face-disk constructor is licensed by that proved
equation; it does not claim to be identical to legacy F42 original
3-cell or an already-proved global strict 3-category. All raw loops
remain syntactically nonempty by polygonRawLoop_ne_nil.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000
noncomputable section

/-- Computable physical dart-on-original-face incidence (not an
assumed star relation). -/
instance dartOnFace_decidable (d : Dart) (p : Polygon) :
    Decidable (dartOnFace d p) := by
  cases p <;> dsimp [dartOnFace] <;> infer_instance

/-- All actual darts in the full 5/6 cycle, INCLUDING the repeated
closing dart, truly lie in their own original C60 polygon. -/
theorem cyclicBoundaryDart_onFace :
    ∀ (p : Polygon) (k : Fin 7), k.val ≤ polygonSideCount p →
      dartOnFace (cyclicBoundaryDart p k.val) p := by
  decide

/-- Each boundary dart has an ORIGINAL Site incidence arrow to its
polygon (before any localization or formal inverse). -/
theorem cyclicDart_le_face (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    Site.vertex (cyclicBoundaryDart p k) ≤ Site.face p := by
  have hn : polygonSideCount p ≤ 6 := by
    cases p <;> simp [polygonSideCount]
  have h7 : k < 7 :=
    Nat.lt_of_le_of_lt (Nat.le_trans hk hn) (by decide : 6 < 7)
  change dartOnFace (cyclicBoundaryDart p k) p
  exact cyclicBoundaryDart_onFace p ⟨k, h7⟩ hk

/-- The common genuine polygon provides a two-legged face-cone span
from the first physical dart to the kth, without changing raw Site. -/
def polygonConePrefix (p : Polygon) (k : Nat)
    (hk : k ≤ polygonSideCount p) :
    Zigzag (Site.vertex (cyclicBoundaryDart p 0))
      (Site.vertex (cyclicBoundaryDart p k)) :=
  .forward (cyclicDart_le_face p 0 (Nat.zero_le _))
    (.backward (cyclicDart_le_face p k hk) (.nil _))

/-- In the ACTUAL localized Site, a forward incidence followed by
its formal inverse is the identity. The raw two-step is NOT nil. -/
theorem siteSpan_same_localized {s v : Site} (a : s ≤ v) :
    zigzagToLocalization
      (Zigzag.forward a (Zigzag.backward a (.nil s))) = 𝟙 _ := by
  let A : siteLocalizationQ.obj s ≅ siteLocalizationQ.obj v :=
    Localization.Construction.wIso (W := (⊤ : MorphismProperty Site))
      (homOfLE a) (by trivial)
  change A.hom ≫ (A.inv ≫ 𝟙 _) = 𝟙 _
  rw [Category.comp_id, A.hom_inv_id]

/-- The proven fan telescope: composing s->face<-t with
t->face<-u cancels only AFTER localization, leaving s->face<-u.
No interchange or higher lifting is assumed. -/
theorem siteSpan_telescope_localized {s t u v : Site}
    (a : s ≤ v) (b : t ≤ v) (c : u ≤ v) :
    zigzagToLocalization
      (append
        (.forward a (.backward b (.nil t)))
        (.forward b (.backward c (.nil u)))) =
    zigzagToLocalization
      (.forward a (.backward c (.nil u))) := by
  let B : siteLocalizationQ.obj t ≅ siteLocalizationQ.obj v :=
    Localization.Construction.wIso (W := (⊤ : MorphismProperty Site))
      (homOfLE b) (by trivial)
  let C : siteLocalizationQ.obj u ≅ siteLocalizationQ.obj v :=
    Localization.Construction.wIso (W := (⊤ : MorphismProperty Site))
      (homOfLE c) (by trivial)
  rw [zigzagToLocalization_append]
  change
    (siteLocalizationQ.map (homOfLE a) ≫ (B.inv ≫ 𝟙 _)) ≫
      (B.hom ≫ (C.inv ≫ 𝟙 _)) =
    siteLocalizationQ.map (homOfLE a) ≫ (C.inv ≫ 𝟙 _)
  simp only [Category.comp_id, Category.assoc]
  rw [← Category.assoc B.inv B.hom C.inv, B.inv_hom_id, Category.id_comp]

/-- The F112-D1 physical face-cone sector has the same raw typed
source as the abstract cone span through this very polygon. Proofs
of incidence are proof irrelevant, but the raw path constructors are
not collapsed. -/
theorem polygonConeRawSide_eq_span (p : Polygon) (i : Fin 6)
    (hi : i.val < polygonSideCount p) :
    polygonConeRawSide p i hi =
      Zigzag.forward (cyclicDart_le_face p i.val (Nat.le_of_lt hi))
        (Zigzag.backward
          (cyclicDart_le_face p (i.val + 1) (Nat.succ_le_of_lt hi))
          (.nil _)) := by
  rfl

/-- The whole certified raw boundary PREFIX is equivalent in the
localization to the two spoke arrows through its real face. This is
an INDUCTION on boundary length and uses the proved sector equations
and the actual face-cone telescope, never a guessed disk relation. -/
theorem polygonRawPrefix_cone_sound (p : Polygon) :
    ∀ (k : Nat) (hk : k ≤ polygonSideCount p),
      zigzagToLocalization (polygonRawPrefix p k hk) =
        zigzagToLocalization (polygonConePrefix p k hk) := by
  intro k
  induction k with
  | zero =>
      intro hk
      have hproof :
          cyclicDart_le_face p 0 hk =
            cyclicDart_le_face p 0 (Nat.zero_le _) :=
        Subsingleton.elim _ _
      change (𝟙 _) =
        zigzagToLocalization
          (.forward (cyclicDart_le_face p 0 (Nat.zero_le _))
            (.backward (cyclicDart_le_face p 0 hk) (.nil _)))
      rw [hproof]
      exact (siteSpan_same_localized
        (cyclicDart_le_face p 0 (Nat.zero_le _))).symm
  | succ k ih =>
      intro hk
      have hklt : k < polygonSideCount p := Nat.lt_of_succ_le hk
      have hk' : k ≤ polygonSideCount p := Nat.le_of_lt hklt
      have hn : polygonSideCount p ≤ 6 := by
        cases p <;> simp [polygonSideCount]
      let i : Fin 6 := ⟨k, Nat.lt_of_lt_of_le hklt hn⟩
      have hi : i.val < polygonSideCount p := hklt
      change
        zigzagToLocalization
          (append (polygonRawPrefix p k hk') (polygonRawSide p i hi)) =
        zigzagToLocalization (polygonConePrefix p (k + 1) hk)
      rw [zigzagToLocalization_append, ih hk',
        polygonFanSector_localized p i hi,
        polygonConeRawSide_eq_span p i hi]
      change
        zigzagToLocalization
          (.forward (cyclicDart_le_face p 0 (Nat.zero_le _))
            (.backward (cyclicDart_le_face p k hk') (.nil _))) ≫
        zigzagToLocalization
          (.forward (cyclicDart_le_face p k hk')
            (.backward (cyclicDart_le_face p (k + 1) hk) (.nil _))) =
        zigzagToLocalization
          (.forward (cyclicDart_le_face p 0 (Nat.zero_le _))
            (.backward (cyclicDart_le_face p (k + 1) hk) (.nil _)))
      simpa only [zigzagToLocalization_append] using
        siteSpan_telescope_localized
          (cyclicDart_le_face p 0 (Nat.zero_le _))
          (cyclicDart_le_face p k hk')
          (cyclicDart_le_face p (k + 1) hk)

/-- A target transport changes only the typing of the codomain of
an actual raw word; its interpretation is postcomposed with the
canonical identity-of-equals morphism, not silently identified. -/
theorem changeZigzagTarget_localized {s t u : Site}
    (h : t = u) (z : Zigzag s t) :
    zigzagToLocalization (changeZigzagTarget h z) =
      zigzagToLocalization z ≫
        eqToHom (congrArg siteLocalizationQ.obj h) := by
  cases h
  simp [changeZigzagTarget]

/-- An original face cone with equal terminal and initial physical
sites localizes to id even if it was not a raw empty path. -/
theorem siteSpan_cast_localized_id {s t v : Site} (h : t = s)
    (a : s ≤ v) (b : t ≤ v) :
    zigzagToLocalization
      (changeZigzagTarget h
        (.forward a (.backward b (.nil t)))) = 𝟙 _ := by
  cases h
  have hb : b = a := Subsingleton.elim _ _
  rw [hb]
  change zigzagToLocalization
    (.forward a (.backward a (.nil s))) = 𝟙 _
  exact siteSpan_same_localized a

/-- The actual original five/six-sided C60 closed raw polygon boundary
localizes to the genuine IDENTITY. This theorem is derived from the
finite fan of real edge-to-face incidences and groupoid cancellation.
It does not assert equality of the unquotiented raw proof words. -/
theorem polygonRawLoop_localized_id (p : Polygon) :
    zigzagToLocalization (polygonRawLoop p) = 𝟙 _ := by
  let hp : Site.vertex (cyclicBoundaryDart p (polygonSideCount p)) =
      Site.vertex (cyclicBoundaryDart p 0) :=
    congrArg Site.vertex (cyclicBoundary_closed p)
  let n := polygonSideCount p
  have hcone :
      zigzagToLocalization
          (changeZigzagTarget hp
            (polygonRawPrefix p n (Nat.le_refl _))) =
        zigzagToLocalization
          (changeZigzagTarget hp
            (polygonConePrefix p n (Nat.le_refl _))) := by
    rw [changeZigzagTarget_localized, changeZigzagTarget_localized,
      polygonRawPrefix_cone_sound p n (Nat.le_refl _)]
  change zigzagToLocalization
    (changeZigzagTarget hp (polygonRawPrefix p n (Nat.le_refl _))) = 𝟙 _
  rw [hcone]
  exact siteSpan_cast_localized_id hp
    (cyclicDart_le_face p 0 (Nat.zero_le _))
    (cyclicDart_le_face p n (Nat.le_refl _))

/-- Exact kernel-quotient face-disk equality, deduced from the actual
localization theorem rather than postulated as a new kernel. -/
theorem polygonRawLoop_kernel_id (p : Polygon) :
    zigzagKernelQ.map (polygonRawLoop p) =
      zigzagKernelQ.map
        (Zigzag.nil (Site.vertex (cyclicBoundaryDart p 0))) := by
  apply (zigzagKernel_exact _ _).2
  simpa only [zigzagToLocalization] using polygonRawLoop_localized_id p

/-- A NEW physically guarded, Type-valued polygon disk presentation.
The generator is admitted ONLY because the complete fan telescope
has already been PROVED above in the original physical localization.
It is not asserted to be the historical complete F42/F54/F55 source. -/
inductive PolygonDiskRewrite :
    {s t : Site} → Zigzag s t → Zigzag s t → Type where
  | ident {s t : Site} (q : Zigzag s t) : PolygonDiskRewrite q q
  | physicalDisk (p : Polygon) :
      PolygonDiskRewrite (polygonRawLoop p)
        (Zigzag.nil (Site.vertex (cyclicBoundaryDart p 0)))
  | inverse {s t : Site} {q r : Zigzag s t}
      (d : PolygonDiskRewrite q r) : PolygonDiskRewrite r q
  | vertical {s t : Site} {q r u : Zigzag s t}
      (d : PolygonDiskRewrite q r) (e : PolygonDiskRewrite r u) :
      PolygonDiskRewrite q u
  | leftContext {r s t : Site} (h : Zigzag r s)
      {q u : Zigzag s t} (d : PolygonDiskRewrite q u) :
      PolygonDiskRewrite (append h q) (append h u)
  | rightContext {r s t : Site}
      {q u : Zigzag r s} (d : PolygonDiskRewrite q u) (h : Zigzag s t) :
      PolygonDiskRewrite (append q h) (append u h)

/-- Structural proof that the new DISK source respects the actual
F69 localization, including ALL its permitted pasting operations. -/
theorem PolygonDiskRewrite.localized_sound
    {s t : Site} {q r : Zigzag s t} (d : PolygonDiskRewrite q r) :
    zigzagToLocalization q = zigzagToLocalization r := by
  induction d with
  | ident q => rfl
  | physicalDisk p =>
      simpa only [zigzagToLocalization] using polygonRawLoop_localized_id p
  | inverse d ih => exact ih.symm
  | vertical d e ihd ihe => exact ihd.trans ihe
  | leftContext h d ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => zigzagToLocalization h ≫ x) ih
  | rightContext d h ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => x ≫ zigzagToLocalization h) ih

theorem PolygonDiskRewrite.kernel_sound
    {s t : Site} {q r : Zigzag s t} (d : PolygonDiskRewrite q r) :
    zigzagKernelQ.map q = zigzagKernelQ.map r :=
  (zigzagKernel_exact q r).2 d.localized_sound

def polygonDiskProof (p : Polygon) :
    PolygonDiskRewrite (polygonRawLoop p)
      (Zigzag.nil (Site.vertex (cyclicBoundaryDart p 0))) :=
  .physicalDisk p

theorem polygonDisk_raw_not_nil (p : Polygon) :
    polygonRawLoop p ≠ Zigzag.nil _ :=
  polygonRawLoop_ne_nil p

#print axioms cyclicBoundaryDart_onFace
#print axioms cyclicDart_le_face
#print axioms siteSpan_same_localized
#print axioms siteSpan_telescope_localized
#print axioms polygonConeRawSide_eq_span
#print axioms polygonRawPrefix_cone_sound
#print axioms changeZigzagTarget_localized
#print axioms siteSpan_cast_localized_id
#print axioms polygonRawLoop_localized_id
#print axioms polygonRawLoop_kernel_id
#print axioms PolygonDiskRewrite.localized_sound
#print axioms PolygonDiskRewrite.kernel_sound
#print axioms polygonDisk_raw_not_nil
end
end Kuu.F112.Physical
