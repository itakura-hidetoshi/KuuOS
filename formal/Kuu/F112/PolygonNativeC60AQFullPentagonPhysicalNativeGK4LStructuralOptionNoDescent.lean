import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4KOptionNatQuotientObserver
import Mathlib.Tactic

/-!
# F112-P94D3GK4L — genuine P92B Option Nat does NOT descend to structural quotient

GK4K defines an actual original-P92B quotient observer:
  some (raw original F54 primitive leaf count) at physical rotation zero,
  none at positive physical rotation. Every some value is strictly positive
and this precise Option Nat observation preserves the genuine original F54
composition using absorbing partial addition. It is NOT a category unit.

The canonical GK4E surjection pi : P92B classes -> Structural classes
forgets strictly more ORIGINAL Type-valued F54 evidence. We prove the
general necessary-and-sufficient factorization criterion for any codomain:
an observer descends through pi exactly when constant on each pi-fiber.

The original GK4D zero-rotation true unit tower at EVERY inhabited,
fully dependent original F45 tree t has
  L(tower(k)) = k + 1,
  GK4K(tower(k)) = some (k + 1),
  physical rotationCount(tower(k)) = 0.
Its P92B classes are distinct, and the true typed F54 leftUnit seam
identifies ALL tower stages in the independently extended Structural
comparison quotient. Hence one genuine structural class has an infinite
set of DIFFERENT GK4K numeric values in its original P92B preimage.
No map from the structural quotient to Option Nat can pull back along pi
to the existing GK4K observer. This conclusion applies to ALL possible
factor maps, not merely one proposed representative section.

In contrast, the coarser GK4G Boolean zero/positive grading DOES factor
through the structural quotient (already proved GK4G), showing exactly
which information the added structural unit seams discard. The true
C60 north-hexagon original F45 triple gives an unconditional instance.

Do not assert all functions fail to descend, prohibit alternative
original P92B compositions, decide original P92B associativity, identify
raw Type-valued proofs with existence quotients, or infer an old typed
P92B/F19/F28/F54/F55 equivalence. The true original 14D unconditional
Countable and old FJ assumption removal, real 19D filler, global
strict n, and hyperdescent remain unproved. No Gray or new axioms.

Lean v4.30.0-rc2 / pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Same-root, append-only, preserve 107 public roots, protect #1558
Draft/OPEN/unmerged. Copyright Hidetoshi Itakura / 板倉英俊.
Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uB

section UniversalDescentCriterion
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- For the REAL GK4E surjection of two distinct existence quotients,
a function on genuine P92B classes factors through structural classes
iff it is constant on every actual structural comparison fiber.
No assumption of faithfulness, bijectivity, or proof-type equality. -/
theorem nativeGK4L_factor_iff_fiber_constant
    {B : Type uB}
    (observe : NativeF55P92AssocRouteClasses first last → B) :
    (∃ lift : NativeGK4EStructuralRouteClasses first last → B,
      ∀ q : NativeF55P92AssocRouteClasses first last,
        lift (nativeGK4EP92ToStructural first last q) = observe q) ↔
    (∀ q r : NativeF55P92AssocRouteClasses first last,
      nativeGK4EP92ToStructural first last q =
        nativeGK4EP92ToStructural first last r →
      observe q = observe r) := by
  classical
  constructor
  · rintro ⟨lift, hlift⟩ q r hqr
    calc
      observe q = lift (nativeGK4EP92ToStructural first last q) := (hlift q).symm
      _ = lift (nativeGK4EP92ToStructural first last r) := congrArg lift hqr
      _ = observe r := hlift r
  · intro hfiber
    let select (v : NativeGK4EStructuralRouteClasses first last) :
        NativeF55P92AssocRouteClasses first last :=
      Classical.choose (nativeGK4EP92ToStructural_surjective first last v)
    refine ⟨fun v => observe (select v), ?_⟩
    intro q
    exact hfiber
      (select (nativeGK4EP92ToStructural first last q)) q
      (Classical.choose_spec
        (nativeGK4EP92ToStructural_surjective first last
          (nativeGK4EP92ToStructural first last q)))

/-- Boolean grade survives the structural comparison for every
genuine fully dependent original F45 source and target. -/
theorem nativeGK4L_bool_grade_factors
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4GP92Grade first last q =
      nativeGK4GStructuralGrade first last
        (nativeGK4EP92ToStructural first last q) := by
  exact nativeGK4G_grading_commutes first last q

