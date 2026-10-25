import Kuu.F112.PolygonNativeC60FiniteObserverDescent
import Mathlib.Tactic

/-!
# F112-P94D3AZ — all-finite C60 two-sided gauge and internal holonomy

AY descends inherited original 14D-boundary and Peiffer observations.
AZ adds a distinct group-valued observation of the ACTUAL AX free
higher-comparison syntax, with a left/source and right/target frame.

The transport law is NONCOMMUTATIVE and holds for every explicitly
supplied finite AX signature plan. New holonomy has an exact new
generator-compatibility obligation at the next quotient; it is not
automatically descended by AY's inherited-observer argument.

Specialization uses the original C60 14D fiber, AQ 15D terms, and
AS physical nontrivial Peiffer kernel. The extra holonomy label is
a CHOICE on the optional Kuu comparison, not a pre-existing
geometric 16-cell or a proof of P92B hyperdescent.

No Gray, abelianization, new axioms, sorry, or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w uD vD uE vE

/-- Gauge the group-valued observation of a typed C60 layer at BOTH
original lower endpoints. In general the two frames are different. -/
def nativeC60AZGauge {L : NativeC60AXLayer.{u}}
    {G : Type v} [Group G] (frame : L.Obj → G)
    (obs : L.Total → G) (c : L.Total) : G :=
  frame c.1.1 * obs c * (frame c.1.2)⁻¹

theorem nativeC60AZGauge_one {L : NativeC60AXLayer.{u}}
    {G : Type v} [Group G] (obs : L.Total → G) :
    nativeC60AZGauge (fun _ => (1 : G)) obs = obs := by
  funext c
  simp [nativeC60AZGauge]

/-- Successive changes of frame compose in ORDER; no commutativity. -/
theorem nativeC60AZGauge_comp {L : NativeC60AXLayer.{u}}
    {G : Type v} [Group G]
    (outer inner : L.Obj → G) (obs : L.Total → G) :
    nativeC60AZGauge outer (nativeC60AZGauge inner obs) =
      nativeC60AZGauge (fun x => outer x * inner x) obs := by
  funext c
  change outer c.1.1 *
    (inner c.1.1 * obs c * (inner c.1.2)⁻¹) * (outer c.1.2)⁻¹ =
      (outer c.1.1 * inner c.1.1) * obs c *
        (outer c.1.2 * inner c.1.2)⁻¹
  group

/-- A homomorphism transports BOTH frames, retaining the ordered
noncommutative product in every target receiver. -/
theorem nativeC60AZGauge_map {L : NativeC60AXLayer.{u}}
    {G : Type v} [Group G] {H : Type w} [Group H]
    (f : G →* H) (frame : L.Obj → G) (obs : L.Total → G) :
    (fun c => f (nativeC60AZGauge frame obs c)) =
      nativeC60AZGauge (fun x => f (frame x)) (fun c => f (obs c)) := by
  funext c
  simp only [nativeC60AZGauge, map_mul, map_inv]

/-- Two-sided gauging cannot alter generator compatibility, since
the exact SOURCE and TARGET of every declared generator agree. -/
theorem nativeC60AZGauge_respects_iff
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {G : Type v} [Group G]
    (frame : L.Obj → G) (obs : L.Total → G) :
    NativeC60AYRespects S (nativeC60AZGauge frame obs) ↔
      NativeC60AYRespects S obs := by
  constructor
  · intro h x y g
    have hs : frame x.1.1 = frame y.1.1 :=
      congrArg (fun endpoints : L.Obj × L.Obj => frame endpoints.1) (S.boundary g)
    have ht : frame x.1.2 = frame y.1.2 :=
      congrArg (fun endpoints : L.Obj × L.Obj => frame endpoints.2) (S.boundary g)
    have hg := h g
    change frame x.1.1 * obs x * (frame x.1.2)⁻¹ =
      frame y.1.1 * obs y * (frame y.1.2)⁻¹ at hg
    rw [hs, ht] at hg
    exact mul_left_cancel (mul_right_cancel hg)
  · intro h x y g
    have hs : frame x.1.1 = frame y.1.1 :=
      congrArg (fun endpoints : L.Obj × L.Obj => frame endpoints.1) (S.boundary g)
    have ht : frame x.1.2 = frame y.1.2 :=
      congrArg (fun endpoints : L.Obj × L.Obj => frame endpoints.2) (S.boundary g)
    change frame x.1.1 * obs x * (frame x.1.2)⁻¹ =
      frame y.1.1 * obs y * (frame y.1.2)⁻¹
    rw [hs, ht, h g]

