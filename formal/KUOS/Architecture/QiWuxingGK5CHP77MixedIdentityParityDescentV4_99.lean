import KUOS.Architecture.QiWuxingGK5CHP77IdentityDoubleHigherLocalCompletionV4_98

/-!
Qi v4.99 — MIXED IDENTITY PEAKS AND RESIDUAL PARITY DESCENT.

Qi v4.98 destroys integer-valued sevenIdentityBalance R as an
invariant of the new eighth-history quotient by adding precisely
one identity/doubleInverse comparison with charge jump 2.

We prove that its RESIDUE modulo 2 nevertheless survives EVERY
constructor of the FULL chosen IdentityEightCell grammar.
The quotient therefore has a genuine Bool-valued parity observer
defined by Quotient.lift, while R itself provably does not descend.

We construct three actually indexed mixed critical pairs combining
the NEW identityDouble comparison with OLD, genuinely sourced
  (a) left inverseComp/unit,
  (b) right inverseComp/unit,
  (c) doubleInverse/inverse-cancellation
comparisons. All three are filled with explicit Type-valued
compositeContext witnesses using only existing constructors, but
none can be joined in the old v4.95 InverseCompEightCell grammar
because its R-invariance sees a 0-versus-2 jump.

The restricted mixed critical-peak family is constructively fillable
by induction over all its listed contextual constructors. This
asserts NO all-parallel seventh-history completeness or ninth cells.
Original GK5CG five-cell Type authority and its equality-interpreter
obstruction are preserved for each actual P77 final raw index.

Append-only / tighten-only / same-root; published root107 unchanged.
Pinned Lean v4.30.0-rc2; mathlib
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

/-- Residual mod-two observation on the unchanged RAW seventh history,
not a claim that the original integer R descends. -/
def sevenIdentityParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  sevenIdentityBalance s % 2

/-- The ACTUAL v4.98 new generator destroys integer R but its
charge jump is even, hence the residue modulo 2 is unchanged. -/
theorem identityDouble_preservesParity (w : W) :
    sevenIdentityParity
        (sevenIdentityDoubleDirect (long := long) (short := short) w) =
      sevenIdentityParity
        (sevenIdentityDoubleVia (long := long) (short := short) w) := by
  simp [sevenIdentityParity, sevenIdentityDoubleDirect,
    sevenIdentityDoubleVia, sevenIdentityBalance]

/-- Every constructor of the final v4.98 IdentityEightCell grammar
preserves parity, including the old inverseComp/triangle/involution
comparisons, the genuinely new identityDouble, and all contexts. -/
theorem identityEightCell_preservesParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : IdentityEightCell W long short s t) :
    sevenIdentityParity s = sevenIdentityParity t := by
  induction q with
  | previous q =>
      exact congrArg (fun a : ℤ => a % 2)
        (inverseCompEightCell_preservesIdentityBalance q)
  | identityDouble w =>
      exact identityDouble_preservesParity w
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simp only [sevenIdentityParity] at ih ⊢
      simp only [sevenIdentityBalance]
      omega
  | whiskerRight q after ih =>
      simp only [sevenIdentityParity] at ih ⊢
      simp only [sevenIdentityBalance]
      omega
  | inverseContext q ih =>
      simpa [sevenIdentityParity, sevenIdentityBalance] using ih
  | compositeContext q q' ih ih' =>
      simp only [sevenIdentityParity] at ih ih' ⊢
      simp only [sevenIdentityBalance]
      omega

/-- Equality in the NEW chosen higher-history quotient forces parity
equality, even though the integer R itself does not descend. -/
theorem identityHistoryClass_eq_preservesParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : identityHistoryClass s = identityHistoryClass t) :
    sevenIdentityParity s = sevenIdentityParity t := by
  rcases (identityHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact identityEightCell_preservesParity q

/-- A genuine Bool observer on the actual NEW higher-history quotient.
It is constructed by Quotient.lift from the proved all-constructor
compatibility, never by identifying original raw histories. -/
def identityHistoryParity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z} :
    Quotient (identityHistorySetoid W long short (c := c) (d := d)) →
      Bool :=
  Quotient.lift
    (fun s : SevenRewrite W long short c d =>
      decide (sevenIdentityParity s = 1))
    (by
      intro s t h
      rcases h with ⟨q⟩
      exact congrArg (fun a : ℤ => decide (a = 1))
        (identityEightCell_preservesParity q))

