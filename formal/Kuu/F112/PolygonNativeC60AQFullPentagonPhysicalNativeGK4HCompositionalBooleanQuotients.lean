import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4GBooleanQuotientGrading
import Mathlib.Tactic

/-!
# F112-P94D3GK4H — true compositional Boolean quotient descent

Keep the independently typed original F45 Tree, D/E categorical Blocks,
two Nat depth indices, the five-constructor F54 source route grammar,
and two DISTINCT quotient presentations. The GK4G Boolean observation is
true exactly on zero-primitive-rotation raw F54 witnesses.

1. The true F54 vertical composition adds exact original physical
rotation counts; its Bool zero-grade therefore multiplies by Bool.and.
2. P92B pre/post 3-cell constructors transport representatives, so the
EXISTING actual P92B witness-existence quotient has a well-defined
dependent route composition; its Bool grade is multiplicative.
3. An extended StructuralComparison proof has no primitive pre/post
constructors, but its original and structural F54 components do.
We derive two actual Type-valued pre/post transports by recursion
over its three constructors, allowing the distinct EXISTING structural
witness-existence quotient to carry dependent composition. Its grade
is multiplicative. The GK4E canonical nonfaithful P92B→structural
quotient surjection strictly preserves the dependent composition.
4. Genuine original F54 StructuralSeam reassoc/leftUnit/rightUnit
makes the STRUCTURAL quotient composition associative and unital.
By contrast GK4C's exact original zero-chain unit atom obstruction
shows the ORIGINAL P92B quotient composition is NOT left/right
unital even on genuine typed physical C60 routes. The Bool grade
does NOT falsely reflect that missing identity law.

No quotient is conflated with original Type-valued 3-cell evidence.
P92B associativity/units, historical F19/F28/F54/F55 typed equivalence,
genuine 14D unconditional Countable, true 19D filler, global strict n
and higher hyperdescent remain outside the proved scope. No Gray.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only/same-root, 107 public roots, protected #1558 unchanged.
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

section FullyTypedComposition

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
variable (t₄ : KuuNativeF45Tree p n₄ m₄ ma pa mb pb)

/-- Exact primitive rotation count, not shadow or quotient count. -/
@[simp] theorem nativeGK4H_raw_rotationCount_compose
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).rotationCount =
      u.rotationCount + v.rotationCount := by
  rfl

/-- A ZERO original physical-rotation count of u≫v occurs iff
BOTH original proof routes have zero physical rotation count. -/
theorem nativeGK4H_rawGrade_compose
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
    nativeGK4GRawGrade t₁ t₃ (.trans u v) =
      (nativeGK4GRawGrade t₁ t₂ u &&
        nativeGK4GRawGrade t₂ t₃ v) := by
  change decide (u.rotationCount + v.rotationCount = 0) =
    (decide (u.rotationCount = 0) && decide (v.rotationCount = 0))
  by_cases hu : u.rotationCount = 0
  · by_cases hv : v.rotationCount = 0
    · simp [hu, hv]
    · have hn : u.rotationCount + v.rotationCount ≠ 0 := by omega
      simp [hu, hv, hn]
  · have hn : u.rotationCount + v.rotationCount ≠ 0 := by omega
    simp [hu, hn]

