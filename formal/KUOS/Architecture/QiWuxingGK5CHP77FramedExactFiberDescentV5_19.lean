import KUOS.Architecture.QiWuxingGK5CHP77DoubleWhiskerFramedTwelfthV5_18

/-!
Qi v5.19 — EXACT-FIBER TWELFTH LIFTABILITY, OBSTRUCTION AND QUOTIENT.

The independently framed 12D double-whisker comparison in v5.18
does NOT silently reindex to the old fixed-fiber 12D proof type.
Here the FULL ORIGINAL dependent 6D–10D spine is separated from
the unchanged original raw 11D evidence. Equality of these spines
permits an actual Eq-rec transport of a witness, and ONLY THEN
an old Qi v5.17 twelfth comparison is type-correct.

An independently typed inherited-only framed presentation with
strict / previous / reverse / chain is EXACTLY equivalent to an
explicit spine equality together with the old twelfth witness.
The new double-whisker interchanger is PROVABLY not inherited-only:
its 7D source/target are 8D-associator compatible, yet its actual
raw tenth whisker histories obstruct exact spine equality.

The inherited-only quotient retains a genuine spine observer.
There is a canonical quotient map to the v5.18 framed quotient,
but it is not injective, and no factorization of the complete spine
observer through the newer quotient can exist. The original
three Nat-valued observers, P77/GK5CG source and residual strict
obstructions remain unchanged.

No general 8D-to-Eq coercion, arbitrary reindexing, universal
thinness, or change of old F55/P77/GK5CG evidence is asserted.

append-only / tighten-only / overwrite-forbidden / same-root.
Public root107. Lean v4.30.0-rc2; mathlib
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

/-- All ORIGINAL raw 6D–10D indices of a v5.18 framed eleventh
proof, but WITHOUT its final original 11D proof witness.
It is a separate Type, not a quotient or an equality assertion. -/
structure FramedElevenExactSpine (W : Type uSix) (l r : W) : Type uSix where
  w : W
  z : W
  c : PentagonAdjoinedSixCell W l r w z
  d : PentagonAdjoinedSixCell W l r w z
  s : SevenRewrite W l r c d
  t : SevenRewrite W l r c d
  q₀ : PentagonAssocEightCell W l r s t
  q₁ : PentagonAssocEightCell W l r s t
  alpha : MixedCancelNineCell W l r q₀ q₁
  beta : MixedCancelNineCell W l r q₀ q₁
  xi : MixedUnitAssocTenCell W l r alpha beta
  zeta : MixedUnitAssocTenCell W l r alpha beta

/-- The genuine original 11D proof Type over the exact lower spine. -/
def framedElevenSpineWitness {l r : W}
    (S : FramedElevenExactSpine W l r) : Type uSix :=
  MixedExchangeUnitElevenCell W l r S.xi S.zeta

/-- Forget ONLY the top-level 11D proof value, retaining every raw
dependent boundary and proof term from sixth through tenth level. -/
def framedElevenExactSpine (l r : W) (F : FramedEleven W l r) :
    FramedElevenExactSpine W l r :=
  { w := F.w, z := F.z, c := F.c, d := F.d,
    s := F.s, t := F.t, q₀ := F.q₀, q₁ := F.q₁,
    alpha := F.alpha, beta := F.beta, xi := F.xi, zeta := F.zeta }

/-- Reassemble WITHOUT altering the old raw 11D constructor. -/
def framedElevenSpinePack (l r : W)
    (S : FramedElevenExactSpine W l r)
    (H : framedElevenSpineWitness S) : FramedEleven W l r :=
  { w := S.w, z := S.z, c := S.c, d := S.d,
    s := S.s, t := S.t, q₀ := S.q₀, q₁ := S.q₁,
    alpha := S.alpha, beta := S.beta,
    xi := S.xi, zeta := S.zeta, H := H }

theorem framedElevenSpinePack_exact (l r : W)
    (F : FramedEleven W l r) :
    framedElevenSpinePack l r (framedElevenExactSpine l r F) F.H = F := by
  cases F
  rfl

