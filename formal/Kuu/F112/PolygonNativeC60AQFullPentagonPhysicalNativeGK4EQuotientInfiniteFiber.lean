import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4DInfiniteUnitTower
import Kuu.F112.PolygonNativeF55P94DK5ReorientedTypedNineCycle

/-!
# F112-P94D3GK4E — actual P92B quotient and an infinite collapse fiber

Reuse the EXISTING nativeF55P92AssocRouteSetoid/Classes, whose relation
is existence of the original fully typed P92B comparison. Separately
form a quotient by existence of the original extended
NativeF55StructuralComparison, using its actual reverse operation.
Neither quotient is identified with raw Type-valued evidence.

The original P92B inclusion induces a canonical SURJECTION between
these quotients on identical fully typed F45/F54 boundaries. GK4D's
unit tower gives infinitely many DISTINCT P92B classes, ALL with the
same image in the structural-comparison quotient. Under explicit
Countable D/E objects and every Hom fiber, both the entire P92B
self-route quotient and this ONE collapse fiber have cardinal aleph0.
The north C60 hexagon specialization has no extra Countable premise.

We do NOT assert that the entire target quotient is a singleton,
that structural seam alone contains P92B, or that either quotient
recovers original proof histories. No higher filler, historical full
typed equivalence, true 14D Countable, or old FJ assumption removal.
Append-only; 107 public roots, no Gray, no new axioms or proof holes.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section Boundary
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- A DISTINCT relation: existence of actual extended structural
comparison evidence, not equality of raw proofs or seam-only evidence. -/
def nativeGK4EStructuralRouteSetoid :
    Setoid (KuuNativeF45Tree.DepthRotationRoute p first last) where
  r := fun r s => Nonempty (NativeF55StructuralComparison p r s)
  iseqv := ⟨
    (fun r => ⟨.original (.refl r)⟩),
    (fun h => h.elim (fun w => ⟨w.reverse⟩)),
    (fun h k => h.elim (fun w => k.elim (fun v => ⟨.trans w v⟩)))⟩

abbrev NativeGK4EStructuralRouteClasses :=
  _root_.Quotient (nativeGK4EStructuralRouteSetoid first last)

/-- Keep the quotient projection explicit rather than coercing raw
F54 routes or Type-valued witnesses to an observational shadow. -/
def nativeGK4EStructuralRouteClass
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeGK4EStructuralRouteClasses first last :=
  _root_.Quotient.mk _ r

/-- The new quotient equality means precisely actual extended
Type-valued comparison existence at the original boundaries. -/
theorem nativeGK4EStructuralRouteClass_eq_iff
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4EStructuralRouteClass first last r =
      nativeGK4EStructuralRouteClass first last s ↔
      Nonempty (NativeF55StructuralComparison p r s) := by
  constructor
  · intro h
    exact _root_.Quotient.exact h
  · intro h
    exact _root_.Quotient.sound h

/-- The ORIGINAL P92B inclusion makes this quotient map well defined.
It does not make a map back to raw original P92B witnesses. -/
def nativeGK4EP92ToStructural :
    NativeF55P92AssocRouteClasses first last →
      NativeGK4EStructuralRouteClasses first last :=
  _root_.Quotient.lift (nativeGK4EStructuralRouteClass first last)
    (fun _ _ h => h.elim (fun cell =>
      _root_.Quotient.sound ⟨NativeF55StructuralComparison.original cell⟩))

/-- The comparison is over the SAME actual original route representative. -/
theorem nativeGK4EP92ToStructural_class
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4EP92ToStructural first last
        (nativeF55P92AssocRouteClass first last r) =
      nativeGK4EStructuralRouteClass first last r := by
  rfl

/-- Every structural class has an original F54 representative, hence
is the image of its P92B class; no representative is invented. -/
theorem nativeGK4EP92ToStructural_surjective :
    Function.Surjective (nativeGK4EP92ToStructural first last) := by
  intro q
  refine _root_.Quotient.inductionOn q ?_
  intro r
  exact ⟨nativeF55P92AssocRouteClass first last r, rfl⟩

