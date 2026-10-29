import Kuu.F112.PolygonNativeC60AQFullPentagonRootedSectorKernelClassification

/-!
# F112-P94D3FR — exact recursive-spine normal kernel and inner-code obstruction

FQ classified all ACTUAL dependent 18D DV collisions by top-level
assoc/post/pre and rooted each code fiber without assuming surjectivity.
FR refines this for the ENTIRE, arbitrarily nested original
post/pre/.../assoc constructor spine, using FI's already proved
full-spine preservation rather than a new scalar projection.

(1) The original FO all-code collision family is EXACTLY the union
    of collision pair families indexed by complete recursive spines.
    Its normal closure remains the WHOLE genuine noncommutative kernel.
(2) FQ's chosen actual-image fiber roots preserve the ENTIRE original
    nested spine. Rooted normal generators decompose by this spine.
    No finite number of spines or finite generator set is assumed.
(3) Receiver factorization is UNIQUE on the actual DV IMAGE iff all
    same-spine collisions agree, equivalently iff the receiver
    identifies each original letter with its own image-fiber root.
(4) FH's true Type-valued post/pre INNER code extractors yield
    unconditional necessary equality of transported inner 18D codes
    for every fixed-boundary outer post/pre collision. If the
    inner images differ, the OUTER full codes and corresponding
    ordered two-letter free-group defects cannot lie in the DV kernel.
    No lower 17D context injectivity assumption is needed for these
    necessary obstructions.
(5) Within-spine full-code faithfulness is equivalent to the
    ACTUAL original 17D context-object injectivity gate (FI),
    without asserting that an arbitrary physical frame satisfies it.

Do not identify FO's whole-kernel presentation with a single known
physical FJ defect, a finite or minimal normal generating set, or
a true geometric 19D filler. No erased raw17D arguments, no
cross-sector commutativity, no new Gray, strict n-category or
hyperdescent claim. Old FJ and alternate FK/FL/FM stay distinct.
Keep all prior Type-valued 14D--18D, DS and no-go evidence, strict
Kuu primary, independent Kuu as a presentation, 107 public roots.
Append-only / tighten-only. No new axioms, sorry or admit.
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

section FullRecursiveSpineClassification

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- All ORIGINAL full 18D code collisions with a specified ENTIRE
ordered recursive constructor spine, not merely a top-level tag.
Source, target and dependent 17D witness remain in each code. -/
def nativeC60FRSpinePairs
    (word : List Bool) (spine : List NativeC60FGConstructorTag) :
    Set (NativeC60DTFullFree S F × NativeC60DTFullFree S F) :=
  {pair | ∃ a b : NativeC60DSCompleteEighteenCode S F,
    nativeC60DVTransportCompleteCode S F word a =
      nativeC60DVTransportCompleteCode S F word b ∧
    nativeC60FIOriginalCodeSpine S F a = spine ∧
    nativeC60FIOriginalCodeSpine S F b = spine ∧
    pair = (FreeGroup.of a, FreeGroup.of b)}

/-- Every finite full recursion spine is a possible index, without
asserting any finite bound on the set of actual code spines. -/
def nativeC60FRAllSpinePairs (word : List Bool) :
    Set (NativeC60DTFullFree S F × NativeC60DTFullFree S F) :=
  ⋃ spine : List NativeC60FGConstructorTag,
    nativeC60FRSpinePairs S F word spine

/-- EXACT all-pairs classification: an actual DV 18D code collision
belongs to ONE full recursive spine, because FI proves transport
preserves the entire original nested constructor order. -/
theorem nativeC60FRFullPairs_eq_spineUnion
    (word : List Bool) :
    nativeC60FOFiberPairs (nativeC60DVTransportCompleteCode S F word) =
      nativeC60FRAllSpinePairs S F word := by
  ext pair
  constructor
  · rintro ⟨a, b, hab, rfl⟩
    apply Set.mem_iUnion.mpr
    refine ⟨nativeC60FIOriginalCodeSpine S F a, ?_⟩
    exact ⟨a, b, hab, rfl,
      (nativeC60FICompleteCodeCollision_preserves_spine S F word hab).symm,
      rfl⟩
  · intro hp
    obtain ⟨spine, hspine⟩ := Set.mem_iUnion.mp hp
    rcases hspine with ⟨a, b, hab, _, _, hpair⟩
    exact ⟨a, b, hab, hpair⟩

