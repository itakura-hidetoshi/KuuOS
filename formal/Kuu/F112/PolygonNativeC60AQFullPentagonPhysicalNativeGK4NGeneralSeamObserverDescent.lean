import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4MOptionObserverFactorClassification
import Mathlib.Tactic

/-!
# F112-P94D3GK4N — arbitrary original P92B observers: exact structural seam criterion

GK4L states that a map on actual original P92B proof-existence classes
descends along the genuine canonical surjection to the independent
F54 structural-comparison quotient exactly when it is constant on
EVERY full structural quotient fiber. GK4M specializes to postprocessors
of GK4K's genuine zero-rotation conditional Option Nat measurement.

Now handle an ARBITRARY function from the ACTUAL original P92B quotient
to any codomain Type B, at arbitrary original D/E categories, four
Blocks, both Nat depths, fully dependent F45 first/last, and actual F54
route histories. The factorization through the ACTUAL GK4E structural
quotient is possible IFF the observer respects EACH true Type-valued
NativeF54StructuralSeam on original raw representatives. This is a
local proof-obligation criterion over the 14 original F54 seam
constructors. Original P92B generators are already respected because
the function is defined on the original P92B quotient.

Prove this by full induction over the THREE distinct constructors of
NativeF55StructuralComparison: original P92B 3-cell, genuine F54
structural seam, and typed trans of those comparisons. No fake
reverse P92B witness is constructed. The converse uses the true GK4E
structural quotient equality iff and GK4L's universal fiber criterion;
the structural factor is unique by genuine GK4E surjectivity.

Separately, for an ARBITRARY raw F54 B-valued observer (not already
defined on P92B classes), show an exact TWO-family criterion:
it descends through the structural quotient IFF it respects both the
original full Type-valued P92B comparisons and all original full
F54 structural seams. This distinguishes source raw evidence from the
two genuinely different witness-existence quotients.

The true GK4G Boolean grade respects all structural seams because
primitive physical rotation count is unchanged. Conversely one
explicit left-unit F54 seam already separates some 2 from some 1 in
GK4K's genuine original P92B Option Nat quotient. Thus the same
criterion constructs the exact local obstruction from ORIGINAL typed
F54 evidence, at any inhabited F45 stage and unconditionally on the
genuine physical C60 north triple.

This classifies descent of arbitrary original P92B observers through
the FIXED independent GK4E structural quotient. It does NOT prove
original P92B associativity, arbitrary alternative composition,
historical P92B/F19/F28/F54/F55 full typed equivalence, original
14D unconditional Countable, real 19D filler, global strict n,
or hyperdescent; no structural seam is silently made a P92B cell.
No sorry/admit, new axiom, or Gray.

Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only / same-root, 107 public roots remain unchanged. Preserve
validation-only PR #1558 Draft/open/unmerged. Strict 空 center,
independent Kuu one presentation. Copyright Hidetoshi Itakura /
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

section ArbitraryObserver
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- The only EXTRA local obligation for an observer that already lives
on actual original P92B witness-existence classes: invariance under
EVERY original Type-valued F54 structural seam. -/
def nativeGK4NSeamInvariant {B : Type uB}
    (observe : NativeF55P92AssocRouteClasses first last → B) : Prop :=
  ∀ (r s : KuuNativeF45Tree.DepthRotationRoute p first last),
    NativeF54StructuralSeam p r s →
      observe (nativeF55P92AssocRouteClass first last r) =
        observe (nativeF55P92AssocRouteClass first last s)

/-- The full three-constructor structural comparison is sound
whenever an original P92B observer respects every new genuine
F54 seam. The original case uses the EXISTING P92B quotient,
not a fabricated comparison witness. -/
theorem nativeGK4N_structuralComparison_sound
    {B : Type uB}
    (observe : NativeF55P92AssocRouteClasses first last → B)
    (hseam : nativeGK4NSeamInvariant first last observe)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55StructuralComparison p r s) :
    observe (nativeF55P92AssocRouteClass first last r) =
      observe (nativeF55P92AssocRouteClass first last s) := by
  induction cell with
  | original old =>
      exact congrArg observe
        ((nativeF55P92AssocRouteClass_eq_iff first last _ _).mpr ⟨old⟩)
  | structural seam =>
      exact hseam _ _ seam
  | trans left right ihLeft ihRight =>
      exact ihLeft.trans ihRight

