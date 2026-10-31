import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4LStructuralOptionNoDescent
import Mathlib.Tactic

/-!
# F112-P94D3GK4M — exact Boolean boundary for Option Nat postprocessing

The original fully dependent F54 raw witness has a strictly positive
GK4J primitive leaf count, conditionally P92B invariant at ZERO physical
primitive rotations. GK4K descends the precise Option Nat observer to
the ORIGINAL P92B proof-existence quotient, mapping zero rotations to
some (leafCount) and positive rotations to none. GK4L proves this full
Option Nat observer cannot descend to the independently extended
STRUCTURAL existence quotient: one true GK4D unit tower collapses under
the structural quotient while its some(k+1) values remain all distinct.

GK4M settles the precise information-loss boundary FOR ALL POSTPROCESSORS:
for any original inhabited F45 stage t, arbitrary codomain Type B and
f : Option Nat -> B, the composite f ∘ GK4K_P92 descends through the
GENUINE GK4E surjection pi from P92B to structural classes IFF
  forall n > 0, f (some n) = f (some 1).
Equivalently all positive some values are identified. The unique
structural factor is explicit: it evaluates f(some 1) on the actual
GK4G structural zero-rotation Boolean grade true, and f(none) on false.
Thus any surviving postprocessing factors canonically through the
ACTUAL structural Boolean grade. No invertibility, faithfulness or
surjectivity to Bool is claimed at arbitrary typed stages.

We also prove the equivalent pairwise-positive criterion, uniqueness
of a factor through the surjective structural comparison, exact
compatibility of Option.isSome, and the unconditional physical north
C60 F45 stage theorem. In particular the identity postprocessor
fails, agreeing exactly with GK4L.

This does not mean arbitrary P92B observers factor only through Bool;
the classification applies specifically to observations of the form
f ∘ GK4K_P92. Neither original P92B associativity nor a new
composition is claimed. No historical F19/F28/F54/F55/P92B typed
equivalence, original 14D unconditional Countable, 19D filler,
global strict n, or hyperdescent is inferred.

No new axioms, sorry/admit, or Gray. Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root, 107 public roots, protect validation-only
#1558 Draft/open/unmerged. Copyright Hidetoshi Itakura /
板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uB

/-- Every postprocessor that descends to the genuine structural
quotient is determined on GK4K observations by two values:
some 1 (zero rotations) and none (positive rotations). -/
def nativeGK4MShadow {B : Type uB} (f : Option Nat → B) : Bool → B
  | true => f (some 1)
  | false => f none

@[simp] theorem nativeGK4MShadow_true {B : Type uB} (f : Option Nat → B) :
    nativeGK4MShadow f true = f (some 1) := by
  rfl

@[simp] theorem nativeGK4MShadow_false {B : Type uB} (f : Option Nat → B) :
    nativeGK4MShadow f false = f none := by
  rfl

section Classification
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- The canonical factor uses the real structural Boolean grading
already descended in GK4G, not an invented structural comparison. -/
def nativeGK4MCanonicalLift {B : Type uB} (f : Option Nat → B) :
    NativeGK4EStructuralRouteClasses tree tree → B :=
  fun s => nativeGK4MShadow f (nativeGK4GStructuralGrade tree tree s)

/-- Any postprocessor constant on the strictly positive some-values
can be evaluated using only the original P92B Boolean grading. -/
theorem nativeGK4M_shadow_correct
    {B : Type uB} (f : Option Nat → B)
    (hpos : ∀ k : Nat, 0 < k → f (some k) = f (some 1))
    (q : NativeF55P92AssocRouteClasses tree tree) :
    nativeGK4MShadow f (nativeGK4GP92Grade tree tree q) =
      f (nativeGK4KP92Option tree tree q) := by
  have hgrade := nativeGK4KP92Option_grade tree tree q
  cases hopt : nativeGK4KP92Option tree tree q with
  | none =>
      have hbool : nativeGK4GP92Grade tree tree q = false := by
        simpa [hopt] using hgrade.symm
      simp [nativeGK4MShadow, hbool, hopt]
  | some k =>
      have hbool : nativeGK4GP92Grade tree tree q = true := by
        simpa [hopt] using hgrade.symm
      have hk : 0 < k := nativeGK4KP92Option_some_pos tree tree q k hopt
      simpa [nativeGK4MShadow, hbool, hopt] using (hpos k hk).symm

