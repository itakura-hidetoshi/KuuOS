import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CAVariableSubstitutionCRTNaturality
import Mathlib.Algebra.MvPolynomial.Monad
import Mathlib.Algebra.MvPolynomial.Rename
import Mathlib.Tactic

/-!
F112-P94D3GK5CB — ITERATED GENUINE MULTIVARIABLE INTEGER
POLYNOMIAL SUBSTITUTION, RING-HOM NATURALITY AND
SIMULTANEOUS FINITE-COVER/VARIABLE-RECLASSIFICATION CRT DESCENT.

GK5BW: true noncoprime finite CRT RingEquiv.
GK5BX: true global and compatible-local RingHom restriction towers.
GK5BZ: genuine MvPolynomial σ Int evaluation RingHoms.
GK5CA: arbitrary variable rename and arbitrary single substitution.

GK5CB strengthens these results to (1) TWO COMPOSED arbitrary
polynomial substitutions as RingHom equalities, (2) naturality
of those RingHoms under genuine finite-cover restrictions and
the actual CRT RingEquiv, (3) TWO-STAGE nested evaluation after
restriction and genuine CRT, (4) simultaneous noninjective
variable reclassification and the three-cover substitution tower,
and (5) exact original signed-Int two-stage evaluation.

All variable types are unrestricted, including Fin 0. All
finite covers and Nat moduli, including empty, zero and
noncoprime cases, remain allowed. No degree or injectivity
assumptions. No natAbs proxy, no reconstructed F55 Type source,
P77/P89/P94A proof, original-phi universal seam or higher cell.
Strict 空, independent Kuu→Qi, original F54/F55 history, root107.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 stays Draft/open/unmerged.
Append-only. No new axiom/sorry/admit/native_decide/Gray/GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- Genuine polynomial substitution as a RING HOM: the
coefficients stay Int and variables may be reclassified
or replaced with unrestricted multivariable polynomials. -/
def nativeGK5CBSubstitutionRingHom
    {σ τ : Type*} (h : σ → MvPolynomial τ Int) :
    MvPolynomial σ Int →+* MvPolynomial τ Int :=
  (MvPolynomial.bind₁ h).toRingHom

/-- An actual RingHom from the outer polynomial algebra
to the TRUE global finite CRT residue ring, via arbitrary
integer polynomial-valued substitution. -/
def nativeGK5CBGlobalSubstitutionEvalHom
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int) :
    MvPolynomial σ Int →+* ZMod (nativeGK5BUFiniteModulus s moduli) :=
  (nativeGK5BZGlobalMvEvalHom s moduli xs).comp
    (nativeGK5CBSubstitutionRingHom h)

/-- Genuine RingHom into the TRUE compatible-local ZMod
dependent-product Subring, after polynomial substitution. -/
def nativeGK5CBCompatibleSubstitutionEvalHom
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (as : τ → nativeGK5BWCompatibleSubring s moduli)
    (h : σ → MvPolynomial τ Int) :
    MvPolynomial σ Int →+* nativeGK5BWCompatibleSubring s moduli :=
  (nativeGK5BZCompatibleMvEvalHom s moduli as).comp
    (nativeGK5CBSubstitutionRingHom h)

/-- Two arbitrary substitutions compose STRICTLY as actual
RingHoms on the genuine MvPolynomial Int ring. -/
theorem nativeGK5CBSubstitutionRingHom_assoc
    {σ τ υ : Type*}
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int) :
    (nativeGK5CBSubstitutionRingHom k).comp
      (nativeGK5CBSubstitutionRingHom h) =
    nativeGK5CBSubstitutionRingHom
      (fun v => (MvPolynomial.bind₁ k) (h v)) := by
  apply RingHom.ext
  intro P
  exact nativeGK5CA_bind_bind h k P