/-- The WHOLE original noncommutative DV kernel is the normal closure
of just the union of actual SAME-FULL-SPINE collision pair families.
No commutation, direct-product or arbitrary relator is introduced. -/
theorem nativeC60FRFullKernel_eq_spineNormalClosure
    (word : List Bool) :
    (nativeC60DVFullWordTransport S F word).ker =
      nativeC60DTNormalClosure (nativeC60FRAllSpinePairs S F word) := by
  calc
    (nativeC60DVFullWordTransport S F word).ker =
        nativeC60FOFullKernelNormalClosure S F word :=
      nativeC60FOFullTransport_kernel_eq_normalClosure S F word
    _ = nativeC60DTNormalClosure
        (nativeC60FRAllSpinePairs S F word) := by
      change nativeC60DTNormalClosure
        (nativeC60FOFiberPairs (nativeC60DVTransportCompleteCode S F word)) =
          nativeC60DTNormalClosure (nativeC60FRAllSpinePairs S F word)
      rw [nativeC60FRFullPairs_eq_spineUnion S F word]

/-- The actual-image FQ root preserves the ENTIRE recursive spine,
not only its outermost assoc/post/pre tag. -/
theorem nativeC60FRFullRoot_preserves_spine
    (word : List Bool)
    (a : NativeC60DSCompleteEighteenCode S F) :
    nativeC60FIOriginalCodeSpine S F
        (nativeC60FQLetterRoot
          (nativeC60DVTransportCompleteCode S F word) a) =
      nativeC60FIOriginalCodeSpine S F a :=
  nativeC60FICompleteCodeCollision_preserves_spine S F word
    (nativeC60FQLetterRoot_image
      (nativeC60DVTransportCompleteCode S F word) a)

/-- ROOTED code relations from FQ, grouped by exact original full
recursive spine. The root itself has that same spine by the theorem
above; the outer code is never converted to a charge/graph edge. -/
def nativeC60FRSpineRootedPairs
    (word : List Bool) (spine : List NativeC60FGConstructorTag) :
    Set (NativeC60DTFullFree S F × NativeC60DTFullFree S F) :=
  {pair | ∃ a : NativeC60DSCompleteEighteenCode S F,
    nativeC60FIOriginalCodeSpine S F a = spine ∧
    pair = (FreeGroup.of a,
      FreeGroup.of (nativeC60FQLetterRoot
        (nativeC60DVTransportCompleteCode S F word) a))}

/-- ALL FQ rooted relations have a unique original recursive spine.
No implicit finite support or finitely many spine strata is asserted. -/
theorem nativeC60FRRootedPairs_eq_spineUnion
    (word : List Bool) :
    nativeC60FQRootedPairs (nativeC60DVTransportCompleteCode S F word) =
      ⋃ spine : List NativeC60FGConstructorTag,
        nativeC60FRSpineRootedPairs S F word spine := by
  ext pair
  constructor
  · rintro ⟨a, rfl⟩
    apply Set.mem_iUnion.mpr
    refine ⟨nativeC60FIOriginalCodeSpine S F a, ?_⟩
    exact ⟨a, rfl, rfl⟩
  · intro hp
    obtain ⟨spine, hspine⟩ := Set.mem_iUnion.mp hp
    rcases hspine with ⟨a, _, rfl⟩
    exact ⟨a, rfl⟩

/-- Rooted WHOLE-kernel presentation indexed by every genuine
recursive shape, not by a fabricated finite list of defects. -/
theorem nativeC60FRFullKernel_eq_spineRootedNormalClosure
    (word : List Bool) :
    (nativeC60DVFullWordTransport S F word).ker =
      nativeC60DTNormalClosure
        (⋃ spine : List NativeC60FGConstructorTag,
          nativeC60FRSpineRootedPairs S F word spine) := by
  calc
    (nativeC60DVFullWordTransport S F word).ker =
      nativeC60FQRootedNormalClosure
        (nativeC60DVTransportCompleteCode S F word) :=
      nativeC60FQFullKernel_eq_rooted S F word
    _ = nativeC60DTNormalClosure
        (⋃ spine : List NativeC60FGConstructorTag,
          nativeC60FRSpineRootedPairs S F word spine) := by
      change nativeC60DTNormalClosure
        (nativeC60FQRootedPairs (nativeC60DVTransportCompleteCode S F word)) =
          nativeC60DTNormalClosure
            (⋃ spine : List NativeC60FGConstructorTag,
              nativeC60FRSpineRootedPairs S F word spine)
      rw [nativeC60FRRootedPairs_eq_spineUnion S F word]

