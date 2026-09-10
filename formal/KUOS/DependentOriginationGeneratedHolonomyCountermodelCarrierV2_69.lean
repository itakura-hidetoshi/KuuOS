import KUOS.DependentOriginationGeneratedFactorizationV2_68
import Mathlib.CategoryTheory.SingleObj
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Omega

namespace KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68

/-!
# Octahedral carrier for the generated-holonomy truth test v2.69

This file starts the finite truth test immediately after v2.68.  The source is
the six-object poset

```text
{L₀,L₁} < {M₀,M₁} < {H₀,H₁},
```

with every lower-level object below every higher-level object and no comparison
between distinct objects on the same level.  Its order complex is the boundary
of the octahedron (`S⁰ * S⁰ * S⁰`), hence there are nondegenerate triangles but
no nondegenerate tetrahedra.

The target fiber is the one-object groupoid of the multiplicative form of
`ZMod 2`.  Its nontrivial element will be used as a central compositor twist.
Nothing in this file asserts nontrivial generated holonomy yet; it only fixes the
finite carrier and the target automorphism used by the next two files.
-/

/-- A vertex of the octahedral sphere: one of two vertices on one of three
levels. -/
@[ext]
structure OctahedralVertex where
  level : Fin 3
  side : Fin 2
  deriving DecidableEq, Fintype

/-- The octahedral order: equality on a level, and strict comparison between
levels. -/
instance : PartialOrder OctahedralVertex where
  le X Y := X = Y ∨ X.level < Y.level
  le_refl X := Or.inl rfl
  le_trans X Y Z hXY hYZ := by
    rcases hXY with rfl | hXY
    · exact hYZ
    rcases hYZ with rfl | hYZ
    · exact Or.inr hXY
    · exact Or.inr (lt_trans hXY hYZ)
  le_antisymm X Y hXY hYX := by
    rcases hXY with hXY | hXY
    · exact hXY
    rcases hYX with hYX | hYX
    · exact hYX.symm
    · exact False.elim (lt_asymm hXY hYX)

instance : DecidableLE OctahedralVertex := by
  intro X Y
  change Decidable (X = Y ∨ X.level < Y.level)
  infer_instance

/-- The six named vertices. -/
def L0 : OctahedralVertex := ⟨0, 0⟩
def L1 : OctahedralVertex := ⟨0, 1⟩
def M0 : OctahedralVertex := ⟨1, 0⟩
def M1 : OctahedralVertex := ⟨1, 1⟩
def H0 : OctahedralVertex := ⟨2, 0⟩
def H1 : OctahedralVertex := ⟨2, 1⟩

@[simp] theorem L0_level : L0.level = 0 := rfl
@[simp] theorem L1_level : L1.level = 0 := rfl
@[simp] theorem M0_level : M0.level = 1 := rfl
@[simp] theorem M1_level : M1.level = 1 := rfl
@[simp] theorem H0_level : H0.level = 2 := rfl
@[simp] theorem H1_level : H1.level = 2 := rfl

/-- Three composable arrows in the octahedral poset must contain an identity
step.  Equivalently, there is no strict four-object chain and hence no
nondegenerate 3-simplex. -/
theorem adjacent_eq_of_three_composable
    {X Y Z T : OctahedralVertex}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) :
    X = Y ∨ Y = Z ∨ Z = T := by
  have hf : X = Y ∨ X.level < Y.level := leOfHom f
  have hg : Y = Z ∨ Y.level < Z.level := leOfHom g
  have hh : Z = T ∨ Z.level < T.level := leOfHom h
  rcases hf with hXY | hXY
  · exact Or.inl hXY
  rcases hg with hYZ | hYZ
  · exact Or.inr (Or.inl hYZ)
  rcases hh with hZT | hZT
  · exact Or.inr (Or.inr hZT)
  · exfalso
    omega

/-- All morphisms are inverted in the countermodel truth test. -/
def allMorphisms : MorphismProperty OctahedralVertex :=
  fun _ _ _ => True

