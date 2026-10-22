import Kuu.F112.PolygonNativeF55P91RotationDefectConstraint
import Kuu.F112.PolygonNativeF55TypedSquareRouteComparisonP67

/-!
# F112-P91B — exact original F55 witness quotient of genuine F54 route objects

P91A proved source F54 rotation-count defect equals the original F55
pentagon integer shadow for all nine original Type-valued 3-cell
constructors. P90B's associator-naturality comparison is still an
UNINHABITED-STATUS Type slot, not a constructed filler.

P91B constructs a DIFFERENT route-object presentation: only actual
original nine-constructor Type-valued F55 3-cell existence generates
a Prop-valued Setoid on genuinely typed F54 route objects. This is
not the P89 quotient of F55 3-proofs, and the old raw source is intact.

We prove the exact kernel, old square-only P67 comparison map,
and original full-F55 pentagon comparing the genuinely 3-vs-2
rotation histories. Thus raw F54 rotation count descends to the
old square-only P67 quotient but PROVABLY NOT to the new full-F55
route quotient. Source rotation count loss is explicit, while actual
F55 witnesses retain their full signed pentagon/square/odd-phase
shadow independently.

For the P90 triple-route associator-naturality slot, the new route
class equality is exactly equivalent to the mere existence of an
original F55 Type-valued filler. We do NOT claim that equality or
filler holds. No Gray, sorry/admit, new axioms, or retired roots.
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
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}

/-- Least route-object Setoid defined by existence of an ACTUAL
original nine-constructor F55 Type 3-cell, NOT same shadow/charge. -/
def nativeF55P91FullWitnessRouteSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Setoid (KuuNativeF45Tree.DepthRotationRoute p first last) where
  r := fun u v => Nonempty (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
  iseqv := ⟨
    (fun route => ⟨.ident route⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun z => ⟨.trans w z⟩)))⟩

/-- Quotient of ACTUAL original F54 routes, distinct from the
P89 quotient of original F55 3-proofs. -/
abbrev NativeF55P91FullWitnessRouteClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :=
  _root_.Quotient (nativeF55P91FullWitnessRouteSetoid first last)

/-- Canonical map from an original F54 route, NEVER replacing its raw proof. -/
def nativeF55P91FullWitnessRouteClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P91FullWitnessRouteClasses first last :=
  _root_.Quotient.mk _ route

/-- Exact source-witness kernel: a class equality iff an ORIGINAL
genuine typed F55 PresentedCell exists. No shadow equality shortcut. -/
theorem nativeF55P91FullWitnessRouteClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55P91FullWitnessRouteClass first last u =
      nativeF55P91FullWitnessRouteClass first last v ↔
      Nonempty (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) := by
  constructor
  · intro h
    exact _root_.Quotient.exact h
  · intro h
    exact _root_.Quotient.sound h

/-- Any GIVEN real original F55 proof supplies equality in the
new route-object presentation, without rewriting original raw paths. -/
theorem nativeF55P91FullWitnessRouteClass_eq_of_cell
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55P91FullWitnessRouteClass first last u =
      nativeF55P91FullWitnessRouteClass first last v :=
  _root_.Quotient.sound ⟨cell⟩

/-- The ACTUAL four-original-stage F54 long/short pentagon histories
become equal in this NEW quotient by a genuine original F55 pentagon
generator, while their raw histories remain distinct. -/
theorem nativeF55P91FullWitnessRoute_pentagon_class_eq
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    nativeF55P91FullWitnessRouteClass
      (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄) =
    nativeF55P91FullWitnessRouteClass
      (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄) :=
  nativeF55P91FullWitnessRouteClass_eq_of_cell _ _
    (.pentagon t₁ t₂ t₃ t₄)