/-- The global CRT substitution RingHom is exactly the
evaluation RingHom at the substituted values (not merely
a statement about a chosen polynomial). -/
theorem nativeGK5CBGlobalSubstitutionEvalHom_eq
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int) :
    nativeGK5CBGlobalSubstitutionEvalHom s moduli xs h =
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun v => nativeGK5BZGlobalMvEvalHom s moduli xs (h v)) := by
  apply RingHom.ext
  intro P
  exact nativeGK5CAGlobalMvEval_bind s moduli xs h P

/-- Corresponding strict RingHom equation inside the true
gcd-compatible local CRT Subring. -/
theorem nativeGK5CBCompatibleSubstitutionEvalHom_eq
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (as : τ → nativeGK5BWCompatibleSubring s moduli)
    (h : σ → MvPolynomial τ Int) :
    nativeGK5CBCompatibleSubstitutionEvalHom s moduli as h =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BZCompatibleMvEvalHom s moduli as (h v)) := by
  apply RingHom.ext
  intro P
  exact nativeGK5CACompatibleMvEval_bind s moduli as h P

/-- Iterated substitution is associative as a global CRT
RING HOM, rather than only as a polynomial pointwise value. -/
theorem nativeGK5CBGlobalSubstitutionEvalHom_assoc
    {ι σ τ υ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : υ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int) :
    (nativeGK5CBGlobalSubstitutionEvalHom s moduli xs k).comp
      (nativeGK5CBSubstitutionRingHom h) =
    nativeGK5CBGlobalSubstitutionEvalHom s moduli xs
      (fun v => (MvPolynomial.bind₁ k) (h v)) := by
  apply RingHom.ext
  intro P
  exact congrArg (nativeGK5BZGlobalMvEvalHom s moduli xs)
    (nativeGK5CA_bind_bind h k P)

/-- Iterated substitution is associative as an ACTUAL
compatible-local CRT-subring RingHom. -/
theorem nativeGK5CBCompatibleSubstitutionEvalHom_assoc
    {ι σ τ υ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (as : υ → nativeGK5BWCompatibleSubring s moduli)
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int) :
    (nativeGK5CBCompatibleSubstitutionEvalHom s moduli as k).comp
      (nativeGK5CBSubstitutionRingHom h) =
    nativeGK5CBCompatibleSubstitutionEvalHom s moduli as
      (fun v => (MvPolynomial.bind₁ k) (h v)) := by
  apply RingHom.ext
  intro P
  exact congrArg (nativeGK5BZCompatibleMvEvalHom s moduli as)
    (nativeGK5CA_bind_bind h k P)

/-- A global polynomial-substitution RingHom commutes
STRICTLY with restriction to EVERY finite subcover. -/
theorem nativeGK5CBGlobalSubstitutionEvalHom_restrict
    {ι σ τ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int) :
    (nativeGK5BXGlobalRestrictHom s t moduli inc).comp
      (nativeGK5CBGlobalSubstitutionEvalHom s moduli xs h) =
    nativeGK5CBGlobalSubstitutionEvalHom t moduli
      (fun v => nativeGK5BXGlobalRestrictHom s t moduli inc (xs v)) h := by
  apply RingHom.ext
  intro P
  exact nativeGK5BZGlobalMvEval_restrict s t moduli inc xs
    ((MvPolynomial.bind₁ h) P)