/-- Exact true-image receiver descent can be checked independently
against collisions inside EACH entire original recursive spine.
It is still one original group and one actual DV image subgroup. -/
theorem nativeC60FRFullReceiver_spine_iff
    {G : Type v} [Group G]
    (word : List Bool) (receiver : NativeC60DTFullFree S F →* G) :
    (∃! induced : NativeC60FPFullImage S F word →* G,
      induced.comp (nativeC60DVFullWordTransport S F word).rangeRestrict =
        receiver) ↔
      ∀ spine : List NativeC60FGConstructorTag,
        ∀ a b : NativeC60DSCompleteEighteenCode S F,
          nativeC60FIOriginalCodeSpine S F a = spine →
          nativeC60FIOriginalCodeSpine S F b = spine →
          nativeC60DVTransportCompleteCode S F word a =
            nativeC60DVTransportCompleteCode S F word b →
          receiver (FreeGroup.of a) = receiver (FreeGroup.of b) := by
  rw [nativeC60FPFullReceiver_image_unique_iff S F word receiver]
  constructor
  · intro hall spine a b _ _ hab
    exact hall a b hab
  · intro hlocal a b hab
    exact hlocal (nativeC60FIOriginalCodeSpine S F a) a b rfl
      (nativeC60FICompleteCodeCollision_preserves_spine S F word hab).symm
      hab

/-- A STILL SMALLER receiver test: equate every ORIGINAL 18D code
only with the root chosen in its actual DV image fiber. It is
necessary and sufficient for the unique induced receiver on range. -/
theorem nativeC60FRFullReceiver_rooted_iff
    {G : Type v} [Group G]
    (word : List Bool) (receiver : NativeC60DTFullFree S F →* G) :
    (∃! induced : NativeC60FPFullImage S F word →* G,
      induced.comp (nativeC60DVFullWordTransport S F word).rangeRestrict =
        receiver) ↔
      ∀ a : NativeC60DSCompleteEighteenCode S F,
        receiver (FreeGroup.of a) =
          receiver (FreeGroup.of (nativeC60FQLetterRoot
            (nativeC60DVTransportCompleteCode S F word) a)) := by
  rw [nativeC60FPFullReceiver_image_unique_iff S F word receiver]
  constructor
  · intro hall a
    exact hall a _ (nativeC60FQLetterRoot_image
      (nativeC60DVTransportCompleteCode S F word) a).symm
  · intro hroot a b hab
    calc
      receiver (FreeGroup.of a) =
          receiver (FreeGroup.of (nativeC60FQLetterRoot
            (nativeC60DVTransportCompleteCode S F word) a)) := hroot a
      _ = receiver (FreeGroup.of (nativeC60FQLetterRoot
            (nativeC60DVTransportCompleteCode S F word) b)) := by
              rw [nativeC60FQLetterRoot_eq_of_image_eq
                (nativeC60DVTransportCompleteCode S F word) hab]
      _ = receiver (FreeGroup.of b) := (hroot b).symm

/-- Complete-code injectivity inside each full-spine stratum
holds exactly when the REAL 17D context-object action is injective.
This is NOT an assumption that actual original physical FJ contexts
are faithful; FJ explicitly violates it at every nonempty word. -/
theorem nativeC60FRContext_injective_iff_spineLocal
    (word : List Bool) :
    Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word) ↔
    ∀ a b : NativeC60DSCompleteEighteenCode S F,
      nativeC60FIOriginalCodeSpine S F a =
        nativeC60FIOriginalCodeSpine S F b →
      nativeC60DVTransportCompleteCode S F word a =
        nativeC60DVTransportCompleteCode S F word b → a = b := by
  constructor
  · intro hctx a b _ hab
    exact nativeC60FICompleteCode_injective_of_context S F word hctx hab
  · intro hlocal
    apply (nativeC60FICompleteCode_injective_iff_context S F word).mp
    intro a b hab
    exact hlocal a b
      (nativeC60FICompleteCodeCollision_preserves_spine S F word hab)
      hab