theorem identityHistoryParity_onClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    identityHistoryParity
      (identityHistoryClass (long := long) (short := short) s) =
      decide (sevenIdentityParity s = 1) :=
  rfl

/-- Both original v4.97 hidden paths (R=0 and R=2) have the same
residual parity in their newly identified v4.98 quotient. -/
theorem hiddenCritical_parityValues (w : W) :
    sevenIdentityParity
        (sevenHiddenCriticalFirst (long := long) (short := short) w) = 0 ∧
    sevenIdentityParity
        (sevenHiddenCriticalSecond (long := long) (short := short) w) = 0 := by
  have h := sevenHiddenCritical_balanceValues (long := long) (short := short) w
  constructor
  · simp [sevenIdentityParity, h.1]
  · simp [sevenIdentityParity, h.2]

/-- The new quotient carries residual parity while the old
unreduced integer balance has no global descent. -/
theorem identityParity_survivesIntegerFailure (l r : W) :
    (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      identityHistoryClass s = identityHistoryClass t →
        sevenIdentityParity s = sevenIdentityParity t) ∧
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      identityHistoryClass s = identityHistoryClass t →
        sevenIdentityBalance s = sevenIdentityBalance t) := by
  constructor
  · intro w z c d s t h
    exact identityHistoryClass_eq_preservesParity s t h
  · exact identityHistoryClass_noBalanceDescent l r

/-- First mixed pair: NEW identity/doubleInverse at the target z,
combined with the OLD left inverseComp/unit overlap on the inverse
arrow z → w. Both are true typed seventh-level histories. -/
def mixedIdentityInvCompLeftFirst {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm (.symm (.refl z)))
        (.symm (.trans (.refl w) c)))
      (.trans (.refl z) (.symm c)) :=
  .congrComp (sevenIdentityDoubleDirect z)
    (sevenInvCompLeftDirect c)

def mixedIdentityInvCompLeftSecond {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm (.symm (.refl z)))
        (.symm (.trans (.refl w) c)))
      (.trans (.refl z) (.symm c)) :=
  .congrComp (sevenIdentityDoubleVia z)
    (sevenInvCompLeftVia c)

/-- The right inverseComp/unit overlap gives an independent
typed mixed-pair family with the same z → w boundary. -/
def mixedIdentityInvCompRightFirst {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm (.symm (.refl z)))
        (.symm (.trans c (.refl z))))
      (.trans (.refl z) (.symm c)) :=
  .congrComp (sevenIdentityDoubleDirect z)
    (sevenInvCompRightDirect c)

def mixedIdentityInvCompRightSecond {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm (.symm (.refl z)))
        (.symm (.trans c (.refl z))))
      (.trans (.refl z) (.symm c)) :=
  .congrComp (sevenIdentityDoubleVia z)
    (sevenInvCompRightVia c)

/-- Third mixed pair: identityDouble at w is horizontally pasted
with the OLD v4.94 double-inverse/inverse-cancellation overlap at w. -/
def mixedIdentityInvolutionLeftFirst {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm (.symm (.refl w)))
        (.trans (.symm (.symm c)) (.symm c)))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenIdentityDoubleDirect w)
    (sevenLeftDoubleInverseDirect c)

def mixedIdentityInvolutionLeftSecond {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm (.symm (.refl w)))
        (.trans (.symm (.symm c)) (.symm c)))
      (.trans (.refl w) (.refl w)) :=
  .congrComp (sevenIdentityDoubleVia w)
    (sevenLeftDoubleInverseVia c)