/-- The free higher step has its OWN internal group-valued holonomy,
independent of the inherited boundary observer of AY. -/
def nativeC60AZHolonomy {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) {G : Type v} [Group G]
    (weight : ∀ {x y}, S.Gen x y → G)
    {x y : L.Total} (c : NativeC60AXStep S x y) : G :=
  c.fold (K := fun _ _ => G) weight
    (fun _ => 1) (fun z => z⁻¹) (fun z t => z * t)

@[simp] theorem nativeC60AZHolonomy_atom
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {G : Type v} [Group G] (weight : ∀ {x y}, S.Gen x y → G)
    {x y : L.Total} (g : S.Gen x y) :
    nativeC60AZHolonomy S weight (.atom g) = weight g := rfl

@[simp] theorem nativeC60AZHolonomy_refl
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {G : Type v} [Group G] (weight : ∀ {x y}, S.Gen x y → G)
    (x : L.Total) :
    nativeC60AZHolonomy S weight (.refl x) = 1 := rfl

@[simp] theorem nativeC60AZHolonomy_symm
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {G : Type v} [Group G] (weight : ∀ {x y}, S.Gen x y → G)
    {x y : L.Total} (c : NativeC60AXStep S x y) :
    nativeC60AZHolonomy S weight (.symm c) =
      (nativeC60AZHolonomy S weight c)⁻¹ := rfl

@[simp] theorem nativeC60AZHolonomy_trans
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {G : Type v} [Group G] (weight : ∀ {x y}, S.Gen x y → G)
    {x y z : L.Total} (c : NativeC60AXStep S x y)
    (d : NativeC60AXStep S y z) :
    nativeC60AZHolonomy S weight (.trans c d) =
      nativeC60AZHolonomy S weight c *
        nativeC60AZHolonomy S weight d := rfl

/-- Frame changes of primitive HIGHER comparisons are fully
two-sided and depend on the TRUE previous-level cell endpoints. -/
def nativeC60AZGaugeWeight {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) {G : Type v} [Group G]
    (frame : L.Total → G)
    (weight : ∀ {x y}, S.Gen x y → G) :
    ∀ {x y}, S.Gen x y → G :=
  fun {x y} g => frame x * weight g * (frame y)⁻¹

/-- Exact noncommutative gauge covariance of every higher AX
comparison word, including reversal and ordered composition. -/
theorem nativeC60AZHolonomy_covariant
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {G : Type v} [Group G]
    (frame : L.Total → G)
    (weight : ∀ {x y}, S.Gen x y → G)
    {x y : L.Total} (c : NativeC60AXStep S x y) :
    nativeC60AZHolonomy S (nativeC60AZGaugeWeight S frame weight) c =
      frame x * nativeC60AZHolonomy S weight c * (frame y)⁻¹ := by
  induction c with
  | atom g => rfl
  | refl a =>
      simp only [nativeC60AZHolonomy_refl]
      group
  | symm h ih =>
      simp only [nativeC60AZHolonomy_symm, ih]
      group
  | trans h k ih ik =>
      simp only [nativeC60AZHolonomy_trans, ih, ik]
      group

/-- Finite-height gauge covariance is a SINGLE dependent induction.
Each stage may choose its own two-sided frame and generator values. -/
def NativeC60AZAllFiniteCovariant {G : Type v} [Group G] :
    (L : NativeC60AXLayer.{u}) → (N : Nat) → NativeC60AXPlan L N → Prop
  | _, 0, _ => True
  | L, N + 1, p =>
      (∀ (frame : L.Total → G)
          (weight : ∀ {x y}, p.1.Gen x y → G)
          {x y : L.Total} (c : NativeC60AXStep p.1 x y),
        nativeC60AZHolonomy p.1 (nativeC60AZGaugeWeight p.1 frame weight) c =
          frame x * nativeC60AZHolonomy p.1 weight c * (frame y)⁻¹) ∧
      NativeC60AZAllFiniteCovariant (G := G)
        (nativeC60AXNext L p.1) N p.2

theorem nativeC60AZAllFiniteCovariant_sound
    {G : Type v} [Group G]
    (L : NativeC60AXLayer.{u}) (N : Nat) (p : NativeC60AXPlan L N) :
    NativeC60AZAllFiniteCovariant (G := G) L N p := by
  induction N generalizing L with
  | zero => trivial
  | succ N ih =>
      refine ⟨?_, ih (nativeC60AXNext L p.1) p.2⟩
      intro frame weight x y c
      exact nativeC60AZHolonomy_covariant p.1 frame weight c

/-- Observe the NEW higher comparison cell itself, not just its
original 14D source inherited through the AX tower. -/
def nativeC60AZInternalObserver
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {G : Type v} [Group G]
    (weight : ∀ {x y}, S.Gen x y → G) :
    (nativeC60AXNext L S).Total → G :=
  fun c => nativeC60AZHolonomy S weight c.2

