import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4FTwoInfiniteQuotientFibers

/-!
# F112-P94D3GK4G — canonical two-valued descent of real F54 zero/positive rotation

The original *fully typed* F54 route carries a genuine primitive local-
rotation count. GK4F proved that its ZERO-versus-POSITIVE distinction is
respected by every original F55 generator, every independently adjoined
P92B generator, and every constructor of the additional F54 structural
comparison. We descend this invariant to EACH OF THE TWO ACTUAL quotient
presentations over the SAME original D/E, Blocks, F45, double-Nat and
F54 source/target boundary. The two quotient gradings COMMUTE with the
canonical surjective-but-nonfaithful GK4E comparison.

The descent is unique given its values on all raw original route classes.
When an ACTUAL original LocalRotation exists, we construct explicit
Bool-indexed sections of BOTH graded quotient maps using an original
zero-edge unit and a forward/backward 2-edge physical backtrack. These
sections are compatible with the original-P92B-to-structural quotient
map, giving a constructive split epimorphism to Bool, not a false
identification of the full structural quotient with Bool.

More strongly, the two Bool grade fibers of the ORIGINAL P92B route
quotient each have exact cardinality aleph-null: actual zero-edge unit
towers in one grade and genuine 2-rotation backtrack towers in the
other, with the original GK4C unit-atom invariant proving injectivity.
GI's entire dependent original route-fiber countability supplies the
upper bound under explicit Countable D/E objects AND every Hom fiber.
The true north C60 hexagon original Site x Site triple specializes all
claims unconditionally, preserving the actual categorical source.

Does NOT classify all structural equivalence classes, assert only two
classes exist, prove historical P92B/F19/F28/F54/F55 equivalence,
true 14D Countable, old FJ 14D assumption removal, original 19D
filler, global strict n, or higher hyperdescent.
No quotient is treated as a raw Type-valued proof; no Gray or new axiom.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root, 107 public roots, protected PR #1558 unchanged.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

/-- The truth value of ZERO original F54 primitive local rotations is
unchanged under any genuine original comparison preserving zero. -/
private theorem nativeGK4G_decide_zero_congr (a b : Nat)
    (h : (a = 0 ↔ b = 0)) :
    decide (a = 0) = decide (b = 0) := by
  by_cases ha : a = 0
  · have hb : b = 0 := h.mp ha
    simp [ha, hb]
  · have hb : b ≠ 0 := fun hb => ha (h.mpr hb)
    simp [ha, hb]

section Boundary

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Raw evidence-level *Boolean measurement*, not a 3-cell itself.
true = zero primitive F54 rotations; false = at least one. -/
def nativeGK4GRawGrade
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : Bool :=
  decide (route.rotationCount = 0)

/-- The graded observation DESCENDS through the genuine Structural-
Comparison existence quotient because all three original proof
constructors preserve zero vs positive (GK4F). -/
def nativeGK4GStructuralGrade :
    NativeGK4EStructuralRouteClasses first last → Bool :=
  _root_.Quotient.lift (nativeGK4GRawGrade first last)
    (fun r s h => h.elim (fun cell =>
      nativeGK4G_decide_zero_congr _ _
        (nativeGK4FStructural_zero_rotation_iff cell)))

/-- The independent original P92B existence quotient also admits
the same descent, using all nine original P92B constructors. -/
def nativeGK4GP92Grade :
    NativeF55P92AssocRouteClasses first last → Bool :=
  _root_.Quotient.lift (nativeGK4GRawGrade first last)
    (fun r s h => h.elim (fun cell =>
      nativeGK4G_decide_zero_congr _ _
        (nativeGK4FP92B_zero_rotation_iff cell)))

theorem nativeGK4GStructuralGrade_class
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4GStructuralGrade first last
      (nativeGK4EStructuralRouteClass first last route) =
        nativeGK4GRawGrade first last route := by
  rfl

theorem nativeGK4GP92Grade_class
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4GP92Grade first last
      (nativeF55P92AssocRouteClass first last route) =
        nativeGK4GRawGrade first last route := by
  rfl

/-- Actual commutative quotient square: original P92B class -> extended
structural class -> Bool equals P92B class -> Bool on EVERY element.
Surjectivity does not give a missing Type-valued return map. -/
theorem nativeGK4G_grading_commutes
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4GP92Grade first last q =
      nativeGK4GStructuralGrade first last
        (nativeGK4EP92ToStructural first last q) := by
  refine _root_.Quotient.inductionOn q ?_
  intro route
  rfl