/-- EXACT necessary and sufficient condition for ANY B-valued
observer on the genuine original P92B quotient to descend to the
separate genuine structural-comparison existence quotient. -/
theorem nativeGK4N_observer_factor_iff_seam
    {B : Type uB}
    (observe : NativeF55P92AssocRouteClasses first last → B) :
    (∃ lift : NativeGK4EStructuralRouteClasses first last → B,
      ∀ q : NativeF55P92AssocRouteClasses first last,
        lift (nativeGK4EP92ToStructural first last q) = observe q) ↔
      nativeGK4NSeamInvariant first last observe := by
  constructor
  · rintro ⟨lift, hfactor⟩ r s seam
    have hstruct :
        nativeGK4EP92ToStructural first last
            (nativeF55P92AssocRouteClass first last r) =
          nativeGK4EP92ToStructural first last
            (nativeF55P92AssocRouteClass first last s) := by
      simpa only [nativeGK4EP92ToStructural_class] using
        ((nativeGK4EStructuralRouteClass_eq_iff first last r s).mpr
          ⟨NativeF55StructuralComparison.structural seam⟩)
    calc
      observe (nativeF55P92AssocRouteClass first last r) =
          lift (nativeGK4EP92ToStructural first last
            (nativeF55P92AssocRouteClass first last r)) :=
        (hfactor _).symm
      _ = lift (nativeGK4EP92ToStructural first last
            (nativeF55P92AssocRouteClass first last s)) :=
        congrArg lift hstruct
      _ = observe (nativeF55P92AssocRouteClass first last s) := hfactor _
  · intro hseam
    apply (nativeGK4L_factor_iff_fiber_constant first last observe).mpr
    intro q z hqz
    revert hqz
    refine _root_.Quotient.inductionOn q ?_
    intro rawQ hqz
    revert hqz
    refine _root_.Quotient.inductionOn z ?_
    intro rawZ hqz
    have hstruct :
        nativeGK4EStructuralRouteClass first last rawQ =
          nativeGK4EStructuralRouteClass first last rawZ := by
      simpa only [nativeGK4EP92ToStructural_class] using hqz
    rcases (nativeGK4EStructuralRouteClass_eq_iff first last rawQ rawZ).mp
        hstruct with ⟨cell⟩
    exact nativeGK4N_structuralComparison_sound first last observe hseam cell

/-- Surjectivity of GK4E makes the factor of an arbitrary admitted
P92B observer UNIQUE. This is not restricted to Option Nat. -/
theorem nativeGK4N_factor_unique
    {B : Type uB}
    (observe : NativeF55P92AssocRouteClasses first last → B)
    (lift₁ lift₂ : NativeGK4EStructuralRouteClasses first last → B)
    (h₁ : ∀ q : NativeF55P92AssocRouteClasses first last,
      lift₁ (nativeGK4EP92ToStructural first last q) = observe q)
    (h₂ : ∀ q : NativeF55P92AssocRouteClasses first last,
      lift₂ (nativeGK4EP92ToStructural first last q) = observe q) :
    lift₁ = lift₂ := by
  funext z
  rcases nativeGK4EP92ToStructural_surjective first last z with ⟨q, hq⟩
  calc
    lift₁ z = lift₁ (nativeGK4EP92ToStructural first last q) :=
      congrArg lift₁ hq.symm
    _ = observe q := h₁ q
    _ = lift₂ (nativeGK4EP92ToStructural first last q) := (h₂ q).symm
    _ = lift₂ z := congrArg lift₂ hq

/-- The raw original F54 observation respects the ENTIRE separate
structural comparison precisely when it respects both independent
Type-valued generating families: original P92B and structural seams. -/
theorem nativeGK4N_rawComparison_sound
    {B : Type uB}
    (raw : KuuNativeF45Tree.DepthRotationRoute p first last → B)
    (hP92 : ∀ (r s : KuuNativeF45Tree.DepthRotationRoute p first last),
      NativeF55P92AssocComparison p r s → raw r = raw s)
    (hSeam : ∀ (r s : KuuNativeF45Tree.DepthRotationRoute p first last),
      NativeF54StructuralSeam p r s → raw r = raw s)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55StructuralComparison p r s) :
    raw r = raw s := by
  induction cell with
  | original old => exact hP92 _ _ old
  | structural seam => exact hSeam _ _ seam
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight

/-- General RAW F54 observation gluing: the exact two-generator
criterion for a map on raw Type-valued F54 proof terms to descend
to the actual independent STRUCTURAL comparison existence quotient.
Neither original P92B nor new structural seam evidence is erased. -/
theorem nativeGK4N_raw_factor_iff_two_generators
    {B : Type uB}
    (raw : KuuNativeF45Tree.DepthRotationRoute p first last → B) :
    (∃ lift : NativeGK4EStructuralRouteClasses first last → B,
      ∀ r : KuuNativeF45Tree.DepthRotationRoute p first last,
        lift (nativeGK4EStructuralRouteClass first last r) = raw r) ↔
      (∀ (r s : KuuNativeF45Tree.DepthRotationRoute p first last),
        NativeF55P92AssocComparison p r s → raw r = raw s) ∧
      (∀ (r s : KuuNativeF45Tree.DepthRotationRoute p first last),
        NativeF54StructuralSeam p r s → raw r = raw s) := by
  constructor
  · rintro ⟨lift, hfactor⟩
    constructor
    · intro r s cell
      have hclasses :
          nativeGK4EStructuralRouteClass first last r =
            nativeGK4EStructuralRouteClass first last s :=
        (nativeGK4EStructuralRouteClass_eq_iff first last r s).mpr
          ⟨NativeF55StructuralComparison.original cell⟩
      calc
        raw r = lift (nativeGK4EStructuralRouteClass first last r) :=
          (hfactor r).symm
        _ = lift (nativeGK4EStructuralRouteClass first last s) :=
          congrArg lift hclasses
        _ = raw s := hfactor s
    · intro r s seam
      have hclasses :
          nativeGK4EStructuralRouteClass first last r =
            nativeGK4EStructuralRouteClass first last s :=
        (nativeGK4EStructuralRouteClass_eq_iff first last r s).mpr
          ⟨NativeF55StructuralComparison.structural seam⟩
      calc
        raw r = lift (nativeGK4EStructuralRouteClass first last r) :=
          (hfactor r).symm
        _ = lift (nativeGK4EStructuralRouteClass first last s) :=
          congrArg lift hclasses
        _ = raw s := hfactor s
  · rintro ⟨hP92, hSeam⟩
    refine ⟨_root_.Quotient.lift raw (fun r s h => ?_), ?_⟩
    · exact h.elim (fun cell =>
        nativeGK4N_rawComparison_sound first last raw hP92 hSeam cell)
    · intro r
      rfl

/-- The genuine original physical rotation-zero Boolean grade DOES
satisfy all 14 F54 structural seam obligations at every actual F45
source and target, by an existing Type-valued seam rotation theorem. -/
theorem nativeGK4N_boolean_seam_sound
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (seam : NativeF54StructuralSeam p r s) :
    nativeGK4GP92Grade first last
        (nativeF55P92AssocRouteClass first last r) =
      nativeGK4GP92Grade first last
        (nativeF55P92AssocRouteClass first last s) := by
  have hrot := NativeF54StructuralSeam.rotationCount_sound seam
  change decide (r.rotationCount = 0) = decide (s.rotationCount = 0)
  rw [hrot]

/-- In particular GK4G's Boolean grade meets the arbitrary observer
necessary-and-sufficient local seam criterion, and hence descends. -/
theorem nativeGK4N_boolean_seam_invariant :
    nativeGK4NSeamInvariant first last
      (nativeGK4GP92Grade first last) := by
  intro r s seam
  exact nativeGK4N_boolean_seam_sound first last r s seam

end ArbitraryObserver

