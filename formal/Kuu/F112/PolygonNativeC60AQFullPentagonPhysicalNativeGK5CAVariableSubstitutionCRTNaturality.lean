import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BZMultivariableCRTNaturality
import Mathlib.Algebra.MvPolynomial.Rename
import Mathlib.Algebra.MvPolynomial.Monad
import Mathlib.Tactic

/-!
F112-P94D3GK5CA — GENUINE MULTIVARIABLE VARIABLE REINDEXING,
POLYNOMIAL SUBSTITUTION AND FINITE NONCOPRIME CRT NATURALITY.

GK5BZ constructed ACTUAL polynomial evaluation RingHoms into the
global ZMod L and the compatible-local dependent-product Subring,
with true finite-cover restriction, CRT RingEquiv and three-cover
naturality. This append-only module proves the NEXT coherence:
arbitrary variable reclassification (including noninjective maps)
and arbitrary polynomial-valued substitution commute with those
evaluations, the true CRT, and finite-cover restriction/towers.

The coefficient ring remains Int, with negative signed coefficients,
zero moduli (ZMod 0 = Int), empty covers and Fin 0 variables allowed.
Original GK5BQ signed numerators are not replaced by natAbs.

These are NUMERIC polynomial and ring-level identities. No
original F55 Type witnesses, P77/P89/P94A comparison proofs or
unconditional original-phi seam are reconstructed; independent Kuu
and strict 空 authorities stay separate. Root107; pinned Lean
v4.30.0-rc2 and mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 remains Draft/open/unmerged.
No axioms, sorry/admit/native_decide, Gray or GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- Reclassifying polynomial variables by any function, even
noninjective, commutes with evaluation in the TRUE global ZMod. -/
theorem nativeGK5CAGlobalMvEval_rename
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (f : σ → τ)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli xs
      ((MvPolynomial.rename f) P) =
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun v => xs (f v)) P :=
  MvPolynomial.eval₂Hom_rename
    (Int.castRingHom (ZMod (nativeGK5BUFiniteModulus s moduli)))
    f xs P

/-- Variable reclassification commutes with evaluation in the
ACTUAL compatible-local CRT dependent-product SUBRING. -/
theorem nativeGK5CACompatibleMvEval_rename
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (f : σ → τ)
    (as : τ → nativeGK5BWCompatibleSubring s moduli)
    (P : MvPolynomial σ Int) :
    nativeGK5BZCompatibleMvEvalHom s moduli as
      ((MvPolynomial.rename f) P) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => as (f v)) P :=
  MvPolynomial.eval₂Hom_rename
    (Int.castRingHom (nativeGK5BWCompatibleSubring s moduli))
    f as P

/-- TRUE arbitrary polynomial substitution commutes with the
global evaluation RingHom: no degree or coprimality hypothesis. -/
theorem nativeGK5CAGlobalMvEval_bind
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int) (P : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli xs
      ((MvPolynomial.bind₁ h) P) =
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun v => nativeGK5BZGlobalMvEvalHom s moduli xs (h v)) P :=
  MvPolynomial.eval₂Hom_bind₁
    (Int.castRingHom (ZMod (nativeGK5BUFiniteModulus s moduli)))
    xs h P

/-- TRUE arbitrary polynomial substitution commutes with
evaluation in the compatible-local CRT subring. -/
theorem nativeGK5CACompatibleMvEval_bind
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (as : τ → nativeGK5BWCompatibleSubring s moduli)
    (h : σ → MvPolynomial τ Int) (P : MvPolynomial σ Int) :
    nativeGK5BZCompatibleMvEvalHom s moduli as
      ((MvPolynomial.bind₁ h) P) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BZCompatibleMvEvalHom s moduli as (h v)) P :=
  MvPolynomial.eval₂Hom_bind₁
    (Int.castRingHom (nativeGK5BWCompatibleSubring s moduli))
    as h P

/-- THE CRT NATURALITY SQUARE for arbitrary reindexing, including
variable collisions, in the true global/local rings. -/
theorem nativeGK5CACRT_rename
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (f : σ → τ)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (nativeGK5BZGlobalMvEvalHom s moduli xs
        ((MvPolynomial.rename f) P)) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs (f v))) P := by
  calc
    _ = nativeGK5BWFiniteCRTRingEquiv s moduli
          (nativeGK5BZGlobalMvEvalHom s moduli
            (fun v => xs (f v)) P) :=
      congrArg (nativeGK5BWFiniteCRTRingEquiv s moduli)
        (nativeGK5CAGlobalMvEval_rename s moduli f xs P)
    _ = _ := nativeGK5BZCRTMvEval_apply s moduli
      (fun v => xs (f v)) P

