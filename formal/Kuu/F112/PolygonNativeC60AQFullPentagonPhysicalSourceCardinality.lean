import Mathlib.SetTheory.Cardinal.Basic
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalExactNormalRank

/-!
# F112-P94D3FY — actual original 18D source-cardinality decomposition,
# exact image/active obstruction, and conditional countably infinite normal rank

FX established the EXACT minimal cardinal of all arbitrary
noncommutative normal generating sets of ker(FreeGroup.map f):
#D_f, where D_f consists of original source letters not equal to
their chosen true-image-fiber roots.

FY now identifies what controls that cardinal in the actual
proof-relevant physical 18D source alphabet. The fiber-root selector
takes exactly one original source letter per actually received
target-code image. There is a genuine EQUIVALENCE OF TYPES
  original source A ≃ D_f ⊕ Set.range f.
Thus the original source's cardinal splits EXACTLY into active
(nonroot) 18D codes and genuinely distinct received-image fibers.
This is a stronger obstruction boundary than presuming that the
finite C60 geometry makes the arbitrarily dependent proof universe
countable.

An actual physical word with nonempty C60 AQ context always has
INFINITELY many active codes (FU). If, and only if appropriate
countability hypotheses on the *original Type-valued alphabet*
hold, it is legitimate to sharpen the exact normal cardinal
to aleph-null; the original dependent 14D–17D proof types are
NOT silently declared countable. In particular, countability
of the truly received image ALONE is not the same as countability
of the original 18D code alphabet; the exact split displays
both constituents.

No source Type replacement by a numeric invariant, no new logical
axioms, sorry or admit. Retain original signed noncommutative kernel,
raw 14D–18D history, distinct FJ and FK–FM presentations, strict
Kuu core and independent Kuu presentation, 107 public roots, no
Gray, pinned Lean v4.30.0-rc2 and pinned mathlib. No geometric
19D filler, global strict coherence or hyperdescent is asserted.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory Cardinal
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

section ExactImageFiberRootSplit

/-- A genuine selected representative of an actual target-image
fiber is itself fixed by the root selector. Proof retains the
actual dependent source letter rather than replacing it by a
quotient or an arbitrary numeric token. -/
theorem nativeC60FYImageRoot_fixed
    {A : Type u} {B : Type v} (f : A → B)
    (b : Set.range f) :
    nativeC60FQLetterRoot f (nativeC60FQImageRoot f b) =
      nativeC60FQImageRoot f b := by
  unfold nativeC60FQLetterRoot
  have h :
      (⟨f (nativeC60FQImageRoot f b),
        ⟨nativeC60FQImageRoot f b, rfl⟩⟩ : Set.range f) = b :=
    Subtype.ext (nativeC60FQImageRoot_maps_to_image f b)
  rw [h]

/-- EXACT TYPE decomposition of the ORIGINAL free-group source
alphabet into all genuinely nonroot source letters (left) and
one original chosen root per ACTUALLY RECEIVED target image
(right). The right component is Set.range f, NOT the arbitrary
full target B. No finite or countable assumptions. -/
noncomputable def nativeC60FYSourceEquivActiveSumImage
    {A : Type u} {B : Type v} (f : A → B) :
    A ≃ Sum (nativeC60FSActiveLetters f) (Set.range f) := by
  classical
  refine
    { toFun := fun a =>
        if ha : a ∈ nativeC60FSActiveLetters f
        then Sum.inl ⟨a, ha⟩
        else Sum.inr ⟨f a, ⟨a, rfl⟩⟩
      invFun := fun z =>
        match z with
        | .inl a => a.1
        | .inr b => nativeC60FQImageRoot f b
      left_inv := ?_
      right_inv := ?_ }
  · intro a
    by_cases ha : a ∈ nativeC60FSActiveLetters f
    · simp only [dif_pos ha]
    · have hroot : a = nativeC60FQLetterRoot f a := by
        by_contra hne
        apply ha
        change a ≠ nativeC60FQLetterRoot f a
        exact hne
      simpa only [dif_neg ha, nativeC60FQLetterRoot] using hroot.symm
  · intro z
    cases z with
    | inl a =>
      rcases a with ⟨a, ha⟩
      simp only [dif_pos ha]
    | inr b =>
      have hnot :
          nativeC60FQImageRoot f b ∉ nativeC60FSActiveLetters f := by
        intro hactive
        change nativeC60FQImageRoot f b ≠
          nativeC60FQLetterRoot f (nativeC60FQImageRoot f b) at hactive
        exact hactive (nativeC60FYImageRoot_fixed f b).symm
      have hb :
          (⟨f (nativeC60FQImageRoot f b),
            ⟨nativeC60FQImageRoot f b, rfl⟩⟩ : Set.range f) = b :=
        Subtype.ext (nativeC60FQImageRoot_maps_to_image f b)
      simpa only [dif_neg hnot] using
        (congrArg
          (Sum.inr : Set.range f →
            Sum (nativeC60FSActiveLetters f) (Set.range f))
          hb)