/-- Explicit true GK4E structural quotient factor when the exact
positive-some constancy condition holds. -/
theorem nativeGK4M_canonical_factor_correct
    {B : Type uB} (f : Option Nat → B)
    (hpos : ∀ k : Nat, 0 < k → f (some k) = f (some 1))
    (q : NativeF55P92AssocRouteClasses tree tree) :
    nativeGK4MCanonicalLift tree f
        (nativeGK4EP92ToStructural tree tree q) =
      f (nativeGK4KP92Option tree tree q) := by
  change nativeGK4MShadow f
    (nativeGK4GStructuralGrade tree tree
      (nativeGK4EP92ToStructural tree tree q)) =
    f (nativeGK4KP92Option tree tree q)
  rw [← nativeGK4L_bool_grade_factors tree tree q]
  exact nativeGK4M_shadow_correct tree f hpos q

/-- COMPLETE classification of postprocessed GK4K Option Nat
observations that survive the REAL GK4E structural quotient.
The quantifier on n covers all positive original F54 tower leaves;
none is not constrained, and no arbitrary alternative composition is
introduced. -/
theorem nativeGK4M_postprocess_factor_iff
    {B : Type uB} (f : Option Nat → B) :
    (∃ lift : NativeGK4EStructuralRouteClasses tree tree → B,
      ∀ q : NativeF55P92AssocRouteClasses tree tree,
        lift (nativeGK4EP92ToStructural tree tree q) =
          f (nativeGK4KP92Option tree tree q)) ↔
      (∀ k : Nat, 0 < k → f (some k) = f (some 1)) := by
  constructor
  · rintro ⟨lift, hlift⟩ k hk
    cases k with
    | zero =>
        omega
    | succ j =>
        have hsame :
            f (nativeGK4KP92Option tree tree (nativeGK4ETowerClass tree j)) =
              f (nativeGK4KP92Option tree tree
                (nativeGK4ETowerClass tree 0)) := by
          calc
            f (nativeGK4KP92Option tree tree (nativeGK4ETowerClass tree j)) =
                lift (nativeGK4EP92ToStructural tree tree
                  (nativeGK4ETowerClass tree j)) := (hlift _).symm
            _ = lift (nativeGK4EP92ToStructural tree tree
                  (nativeGK4ETowerClass tree 0)) :=
                congrArg lift (nativeGK4ETowerClass_collapse tree j 0)
            _ = f (nativeGK4KP92Option tree tree
                  (nativeGK4ETowerClass tree 0)) := hlift _
        simpa [nativeGK4L_unitTower_option, Nat.succ_eq_add_one] using hsame
  · intro hpos
    refine ⟨nativeGK4MCanonicalLift tree f, ?_⟩
    intro q
    exact nativeGK4M_canonical_factor_correct tree f hpos q

/-- Equivalent symmetric form: ALL positive integer labels lose their
individual identities under any descended postprocessing. -/
theorem nativeGK4M_postprocess_factor_iff_pairwise
    {B : Type uB} (f : Option Nat → B) :
    (∃ lift : NativeGK4EStructuralRouteClasses tree tree → B,
      ∀ q : NativeF55P92AssocRouteClasses tree tree,
        lift (nativeGK4EP92ToStructural tree tree q) =
          f (nativeGK4KP92Option tree tree q)) ↔
      (∀ i j : Nat, 0 < i → 0 < j →
        f (some i) = f (some j)) := by
  constructor
  · intro h i j hi hj
    have hpos := (nativeGK4M_postprocess_factor_iff tree f).mp h
    exact (hpos i hi).trans (hpos j hj).symm
  · intro h
    apply (nativeGK4M_postprocess_factor_iff tree f).mpr
    intro k hk
    exact h k 1 hk (by omega)

/-- The factor across the GK4E *surjection* is unique even without
assuming a specific target B is decidable or a map is faithful. -/
theorem nativeGK4M_factor_unique
    {B : Type uB} (f : Option Nat → B)
    (lift₁ lift₂ : NativeGK4EStructuralRouteClasses tree tree → B)
    (h₁ : ∀ q : NativeF55P92AssocRouteClasses tree tree,
      lift₁ (nativeGK4EP92ToStructural tree tree q) =
        f (nativeGK4KP92Option tree tree q))
    (h₂ : ∀ q : NativeF55P92AssocRouteClasses tree tree,
      lift₂ (nativeGK4EP92ToStructural tree tree q) =
        f (nativeGK4KP92Option tree tree q)) :
    lift₁ = lift₂ := by
  funext s
  rcases nativeGK4EP92ToStructural_surjective tree tree s with ⟨q, hq⟩
  calc
    lift₁ s = lift₁ (nativeGK4EP92ToStructural tree tree q) :=
      congrArg lift₁ hq.symm
    _ = f (nativeGK4KP92Option tree tree q) := h₁ q
    _ = lift₂ (nativeGK4EP92ToStructural tree tree q) := (h₂ q).symm
    _ = lift₂ s := congrArg lift₂ hq

