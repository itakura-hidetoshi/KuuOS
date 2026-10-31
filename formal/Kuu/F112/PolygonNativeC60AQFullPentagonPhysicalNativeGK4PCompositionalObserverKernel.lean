import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4OPrimitiveSeamTransportCriterion
import Mathlib.Tactic

/-!
# F112-P94D3GK4P — compositional observation laws imply kernel congruence

GK4O reduces genuine F54 structural-seam preservation to seven primitive
checks ONLY under four explicit equality-kernel congruence assumptions.
Here derive these four assumptions from THREE concrete observation laws:
actual F54 vertical composition is measured by a specified binary operation,
and actual left/right F45 contexts act through specified value functions.
No associativity, unit, injectivity, or invertibility of those value
operations is assumed. These are sufficient observation-law hypotheses,
not a claim that arbitrary original P92B observers satisfy them.

Keep the actual uniform original P92B quotient observer family across
independent D/E categories, all four Blocks, both Nat depths and the
full original F45 source/target. Context actions depend on the actual
context tree. They never manufacture original Type-valued seam evidence.
Connect the derived kernel congruence to BOTH GK4O fourteen-versus-seven
seam equivalence and the actual GK4E structural-quotient descent criterion.

The actual GK4G Boolean family obeys these three laws: Bool.and for
composition and identity value actions for both contexts. The actual
GK4K Option Nat family ALSO obeys them: none-absorbing addition for
composition and identity context actions. Consequently BOTH actual
observer families have all four kernel congruences, unconditionally.

Nevertheless the finer Option Nat family does NOT descend whenever an
original F45 stage exists. The genuine leftUnit structural seam identifies
routes measured as some 2 and some 1. Thus kernel compatibility alone
is NOT sufficient for structural descent; the seven primitive obligations
are mathematically independent requirements in the conditional criterion.
This statement does not assert logical independence of all seven checks
from one another or minimality of the chosen generator set. Boolean
satisfies the full seam criterion and genuinely descends. Retain the
original physical C60 north F45 triple as a concrete instance.

No original P92B associativity or alternative composition, historical
complete typed equivalence, genuine 14D unconditional Countable, 19D
filler, global strict n or hyperdescent is inferred. No new axioms,
proof holes or Gray. Same-root, append-only, 107 public roots unchanged.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected #1558 remains Draft/open/unmerged.
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

/-- Value action indexed by a genuinely typed original F45 context tree.
The source categories, Blocks and both depth indices are retained. -/
abbrev NativeGK4PContextAction
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] (B : Type uB) :=
  ∀ {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y},
    KuuNativeF45Tree p n m ma pa mb pb → B → B

/-- Identity VALUE action; this does not erase or identify the actual
original F54 context route or its Type-valued comparison history. -/
def nativeGK4PIdentityAction
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] (B : Type uB) :
    NativeGK4PContextAction p D E B :=
  fun _ value => value

/-- Three sufficient observation laws. The value binary operation need
not be associative or unital. Both context laws use actual F45 contexts,
not functions on an invented replacement for the original quotient. -/
structure NativeGK4PObservationLaws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B) : Prop where
  map_trans :
    ∀ {a b : D} {x y : E}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
      (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃),
      nativeGK4ORead observe (KuuNativeF45Tree.DepthRotationRoute.trans u v) =
        combine (nativeGK4ORead observe u) (nativeGK4ORead observe v)
  map_leftContext :
    ∀ {a b : D} {x y : E} {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      (r : KuuNativeF45Tree.DepthRotationRoute p first last)
      (later : KuuNativeF45Tree p k l mb pb mc pc),
      nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.leftContext r later) =
        leftAction later (nativeGK4ORead observe r)
  map_rightContext :
    ∀ {a b : D} {x y : E} {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      (r : KuuNativeF45Tree.DepthRotationRoute p first last),
      nativeGK4ORead observe
          (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier r) =
        rightAction earlier (nativeGK4ORead observe r)

/-- Congruence of equality under the three specified value operations
supplies all FOUR actual GK4O kernel transport hypotheses. -/
theorem nativeGK4P_kernel_of_laws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction) :
    NativeGK4OKernelCongruence observe := by
  constructor
  · intro a b x y ma mb pa pb n₁ n₂ n₃ m₁ m₂ m₃ t₁ t₂ t₃ prior r s h
    rw [laws.map_trans prior r, laws.map_trans prior s, h]
  · intro a b x y ma mb pa pb n₁ n₂ n₃ m₁ m₂ m₃ t₁ t₂ t₃ r s suffix h
    rw [laws.map_trans r suffix, laws.map_trans s suffix, h]
  · intro a b x y n n' m m' k l ma mb mc pa pb pc first last r s later h
    rw [laws.map_leftContext r later, laws.map_leftContext s later, h]
  · intro a b x y k l n n' m m' ma mb mc pa pb pc earlier first last r s h
    rw [laws.map_rightContext earlier r, laws.map_rightContext earlier s, h]