/-- A new internal holonomy descends at the NEXT layer iff each
new primitive explicitly conserves it. This is independent of AY's
automatic descent of inherited LOWER-boundary observables. -/
theorem nativeC60AZInternalDescent_iff
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    {G : Type v} [Group G] (weight : ∀ {x y}, S.Gen x y → G) :
    (∃ f : Quotient (nativeC60AXSetoid T) → G,
      ∀ c, f (Quotient.mk (nativeC60AXSetoid T) c) =
        nativeC60AZInternalObserver S weight c) ↔
      (∀ {x y}, T.Gen x y →
        nativeC60AZHolonomy S weight x.2 =
          nativeC60AZHolonomy S weight y.2) :=
  nativeC60AXDescent_iff T (nativeC60AZInternalObserver S weight)

/-- Compatibility of a NEW internal observer with the first NEXT
signature is necessary and sufficient through every later finite
continuation (for its inherited transport after that first test). -/
theorem nativeC60AZInternalFiniteDescent_iff
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    (N : Nat)
    (p : NativeC60AXPlan (nativeC60AXNext L S) (N + 1))
    {G : Type v} [Group G] (weight : ∀ {x y}, S.Gen x y → G) :
    Nonempty (NativeC60AYFiniteDescentData
      (nativeC60AXNext L S) (N + 1) p
      (nativeC60AZInternalObserver S weight)) ↔
      (∀ {x y}, p.1.Gen x y →
        nativeC60AZHolonomy S weight x.2 =
          nativeC60AZHolonomy S weight y.2) := by
  rw [nativeC60AYFiniteDescentData_iff, nativeC60AYFinite_observer_iff]
  rfl

/-- A distinguished new generator with unequal internal holonomies
is a concrete obstruction: equal lower boundaries are NOT enough. -/
theorem nativeC60AZInternal_no_descent
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    {G : Type v} [Group G] (weight : ∀ {x y}, S.Gen x y → G)
    {x y : (nativeC60AXNext L S).Total} (g : T.Gen x y)
    (hne : nativeC60AZHolonomy S weight x.2 ≠
      nativeC60AZHolonomy S weight y.2) :
    ¬ ∃ f : Quotient (nativeC60AXSetoid T) → G,
      ∀ c, f (Quotient.mk (nativeC60AXSetoid T) c) =
        nativeC60AZInternalObserver S weight c := by
  intro hf
  have hs : ∀ {a b}, T.Gen a b →
      nativeC60AZHolonomy S weight a.2 =
        nativeC60AZHolonomy S weight b.2 :=
    (nativeC60AZInternalDescent_iff S T weight).mp hf
  exact hne (hs g)

/-- Assign a freely chosen value to each declared generator. The
choice is independent of the AX/AY inherited boundary and Peiffer. -/
def nativeC60AZConstantWeight
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {G : Type v} [Group G] (z : G) :
    ∀ {x y}, S.Gen x y → G :=
  fun {_ _} _ => z

theorem nativeC60AZAtom_weight_detects
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {G : Type v} [Group G] (z : G) (hz : z ≠ 1)
    {x y : L.Total} (g : S.Gen x y) :
    nativeC60AZHolonomy S (nativeC60AZConstantWeight S z) (.atom g) ≠
      nativeC60AZHolonomy S (nativeC60AZConstantWeight S 1) (.atom g) := by
  change z ≠ 1
  exact hz

section PhysicalC60

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- The ORIGINAL C60 Peiffer group is gauged at its TWO actual
fourteen-cell endpoints, while both boundaries are retained. -/
def nativeK5AZPhysicalGaugeInvariant (W : NativeK5StructuralThirteenCell p U V)
    (frame : (nativeK5AXBaseLayer W).Obj → NativeK5ASPeifferKernel W) :
    (nativeK5AXBaseLayer W).Total →
      ((nativeK5AXBaseLayer W).Obj × (nativeK5AXBaseLayer W).Obj) ×
        NativeK5ASPeifferKernel W :=
  fun c => (c.1, nativeC60AZGauge frame (nativeK5AXPeiffer W) c)

theorem nativeK5AZPhysicalGaugeInvariant_respects
    (W : NativeK5StructuralThirteenCell p U V)
    (frame : (nativeK5AXBaseLayer W).Obj → NativeK5ASPeifferKernel W) :
    NativeC60AYRespects (nativeK5AXKuuSignature W)
      (nativeK5AZPhysicalGaugeInvariant W frame) := by
  intro x y g
  apply Prod.ext ((nativeK5AXKuuSignature W).boundary g)
  exact (nativeC60AZGauge_respects_iff (nativeK5AXKuuSignature W)
    frame (nativeK5AXPeiffer W)).mpr
      (by
        intro a b h
        exact nativeK5AXPeiffer_step_sound W (.atom h)) g

