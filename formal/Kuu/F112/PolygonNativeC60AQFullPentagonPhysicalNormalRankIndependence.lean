import Mathlib.Data.Set.Countable
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNonFiniteNormalKernel

/-!
# F112-P94D3FW — irredundant original rooted normal presentation
# and coordinate coverage of every possible normal presentation

FV proved that the exact full noncommutative FreeGroup.map kernel is
finitely normally generated IFF the source's genuinely nonroot
image-fiber letters form a finite set. The genuine old-FJ physical
full 18D DV kernel is thus not finitely normally generated for any
nonempty real finite AQ context.

FW tightens that result without identifying the original signed
free words or dependent 18D Type-valued source certificates with
their integer-coordinate *detectors*.

1. Each actual f-image-fiber root is fixed by the root selector and
   therefore is never an active nonroot source letter.
2. Distinct active source letters have exactly off-diagonal ZERO
   integer-coordinate evaluations on one another's rooted relators;
   each active relator has its own coordinate +1.
3. Removing ANY active source letter from ANY rooted presentation
   makes the remaining original rooted relations insufficient even
   for NORMAL generation. The explicit full FS active rooted family
   is normally irredundant, and its relator map is injective.
4. EVERY arbitrary alternative normal generating family of the
   entire original kernel must contain some word with nonzero
   integer a-coordinate for EACH active source letter a. The
   relators in that alternative family need not be rooted words.

This proves strong irredundancy/coordinate coverage; it does NOT
yet prove exact minimal normal generating cardinality or that the
normal subgroup itself admits a free basis. In particular, FU/FV's
infinite genuine FJ physical active support does not alone prove
countability of the source alphabet or the minimal normal rank.
No original geometric 19D filler, global strict higher coherence,
or hyperdescent is asserted.

Append-only; no existing theorem or original Type-valued evidence
is replaced; no sorry/admit/new axioms. Preserve 107 public roots,
the strict Kuu core, the independent Kuu presentation, no Gray,
and pinned Lean/mathlib.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v

section GeneralNormalIndependence

/-- The root is chosen by image-fiber value, so applying the
root-selector twice fixes the originally selected representative. -/
theorem nativeC60FWLetterRoot_idempotent
    {A : Type u} {B : Type v} (f : A → B) (a : A) :
    nativeC60FQLetterRoot f (nativeC60FQLetterRoot f a) =
      nativeC60FQLetterRoot f a := by
  exact nativeC60FQLetterRoot_eq_of_image_eq f
    (nativeC60FQLetterRoot_image f a)

/-- An actual chosen root is not in the genuinely nonroot
source-letter support, even if its image fiber is infinite. -/
theorem nativeC60FWLetterRoot_not_active
    {A : Type u} {B : Type v} (f : A → B) (b : A) :
    nativeC60FQLetterRoot f b ∉ nativeC60FSActiveLetters f := by
  intro h
  change nativeC60FQLetterRoot f b ≠
    nativeC60FQLetterRoot f (nativeC60FQLetterRoot f b) at h
  exact h (nativeC60FWLetterRoot_idempotent f b).symm

/-- No selected root can coincide with an active source letter. -/
theorem nativeC60FWLetterRoot_ne_active
    {A : Type u} {B : Type v} (f : A → B)
    (a : A) (ha : a ∈ nativeC60FSActiveLetters f) (b : A) :
    nativeC60FQLetterRoot f b ≠ a := by
  intro hab
  have hroot : nativeC60FQLetterRoot f b ∉
      nativeC60FSActiveLetters f :=
    nativeC60FWLetterRoot_not_active f b
  rw [hab] at hroot
  exact hroot ha

/-- Off-diagonal evaluations of the ACTUAL rooted original signed
free-group relators vanish, while FV proved diagonal evaluation +1.
Crucially the root of b cannot be the active letter a. -/
theorem nativeC60FWOffDiagonal_coordinate
    {A : Type u} {B : Type v} (f : A → B)
    (a b : A) (ha : a ∈ nativeC60FSActiveLetters f)
    (hba : b ≠ a) :
    (nativeC60FVLetterCoordinate a)
        (nativeC60FSRootedRelator f b) = 1 := by
  have hroot : nativeC60FQLetterRoot f b ≠ a :=
    nativeC60FWLetterRoot_ne_active f a ha b
  simp only [nativeC60FSRootedRelator, map_mul, map_inv,
    nativeC60FVLetterCoordinate, FreeGroup.lift_apply_of,
    if_neg hba, if_neg hroot, inv_one, one_mul]