/-- Under the three explicit observation laws, GK4O's full typed seam
criterion reduces to seven primitive checks. No laws are weakened. -/
theorem nativeGK4P_full_iff_seven_of_laws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction) :
    NativeGK4OFullInvariant observe ↔ NativeGK4OPrimitiveInvariant observe := by
  exact nativeGK4O_full_iff_seven_of_kernel observe
    (nativeGK4P_kernel_of_laws observe combine leftAction rightAction laws)

/-- The actual independent GK4E structural quotient descent is
characterized by the seven primitive checks under these sufficient
observation laws; the original P92B composition is not replaced. -/
theorem nativeGK4P_factor_iff_seven_of_laws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction) :
    NativeGK4OGlobalFactors observe ↔ NativeGK4OPrimitiveInvariant observe := by
  exact nativeGK4O_global_factor_iff_seven_of_kernel observe
    (nativeGK4P_kernel_of_laws observe combine leftAction rightAction laws)

/-- The genuine GK4G physical zero/positive Boolean observer obeys
actual F54 composition and both context laws, without new assumptions. -/
theorem nativeGK4P_boolean_laws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4PObservationLaws (nativeGK4OBooleanFamily p D E) Bool.and
      (nativeGK4PIdentityAction p D E Bool)
      (nativeGK4PIdentityAction p D E Bool) := by
  constructor
  · intro a b x y ma mb pa pb n₁ n₂ n₃ m₁ m₂ m₃ t₁ t₂ t₃ u v
    change nativeGK4GRawGrade t₁ t₃ (.trans u v) =
      (nativeGK4GRawGrade t₁ t₂ u && nativeGK4GRawGrade t₂ t₃ v)
    exact nativeGK4H_rawGrade_compose t₁ t₂ t₃ u v
  · intro a b x y n n' m m' k l ma mb mc pa pb pc first last r later
    rfl
  · intro a b x y k l n n' m m' ma mb mc pa pb pc earlier first last r
    rfl

/-- The finer, actual GK4K Option Nat observer ALSO obeys the three
laws. Its count and zero-rotation predicate are definitionally unchanged
under genuine left/right contexts; composition is GK4K absorbing addition. -/
theorem nativeGK4P_option_laws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4PObservationLaws (nativeGK4OOptionFamily p D E) nativeGK4KAdd
      (nativeGK4PIdentityAction p D E (Option Nat))
      (nativeGK4PIdentityAction p D E (Option Nat)) := by
  constructor
  · intro a b x y ma mb pa pb n₁ n₂ n₃ m₁ m₂ m₃ t₁ t₂ t₃ u v
    change nativeGK4KRawOption t₁ t₃ (.trans u v) =
      nativeGK4KAdd (nativeGK4KRawOption t₁ t₂ u) (nativeGK4KRawOption t₂ t₃ v)
    exact nativeGK4KRawOption_trans t₁ t₂ t₃ u v
  · intro a b x y n n' m m' k l ma mb mc pa pb pc first last r later
    rfl
  · intro a b x y k l n n' m m' ma mb mc pa pb pc earlier first last r
    rfl

/-- All four GK4O kernel congruences hold for the original Boolean
observer family at ALL actual original dependent F45 boundaries. -/
theorem nativeGK4P_boolean_kernel
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4OKernelCongruence (nativeGK4OBooleanFamily p D E) := by
  exact nativeGK4P_kernel_of_laws (nativeGK4OBooleanFamily p D E) Bool.and
    (nativeGK4PIdentityAction p D E Bool)
    (nativeGK4PIdentityAction p D E Bool) nativeGK4P_boolean_laws

/-- All four GK4O kernel congruences ALSO hold for the original finer
Option Nat observer. This is NOT a proof of primitive unit preservation. -/
theorem nativeGK4P_option_kernel
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4OKernelCongruence (nativeGK4OOptionFamily p D E) := by
  exact nativeGK4P_kernel_of_laws (nativeGK4OOptionFamily p D E) nativeGK4KAdd
    (nativeGK4PIdentityAction p D E (Option Nat))
    (nativeGK4PIdentityAction p D E (Option Nat)) nativeGK4P_option_laws

