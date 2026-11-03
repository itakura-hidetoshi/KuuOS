import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BGDepthGeneratingPolynomial
import Mathlib.Tactic

/-!
F112-P94D3GK5BH — POSITIVE polynomial support at weights zero and
one, and an exact collapse of GK5BG's full-depth polynomial gate
to GK5BF's W=1 threshold for local ORIGINAL→phi seams.

GK5BG proves the full P92B generating polynomial P(f) in Int[X]
is preserved by every genuine chosen P94A four-cell. It also
recovers N=P(1), S=P(-1), and W=P(2), and distinguishes genuine
P92B loops that the three scalar observations cannot distinguish.

However the polynomial is built ONLY from nonnegative original
wrapper occurrences at finite chosen inversion depths. For ANY
actual typed P92B three-proof (not only north C60) we prove by
induction on ALL NINE constructors:
  W(f)=0 → P(f)=0;
  W(f)=1 → P(f)=1.
The converse P(f)=1 → W(f)=1 follows from GK5BG evaluation at 2.
Thus P(f)=1 ↔ W(f)=1 WITHOUT assumptions on F54 sources.

Consequently W(f)=1 also forces GK5BB N(f)=1 and GK5BE
S(f)=1, and the three numerical necessary conditions of GK5BF
are equivalent to W=1 alone. This theorem explains EXACTLY why
the full polynomial, while strictly stronger for arbitrary
chosen P94A comparisons, adds no NEW numerical obstruction at
the particular local-seam raw-original target polynomial ONE.

Prove the equivalence on the actual P77 source quotient via
GK5BG's Polynomial Int-valued Quotient.lift and GK5BF's
Prop-valued triple-gate descent, not by identification of raw
Type-valued original three-proofs. Actual local seam still
implies W=1. NO converse W=1→seam is asserted. In particular
the GK5BG chosen P92B endomorphism-loop counterexample retains
identical N/S/W but different full polynomials, confirming
full polynomial is stronger for GENERAL selected comparisons.

Strict 空 authority, independent Kuu→Qi, original F54
two-Nat/two-category/Blocks and Type-valued F55 proof history
preserved. Append-only same public root107; protected PR #1558
remains Draft/OPEN/unmerged. Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry/admit/native_decide/new axioms, Gray, universal
GK5AY seam, GK5BA kit, unconditional P89 faithfulness or
unsupported P94A normal form.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- Constructor-by-constructor nonnegative-origin rigidity at
the first TWO possible inverse-depth weights. All nine actual
P92B constructors are covered: original, assocNaturality,
refl, symm, trans, two F45 contexts, F54 pre/post.

The proof never assumes a polynomial with arbitrary negative
coefficients: its coefficients originate from actual source
constructors and only shift/add. -/
theorem NativeF55P92AssocComparison.gk5bhWeight_zero_one_poly
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    (f.gk5bfInverseDepthWeight = 0 →
      f.gk5bgDepthPolynomial = 0) ∧
    (f.gk5bfInverseDepthWeight = 1 →
      f.gk5bgDepthPolynomial = 1) := by
  induction f with
  | original old =>
      constructor
      · intro h
        change (1 : Nat) = 0 at h
        omega
      · intro _
        rfl
  | assocNaturality u v w =>
      constructor
      · intro _
        rfl
      · intro h
        change (0 : Nat) = 1 at h
        omega
  | refl r =>
      constructor
      · intro _
        rfl
      · intro h
        change (0 : Nat) = 1 at h
        omega
  | symm f ih =>
      obtain ⟨hZero, hOne⟩ := ih
      constructor
      · intro h
        have hf : f.gk5bfInverseDepthWeight = 0 := by
          change 2 * f.gk5bfInverseDepthWeight = 0 at h
          omega
        change f.gk5bgDepthPolynomial * Polynomial.X = 0
        rw [hZero hf]
        simp
      · intro h
        change 2 * f.gk5bfInverseDepthWeight = 1 at h
        omega
  | trans f g ihf ihg =>
      obtain ⟨hfZero, hfOne⟩ := ihf
      obtain ⟨hgZero, hgOne⟩ := ihg
      constructor
      · intro h
        change f.gk5bfInverseDepthWeight +
          g.gk5bfInverseDepthWeight = 0 at h
        have hf : f.gk5bfInverseDepthWeight = 0 := by omega
        have hg : g.gk5bfInverseDepthWeight = 0 := by omega
        change f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial = 0
        rw [hfZero hf, hgZero hg]
        ring
      · intro h
        change f.gk5bfInverseDepthWeight +
          g.gk5bfInverseDepthWeight = 1 at h
        have hsplit :
            (f.gk5bfInverseDepthWeight = 1 ∧
              g.gk5bfInverseDepthWeight = 0) ∨
            (f.gk5bfInverseDepthWeight = 0 ∧
              g.gk5bfInverseDepthWeight = 1) := by omega
        change f.gk5bgDepthPolynomial + g.gk5bgDepthPolynomial = 1
        rcases hsplit with ⟨hf, hg⟩ | ⟨hf, hg⟩
        · rw [hfOne hf, hgZero hg]
          ring
        · rw [hfZero hf, hgOne hg]
          ring
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- At weight zero, the entire origin-depth polynomial is ZERO.
An arbitrary signed polynomial cancellation has NOT been used. -/
theorem NativeF55P92AssocComparison.gk5bhPoly_zero_of_weight_zero
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (h : f.gk5bfInverseDepthWeight = 0) :
    f.gk5bgDepthPolynomial = 0 :=
  f.gk5bhWeight_zero_one_poly.1 h