/-- The local reclassification path uses the same TRUE CRT
images of individual global variables. -/
theorem nativeGK5CALocalCRT_rename
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (f : σ → τ)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs v))
      ((MvPolynomial.rename f) P) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs (f v))) P :=
  nativeGK5CACompatibleMvEval_rename s moduli f
    (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs v)) P

/-- Under arbitrary polynomial substitution, FIRST evaluate
each substituted polynomial, then glue by CRT and evaluate
the outer polynomial. Equals global substitution then CRT. -/
theorem nativeGK5CACRT_bind
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int) (P : MvPolynomial σ Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (nativeGK5BZGlobalMvEvalHom s moduli xs
        ((MvPolynomial.bind₁ h) P)) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
        (nativeGK5BZGlobalMvEvalHom s moduli xs (h v))) P := by
  calc
    _ = nativeGK5BWFiniteCRTRingEquiv s moduli
          (nativeGK5BZGlobalMvEvalHom s moduli
            (fun v => nativeGK5BZGlobalMvEvalHom s moduli xs (h v)) P) :=
      congrArg (nativeGK5BWFiniteCRTRingEquiv s moduli)
        (nativeGK5CAGlobalMvEval_bind s moduli xs h P)
    _ = _ := nativeGK5BZCRTMvEval_apply s moduli
      (fun v => nativeGK5BZGlobalMvEvalHom s moduli xs (h v)) P

/-- SUBSTITUTION-CRT INTERCHANGE: locally substitute the
CRT images of variables, or first evaluate each substituted
polynomial globally and glue its result, then evaluate the
outer polynomial. Both are equal in the same SUBRING. -/
theorem nativeGK5CALocalSubstitution_CRT
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int) (P : MvPolynomial σ Int) :
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs v))
      ((MvPolynomial.bind₁ h) P) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli
        (nativeGK5BZGlobalMvEvalHom s moduli xs (h v))) P := by
  calc
    _ = nativeGK5BZCompatibleMvEvalHom s moduli
          (fun v => nativeGK5BZCompatibleMvEvalHom s moduli
            (fun j => nativeGK5BWFiniteCRTRingEquiv s moduli (xs j))
            (h v)) P :=
      nativeGK5CACompatibleMvEval_bind s moduli
        (fun j => nativeGK5BWFiniteCRTRingEquiv s moduli (xs j)) h P
    _ = _ := congrArg
      (fun ys : σ → nativeGK5BWCompatibleSubring s moduli =>
        nativeGK5BZCompatibleMvEvalHom s moduli ys P)
      (funext fun v => (nativeGK5BZCRTMvEval_apply s moduli xs (h v)).symm)

/-- Finite-cover restriction COMMUTES WITH POLYNOMIAL
SUBSTITUTION in the TRUE global ZMod family. -/
theorem nativeGK5CAGlobalMvEval_restrict_bind
    {ι σ τ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int) (P : MvPolynomial σ Int) :
    nativeGK5BXGlobalRestrictHom s t moduli inc
      (nativeGK5BZGlobalMvEvalHom s moduli xs
        ((MvPolynomial.bind₁ h) P)) =
    nativeGK5BZGlobalMvEvalHom t moduli
      (fun v => nativeGK5BZGlobalMvEvalHom t moduli
        (fun j => nativeGK5BXGlobalRestrictHom s t moduli inc (xs j))
        (h v)) P := by
  calc
    _ = nativeGK5BZGlobalMvEvalHom t moduli
          (fun j => nativeGK5BXGlobalRestrictHom s t moduli inc (xs j))
          ((MvPolynomial.bind₁ h) P) :=
      nativeGK5BZGlobalMvEval_restrict s t moduli inc xs
        ((MvPolynomial.bind₁ h) P)
    _ = _ := nativeGK5CAGlobalMvEval_bind t moduli
      (fun j => nativeGK5BXGlobalRestrictHom s t moduli inc (xs j)) h P

