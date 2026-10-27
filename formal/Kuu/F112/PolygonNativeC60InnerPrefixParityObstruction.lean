import Kuu.F112.PolygonNativeC60InnerPrefixStrictTransport

/-!
# F112-P94D3DG — exact finite inner-prefix parity naturality obstruction

DF constructs a genuine strict GROUP EQUIVALENCE for every additional
original finite inner AQ context; DE and CZ retain the full original
15D Type-valued proof provenance. DG determines exactly what is still
necessary to make DC's selected NONCOMMUTATIVE FreeGroup Bool observable
natural along that actual strict equivalence.

Crucial improvement over a tautological "check all strict loops":
because DC's original partial quotient is ONTO FreeGroup Bool,
the full naturality square is equivalent to just:
  (i) exact containment of the original DC quotient kernel under DF;
 (ii) the transported original genuine CZ symm-depth=0 generator
      still maps to the original Bool false group generator; and
(iii) the transported original genuine CZ symm-depth=1 generator
      still maps to the original Bool true group generator.
The two finite witness tests are mathematically sufficient, jointly
with kernel inclusion, for ALL original noncommutative strict loops.
No need to check every independently generated high-dimensional word.

Failure of (i) has an ACTUAL strict pair with equal original parity
but unequal transported parity, by DC's proved fiber/kernel theorem;
failure of either (ii)/(iii) is a concrete original proof-bearing
strict generator obstruction.

The statements explicitly DO NOT assume or assert that all three
obligations hold for arbitrary original inner AQ prefixes. Establishing
the necessary extra CX-to-BV generator transport correspondence is
a separate proof target, not a new 16-cell filler. Full CN and BW
remain non-descending through the noninjective parity quotient.

No Gray, no new geometric 16-cell, no axioms, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDG vDG wDG uD vD uE vE

section ExactFreeTwoLetterCriterion

variable {G : Type uDG} [Group G]
variable {Q : Type vDG} {T : Type wDG} [Group Q] [Group T]

/-- A failure of true partial gauge descent is ALWAYS witnessed by
two actual group elements with the same old quotient value but
different new values. The fibers are those of the ORIGINAL quotient. -/
theorem nativeC60DGKernelFailure_iff_pair
    (q : G →* Q) (f : G →* T) :
    ¬ q.ker ≤ f.ker ↔
      ∃ x y : G, q x = q y ∧ f x ≠ f y := by
  classical
  constructor
  · intro hk
    have hbad : ¬ NativeC60DCFiberCompatible q f := by
      intro hc
      exact hk ((nativeC60DCFiber_iff_kernel_le q f).mp hc)
    unfold NativeC60DCFiberCompatible at hbad
    push Not at hbad
    exact hbad
  · rintro ⟨x, y, hq, hf⟩ hk
    have hc : NativeC60DCFiberCompatible q f :=
      (nativeC60DCFiber_iff_kernel_le q f).mpr hk
    exact hf (hc x y hq)

/-- If a quotient is ONTO the genuine free noncommutative group on
two letters, then a proposed whole-group observable factors exactly
as the SAME observable (rather than an arbitrary quotient endomorphism)
iff kernel inclusion and two ORIGINAL typed generator tests hold.
The type of the original representatives is G, not a model group. -/
theorem nativeC60DGFreeBool_exact_naturality_iff
    (q r : G →* FreeGroup Bool)
    (hq : Function.Surjective q)
    (x0 x1 : G)
    (h0 : q x0 = FreeGroup.of false)
    (h1 : q x1 = FreeGroup.of true) :
    r = q ↔
      q.ker ≤ r.ker ∧
      r x0 = FreeGroup.of false ∧
      r x1 = FreeGroup.of true := by
  constructor
  · intro hr
    subst r
    exact ⟨le_rfl, h0, h1⟩
  · rintro ⟨hker, hr0, hr1⟩
    obtain ⟨decoder, hdecoder⟩ :=
      (nativeC60DCPartial_descent_iff_kernel q hq r).mpr hker
    have hx0 : decoder (FreeGroup.of false) = FreeGroup.of false := by
      have hx := DFunLike.congr_fun hdecoder x0
      change decoder (q x0) = r x0 at hx
      rw [h0] at hx
      exact hx.trans hr0
    have hx1 : decoder (FreeGroup.of true) = FreeGroup.of true := by
      have hx := DFunLike.congr_fun hdecoder x1
      change decoder (q x1) = r x1 at hx
      rw [h1] at hx
      exact hx.trans hr1
    have hid : decoder = MonoidHom.id (FreeGroup Bool) := by
      apply FreeGroup.ext_hom
      intro b
      cases b with
      | false => simpa using hx0
      | true => simpa using hx1
    calc
      r = decoder.comp q := hdecoder.symm
      _ = (MonoidHom.id (FreeGroup Bool)).comp q := by rw [hid]
      _ = q := by
        apply MonoidHom.ext
        intro x
        rfl