/-- The explicit Boolean-shadow factor is the UNIQUE lift of any
admissible postprocessor; there are no hidden extra degrees of
freedom on structural quotient classes. -/
theorem nativeGK4M_factor_canonical_unique
    {B : Type uB} (f : Option Nat → B)
    (lift : NativeGK4EStructuralRouteClasses tree tree → B)
    (hlift : ∀ q : NativeF55P92AssocRouteClasses tree tree,
      lift (nativeGK4EP92ToStructural tree tree q) =
        f (nativeGK4KP92Option tree tree q)) :
    lift = nativeGK4MCanonicalLift tree f := by
  have hpos := (nativeGK4M_postprocess_factor_iff tree f).mp ⟨lift, hlift⟩
  apply nativeGK4M_factor_unique tree f lift
    (nativeGK4MCanonicalLift tree f) hlift
  intro q
  exact nativeGK4M_canonical_factor_correct tree f hpos q

/-- GK4K's Option.isSome projection IS the actual coarse GK4G
structural zero/positive-rotation grading after GK4E comparison. -/
theorem nativeGK4M_isSome_descends
    (q : NativeF55P92AssocRouteClasses tree tree) :
    nativeGK4GStructuralGrade tree tree
        (nativeGK4EP92ToStructural tree tree q) =
      (nativeGK4KP92Option tree tree q).isSome := by
  exact ((nativeGK4KP92Option_grade tree tree q).trans
    (nativeGK4L_bool_grade_factors tree tree q)).symm

/-- The unchanged finer Option Nat observer is not eligible for
structural descent; no contradiction with the exact positive-some
classification. -/
theorem nativeGK4M_identity_postprocess_not_factor :
    ¬ ∃ lift : NativeGK4EStructuralRouteClasses tree tree → Option Nat,
        ∀ q : NativeF55P92AssocRouteClasses tree tree,
          lift (nativeGK4EP92ToStructural tree tree q) =
            nativeGK4KP92Option tree tree q := by
  intro hf
  have hpos :=
    (nativeGK4M_postprocess_factor_iff tree (fun o : Option Nat => o)).mp hf
  have heq := hpos 2 (by omega)
  injection heq with heqNat
  omega

end Classification

section PhysicalNorth
/-- On the actual original fully typed physical C60 north-hexagon
F45 triple, every arbitrary codomain B obeys the EXACT same
positive-some collapse criterion. No countability assumptions. -/
theorem nativeGK4M_physical_north_postprocess_factor_iff
    {B : Type uB} (f : Option Nat → B) :
    (∃ lift : NativeGK4EStructuralRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple → B,
      ∀ q : NativeF55P92AssocRouteClasses
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
        lift (nativeGK4EP92ToStructural
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q) =
        f (nativeGK4KP92Option
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q)) ↔
      (∀ k : Nat, 0 < k → f (some k) = f (some 1)) :=
  nativeGK4M_postprocess_factor_iff nativeGK4FPhysicalNorthTriple f
end PhysicalNorth

#print axioms nativeGK4MShadow
#print axioms nativeGK4MShadow_true
#print axioms nativeGK4MShadow_false
#print axioms nativeGK4MCanonicalLift
#print axioms nativeGK4M_shadow_correct
#print axioms nativeGK4M_canonical_factor_correct
#print axioms nativeGK4M_postprocess_factor_iff
#print axioms nativeGK4M_postprocess_factor_iff_pairwise
#print axioms nativeGK4M_factor_unique
#print axioms nativeGK4M_factor_canonical_unique
#print axioms nativeGK4M_isSome_descends
#print axioms nativeGK4M_identity_postprocess_not_factor
#print axioms nativeGK4M_physical_north_postprocess_factor_iff

end
end Kuu.F112.Physical