/-- Uniqueness: any other Boolean observer on the structural quotient
agreeing with the raw zero-count predicate on every original F54
representative is exactly the grade defined above. -/
theorem nativeGK4GStructuralGrade_unique
    (observer : NativeGK4EStructuralRouteClasses first last → Bool)
    (hsound : ∀ route : KuuNativeF45Tree.DepthRotationRoute p first last,
      observer (nativeGK4EStructuralRouteClass first last route) =
        nativeGK4GRawGrade first last route) :
    observer = nativeGK4GStructuralGrade first last := by
  funext q
  refine _root_.Quotient.inductionOn q ?_
  intro route
  simpa only [nativeGK4GStructuralGrade_class] using hsound route

/-- The structural quotient, even if not a finite two-point type,
is at least countable whenever the actual original D/E objects and
every categorical Hom fiber are countable. -/
theorem nativeGK4GStructuralClasses_countable
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK4EStructuralRouteClasses first last) := by
  letI : Countable (KuuNativeF45Tree.DepthRotationRoute p first last) :=
    nativeGIOriginalDepthFiber_countable
      hobjD hhomD hobjE hhomE first last
  infer_instance

/-- Actual original P92B equivalence classes of a selected Boolean
grade, NOT raw route evidence or structural classes. -/
abbrev NativeGK4GP92GradeFiber (grade : Bool) :=
  {q : NativeF55P92AssocRouteClasses first last //
    nativeGK4GP92Grade first last q = grade}

/-- The two grade fibers inherit the strict GI original-fiber
countability bound (all D/E object and Hom assumptions explicit). -/
theorem nativeGK4GP92GradeFiber_countable
    (grade : Bool)
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK4GP92GradeFiber first last grade) := by
  letI : Countable (NativeF55P92AssocRouteClasses first last) :=
    nativeGK4EP92Classes_countable
      first last hobjD hhomD hobjE hhomE
  infer_instance

end Boundary

section Tower
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

/-- All original F54 unit-tower stages contain ZERO primitive
local rotations, even though their ZERO-EDGE atom count grows. -/
theorem nativeGK4GUnitTower_rotationCount
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (k : Nat) :
    (nativeGK4DUnitTower tree k).rotationCount = 0 := by
  induction k with
  | zero => rfl
  | succ k ih =>
      change 0 + (nativeGK4DUnitTower tree k).rotationCount = 0
      omega

/-- Every genuine original zero-unit tower class has Bool grade true. -/
theorem nativeGK4GZeroTower_grade
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (k : Nat) :
    nativeGK4GP92Grade tree tree (nativeGK4ETowerClass tree k) = true := by
  change decide ((nativeGK4DUnitTower tree k).rotationCount = 0) = true
  rw [nativeGK4GUnitTower_rotationCount]
  decide

/-- An injective ℕ-family of P92B classes in the true (zero-rotation)
Boolean grade fiber. This uses the unchanged original GK4D tower. -/
def nativeGK4GZeroGradeTowerFiber
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (k : Nat) :
    NativeGK4GP92GradeFiber tree tree true :=
  ⟨nativeGK4ETowerClass tree k, nativeGK4GZeroTower_grade tree k⟩

theorem nativeGK4GZeroGradeTowerFiber_injective
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    Function.Injective (nativeGK4GZeroGradeTowerFiber tree) := by
  intro i j hij
  apply nativeGK4ETowerClass_injective tree
  exact congrArg
    (fun q : NativeGK4GP92GradeFiber tree tree true => q.1) hij

end Tower

section RealRotation
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}

/-- The genuine two-edge forward/backward F54 loop plus ANY number of
zero-edge units still has exactly TWO primitive rotation edges. -/
theorem nativeGK4GPositiveTower_rotationCount
    (rot : KuuNativeF45Tree.LocalRotation p before after)
    (k : Nat) :
    (nativeGK4FPositiveTower rot k).rotationCount = 2 := by
  change (nativeGK4FBacktrack rot).rotationCount +
    (nativeGK4DUnitTower before k).rotationCount = 2
  rw [nativeGK4FBacktrack_rotationCount,
    nativeGK4GUnitTower_rotationCount]
  omega

/-- An explicit SECTION of the structural quotient's Bool grade.
false witnesses a genuine original 2-edge backtrack; true witnesses
the original zero-edge unit route. These are different quotient
classes (GK4F); no assertion that they exhaust the quotient. -/
def nativeGK4GStructuralSection
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    Bool → NativeGK4EStructuralRouteClasses before before
  | false => nativeGK4EStructuralRouteClass before before
      (nativeGK4FBacktrack rot)
  | true => nativeGK4EStructuralRouteClass before before
      (nativeGK4DUnitTower before 0)

/-- The same two true raw representatives select a section of the
ORIGINAL P92B quotient Bool grade. -/
def nativeGK4GP92Section
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    Bool → NativeF55P92AssocRouteClasses before before
  | false => nativeF55P92AssocRouteClass before before
      (nativeGK4FBacktrack rot)
  | true => nativeGK4ETowerClass before 0