/-- Quotient upper bound inherited from GI's FULL dependent raw-route
countability, with all generic object/Hom premises explicitly retained. -/
theorem nativeGK4EP92Classes_countable
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeF55P92AssocRouteClasses first last) := by
  letI : Countable (KuuNativeF45Tree.DepthRotationRoute p first last) :=
    nativeGIOriginalDepthFiber_countable hobjD hhomD hobjE hhomE first last
  infer_instance

end Boundary

section Tower
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- The GK4D tower projected into the EXISTING original P92B quotient. -/
def nativeGK4ETowerClass (k : Nat) :
    NativeF55P92AssocRouteClasses tree tree :=
  nativeF55P92AssocRouteClass tree tree (nativeGK4DUnitTower tree k)

/-- Distinct raw tower stages remain distinct AFTER taking the
actual P92B witness-existence quotient, not merely before quotienting. -/
theorem nativeGK4ETowerClass_injective :
    Function.Injective (nativeGK4ETowerClass tree) := by
  intro i j hij
  by_contra hne
  apply nativeGK4DUnitTower_no_P92B tree hne
  exact (nativeF55P92AssocRouteClass_eq_iff tree tree
    (nativeGK4DUnitTower tree i) (nativeGK4DUnitTower tree j)).mp hij

/-- All these pairwise distinct P92B classes land in ONE structural
class, because GK4D supplies actual Type-valued structural comparisons. -/
theorem nativeGK4ETowerClass_collapse (i j : Nat) :
    nativeGK4EP92ToStructural tree tree (nativeGK4ETowerClass tree i) =
      nativeGK4EP92ToStructural tree tree (nativeGK4ETowerClass tree j) := by
  change nativeGK4EStructuralRouteClass tree tree (nativeGK4DUnitTower tree i) =
    nativeGK4EStructuralRouteClass tree tree (nativeGK4DUnitTower tree j)
  exact _root_.Quotient.sound (nativeGK4DUnitTower_structural_exists tree i j)

/-- Surjectivity does NOT imply faithful comparison of the quotients. -/
theorem nativeGK4EP92ToStructural_not_injective :
    ¬ Function.Injective (nativeGK4EP92ToStructural tree tree) := by
  intro hinj
  have h := hinj (nativeGK4ETowerClass_collapse tree 0 1)
  exact Nat.zero_ne_one (nativeGK4ETowerClass_injective tree h)

/-- ONE specified fiber of the canonical quotient surjection.
This is a subtype of P92B CLASSES, not a subtype of raw F54 routes. -/
abbrev NativeGK4ECollapsedFiber :=
  {q : NativeF55P92AssocRouteClasses tree tree //
    nativeGK4EP92ToStructural tree tree q =
      nativeGK4EP92ToStructural tree tree (nativeGK4ETowerClass tree 0)}

/-- Explicit witnesses in the selected fiber for every natural number. -/
def nativeGK4ETowerFiber (k : Nat) : NativeGK4ECollapsedFiber tree :=
  ⟨nativeGK4ETowerClass tree k, nativeGK4ETowerClass_collapse tree k 0⟩

/-- The collapse fiber contains infinitely many distinct P92B classes. -/
theorem nativeGK4ETowerFiber_injective :
    Function.Injective (nativeGK4ETowerFiber tree) := by
  intro i j hij
  apply nativeGK4ETowerClass_injective tree
  exact congrArg (fun q : NativeGK4ECollapsedFiber tree => q.1) hij

/-- Exact aleph-null cardinality of the ENTIRE existing P92B
self-route quotient under explicit generic countability assumptions. -/
theorem nativeGK4EP92Classes_aleph0
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Cardinal.mk (NativeF55P92AssocRouteClasses tree tree) = Cardinal.aleph0 := by
  letI : Countable (NativeF55P92AssocRouteClasses tree tree) :=
    nativeGK4EP92Classes_countable tree tree hobjD hhomD hobjE hhomE
  letI : Infinite (NativeF55P92AssocRouteClasses tree tree) :=
    Infinite.of_injective (nativeGK4ETowerClass tree)
      (nativeGK4ETowerClass_injective tree)
  exact Cardinal.mk_eq_aleph0 _