/-- All three genuine mixed overlaps retain an EXACT old R-gap of 2.
The previously completed inverseComp and involution branches each
have balance 0; the new identityDouble branch changes R by 2. -/
theorem mixedIdentityInvCompLeft_balanceGap {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenIdentityBalance
        (mixedIdentityInvCompLeftFirst (long := long) (short := short) c) = 0 ∧
    sevenIdentityBalance
        (mixedIdentityInvCompLeftSecond (long := long) (short := short) c) = 2 := by
  constructor <;>
    norm_num [mixedIdentityInvCompLeftFirst,
      mixedIdentityInvCompLeftSecond, sevenIdentityDoubleDirect,
      sevenIdentityDoubleVia, sevenInvCompLeftDirect,
      sevenInvCompLeftVia, sevenIdentityBalance]

theorem mixedIdentityInvCompRight_balanceGap {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenIdentityBalance
        (mixedIdentityInvCompRightFirst (long := long) (short := short) c) = 0 ∧
    sevenIdentityBalance
        (mixedIdentityInvCompRightSecond (long := long) (short := short) c) = 2 := by
  constructor <;>
    norm_num [mixedIdentityInvCompRightFirst,
      mixedIdentityInvCompRightSecond, sevenIdentityDoubleDirect,
      sevenIdentityDoubleVia, sevenInvCompRightDirect,
      sevenInvCompRightVia, sevenIdentityBalance]

theorem mixedIdentityInvolutionLeft_balanceGap {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenIdentityBalance
        (mixedIdentityInvolutionLeftFirst (long := long) (short := short) c) = 0 ∧
    sevenIdentityBalance
        (mixedIdentityInvolutionLeftSecond (long := long) (short := short) c) = 2 := by
  constructor <;>
    norm_num [mixedIdentityInvolutionLeftFirst,
      mixedIdentityInvolutionLeftSecond, sevenIdentityDoubleDirect,
      sevenIdentityDoubleVia, sevenLeftDoubleInverseDirect,
      sevenLeftDoubleInverseVia, sevenIdentityBalance]

/-- Each mixed overlap is explicitly joinable in the NEW v4.98
grammar. No new primitive eighth-level generator is required. -/
def mixedIdentityInvCompLeft_fill {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    IdentityEightCell W long short
      (mixedIdentityInvCompLeftFirst (long := long) (short := short) c)
      (mixedIdentityInvCompLeftSecond (long := long) (short := short) c) :=
  .compositeContext
    (.identityDouble z)
    (.previous (.leftOverlap c))

def mixedIdentityInvCompRight_fill {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    IdentityEightCell W long short
      (mixedIdentityInvCompRightFirst (long := long) (short := short) c)
      (mixedIdentityInvCompRightSecond (long := long) (short := short) c) :=
  .compositeContext
    (.identityDouble z)
    (.previous (.rightOverlap c))

def mixedIdentityInvolutionLeft_fill {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    IdentityEightCell W long short
      (mixedIdentityInvolutionLeftFirst (long := long) (short := short) c)
      (mixedIdentityInvolutionLeftSecond (long := long) (short := short) c) :=
  .compositeContext
    (.identityDouble w)
    (.previous (.previous (.leftOverlap c)))

/-- Each mixed pair remains NOT joinable in the ORIGINAL
v4.95 comparison grammar. This is stronger than non-discovery:
the old all-constructor R preservation contradicts the 0/2 gap. -/
theorem mixedIdentityInvCompLeft_noPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (InverseCompEightCell W long short
      (mixedIdentityInvCompLeftFirst (long := long) (short := short) c)
      (mixedIdentityInvCompLeftSecond (long := long) (short := short) c)) := by
  rintro ⟨q⟩
  have h := inverseCompEightCell_preservesIdentityBalance q
  have vals := mixedIdentityInvCompLeft_balanceGap c
  rw [vals.1, vals.2] at h
  norm_num at h

theorem mixedIdentityInvCompRight_noPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (InverseCompEightCell W long short
      (mixedIdentityInvCompRightFirst (long := long) (short := short) c)
      (mixedIdentityInvCompRightSecond (long := long) (short := short) c)) := by
  rintro ⟨q⟩
  have h := inverseCompEightCell_preservesIdentityBalance q
  have vals := mixedIdentityInvCompRight_balanceGap c
  rw [vals.1, vals.2] at h
  norm_num at h

theorem mixedIdentityInvolutionLeft_noPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (InverseCompEightCell W long short
      (mixedIdentityInvolutionLeftFirst (long := long) (short := short) c)
      (mixedIdentityInvolutionLeftSecond (long := long) (short := short) c)) := by
  rintro ⟨q⟩
  have h := inverseCompEightCell_preservesIdentityBalance q
  have vals := mixedIdentityInvolutionLeft_balanceGap c
  rw [vals.1, vals.2] at h
  norm_num at h

/-- Three independently typed mixed peaks are each new-vs-old,
and each retains the SAME residual parity after filling. -/
theorem mixedIdentityInvCompLeft_newVsOld {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (IdentityEightCell W long short
      (mixedIdentityInvCompLeftFirst (long := long) (short := short) c)
      (mixedIdentityInvCompLeftSecond (long := long) (short := short) c)) ∧
    ¬ Nonempty (InverseCompEightCell W long short
      (mixedIdentityInvCompLeftFirst (long := long) (short := short) c)
      (mixedIdentityInvCompLeftSecond (long := long) (short := short) c)) ∧
    sevenIdentityParity
        (mixedIdentityInvCompLeftFirst (long := long) (short := short) c) =
      sevenIdentityParity
        (mixedIdentityInvCompLeftSecond (long := long) (short := short) c) :=
  ⟨⟨mixedIdentityInvCompLeft_fill c⟩,
    mixedIdentityInvCompLeft_noPrevious c,
    identityEightCell_preservesParity (mixedIdentityInvCompLeft_fill c)⟩

theorem mixedIdentityInvCompRight_newVsOld {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (IdentityEightCell W long short
      (mixedIdentityInvCompRightFirst (long := long) (short := short) c)
      (mixedIdentityInvCompRightSecond (long := long) (short := short) c)) ∧
    ¬ Nonempty (InverseCompEightCell W long short
      (mixedIdentityInvCompRightFirst (long := long) (short := short) c)
      (mixedIdentityInvCompRightSecond (long := long) (short := short) c)) ∧
    sevenIdentityParity
        (mixedIdentityInvCompRightFirst (long := long) (short := short) c) =
      sevenIdentityParity
        (mixedIdentityInvCompRightSecond (long := long) (short := short) c) :=
  ⟨⟨mixedIdentityInvCompRight_fill c⟩,
    mixedIdentityInvCompRight_noPrevious c,
    identityEightCell_preservesParity (mixedIdentityInvCompRight_fill c)⟩

theorem mixedIdentityInvolutionLeft_newVsOld {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (IdentityEightCell W long short
      (mixedIdentityInvolutionLeftFirst (long := long) (short := short) c)
      (mixedIdentityInvolutionLeftSecond (long := long) (short := short) c)) ∧
    ¬ Nonempty (InverseCompEightCell W long short
      (mixedIdentityInvolutionLeftFirst (long := long) (short := short) c)
      (mixedIdentityInvolutionLeftSecond (long := long) (short := short) c)) ∧
    sevenIdentityParity
        (mixedIdentityInvolutionLeftFirst (long := long) (short := short) c) =
      sevenIdentityParity
        (mixedIdentityInvolutionLeftSecond (long := long) (short := short) c) :=
  ⟨⟨mixedIdentityInvolutionLeft_fill c⟩,
    mixedIdentityInvolutionLeft_noPrevious c,
    identityEightCell_preservesParity (mixedIdentityInvolutionLeft_fill c)⟩

/-- Three genuine mixed primitive families and their explicit typed
context closure: an operation-specific local family, not a new
universal constructor identifying all parallel seventh histories. -/
inductive MixedIdentityCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | leftInvComp {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      MixedIdentityCriticalPeak W l r
        (mixedIdentityInvCompLeftFirst (long := l) (short := r) c)
        (mixedIdentityInvCompLeftSecond (long := l) (short := r) c)
  | rightInvComp {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      MixedIdentityCriticalPeak W l r
        (mixedIdentityInvCompRightFirst (long := l) (short := r) c)
        (mixedIdentityInvCompRightSecond (long := l) (short := r) c)
  | leftInvolution {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      MixedIdentityCriticalPeak W l r
        (mixedIdentityInvolutionLeftFirst (long := l) (short := r) c)
        (mixedIdentityInvolutionLeftSecond (long := l) (short := r) c)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedIdentityCriticalPeak W l r s t) :
      MixedIdentityCriticalPeak W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : MixedIdentityCriticalPeak W l r s t)
      (q' : MixedIdentityCriticalPeak W l r t u) :
      MixedIdentityCriticalPeak W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : MixedIdentityCriticalPeak W l r s t) :
      MixedIdentityCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedIdentityCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      MixedIdentityCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : MixedIdentityCriticalPeak W l r s t) :
      MixedIdentityCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : MixedIdentityCriticalPeak W l r s s')
      (q' : MixedIdentityCriticalPeak W l r t t') :
      MixedIdentityCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

/-- Every selected mixed critical peak has an actual Type-valued
v4.98 comparison, by full constructor induction. -/
def mixedIdentityCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : MixedIdentityCriticalPeak W long short s t) :
    IdentityEightCell W long short s t := by
  induction p with
  | leftInvComp c => exact mixedIdentityInvCompLeft_fill c
  | rightInvComp c => exact mixedIdentityInvCompRight_fill c
  | leftInvolution c => exact mixedIdentityInvolutionLeft_fill c
  | reverse q ih => exact .reverse ih
  | chain q q' ih ih' => exact .chain ih ih'
  | whiskerLeft before q ih => exact .whiskerLeft before ih
  | whiskerRight q after ih => exact .whiskerRight ih after
  | inverseContext q ih => exact .inverseContext ih
  | compositeContext q q' ih ih' => exact .compositeContext ih ih'

theorem mixedIdentityCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : MixedIdentityCriticalPeak W long short s t) :
    Nonempty (IdentityEightCell W long short s t) :=
  ⟨mixedIdentityCriticalPeak_fill p⟩

/-- Restricted family coherence descends to the actual chosen
new quotient; raw history equality is NOT inferred. -/
theorem mixedIdentityCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : MixedIdentityCriticalPeak W long short s t) :
    identityHistoryClass s = identityHistoryClass t :=
  (identityHistoryClass_eq_iff s t).2 (mixedIdentityCriticalPeak_joinable p)

/-- The three explicit mixed critical peak witnesses yield strict
new-vs-old quotient comparisons; this is not an arbitrary
all-history completeness statement. -/
theorem mixedIdentityInvCompLeft_strictClasses {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    identityHistoryClass
        (mixedIdentityInvCompLeftFirst (long := long) (short := short) c) =
      identityHistoryClass
        (mixedIdentityInvCompLeftSecond (long := long) (short := short) c) ∧
    inverseCompHistoryClass
        (mixedIdentityInvCompLeftFirst (long := long) (short := short) c) ≠
      inverseCompHistoryClass
        (mixedIdentityInvCompLeftSecond (long := long) (short := short) c) := by
  constructor
  · exact (identityHistoryClass_eq_iff _ _).2
      ⟨mixedIdentityInvCompLeft_fill c⟩
  · intro h
    exact mixedIdentityInvCompLeft_noPrevious c
      ((inverseCompHistoryClass_eq_iff _ _).1 h)

end PentagonAdjoinedSixCell

section ActualOriginalP77MixedIdentityParity
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

/-- At EVERY genuine P77 terminal raw index, the ORIGINAL GK5CG
five-cell endpoints supply a true six-cell generator for a mixed
identityDouble/inverseComp critical pair. The new comparison exists,
the old one is genuinely obstructed by R, and the strict source
equality-interpreter obstruction is unchanged. -/
theorem pentagonActualMixedIdentityParityWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      Nonempty (PentagonAdjoinedSixCell.IdentityEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.mixedIdentityInvCompLeftFirst c)
        (PentagonAdjoinedSixCell.mixedIdentityInvCompLeftSecond c)) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.InverseCompEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.mixedIdentityInvCompLeftFirst c)
        (PentagonAdjoinedSixCell.mixedIdentityInvCompLeftSecond c)) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    ⟨PentagonAdjoinedSixCell.mixedIdentityInvCompLeft_fill _⟩,
    PentagonAdjoinedSixCell.mixedIdentityInvCompLeft_noPrevious _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.sevenIdentityParity
#print axioms PentagonAdjoinedSixCell.identityDouble_preservesParity
#print axioms PentagonAdjoinedSixCell.identityEightCell_preservesParity
#print axioms PentagonAdjoinedSixCell.identityHistoryClass_eq_preservesParity
#print axioms PentagonAdjoinedSixCell.identityHistoryParity
#print axioms PentagonAdjoinedSixCell.identityHistoryParity_onClass
#print axioms PentagonAdjoinedSixCell.hiddenCritical_parityValues
#print axioms PentagonAdjoinedSixCell.identityParity_survivesIntegerFailure
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompLeftFirst
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompLeftSecond
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompRightFirst
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompRightSecond
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvolutionLeftFirst
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvolutionLeftSecond
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompLeft_balanceGap
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompRight_balanceGap
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvolutionLeft_balanceGap
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompLeft_fill
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompRight_fill
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvolutionLeft_fill
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompLeft_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompRight_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvolutionLeft_noPrevious
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompLeft_newVsOld
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompRight_newVsOld
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvolutionLeft_newVsOld
#print axioms PentagonAdjoinedSixCell.MixedIdentityCriticalPeak
#print axioms PentagonAdjoinedSixCell.mixedIdentityCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.mixedIdentityCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.mixedIdentityCriticalPeak_classEq
#print axioms PentagonAdjoinedSixCell.mixedIdentityInvCompLeft_strictClasses
#print axioms pentagonActualMixedIdentityParityWithSourceObstruction

end ActualOriginalP77MixedIdentityParity
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