/-- Genuine dependent Eq-rec transport: unlike an arbitrary 8D
associator, exact spine equality suffices to reindex old 11D. -/
def framedElevenSpineTransport {l r : W}
    {S T : FramedElevenExactSpine W l r}
    (e : S = T) (H : framedElevenSpineWitness S) :
    framedElevenSpineWitness T := by
  cases e
  exact H

theorem framedElevenSpineTransport_refl {l r : W}
    (S : FramedElevenExactSpine W l r)
    (H : framedElevenSpineWitness S) :
    framedElevenSpineTransport (S := S) (T := S) rfl H = H := rfl

/-- A TYPE-valued exact-fiber certificate: raw spine Eq followed
by an original v5.17 12D witness after genuinely typed transport.
No higher comparison is promoted to raw equality. -/
def FramedExactFiberTwelfthLift (l r : W)
    (F G : FramedEleven W l r) : Type uSix :=
  Σ (e : framedElevenExactSpine l r F =
      framedElevenExactSpine l r G),
    MixedExchangeInverseTwelveCell W l r
      (framedElevenSpineTransport e F.H) G.H

def framedExactFiberTwelfthLift_refl (l r : W)
    (F : FramedEleven W l r) :
    FramedExactFiberTwelfthLift l r F F :=
  ⟨rfl, .strict rfl⟩

/-- Exact transport is symmetric: the reversed 12D old proof is
available ONLY after the spine equality has been inverted. -/
def framedExactFiberTransport_reverse (l r : W)
    {S T : FramedElevenExactSpine W l r}
    {H : framedElevenSpineWitness S}
    {K : framedElevenSpineWitness T}
    (cert : Σ (e : S = T),
      MixedExchangeInverseTwelveCell W l r
        (framedElevenSpineTransport e H) K) :
    Σ (e : T = S),
      MixedExchangeInverseTwelveCell W l r
        (framedElevenSpineTransport e K) H := by
  rcases cert with ⟨e, t⟩
  cases e
  exact ⟨rfl, .reverse t⟩

/-- Composition of exact-fiber transports preserves the original
proof's type index; there is no untyped context reindexing here. -/
def framedExactFiberTransport_chain (l r : W)
    {S T U : FramedElevenExactSpine W l r}
    {H : framedElevenSpineWitness S}
    {K : framedElevenSpineWitness T}
    {L : framedElevenSpineWitness U}
    (cert : Σ (e : S = T),
      MixedExchangeInverseTwelveCell W l r
        (framedElevenSpineTransport e H) K)
    (next : Σ (e : T = U),
      MixedExchangeInverseTwelveCell W l r
        (framedElevenSpineTransport e K) L) :
    Σ (e : S = U),
      MixedExchangeInverseTwelveCell W l r
        (framedElevenSpineTransport e H) L := by
  rcases cert with ⟨e, t⟩
  rcases next with ⟨e', u⟩
  cases e
  cases e'
  exact ⟨rfl, .chain t u⟩