end UniversalDescentCriterion

section AllStageObstruction
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- The ORIGINAL GK4D unit tower has strictly increasing GK4J
primitive route-leaf count. The base route is itself one original leaf,
not an empty syntax term. -/
theorem nativeGK4L_unitTower_leafCount (k : Nat) :
    (nativeGK4DUnitTower tree k).gk4jLeafCount = k + 1 := by
  induction k with
  | zero =>
      rfl
  | succ k ih =>
      change 1 + (nativeGK4DUnitTower tree k).gk4jLeafCount = (k + 1) + 1
      omega

/-- Real zero physical rotation and the GK4J positive count together
give the exact GK4K Option Nat value of every actual P92B tower class. -/
theorem nativeGK4L_unitTower_option (k : Nat) :
    nativeGK4KP92Option tree tree (nativeGK4ETowerClass tree k) =
      some (k + 1) := by
  change (if (nativeGK4DUnitTower tree k).rotationCount = 0
    then some (nativeGK4DUnitTower tree k).gk4jLeafCount else none) = some (k + 1)
  rw [nativeGK4GUnitTower_rotationCount tree k, nativeGK4L_unitTower_leafCount tree k]
  rfl

/-- Genuine tower P92B classes have different numeric Option values.
This is stronger than mere P92B class injectivity. -/
theorem nativeGK4L_unitTower_option_injective :
    Function.Injective (fun k : Nat =>
      nativeGK4KP92Option tree tree (nativeGK4ETowerClass tree k)) := by
  intro i j hij
  have h : (some (i + 1) : Option Nat) = some (j + 1) := by
    simpa only [nativeGK4L_unitTower_option] using hij
  injection h with hcount
  omega

/-- The same structural quotient class hides infinitely many distinct
GK4K numeric measurements on its actual original P92B preimage. -/
theorem nativeGK4L_option_injective_in_collapsed_fiber :
    Function.Injective (fun k : Nat =>
      nativeGK4KP92Option tree tree (nativeGK4ETowerFiber tree k).1) := by
  intro i j hij
  exact nativeGK4L_unitTower_option_injective tree hij

/-- Every strictly positive natural number occurs as a genuine
some-value of the original P92B quotient at ANY inhabited F45 stage;
some zero is excluded by GK4K. This is a complete characterization
of the numeric some-part, not a claim that none is always inhabited. -/
theorem nativeGK4L_some_iff_positive (k : Nat) :
    (∃ q : NativeF55P92AssocRouteClasses tree tree,
      nativeGK4KP92Option tree tree q = some k) ↔ 0 < k := by
  constructor
  · rintro ⟨q, hq⟩
    exact nativeGK4KP92Option_some_pos tree tree q k hq
  · intro hk
    cases k with
    | zero => omega
    | succ j =>
        exact ⟨nativeGK4ETowerClass tree j, nativeGK4L_unitTower_option tree j⟩

/-- All GK4D tower stages have equal STRUCTURAL images, while
their GK4K Option Nat observations are pairwise distinct. -/
theorem nativeGK4L_tower_collapse_but_option_separates
    (i j : Nat) (hij : i ≠ j) :
    nativeGK4EP92ToStructural tree tree (nativeGK4ETowerClass tree i) =
        nativeGK4EP92ToStructural tree tree (nativeGK4ETowerClass tree j) ∧
    nativeGK4KP92Option tree tree (nativeGK4ETowerClass tree i) ≠
        nativeGK4KP92Option tree tree (nativeGK4ETowerClass tree j) := by
  refine ⟨nativeGK4ETowerClass_collapse tree i j, ?_⟩
  intro heq
  exact hij (nativeGK4L_unitTower_option_injective tree heq)

/-- The concrete obstruction to GK4K descent: a SINGLE canonical
structural fiber has two classes with unequal Option Nat values.
Unlike GK4G Bool grade, GK4K does not respect the newly adjoined
true F54 structural unit seam. -/
theorem nativeGK4L_option_not_fiber_constant :
    ¬ (∀ q r : NativeF55P92AssocRouteClasses tree tree,
      nativeGK4EP92ToStructural tree tree q =
        nativeGK4EP92ToStructural tree tree r →
      nativeGK4KP92Option tree tree q = nativeGK4KP92Option tree tree r) := by
  intro hc
  have h := hc (nativeGK4ETowerClass tree 0) (nativeGK4ETowerClass tree 1)
    (nativeGK4ETowerClass_collapse tree 0 1)
  exact Nat.zero_ne_one (nativeGK4L_unitTower_option_injective tree h)