/-- For ANY collection T of source letters omitting an actual
active letter a, its rooted relators do not normally generate
the specific genuinely nontrivial a-rooted relator.
No finiteness, decidability or commutativity is assumed. -/
theorem nativeC60FWRootedRelator_outside_subfamily_normalClosure
    {A : Type u} {B : Type v} (f : A → B)
    (a : A) (ha : a ∈ nativeC60FSActiveLetters f)
    (T : Set A) (haT : a ∉ T) :
    nativeC60FSRootedRelator f a ∉
      Subgroup.normalClosure
        (Set.image (nativeC60FSRootedRelator f) T) := by
  have hsubset :
      Set.image (nativeC60FSRootedRelator f) T ⊆
        (nativeC60FVLetterCoordinate a).ker := by
    rintro z ⟨b, hb, rfl⟩
    have hba : b ≠ a := by
      intro hab
      apply haT
      exact hab ▸ hb
    exact MonoidHom.mem_ker.mpr
      (nativeC60FWOffDiagonal_coordinate f a b ha hba)
  have hnormal :
      Subgroup.normalClosure (Set.image (nativeC60FSRootedRelator f) T) ≤
        (nativeC60FVLetterCoordinate a).ker := by
    apply Subgroup.normalClosure_le_normal
    intro z hz
    exact hsubset hz
  intro hmem
  have hzero :
      (nativeC60FVLetterCoordinate a)
          (nativeC60FSRootedRelator f a) = 1 :=
    MonoidHom.mem_ker.mp (hnormal hmem)
  exact (nativeC60FVActiveRoot_coordinate_ne_one f a ha) hzero

/-- Every relator in the exact original FS rooted presentation
is necessary: the normal closure of ALL other active rooted
relations still does not contain the omitted original relator. -/
theorem nativeC60FWActiveRootedFamily_normalIrredundant
    {A : Type u} {B : Type v} (f : A → B)
    (a : A) (ha : a ∈ nativeC60FSActiveLetters f) :
    nativeC60FSRootedRelator f a ∉
      Subgroup.normalClosure
        (Set.image (nativeC60FSRootedRelator f)
          {b : A | b ∈ nativeC60FSActiveLetters f ∧ b ≠ a}) := by
  apply nativeC60FWRootedRelator_outside_subfamily_normalClosure f a ha
  intro hmem
  exact hmem.2 rfl

/-- No distinct active original source letters give the same
actual noncommutative two-letter rooted relator. This proves
non-repetition of the canonical normal presentation, not a
free-group basis theorem for the full kernel. -/
theorem nativeC60FWActiveRootedRelators_injectiveOn
    {A : Type u} {B : Type v} (f : A → B) :
    Set.InjOn (nativeC60FSRootedRelator f)
      (nativeC60FSActiveLetters f) := by
  intro a ha b _hb hab
  by_contra hne
  have hba : b ≠ a := Ne.symm hne
  have hzero :
      (nativeC60FVLetterCoordinate a)
          (nativeC60FSRootedRelator f b) = 1 :=
    nativeC60FWOffDiagonal_coordinate f a b ha hba
  have hdet :
      (nativeC60FVLetterCoordinate a)
          (nativeC60FSRootedRelator f a) =
        (nativeC60FVLetterCoordinate a)
          (nativeC60FSRootedRelator f b) :=
    congrArg (nativeC60FVLetterCoordinate a) hab
  exact (nativeC60FVActiveRoot_coordinate_ne_one f a ha)
    (hdet.trans hzero)

/-- NECESSARY condition on EVERY arbitrary set R of ORIGINAL
noncommutative free-group words that normally generates the
whole kernel: EACH genuinely active letter must be detected
by at least ONE word of R in its own integer coordinate.