/-- Identical finite-cover substitution coherence in the
TRUE compatible-local dependent-product Subring. -/
theorem nativeGK5CACompatibleMvEval_restrict_bind
    {ι σ τ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s)
    (as : τ → nativeGK5BWCompatibleSubring s moduli)
    (h : σ → MvPolynomial τ Int) (P : MvPolynomial σ Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli inc
      (nativeGK5BZCompatibleMvEvalHom s moduli as
        ((MvPolynomial.bind₁ h) P)) =
    nativeGK5BZCompatibleMvEvalHom t moduli
      (fun v => nativeGK5BZCompatibleMvEvalHom t moduli
        (fun j => nativeGK5BXCompatibleRestrictHom s t moduli inc (as j))
        (h v)) P := by
  calc
    _ = nativeGK5BZCompatibleMvEvalHom t moduli
          (fun j => nativeGK5BXCompatibleRestrictHom s t moduli inc (as j))
          ((MvPolynomial.bind₁ h) P) :=
      nativeGK5BZCompatibleMvEval_restrict s t moduli inc as
        ((MvPolynomial.bind₁ h) P)
    _ = _ := nativeGK5CACompatibleMvEval_bind t moduli
      (fun j => nativeGK5BXCompatibleRestrictHom s t moduli inc (as j)) h P

/-- Three genuine noncoprime covers: substitute integer
polynomials on the LARGEST cover, glue, restrict TWICE,
or restrict every variable to the smallest cover, evaluate
each substituted polynomial there, glue and evaluate.
This is a true global/local CRT substitution tower. -/
theorem nativeGK5CACRT_bind_threeCover
    {ι σ τ : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : u ⊆ t)
    (xs : τ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (h : σ → MvPolynomial τ Int) (P : MvPolynomial σ Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (nativeGK5BZGlobalMvEvalHom s moduli xs
            ((MvPolynomial.bind₁ h) P)))) =
    nativeGK5BZCompatibleMvEvalHom u moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv u moduli
        (nativeGK5BZGlobalMvEvalHom u moduli
          (fun j => nativeGK5BXGlobalRestrictHom s u moduli
            (fun i hi => inc (inc' hi)) (xs j))
          (h v))) P := by
  calc
    _ = nativeGK5BWFiniteCRTRingEquiv u moduli
          (nativeGK5BZGlobalMvEvalHom u moduli
            (fun j => nativeGK5BXGlobalRestrictHom s u moduli
              (fun i hi => inc (inc' hi)) (xs j))
            ((MvPolynomial.bind₁ h) P)) :=
      nativeGK5BZMultivariableCRTTower_natural
        s t u moduli inc inc' xs ((MvPolynomial.bind₁ h) P)
    _ = nativeGK5BWFiniteCRTRingEquiv u moduli
          (nativeGK5BZGlobalMvEvalHom u moduli
            (fun v => nativeGK5BZGlobalMvEvalHom u moduli
              (fun j => nativeGK5BXGlobalRestrictHom s u moduli
                (fun i hi => inc (inc' hi)) (xs j))
              (h v)) P) :=
      congrArg (nativeGK5BWFiniteCRTRingEquiv u moduli)
        (nativeGK5CAGlobalMvEval_bind u moduli
          (fun j => nativeGK5BXGlobalRestrictHom s u moduli
            (fun i hi => inc (inc' hi)) (xs j)) h P)
    _ = _ := nativeGK5BZCRTMvEval_apply u moduli
      (fun v => nativeGK5BZGlobalMvEvalHom u moduli
        (fun j => nativeGK5BXGlobalRestrictHom s u moduli
          (fun i hi => inc (inc' hi)) (xs j))
        (h v)) P

/-- Polynomial substitution respects PRIOR variable
reclassification: noninjective maps remain allowed. -/
theorem nativeGK5CA_bind_rename
    {σ τ υ : Type*}
    (f : σ → τ) (h : τ → MvPolynomial υ Int)
    (P : MvPolynomial σ Int) :
    (MvPolynomial.bind₁ h) ((MvPolynomial.rename f) P) =
      (MvPolynomial.bind₁ (h ∘ f)) P :=
  MvPolynomial.bind₁_rename h f P

/-- Actual polynomial substitution is associative even
for arbitrary variable types and negative coefficients. -/
theorem nativeGK5CA_bind_bind
    {σ τ υ : Type*}
    (h : σ → MvPolynomial τ Int)
    (k : τ → MvPolynomial υ Int)
    (P : MvPolynomial σ Int) :
    (MvPolynomial.bind₁ k) ((MvPolynomial.bind₁ h) P) =
      (MvPolynomial.bind₁
        (fun v => (MvPolynomial.bind₁ k) (h v))) P :=
  MvPolynomial.bind₁_bind₁ h k P

/-- Reclassification before a polynomial-valued substitution
commutes with evaluation in the genuine global CRT ring. -/
theorem nativeGK5CAGlobalMvEval_bind_rename
    {ι σ τ υ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (f : σ → τ) (h : τ → MvPolynomial υ Int)
    (xs : υ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli xs
      ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) P)) =
    nativeGK5BZGlobalMvEvalHom s moduli xs
      ((MvPolynomial.bind₁ (h ∘ f)) P) :=
  congrArg (nativeGK5BZGlobalMvEvalHom s moduli xs)
    (nativeGK5CA_bind_rename f h P)

/-- Reclassification-substitution coherence also holds
inside the actual compatible-local CRT subring. -/
theorem nativeGK5CACompatibleMvEval_bind_rename
    {ι σ τ υ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (f : σ → τ) (h : τ → MvPolynomial υ Int)
    (as : υ → nativeGK5BWCompatibleSubring s moduli)
    (P : MvPolynomial σ Int) :
    nativeGK5BZCompatibleMvEvalHom s moduli as
      ((MvPolynomial.bind₁ h) ((MvPolynomial.rename f) P)) =
    nativeGK5BZCompatibleMvEvalHom s moduli as
      ((MvPolynomial.bind₁ (h ∘ f)) P) :=
  congrArg (nativeGK5BZCompatibleMvEvalHom s moduli as)
    (nativeGK5CA_bind_rename f h P)

/-- Original SIGNED integer variable values: evaluation
after arbitrary genuine polynomial substitution can be
performed in Int BEFORE reduction to any ZMod quotient. -/
theorem nativeGK5CASignedIntMvEval_bind_global
    {ι σ τ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (zs : τ → Int)
    (h : σ → MvPolynomial τ Int) (P : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun v => (zs v : ZMod (nativeGK5BUFiniteModulus s moduli)))
      ((MvPolynomial.bind₁ h) P) =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int)
      (fun v => MvPolynomial.eval₂Hom (Int.castRingHom Int) zs (h v)) P : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) := by
  calc
    _ = ((MvPolynomial.eval₂Hom (Int.castRingHom Int) zs
           ((MvPolynomial.bind₁ h) P) : Int) :
          ZMod (nativeGK5BUFiniteModulus s moduli)) :=
      nativeGK5BZSignedIntMvEval_global s moduli zs ((MvPolynomial.bind₁ h) P)
    _ = _ := congrArg
      (fun z : Int => (z : ZMod (nativeGK5BUFiniteModulus s moduli)))
      (MvPolynomial.eval₂Hom_bind₁ (Int.castRingHom Int) zs h P)

/-- The concrete Fin m → Fin n case includes m=0, n=0
and all NONINJECTIVE variable reindexings without a proof
of finiteness of a fibre or any coprime assumption. -/
theorem nativeGK5CAFinVariableGlobal_rename
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (m n : Nat) (f : Fin m → Fin n)
    (xs : Fin n → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial (Fin m) Int) :
    nativeGK5BZGlobalMvEvalHom s moduli xs
      ((MvPolynomial.rename f) P) =
    nativeGK5BZGlobalMvEvalHom s moduli (fun v => xs (f v)) P :=
  nativeGK5CAGlobalMvEval_rename s moduli f xs P

#print axioms nativeGK5CAGlobalMvEval_rename
#print axioms nativeGK5CACompatibleMvEval_rename
#print axioms nativeGK5CAGlobalMvEval_bind
#print axioms nativeGK5CACompatibleMvEval_bind
#print axioms nativeGK5CACRT_rename
#print axioms nativeGK5CALocalCRT_rename
#print axioms nativeGK5CACRT_bind
#print axioms nativeGK5CALocalSubstitution_CRT
#print axioms nativeGK5CAGlobalMvEval_restrict_bind
#print axioms nativeGK5CACompatibleMvEval_restrict_bind
#print axioms nativeGK5CACRT_bind_threeCover
#print axioms nativeGK5CA_bind_rename
#print axioms nativeGK5CA_bind_bind
#print axioms nativeGK5CAGlobalMvEval_bind_rename
#print axioms nativeGK5CACompatibleMvEval_bind_rename
#print axioms nativeGK5CASignedIntMvEval_bind_global
#print axioms nativeGK5CAFinVariableGlobal_rename

end
end Kuu.F112.Physical