/-- Completely explicit trichotomy of failures. Each disjunct is
either a genuine old-parity fiber violation or one of the two distinct
original Bool-free-group generator witness failures. -/
theorem nativeC60DGFreeBool_failure_iff
    (q r : G →* FreeGroup Bool)
    (hq : Function.Surjective q)
    (x0 x1 : G)
    (h0 : q x0 = FreeGroup.of false)
    (h1 : q x1 = FreeGroup.of true) :
    r ≠ q ↔
      (∃ x y : G, q x = q y ∧ r x ≠ r y) ∨
      r x0 ≠ FreeGroup.of false ∨
      r x1 ≠ FreeGroup.of true := by
  simp only [ne_eq]
  rw [nativeC60DGFreeBool_exact_naturality_iff q r hq x0 x1 h0 h1]
  simp only [not_and_or, nativeC60DGKernelFailure_iff_pair, or_assoc]

end ExactFreeTwoLetterCriterion

section OriginalPhysicalInnerPrefix

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

/-- The full original strict map produced by DF, observed by DC's
actual partial noncommutative parity quotient after inner prefix. -/
def nativeK5DGInnerPrefixTransportedParity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DBIsotropy W R inner outer →* FreeGroup Bool :=
  (nativeK5DCParityQuotient W R (shift ++ inner) outer).comp
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).toMonoidHom

/-- Two concrete ORIGINAL Type-valued conservative 15D witness
generators, not abstract test inputs or a numerical charge. -/
def nativeK5DGOriginalParityTestZero
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DBIsotropy W R inner outer :=
  nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of 0)

def nativeK5DGOriginalParityTestOne
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DBIsotropy W R inner outer :=
  nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of 1)

/-- Directly from DC's genuine Type-valued CZ certificates, the
two representatives generate the ENTIRE noncommutative parity target. -/
theorem nativeK5DGOriginalParityTestZero_value
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DCParityQuotient W R inner outer
        (nativeK5DGOriginalParityTestZero W R inner outer) =
      FreeGroup.of false := by
  simpa only [nativeK5DGOriginalParityTestZero] using
    (nativeK5DCParityQuotient_CZ W R inner outer 0)

theorem nativeK5DGOriginalParityTestOne_value
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DCParityQuotient W R inner outer
        (nativeK5DGOriginalParityTestOne W R inner outer) =
      FreeGroup.of true := by
  simpa only [nativeK5DGOriginalParityTestOne] using
    (nativeK5DCParityQuotient_CZ W R inner outer 1)

/-- CORE DG classification: equality of the WHOLE genuine strict
inner-prefix parity square is equivalent to a SINGLE original DC
kernel inclusion plus preservation of TWO concrete original
14D/15D Type-valued proof-bearing generators.

The theorem is unconditional; the right-hand OBLIGATIONS are not
asserted to hold without further original generator transport lemmas. -/
theorem nativeK5DGInnerPrefix_full_parity_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DGInnerPrefixTransportedParity W R inner outer shift =
        nativeK5DCParityQuotient W R inner outer ↔
      (nativeK5DCParityQuotient W R inner outer).ker ≤
        (nativeK5DGInnerPrefixTransportedParity W R inner outer shift).ker ∧
      nativeK5DGInnerPrefixTransportedParity W R inner outer shift
          (nativeK5DGOriginalParityTestZero W R inner outer) =
        FreeGroup.of false ∧
      nativeK5DGInnerPrefixTransportedParity W R inner outer shift
          (nativeK5DGOriginalParityTestOne W R inner outer) =
        FreeGroup.of true :=
  nativeC60DGFreeBool_exact_naturality_iff
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DGInnerPrefixTransportedParity W R inner outer shift)
    (nativeK5DCParityQuotient_surjective W R inner outer)
    (nativeK5DGOriginalParityTestZero W R inner outer)
    (nativeK5DGOriginalParityTestOne W R inner outer)
    (nativeK5DGOriginalParityTestZero_value W R inner outer)
    (nativeK5DGOriginalParityTestOne_value W R inner outer)