/-- Preservation and actual quotient descent for EVERY finite AX
extension of the true source-dependent C60 data, with no invented
higher geometric cell. -/
theorem nativeK5AZFiniteGaugeSound
    (W : NativeK5StructuralThirteenCell p U V)
    (frame : (nativeK5AXBaseLayer W).Obj → NativeK5ASPeifferKernel W)
    (N : Nat) :
    NativeC60AYFiniteObserverSound (nativeK5AXBaseLayer W) N
      (nativeK5AXFiniteKuuPlan W N)
      (nativeK5AZPhysicalGaugeInvariant W frame) := by
  cases N with
  | zero => trivial
  | succ N =>
      exact (nativeC60AYFinite_observer_iff _ N
        (nativeK5AXFiniteKuuPlan W (N + 1))
        (nativeK5AZPhysicalGaugeInvariant W frame)).mpr
          (nativeK5AZPhysicalGaugeInvariant_respects W frame)

def nativeK5AZFiniteGaugeDescents
    (W : NativeK5StructuralThirteenCell p U V)
    (frame : (nativeK5AXBaseLayer W).Obj → NativeK5ASPeifferKernel W)
    (N : Nat) :
    NativeC60AYFiniteDescentData (nativeK5AXBaseLayer W) N
      (nativeK5AXFiniteKuuPlan W N)
      (nativeK5AZPhysicalGaugeInvariant W frame) :=
  nativeC60AYBuildFiniteDescents _ _ _ _ (nativeK5AZFiniteGaugeSound W frame N)

/-- Finite two-sided gauge covariance also holds for every actual C60
relative Kuu plan; subsequent signatures may be nonstructural. -/
theorem nativeK5AZFiniteHolonomyCovariant
    (W : NativeK5StructuralThirteenCell p U V)
    (N : Nat) (plan : NativeC60AXPlan (nativeK5AXBaseLayer W) N) :
    NativeC60AZAllFiniteCovariant (G := NativeK5ASPeifferKernel W)
      (nativeK5AXBaseLayer W) N plan :=
  nativeC60AZAllFiniteCovariant_sound _ _ _

/-- One actual AQ exchange has a DECLARED optional comparison with
a nontrivial free holonomy label. The label 1 gives a DIFFERENT
internal observable on the SAME raw higher term, even though both
induce the same inherited AY boundary data. This does NOT construct
an original geometric 16-cell. -/
theorem nativeK5AZPhysicalInternal_new_information
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeC60AZHolonomy (nativeK5AXKuuSignature W)
      (nativeC60AZConstantWeight (nativeK5AXKuuSignature W)
        (nativeK5ASPhysicalDefect W []))
      (nativeK5AXDeclaredNaturality W (nativeK5AQExchange W [])) ≠
    nativeC60AZHolonomy (nativeK5AXKuuSignature W)
      (nativeC60AZConstantWeight (nativeK5AXKuuSignature W) 1)
      (nativeK5AXDeclaredNaturality W (nativeK5AQExchange W [])) := by
  change nativeK5ASPhysicalDefect W [] ≠ 1
  exact nativeK5ASPhysicalDefect_base_ne_one W

end PhysicalC60

#print axioms nativeC60AZGauge
#print axioms nativeC60AZGauge_one
#print axioms nativeC60AZGauge_comp
#print axioms nativeC60AZGauge_map
#print axioms nativeC60AZGauge_respects_iff
#print axioms nativeC60AZHolonomy
#print axioms nativeC60AZHolonomy_atom
#print axioms nativeC60AZHolonomy_refl
#print axioms nativeC60AZHolonomy_symm
#print axioms nativeC60AZHolonomy_trans
#print axioms nativeC60AZGaugeWeight
#print axioms nativeC60AZHolonomy_covariant
#print axioms NativeC60AZAllFiniteCovariant
#print axioms nativeC60AZAllFiniteCovariant_sound
#print axioms nativeC60AZInternalObserver
#print axioms nativeC60AZInternalDescent_iff
#print axioms nativeC60AZInternalFiniteDescent_iff
#print axioms nativeC60AZInternal_no_descent
#print axioms nativeC60AZConstantWeight
#print axioms nativeC60AZAtom_weight_detects
#print axioms nativeK5AZPhysicalGaugeInvariant
#print axioms nativeK5AZPhysicalGaugeInvariant_respects
#print axioms nativeK5AZFiniteGaugeSound
#print axioms nativeK5AZFiniteGaugeDescents
#print axioms nativeK5AZFiniteHolonomyCovariant
#print axioms nativeK5AZPhysicalInternal_new_information

end
end Kuu.F112.Physical