/-- Explicit split surjection of the real structural quotient onto
Bool, conditional ONLY on an actual typed original LocalRotation. -/
theorem nativeGK4GStructuralSection_rightInverse
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    Function.RightInverse (nativeGK4GStructuralGrade before before)
      (nativeGK4GStructuralSection rot) := by
  intro grade
  cases grade <;> rfl

/-- The original P92B Boolean grade also splits onto two genuinely
represented truth values, without inventing a strict 3-cell. -/
theorem nativeGK4GP92Section_rightInverse
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    Function.RightInverse (nativeGK4GP92Grade before before)
      (nativeGK4GP92Section rot) := by
  intro grade
  cases grade <;> rfl

/-- The two chosen sections commute with the canonical GK4E quotient
surjection. This is a representation-compatible *split grading*,
not an inverse for the nonfaithful comparison itself. -/
theorem nativeGK4GSections_compatible
    (rot : KuuNativeF45Tree.LocalRotation p before after)
    (grade : Bool) :
    nativeGK4EP92ToStructural before before
      (nativeGK4GP92Section rot grade) =
        nativeGK4GStructuralSection rot grade := by
  cases grade <;> rfl

theorem nativeGK4GStructuralGrade_surjective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    Function.Surjective (nativeGK4GStructuralGrade before before) := by
  intro grade
  exact ⟨nativeGK4GStructuralSection rot grade,
    nativeGK4GStructuralSection_rightInverse rot grade⟩

theorem nativeGK4GP92Grade_surjective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    Function.Surjective (nativeGK4GP92Grade before before) := by
  intro grade
  exact ⟨nativeGK4GP92Section rot grade,
    nativeGK4GP92Section_rightInverse rot grade⟩

/-- Positive-loop unit-tower classes have grade FALSE in the actual
original P92B comparison quotient. -/
theorem nativeGK4GPositiveTower_grade
    (rot : KuuNativeF45Tree.LocalRotation p before after)
    (k : Nat) :
    nativeGK4GP92Grade before before
      (nativeF55P92AssocRouteClass before before
        (nativeGK4FPositiveTower rot k)) = false := by
  change decide ((nativeGK4FPositiveTower rot k).rotationCount = 0) = false
  rw [nativeGK4GPositiveTower_rotationCount]
  decide

/-- A genuine full F54 2-rotation proof tower in the *positive*
Boolean grade fiber of the ORIGINAL P92B quotient. -/
def nativeGK4GPositiveGradeTowerFiber
    (rot : KuuNativeF45Tree.LocalRotation p before after)
    (k : Nat) :
    NativeGK4GP92GradeFiber before before false :=
  ⟨nativeF55P92AssocRouteClass before before
      (nativeGK4FPositiveTower rot k),
    nativeGK4GPositiveTower_grade rot k⟩

/-- Full original GK4C unit-count soundness proves that all positive
graded tower classes are PAIRWISE distinct; Bool grading alone does
not falsely identify different original P92B certificates. -/
theorem nativeGK4GPositiveGradeTowerFiber_injective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    Function.Injective (nativeGK4GPositiveGradeTowerFiber rot) := by
  intro i j hij
  have hclasses := congrArg
    (fun q : NativeGK4GP92GradeFiber before before false => q.1) hij
  have hex := (nativeF55P92AssocRouteClass_eq_iff before before
    (nativeGK4FPositiveTower rot i)
    (nativeGK4FPositiveTower rot j)).mp hclasses
  rcases hex with ⟨cell⟩
  have hcount := nativeGK4C_P92B_unitCount_sound cell
  rw [nativeGK4FPositiveTower_unitCount,
    nativeGK4FPositiveTower_unitCount] at hcount
  omega

/-- Both Boolean grades of the ENTIRE original P92B self-route quotient
have exact cardinal aleph-null, not merely the previously selected
single structural-collapse fiber in each grade. The GENERIC D/E
object and each Hom-fiber Countable hypotheses are all explicit.
Proof uses the actual two original, independently typed towers. -/
theorem nativeGK4GP92Grade_twoFibers_aleph0
    (rot : KuuNativeF45Tree.LocalRotation p before after)
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Cardinal.mk (NativeGK4GP92GradeFiber before before true) =
      Cardinal.aleph0 ∧
    Cardinal.mk (NativeGK4GP92GradeFiber before before false) =
      Cardinal.aleph0 := by
  letI : Countable (NativeF55P92AssocRouteClasses before before) :=
    nativeGK4EP92Classes_countable before before
      hobjD hhomD hobjE hhomE
  constructor
  · letI : Countable (NativeGK4GP92GradeFiber before before true) :=
      inferInstance
    letI : Infinite (NativeGK4GP92GradeFiber before before true) :=
      Infinite.of_injective (nativeGK4GZeroGradeTowerFiber before)
        (nativeGK4GZeroGradeTowerFiber_injective before)
    exact Cardinal.mk_eq_aleph0 _
  · letI : Countable (NativeGK4GP92GradeFiber before before false) :=
      inferInstance
    letI : Infinite (NativeGK4GP92GradeFiber before before false) :=
      Infinite.of_injective (nativeGK4GPositiveGradeTowerFiber rot)
        (nativeGK4GPositiveGradeTowerFiber_injective rot)
    exact Cardinal.mk_eq_aleph0 _