/-- At weight ONE, the entire polynomial is necessarily the
constant ONE, even with arbitrary original F54 route contexts. -/
theorem NativeF55P92AssocComparison.gk5bhPoly_one_of_weight_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (h : f.gk5bfInverseDepthWeight = 1) :
    f.gk5bgDepthPolynomial = 1 :=
  f.gk5bhWeight_zero_one_poly.2 h

/-- Exact all-source equivalence: full polynomial ONE iff
GK5BF inverse-depth weight ONE. The reverse direction uses
GK5BG's formally proved polynomial evaluation at 2. -/
theorem NativeF55P92AssocComparison.gk5bhPoly_one_iff_weight_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    f.gk5bgDepthPolynomial = 1 ↔
      f.gk5bfInverseDepthWeight = 1 := by
  constructor
  · intro hp
    have heval := f.gk5bgEval_two
    rw [hp] at heval
    have hcast : (f.gk5bfInverseDepthWeight : Int) = 1 := by
      simpa using heval.symm
    exact_mod_cast hcast
  · exact f.gk5bhPoly_one_of_weight_one

/-- Because the full polynomial is ONE, both previous scalar
charges are automatically ONE. In particular GK5BF's weight
gate subsumes GK5BB unsigned and GK5BE signed local gates. -/
theorem NativeF55P92AssocComparison.gk5bhWeight_one_implies_N_S
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (hw : f.gk5bfInverseDepthWeight = 1) :
    f.gk5bbOriginalCount = 1 ∧ f.gk5beSignedCount = 1 := by
  have hp := f.gk5bhPoly_one_of_weight_one hw
  have hn := f.gk5bgEval_one
  have hs := f.gk5bgEval_neg_one
  rw [hp] at hn hs
  have hnCast : (f.gk5bbOriginalCount : Int) = 1 := by
    simpa using hn.symm
  have hsInt : f.gk5beSignedCount = 1 := by
    simpa using hs.symm
  exact ⟨by exact_mod_cast hnCast, hsInt⟩

/-- The three GK5BF numerical necessary gates are equivalent
to W=1 alone, for every genuinely typed P92B source proof.
This does NOT supply any P94A seam from the gates. -/
theorem NativeF55P92AssocComparison.gk5bhThree_scalar_gates_iff_weight_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    (f.gk5bbOriginalCount = 1 ∧
      f.gk5beSignedCount = 1 ∧
      f.gk5bfInverseDepthWeight = 1) ↔
      f.gk5bfInverseDepthWeight = 1 := by
  constructor
  · exact fun h => h.2.2
  · intro hw
    obtain ⟨hn, hs⟩ := f.gk5bhWeight_one_implies_N_S hw
    exact ⟨hn, hs, hw⟩