No cardinality or restricted form is assumed for R. Its words
can be arbitrary signed noncommutative words, not only FQ/FS
rooted pairs. -/
theorem nativeC60FWAnyNormalGenerators_detect_every_active
    {A : Type u} {B : Type v} (f : A → B)
    (R : Set (FreeGroup A))
    (hR : (FreeGroup.map f).ker = Subgroup.normalClosure R)
    (a : A) (ha : a ∈ nativeC60FSActiveLetters f) :
    ∃ z : FreeGroup A, z ∈ R ∧
      (nativeC60FVLetterCoordinate a) z ≠ 1 := by
  classical
  by_contra hnone
  have hRcoordinate :
      R ⊆ (nativeC60FVLetterCoordinate a).ker := by
    intro z hz
    apply MonoidHom.mem_ker.mpr
    by_contra hnz
    exact hnone ⟨z, hz, hnz⟩
  have hnormal :
      Subgroup.normalClosure R ≤
        (nativeC60FVLetterCoordinate a).ker := by
    apply Subgroup.normalClosure_le_normal
    intro z hz
    exact hRcoordinate hz
  have hrootKer :
      nativeC60FSRootedRelator f a ∈ (FreeGroup.map f).ker := by
    rw [nativeC60FSFreeMap_kernel_eq_active f]
    exact Subgroup.subset_normalClosure
      (nativeC60FSActiveRelator_mem f a ha)
  have hrootR :
      nativeC60FSRootedRelator f a ∈ Subgroup.normalClosure R := by
    rw [← hR]
    exact hrootKer
  have hzero :
      (nativeC60FVLetterCoordinate a)
          (nativeC60FSRootedRelator f a) = 1 :=
    MonoidHom.mem_ker.mp (hnormal hrootR)
  exact (nativeC60FVActiveRoot_coordinate_ne_one f a ha) hzero

/-- For each active original letter, the finite supports of an
arbitrary normally generating family R cannot simultaneously
miss that letter. This is the global coordinate-coverage
obstruction from which a subsequent cardinal rank bound may
be derived, retaining arbitrary noncommutative relators. -/
theorem nativeC60FWAnyNormalGenerators_cover_active
    {A : Type u} {B : Type v} (f : A → B)
    (R : Set (FreeGroup A))
    (hR : (FreeGroup.map f).ker = Subgroup.normalClosure R) :
    nativeC60FSActiveLetters f ⊆
      {a : A | ∃ z : FreeGroup A, z ∈ R ∧
        (nativeC60FVLetterCoordinate a) z ≠ 1} := by
  intro a ha
  exact nativeC60FWAnyNormalGenerators_detect_every_active f R hR a ha

/-- EXACT characterization of WHICH collections of actual source
letters suffice for a FULL rooted normal presentation. The source
letter set T can be infinite and may include redundant chosen roots:
its rooted relators normally generate the whole original full kernel
IFF it contains EVERY genuinely nonroot original active letter.

This is an inclusion-minimality theorem for the rooted presentation;
it does not conflate rooted-presentation minimality with cardinal
minimality among arbitrary non-rooted normal presentations. -/
theorem nativeC60FWRootedNormalGeneration_iff_active_subset
    {A : Type u} {B : Type v} (f : A → B) (T : Set A) :
    Subgroup.normalClosure (Set.image (nativeC60FSRootedRelator f) T) =
      (FreeGroup.map f).ker ↔
    nativeC60FSActiveLetters f ⊆ T := by
  constructor
  · intro hnormal a ha
    by_contra hanot
    have hmissing :
        nativeC60FSRootedRelator f a ∉
          Subgroup.normalClosure
            (Set.image (nativeC60FSRootedRelator f) T) :=
      nativeC60FWRootedRelator_outside_subfamily_normalClosure
        f a ha T hanot
    have hrootKer :
        nativeC60FSRootedRelator f a ∈
          (FreeGroup.map f).ker := by
      rw [nativeC60FSFreeMap_kernel_eq_active f]
      exact Subgroup.subset_normalClosure
        (nativeC60FSActiveRelator_mem f a ha)
    rw [← hnormal] at hrootKer
    exact hmissing hrootKer
  · intro hactive
    apply le_antisymm
    · apply Subgroup.normalClosure_le_normal
      rintro z ⟨b, _hb, rfl⟩
      rw [nativeC60FQFreeMap_kernel_eq_rooted f]
      exact nativeC60FQRootedDefect_mem f b
    · rw [nativeC60FSFreeMap_kernel_eq_active f]
      apply Subgroup.normalClosure_le_normal
      rintro z ⟨b, hb, rfl⟩
      exact Subgroup.subset_normalClosure ⟨b, hactive hb, rfl⟩