/-- A NEW inherited-only framed 12D grammar, containing EXACTLY
the old 12D comparison and structural equivalence closure, but
NOT the v5.18 independent double-whisker primitive. -/
inductive FramedInheritedTwelfth (W : Type uSix) (l r : W) :
    FramedEleven W l r → FramedEleven W l r → Type uSix where
  | strict (F : FramedEleven W l r) :
      FramedInheritedTwelfth W l r F F
  | previous {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      {q q' : PentagonAssocEightCell W l r s t}
      {alpha beta : MixedCancelNineCell W l r q q'}
      {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
      {H K : MixedExchangeUnitElevenCell W l r xi zeta}
      (T : MixedExchangeInverseTwelveCell W l r H K) :
      FramedInheritedTwelfth W l r
        (framedEleven_ofRaw l r H) (framedEleven_ofRaw l r K)
  | reverse {F G : FramedEleven W l r}
      (T : FramedInheritedTwelfth W l r F G) :
      FramedInheritedTwelfth W l r G F
  | chain {F G K : FramedEleven W l r}
      (T : FramedInheritedTwelfth W l r F G)
      (U : FramedInheritedTwelfth W l r G K) :
      FramedInheritedTwelfth W l r F K

/-- Faithful inclusion of the inherited-only 12D comparisons in
the full v5.18 framed grammar. -/
def framedInheritedTwelfth_toFull (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedInheritedTwelfth W l r F G) :
    FramedDoubleWhiskerTwelveCell W l r F G := by
  induction T with
  | strict F => exact .strict F
  | previous T => exact .previous T
  | reverse T ih => exact .reverse ih
  | chain T U ih ih' => exact .chain ih ih'

/-- Every inherited-only proof yields an exact raw spine alignment
AND an actual original twelfth comparison after reindexing.
Both necessities are constructed, not assumed as extra axioms. -/
def framedInheritedTwelfth_toExact (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedInheritedTwelfth W l r F G) :
    FramedExactFiberTwelfthLift l r F G := by
  induction T with
  | strict F => exact ⟨rfl, .strict rfl⟩
  | previous T => exact ⟨rfl, T⟩
  | reverse T ih =>
      exact framedExactFiberTransport_reverse l r ih
  | chain T U ih ih' =>
      exact framedExactFiberTransport_chain l r ih ih'

theorem framedInheritedTwelfth_preservesSpine (l r : W)
    {F G : FramedEleven W l r}
    (T : FramedInheritedTwelfth W l r F G) :
    framedElevenExactSpine l r F = framedElevenExactSpine l r G :=
  (framedInheritedTwelfth_toExact l r T).fst

/-- An actual original twelfth witness and its chosen EXACT
spine Eq yield a previous-only framed comparison. -/
def framedExactTransport_toInherited (l r : W)
    {S T : FramedElevenExactSpine W l r}
    (e : S = T)
    {H : framedElevenSpineWitness S}
    {K : framedElevenSpineWitness T}
    (cert : MixedExchangeInverseTwelveCell W l r
      (framedElevenSpineTransport e H) K) :
    FramedInheritedTwelfth W l r
      (framedElevenSpinePack l r S H)
      (framedElevenSpinePack l r T K) := by
  cases e
  exact .previous cert

def framedExactFiberTwelfthLift_toInherited (l r : W)
    {F G : FramedEleven W l r}
    (cert : FramedExactFiberTwelfthLift l r F G) :
    FramedInheritedTwelfth W l r F G := by
  rcases cert with ⟨e, T⟩
  have h := framedExactTransport_toInherited l r e T
  rw [framedElevenSpinePack_exact l r F,
    framedElevenSpinePack_exact l r G] at h
  exact h

/-- Exact necessary AND sufficient criterion for comparison in
the inherited-only presentation, retaining the full original
dependent index hierarchy. -/
theorem framedInheritedTwelfth_iff_exactFiber (l r : W)
    (F G : FramedEleven W l r) :
    Nonempty (FramedInheritedTwelfth W l r F G) ↔
      Nonempty (FramedExactFiberTwelfthLift l r F G) := by
  constructor
  · rintro ⟨T⟩
    exact ⟨framedInheritedTwelfth_toExact l r T⟩
  · rintro ⟨cert⟩
    exact ⟨framedExactFiberTwelfthLift_toInherited l r cert⟩

theorem framedExactFiberLift_sufficientForFull (l r : W)
    (F G : FramedEleven W l r)
    (cert : FramedExactFiberTwelfthLift l r F G) :
    Nonempty (FramedDoubleWhiskerTwelveCell W l r F G) :=
  ⟨framedInheritedTwelfth_toFull l r
    (framedExactFiberTwelfthLift_toInherited l r cert)⟩

/-- At the ORIGINAL fixed fiber this criterion is EXACTLY the
unchanged v5.17 type-valued twelfth proof, not a newly invented
equality of eleventh witnesses. -/
theorem framedExactFiberLift_onOriginal_iff (l r : W)
    {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H K : MixedExchangeUnitElevenCell W l r xi zeta) :
    Nonempty (FramedExactFiberTwelfthLift l r
      (framedEleven_ofRaw l r H) (framedEleven_ofRaw l r K)) ↔
    Nonempty (MixedExchangeInverseTwelveCell W l r H K) := by
  constructor
  · rintro ⟨⟨e, T⟩⟩
    cases e
    exact ⟨T⟩
  · rintro ⟨T⟩
    exact ⟨⟨rfl, T⟩⟩

theorem framedInheritedTwelfth_onOriginal_iff (l r : W)
    {w z : W}
    {c d : PentagonAdjoinedSixCell W l r w z}
    {s t : SevenRewrite W l r c d}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H K : MixedExchangeUnitElevenCell W l r xi zeta) :
    Nonempty (FramedInheritedTwelfth W l r
      (framedEleven_ofRaw l r H) (framedEleven_ofRaw l r K)) ↔
    Nonempty (MixedExchangeInverseTwelveCell W l r H K) :=
  (framedInheritedTwelfth_iff_exactFiber l r _ _).trans
    (framedExactFiberLift_onOriginal_iff l r H K)

/-- The two raw double-whisker packets are NEVER exactly
spine-aligned. It is not merely the top-level 11D proof that
differs: the original tenth whisker histories already obstruct. -/
theorem doubleWhiskerExactSpineGap (l r : W) {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (after : SevenRewrite W l r e f₆) :
    framedElevenExactSpine l r
        (doubleWhiskerLeftAfterRightFrame l r before H after) ≠
      framedElevenExactSpine l r
        (doubleWhiskerRightAfterLeftFrame l r before H after) := by
  intro eEq
  have ht := congrArg
    (fun S : FramedElevenExactSpine W l r =>
      mixedTenWhiskerRawTrace S.xi) eEq
  change framedWhiskerRawTrace
      (doubleWhiskerLeftAfterRightFrame l r before H after) =
    framedWhiskerRawTrace
      (doubleWhiskerRightAfterLeftFrame l r before H after) at ht
  rw [(doubleWhiskerRawTraceValues l r before H after).1,
    (doubleWhiskerRawTraceValues l r before H after).2] at ht
  cases ht

/-- Strong original counterexample: the v5.18 exchange-unit
critical pair admits real source/target 8D associator coherence,
but cannot be reindexed by raw Eq of its complete original spine. -/
theorem originalDoubleWhiskerExactSpineGap (l r : W) :
    framedElevenExactSpine l r (originalDoubleWhiskerLeftFrame l r) ≠
      framedElevenExactSpine l r (originalDoubleWhiskerRightFrame l r) :=
  doubleWhiskerExactSpineGap l r
    (.refl _) (.exchangeUnit) (.refl _)

theorem doubleWhiskerEightCompatible_notExactSpine (l r : W)
    {w z : W}
    {c d e f₆ : PentagonAdjoinedSixCell W l r w z}
    (before : SevenRewrite W l r c d)
    {s t : SevenRewrite W l r d e}
    {q q' : PentagonAssocEightCell W l r s t}
    {alpha beta : MixedCancelNineCell W l r q q'}
    {xi zeta : MixedUnitAssocTenCell W l r alpha beta}
    (H : MixedExchangeUnitElevenCell W l r xi zeta)
    (after : SevenRewrite W l r e f₆) :
    (Nonempty (EightCell W l r
       (.trans before (.trans s after))
       (.trans (.trans before s) after)) ∧
     Nonempty (EightCell W l r
       (.trans before (.trans t after))
       (.trans (.trans before t) after))) ∧
    framedElevenExactSpine l r
        (doubleWhiskerLeftAfterRightFrame l r before H after) ≠
      framedElevenExactSpine l r
        (doubleWhiskerRightAfterLeftFrame l r before H after) :=
  ⟨doubleWhiskerBoundaryCompatibility l r before after,
    doubleWhiskerExactSpineGap l r before H after⟩

theorem originalDoubleWhisker_noExactFiberLift (l r : W) :
    ¬ Nonempty (FramedExactFiberTwelfthLift l r
      (originalDoubleWhiskerLeftFrame l r)
      (originalDoubleWhiskerRightFrame l r)) := by
  rintro ⟨⟨e, T⟩⟩
  exact originalDoubleWhiskerExactSpineGap l r e

theorem originalDoubleWhisker_notInherited (l r : W) :
    ¬ Nonempty (FramedInheritedTwelfth W l r
      (originalDoubleWhiskerLeftFrame l r)
      (originalDoubleWhiskerRightFrame l r)) := by
  intro h
  exact originalDoubleWhisker_noExactFiberLift l r
    ((framedInheritedTwelfth_iff_exactFiber l r _ _).mp h)

/-- The added framed interchanger is strictly new relative to
ALL old twelfth witnesses plus strict/reverse/chain closure.
Merely possessing two eighth associators does not fix this. -/
theorem framedDoubleWhisker_strictBeyondExact (l r : W) :
    Nonempty (FramedDoubleWhiskerTwelveCell W l r
      (originalDoubleWhiskerLeftFrame l r)
      (originalDoubleWhiskerRightFrame l r)) ∧
    ¬ Nonempty (FramedInheritedTwelfth W l r
      (originalDoubleWhiskerLeftFrame l r)
      (originalDoubleWhiskerRightFrame l r)) ∧
    ¬ Nonempty (FramedExactFiberTwelfthLift l r
      (originalDoubleWhiskerLeftFrame l r)
      (originalDoubleWhiskerRightFrame l r)) :=
  ⟨(originalDoubleWhiskerFramedCompletion l r).1,
    originalDoubleWhisker_notInherited l r,
    originalDoubleWhisker_noExactFiberLift l r⟩

/-- One cannot globally interpret every framed comparison as
an exact-fiber old twelfth certificate. -/
theorem framedDoubleWhisker_noUniversalExactTransport (l r : W) :
    ¬ (∀ (F G : FramedEleven W l r),
      FramedDoubleWhiskerTwelveCell W l r F G →
        Nonempty (FramedExactFiberTwelfthLift l r F G)) := by
  intro interpret
  exact originalDoubleWhisker_noExactFiberLift l r
    (interpret _ _ (.doubleWhisker (.refl _) (.exchangeUnit) (.refl _)))

/-- The inherited-only comparison is an honest equivalence
relation, with NO new double-whisker comparison constructor. -/
def framedInheritedTwelfthSetoid (W : Type uSix) (l r : W) :
    Setoid (FramedEleven W l r) where
  r := fun F G => Nonempty (FramedInheritedTwelfth W l r F G)
  iseqv := by
    constructor
    · intro F
      exact ⟨.strict F⟩
    · intro F G h
      rcases h with ⟨T⟩
      exact ⟨.reverse T⟩
    · intro F G K h h'
      rcases h with ⟨T⟩
      rcases h' with ⟨U⟩
      exact ⟨.chain T U⟩

def framedInheritedTwelfthClass
    (F : FramedEleven W long short) :
    Quotient (framedInheritedTwelfthSetoid W long short) :=
  Quotient.mk _ F

theorem framedInheritedTwelfthClass_eq_iff
    (F G : FramedEleven W long short) :
    framedInheritedTwelfthClass F = framedInheritedTwelfthClass G ↔
      Nonempty (FramedInheritedTwelfth W long short F G) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- IMPORTANT POSITIVE DESCENT. Complete raw spine (6D–10D)
is an actual observer on the inherited-only quotient because its
value is preserved by EVERY old-only framed comparison. -/
def framedInheritedSpineObserver :
    Quotient (framedInheritedTwelfthSetoid W long short) →
      FramedElevenExactSpine W long short :=
  Quotient.lift
    (fun F : FramedEleven W long short =>
      framedElevenExactSpine long short F)
    (by
      intro F G h
      rcases h with ⟨T⟩
      exact framedInheritedTwelfth_preservesSpine long short T)

theorem framedInheritedSpineObserver_onClass
    (F : FramedEleven W long short) :
    framedInheritedSpineObserver (framedInheritedTwelfthClass F) =
      framedElevenExactSpine long short F := rfl

/-- Canonical monotone map from old-only framed classes to the
strictly coarser selected v5.18 framed twelfth quotient. -/
def framedInheritedToFullQuotient :
    Quotient (framedInheritedTwelfthSetoid W long short) →
      Quotient (framedDoubleWhiskerSetoid W long short) :=
  Quotient.lift
    (fun F : FramedEleven W long short => framedDoubleWhiskerClass F)
    (by
      intro F G h
      rcases h with ⟨T⟩
      exact (framedDoubleWhiskerClass_eq_iff F G).2
        ⟨framedInheritedTwelfth_toFull long short T⟩)

theorem framedInheritedToFullQuotient_onClass
    (F : FramedEleven W long short) :
    framedInheritedToFullQuotient (framedInheritedTwelfthClass F) =
      framedDoubleWhiskerClass F := rfl

/-- The v5.18 double-whisker identification really does coarsen
the inherited-only quotient: its canonical map is NOT injective.
This is witnessed at authentic v5.16 original exchange-unit data. -/
theorem framedInheritedToFullQuotient_notInjective (l r : W) :
    ¬ Function.Injective
        (framedInheritedToFullQuotient (W := W)
          (long := l) (short := r)) := by
  intro inj
  have h : framedInheritedTwelfthClass
        (originalDoubleWhiskerLeftFrame l r) =
      framedInheritedTwelfthClass
        (originalDoubleWhiskerRightFrame l r) := by
    apply inj
    exact framedDoubleWhiskerClass_originalCritical l r
  have hs := congrArg
    (framedInheritedSpineObserver (W := W)
      (long := l) (short := r)) h
  change framedElevenExactSpine l r
      (originalDoubleWhiskerLeftFrame l r) =
    framedElevenExactSpine l r
      (originalDoubleWhiskerRightFrame l r) at hs
  exact originalDoubleWhiskerExactSpineGap l r hs

/-- No spine-valued observable on the v5.18 full quotient can
factor the actual inherited-only spine observer along its canonical
quotient map. This is stronger than raw frame inequality alone. -/
theorem framedExactSpine_noFactorThroughFullQuotient (l r : W) :
    ¬ ∃ (recover :
      Quotient (framedDoubleWhiskerSetoid W l r) →
        FramedElevenExactSpine W l r),
      ∀ (q : Quotient (framedInheritedTwelfthSetoid W l r)),
        recover (framedInheritedToFullQuotient q) =
          framedInheritedSpineObserver q := by
  rintro ⟨recover, compatible⟩
  have hL := compatible
    (framedInheritedTwelfthClass (originalDoubleWhiskerLeftFrame l r))
  have hR := compatible
    (framedInheritedTwelfthClass (originalDoubleWhiskerRightFrame l r))
  change recover
      (framedDoubleWhiskerClass (originalDoubleWhiskerLeftFrame l r)) =
    framedElevenExactSpine l r (originalDoubleWhiskerLeftFrame l r) at hL
  change recover
      (framedDoubleWhiskerClass (originalDoubleWhiskerRightFrame l r)) =
    framedElevenExactSpine l r (originalDoubleWhiskerRightFrame l r) at hR
  have heq := congrArg recover
    (framedDoubleWhiskerClass_originalCritical l r)
  exact originalDoubleWhiskerExactSpineGap l r
    (hL.symm.trans (heq.trans hR))

/-- No global left inverse to the old-only → full quotient map:
a left inverse would force injectivity, already disproved. -/
theorem framedInheritedToFullQuotient_noLeftInverse (l r : W) :
    ¬ ∃ (decode :
      Quotient (framedDoubleWhiskerSetoid W l r) →
        Quotient (framedInheritedTwelfthSetoid W l r)),
      ∀ (q : Quotient (framedInheritedTwelfthSetoid W l r)),
        decode (framedInheritedToFullQuotient q) = q := by
  rintro ⟨decode, leftInv⟩
  apply framedInheritedToFullQuotient_notInjective l r
  intro x y h
  calc
    x = decode (framedInheritedToFullQuotient x) := (leftInv x).symm
    _ = decode (framedInheritedToFullQuotient y) :=
      congrArg decode h
    _ = y := leftInv y

/-- The genuinely ORIGINAL 1-versus-0 tenSymm barrier remains,
even with exact-fiber reindexing: the inherited-only grammar
cannot create a non-existent comparison under the old 12D source. -/
theorem framedExactFiber_retainsTenSymmObstruction (l r : W) :
    ¬ Nonempty (FramedInheritedTwelfth W l r
      (framedOriginalTenSymmCriticalLoop l r)
      (framedOriginalTenSymmCriticalRefl l r)) := by
  rintro ⟨T⟩
  exact framedOriginalTenSymm_noComparison l r
    ⟨framedInheritedTwelfth_toFull l r T⟩

end PentagonAdjoinedSixCell

section ActualOriginalP77ExactFiberFrontier
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

/-- Every genuine original P77 final raw index realizes the new
framed 12D comparison, but NOT an exact-fiber old 12D lift;
the original raw five-cell strict equality interpreter remains
impossible. No artificial source or additional axiom is used. -/
theorem pentagonActualExactFiberObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.FramedDoubleWhiskerTwelveCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.originalDoubleWhiskerLeftFrame
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.originalDoubleWhiskerRightFrame
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ Nonempty (PentagonAdjoinedSixCell.FramedExactFiberTwelfthLift
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.originalDoubleWhiskerLeftFrame
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.originalDoubleWhiskerRightFrame
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨(PentagonAdjoinedSixCell.originalDoubleWhiskerFramedCompletion
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)).1,
    PentagonAdjoinedSixCell.originalDoubleWhisker_noExactFiberLift _ _,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.FramedElevenExactSpine
#print axioms PentagonAdjoinedSixCell.framedElevenSpineWitness
#print axioms PentagonAdjoinedSixCell.framedElevenExactSpine
#print axioms PentagonAdjoinedSixCell.framedElevenSpinePack
#print axioms PentagonAdjoinedSixCell.framedElevenSpinePack_exact
#print axioms PentagonAdjoinedSixCell.framedElevenSpineTransport
#print axioms PentagonAdjoinedSixCell.framedElevenSpineTransport_refl
#print axioms PentagonAdjoinedSixCell.FramedExactFiberTwelfthLift
#print axioms PentagonAdjoinedSixCell.framedExactFiberTwelfthLift_refl
#print axioms PentagonAdjoinedSixCell.framedExactFiberTransport_reverse
#print axioms PentagonAdjoinedSixCell.framedExactFiberTransport_chain
#print axioms PentagonAdjoinedSixCell.FramedInheritedTwelfth
#print axioms PentagonAdjoinedSixCell.framedInheritedTwelfth_toFull
#print axioms PentagonAdjoinedSixCell.framedInheritedTwelfth_toExact
#print axioms PentagonAdjoinedSixCell.framedInheritedTwelfth_preservesSpine
#print axioms PentagonAdjoinedSixCell.framedExactTransport_toInherited
#print axioms PentagonAdjoinedSixCell.framedExactFiberTwelfthLift_toInherited
#print axioms PentagonAdjoinedSixCell.framedInheritedTwelfth_iff_exactFiber
#print axioms PentagonAdjoinedSixCell.framedExactFiberLift_sufficientForFull
#print axioms PentagonAdjoinedSixCell.framedExactFiberLift_onOriginal_iff
#print axioms PentagonAdjoinedSixCell.framedInheritedTwelfth_onOriginal_iff
#print axioms PentagonAdjoinedSixCell.doubleWhiskerExactSpineGap
#print axioms PentagonAdjoinedSixCell.originalDoubleWhiskerExactSpineGap
#print axioms PentagonAdjoinedSixCell.doubleWhiskerEightCompatible_notExactSpine
#print axioms PentagonAdjoinedSixCell.originalDoubleWhisker_noExactFiberLift
#print axioms PentagonAdjoinedSixCell.originalDoubleWhisker_notInherited
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_strictBeyondExact
#print axioms PentagonAdjoinedSixCell.framedDoubleWhisker_noUniversalExactTransport
#print axioms PentagonAdjoinedSixCell.framedInheritedTwelfthSetoid
#print axioms PentagonAdjoinedSixCell.framedInheritedTwelfthClass
#print axioms PentagonAdjoinedSixCell.framedInheritedTwelfthClass_eq_iff
#print axioms PentagonAdjoinedSixCell.framedInheritedSpineObserver
#print axioms PentagonAdjoinedSixCell.framedInheritedSpineObserver_onClass
#print axioms PentagonAdjoinedSixCell.framedInheritedToFullQuotient
#print axioms PentagonAdjoinedSixCell.framedInheritedToFullQuotient_onClass
#print axioms PentagonAdjoinedSixCell.framedInheritedToFullQuotient_notInjective
#print axioms PentagonAdjoinedSixCell.framedExactSpine_noFactorThroughFullQuotient
#print axioms PentagonAdjoinedSixCell.framedInheritedToFullQuotient_noLeftInverse
#print axioms PentagonAdjoinedSixCell.framedExactFiber_retainsTenSymmObstruction
#print axioms pentagonActualExactFiberObstruction

end ActualOriginalP77ExactFiberFrontier
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