/-- Original source f has the GK5BF three-gate local necessary
certificate iff its structural phi has weight ONE, which in turn
is equivalent to having the full polynomial ONE. -/
theorem nativeGK5BHSource_three_gate_iff_polynomial_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (nativeGK5BFCountSignedGate f ∧ nativeGK5BFWeightGate f) ↔
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial = 1 := by
  constructor
  · rintro ⟨_, hw⟩
    exact ((nativeGK5AIOriginalToP92Structural f).gk5bhPoly_one_iff_weight_one).2 hw
  · intro hp
    have hw := ((nativeGK5AIOriginalToP92Structural f).gk5bhPoly_one_iff_weight_one).1 hp
    have hns := (nativeGK5AIOriginalToP92Structural f).gk5bhWeight_one_implies_N_S hw
    exact ⟨hns, hw⟩

/-- Exact P77 quotient-level equivalence between the existing
three numerical gates and full polynomial equality to ONE.
Use the ACTUAL pre-existing source P77 quotient and independent
GK5BG Polynomial Int-valued Quotient.lift. -/
theorem nativeGK5BHThree_gates_class_iff_poly_one
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s) :
    nativeGK5BFThreeGatesOnP77Class first last r s q ↔
      nativeGK5BGPolyOnP77Class first last r s q = 1 := by
  refine _root_.Quotient.inductionOn q ?_
  intro f
  change (nativeGK5BFCountSignedGate f ∧ nativeGK5BFWeightGate f) ↔
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial = 1
  exact nativeGK5BHSource_three_gate_iff_polynomial_one f

/-- The genuinely constructed local P94A four-cell seam
implies W(phi)=1. The converse is deliberately absent. -/
theorem nativeGK5BHSeam_implies_weight_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bridge : nativeGK5AZSeamAt f) :
    (nativeGK5AIOriginalToP92Structural f).gk5bfInverseDepthWeight = 1 :=
  (nativeGK5BFLocalSeam_three_necessary f bridge).2.2

/-- The complete polynomial is STRICTLY more discriminating for
arbitrary selected P92B 3-proof four-cell comparisons, as GK5BG
already showed with real typed endo-three-proofs. We make clear
this does NOT contradict the unit-threshold gate collapse. -/
theorem nativeGK5BHSelected_comparison_scalar_blind_spot
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ((nativeGK5BGTripleLeft r).gk5bbOriginalCount =
       (nativeGK5BGTripleRight r).gk5bbOriginalCount) ∧
    ((nativeGK5BGTripleLeft r).gk5beSignedCount =
       (nativeGK5BGTripleRight r).gk5beSignedCount) ∧
    ((nativeGK5BGTripleLeft r).gk5bfInverseDepthWeight =
       (nativeGK5BGTripleRight r).gk5bfInverseDepthWeight) ∧
    ((nativeGK5BGTripleLeft r).gk5bgDepthPolynomial ≠
       (nativeGK5BGTripleRight r).gk5bgDepthPolynomial) ∧
    (¬ Nonempty (NativeF55P94UnitFourCell
       (nativeGK5BGTripleLeft r) (nativeGK5BGTripleRight r))) := by
  obtain ⟨hN, hS, hW⟩ := nativeGK5BGTriple_equal_three_scalars r
  exact ⟨hN, hS, hW,
    nativeGK5BGTriple_poly_ne r, nativeGK5BGTriple_no_P94 r⟩

#print axioms NativeF55P92AssocComparison.gk5bhWeight_zero_one_poly
#print axioms NativeF55P92AssocComparison.gk5bhPoly_zero_of_weight_zero
#print axioms NativeF55P92AssocComparison.gk5bhPoly_one_of_weight_one
#print axioms NativeF55P92AssocComparison.gk5bhPoly_one_iff_weight_one
#print axioms NativeF55P92AssocComparison.gk5bhWeight_one_implies_N_S
#print axioms NativeF55P92AssocComparison.gk5bhThree_scalar_gates_iff_weight_one
#print axioms nativeGK5BHSource_three_gate_iff_polynomial_one
#print axioms nativeGK5BHThree_gates_class_iff_poly_one
#print axioms nativeGK5BHSeam_implies_weight_one
#print axioms nativeGK5BHSelected_comparison_scalar_blind_spot

end
end Kuu.F112.Physical
