import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4CP92UnitCountObstruction

/-!
# F112-P94D3GK4D — infinite genuine unit towers and presentation separation

GK4C proves that original P92B nine-constructor Type-valued
presentation preserves the NUMBER of original F54 zero-edge
RotationChain.refl atoms, including the new assocNaturality generator.
The independent F54 structural presentation explicitly adds units.

Given ANY fully typed original F45 tree, we construct an infinite tower
of distinct original F54 routes with identical genuine F45 endpoints,
by repeatedly composing a true zero-edge reflexivity route. Every
tower stage is connected to every other stage by ORIGINAL Type-valued
F54 structural seam proofs, and thus by independent StructuralComparison
witnesses. In contrast, distinct tower stages admit NO original P92B
comparison. The finite genuine C60 north-hexagon specialization uses
an actual original Site×Site F45 stage, not a cardinality argument.

No quotient, chosen shadow, extra 3-cell axiom, or Gray. No sorry/admit.
Lean v4.30.0-rc2; pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, 107 public roots and protected PR #1558 untouched.
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

section Tower

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

/-- Full raw F54 unit tower at ONE original F45 stage: depth zero
has one true unit atom, each successor includes another such atom. -/
def nativeGK4DUnitTower
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    Nat → KuuNativeF45Tree.DepthRotationRoute p tree tree
  | 0 => .chain (.refl tree)
  | k + 1 => .trans (.chain (.refl tree)) (nativeGK4DUnitTower tree k)

/-- Count the complete genuine original zero-edge unit occurrences. -/
theorem nativeGK4DUnitTower_count
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (k : Nat) :
    (nativeGK4DUnitTower tree k).gk4cUnitCount = k + 1 := by
  induction k with
  | zero => rfl
  | succ k ih =>
      simp only [nativeGK4DUnitTower, nativeGK4C_unitCount_trans,
        nativeGK4C_unitCount_unit, ih]
      omega

/-- Distinct natural numbers produce distinct original Type-valued
F54 routes despite identical endpoints and source Blocks. -/
theorem nativeGK4DUnitTower_injective
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    Function.Injective (nativeGK4DUnitTower tree) := by
  intro i j hij
  have hcount := congrArg
    (fun route : KuuNativeF45Tree.DepthRotationRoute p tree tree =>
      route.gk4cUnitCount) hij
  rw [nativeGK4DUnitTower_count, nativeGK4DUnitTower_count] at hcount
  omega

/-- P92B cannot compare ANY distinct stages of this original tower. -/
theorem nativeGK4DUnitTower_no_P92B
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    {i j : Nat} (hij : i ≠ j) :
    ¬ Nonempty (NativeF55P92AssocComparison p
      (nativeGK4DUnitTower tree i) (nativeGK4DUnitTower tree j)) := by
  rintro ⟨cell⟩
  have hcount := nativeGK4C_P92B_unitCount_sound cell
  rw [nativeGK4DUnitTower_count, nativeGK4DUnitTower_count] at hcount
  exact hij (by omega)

/-- Each successor has a genuine original typed F54 left-unit seam
to its predecessor, not an equality in the raw F54 source. -/
def nativeGK4DUnitTower_step
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (k : Nat) :
    NativeF54StructuralSeam p
      (nativeGK4DUnitTower tree (k + 1))
      (nativeGK4DUnitTower tree k) :=
  .leftUnit (nativeGK4DUnitTower tree k)

/-- Every pair of tower stages is connected by genuinely typed F54
structural seams, composed only with original refl/symm/trans. -/
def nativeGK4DUnitTower_connect
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (i j : Nat) :
    NativeF54StructuralSeam p
      (nativeGK4DUnitTower tree i)
      (nativeGK4DUnitTower tree j) := by
  induction i with
  | zero =>
      induction j with
      | zero => exact .refl (nativeGK4DUnitTower tree 0)
      | succ j ih =>
          exact .trans ih (.symm (nativeGK4DUnitTower_step tree j))
  | succ i ih =>
      exact .trans (nativeGK4DUnitTower_step tree i) ih

/-- Independent StructuralComparison has an ACTUAL original-typed
witness for every pair of original F54 tower stages. -/
theorem nativeGK4DUnitTower_structural_exists
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (i j : Nat) :
    Nonempty (NativeF55StructuralComparison p
      (nativeGK4DUnitTower tree i) (nativeGK4DUnitTower tree j)) :=
  ⟨.structural (nativeGK4DUnitTower_connect tree i j)⟩

/-- Infinite exact separation: the same original F54 pair is
connected in the added structural presentation, but not in P92B. -/
theorem nativeGK4DUnitTower_structural_not_P92B
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    {i j : Nat} (hij : i ≠ j) :
    Nonempty (NativeF55StructuralComparison p
      (nativeGK4DUnitTower tree i) (nativeGK4DUnitTower tree j)) ∧
    ¬ Nonempty (NativeF55P92AssocComparison p
      (nativeGK4DUnitTower tree i) (nativeGK4DUnitTower tree j)) := by
  exact ⟨nativeGK4DUnitTower_structural_exists tree i j,
    nativeGK4DUnitTower_no_P92B tree hij⟩

end Tower

/-! Actual finite C60 north-hexagon F45 witness, no model substitution. -/

/-- An explicit Nat-injective family of full original F54 proof
routes on an ACTUAL physical Site×Site north hexagon. -/
theorem nativeGK4D_physical_north_unitTower_injective :
    Function.Injective (nativeGK4DUnitTower (northHexagonNativeUnit 0)) :=
  nativeGK4DUnitTower_injective (northHexagonNativeUnit 0)

/-- Every pair of C60 tower stages is structurally connected. -/
theorem nativeGK4D_physical_north_unitTower_structural_exists
    (i j : Nat) :
    Nonempty (NativeF55StructuralComparison (.hexagon (.top 0))
      (nativeGK4DUnitTower (northHexagonNativeUnit 0) i)
      (nativeGK4DUnitTower (northHexagonNativeUnit 0) j)) :=
  nativeGK4DUnitTower_structural_exists (northHexagonNativeUnit 0) i j

/-- Every distinct C60 tower pair is connected in the structural
presentation but admits no original P92B comparison at all. -/
theorem nativeGK4D_physical_north_unitTower_separation
    {i j : Nat} (hij : i ≠ j) :
    Nonempty (NativeF55StructuralComparison (.hexagon (.top 0))
      (nativeGK4DUnitTower (northHexagonNativeUnit 0) i)
      (nativeGK4DUnitTower (northHexagonNativeUnit 0) j)) ∧
    ¬ Nonempty (NativeF55P92AssocComparison (.hexagon (.top 0))
      (nativeGK4DUnitTower (northHexagonNativeUnit 0) i)
      (nativeGK4DUnitTower (northHexagonNativeUnit 0) j)) :=
  nativeGK4DUnitTower_structural_not_P92B (northHexagonNativeUnit 0) hij

#print axioms nativeGK4DUnitTower
#print axioms nativeGK4DUnitTower_count
#print axioms nativeGK4DUnitTower_injective
#print axioms nativeGK4DUnitTower_no_P92B
#print axioms nativeGK4DUnitTower_step
#print axioms nativeGK4DUnitTower_connect
#print axioms nativeGK4DUnitTower_structural_exists
#print axioms nativeGK4DUnitTower_structural_not_P92B
#print axioms nativeGK4D_physical_north_unitTower_injective
#print axioms nativeGK4D_physical_north_unitTower_structural_exists
#print axioms nativeGK4D_physical_north_unitTower_separation

end
end Kuu.F112.Physical
