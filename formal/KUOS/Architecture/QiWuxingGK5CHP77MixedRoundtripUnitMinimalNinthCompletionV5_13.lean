import KUOS.Architecture.QiWuxingGK5CHP77PentagonRoundtripUnitMinimalNinthCompletionV5_12

/-!
Qi v5.13 — TRUE MIXED-RESIDUE ROUNDTRIP/UNIT NINTH COMPLETION.

Qi v5.12 compares the original P-roundtrip and original reflexive
eighth proofs, but proves the old mixedResidue roundtrip and original
reflexive eighth proof cannot be compared in its chosen ninth grammar:
their original M-primitive occurrence counts are 2 and 0.

Add exactly ONE new, genuinely typed comparison primitive cancelMixed
between these two original eighth-cell values. Keep ALL earlier
PentagonCancelNineCell evidence via previous. All other constructors
are typed reversals, chains and inherited eight-proof contexts.

For the resulting selected quotient:
 - old M occurrence COUNT does not descend;
 - P parity and M parity descend by actual Quotient.lift and full
   structural induction through every new comparison constructor.
A new independent integer-valued raw-eighth complexity invariant
is preserved by ALL original ninth grammars and the newly selected
mixed cancellation. It separates the chain of two original
reflexive eighth proofs from one original reflexive proof, despite
equal P/M counts (both zero). Thus global thinness remains false.

Construct a genuine original GK5CG/P77-anchored P-cancellation versus
M-cancellation higher critical diamond: two independent typed
ninth proof histories are constructed between exactly the same
raw eighth values. Their primitive ninth-event order differs,
hence strict raw ninth equality does not hold. This does NOT
exclude a future tenth-cell comparison between these histories.

No modification of original F55/P77/GK5CG, old independent
six/seven/eighth/ninth grammars, raw evidence or pinned toolchain.
No added axioms; no universal thinness or source strict Eq.
append-only / tighten-only / overwrite-forbidden / same-root.
Public root 107; Lean v4.30.0-rc2; pinned mathlib
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