/-- Stronger than mere noninjectivity: a specified canonical-surjection
fiber has exactly aleph-null distinct ORIGINAL P92B equivalence classes. -/
theorem nativeGK4ECollapsedFiber_aleph0
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Cardinal.mk (NativeGK4ECollapsedFiber tree) = Cardinal.aleph0 := by
  letI : Countable (NativeF55P92AssocRouteClasses tree tree) :=
    nativeGK4EP92Classes_countable tree tree hobjD hhomD hobjE hhomE
  letI : Countable (NativeGK4ECollapsedFiber tree) := inferInstance
  letI : Infinite (NativeGK4ECollapsedFiber tree) :=
    Infinite.of_injective (nativeGK4ETowerFiber tree)
      (nativeGK4ETowerFiber_injective tree)
  exact Cardinal.mk_eq_aleph0 _

end Tower

/-! ### Original Site x Site C60 specialization; no extra hypotheses. -/

/-- The genuine physical north-hexagon P92B quotient is countably infinite. -/
theorem nativeGK4E_physical_north_P92Classes_aleph0 :
    Cardinal.mk (NativeF55P92AssocRouteClasses
      (northHexagonNativeUnit 0) (northHexagonNativeUnit 0)) = Cardinal.aleph0 :=
  nativeGK4EP92Classes_aleph0 (northHexagonNativeUnit 0)
    nativeC60GEPhysicalSite_countable nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable nativeC60GEPhysicalIncidenceHom_countable

/-- A single actual structural-comparison class receives aleph-null
many distinct physical original P92B classes under the canonical map. -/
theorem nativeGK4E_physical_north_collapsedFiber_aleph0 :
    Cardinal.mk (NativeGK4ECollapsedFiber (northHexagonNativeUnit 0)) =
      Cardinal.aleph0 :=
  nativeGK4ECollapsedFiber_aleph0 (northHexagonNativeUnit 0)
    nativeC60GEPhysicalSite_countable nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable nativeC60GEPhysicalIncidenceHom_countable

/-- The physical map is a surjection but not an injection; it is NOT
an equivalence of the two selected presentations over raw representatives. -/
theorem nativeGK4E_physical_north_surjective_not_injective :
    Function.Surjective (nativeGK4EP92ToStructural
      (northHexagonNativeUnit 0) (northHexagonNativeUnit 0)) ∧
    ¬ Function.Injective (nativeGK4EP92ToStructural
      (northHexagonNativeUnit 0) (northHexagonNativeUnit 0)) :=
  ⟨nativeGK4EP92ToStructural_surjective _ _,
    nativeGK4EP92ToStructural_not_injective (northHexagonNativeUnit 0)⟩

#print axioms nativeGK4EStructuralRouteSetoid
#print axioms nativeGK4EStructuralRouteClass
#print axioms nativeGK4EStructuralRouteClass_eq_iff
#print axioms nativeGK4EP92ToStructural
#print axioms nativeGK4EP92ToStructural_class
#print axioms nativeGK4EP92ToStructural_surjective
#print axioms nativeGK4EP92Classes_countable
#print axioms nativeGK4ETowerClass
#print axioms nativeGK4ETowerClass_injective
#print axioms nativeGK4ETowerClass_collapse
#print axioms nativeGK4EP92ToStructural_not_injective
#print axioms nativeGK4ETowerFiber
#print axioms nativeGK4ETowerFiber_injective
#print axioms nativeGK4EP92Classes_aleph0
#print axioms nativeGK4ECollapsedFiber_aleph0
#print axioms nativeGK4E_physical_north_P92Classes_aleph0
#print axioms nativeGK4E_physical_north_collapsedFiber_aleph0
#print axioms nativeGK4E_physical_north_surjective_not_injective

end
end Kuu.F112.Physical