/-- The same strict RingHom naturality for genuine
compatible-local finite noncoprime CRT restrictions. -/
theorem nativeGK5CBCompatibleSubstitutionEvalHom_restrict
    {ι σ τ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (as : τ → nativeGK5BWCompatibleSubring s moduli)
    (h : σ → MvPolynomial τ Int) :
    (nativeGK5BXCompatibleRestrictHom s t moduli inc).comp
      (nativeGK5CBCompatibleSubstitutionEvalHom s moduli as h) =
    nativeGK5CBCompatibleSubstitutionEvalHom t moduli
      (fun v => nativeGK5BXCompatibleRestrictHom s t moduli inc (as v)) h := by
  apply RingHom.ext
  intro P
  exact nativeGK5BZCompatibleMvEval_restrict s t moduli inc as
    ((MvPolynomial.bind₁ h) P)

/-- The ACTUAL CRT RingEquiv intertwines entire arbitrary
polynomial-substitution RingHoms in the true global and
compatible-local rings. This is a RingHom equality. -/
theorem nativeGK5CBCRTSubstitutionEvalHom_natural
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int) :
    (nativeGK5BWGlobalCompatibleHom s moduli).comp
      (nativeGK5CBGlobalSubstitutionEvalHom s moduli xs h) =
    nativeGK5CBCompatibleSubstitutionEvalHom s moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs v)) h := by
  apply RingHom.ext
  intro P
  simpa only [nativeGK5CBGlobalSubstitutionEvalHom,
    nativeGK5CBCompatibleSubstitutionEvalHom,
    nativeGK5CBSubstitutionRingHom, RingHom.comp_apply,
    nativeGK5BWFiniteCRTRingEquiv_apply] using
    (nativeGK5BZCRTMvEval_apply s moduli xs ((MvPolynomial.bind₁ h) P))

/-- Evaluate TWO genuinely nested polynomial substitutions
in the global finite CRT quotient by evaluating the inner
substitution, then the middle one, then the outer polynomial. -/
theorem nativeGK5CBGlobalDoubleBind_expand
    {ι σ τ υ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : υ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int)
    (P : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli xs
      ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P)) =
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun i => nativeGK5BZGlobalMvEvalHom s moduli
        (fun j => nativeGK5BZGlobalMvEvalHom s moduli xs (k j))
        (h i)) P := by
  calc
    _ = nativeGK5BZGlobalMvEvalHom s moduli xs
          ((MvPolynomial.bind₁
            (fun i => (MvPolynomial.bind₁ k) (h i))) P) :=
      congrArg (nativeGK5BZGlobalMvEvalHom s moduli xs)
        (nativeGK5CA_bind_bind h k P)
    _ = nativeGK5BZGlobalMvEvalHom s moduli
          (fun i => nativeGK5BZGlobalMvEvalHom s moduli xs
            ((MvPolynomial.bind₁ k) (h i))) P :=
      nativeGK5CAGlobalMvEval_bind s moduli xs
        (fun i => (MvPolynomial.bind₁ k) (h i)) P
    _ = _ := congrArg
      (fun ys : σ → ZMod (nativeGK5BUFiniteModulus s moduli) =>
        nativeGK5BZGlobalMvEvalHom s moduli ys P)
      (funext fun i =>
        nativeGK5CAGlobalMvEval_bind s moduli xs k (h i))

/-- Two nested true multivariable substitutions also
evaluate in three stages in the compatible-local CRT Subring. -/
theorem nativeGK5CBCompatibleDoubleBind_expand
    {ι σ τ υ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (as : υ → nativeGK5BWCompatibleSubring s moduli)
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int)
    (P : MvPolynomial σ Int) :
    nativeGK5BZCompatibleMvEvalHom s moduli as
      ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P)) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom s moduli
        (fun j => nativeGK5BZCompatibleMvEvalHom s moduli as (k j))
        (h i)) P := by
  calc
    _ = nativeGK5BZCompatibleMvEvalHom s moduli as
          ((MvPolynomial.bind₁
            (fun i => (MvPolynomial.bind₁ k) (h i))) P) :=
      congrArg (nativeGK5BZCompatibleMvEvalHom s moduli as)
        (nativeGK5CA_bind_bind h k P)
    _ = nativeGK5BZCompatibleMvEvalHom s moduli
          (fun i => nativeGK5BZCompatibleMvEvalHom s moduli as
            ((MvPolynomial.bind₁ k) (h i))) P :=
      nativeGK5CACompatibleMvEval_bind s moduli as
        (fun i => (MvPolynomial.bind₁ k) (h i)) P
    _ = _ := congrArg
      (fun ys : σ → nativeGK5BWCompatibleSubring s moduli =>
        nativeGK5BZCompatibleMvEvalHom s moduli ys P)
      (funext fun i =>
        nativeGK5CACompatibleMvEval_bind s moduli as k (h i))