end FullRecursiveSpineClassification

section ActualRecursiveInnerObstructions

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- In a fixed ACTUAL dependent 17D boundary fiber, equality of two
genuine OUTER post complete-code images NECESSARILY equates their
entire transported INNER 18D codes. FH extracts original dependent
source/target of that inner code, not a numeric shadow. -/
theorem nativeC60FRPostInner_image_eq_of_collision
    (word : List Bool)
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F a b}
    (r s : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p)
      (nativeC60DRPackSeventeen S F q))
    (h k : NativeC60FGOriginal17Step S F b c)
    (hab : nativeC60FHPostPairTransport S F word (r, h) =
      nativeC60FHPostPairTransport S F word (s, k)) :
    nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F r) =
      nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F s) := by
  have hinner := congrArg (nativeC60FHClosedPostInnerCode S F) hab
  change some (nativeC60DVTransportCompleteCode S F word
      (nativeC60DSCode S F r)) =
    some (nativeC60DVTransportCompleteCode S F word
      (nativeC60DSCode S F s)) at hinner
  exact Option.some.inj hinner

/-- A different ACTUAL transported recursive INNER code prevents
the corresponding OUTER post complete codes from colliding.
No 17D context-injectivity hypothesis is needed. -/
theorem nativeC60FRPost_distinct_inner_no_collision
    (word : List Bool)
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F a b}
    (r s : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p)
      (nativeC60DRPackSeventeen S F q))
    (h k : NativeC60FGOriginal17Step S F b c)
    (hne : nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F r) ≠
      nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F s)) :
    nativeC60FHPostPairTransport S F word (r, h) ≠
      nativeC60FHPostPairTransport S F word (s, k) := by
  intro hab
  exact hne (nativeC60FRPostInner_image_eq_of_collision
    S F word r s h k hab)

/-- The same actual dependent INNER-code necessity for PRE:
the outer prefix may vary, but cannot conceal distinct transported
inner codes under actual unquotiented DV transport. -/
theorem nativeC60FRPreInner_image_eq_of_collision
    (word : List Bool)
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F b c}
    (h k : NativeC60FGOriginal17Step S F a b)
    (r s : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p)
      (nativeC60DRPackSeventeen S F q))
    (hab : nativeC60FHPrePairTransport S F word (h, r) =
      nativeC60FHPrePairTransport S F word (k, s)) :
    nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F r) =
      nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F s) := by
  have hinner := congrArg (nativeC60FHClosedPreInnerCode S F) hab
  change some (nativeC60DVTransportCompleteCode S F word
      (nativeC60DSCode S F r)) =
    some (nativeC60DVTransportCompleteCode S F word
      (nativeC60DSCode S F s)) at hinner
  exact Option.some.inj hinner

/-- An exact PRE outer-code no-collision result from unequal actual
transported recursive inner evidence, with ALL dependent boundaries. -/
theorem nativeC60FRPre_distinct_inner_no_collision
    (word : List Bool)
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F b c}
    (h k : NativeC60FGOriginal17Step S F a b)
    (r s : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p)
      (nativeC60DRPackSeventeen S F q))
    (hne : nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F r) ≠
      nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F s)) :
    nativeC60FHPrePairTransport S F word (h, r) ≠
      nativeC60FHPrePairTransport S F word (k, s) := by
  intro hab
  exact hne (nativeC60FRPreInner_image_eq_of_collision
    S F word h k r s hab)

end ActualRecursiveInnerObstructions

#print axioms nativeC60FRFullPairs_eq_spineUnion
#print axioms nativeC60FRFullKernel_eq_spineNormalClosure
#print axioms nativeC60FRFullRoot_preserves_spine
#print axioms nativeC60FRRootedPairs_eq_spineUnion
#print axioms nativeC60FRFullKernel_eq_spineRootedNormalClosure
#print axioms nativeC60FRFullReceiver_spine_iff
#print axioms nativeC60FRFullReceiver_rooted_iff
#print axioms nativeC60FRContext_injective_iff_spineLocal
#print axioms nativeC60FRPostInner_image_eq_of_collision
#print axioms nativeC60FRPost_distinct_inner_no_collision
#print axioms nativeC60FRPreInner_image_eq_of_collision
#print axioms nativeC60FRPre_distinct_inner_no_collision

end
end Kuu.F112.Physical