/-- A rigorous cardinal UPPER gate: if the genuinely active source
letters are countable, the entire original noncommutative free-map
kernel has a countable normal presentation. This does NOT claim
that the actual old-FJ physical active alphabet has been proved
countable; FU proves an infinite injection, not this upper gate. -/
theorem nativeC60FWKernel_countably_normalGenerated_of_active_countable
    {A : Type u} {B : Type v} (f : A → B)
    (hc : (nativeC60FSActiveLetters f).Countable) :
    ∃ R : Set (FreeGroup A), R.Countable ∧
      (FreeGroup.map f).ker = Subgroup.normalClosure R := by
  exact ⟨nativeC60FSActiveRelators f,
    hc.image (nativeC60FSRootedRelator f),
    nativeC60FSFreeMap_kernel_eq_active f⟩

/-- EXACT countable normal-generation gate for ANY original full
noncommutative free-group map. The converse does not rely on a
countable source alphabet: EACH word has FV's finite original-letter
support, so the union of supports of a countable family of arbitrary
normal relators is countable. Every active source letter must be
detected by SOME proposed relator (FW coverage), hence belongs to
that union. The reverse follows from the canonical FS presentation.
The result is conditional: actual physical FJ source countability is
not asserted. -/
theorem nativeC60FWKernel_countableNormal_iff_activeCountable
    {A : Type u} {B : Type v} (f : A → B) :
    (∃ R : Set (FreeGroup A), R.Countable ∧
      (FreeGroup.map f).ker = Subgroup.normalClosure R) ↔
      (nativeC60FSActiveLetters f).Countable := by
  classical
  constructor
  · rintro ⟨R, hRcount, hRnormal⟩
    have hsupportCountable :
        (⋃ z ∈ R,
          (↑(nativeC60FVWordSupport z) : Set A)).Countable := by
      apply (Set.Countable.biUnion_iff hRcount).2
      intro z _hz
      exact Finset.countable_toSet (nativeC60FVWordSupport z)
    apply hsupportCountable.mono
    intro a ha
    obtain ⟨z, hz, hnonzero⟩ :=
      nativeC60FWAnyNormalGenerators_detect_every_active
        f R hRnormal a ha
    have haSupport : a ∈ nativeC60FVWordSupport z := by
      by_contra hnot
      exact hnonzero (nativeC60FVWordSupport_outside z a hnot)
    exact Set.mem_iUnion.mpr
      ⟨z, Set.mem_iUnion.mpr ⟨hz, haSupport⟩⟩
  · intro hcountable
    exact nativeC60FWKernel_countably_normalGenerated_of_active_countable
      f hcountable

end GeneralNormalIndependence

#print axioms nativeC60FWLetterRoot_idempotent
#print axioms nativeC60FWLetterRoot_not_active
#print axioms nativeC60FWLetterRoot_ne_active
#print axioms nativeC60FWOffDiagonal_coordinate
#print axioms nativeC60FWRootedRelator_outside_subfamily_normalClosure
#print axioms nativeC60FWActiveRootedFamily_normalIrredundant
#print axioms nativeC60FWActiveRootedRelators_injectiveOn
#print axioms nativeC60FWAnyNormalGenerators_detect_every_active
#print axioms nativeC60FWAnyNormalGenerators_cover_active
#print axioms nativeC60FWRootedNormalGeneration_iff_active_subset
#print axioms nativeC60FWKernel_countably_normalGenerated_of_active_countable
#print axioms nativeC60FWKernel_countableNormal_iff_activeCountable

end
end Kuu.F112.Physical
