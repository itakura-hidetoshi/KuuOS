/-
KuString-MGAP4D-Emptiness Core v0.2

Specification skeleton.
This file is intentionally small: it records the theorem spine before the full
Hilbert-space / self-adjoint-operator / spectrum implementation.
-/

namespace KUOS
namespace KuString
namespace MGAP4D
namespace EmptinessCoreV02

structure KuWorld where
  State : Type
  H_world : State -> State
  K : State
  Orthogonal : State -> State -> Prop
  NormOne : State -> Prop

/-- K is the non-reified zero point for relational world-generation. -/
def IsEmptinessGround (W : KuWorld) : Prop :=
  W.H_world W.K = W.K

/-- K_perp is represented by states orthogonal to K. -/
def InKPerp (W : KuWorld) (psi : W.State) : Prop :=
  W.Orthogonal W.K psi

structure StringMode (W : KuWorld) where
  state : W.State
  in_appearance_space : InKPerp W state
  worldsheet_consistent : Prop
  non_reified : Prop

structure BraneMode (W : KuWorld) where
  boundary_supports : StringMode W -> Prop
  not_substance : Prop
  transition_surface : Prop

structure StableGapExcitation (W : KuWorld) where
  psi : W.State
  in_k_perp : InKPerp W psi
  normalized : W.NormOne psi
  eigen_gap_33_20 : Prop
  locally_detectable : Prop

/-- GapStabilizer must act on K_perp and must not reify K. -/
def GapDoesNotReifyK (W : KuWorld) : Prop :=
  forall psi : W.State, InKPerp W psi -> psi <> W.K

/-- P3: every valid string mode belongs to K_perp. -/
theorem string_modes_live_in_k_perp
  (W : KuWorld)
  (s : StringMode W) :
  InKPerp W s.state :=
  s.in_appearance_space

/-- P4: brane mode carries a non-substance witness. -/
theorem brane_does_not_reify_string
  (W : KuWorld)
  (b : BraneMode W) :
  b.not_substance :=
  b.not_substance

/-- P6/P9: a stable gap excitation is not K if the gap does not reify K. -/
theorem stable_excitation_not_K
  (W : KuWorld)
  (g : StableGapExcitation W)
  (h : GapDoesNotReifyK W) :
  g.psi <> W.K :=
  h g.psi g.in_k_perp

end EmptinessCoreV02
end MGAP4D
end KuString
end KUOS