/-- Countability is EXACTLY the two-component compatibility
condition: both actual nonroot original letters AND the chosen
true target-image roots must be countable. Merely observing a
countable quotient or finite physical geometry is not enough. -/
theorem nativeC60FYSource_countable_iff_active_and_image_countable
    {A : Type u} {B : Type v} (f : A → B) :
    Countable A ↔
      Countable (nativeC60FSActiveLetters f) ∧
      Countable (Set.range f) := by
  rw [(nativeC60FYSourceEquivActiveSumImage f).countable_iff]
  constructor
  · intro h
    letI : Countable
      (Sum (nativeC60FSActiveLetters f) (Set.range f)) := h
    exact ⟨
      (show Function.Injective
        (Sum.inl : nativeC60FSActiveLetters f →
          Sum (nativeC60FSActiveLetters f) (Set.range f)) from
        Sum.inl_injective).countable,
      (show Function.Injective
        (Sum.inr : Set.range f →
          Sum (nativeC60FSActiveLetters f) (Set.range f)) from
        Sum.inr_injective).countable⟩
  · rintro ⟨hleft, hright⟩
    letI : Countable (nativeC60FSActiveLetters f) := hleft
    letI : Countable (Set.range f) := hright
    infer_instance

/-- When the ACTUAL received-image fiber type is already
countable, the only remaining source-countability obstruction
is the genuine active original-letter type. -/
theorem nativeC60FYSource_countable_iff_active_of_image_countable
    {A : Type u} {B : Type v} (f : A → B)
    (himage : Countable (Set.range f)) :
    Countable A ↔ Countable (nativeC60FSActiveLetters f) := by
  constructor
  · intro h
    exact (nativeC60FYSource_countable_iff_active_and_image_countable f).mp h |>.1
  · intro h
    exact (nativeC60FYSource_countable_iff_active_and_image_countable f).mpr
      ⟨h, himage⟩

/-- An EXACT cardinal decomposition whenever the source and
target alphabets live in the same universe. No cardinal term
is silently dropped, even when the actual image is infinite. -/
theorem nativeC60FYSource_cardinal_eq_active_add_image
    {A : Type u} {B : Type u} (f : A → B) :
    #A = #(nativeC60FSActiveLetters f) + #(Set.range f) := by
  calc
    #A = #(Sum (nativeC60FSActiveLetters f) (Set.range f)) :=
      Cardinal.mk_congr (nativeC60FYSourceEquivActiveSumImage f)
    _ = #(nativeC60FSActiveLetters f) + #(Set.range f) := by
      simp only [Cardinal.mk_sum, Cardinal.lift_id]

/-- FU-style infinitude plus real original alphabet countability
forces precisely aleph-null active roots; no countability of
original source letters is inferred from infinitude alone. -/
theorem nativeC60FYActive_aleph0_of_source_countable_infinite
    {A : Type u} {B : Type v} (f : A → B)
    (hsource : Countable A)
    (hactive : Infinite (nativeC60FSActiveLetters f)) :
    #(nativeC60FSActiveLetters f) = ℵ₀ := by
  letI : Countable A := hsource
  letI : Infinite (nativeC60FSActiveLetters f) := hactive
  exact Cardinal.mk_eq_aleph0 _

end ExactImageFiberRootSplit