end RealRotation

/-! ### Fully physical true C60 north-hexagon, independent Site x Site. -/

/-- The two quotient gradings are compatibly and explicitly split
onto Bool by the ACTUAL north C60 triple F54 associator rotation. -/
theorem nativeGK4G_physical_north_split_grading :
    Function.RightInverse
      (nativeGK4GStructuralGrade
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple)
      (nativeGK4GStructuralSection northHexagonNativeLeftRotation) ∧
    Function.RightInverse
      (nativeGK4GP92Grade
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple)
      (nativeGK4GP92Section northHexagonNativeLeftRotation) :=
  ⟨nativeGK4GStructuralSection_rightInverse northHexagonNativeLeftRotation,
    nativeGK4GP92Section_rightInverse northHexagonNativeLeftRotation⟩

/-- Actual physical C60 P92B equivalence classes have precisely
aleph-null elements in BOTH zero and positive raw-rotation grades.
This is stronger than two specified structural fibers: each grade
fiber covers ALL structural quotient classes of that grade. -/
theorem nativeGK4G_physical_north_two_full_grade_fibers_aleph0 :
    Cardinal.mk (NativeGK4GP92GradeFiber nativeGK4FPhysicalNorthTriple
      nativeGK4FPhysicalNorthTriple true) = Cardinal.aleph0 ∧
    Cardinal.mk (NativeGK4GP92GradeFiber nativeGK4FPhysicalNorthTriple
      nativeGK4FPhysicalNorthTriple false) = Cardinal.aleph0 :=
  nativeGK4GP92Grade_twoFibers_aleph0
    northHexagonNativeLeftRotation
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

/-- No false finite/2-element conclusion: the actual physical C60
structural quotient is Countable, and the explicit grading is
surjective onto Bool. Its exact total cardinality remains open. -/
theorem nativeGK4G_physical_north_structural_countable_and_graded :
    Countable (NativeGK4EStructuralRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) ∧
    Function.Surjective (nativeGK4GStructuralGrade
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  constructor
  · exact nativeGK4GStructuralClasses_countable
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
      nativeC60GEPhysicalSite_countable
      nativeC60GEPhysicalIncidenceHom_countable
      nativeC60GEPhysicalSite_countable
      nativeC60GEPhysicalIncidenceHom_countable
  · exact nativeGK4GStructuralGrade_surjective
      northHexagonNativeLeftRotation

#print axioms nativeGK4GRawGrade
#print axioms nativeGK4GStructuralGrade
#print axioms nativeGK4GP92Grade
#print axioms nativeGK4GStructuralGrade_class
#print axioms nativeGK4GP92Grade_class
#print axioms nativeGK4G_grading_commutes
#print axioms nativeGK4GStructuralGrade_unique
#print axioms nativeGK4GStructuralClasses_countable
#print axioms nativeGK4GP92GradeFiber_countable
#print axioms nativeGK4GUnitTower_rotationCount
#print axioms nativeGK4GZeroTower_grade
#print axioms nativeGK4GZeroGradeTowerFiber
#print axioms nativeGK4GZeroGradeTowerFiber_injective
#print axioms nativeGK4GPositiveTower_rotationCount
#print axioms nativeGK4GStructuralSection
#print axioms nativeGK4GP92Section
#print axioms nativeGK4GStructuralSection_rightInverse
#print axioms nativeGK4GP92Section_rightInverse
#print axioms nativeGK4GSections_compatible
#print axioms nativeGK4GStructuralGrade_surjective
#print axioms nativeGK4GP92Grade_surjective
#print axioms nativeGK4GPositiveTower_grade
#print axioms nativeGK4GPositiveGradeTowerFiber
#print axioms nativeGK4GPositiveGradeTowerFiber_injective
#print axioms nativeGK4GP92Grade_twoFibers_aleph0
#print axioms nativeGK4G_physical_north_split_grading
#print axioms nativeGK4G_physical_north_two_full_grade_fibers_aleph0
#print axioms nativeGK4G_physical_north_structural_countable_and_graded

end
end Kuu.F112.Physical