/-- Complete proof-carrying obstruction classification: failure of the
inner-prefix parity square MUST be visible as either an actual pair
of distinct strict loops merged by the old coarse quotient but
separated after transport, or one of the two original conservative
15D symm-depth witness checks. -/
theorem nativeK5DGInnerPrefix_full_parity_failure_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DGInnerPrefixTransportedParity W R inner outer shift ≠
        nativeK5DCParityQuotient W R inner outer ↔
      (∃ z z' : nativeK5DBIsotropy W R inner outer,
        nativeK5DCParityQuotient W R inner outer z =
          nativeK5DCParityQuotient W R inner outer z' ∧
        nativeK5DGInnerPrefixTransportedParity W R inner outer shift z ≠
          nativeK5DGInnerPrefixTransportedParity W R inner outer shift z') ∨
      nativeK5DGInnerPrefixTransportedParity W R inner outer shift
          (nativeK5DGOriginalParityTestZero W R inner outer) ≠
        FreeGroup.of false ∨
      nativeK5DGInnerPrefixTransportedParity W R inner outer shift
          (nativeK5DGOriginalParityTestOne W R inner outer) ≠
        FreeGroup.of true :=
  nativeC60DGFreeBool_failure_iff
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DGInnerPrefixTransportedParity W R inner outer shift)
    (nativeK5DCParityQuotient_surjective W R inner outer)
    (nativeK5DGOriginalParityTestZero W R inner outer)
    (nativeK5DGOriginalParityTestOne W R inner outer)
    (nativeK5DGOriginalParityTestZero_value W R inner outer)
    (nativeK5DGOriginalParityTestOne_value W R inner outer)

/-- Original DC exact descent condition is the first DG obstruction.
This is a genuine surjective strict quotient and actual DF group
equivalence, with no invented geometric 16-cell. -/
theorem nativeK5DGInnerPrefix_partial_descent_iff_fiber
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    (∃ decoder : FreeGroup Bool →* FreeGroup Bool,
      decoder.comp (nativeK5DCParityQuotient W R inner outer) =
        nativeK5DGInnerPrefixTransportedParity W R inner outer shift) ↔
      ∀ z z' : nativeK5DBIsotropy W R inner outer,
        nativeK5DCParityQuotient W R inner outer z =
          nativeK5DCParityQuotient W R inner outer z' →
        nativeK5DGInnerPrefixTransportedParity W R inner outer shift z =
          nativeK5DGInnerPrefixTransportedParity W R inner outer shift z' := by
  rw [nativeC60DCPartial_descent_iff_kernel
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient_surjective W R inner outer)
    (nativeK5DGInnerPrefixTransportedParity W R inner outer shift)]
  exact (nativeC60DCFiber_iff_kernel_le
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DGInnerPrefixTransportedParity W R inner outer shift)).symm

end OriginalPhysicalInnerPrefix

#print axioms nativeC60DGKernelFailure_iff_pair
#print axioms nativeC60DGFreeBool_exact_naturality_iff
#print axioms nativeC60DGFreeBool_failure_iff
#print axioms nativeK5DGInnerPrefixTransportedParity
#print axioms nativeK5DGOriginalParityTestZero
#print axioms nativeK5DGOriginalParityTestOne
#print axioms nativeK5DGOriginalParityTestZero_value
#print axioms nativeK5DGOriginalParityTestOne_value
#print axioms nativeK5DGInnerPrefix_full_parity_iff
#print axioms nativeK5DGInnerPrefix_full_parity_failure_iff
#print axioms nativeK5DGInnerPrefix_partial_descent_iff_fiber

end
end Kuu.F112.Physical
