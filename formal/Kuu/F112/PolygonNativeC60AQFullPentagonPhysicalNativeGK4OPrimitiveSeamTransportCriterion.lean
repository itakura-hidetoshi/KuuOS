import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4NGeneralSeamObserverDescent
import Mathlib.Tactic

/-!
# F112-P94D3GK4O — seven primitive F54 seam checks under explicit kernel congruence

Retain canonical GK4N: any B-valued observer on the genuine ORIGINAL
P92B witness-existence quotient descends through the actual independent
F54 STRUCTURAL-comparison quotient iff it preserves ALL 14 original
Type-valued F54 structural seam constructors. A fixed-endpoint observer
does not automatically commute with vertical pre/post-composition and
dependent horizontal left/right F45 contexts.

Introduce a UNIFORM original P92B observer family over all original F45
source/target trees and all four blocks (with independent original
D/E categories), to retain those varying context boundaries.

Select exactly SEVEN generating structural seam constructors:
  reassoc, leftUnit, rightUnit,
  leftContextTrans, rightContextTrans,
  leftContextUnit, rightContextUnit.
Refl/symm/trans follow from equality. The FOUR remaining constructors
precompose, postcompose, leftContextCongruence, rightContextCongruence
follow by structural induction IF the observation's EQUALITY KERNEL is
explicitly compatible with the corresponding four actual source route
operations. This kernel compatibility is an extra hypothesis, NEVER
silently assumed for arbitrary observations and NOT claimed necessary
for GK4N descent. Under that explicit hypothesis, ALL 14 seam
invariance iff those seven primitive checks, and thus uniform genuine
GK4E structural descent iff the seven checks. The proof retains all
original typed source routes and independent P92B existence quotients;
no shadow equality is promoted to a Type-valued structural seam.

The genuine original GK4G Boolean observer family does descend. The
true GK4K primitive-leaf Option Nat observer family fails ONE primitive
leftUnit seam on every inhabited fully dependent F45 tree: true
original zero-rotation routes have some 2 versus some 1. A concrete
physical C60 north stage inherits the explicit obstruction.

This does NOT prove the four kernel-compatibility hypotheses for every
observer, nor reduce all GK4N checks unconditionally, establish a
minimality theorem for the chosen seven generators, prove original
P92B associativity or alternative composition, historical complete
P92B/F19/F28/F54/F55 typed equivalence, unconditional original
14D Countable, original 19D filler, global strict n or hyperdescent.
No sorry/admit/new axioms/Gray. Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root, 107 public roots, protected validation-only
PR #1558 Draft/open/unmerged.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uB

/-- An observer over ALL original typed F45 boundaries in the same
two independent D/E categories. Every value reads an ACTUAL original
P92B comparison-existence quotient, not a raw Type-valued 3-cell. -/
abbrev NativeGK4OObserverFamily
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] (B : Type uB) :=
  ∀ {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb),
    NativeF55P92AssocRouteClasses first last → B

/-- Evaluate the genuine P92B quotient family on the class of the
ACTUAL original F54 route while retaining all dependent endpoints. -/
def nativeGK4ORead
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : B :=
  observe first last (nativeF55P92AssocRouteClass first last route)

/-- A proof-relevant selector for the SEVEN primitive structural seam
constructors. It is a Prop PREDICATE ON a genuine Type-valued witness:
the witness itself is never coerced from Type to Prop. -/
def nativeGK4OIsPrimitive
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (seam : NativeF54StructuralSeam p r s) : Prop :=
  match seam with
  | .reassoc _ _ _ => True
  | .leftUnit _ => True
  | .rightUnit _ => True
  | .leftContextTrans _ _ _ => True
  | .rightContextTrans _ _ _ => True
  | .leftContextUnit _ _ => True
  | .rightContextUnit _ _ => True
  | _ => False

