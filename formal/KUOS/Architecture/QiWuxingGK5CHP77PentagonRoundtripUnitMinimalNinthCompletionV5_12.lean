import KUOS.Architecture.QiWuxingGK5CHP77FourfoldMixedMinimalNinthCompletionV5_11

/-!
Qi v5.12 — ORIGINAL PENTAGON ROUNDTRIP / UNIT MINIMAL NINTH COMPLETION.

The actual Qi v5.11 free eighth proof of a pentagon comparison
followed by its reverse has the SAME ORIGINAL SevenRewrite endpoints
as the genuine reflexive eighth proof. Nevertheless the chosen old
ninth grammar cannot join them, because the P-event count is 2 vs 0.

Add precisely ONE new primitive ninth comparison, cancelPentagon,
between these two EXACT original eighth proof values. Retain ALL
former FourfoldMixedNineCell proofs via previous. The constructor
closure follows the same genuinely typed eighth-proof contexts.

On the strictly coarser chosen ninth quotient:
 * the raw P-event count does NOT descend;
 * P-event PARITY and M-event COUNT do descend by Quotient.lift,
   proved by induction through EVERY new ninth constructor;
 * an actual mixed-residue eighth roundtrip still has M-count 2
   versus 0 for a reflexive eighth proof, and therefore remains
   non-comparable in the new grammar.

In addition, construct a real typed overlap of the NEW pentagon
cancellation and the PREVIOUS selected P/M interchange at their
genuine fourfold-mixed seven-cell endpoints. Both ninth histories
exist between the same raw eighth proofs, but their primitive
ninth-event sequences are [cancel,interchange] vs
[interchange,cancel], so the two raw ninth PROOF values are not
strictly equal. This does NOT say a selected tenth-cell comparison
is impossible.