/-- The eight lower-to-middle edges. -/
def a00 : L0 ⟶ M0 := homOfLE (by decide)
def a01 : L0 ⟶ M1 := homOfLE (by decide)
def a10 : L1 ⟶ M0 := homOfLE (by decide)
def a11 : L1 ⟶ M1 := homOfLE (by decide)

/-- The four middle-to-upper edges. -/
def b00 : M0 ⟶ H0 := homOfLE (by decide)
def b01 : M0 ⟶ H1 := homOfLE (by decide)
def b10 : M1 ⟶ H0 := homOfLE (by decide)
def b11 : M1 ⟶ H1 := homOfLE (by decide)

/-- The four direct lower-to-upper edges. -/
def c00 : L0 ⟶ H0 := homOfLE (by decide)
def c01 : L0 ⟶ H1 := homOfLE (by decide)
def c10 : L1 ⟶ H0 := homOfLE (by decide)
def c11 : L1 ⟶ H1 := homOfLE (by decide)

/-- Every triangular composite is the unique direct lower-to-upper arrow. -/
theorem triangle_comp_eq
    {L M H : OctahedralVertex}
    (a : L ⟶ M) (b : M ⟶ H) (c : L ⟶ H) :
    a ≫ b = c :=
  Subsingleton.elim _ _

/-- The central two-element group used by the target one-object groupoid. -/
abbrev C2 := Multiplicative (ZMod 2)

/-- The one-object groupoid carrying the compositor twist. -/
abbrev CounterFiber := SingleObj C2

/-- The nontrivial element of `C2`. -/
def zeta : C2 := Multiplicative.ofAdd (1 : ZMod 2)

@[simp] theorem zeta_mul_zeta : zeta * zeta = 1 := by
  change Multiplicative.ofAdd ((1 : ZMod 2) + 1) = Multiplicative.ofAdd 0
  congr
  norm_num

@[simp] theorem zeta_inv : zeta⁻¹ = zeta := by
  apply inv_eq_iff_mul_eq_one.mpr
  exact zeta_mul_zeta

/-- The twist is genuinely nontrivial. -/
theorem zeta_ne_one : zeta ≠ 1 := by
  intro h
  have h' := congrArg Multiplicative.toAdd h
  change (1 : ZMod 2) = 0 at h'
  exact one_ne_zero h'

/-- A central natural automorphism of the identity functor on the one-object
`C2` groupoid, represented by a group element. -/
noncomputable def scalarIdNatIso (z : C2) :
    (𝟭 CounterFiber) ≅ (𝟭 CounterFiber) :=
  NatIso.ofComponents
    (fun X => by
      cases X
      exact asIso (SingleObj.toEnd C2 z))
    (by
      intro X Y f
      cases X
      cases Y
      simp only [Functor.id_obj, Functor.id_map, SingleObj.comp_as_mul,
        SingleObj.toEnd_def]
      exact mul_comm _ _)

/-- Multiplication of scalar identity automorphisms follows multiplication in
`C2`.  This is the finite centrality fact later used to cancel the two
admissibility-generated inverse-pair contributions. -/
theorem scalarIdNatIso_hom_app_star
    (z : C2) :
    (scalarIdNatIso z).hom.app (SingleObj.star C2) = z := by
  rfl

/-- The scalar automorphism attached to `zeta` is not the identity natural
isomorphism. -/
theorem scalarIdNatIso_zeta_ne_refl :
    scalarIdNatIso zeta ≠ Iso.refl (𝟭 CounterFiber) := by
  intro h
  have h' := congrArg
    (fun e : (𝟭 CounterFiber) ≅ (𝟭 CounterFiber) =>
      e.hom.app (SingleObj.star C2)) h
  have hz : zeta = 1 := by
    simpa [scalarIdNatIso_hom_app_star] using h'
  exact zeta_ne_one hz

end KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