/-- All actual source F54 structural seams preserve the observer. -/
def NativeGK4OFullInvariant
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B) : Prop :=
  ∀ {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (seam : NativeF54StructuralSeam p r s),
    nativeGK4ORead observe r = nativeGK4ORead observe s

/-- Only SEVEN basic original F54 structural seam constructors are
requested; the other seven are not silently discarded. -/
def NativeGK4OPrimitiveInvariant
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B) : Prop :=
  ∀ {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (seam : NativeF54StructuralSeam p r s),
    nativeGK4OIsPrimitive seam →
      nativeGK4ORead observe r = nativeGK4ORead observe s

/-- Four explicit congruence hypotheses for the EQUALITY KERNEL of
an arbitrary original P92B observer FAMILY, NOT automatic from mere
original P92B quotient well-definedness. Each field changes genuine
F45 endpoints or source blocks exactly as the original F54 route
constructor does. -/
structure NativeGK4OKernelCongruence
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B) : Prop where
  precompose :
    ∀ {a b : D} {x y : E}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (prior : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
      {r s : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃},
      nativeGK4ORead observe r = nativeGK4ORead observe s →
        nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.trans prior r) =
        nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.trans prior s)
  postcompose :
    ∀ {a b : D} {x y : E}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂}
      (suffix : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃),
      nativeGK4ORead observe r = nativeGK4ORead observe s →
        nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.trans r suffix) =
        nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.trans s suffix)
  leftContext :
    ∀ {a b : D} {x y : E} {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (later : KuuNativeF45Tree p k l mb pb mc pc),
      nativeGK4ORead observe r = nativeGK4ORead observe s →
        nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.leftContext r later) =
        nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.leftContext s later)
  rightContext :
    ∀ {a b : D} {x y : E} {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last},
      nativeGK4ORead observe r = nativeGK4ORead observe s →
        nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier r) =
        nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier s)

section PrimitiveClosure
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {B : Type uB}
variable (observe : NativeGK4OObserverFamily p D E B)
variable (hprim : NativeGK4OPrimitiveInvariant observe)
variable (hkernel : NativeGK4OKernelCongruence observe)
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}

/-- FULL typed structural recursion: 7 selected primitive checks,
3 equality constructors, 4 transport/congruence constructors. -/
theorem nativeGK4O_all_seams_of_seven
    (seam : NativeF54StructuralSeam p r s) :
    nativeGK4ORead observe r = nativeGK4ORead observe s := by
  induction seam with
  | refl route =>
      rfl
  | symm w ih =>
      exact ih.symm
  | trans w v ihw ihv =>
      exact ihw.trans ihv
  | reassoc u v w =>
      exact hprim (.reassoc u v w) (by rfl)
  | leftUnit route =>
      exact hprim (.leftUnit route) (by rfl)
  | rightUnit route =>
      exact hprim (.rightUnit route) (by rfl)
  | precompose prior w ih =>
      exact hkernel.precompose prior ih
  | postcompose w suffix ih =>
      exact hkernel.postcompose suffix ih
  | leftContextTrans u v later =>
      exact hprim (.leftContextTrans u v later) (by rfl)
  | rightContextTrans earlier u v =>
      exact hprim (.rightContextTrans earlier u v) (by rfl)
  | leftContextUnit earlier later =>
      exact hprim (.leftContextUnit earlier later) (by rfl)
  | rightContextUnit earlier later =>
      exact hprim (.rightContextUnit earlier later) (by rfl)
  | leftContextCongruence w later ih =>
      exact hkernel.leftContext later ih
  | rightContextCongruence earlier w ih =>
      exact hkernel.rightContext earlier ih

end PrimitiveClosure

/-- Conditional exact theorem. The kernel congruence is an EXPLICIT
additional assumption and is NOT a consequence of GK4N for arbitrary
observers. Under this assumption, all fourteen original seams reduce
to seven primitive proof obligations. -/
theorem nativeGK4O_full_iff_seven_of_kernel
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (hkernel : NativeGK4OKernelCongruence observe) :
    NativeGK4OFullInvariant observe ↔
      NativeGK4OPrimitiveInvariant observe := by
  constructor
  · intro hfull
    intro a b x y n n' m m' ma mb pa pb first last r s seam _
    exact hfull seam
  · intro hprim
    intro a b x y n n' m m' ma mb pa pb first last r s seam
    exact nativeGK4O_all_seams_of_seven observe hprim hkernel seam

/-- Uniform existence of genuine GK4E structural factors across
every valid original F45 source/target and every block boundary. -/
def NativeGK4OGlobalFactors
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B) : Prop :=
  ∀ {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb),
    ∃ lift : NativeGK4EStructuralRouteClasses first last → B,
      ∀ q : NativeF55P92AssocRouteClasses first last,
        lift (nativeGK4EP92ToStructural first last q) =
          observe first last q