/-- NO observer on the genuine structural comparison quotient can
recover the existing GK4K Option Nat P92B observer by pullback along
the canonical SURJECTIVE GK4E comparison. ALL factor maps are ruled out,
not just a chosen section. -/
theorem nativeGK4L_no_option_descent :
    ¬ ∃ lift : NativeGK4EStructuralRouteClasses tree tree → Option Nat,
      ∀ q : NativeF55P92AssocRouteClasses tree tree,
        lift (nativeGK4EP92ToStructural tree tree q) =
          nativeGK4KP92Option tree tree q := by
  intro hfactor
  exact nativeGK4L_option_not_fiber_constant tree
    ((nativeGK4L_factor_iff_fiber_constant tree tree
      (nativeGK4KP92Option tree tree)).mp hfactor)

/-- Equivalently there is NO observer at the structural quotient
that reproduces the true ORIGINAL raw F54 GK4K measurement on all
genuine original raw route representatives. -/
theorem nativeGK4L_no_raw_structural_option :
    ¬ ∃ lift : NativeGK4EStructuralRouteClasses tree tree → Option Nat,
      ∀ r : KuuNativeF45Tree.DepthRotationRoute p tree tree,
        lift (nativeGK4EStructuralRouteClass tree tree r) =
          nativeGK4KRawOption tree tree r := by
  rintro ⟨lift, hlift⟩
  apply nativeGK4L_no_option_descent tree
  refine ⟨lift, ?_⟩
  intro q
  refine _root_.Quotient.inductionOn q ?_
  intro r
  simpa only [nativeGK4EP92ToStructural_class, nativeGK4KP92Option_class]
    using hlift r

/-- Exact contrast: TRUE Boolean physical-rotation grade factors
through the structural quotient, but the strictly finer GK4K Option
Nat observer cannot, at the SAME original fully typed F45 stage. -/
theorem nativeGK4L_bool_yes_option_no :
    (∀ q : NativeF55P92AssocRouteClasses tree tree,
      nativeGK4GP92Grade tree tree q =
        nativeGK4GStructuralGrade tree tree
          (nativeGK4EP92ToStructural tree tree q)) ∧
    (¬ ∃ lift : NativeGK4EStructuralRouteClasses tree tree → Option Nat,
      ∀ q : NativeF55P92AssocRouteClasses tree tree,
        lift (nativeGK4EP92ToStructural tree tree q) =
          nativeGK4KP92Option tree tree q) := by
  exact ⟨nativeGK4L_bool_grade_factors tree tree,
    nativeGK4L_no_option_descent tree⟩

end AllStageObstruction

section PhysicalNorth
/-- On the ACTUAL original C60 north hexagon fully dependent F45
tree, the Option Nat observer provably cannot factor through the
independent structural quotient. No countability assumptions. -/
theorem nativeGK4L_physical_north_no_option_descent :
    ¬ ∃ lift : NativeGK4EStructuralRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple → Option Nat,
      ∀ q : NativeF55P92AssocRouteClasses
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
        lift (nativeGK4EP92ToStructural
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q) =
        nativeGK4KP92Option
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q :=
  nativeGK4L_no_option_descent nativeGK4FPhysicalNorthTriple
end PhysicalNorth

#print axioms nativeGK4L_factor_iff_fiber_constant
#print axioms nativeGK4L_bool_grade_factors
#print axioms nativeGK4L_unitTower_leafCount
#print axioms nativeGK4L_unitTower_option
#print axioms nativeGK4L_unitTower_option_injective
#print axioms nativeGK4L_option_injective_in_collapsed_fiber
#print axioms nativeGK4L_some_iff_positive
#print axioms nativeGK4L_tower_collapse_but_option_separates
#print axioms nativeGK4L_option_not_fiber_constant
#print axioms nativeGK4L_no_option_descent
#print axioms nativeGK4L_no_raw_structural_option
#print axioms nativeGK4L_bool_yes_option_no
#print axioms nativeGK4L_physical_north_no_option_descent

end
end Kuu.F112.Physical