/-- Two-stage substitution and simultaneous arbitrary global
finite-cover restriction commute; all nested variable values
are taken in the SMALLEST global ZMod quotient. -/
theorem nativeGK5CBGlobalDoubleBind_restrict
    {ι σ τ υ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (xs : υ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int)
    (P : MvPolynomial σ Int) :
    nativeGK5BXGlobalRestrictHom s t moduli inc
      (nativeGK5BZGlobalMvEvalHom s moduli xs
        ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P))) =
    nativeGK5BZGlobalMvEvalHom t moduli
      (fun i => nativeGK5BZGlobalMvEvalHom t moduli
        (fun j => nativeGK5BZGlobalMvEvalHom t moduli
          (fun z => nativeGK5BXGlobalRestrictHom s t moduli inc (xs z))
          (k j)) (h i)) P := by
  calc
    _ = nativeGK5BZGlobalMvEvalHom t moduli
          (fun z => nativeGK5BXGlobalRestrictHom s t moduli inc (xs z))
          ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P)) :=
      nativeGK5BZGlobalMvEval_restrict s t moduli inc xs
        ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P))
    _ = _ := nativeGK5CBGlobalDoubleBind_expand t moduli
      (fun z => nativeGK5BXGlobalRestrictHom s t moduli inc (xs z))
      h k P

/-- Two-stage substitution and TRUE compatible-local CRT
restriction commute, including all noncoprime moduli. -/
theorem nativeGK5CBCompatibleDoubleBind_restrict
    {ι σ τ υ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (as : υ → nativeGK5BWCompatibleSubring s moduli)
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int)
    (P : MvPolynomial σ Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli inc
      (nativeGK5BZCompatibleMvEvalHom s moduli as
        ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P))) =
    nativeGK5BZCompatibleMvEvalHom t moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom t moduli
        (fun j => nativeGK5BZCompatibleMvEvalHom t moduli
          (fun z => nativeGK5BXCompatibleRestrictHom s t moduli inc (as z))
          (k j)) (h i)) P := by
  calc
    _ = nativeGK5BZCompatibleMvEvalHom t moduli
          (fun z => nativeGK5BXCompatibleRestrictHom s t moduli inc (as z))
          ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P)) :=
      nativeGK5BZCompatibleMvEval_restrict s t moduli inc as
        ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P))
    _ = _ := nativeGK5CBCompatibleDoubleBind_expand t moduli
      (fun z => nativeGK5BXCompatibleRestrictHom s t moduli inc (as z))
      h k P