section GenuineUnitObstruction
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- A SINGLE genuine original F54 leftUnit seam identifies two actual
raw zero-rotation F54 routes whose ORIGINAL P92B GK4K Option Nat
observations are respectively some 2 and some 1. -/
theorem nativeGK4N_genuine_leftUnit_option_obstruction :
    ∃ (r s : KuuNativeF45Tree.DepthRotationRoute p tree tree),
      NativeF54StructuralSeam p r s ∧
      nativeGK4KP92Option tree tree
          (nativeF55P92AssocRouteClass tree tree r) ≠
        nativeGK4KP92Option tree tree
          (nativeF55P92AssocRouteClass tree tree s) := by
  let unit : KuuNativeF45Tree.DepthRotationRoute p tree tree :=
    .chain (.refl tree)
  refine ⟨.trans unit unit, unit, .leftUnit unit, ?_⟩
  have htwo :
      nativeGK4KP92Option tree tree
        (nativeF55P92AssocRouteClass tree tree (.trans unit unit)) =
        some 2 := by
    rfl
  have hone :
      nativeGK4KP92Option tree tree
        (nativeF55P92AssocRouteClass tree tree unit) = some 1 := by
    rfl
  rw [htwo, hone]
  decide

/-- The exact local witness proves GK4K's Option Nat observer fails
the FULL structural seam criterion, regardless of attempted lift. -/
theorem nativeGK4N_original_option_fails_seam :
    ¬ nativeGK4NSeamInvariant tree tree
      (nativeGK4KP92Option tree tree) := by
  intro hs
  rcases nativeGK4N_genuine_leftUnit_option_obstruction tree with
    ⟨r, s, seam, hneq⟩
  exact hneq (hs r s seam)

/-- Contrast at precisely the same actual inhabited original F45
stage: Boolean zero/positive observer respects all genuine seams,
while the finer Option Nat primitive-leaf observer fails already
at one original Type-valued leftUnit seam. -/
theorem nativeGK4N_boolean_yes_option_no :
    nativeGK4NSeamInvariant tree tree
        (nativeGK4GP92Grade tree tree) ∧
      ¬ nativeGK4NSeamInvariant tree tree
        (nativeGK4KP92Option tree tree) := by
  exact ⟨nativeGK4N_boolean_seam_invariant tree tree,
    nativeGK4N_original_option_fails_seam tree⟩

end GenuineUnitObstruction

section PhysicalNorth
/-- Unconditional on the true original C60 north-hexagon F45 tree:
the GENERAL arbitrary-B original P92B observer criterion holds. -/
theorem nativeGK4N_physical_north_general_observer_iff
    {B : Type uB}
    (observe : NativeF55P92AssocRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple → B) :
    (∃ lift : NativeGK4EStructuralRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple → B,
      ∀ q : NativeF55P92AssocRouteClasses
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
        lift (nativeGK4EP92ToStructural
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q) =
          observe q) ↔
      nativeGK4NSeamInvariant
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple observe :=
  nativeGK4N_observer_factor_iff_seam
    nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple observe

/-- Unconditional original physical C60 north leftUnit seam exposes
actual Option Nat some 2 / some 1 non-descent at real F54 routes. -/
theorem nativeGK4N_physical_north_leftUnit_option_obstruction :
    ∃ (r s : KuuNativeF45Tree.DepthRotationRoute
          (.hexagon (.top 0))
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple),
      NativeF54StructuralSeam (.hexagon (.top 0)) r s ∧
      nativeGK4KP92Option
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
          (nativeF55P92AssocRouteClass
            nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple r) ≠
        nativeGK4KP92Option
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
          (nativeF55P92AssocRouteClass
            nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple s) :=
  nativeGK4N_genuine_leftUnit_option_obstruction nativeGK4FPhysicalNorthTriple
end PhysicalNorth

#print axioms nativeGK4NSeamInvariant
#print axioms nativeGK4N_structuralComparison_sound
#print axioms nativeGK4N_observer_factor_iff_seam
#print axioms nativeGK4N_factor_unique
#print axioms nativeGK4N_rawComparison_sound
#print axioms nativeGK4N_raw_factor_iff_two_generators
#print axioms nativeGK4N_boolean_seam_sound
#print axioms nativeGK4N_boolean_seam_invariant
#print axioms nativeGK4N_genuine_leftUnit_option_obstruction
#print axioms nativeGK4N_original_option_fails_seam
#print axioms nativeGK4N_boolean_yes_option_no
#print axioms nativeGK4N_physical_north_general_observer_iff
#print axioms nativeGK4N_physical_north_leftUnit_option_obstruction

end
end Kuu.F112.Physical