/-- Boolean has BOTH kernel congruence and actual structural quotient
factors. The factor assertion uses the proven original seam invariance. -/
theorem nativeGK4P_boolean_kernel_and_descent
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4OKernelCongruence (nativeGK4OBooleanFamily p D E) ∧
      NativeGK4OGlobalFactors (nativeGK4OBooleanFamily p D E) := by
  exact ⟨nativeGK4P_boolean_kernel, nativeGK4O_boolean_global_factor⟩

/-- The true left-unit primitive obstruction prevents Option Nat
descent despite its now-proved four kernel compatibility laws. -/
theorem nativeGK4P_option_no_global_factor
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ¬ NativeGK4OGlobalFactors (nativeGK4OOptionFamily p D E) := by
  intro hfactor
  exact nativeGK4O_option_fails_primitive tree
    ((nativeGK4O_global_factor_iff_seven_of_kernel
      (nativeGK4OOptionFamily p D E) nativeGK4P_option_kernel).mp hfactor)

/-- Concrete counterexample to sufficiency of kernel compatibility:
the ACTUAL original Option Nat observer is compatible under all four
transports but has no global structural factor at an inhabited stage. -/
theorem nativeGK4P_option_kernel_without_descent
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    NativeGK4OKernelCongruence (nativeGK4OOptionFamily p D E) ∧
      ¬ NativeGK4OGlobalFactors (nativeGK4OOptionFamily p D E) := by
  exact ⟨nativeGK4P_option_kernel, nativeGK4P_option_no_global_factor tree⟩

/-- The general implication from equality-kernel congruence ALONE to
structural descent is false whenever an actual original F45 stage exists. -/
theorem nativeGK4P_kernel_not_sufficient
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ¬ (∀ observe : NativeGK4OObserverFamily p D E (Option Nat),
      NativeGK4OKernelCongruence observe → NativeGK4OGlobalFactors observe) := by
  intro hall
  exact nativeGK4P_option_no_global_factor tree
    (hall (nativeGK4OOptionFamily p D E) nativeGK4P_option_kernel)

/-- Concrete genuine C60 north P92B quotient: real composition respects
Option Nat equality even though no structural quotient observer recovers
this measurement. No synthetic route space or countability premise. -/
theorem nativeGK4P_physical_north_kernel_vs_descent :
    (∀ prior r s : NativeF55P92AssocRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      nativeGK4KP92Option
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple r =
        nativeGK4KP92Option
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple s →
      nativeGK4KP92Option
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
          (nativeGK4H_p92Compose nativeGK4FPhysicalNorthTriple
            nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple prior r) =
        nativeGK4KP92Option
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
          (nativeGK4H_p92Compose nativeGK4FPhysicalNorthTriple
            nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple prior s)) ∧
    (¬ ∃ lift : NativeGK4EStructuralRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple → Option Nat,
      ∀ q : NativeF55P92AssocRouteClasses
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
        lift (nativeGK4EP92ToStructural
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q) =
          nativeGK4KP92Option
            nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q) := by
  constructor
  · intro prior r s h
    rw [nativeGK4KP92Option_compose, nativeGK4KP92Option_compose, h]
  · exact nativeGK4L_no_option_descent nativeGK4FPhysicalNorthTriple

/-! The three original compiler contracts are retained unchanged. -/

example {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4OKernelCongruence (nativeGK4OBooleanFamily p D E) :=
  nativeGK4P_boolean_kernel

example {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4OKernelCongruence (nativeGK4OOptionFamily p D E) :=
  nativeGK4P_option_kernel

example {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    NativeGK4OKernelCongruence (nativeGK4OOptionFamily p D E) ∧
      ¬ NativeGK4OGlobalFactors (nativeGK4OOptionFamily p D E) :=
  nativeGK4P_option_kernel_without_descent tree

#print axioms NativeGK4PContextAction
#print axioms nativeGK4PIdentityAction
#print axioms NativeGK4PObservationLaws
#print axioms nativeGK4P_kernel_of_laws
#print axioms nativeGK4P_full_iff_seven_of_laws
#print axioms nativeGK4P_factor_iff_seven_of_laws
#print axioms nativeGK4P_boolean_laws
#print axioms nativeGK4P_option_laws
#print axioms nativeGK4P_boolean_kernel
#print axioms nativeGK4P_option_kernel
#print axioms nativeGK4P_boolean_kernel_and_descent
#print axioms nativeGK4P_option_no_global_factor
#print axioms nativeGK4P_option_kernel_without_descent
#print axioms nativeGK4P_kernel_not_sufficient
#print axioms nativeGK4P_physical_north_kernel_vs_descent

end
end Kuu.F112.Physical