/-- Genuine three-cover CRT COHERENCE for TWO arbitrary
polynomial substitutions: global substitute/evaluate on s,
glue by the TRUE CRT, restrict via t and u; equals TRIPLE
NESTED LOCAL evaluation directly at u. -/
theorem nativeGK5CBCRTDoubleBind_threeCover
    {ι σ τ υ : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u ⊆ t)
    (xs : υ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int)
    (P : MvPolynomial σ Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (nativeGK5BZGlobalMvEvalHom s moduli xs
            ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P))))) =
    nativeGK5BZCompatibleMvEvalHom u moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom u moduli
        (fun j => nativeGK5BZCompatibleMvEvalHom u moduli
          (fun z => nativeGK5BWFiniteCRTRingEquiv u moduli
            (nativeGK5BXGlobalRestrictHom s u moduli
              (fun v hv => inc (inc' hv)) (xs z)))
          (k j)) (h i)) P := by
  calc
    _ = nativeGK5BWFiniteCRTRingEquiv u moduli
          (nativeGK5BZGlobalMvEvalHom u moduli
            (fun z => nativeGK5BXGlobalRestrictHom s u moduli
              (fun v hv => inc (inc' hv)) (xs z))
            ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P))) :=
      nativeGK5BZMultivariableCRTTower_natural s t u moduli
        inc inc' xs ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P))
    _ = nativeGK5BZCompatibleMvEvalHom u moduli
          (fun z => nativeGK5BWFiniteCRTRingEquiv u moduli
            (nativeGK5BXGlobalRestrictHom s u moduli
              (fun v hv => inc (inc' hv)) (xs z)))
          ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P)) :=
      nativeGK5BZCRTMvEval_apply u moduli
        (fun z => nativeGK5BXGlobalRestrictHom s u moduli
          (fun v hv => inc (inc' hv)) (xs z))
        ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P))
    _ = _ := nativeGK5CBCompatibleDoubleBind_expand u moduli
      (fun z => nativeGK5BWFiniteCRTRingEquiv u moduli
        (nativeGK5BXGlobalRestrictHom s u moduli
          (fun v hv => inc (inc' hv)) (xs z))) h k P

/-- Genuine global CRT numeric evaluation: an arbitrary
variable reclassification BEFORE TWO substitutions equals
three-stage evaluation with reclassified outer variables. -/
theorem nativeGK5CBGlobalRenameDoubleBind
    {ι σ τ υ ω : Type*} (s : Finset ι) (moduli : ι → Nat)
    (f : σ → τ)
    (h : τ → MvPolynomial υ Int)
    (k : υ → MvPolynomial ω Int)
    (xs : ω → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli xs
      ((MvPolynomial.bind₁ k)
        ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) P))) =
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun i => nativeGK5BZGlobalMvEvalHom s moduli
        (fun j => nativeGK5BZGlobalMvEvalHom s moduli xs (k j))
        (h (f i))) P := by
  calc
    _ = nativeGK5BZGlobalMvEvalHom s moduli xs
          ((MvPolynomial.bind₁ k)
            ((MvPolynomial.bind₁ (h ∘ f)) P)) :=
      congrArg (nativeGK5BZGlobalMvEvalHom s moduli xs)
        (congrArg (MvPolynomial.bind₁ k)
          (nativeGK5CA_bind_rename f h P))
    _ = _ := nativeGK5CBGlobalDoubleBind_expand s moduli xs
      (h ∘ f) k P

/-- SAME triple substitution/reclassification coherence in
the ACTUAL compatible-local CRT Subring, with collisions. -/
theorem nativeGK5CBCompatibleRenameDoubleBind
    {ι σ τ υ ω : Type*} (s : Finset ι) (moduli : ι → Nat)
    (f : σ → τ)
    (h : τ → MvPolynomial υ Int)
    (k : υ → MvPolynomial ω Int)
    (as : ω → nativeGK5BWCompatibleSubring s moduli)
    (P : MvPolynomial σ Int) :
    nativeGK5BZCompatibleMvEvalHom s moduli as
      ((MvPolynomial.bind₁ k)
        ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) P))) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom s moduli
        (fun j => nativeGK5BZCompatibleMvEvalHom s moduli as (k j))
        (h (f i))) P := by
  calc
    _ = nativeGK5BZCompatibleMvEvalHom s moduli as
          ((MvPolynomial.bind₁ k)
            ((MvPolynomial.bind₁ (h ∘ f)) P)) :=
      congrArg (nativeGK5BZCompatibleMvEvalHom s moduli as)
        (congrArg (MvPolynomial.bind₁ k)
          (nativeGK5CA_bind_rename f h P))
    _ = _ := nativeGK5CBCompatibleDoubleBind_expand s moduli as
      (h ∘ f) k P

/-- SIMULTANEOUS finite-cover restriction, CRT gluing,
noninjective variable reclassification and two genuine
polynomial substitutions form one commuting diagram.
All evaluation on the RHS is at the smallest cover u. -/
theorem nativeGK5CBCRTRenameDoubleBind_threeCover
    {ι σ τ υ ω : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u ⊆ t)
    (f : σ → τ)
    (h : τ → MvPolynomial υ Int)
    (k : υ → MvPolynomial ω Int)
    (xs : ω → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (nativeGK5BZGlobalMvEvalHom s moduli xs
            ((MvPolynomial.bind₁ k)
              ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) P)))))) =
    nativeGK5BZCompatibleMvEvalHom u moduli
      (fun i => nativeGK5BZCompatibleMvEvalHom u moduli
        (fun j => nativeGK5BZCompatibleMvEvalHom u moduli
          (fun z => nativeGK5BWFiniteCRTRingEquiv u moduli
            (nativeGK5BXGlobalRestrictHom s u moduli
              (fun v hv => inc (inc' hv)) (xs z)))
          (k j)) (h (f i))) P := by
  have hreclass :
      (MvPolynomial.bind₁ k)
          ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) P)) =
      (MvPolynomial.bind₁ k)
          ((MvPolynomial.bind₁ (h ∘ f)) P) :=
    congrArg (MvPolynomial.bind₁ k) (nativeGK5CA_bind_rename f h P)
  rw [hreclass]
  exact nativeGK5CBCRTDoubleBind_threeCover s t u moduli
    inc inc' xs (h ∘ f) k P

/-- Both integer substitutions can be evaluated on the
ORIGINAL SIGNED Int coordinates BEFORE reduction, with the
same genuine global finite CRT class, including ZMod 0. -/
theorem nativeGK5CBSignedIntDoubleBind_global
    {ι σ τ υ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (zs : υ → Int)
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int)
    (P : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun z => (zs z : ZMod (nativeGK5BUFiniteModulus s moduli)))
      ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P)) =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
      (fun i => MvPolynomial.eval₂Hom (Int.castRingHom Int)
        (fun j => MvPolynomial.eval₂Hom (Int.castRingHom Int) zs (k j))
        (h i)) P : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) := by
  calc
    _ = ((MvPolynomial.eval₂Hom (Int.castRingHom Int) zs
          ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P)) : Int) :
        ZMod (nativeGK5BUFiniteModulus s moduli)) :=
      nativeGK5BZSignedIntMvEval_global s moduli zs
        ((MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P))
    _ = ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
          (fun j => MvPolynomial.eval₂Hom (Int.castRingHom Int)
            zs (k j)) ((MvPolynomial.bind₁ h) P) : Int) :
          ZMod (nativeGK5BUFiniteModulus s moduli)) :=
      congrArg
        (fun z : Int => (z : ZMod (nativeGK5BUFiniteModulus s moduli)))
        (MvPolynomial.eval₂Hom_bind₁ (Int.castRingHom Int) zs k
          ((MvPolynomial.bind₁ h) P))
    _ = _ :=
      congrArg
        (fun z : Int => (z : ZMod (nativeGK5BUFiniteModulus s moduli)))
        (MvPolynomial.eval₂Hom_bind₁ (Int.castRingHom Int)
          (fun j => MvPolynomial.eval₂Hom (Int.castRingHom Int) zs (k j))
          h P)

