import Mathlib

namespace KUOS.GaugeInvariantDependentOriginationDenseDescentV0_1

open Set Topology

universe u v w z

variable {X : Type u} {Y : Type v} {Gauge : Type w}
variable {Local : ℕ → Type z}

/-- The union of all local realization images inside one global carrier. -/
def realizationImageUnion
    (realize : (n : ℕ) → Local n → X) : Set X :=
  {x | ∃ n : ℕ, ∃ u : Local n, realize n u = x}

/-- Cross-scale compatibility means that two local representatives which realize
as the same global point have exactly the same readout. -/
def CrossScaleCompatible
    (realize : (n : ℕ) → Local n → X)
    (target : (n : ℕ) → Local n → Y) : Prop :=
  ∀ (n m : ℕ) (u : Local n) (v : Local m),
    realize n u = realize m v → target n u = target m v

/-- Any exact global readout automatically forces cross-scale compatibility.
No density or topology is needed for this direction. -/
theorem crossScaleCompatible_of_globalReadout
    (realize : (n : ℕ) → Local n → X)
    (target : (n : ℕ) → Local n → Y)
    (globalReadout : X → Y)
    (hreadout : ∀ (n : ℕ) (u : Local n),
      globalReadout (realize n u) = target n u) :
    CrossScaleCompatible realize target := by
  intro n m u v huv
  calc
    target n u = globalReadout (realize n u) := (hreadout n u).symm
    _ = globalReadout (realize m v) := congrArg globalReadout huv
    _ = target m v := hreadout m v

/-- Dense local realization, continuous global semantics, equivariant transport,
and exact local gauge invariance generate global semantic gauge invariance.

This is the abstract KuuOS local-to-global descent schema extracted from the
Wilson interpolation argument: the proof is Mathlib's identity principle for
continuous maps on a dense set.  No Haar averaging, global surjectivity, or
preferred gauge representative is required. -/
theorem semantic_invariant_of_dense_local_realization
    [TopologicalSpace X] [TopologicalSpace Y] [T2Space Y]
    (realize : (n : ℕ) → Local n → X)
    (globalAction : Gauge → X → X)
    (localAction : (n : ℕ) → Gauge → Local n → Local n)
    (semantic : ContinuousMap X Y)
    (hDense : Dense (realizationImageUnion realize))
    (hActionContinuous : ∀ g : Gauge, Continuous (globalAction g))
    (hEquivariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      globalAction g (realize n u) = realize n (localAction n g u))
    (hLocalInvariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      semantic (realize n (localAction n g u)) = semantic (realize n u)) :
    ∀ (g : Gauge) (x : X), semantic (globalAction g x) = semantic x := by
  intro g x
  have hfun :
      (fun y : X => semantic (globalAction g y)) =
        (fun y : X => semantic y) := by
    apply Continuous.ext_on hDense
    · exact semantic.continuous.comp (hActionContinuous g)
    · exact semantic.continuous
    · intro y hy
      rcases hy with ⟨n, u, rfl⟩
      rw [hEquivariant n g u]
      exact hLocalInvariant n g u
  exact congrFun hfun x

/-- Once exact readout values are prescribed on a dense realization union,
there is at most one continuous global semantic extension.  Thus density gives
uniqueness, not existence. -/
theorem continuous_globalReadout_unique_of_dense
    [TopologicalSpace X] [TopologicalSpace Y] [T2Space Y]
    (realize : (n : ℕ) → Local n → X)
    (target : (n : ℕ) → Local n → Y)
    (hDense : Dense (realizationImageUnion realize))
    (O₁ O₂ : ContinuousMap X Y)
    (hreadout₁ : ∀ (n : ℕ) (u : Local n), O₁ (realize n u) = target n u)
    (hreadout₂ : ∀ (n : ℕ) (u : Local n), O₂ (realize n u) = target n u) :
    O₁ = O₂ := by
  have hfun : (fun x : X => O₁ x) = (fun x : X => O₂ x) := by
    apply Continuous.ext_on hDense
    · exact O₁.continuous
    · exact O₂.continuous
    · intro x hx
      rcases hx with ⟨n, u, rfl⟩
      calc
        O₁ (realize n u) = target n u := hreadout₁ n u
        _ = O₂ (realize n u) := (hreadout₂ n u).symm
  ext x
  exact congrFun hfun x

/-- Gauge-related representatives have the same semantic value whenever the
semantic readout is globally invariant.  This is the formal non-privileging of
a gauge representative at the semantic layer. -/
theorem semantic_eq_of_gauge_related
    (globalAction : Gauge → X → X)
    (semantic : X → Y)
    (hInvariant : ∀ (g : Gauge) (x : X),
      semantic (globalAction g x) = semantic x)
    {x y : X}
    (hxy : ∃ g : Gauge, globalAction g x = y) :
    semantic y = semantic x := by
  rcases hxy with ⟨g, rfl⟩
  exact hInvariant g x

/-- Exact local readout plus dense descent simultaneously yields semantic gauge
invariance and cross-scale compatibility, while keeping global extension
existence as an explicit input. -/
theorem dense_descent_invariance_and_compatibility
    [TopologicalSpace X] [TopologicalSpace Y] [T2Space Y]
    (realize : (n : ℕ) → Local n → X)
    (target : (n : ℕ) → Local n → Y)
    (globalAction : Gauge → X → X)
    (localAction : (n : ℕ) → Gauge → Local n → Local n)
    (semantic : ContinuousMap X Y)
    (hDense : Dense (realizationImageUnion realize))
    (hActionContinuous : ∀ g : Gauge, Continuous (globalAction g))
    (hEquivariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      globalAction g (realize n u) = realize n (localAction n g u))
    (hreadout : ∀ (n : ℕ) (u : Local n),
      semantic (realize n u) = target n u)
    (hTargetInvariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      target n (localAction n g u) = target n u) :
    (∀ (g : Gauge) (x : X), semantic (globalAction g x) = semantic x) ∧
      CrossScaleCompatible realize target := by
  constructor
  · apply semantic_invariant_of_dense_local_realization
      realize globalAction localAction semantic hDense hActionContinuous hEquivariant
    intro n g u
    rw [hreadout n, hreadout n]
    exact hTargetInvariant n g u
  · exact crossScaleCompatible_of_globalReadout realize target semantic hreadout

end KUOS.GaugeInvariantDependentOriginationDenseDescentV0_1