Neither old proofs nor original sources are modified. No universal
thinness, extra axioms, or original strict source equality.
append-only / tighten-only / overwrite-forbidden / same-root.
Public root107; Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uSix
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}
variable
  (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
  (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
  (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
  (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)

namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell
variable {W : Type uSix} {long short : W}

/-- An independent selected ninth comparison: ONE new genuine
roundtrip-to-reflexivity generator, all v5.11 comparisons via
previous, and only the usual well-typed comparison contexts. -/
inductive PentagonCancelNineCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    {s t : SevenRewrite W l r c d} →
    PentagonAssocEightCell W l r s t →
    PentagonAssocEightCell W l r s t → Type uSix where
  | previous {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : FourfoldMixedNineCell W l r q q') :
      PentagonCancelNineCell W l r q q'
  | cancelPentagon :
      PentagonCancelNineCell W l r
        (ninthPentagonRoundtrip l r)
        (ninthPentagonReflexive l r)
  | reverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : PentagonCancelNineCell W l r q q') :
      PentagonCancelNineCell W l r q' q
  | chain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' q'' : PentagonAssocEightCell W l r s t}
      (alpha : PentagonCancelNineCell W l r q q')
      (beta : PentagonCancelNineCell W l r q' q'') :
      PentagonCancelNineCell W l r q q''
  | reverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : PentagonCancelNineCell W l r q q') :
      PentagonCancelNineCell W l r (.reverse q) (.reverse q')
  | chainContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {b b' : PentagonAssocEightCell W l r t u}
      (alpha : PentagonCancelNineCell W l r q q')
      (beta : PentagonCancelNineCell W l r b b') :
      PentagonCancelNineCell W l r (.chain q b) (.chain q' b')
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : PentagonCancelNineCell W l r q q') :
      PentagonCancelNineCell W l r
        (.whiskerLeft before q) (.whiskerLeft before q')
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : PentagonCancelNineCell W l r q q')
      (after : SevenRewrite W l r d e) :
      PentagonCancelNineCell W l r
        (.whiskerRight q after) (.whiskerRight q' after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : PentagonCancelNineCell W l r q q') :
      PentagonCancelNineCell W l r
        (.inverseContext q) (.inverseContext q')
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      {q q' : PentagonAssocEightCell W l r s s'}
      {b b' : PentagonAssocEightCell W l r t t'}
      (alpha : PentagonCancelNineCell W l r q q')
      (beta : PentagonCancelNineCell W l r b b') :
      PentagonCancelNineCell W l r
        (.compositeContext q b) (.compositeContext q' b')

def pentagonCancelNineCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    PentagonCancelNineCell W long short q q :=
  .previous (.strict rfl)

def pentagonCancelNineCell_ofPrevious {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : FourfoldMixedNineCell W long short q q') :
    PentagonCancelNineCell W long short q q' :=
  .previous alpha

theorem ninthPentagonRoundtrip_rawGap (l r : W) :
    ninthPentagonRoundtrip l r ≠ ninthPentagonReflexive l r := by
  intro heq
  have h := congrArg
    (fun q => ninthPrimitiveEventCount true
      (pentagonAssocPrimitiveTrace q)) heq
  have vals := ninthPentagonRoundtripVsReflexiveCounts l r
  rw [vals.1, vals.2] at h
  omega

theorem pentagonCancelNineCell_strictlyNew (l r : W) :
    Nonempty (PentagonCancelNineCell W l r
      (ninthPentagonRoundtrip l r)
      (ninthPentagonReflexive l r)) ∧
    ¬ Nonempty (FourfoldMixedNineCell W l r
      (ninthPentagonRoundtrip l r)
      (ninthPentagonReflexive l r)) ∧
    ninthPentagonRoundtrip l r ≠ ninthPentagonReflexive l r :=
  ⟨⟨.cancelPentagon⟩,
    ninthPentagonRoundtrip_noNineComparison l r,
    ninthPentagonRoundtrip_rawGap l r⟩

theorem pentagonCancelNineCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q q' : PentagonAssocEightCell W l r s t),
      PentagonCancelNineCell W l r q q' →
        FourfoldMixedNineCell W l r q q') := by
  rintro ⟨interpret⟩
  exact ninthPentagonRoundtrip_noNineComparison l r
    ⟨interpret _ _ (.cancelPentagon)⟩

theorem pentagonCancelNineCell_noRawEqualityInterpreter (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q q' : PentagonAssocEightCell W l r s t),
      PentagonCancelNineCell W l r q q' → q = q') := by
  intro interpret
  exact ninthPentagonRoundtrip_rawGap l r
    (interpret _ _ (.cancelPentagon))

/-- The selected ninth quotient is ONLY on parallel, typed ORIGINAL
eighth proofs; it does not touch SevenRewrite or raw six-cell values. -/
def pentagonCancelNinthSetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d} :
    Setoid (PentagonAssocEightCell W l r s t) where
  r := fun q q' => Nonempty (PentagonCancelNineCell W l r q q')
  iseqv := by
    constructor
    · intro q
      exact ⟨pentagonCancelNineCell_refl q⟩
    · intro q q' h
      rcases h with ⟨alpha⟩
      exact ⟨.reverse alpha⟩
    · intro q q' q'' h h'
      rcases h with ⟨alpha⟩
      rcases h' with ⟨beta⟩
      exact ⟨.chain alpha beta⟩

def pentagonCancelNinthClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    Quotient (pentagonCancelNinthSetoid W long short (s := s) (t := t)) :=
  Quotient.mk _ q

theorem pentagonCancelNinthClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q q' : PentagonAssocEightCell W long short s t) :
    pentagonCancelNinthClass q = pentagonCancelNinthClass q' ↔
      Nonempty (PentagonCancelNineCell W long short q q') := by
  constructor
  · intro heq
    exact Quotient.exact heq
  · intro h
    exact Quotient.sound h

theorem oldNinthClass_descendsToPentagonCancel {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q q' : PentagonAssocEightCell W long short s t)
    (h : fourfoldMixedNinthClass q = fourfoldMixedNinthClass q') :
    pentagonCancelNinthClass q = pentagonCancelNinthClass q' := by
  rcases (fourfoldMixedNinthClass_eq_iff q q').1 h with ⟨alpha⟩
  exact (pentagonCancelNinthClass_eq_iff q q').2 ⟨.previous alpha⟩

theorem pentagonCancelNinthClass_strictlyNew (l r : W) :
    (pentagonCancelNinthClass (ninthPentagonRoundtrip l r) =
      pentagonCancelNinthClass (ninthPentagonReflexive l r)) ∧
    (fourfoldMixedNinthClass (ninthPentagonRoundtrip l r) ≠
      fourfoldMixedNinthClass (ninthPentagonReflexive l r)) :=
  ⟨(pentagonCancelNinthClass_eq_iff _ _).2 ⟨.cancelPentagon⟩,
    ninthPentagonRoundtrip_distinctClass l r⟩

/-- Entire raw eighth proof history is NOT recoverable by a
global section left-inverse of this selected new quotient. -/
theorem pentagonCancelNinthClass_noRawRetraction (l r : W) :
    ¬ ∃ (decode :
      Quotient (pentagonCancelNinthSetoid W l r
        (s := sevenFourfoldInversePentagonThree l r)
        (t := sevenFourfoldInversePentagonThree l r)) →
      PentagonAssocEightCell W l r
        (sevenFourfoldInversePentagonThree l r)
        (sevenFourfoldInversePentagonThree l r)),
      ∀ (q : PentagonAssocEightCell W l r
        (sevenFourfoldInversePentagonThree l r)
        (sevenFourfoldInversePentagonThree l r)),
        decode (pentagonCancelNinthClass q) = q := by
  rintro ⟨decode, inverse⟩
  apply ninthPentagonRoundtrip_rawGap l r
  calc
    ninthPentagonRoundtrip l r =
        decode (pentagonCancelNinthClass (ninthPentagonRoundtrip l r)) :=
      (inverse _).symm
    _ = decode (pentagonCancelNinthClass (ninthPentagonReflexive l r)) :=
      congrArg decode (pentagonCancelNinthClass_strictlyNew l r).1
    _ = ninthPentagonReflexive l r := inverse _

/-- M-event count survives even the new cancellation, where it is
0 on BOTH original roundtrip and reflexive eighth proofs. -/
theorem pentagonCancelNineCell_preservesMixedCount
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : PentagonCancelNineCell W long short q q') :
    ninthPrimitiveEventCount false (pentagonAssocPrimitiveTrace q) =
      ninthPrimitiveEventCount false (pentagonAssocPrimitiveTrace q') := by
  induction alpha with
  | previous alpha =>
      exact fourfoldMixedNineCell_preservesEventCount false alpha
  | cancelPentagon => rfl
  | reverse alpha ih => exact ih.symm
  | chain alpha beta ih ih' => exact ih.trans ih'
  | reverseContext alpha ih =>
      simpa only [pentagonAssocPrimitiveTrace,
        ninthPrimitiveEventCount_reverse] using ih
  | chainContext alpha beta ih ih' =>
      simpa only [pentagonAssocPrimitiveTrace,
        ninthPrimitiveEventCount_append] using congrArg₂ Nat.add ih ih'
  | whiskerLeft before alpha ih =>
      simpa only [pentagonAssocPrimitiveTrace] using ih
  | whiskerRight alpha after ih =>
      simpa only [pentagonAssocPrimitiveTrace] using ih
  | inverseContext alpha ih =>
      simpa only [pentagonAssocPrimitiveTrace] using ih
  | compositeContext alpha beta ih ih' =>
      simpa only [pentagonAssocPrimitiveTrace,
        ninthPrimitiveEventCount_append] using congrArg₂ Nat.add ih ih'

/-- The P-count itself is NOT preserved by new cancelPentagon,
but its residue modulo 2 is preserved under EVERY constructor. -/
theorem pentagonCancelNineCell_preservesPentagonParity
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : PentagonCancelNineCell W long short q q') :
    ninthPrimitiveEventCount true (pentagonAssocPrimitiveTrace q) % 2 =
      ninthPrimitiveEventCount true (pentagonAssocPrimitiveTrace q') % 2 := by
  induction alpha with
  | previous alpha =>
      exact congrArg (fun n : Nat => n % 2)
        (fourfoldMixedNineCell_preservesEventCount true alpha)
  | cancelPentagon =>
      have vals := ninthPentagonRoundtripVsReflexiveCounts long short
      rw [vals.1, vals.2]
      decide
  | reverse alpha ih => exact ih.symm
  | chain alpha beta ih ih' => exact ih.trans ih'
  | reverseContext alpha ih =>
      simpa only [pentagonAssocPrimitiveTrace,
        ninthPrimitiveEventCount_reverse] using ih
  | chainContext alpha beta ih ih' =>
      simp only [pentagonAssocPrimitiveTrace,
        ninthPrimitiveEventCount_append] at ih ih' ⊢
      omega
  | whiskerLeft before alpha ih =>
      simpa only [pentagonAssocPrimitiveTrace] using ih
  | whiskerRight alpha after ih =>
      simpa only [pentagonAssocPrimitiveTrace] using ih
  | inverseContext alpha ih =>
      simpa only [pentagonAssocPrimitiveTrace] using ih
  | compositeContext alpha beta ih ih' =>
      simp only [pentagonAssocPrimitiveTrace,
        ninthPrimitiveEventCount_append] at ih ih' ⊢
      omega

/-- Genuine Nat-valued observer on the newly selected ninth quotient. -/
def pentagonCancelNinthMixedCount {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d} :
    Quotient (pentagonCancelNinthSetoid W long short (s := s) (t := t)) →
      Nat :=
  Quotient.lift
    (fun q : PentagonAssocEightCell W long short s t =>
      ninthPrimitiveEventCount false (pentagonAssocPrimitiveTrace q))
    (by
      intro q q' h
      rcases h with ⟨alpha⟩
      exact pentagonCancelNineCell_preservesMixedCount alpha)

/-- Genuine Nat-valued P-parity observer on the NEW ninth quotient. -/
def pentagonCancelNinthPentagonParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d} :
    Quotient (pentagonCancelNinthSetoid W long short (s := s) (t := t)) →
      Nat :=
  Quotient.lift
    (fun q : PentagonAssocEightCell W long short s t =>
      ninthPrimitiveEventCount true (pentagonAssocPrimitiveTrace q) % 2)
    (by
      intro q q' h
      rcases h with ⟨alpha⟩
      exact pentagonCancelNineCell_preservesPentagonParity alpha)

theorem pentagonCancelNinthMixedCount_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    pentagonCancelNinthMixedCount (pentagonCancelNinthClass q) =
      ninthPrimitiveEventCount false (pentagonAssocPrimitiveTrace q) := rfl

theorem pentagonCancelNinthPentagonParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    pentagonCancelNinthPentagonParity (pentagonCancelNinthClass q) =
      ninthPrimitiveEventCount true (pentagonAssocPrimitiveTrace q) % 2 := rfl

/-- The former P-count observer cannot descend: the specific
roundtrip and reflexive histories become equal in the new quotient
but have original P-count 2 and 0. -/
theorem pentagonCancelNinthClass_noPentagonCountDescent (l r : W) :
    ¬ ∃ (observe :
      Quotient (pentagonCancelNinthSetoid W l r
        (s := sevenFourfoldInversePentagonThree l r)
        (t := sevenFourfoldInversePentagonThree l r)) → Nat),
      ∀ (q : PentagonAssocEightCell W l r
        (sevenFourfoldInversePentagonThree l r)
        (sevenFourfoldInversePentagonThree l r)),
        observe (pentagonCancelNinthClass q) =
          ninthPrimitiveEventCount true (pentagonAssocPrimitiveTrace q) := by
  rintro ⟨observe, compatible⟩
  have h := congrArg observe (pentagonCancelNinthClass_strictlyNew l r).1
  have vals := ninthPentagonRoundtripVsReflexiveCounts l r
  rw [compatible (ninthPentagonRoundtrip l r),
    compatible (ninthPentagonReflexive l r),
    vals.1, vals.2] at h
  omega

theorem pentagonCancelNinthRoundtripParityValues (l r : W) :
    pentagonCancelNinthPentagonParity
        (pentagonCancelNinthClass (ninthPentagonRoundtrip l r)) = 0 ∧
    pentagonCancelNinthPentagonParity
        (pentagonCancelNinthClass (ninthPentagonReflexive l r)) = 0 ∧
    pentagonCancelNinthMixedCount
        (pentagonCancelNinthClass (ninthPentagonRoundtrip l r)) = 0 ∧
    pentagonCancelNinthMixedCount
        (pentagonCancelNinthClass (ninthPentagonReflexive l r)) = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;>
    simp only [pentagonCancelNinthPentagonParity_onClass,
      pentagonCancelNinthMixedCount_onClass] <;>
    rfl

/-- ACTUAL old mixed-residue comparison, followed by its formal
eighth inverse, still has the same true seven-cell endpoints as
an old reflexive eighth comparison. It contains TWO M events. -/
def ninthMixedRoundtrip (l r : W) :
    PentagonAssocEightCell W l r
      (sevenMixedResidueFirst (long := l) (short := r) r)
      (sevenMixedResidueFirst (long := l) (short := r) r) :=
  .chain (.previous (.mixedResidue r))
    (.reverse (.previous (.mixedResidue r)))

def ninthMixedReflexive (l r : W) :
    PentagonAssocEightCell W l r
      (sevenMixedResidueFirst (long := l) (short := r) r)
      (sevenMixedResidueFirst (long := l) (short := r) r) :=
  pentagonAssocEightCell_refl
    (sevenMixedResidueFirst (long := l) (short := r) r)

theorem ninthMixedRoundtripVsReflexiveCounts (l r : W) :
    ninthPrimitiveEventCount false
        (pentagonAssocPrimitiveTrace (ninthMixedRoundtrip l r)) = 2 ∧
    ninthPrimitiveEventCount false
        (pentagonAssocPrimitiveTrace (ninthMixedReflexive l r)) = 0 := by
  constructor <;> rfl

/-- A true residual obstruction remains even AFTER cancelling
the pentagon eighth roundtrip: M-count 2 vs 0. -/
theorem ninthMixedRoundtrip_noPentagonCancelComparison (l r : W) :
    ¬ Nonempty (PentagonCancelNineCell W l r
      (ninthMixedRoundtrip l r)
      (ninthMixedReflexive l r)) := by
  rintro ⟨alpha⟩
  have h := pentagonCancelNineCell_preservesMixedCount alpha
  have vals := ninthMixedRoundtripVsReflexiveCounts l r
  rw [vals.1, vals.2] at h
  omega

theorem ninthMixedRoundtrip_distinctCancelClass (l r : W) :
    pentagonCancelNinthClass (ninthMixedRoundtrip l r) ≠
      pentagonCancelNinthClass (ninthMixedReflexive l r) := by
  intro h
  exact ninthMixedRoundtrip_noPentagonCancelComparison l r
    ((pentagonCancelNinthClass_eq_iff _ _).1 h)

theorem pentagonCancelNineCell_notGloballyThin (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q q' : PentagonAssocEightCell W l r s t),
      Nonempty (PentagonCancelNineCell W l r q q')) := by
  intro interpret
  exact ninthMixedRoundtrip_noPentagonCancelComparison l r
    (interpret _ _)

/-! ## Actual critical overlap: old P/M interchange against new P cancellation. -/

/-- Original fourfold-mixed NW SevenRewrite is the composite
of H3 and the ACTUAL original mixed-residue first history. -/
def fourfoldMixedPentagonRoundtripNW (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueFirst l r) :=
  .compositeContext (ninthPentagonRoundtrip l r)
    (pentagonAssocEightCell_refl
      (sevenMixedResidueFirst (long := l) (short := r) r))

def fourfoldMixedPentagonReflexiveNW (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueFirst l r) :=
  .compositeContext (ninthPentagonReflexive l r)
    (pentagonAssocEightCell_refl
      (sevenMixedResidueFirst (long := l) (short := r) r))

/-- A genuine new ninth cancellation in the ORIGINAL composite
of the P77 fourfold history and the mixedResidue history. -/
def fourfoldMixedPentagonCancelNW (l r : W) :
    PentagonCancelNineCell W l r
      (fourfoldMixedPentagonRoundtripNW l r)
      (fourfoldMixedPentagonReflexiveNW l r) :=
  .compositeContext (.cancelPentagon) (.previous (.strict rfl))

def fourfoldMixedCancelOverlapTopLeft (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r) :=
  .chain (fourfoldMixedPentagonRoundtripNW l r)
    (fourfoldMixedCriticalPThenM l r)

def fourfoldMixedCancelOverlapTopRight (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r) :=
  .chain (fourfoldMixedPentagonRoundtripNW l r)
    (fourfoldMixedCriticalMThenP l r)

def fourfoldMixedCancelOverlapBottomLeft (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r) :=
  .chain (fourfoldMixedPentagonReflexiveNW l r)
    (fourfoldMixedCriticalPThenM l r)

def fourfoldMixedCancelOverlapBottomRight (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueSecond l r) :=
  .chain (fourfoldMixedPentagonReflexiveNW l r)
    (fourfoldMixedCriticalMThenP l r)

/-- TOP old P/M ninth interchange, lifted through the true
pentagon-roundtrip left eighth context. -/
def fourfoldMixedCancelOverlapTop (l r : W) :
    PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopLeft l r)
      (fourfoldMixedCancelOverlapTopRight l r) :=
  .previous (.chainContext (.strict rfl) (.interchange))

/-- BOTTOM old P/M interchange, now with the genuine original
pentagon-reflexive eighth prefix. -/
def fourfoldMixedCancelOverlapBottom (l r : W) :
    PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapBottomLeft l r)
      (fourfoldMixedCancelOverlapBottomRight l r) :=
  .previous (.chainContext (.strict rfl) (.interchange))

/-- LEFT new cancellation, whiskered with the actual old
P-then-M eighth history without an equality shortcut. -/
def fourfoldMixedCancelOverlapLeft (l r : W) :
    PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopLeft l r)
      (fourfoldMixedCancelOverlapBottomLeft l r) :=
  .chainContext (fourfoldMixedPentagonCancelNW l r)
    (pentagonCancelNineCell_refl (fourfoldMixedCriticalPThenM l r))

/-- RIGHT new cancellation, whiskered with the actual old
M-then-P eighth history. -/
def fourfoldMixedCancelOverlapRight (l r : W) :
    PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopRight l r)
      (fourfoldMixedCancelOverlapBottomRight l r) :=
  .chainContext (fourfoldMixedPentagonCancelNW l r)
    (pentagonCancelNineCell_refl (fourfoldMixedCriticalMThenP l r))

/-- A complete typed ninth proof history: cancel then interchange. -/
def fourfoldMixedCancelThenInterchange (l r : W) :
    PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopLeft l r)
      (fourfoldMixedCancelOverlapBottomRight l r) :=
  .chain (fourfoldMixedCancelOverlapLeft l r)
    (fourfoldMixedCancelOverlapBottom l r)

/-- Another complete typed ninth proof history with the SAME
eighth proof endpoints: interchange then cancel. -/
def fourfoldMixedInterchangeThenCancel (l r : W) :
    PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopLeft l r)
      (fourfoldMixedCancelOverlapBottomRight l r) :=
  .chain (fourfoldMixedCancelOverlapTop l r)
    (fourfoldMixedCancelOverlapRight l r)

theorem fourfoldMixedCancelCriticalDiamond (l r : W) :
    Nonempty (PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopLeft l r)
      (fourfoldMixedCancelOverlapTopRight l r)) ∧
    Nonempty (PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopLeft l r)
      (fourfoldMixedCancelOverlapBottomLeft l r)) ∧
    Nonempty (PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopRight l r)
      (fourfoldMixedCancelOverlapBottomRight l r)) ∧
    Nonempty (PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapBottomLeft l r)
      (fourfoldMixedCancelOverlapBottomRight l r)) ∧
    Nonempty (PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopLeft l r)
      (fourfoldMixedCancelOverlapBottomRight l r)) :=
  ⟨⟨fourfoldMixedCancelOverlapTop l r⟩,
    ⟨fourfoldMixedCancelOverlapLeft l r⟩,
    ⟨fourfoldMixedCancelOverlapRight l r⟩,
    ⟨fourfoldMixedCancelOverlapBottom l r⟩,
    ⟨fourfoldMixedCancelThenInterchange l r⟩⟩

/-- Syntactic trace of the ONE old original ninth interchange
primitive, preserving all typed ninth comparison contexts. -/
def oldNinthInterchangeTrace {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : FourfoldMixedNineCell W long short q q') : List Bool :=
  match alpha with
  | .strict _ => []
  | .interchange => [false]
  | .reverse alpha => (oldNinthInterchangeTrace alpha).reverse
  | .chain alpha beta =>
      oldNinthInterchangeTrace alpha ++ oldNinthInterchangeTrace beta
  | .reverseContext alpha => oldNinthInterchangeTrace alpha
  | .chainContext alpha beta =>
      oldNinthInterchangeTrace alpha ++ oldNinthInterchangeTrace beta
  | .whiskerLeft _ alpha => oldNinthInterchangeTrace alpha
  | .whiskerRight alpha _ => oldNinthInterchangeTrace alpha
  | .inverseContext alpha => oldNinthInterchangeTrace alpha
  | .compositeContext alpha beta =>
      oldNinthInterchangeTrace alpha ++ oldNinthInterchangeTrace beta

/-- A strictly RAW ninth proof event trace: true is newly adjoined
cancelPentagon, false is the original genuine P/M interchange.
It is NOT declared invariant under any future tenth-cell relation. -/
def pentagonCancelNinePrimitiveTrace {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : PentagonCancelNineCell W long short q q') : List Bool :=
  match alpha with
  | .previous old => oldNinthInterchangeTrace old
  | .cancelPentagon => [true]
  | .reverse alpha => (pentagonCancelNinePrimitiveTrace alpha).reverse
  | .chain alpha beta =>
      pentagonCancelNinePrimitiveTrace alpha ++ pentagonCancelNinePrimitiveTrace beta
  | .reverseContext alpha => pentagonCancelNinePrimitiveTrace alpha
  | .chainContext alpha beta =>
      pentagonCancelNinePrimitiveTrace alpha ++ pentagonCancelNinePrimitiveTrace beta
  | .whiskerLeft _ alpha => pentagonCancelNinePrimitiveTrace alpha
  | .whiskerRight alpha _ => pentagonCancelNinePrimitiveTrace alpha
  | .inverseContext alpha => pentagonCancelNinePrimitiveTrace alpha
  | .compositeContext alpha beta =>
      pentagonCancelNinePrimitiveTrace alpha ++ pentagonCancelNinePrimitiveTrace beta

theorem fourfoldMixedCancelInterchangeTraceValues (l r : W) :
    pentagonCancelNinePrimitiveTrace
        (fourfoldMixedCancelThenInterchange l r) = [true, false] ∧
    pentagonCancelNinePrimitiveTrace
        (fourfoldMixedInterchangeThenCancel l r) = [false, true] := by
  constructor <;> rfl

/-- The two genuine ninth proof histories inhabit the same
typed comparison but remain unequal ORIGINAL raw ninth Type values.
No nonexistence of tenth-cell comparison is claimed. -/
theorem fourfoldMixedCancelInterchangeRawNineGap (l r : W) :
    fourfoldMixedCancelThenInterchange l r ≠
      fourfoldMixedInterchangeThenCancel l r := by
  intro h
  have ht := congrArg pentagonCancelNinePrimitiveTrace h
  rw [(fourfoldMixedCancelInterchangeTraceValues l r).1,
    (fourfoldMixedCancelInterchangeTraceValues l r).2] at ht
  cases ht

/-- The new ninth comparison at the actual overlap preserves
the original v5.09 V/R/U parity observation of the underlying
seven-cell endpoints; no original seven-cell Eq is created. -/
theorem fourfoldMixedCancelOverlapParityCompatibility (l r : W) :
    Nonempty (PentagonCancelNineCell W l r
      (fourfoldMixedCancelOverlapTopLeft l r)
      (fourfoldMixedCancelOverlapBottomRight l r)) ∧
    sevenTotalReductionParity (fourfoldMixedResidueFirst l r) =
      sevenTotalReductionParity (fourfoldMixedResidueSecond l r) ∧
    sevenIdentityParity (fourfoldMixedResidueFirst l r) =
      sevenIdentityParity (fourfoldMixedResidueSecond l r) ∧
    sevenUnitCountParity (fourfoldMixedResidueFirst l r) =
      sevenUnitCountParity (fourfoldMixedResidueSecond l r) :=
  ⟨⟨fourfoldMixedCancelThenInterchange l r⟩,
    (fourfoldMixedCriticalParityCompatibility l r).1,
    (fourfoldMixedCriticalParityCompatibility l r).2.1,
    (fourfoldMixedCriticalParityCompatibility l r).2.2⟩

end PentagonAdjoinedSixCell

section ActualOriginalP77PentagonCancelCompletion
variable {u v : FivefoldPathVertex}
variable {family₀ family₁ family₂ family₃ family₄ : Family f g h k u v}
variable {s₀ : State f g h k family₀}
variable {s₁ : State f g h k family₁}
variable {s₂ : State f g h k family₂}
variable {s₃ : State f g h k family₃}
variable {s₄ : State f g h k family₄}
variable (A : DirectNormalBracketTree f g h k family₀ s₀ family₁ s₁)
variable (B : DirectNormalBracketTree f g h k family₁ s₁ family₂ s₂)
variable (C : DirectNormalBracketTree f g h k family₂ s₂ family₃ s₃)
variable (D₄ : DirectNormalBracketTree f g h k family₃ s₃ family₄ s₄)

/-- The single new ninth cancellation exists at EVERY genuinely
sourced final P77 raw index, while the original F55/P77/GK5CG
strict source equality interpretation remains impossible. -/
theorem pentagonActualRoundtripUnitNinthCompletion
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.PentagonCancelNineCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.ninthPentagonRoundtrip
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.ninthPentagonReflexive
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨⟨.cancelPentagon⟩,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.PentagonCancelNineCell
#print axioms PentagonAdjoinedSixCell.pentagonCancelNineCell_refl
#print axioms PentagonAdjoinedSixCell.pentagonCancelNineCell_ofPrevious
#print axioms PentagonAdjoinedSixCell.ninthPentagonRoundtrip_rawGap
#print axioms PentagonAdjoinedSixCell.pentagonCancelNineCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.pentagonCancelNineCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.pentagonCancelNineCell_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthSetoid
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthClass
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthClass_eq_iff
#print axioms PentagonAdjoinedSixCell.oldNinthClass_descendsToPentagonCancel
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthClass_noRawRetraction
#print axioms PentagonAdjoinedSixCell.pentagonCancelNineCell_preservesMixedCount
#print axioms PentagonAdjoinedSixCell.pentagonCancelNineCell_preservesPentagonParity
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthMixedCount
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthPentagonParity
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthMixedCount_onClass
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthPentagonParity_onClass
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthClass_noPentagonCountDescent
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthRoundtripParityValues
#print axioms PentagonAdjoinedSixCell.ninthMixedRoundtrip
#print axioms PentagonAdjoinedSixCell.ninthMixedReflexive
#print axioms PentagonAdjoinedSixCell.ninthMixedRoundtripVsReflexiveCounts
#print axioms PentagonAdjoinedSixCell.ninthMixedRoundtrip_noPentagonCancelComparison
#print axioms PentagonAdjoinedSixCell.ninthMixedRoundtrip_distinctCancelClass
#print axioms PentagonAdjoinedSixCell.pentagonCancelNineCell_notGloballyThin
#print axioms PentagonAdjoinedSixCell.fourfoldMixedPentagonRoundtripNW
#print axioms PentagonAdjoinedSixCell.fourfoldMixedPentagonReflexiveNW
#print axioms PentagonAdjoinedSixCell.fourfoldMixedPentagonCancelNW
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelOverlapTopLeft
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelOverlapTopRight
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelOverlapBottomLeft
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelOverlapBottomRight
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelOverlapTop
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelOverlapBottom
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelOverlapLeft
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelOverlapRight
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelThenInterchange
#print axioms PentagonAdjoinedSixCell.fourfoldMixedInterchangeThenCancel
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelCriticalDiamond
#print axioms PentagonAdjoinedSixCell.oldNinthInterchangeTrace
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinePrimitiveTrace
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelInterchangeTraceValues
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelInterchangeRawNineGap
#print axioms PentagonAdjoinedSixCell.fourfoldMixedCancelOverlapParityCompatibility
#print axioms pentagonActualRoundtripUnitNinthCompletion

end ActualOriginalP77PentagonCancelCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