#print axioms nativeGK5CBSubstitutionRingHom_assoc
#print axioms nativeGK5CBGlobalSubstitutionEvalHom_eq
#print axioms nativeGK5CBCompatibleSubstitutionEvalHom_eq
#print axioms nativeGK5CBGlobalSubstitutionEvalHom_assoc
#print axioms nativeGK5CBCompatibleSubstitutionEvalHom_assoc
#print axioms nativeGK5CBGlobalSubstitutionEvalHom_restrict
#print axioms nativeGK5CBCompatibleSubstitutionEvalHom_restrict
#print axioms nativeGK5CBCRTSubstitutionEvalHom_natural
#print axioms nativeGK5CBGlobalDoubleBind_expand
#print axioms nativeGK5CBCompatibleDoubleBind_expand
#print axioms nativeGK5CBGlobalDoubleBind_restrict
#print axioms nativeGK5CBCompatibleDoubleBind_restrict
#print axioms nativeGK5CBCRTDoubleBind_threeCover
#print axioms nativeGK5CBGlobalRenameDoubleBind
#print axioms nativeGK5CBCompatibleRenameDoubleBind
#print axioms nativeGK5CBCRTRenameDoubleBind_threeCover
#print axioms nativeGK5CBSignedIntDoubleBind_global

end
end Kuu.F112.Physical