/-- Type-valued original P92B comparison pre/post composition remains
GENUINELY available: its two relevant original primitive generators
are explicitly declared, never derived from a shadow. -/
def nativeGK4H_p92Compose
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    NativeF55P92AssocRouteClasses t₁ t₃ :=
  _root_.Quotient.liftOn₂ u v
    (fun r s => nativeF55P92AssocRouteClass t₁ t₃ (.trans r s))
    (by
      intro r s r' s' hrr' hss'
      apply _root_.Quotient.sound
      exact hrr'.elim (fun firstCell => hss'.elim (fun secondCell =>
        ⟨NativeF55P92AssocComparison.trans
          (.postcompose firstCell s) (.precompose r' secondCell)⟩)))

/-- Actual dependent P92B quotient composition on original F54 classes
is represented by the exact original F54 vertical composition. -/
@[simp] theorem nativeGK4H_p92Compose_class
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
    nativeGK4H_p92Compose t₁ t₂ t₃
      (nativeF55P92AssocRouteClass t₁ t₂ u)
      (nativeF55P92AssocRouteClass t₂ t₃ v) =
    nativeF55P92AssocRouteClass t₁ t₃ (.trans u v) := by
  rfl

/-- Transport through the three-constructor extended structural
comparison by ORIGINAL P92B precomposition or ORIGINAL F54 seam
precomposition, keeping all intermediate typed proof histories. -/
def nativeGK4H_structuralPrecompose
    (prior : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    {r s : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃}
    (cell : NativeF55StructuralComparison p r s) :
    NativeF55StructuralComparison p (.trans prior r) (.trans prior s) := by
  induction cell with
  | original old => exact .original (.precompose prior old)
  | structural seam => exact .structural (.precompose prior seam)
  | trans left right ihLeft ihRight => exact .trans ihLeft ihRight

/-- Independent structural comparison is also closed under genuine
original F54 postcomposition, by recursive Type-valued evidence. -/
def nativeGK4H_structuralPostcompose
    {r s : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂}
    (cell : NativeF55StructuralComparison p r s)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
    NativeF55StructuralComparison p (.trans r suffix) (.trans s suffix) := by
  induction cell with
  | original old => exact .original (.postcompose old suffix)
  | structural seam => exact .structural (.postcompose seam suffix)
  | trans left right ihLeft ihRight => exact .trans ihLeft ihRight

/-- Genuine structural route quotient composition is independently
well-defined, because BOTH raw original P92B and the genuinely
additional F54 structural seams have proved pre/post compatibility. -/
def nativeGK4H_structuralCompose
    (u : NativeGK4EStructuralRouteClasses t₁ t₂)
    (v : NativeGK4EStructuralRouteClasses t₂ t₃) :
    NativeGK4EStructuralRouteClasses t₁ t₃ :=
  _root_.Quotient.liftOn₂ u v
    (fun r s => nativeGK4EStructuralRouteClass t₁ t₃ (.trans r s))
    (by
      intro r s r' s' hrr' hss'
      apply _root_.Quotient.sound
      exact hrr'.elim (fun firstCell => hss'.elim (fun secondCell =>
        ⟨NativeF55StructuralComparison.trans
          (nativeGK4H_structuralPostcompose t₁ t₂ t₃ firstCell s)
          (nativeGK4H_structuralPrecompose t₁ t₂ t₃ r' secondCell)⟩)))

@[simp] theorem nativeGK4H_structuralCompose_class
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
    nativeGK4H_structuralCompose t₁ t₂ t₃
      (nativeGK4EStructuralRouteClass t₁ t₂ u)
      (nativeGK4EStructuralRouteClass t₂ t₃ v) =
    nativeGK4EStructuralRouteClass t₁ t₃ (.trans u v) := by
  rfl

/-- Full quotient composition is compatible with GK4G's actually
descended original-P92B zero/positive Boolean grade, not a
composition of forgotten numerical shadows. -/
theorem nativeGK4H_p92Grade_compose
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4GP92Grade t₁ t₃ (nativeGK4H_p92Compose t₁ t₂ t₃ u v) =
      (nativeGK4GP92Grade t₁ t₂ u && nativeGK4GP92Grade t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  refine _root_.Quotient.inductionOn v ?_
  intro s
  exact nativeGK4H_rawGrade_compose t₁ t₂ t₃ r s

/-- The separate structural witness-existence quotient has the
SAME multiplicative Boolean grade, using the same source routes. -/
theorem nativeGK4H_structuralGrade_compose
    (u : NativeGK4EStructuralRouteClasses t₁ t₂)
    (v : NativeGK4EStructuralRouteClasses t₂ t₃) :
    nativeGK4GStructuralGrade t₁ t₃
        (nativeGK4H_structuralCompose t₁ t₂ t₃ u v) =
      (nativeGK4GStructuralGrade t₁ t₂ u &&
        nativeGK4GStructuralGrade t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  refine _root_.Quotient.inductionOn v ?_
  intro s
  exact nativeGK4H_rawGrade_compose t₁ t₂ t₃ r s

/-- The ORIGINAL GK4E P92B→structural quotient surjection strictly
preserves actual dependent proof-route composition. The map is
nonfaithful; no Type-valued reverse comparison is fabricated. -/
theorem nativeGK4H_comparison_preserves_compose
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4EP92ToStructural t₁ t₃
        (nativeGK4H_p92Compose t₁ t₂ t₃ u v) =
      nativeGK4H_structuralCompose t₁ t₂ t₃
        (nativeGK4EP92ToStructural t₁ t₂ u)
        (nativeGK4EP92ToStructural t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  refine _root_.Quotient.inductionOn v ?_
  intro s
  rfl

/-- The separately added F54 reassociator is a TRUE Type-valued
structural seam. Thus structural route class composition is
associative at all original fully dependent F45 endpoints. -/
theorem nativeGK4H_structuralCompose_assoc
    (u : NativeGK4EStructuralRouteClasses t₁ t₂)
    (v : NativeGK4EStructuralRouteClasses t₂ t₃)
    (w : NativeGK4EStructuralRouteClasses t₃ t₄) :
    nativeGK4H_structuralCompose t₁ t₃ t₄
        (nativeGK4H_structuralCompose t₁ t₂ t₃ u v) w =
      nativeGK4H_structuralCompose t₁ t₂ t₄ u
        (nativeGK4H_structuralCompose t₂ t₃ t₄ v w) := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  refine _root_.Quotient.inductionOn v ?_
  intro s
  refine _root_.Quotient.inductionOn w ?_
  intro t
  change nativeGK4EStructuralRouteClass t₁ t₄ (.trans (.trans r s) t) =
    nativeGK4EStructuralRouteClass t₁ t₄ (.trans r (.trans s t))
  exact _root_.Quotient.sound
    ⟨NativeF55StructuralComparison.structural (.reassoc r s t)⟩

/-- Actual original F54 typed zero-edge identity representative. -/
def nativeGK4H_p92Unit :
    NativeF55P92AssocRouteClasses t₁ t₁ :=
  nativeF55P92AssocRouteClass t₁ t₁ (.chain (.refl t₁))

def nativeGK4H_structuralUnit :
    NativeGK4EStructuralRouteClasses t₁ t₁ :=
  nativeGK4EStructuralRouteClass t₁ t₁ (.chain (.refl t₁))

/-- True structural class composition has a left identity, via the
independently adjoined genuine original F54 leftUnit seam. -/
theorem nativeGK4H_structuralCompose_leftUnit
    (u : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4H_structuralCompose t₁ t₁ t₂
      (nativeGK4H_structuralUnit t₁) u = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  exact _root_.Quotient.sound
    ⟨NativeF55StructuralComparison.structural (.leftUnit r)⟩

theorem nativeGK4H_structuralCompose_rightUnit
    (u : NativeGK4EStructuralRouteClasses t₁ t₂) :
    nativeGK4H_structuralCompose t₁ t₂ t₂
      u (nativeGK4H_structuralUnit t₂) = u := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  exact _root_.Quotient.sound
    ⟨NativeF55StructuralComparison.structural (.rightUnit r)⟩

/-- Unbridgeable, ORIGINAL P92B proof-level defect: although its
quotient composition is well-defined, the specified honest F54
zero-edge unit is NOT a left identity at any original source route.
The attempted equality would require a forbidden P92B 3-cell. -/
theorem nativeGK4H_p92Compose_leftUnit_ne
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4H_p92Compose t₁ t₁ t₂
      (nativeGK4H_p92Unit t₁)
      (nativeF55P92AssocRouteClass t₁ t₂ r) ≠
    nativeF55P92AssocRouteClass t₁ t₂ r := by
  intro h
  have hraw :
      nativeF55P92AssocRouteClass t₁ t₂
        (.trans (.chain (.refl t₁)) r) =
      nativeF55P92AssocRouteClass t₁ t₂ r := by
    simpa only [nativeGK4H_p92Compose_class] using h
  exact nativeGK4C_leftUnit_no_P92B r
    ((nativeF55P92AssocRouteClass_eq_iff t₁ t₂ _ _).mp hraw)

/-- The original P92B zero-edge unit is likewise NOT a right identity;
the real structural presentation repairs it using a separately
declared seam, and that seam is not silently a P92B 3-cell. -/
theorem nativeGK4H_p92Compose_rightUnit_ne
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4H_p92Compose t₁ t₂ t₂
      (nativeF55P92AssocRouteClass t₁ t₂ r)
      (nativeGK4H_p92Unit t₂) ≠
    nativeF55P92AssocRouteClass t₁ t₂ r := by
  intro h
  have hraw :
      nativeF55P92AssocRouteClass t₁ t₂
        (.trans r (.chain (.refl t₂))) =
      nativeF55P92AssocRouteClass t₁ t₂ r := by
    simpa only [nativeGK4H_p92Compose_class] using h
  exact nativeGK4C_rightUnit_no_P92B r
    ((nativeF55P92AssocRouteClass_eq_iff t₁ t₂ _ _).mp hraw)

/-- Boolean descent is NOT faithful to the original P92B unit law:
the two original P92B classes are DISTINCT, but have IDENTICAL
Boolean grade. This is an exact obstruction, not an observer-created
3-cell or a category-theoretic statement about a different quotient. -/
theorem nativeGK4H_p92Grade_cannot_reflect_unit
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    (nativeGK4GP92Grade t₁ t₂
        (nativeGK4H_p92Compose t₁ t₁ t₂
          (nativeGK4H_p92Unit t₁)
          (nativeF55P92AssocRouteClass t₁ t₂ r)) =
      nativeGK4GP92Grade t₁ t₂
        (nativeF55P92AssocRouteClass t₁ t₂ r)) ∧
    nativeGK4H_p92Compose t₁ t₁ t₂
        (nativeGK4H_p92Unit t₁)
        (nativeF55P92AssocRouteClass t₁ t₂ r) ≠
      nativeF55P92AssocRouteClass t₁ t₂ r := by
  constructor
  · rw [nativeGK4H_p92Grade_compose]
    have hunit : nativeGK4GP92Grade t₁ t₁
        (nativeGK4H_p92Unit t₁) = true := rfl
    rw [hunit]
    rfl
  · exact nativeGK4H_p92Compose_leftUnit_ne t₁ t₂ r

end FullyTypedComposition

/-! ### Genuine C60 site x site original-stage demonstration. -/

/-- True physical north C60 source retains independent original
Site x Site F45 Tree, categorical Blocks and both Nat depth axes. -/
theorem nativeGK4H_physical_north_structural_unit_and_p92_noUnit :
    nativeGK4H_structuralCompose
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
        nativeGK4FPhysicalNorthTriple
        (nativeGK4H_structuralUnit nativeGK4FPhysicalNorthTriple)
        (nativeGK4H_structuralUnit nativeGK4FPhysicalNorthTriple) =
      nativeGK4H_structuralUnit nativeGK4FPhysicalNorthTriple ∧
    nativeGK4H_p92Compose
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
        nativeGK4FPhysicalNorthTriple
        (nativeGK4H_p92Unit nativeGK4FPhysicalNorthTriple)
        (nativeGK4H_p92Unit nativeGK4FPhysicalNorthTriple) ≠
      nativeGK4H_p92Unit nativeGK4FPhysicalNorthTriple := by
  constructor
  · exact nativeGK4H_structuralCompose_leftUnit
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
      (nativeGK4H_structuralUnit nativeGK4FPhysicalNorthTriple)
  · exact nativeGK4H_p92Compose_leftUnit_ne
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
      (.chain (.refl nativeGK4FPhysicalNorthTriple))

/-- At physical C60, the genuinely quotiented original zero-rotation
Bool grade is strictly multiplicative, while its missing P92B identity
shows that the grade cannot reflect all source category laws. -/
theorem nativeGK4H_physical_north_bool_multiplicative
    (u v : NativeF55P92AssocRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) :
    nativeGK4GP92Grade nativeGK4FPhysicalNorthTriple
        nativeGK4FPhysicalNorthTriple
        (nativeGK4H_p92Compose
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
          nativeGK4FPhysicalNorthTriple u v) =
      nativeGK4GP92Grade nativeGK4FPhysicalNorthTriple
          nativeGK4FPhysicalNorthTriple u &&
        nativeGK4GP92Grade nativeGK4FPhysicalNorthTriple
          nativeGK4FPhysicalNorthTriple v) :=
  nativeGK4H_p92Grade_compose _ _ _ u v

#print axioms nativeGK4H_raw_rotationCount_compose
#print axioms nativeGK4H_rawGrade_compose
#print axioms nativeGK4H_p92Compose
#print axioms nativeGK4H_p92Compose_class
#print axioms nativeGK4H_structuralPrecompose
#print axioms nativeGK4H_structuralPostcompose
#print axioms nativeGK4H_structuralCompose
#print axioms nativeGK4H_structuralCompose_class
#print axioms nativeGK4H_p92Grade_compose
#print axioms nativeGK4H_structuralGrade_compose
#print axioms nativeGK4H_comparison_preserves_compose
#print axioms nativeGK4H_structuralCompose_assoc
#print axioms nativeGK4H_p92Unit
#print axioms nativeGK4H_structuralUnit
#print axioms nativeGK4H_structuralCompose_leftUnit
#print axioms nativeGK4H_structuralCompose_rightUnit
#print axioms nativeGK4H_p92Compose_leftUnit_ne
#print axioms nativeGK4H_p92Compose_rightUnit_ne
#print axioms nativeGK4H_p92Grade_cannot_reflect_unit
#print axioms nativeGK4H_physical_north_structural_unit_and_p92_noUnit
#print axioms nativeGK4H_physical_north_bool_multiplicative

end
end Kuu.F112.Physical