/-- GK4N's exact fixed-boundary arbitrary-observer descent criterion,
assembled across ALL original F45 boundary contexts. -/
theorem nativeGK4O_global_factor_iff_full
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B) :
    NativeGK4OGlobalFactors observe ↔ NativeGK4OFullInvariant observe := by
  constructor
  · intro hfactor
    intro a b x y n n' m m' ma mb pa pb first last r s seam
    exact ((nativeGK4N_observer_factor_iff_seam first last
      (observe first last)).mp (hfactor first last)) r s seam
  · intro hfull
    intro a b x y n n' m m' ma mb pa pb first last
    apply (nativeGK4N_observer_factor_iff_seam first last
      (observe first last)).mpr
    intro r s seam
    exact hfull seam

/-- Actual GK4E quotient-factor criterion with the required four
uniform kernel congruences made explicit: global descent iff SEVEN
primitive original F54 seam checks. No unconditional reduction claim. -/
theorem nativeGK4O_global_factor_iff_seven_of_kernel
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (hkernel : NativeGK4OKernelCongruence observe) :
    NativeGK4OGlobalFactors observe ↔
      NativeGK4OPrimitiveInvariant observe := by
  exact (nativeGK4O_global_factor_iff_full observe).trans
    (nativeGK4O_full_iff_seven_of_kernel observe hkernel)

/-- Real physical zero/positive Boolean family on genuine ORIGINAL
P92B quotient classes. -/
def nativeGK4OBooleanFamily
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    NativeGK4OObserverFamily p D E Bool :=
  fun first last q => nativeGK4GP92Grade first last q

/-- Genuine GK4G Boolean family is globally sound on every original
F54 structural seam, independently of any kernel-congruence hypothesis. -/
theorem nativeGK4O_boolean_full
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4OFullInvariant (nativeGK4OBooleanFamily p D E) := by
  intro a b x y n n' m m' ma mb pa pb first last r s seam
  exact nativeGK4N_boolean_seam_sound first last r s seam

/-- The real Boolean family factors through the independent genuine
structural comparison quotient at all original typed F45 boundaries. -/
theorem nativeGK4O_boolean_global_factor
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4OGlobalFactors (nativeGK4OBooleanFamily p D E) := by
  exact (nativeGK4O_global_factor_iff_full _).mpr
    nativeGK4O_boolean_full

/-- Original GK4K Option Nat observer family, which is finer than
the structural Boolean grade and not forced to respect true units. -/
def nativeGK4OOptionFamily
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    NativeGK4OObserverFamily p D E (Option Nat) :=
  fun first last q => nativeGK4KP92Option first last q

/-- Every actually inhabited original F45 stage supplies a single
TRUE Type-valued leftUnit structural generator that violates the
seven basic conditions for GK4K Option Nat. No assumption that the
Option observer's kernel satisfies uniform context congruence. -/
theorem nativeGK4O_option_fails_primitive
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ¬ NativeGK4OPrimitiveInvariant (nativeGK4OOptionFamily p D E) := by
  intro hprim
  let unit : KuuNativeF45Tree.DepthRotationRoute p tree tree :=
    .chain (.refl tree)
  have h := hprim (NativeF54StructuralSeam.leftUnit unit) (by rfl)
  change (some (2 : Nat) : Option Nat) = some 1 at h
  exact (by decide : (some (2 : Nat) : Option Nat) ≠ some 1) h

/-- True original physical C60 north F45 triple provides an
unconditional Type-valued seam obstruction already at the primitive
level, without any global kernel assumption. -/
theorem nativeGK4O_physical_north_option_obstruction :
    ¬ NativeGK4NSeamInvariant
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
        (nativeGK4KP92Option
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact nativeGK4N_original_option_fails_seam nativeGK4FPhysicalNorthTriple

#print axioms NativeGK4OObserverFamily
#print axioms nativeGK4ORead
#print axioms nativeGK4OIsPrimitive
#print axioms NativeGK4OFullInvariant
#print axioms NativeGK4OPrimitiveInvariant
#print axioms NativeGK4OKernelCongruence
#print axioms nativeGK4O_all_seams_of_seven
#print axioms nativeGK4O_full_iff_seven_of_kernel
#print axioms NativeGK4OGlobalFactors
#print axioms nativeGK4O_global_factor_iff_full
#print axioms nativeGK4O_global_factor_iff_seven_of_kernel
#print axioms nativeGK4OBooleanFamily
#print axioms nativeGK4O_boolean_full
#print axioms nativeGK4O_boolean_global_factor
#print axioms nativeGK4OOptionFamily
#print axioms nativeGK4O_option_fails_primitive
#print axioms nativeGK4O_physical_north_option_obstruction

end
end Kuu.F112.Physical