/-- A TRUE strict enlargement on arbitrary four-original-stage source:
the new route quotient cannot be injective. -/
theorem nativeF55P91FullWitnessRoute_pentagon_notInjective
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    ¬ Function.Injective
      (nativeF55P91FullWitnessRouteClass
        (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
        (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄)) := by
  intro hinj
  exact (KuuNativeF45Tree.DepthRotationRoute.pentagonLong_ne_short t₁ t₂ t₃ t₄)
    (hinj (nativeF55P91FullWitnessRoute_pentagon_class_eq t₁ t₂ t₃ t₄))

/-- Original F54 rotationCount does NOT descend to the new full-F55
witness quotient: it would equate the genuine 3-vs-2 pentagon count.
This precisely records which source observation is lost. -/
theorem nativeF55P91FullWitnessRoute_rotationCount_noDescent
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    ¬ ∃ readout :
        NativeF55P91FullWitnessRouteClasses
          (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
          (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄) → Nat,
      ∀ route, readout
        (nativeF55P91FullWitnessRouteClass
          (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
          (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄) route) =
        route.rotationCount := by
  rintro ⟨readout, hread⟩
  have h := congrArg readout
    (nativeF55P91FullWitnessRoute_pentagon_class_eq t₁ t₂ t₃ t₄)
  rw [hread, hread,
    KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count,
    KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count] at h
  exact (by decide : (3 : Nat) ≠ 2) h

/-- OLD P67 square-only comparisons preserve the real primitive
rotation count, including symmetry and concatenation; the square
generator is 2-to-2. This is a genuine comparison with the distinct
P91 full-witness presentation. -/
theorem KuuNativeF45Tree.DepthRotationRoute.SquareComparable.p91_rotationCount_eq
    (h : KuuNativeF45Tree.DepthRotationRoute.SquareComparable p u v) :
    u.rotationCount = v.rotationCount := by
  induction h with
  | refl route => rfl
  | symm h ih => exact ih.symm
  | trans h k ih ik => exact ih.trans ik
  | square left right =>
      change (2 : Nat) = 2
      rfl

/-- In contrast to P91, rotation count genuinely descends to P67's
old square-only F54 route quotient without collapsing pentagons. -/
def nativeF55P91P67SquareRouteToRotationCount
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55SquareRouteClasses first last → Nat :=
  _root_.Quotient.lift
    (fun route => route.rotationCount)
    (by
      intro u v h
      rcases h with ⟨w⟩
      exact w.p91_rotationCount_eq)

/-- Genuine P67 Type comparisons embed into full native original F55
Type evidence; thus P67 quotient canonically surjects onto P91. -/
def nativeF55P91P67ToFullWitnessRoute
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55SquareRouteClasses first last →
      NativeF55P91FullWitnessRouteClasses first last :=
  _root_.Quotient.lift
    (fun route => nativeF55P91FullWitnessRouteClass first last route)
    (by
      intro u v h
      rcases h with ⟨w⟩
      exact nativeF55P91FullWitnessRouteClass_eq_of_cell first last w.toPresentedCell)

/-- The P67-to-P91 comparison is surjective on all actual typed
F54 routes, not a claim of equality between two presentations. -/
theorem nativeF55P91P67ToFullWitnessRoute_surjective
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Function.Surjective (nativeF55P91P67ToFullWitnessRoute first last) := by
  intro q
  refine _root_.Quotient.inductionOn q (fun raw => ?_)
  exact ⟨nativeF55SquareRouteClass first last raw, rfl⟩

/-- P90's unfilled associator-naturality slot is equivalent EXACTLY
to equality of its two original F54 route classes in the new full
F55 witness quotient; no filler is asserted by this iff theorem. -/
theorem nativeF55P91AssocNaturalityFullWitnessClass_eq_iff

    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    nativeF55P91FullWitnessRouteClass
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter))
      (nativeF54P90AssocNaturalityLeftRoute u v w) =
    nativeF55P91FullWitnessRouteClass
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter))
      (nativeF54P90AssocNaturalityRightRoute u v w) ↔
      Nonempty (NativeF55P90AssocNaturalityCell u v w) := by
  exact nativeF55P91FullWitnessRouteClass_eq_iff _ _ _ _

/-- The ACTUAL C60 north pentagon is one explicit example of full
F55 route-class equality with raw F54 nonidentity and full genuine
pentagon charge +1. The true hexagon odd exchange phase remains
defined and nonzero in the unchanged original source. -/
theorem northNativeF55P91FullWitness_pentagon_equality_and_raw_nonidentity :
    nativeF55P91FullWitnessRouteClass _ _ northNativeF45PentagonLong =
      nativeF55P91FullWitnessRouteClass _ _ northNativeF45PentagonShort ∧
    northNativeF45PentagonLong ≠ northNativeF45PentagonShort ∧
    northNativeF55PentagonCell.nativeShadow.1.1 = (1 : Int) := by
  refine ⟨?_, northNativeF45PentagonLong_ne_short, rfl⟩
  exact nativeF55P91FullWitnessRouteClass_eq_of_cell _ _
    northNativeF55PentagonCell

#print axioms nativeF55P91FullWitnessRouteSetoid
#print axioms NativeF55P91FullWitnessRouteClasses
#print axioms nativeF55P91FullWitnessRouteClass_eq_iff
#print axioms nativeF55P91FullWitnessRouteClass_eq_of_cell
#print axioms nativeF55P91FullWitnessRoute_pentagon_class_eq
#print axioms nativeF55P91FullWitnessRoute_pentagon_notInjective
#print axioms nativeF55P91FullWitnessRoute_rotationCount_noDescent
#print axioms KuuNativeF45Tree.DepthRotationRoute.SquareComparable.p91_rotationCount_eq
#print axioms nativeF55P91P67SquareRouteToRotationCount
#print axioms nativeF55P91P67ToFullWitnessRoute
#print axioms nativeF55P91P67ToFullWitnessRoute_surjective
#print axioms nativeF55P91AssocNaturalityFullWitnessClass_eq_iff
#print axioms northNativeF55P91FullWitness_pentagon_equality_and_raw_nonidentity

end
end Kuu.F112.Physical