/-- Independently typed ninth grammar with ONE new genuine generator:
the exact previously obstructed original M-roundtrip/reflexive pair. -/
inductive MixedCancelNineCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    {s t : SevenRewrite W l r c d} →
    PentagonAssocEightCell W l r s t →
    PentagonAssocEightCell W l r s t → Type uSix where
  | previous {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : PentagonCancelNineCell W l r q q') :
      MixedCancelNineCell W l r q q'
  | cancelMixed :
      MixedCancelNineCell W l r
        (ninthMixedRoundtrip l r)
        (ninthMixedReflexive l r)
  | reverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : MixedCancelNineCell W l r q q') :
      MixedCancelNineCell W l r q' q
  | chain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' q'' : PentagonAssocEightCell W l r s t}
      (alpha : MixedCancelNineCell W l r q q')
      (beta : MixedCancelNineCell W l r q' q'') :
      MixedCancelNineCell W l r q q''
  | reverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : MixedCancelNineCell W l r q q') :
      MixedCancelNineCell W l r (.reverse q) (.reverse q')
  | chainContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {b b' : PentagonAssocEightCell W l r t u}
      (alpha : MixedCancelNineCell W l r q q')
      (beta : MixedCancelNineCell W l r b b') :
      MixedCancelNineCell W l r (.chain q b) (.chain q' b')
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : MixedCancelNineCell W l r q q') :
      MixedCancelNineCell W l r
        (.whiskerLeft before q) (.whiskerLeft before q')
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : MixedCancelNineCell W l r q q')
      (after : SevenRewrite W l r d e) :
      MixedCancelNineCell W l r
        (.whiskerRight q after) (.whiskerRight q' after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      (alpha : MixedCancelNineCell W l r q q') :
      MixedCancelNineCell W l r
        (.inverseContext q) (.inverseContext q')
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      {q q' : PentagonAssocEightCell W l r s s'}
      {b b' : PentagonAssocEightCell W l r t t'}
      (alpha : MixedCancelNineCell W l r q q')
      (beta : MixedCancelNineCell W l r b b') :
      MixedCancelNineCell W l r
        (.compositeContext q b) (.compositeContext q' b')

def mixedCancelNineCell_refl {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    MixedCancelNineCell W long short q q :=
  .previous (pentagonCancelNineCell_refl q)

def mixedCancelNineCell_ofPrevious {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : PentagonCancelNineCell W long short q q') :
    MixedCancelNineCell W long short q q' :=
  .previous alpha

/-- The new comparison is impossible in the old v5.12 grammar
and cannot be a strict equality of the old eighth proof values. -/
theorem ninthMixedRoundtrip_rawGap (l r : W) :
    ninthMixedRoundtrip l r ≠ ninthMixedReflexive l r := by
  intro heq
  have h := congrArg
    (fun q => ninthPrimitiveEventCount false
      (pentagonAssocPrimitiveTrace q)) heq
  change
    ninthPrimitiveEventCount false
        (pentagonAssocPrimitiveTrace (ninthMixedRoundtrip l r)) =
      ninthPrimitiveEventCount false
        (pentagonAssocPrimitiveTrace (ninthMixedReflexive l r)) at h
  have vals := ninthMixedRoundtripVsReflexiveCounts l r
  rw [vals.1, vals.2] at h
  omega

theorem mixedCancelNineCell_strictlyNew (l r : W) :
    Nonempty (MixedCancelNineCell W l r
      (ninthMixedRoundtrip l r)
      (ninthMixedReflexive l r)) ∧
    ¬ Nonempty (PentagonCancelNineCell W l r
      (ninthMixedRoundtrip l r)
      (ninthMixedReflexive l r)) ∧
    ninthMixedRoundtrip l r ≠ ninthMixedReflexive l r :=
  ⟨⟨.cancelMixed⟩,
    ninthMixedRoundtrip_noPentagonCancelComparison l r,
    ninthMixedRoundtrip_rawGap l r⟩

theorem mixedCancelNineCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q q' : PentagonAssocEightCell W l r s t),
      MixedCancelNineCell W l r q q' →
        PentagonCancelNineCell W l r q q') := by
  rintro ⟨interpret⟩
  exact ninthMixedRoundtrip_noPentagonCancelComparison l r
    ⟨interpret _ _ (.cancelMixed)⟩

theorem mixedCancelNineCell_noRawEqualityInterpreter (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q q' : PentagonAssocEightCell W l r s t),
      MixedCancelNineCell W l r q q' → q = q') := by
  intro interpret
  exact ninthMixedRoundtrip_rawGap l r
    (interpret _ _ (.cancelMixed))

/-- Setoid and chosen quotient on the original eighth proof Type;
the previous selected ninth Setoid and its source are untouched. -/
def mixedCancelNinthSetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d} :
    Setoid (PentagonAssocEightCell W l r s t) where
  r := fun q q' => Nonempty (MixedCancelNineCell W l r q q')
  iseqv := by
    constructor
    · intro q
      exact ⟨mixedCancelNineCell_refl q⟩
    · intro q q' h
      rcases h with ⟨alpha⟩
      exact ⟨.reverse alpha⟩
    · intro q q' q'' h h'
      rcases h with ⟨alpha⟩
      rcases h' with ⟨beta⟩
      exact ⟨.chain alpha beta⟩

def mixedCancelNinthClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    Quotient (mixedCancelNinthSetoid W long short (s := s) (t := t)) :=
  Quotient.mk _ q

theorem mixedCancelNinthClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q q' : PentagonAssocEightCell W long short s t) :
    mixedCancelNinthClass q = mixedCancelNinthClass q' ↔
      Nonempty (MixedCancelNineCell W long short q q') := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem pentagonCancelNinthClass_descendsToMixedCancel {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q q' : PentagonAssocEightCell W long short s t)
    (h : pentagonCancelNinthClass q = pentagonCancelNinthClass q') :
    mixedCancelNinthClass q = mixedCancelNinthClass q' := by
  rcases (pentagonCancelNinthClass_eq_iff q q').1 h with ⟨alpha⟩
  exact (mixedCancelNinthClass_eq_iff q q').2 ⟨.previous alpha⟩

theorem mixedCancelNinthClass_strictlyNew (l r : W) :
    (mixedCancelNinthClass (ninthMixedRoundtrip l r) =
      mixedCancelNinthClass (ninthMixedReflexive l r)) ∧
    (pentagonCancelNinthClass (ninthMixedRoundtrip l r) ≠
      pentagonCancelNinthClass (ninthMixedReflexive l r)) :=
  ⟨(mixedCancelNinthClass_eq_iff _ _).2 ⟨.cancelMixed⟩,
    ninthMixedRoundtrip_distinctCancelClass l r⟩

theorem mixedCancelNinthClass_noRawRetraction (l r : W) :
    ¬ ∃ (decode :
      Quotient (mixedCancelNinthSetoid W l r
        (s := sevenMixedResidueFirst (long := l) (short := r) r)
        (t := sevenMixedResidueFirst (long := l) (short := r) r)) →
      PentagonAssocEightCell W l r
        (sevenMixedResidueFirst (long := l) (short := r) r)
        (sevenMixedResidueFirst (long := l) (short := r) r)),
      ∀ (q : PentagonAssocEightCell W l r
        (sevenMixedResidueFirst (long := l) (short := r) r)
        (sevenMixedResidueFirst (long := l) (short := r) r)),
        decode (mixedCancelNinthClass q) = q := by
  rintro ⟨decode, inv⟩
  apply ninthMixedRoundtrip_rawGap l r
  calc
    ninthMixedRoundtrip l r =
        decode (mixedCancelNinthClass (ninthMixedRoundtrip l r)) :=
      (inv _).symm
    _ = decode (mixedCancelNinthClass (ninthMixedReflexive l r)) :=
      congrArg decode (mixedCancelNinthClass_strictlyNew l r).1
    _ = ninthMixedReflexive l r := inv _

/-- The new selected comparison preserves P-event parity. -/
theorem mixedCancelNineCell_preservesPentagonParity
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    ninthPrimitiveEventCount true (pentagonAssocPrimitiveTrace q) % 2 =
      ninthPrimitiveEventCount true (pentagonAssocPrimitiveTrace q') % 2 := by
  induction alpha with
  | previous alpha =>
      exact pentagonCancelNineCell_preservesPentagonParity alpha
  | cancelMixed => rfl
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

/-- M-event count cannot be conserved across the new generator,
but its parity is conserved in EVERY typed ninth-cell context. -/
theorem mixedCancelNineCell_preservesMixedParity
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    ninthPrimitiveEventCount false (pentagonAssocPrimitiveTrace q) % 2 =
      ninthPrimitiveEventCount false (pentagonAssocPrimitiveTrace q') % 2 := by
  induction alpha with
  | previous alpha =>
      exact congrArg (fun n : Nat => n % 2)
        (pentagonCancelNineCell_preservesMixedCount alpha)
  | cancelMixed =>
      have vals := ninthMixedRoundtripVsReflexiveCounts long short
      rw [vals.1, vals.2]
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

/-- Both parity observers are defined by actual Quotient.lift,
not by adding semantic equality of any original eighth evidence. -/
def mixedCancelNinthPentagonParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d} :
    Quotient (mixedCancelNinthSetoid W long short (s := s) (t := t)) →
      Nat :=
  Quotient.lift
    (fun q : PentagonAssocEightCell W long short s t =>
      ninthPrimitiveEventCount true (pentagonAssocPrimitiveTrace q) % 2)
    (by
      intro q q' h
      rcases h with ⟨alpha⟩
      exact mixedCancelNineCell_preservesPentagonParity alpha)

def mixedCancelNinthMixedParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d} :
    Quotient (mixedCancelNinthSetoid W long short (s := s) (t := t)) →
      Nat :=
  Quotient.lift
    (fun q : PentagonAssocEightCell W long short s t =>
      ninthPrimitiveEventCount false (pentagonAssocPrimitiveTrace q) % 2)
    (by
      intro q q' h
      rcases h with ⟨alpha⟩
      exact mixedCancelNineCell_preservesMixedParity alpha)

theorem mixedCancelNinthPentagonParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    mixedCancelNinthPentagonParity (mixedCancelNinthClass q) =
      ninthPrimitiveEventCount true (pentagonAssocPrimitiveTrace q) % 2 := rfl

theorem mixedCancelNinthMixedParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    mixedCancelNinthMixedParity (mixedCancelNinthClass q) =
      ninthPrimitiveEventCount false (pentagonAssocPrimitiveTrace q) % 2 := rfl

/-- M-count itself no longer descends: original count 2 versus 0
on the specific new pair that has equal chosen ninth classes. -/
theorem mixedCancelNinthClass_noMixedCountDescent (l r : W) :
    ¬ ∃ (observe :
      Quotient (mixedCancelNinthSetoid W l r
        (s := sevenMixedResidueFirst (long := l) (short := r) r)
        (t := sevenMixedResidueFirst (long := l) (short := r) r)) → Nat),
      ∀ (q : PentagonAssocEightCell W l r
        (sevenMixedResidueFirst (long := l) (short := r) r)
        (sevenMixedResidueFirst (long := l) (short := r) r)),
        observe (mixedCancelNinthClass q) =
          ninthPrimitiveEventCount false (pentagonAssocPrimitiveTrace q) := by
  rintro ⟨observe, compatible⟩
  have h := congrArg observe (mixedCancelNinthClass_strictlyNew l r).1
  have vals := ninthMixedRoundtripVsReflexiveCounts l r
  rw [compatible (ninthMixedRoundtrip l r),
    compatible (ninthMixedReflexive l r),
    vals.1, vals.2] at h
  omega

/-- A new raw eighth structural invariant that is sensitive to the
actual free eighth CHAIN constructor. An old mixedResidue occurrence
and the one fourfoldPentagon occurrence both have charge -1.
Each eighth chain adds +2. All original contexts are respected. -/
def ninthResidualChainCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) : ℤ :=
  match q with
  | .previous old =>
      - (ninthPrimitiveEventCount false
          (mixedResiduePrimitiveTrace old) : ℤ)
  | .fourfoldPentagon => -1
  | .reverse q => ninthResidualChainCharge q
  | .chain q b =>
      ninthResidualChainCharge q + ninthResidualChainCharge b + 2
  | .whiskerLeft _ q => ninthResidualChainCharge q
  | .whiskerRight q _ => ninthResidualChainCharge q
  | .inverseContext q => ninthResidualChainCharge q
  | .compositeContext q b =>
      ninthResidualChainCharge q + ninthResidualChainCharge b

/-- Structural conservation for EVERY original Qi v5.11 ninth
constructor; the actual P/M interchange has equal net charge. -/
theorem fourfoldMixedNineCell_preservesResidualChainCharge
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : FourfoldMixedNineCell W long short q q') :
    ninthResidualChainCharge q = ninthResidualChainCharge q' := by
  induction alpha with
  | strict heq => cases heq; rfl
  | interchange => rfl
  | reverse alpha ih => exact ih.symm
  | chain alpha beta ih ih' => exact ih.trans ih'
  | reverseContext alpha ih =>
      simpa only [ninthResidualChainCharge] using ih
  | chainContext alpha beta ih ih' =>
      simpa only [ninthResidualChainCharge] using
        congrArg₂ (fun a b : ℤ => a + b + 2) ih ih'
  | whiskerLeft before alpha ih =>
      simpa only [ninthResidualChainCharge] using ih
  | whiskerRight alpha after ih =>
      simpa only [ninthResidualChainCharge] using ih
  | inverseContext alpha ih =>
      simpa only [ninthResidualChainCharge] using ih
  | compositeContext alpha beta ih ih' =>
      simpa only [ninthResidualChainCharge] using
        congrArg₂ (fun a b : ℤ => a + b) ih ih'

theorem pentagonCancelNineCell_preservesResidualChainCharge
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : PentagonCancelNineCell W long short q q') :
    ninthResidualChainCharge q = ninthResidualChainCharge q' := by
  induction alpha with
  | previous alpha =>
      exact fourfoldMixedNineCell_preservesResidualChainCharge alpha
  | cancelPentagon => rfl
  | reverse alpha ih => exact ih.symm
  | chain alpha beta ih ih' => exact ih.trans ih'
  | reverseContext alpha ih =>
      simpa only [ninthResidualChainCharge] using ih
  | chainContext alpha beta ih ih' =>
      simpa only [ninthResidualChainCharge] using
        congrArg₂ (fun a b : ℤ => a + b + 2) ih ih'
  | whiskerLeft before alpha ih =>
      simpa only [ninthResidualChainCharge] using ih
  | whiskerRight alpha after ih =>
      simpa only [ninthResidualChainCharge] using ih
  | inverseContext alpha ih =>
      simpa only [ninthResidualChainCharge] using ih
  | compositeContext alpha beta ih ih' =>
      simpa only [ninthResidualChainCharge] using
        congrArg₂ (fun a b : ℤ => a + b) ih ih'

/-- Full-constructor invariance of the new structural charge, even
after adjoining the one genuine mixed-residue cancellation. -/
theorem mixedCancelNineCell_preservesResidualChainCharge
    {w z : W} {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') :
    ninthResidualChainCharge q = ninthResidualChainCharge q' := by
  induction alpha with
  | previous alpha =>
      exact pentagonCancelNineCell_preservesResidualChainCharge alpha
  | cancelMixed => rfl
  | reverse alpha ih => exact ih.symm
  | chain alpha beta ih ih' => exact ih.trans ih'
  | reverseContext alpha ih =>
      simpa only [ninthResidualChainCharge] using ih
  | chainContext alpha beta ih ih' =>
      simpa only [ninthResidualChainCharge] using
        congrArg₂ (fun a b : ℤ => a + b + 2) ih ih'
  | whiskerLeft before alpha ih =>
      simpa only [ninthResidualChainCharge] using ih
  | whiskerRight alpha after ih =>
      simpa only [ninthResidualChainCharge] using ih
  | inverseContext alpha ih =>
      simpa only [ninthResidualChainCharge] using ih
  | compositeContext alpha beta ih ih' =>
      simpa only [ninthResidualChainCharge] using
        congrArg₂ (fun a b : ℤ => a + b) ih ih'

/-- A third, genuinely integer-valued quotient observer: it
retains free eighth proof composition structure modulo the TWO
selected original cancellation laws and prior interchange. -/
def mixedCancelNinthResidualCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d} :
    Quotient (mixedCancelNinthSetoid W long short (s := s) (t := t)) →
      ℤ :=
  Quotient.lift
    (fun q : PentagonAssocEightCell W long short s t =>
      ninthResidualChainCharge q)
    (by
      intro q q' h
      rcases h with ⟨alpha⟩
      exact mixedCancelNineCell_preservesResidualChainCharge alpha)

theorem mixedCancelNinthResidualCharge_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : PentagonAssocEightCell W long short s t) :
    mixedCancelNinthResidualCharge (mixedCancelNinthClass q) =
      ninthResidualChainCharge q := rfl

/-- Even the genuine original reflexive eighth comparison, when
composed with itself as an ORIGINAL free eighth chain, has a
different raw eighth proof. It carries no P or M primitive events. -/
def ninthDoubleReflexiveChain (l r : W) :
    PentagonAssocEightCell W l r
      (sevenFourfoldInversePentagonThree l r)
      (sevenFourfoldInversePentagonThree l r) :=
  .chain (ninthPentagonReflexive l r)
    (ninthPentagonReflexive l r)

theorem ninthDoubleReflexiveResidualValues (l r : W) :
    ninthResidualChainCharge (ninthDoubleReflexiveChain l r) = 2 ∧
    ninthResidualChainCharge (ninthPentagonReflexive l r) = 0 := by
  constructor <;> rfl

theorem ninthDoubleReflexive_noMixedCancelComparison (l r : W) :
    ¬ Nonempty (MixedCancelNineCell W l r
      (ninthDoubleReflexiveChain l r)
      (ninthPentagonReflexive l r)) := by
  rintro ⟨alpha⟩
  have h := mixedCancelNineCell_preservesResidualChainCharge alpha
  have vals := ninthDoubleReflexiveResidualValues l r
  rw [vals.1, vals.2] at h
  norm_num at h

theorem ninthDoubleReflexive_distinctMixedCancelClass (l r : W) :
    mixedCancelNinthClass (ninthDoubleReflexiveChain l r) ≠
      mixedCancelNinthClass (ninthPentagonReflexive l r) := by
  intro h
  exact ninthDoubleReflexive_noMixedCancelComparison l r
    ((mixedCancelNinthClass_eq_iff _ _).1 h)

theorem mixedCancelNineCell_notGloballyThin (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q q' : PentagonAssocEightCell W l r s t),
      Nonempty (MixedCancelNineCell W l r q q')) := by
  intro interpret
  exact ninthDoubleReflexive_noMixedCancelComparison l r
    (interpret _ _)

/-! A concrete, original-source higher critical diamond between
the newly adjoined M cancellation and the inherited P cancellation. -/

def originalDoubleCancellationTop (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueFirst l r) :=
  .compositeContext (ninthPentagonRoundtrip l r)
    (ninthMixedRoundtrip l r)

def originalDoubleCancellationMidP (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueFirst l r) :=
  .compositeContext (ninthPentagonReflexive l r)
    (ninthMixedRoundtrip l r)

def originalDoubleCancellationMidM (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueFirst l r) :=
  .compositeContext (ninthPentagonRoundtrip l r)
    (ninthMixedReflexive l r)

def originalDoubleCancellationBottom (l r : W) :
    PentagonAssocEightCell W l r
      (fourfoldMixedResidueFirst l r)
      (fourfoldMixedResidueFirst l r) :=
  .compositeContext (ninthPentagonReflexive l r)
    (ninthMixedReflexive l r)

/-- TOP: original P cancellation with the actual M roundtrip
kept as the typed right eighth context. This is PREVIOUS nine. -/
def originalDoubleCancellationPTop (l r : W) :
    MixedCancelNineCell W l r
      (originalDoubleCancellationTop l r)
      (originalDoubleCancellationMidP l r) :=
  .previous (.compositeContext (.cancelPentagon)
    (pentagonCancelNineCell_refl (ninthMixedRoundtrip l r)))

/-- RIGHT: NEW M cancellation in the old P-reflexive context. -/
def originalDoubleCancellationMRight (l r : W) :
    MixedCancelNineCell W l r
      (originalDoubleCancellationMidP l r)
      (originalDoubleCancellationBottom l r) :=
  .compositeContext
    (mixedCancelNineCell_refl (ninthPentagonReflexive l r))
    (.cancelMixed)

/-- LEFT: NEW M cancellation in the original P roundtrip context. -/
def originalDoubleCancellationMLeft (l r : W) :
    MixedCancelNineCell W l r
      (originalDoubleCancellationTop l r)
      (originalDoubleCancellationMidM l r) :=
  .compositeContext
    (mixedCancelNineCell_refl (ninthPentagonRoundtrip l r))
    (.cancelMixed)

/-- BOTTOM: original P cancellation in the M-reflexive context. -/
def originalDoubleCancellationPBottom (l r : W) :
    MixedCancelNineCell W l r
      (originalDoubleCancellationMidM l r)
      (originalDoubleCancellationBottom l r) :=
  .previous (.compositeContext (.cancelPentagon)
    (pentagonCancelNineCell_refl (ninthMixedReflexive l r)))

def originalDoubleCancellationPThenM (l r : W) :
    MixedCancelNineCell W l r
      (originalDoubleCancellationTop l r)
      (originalDoubleCancellationBottom l r) :=
  .chain (originalDoubleCancellationPTop l r)
    (originalDoubleCancellationMRight l r)

def originalDoubleCancellationMThenP (l r : W) :
    MixedCancelNineCell W l r
      (originalDoubleCancellationTop l r)
      (originalDoubleCancellationBottom l r) :=
  .chain (originalDoubleCancellationMLeft l r)
    (originalDoubleCancellationPBottom l r)

theorem originalDoubleCancellationLocalDiamond (l r : W) :
    Nonempty (MixedCancelNineCell W l r
      (originalDoubleCancellationTop l r)
      (originalDoubleCancellationMidP l r)) ∧
    Nonempty (MixedCancelNineCell W l r
      (originalDoubleCancellationMidP l r)
      (originalDoubleCancellationBottom l r)) ∧
    Nonempty (MixedCancelNineCell W l r
      (originalDoubleCancellationTop l r)
      (originalDoubleCancellationMidM l r)) ∧
    Nonempty (MixedCancelNineCell W l r
      (originalDoubleCancellationMidM l r)
      (originalDoubleCancellationBottom l r)) ∧
    Nonempty (MixedCancelNineCell W l r
      (originalDoubleCancellationTop l r)
      (originalDoubleCancellationBottom l r)) :=
  ⟨⟨originalDoubleCancellationPTop l r⟩,
    ⟨originalDoubleCancellationMRight l r⟩,
    ⟨originalDoubleCancellationMLeft l r⟩,
    ⟨originalDoubleCancellationPBottom l r⟩,
    ⟨originalDoubleCancellationPThenM l r⟩⟩

/-- Projection of the PREVIOUS ninth proof grammar onto its P-cancel
primitive events. Old P/M interchange events are intentionally
left outside this specific cancellation-order observation. -/
def oldPentagonCancellationTrace {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : PentagonCancelNineCell W long short q q') : List Bool :=
  match alpha with
  | .previous _ => []
  | .cancelPentagon => [true]
  | .reverse alpha => (oldPentagonCancellationTrace alpha).reverse
  | .chain alpha beta =>
      oldPentagonCancellationTrace alpha ++ oldPentagonCancellationTrace beta
  | .reverseContext alpha => oldPentagonCancellationTrace alpha
  | .chainContext alpha beta =>
      oldPentagonCancellationTrace alpha ++ oldPentagonCancellationTrace beta
  | .whiskerLeft _ alpha => oldPentagonCancellationTrace alpha
  | .whiskerRight alpha _ => oldPentagonCancellationTrace alpha
  | .inverseContext alpha => oldPentagonCancellationTrace alpha
  | .compositeContext alpha beta =>
      oldPentagonCancellationTrace alpha ++ oldPentagonCancellationTrace beta

/-- True for the original P cancellation; false for exactly the
NEW M cancellation. This trace records raw ninth proof syntax, NOT
an invariant of a future tenth-cell comparison presentation. -/
def mixedCancelNinePrimitiveTrace {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    {q q' : PentagonAssocEightCell W long short s t}
    (alpha : MixedCancelNineCell W long short q q') : List Bool :=
  match alpha with
  | .previous old => oldPentagonCancellationTrace old
  | .cancelMixed => [false]
  | .reverse alpha => (mixedCancelNinePrimitiveTrace alpha).reverse
  | .chain alpha beta =>
      mixedCancelNinePrimitiveTrace alpha ++ mixedCancelNinePrimitiveTrace beta
  | .reverseContext alpha => mixedCancelNinePrimitiveTrace alpha
  | .chainContext alpha beta =>
      mixedCancelNinePrimitiveTrace alpha ++ mixedCancelNinePrimitiveTrace beta
  | .whiskerLeft _ alpha => mixedCancelNinePrimitiveTrace alpha
  | .whiskerRight alpha _ => mixedCancelNinePrimitiveTrace alpha
  | .inverseContext alpha => mixedCancelNinePrimitiveTrace alpha
  | .compositeContext alpha beta =>
      mixedCancelNinePrimitiveTrace alpha ++ mixedCancelNinePrimitiveTrace beta

theorem originalDoubleCancellationTraceValues (l r : W) :
    mixedCancelNinePrimitiveTrace
        (originalDoubleCancellationPThenM l r) = [true, false] ∧
    mixedCancelNinePrimitiveTrace
        (originalDoubleCancellationMThenP l r) = [false, true] := by
  constructor <;> rfl

/-- The two local ninth completions are differently ordered RAW
proof values with exactly the SAME eighth source and target.
This DOES NOT assert nonexistence of a tenth comparison. -/
theorem originalDoubleCancellationRawNineGap (l r : W) :
    originalDoubleCancellationPThenM l r ≠
      originalDoubleCancellationMThenP l r := by
  intro h
  have ht := congrArg mixedCancelNinePrimitiveTrace h
  rw [(originalDoubleCancellationTraceValues l r).1,
    (originalDoubleCancellationTraceValues l r).2] at ht
  cases ht

end PentagonAdjoinedSixCell

section ActualOriginalP77MixedRoundtripCompletion
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

/-- The new genuinely typed ninth M cancellation exists at every
original P77 final raw index with the original GK5CG long/short
Type-valued sources and the old source strict Eq obstruction. -/
theorem pentagonActualMixedRoundtripNinthCompletion
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.MixedCancelNineCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.ninthMixedRoundtrip
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.ninthMixedReflexive
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨⟨.cancelMixed⟩,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.MixedCancelNineCell
#print axioms PentagonAdjoinedSixCell.mixedCancelNineCell_refl
#print axioms PentagonAdjoinedSixCell.mixedCancelNineCell_ofPrevious
#print axioms PentagonAdjoinedSixCell.ninthMixedRoundtrip_rawGap
#print axioms PentagonAdjoinedSixCell.mixedCancelNineCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.mixedCancelNineCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.mixedCancelNineCell_noRawEqualityInterpreter
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthSetoid
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthClass
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthClass_eq_iff
#print axioms PentagonAdjoinedSixCell.pentagonCancelNinthClass_descendsToMixedCancel
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthClass_noRawRetraction
#print axioms PentagonAdjoinedSixCell.mixedCancelNineCell_preservesPentagonParity
#print axioms PentagonAdjoinedSixCell.mixedCancelNineCell_preservesMixedParity
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthPentagonParity
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthMixedParity
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthPentagonParity_onClass
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthMixedParity_onClass
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthClass_noMixedCountDescent
#print axioms PentagonAdjoinedSixCell.ninthResidualChainCharge
#print axioms PentagonAdjoinedSixCell.fourfoldMixedNineCell_preservesResidualChainCharge
#print axioms PentagonAdjoinedSixCell.pentagonCancelNineCell_preservesResidualChainCharge
#print axioms PentagonAdjoinedSixCell.mixedCancelNineCell_preservesResidualChainCharge
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthResidualCharge
#print axioms PentagonAdjoinedSixCell.mixedCancelNinthResidualCharge_onClass
#print axioms PentagonAdjoinedSixCell.ninthDoubleReflexiveChain
#print axioms PentagonAdjoinedSixCell.ninthDoubleReflexiveResidualValues
#print axioms PentagonAdjoinedSixCell.ninthDoubleReflexive_noMixedCancelComparison
#print axioms PentagonAdjoinedSixCell.ninthDoubleReflexive_distinctMixedCancelClass
#print axioms PentagonAdjoinedSixCell.mixedCancelNineCell_notGloballyThin
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationTop
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationMidP
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationMidM
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationBottom
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationPTop
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationMRight
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationMLeft
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationPBottom
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationPThenM
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationMThenP
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationLocalDiamond
#print axioms PentagonAdjoinedSixCell.oldPentagonCancellationTrace
#print axioms PentagonAdjoinedSixCell.mixedCancelNinePrimitiveTrace
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationTraceValues
#print axioms PentagonAdjoinedSixCell.originalDoubleCancellationRawNineGap
#print axioms pentagonActualMixedRoundtripNinthCompletion

end ActualOriginalP77MixedRoundtripCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