section GenuinePhysicalSourceCardinal

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- The true dependent ORIGINAL 18D alphabet is precisely the
sum of its genuinely active source generators and selected
roots, one for each ACTUALLY RECEIVED full 18D DV code. -/
noncomputable def nativeK5FYPhysical_originalSource_equiv_active_plus_image
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    NativeC60DSCompleteEighteenCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) ≃
      Sum
        (nativeC60FSActiveLetters
          (nativeC60DVTransportCompleteCode
            (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word))
        (Set.range (nativeC60DVTransportCompleteCode
            (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)) :=
  nativeC60FYSourceEquivActiveSumImage
    (nativeC60DVTransportCompleteCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)

/-- Exact source alphabet CARDINAL decomposition for every
physical C60 AQ word, with original 17D boundary evidence and
recursively generated 18D source codes retained. -/
theorem nativeK5FYPhysical_originalSource_cardinal_split
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    #(NativeC60DSCompleteEighteenCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) =
      #(nativeC60FSActiveLetters
        (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)) +
      #(Set.range (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)) :=
  nativeC60FYSource_cardinal_eq_active_add_image
    (nativeC60DVTransportCompleteCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)

/-- The genuinely physical 18D original SOURCE countability
gate retains BOTH its nonroot source support and the true
distinct received-image source-fiber representatives. -/
theorem nativeK5FYPhysical_originalSource_countable_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    Countable (NativeC60DSCompleteEighteenCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) ↔
      Countable (nativeC60FSActiveLetters
        (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)) ∧
      Countable (Set.range (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)) :=
  nativeC60FYSource_countable_iff_active_and_image_countable
    (nativeC60DVTransportCompleteCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)

/-- An actual original source 18D Type COUNTABILITY hypothesis
(and independently FU's unconditional physical nonempty infinite
rooted support) implies the physically sharp active cardinal ℵ₀.
This is a conditional theorem, NOT an unproved existence of
an enumeration of arbitrary input-category raw proof types. -/
theorem nativeK5FYPhysical_active_aleph0_of_source_countable
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ [])
    (hsource : Countable (NativeC60DSCompleteEighteenCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W))) :
    #(nativeC60FSActiveLetters
      (nativeC60DVTransportCompleteCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)) = ℵ₀ :=
  nativeC60FYActive_aleph0_of_source_countable_infinite
    (nativeC60DVTransportCompleteCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)
    hsource (nativeK5FUPhysical_canonicalActiveSource_infinite W word hne)

/-- Exact MINIMUM normal rank (all finite/infinite cardinals)
is explicitly instantiated on the ORIGINAL 18D noncommutative
physical full-DV kernel for any genuine finite AQ word.
No 18D alphabet cardinal is assumed. -/
theorem nativeK5FYPhysical_fullDV_exactNormalRank
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    (∀ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
          Subgroup.normalClosure R →
      #(nativeC60FSActiveLetters
        (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)) ≤ #R) ∧
    (∃ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
          Subgroup.normalClosure R ∧
      #R = #(nativeC60FSActiveLetters
        (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word))) := by
  rw [nativeC60FCTransport_eq_freeMap
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word]
  exact nativeC60FXFullFreeMap_kernel_exact_normalRank
    (nativeC60DVTransportCompleteCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)

/-- SHARP conditional physical result: for each nonempty genuine
C60 AQ word, if the ORIGINAL raw dependent 18D source code type
is countable, then its WHOLE original noncommutative physical
kernel has exact minimum normal generator cardinal aleph-null.
Neither source countability nor any restriction on lower 14D–17D
data is silently inferred from finite C60 geometry. -/
theorem nativeK5FYPhysical_fullDV_exactAleph0NormalRank_of_sourceCountable
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ [])
    (hsource : Countable (NativeC60DSCompleteEighteenCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W))) :
    (∀ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
          Subgroup.normalClosure R → ℵ₀ ≤ #R) ∧
    (∃ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
        Subgroup.normalClosure R ∧ #R = ℵ₀) := by
  have hactive :
      #(nativeC60FSActiveLetters
        (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)) = ℵ₀ :=
    nativeK5FYPhysical_active_aleph0_of_source_countable
      W word hne hsource
  obtain ⟨hlower, ⟨R₀, hR₀, hcard⟩⟩ :=
    nativeK5FYPhysical_fullDV_exactNormalRank W word
  constructor
  · intro R hR
    simpa only [hactive] using hlower R hR
  · exact ⟨R₀, hR₀, hcard.trans hactive⟩

end GenuinePhysicalSourceCardinal

#print axioms nativeC60FYImageRoot_fixed
#print axioms nativeC60FYSource_countable_iff_active_and_image_countable
#print axioms nativeC60FYSource_countable_iff_active_of_image_countable
#print axioms nativeC60FYSource_cardinal_eq_active_add_image
#print axioms nativeC60FYActive_aleph0_of_source_countable_infinite
#print axioms nativeK5FYPhysical_originalSource_cardinal_split
#print axioms nativeK5FYPhysical_originalSource_countable_iff
#print axioms nativeK5FYPhysical_active_aleph0_of_source_countable
#print axioms nativeK5FYPhysical_fullDV_exactNormalRank
#print axioms nativeK5FYPhysical_fullDV_exactAleph0NormalRank_of_sourceCountable

end
end Kuu.F112.Physical
