import Kuu.F112.PolygonNativeC60FiniteRelativeKuuExtension

/-!
# F112-P94D3AY — finite C60 observer descent and relative necessity

AX constructs finite dependent extensions on the original C60. Here the
original boundary and noncommutative Peiffer observation are carried through
ALL finitely many layers by explicit quotient maps. An inherited observation
is pulled along a cell's source boundary. Globularity preserves it under every
later declared comparison; compatibility at the FIRST layer is still necessary.

This is a theorem about inherited boundary observations, not arbitrary new
higher observables, higher holonomies, or universal geometric fillers.

At the actual AQ exchange, the packed AU naturality terms are distinct and
cannot be compared by the structural-only signature. The explicitly declared
Kuu comparison exists, but the raw discriminator does NOT descend through it.
Thus the original terms survive outside the quotient without pretending that
all raw observations survive a genuine change of presentation.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- Compatibility with exactly the declared generators. -/
def NativeC60AYRespects {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) {B : Type v} (obs : L.Total → B) : Prop :=
  ∀ {x y}, S.Gen x y → obs x = obs y

/-- Inherit the previous observer through the exact source boundary.
This is not a new observation of the internal higher proof syntax. -/
def nativeC60AYBoundaryObserver {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) {B : Type v} (obs : L.Total → B) :
    (nativeC60AXNext L S).Total → B :=
  fun c => obs c.1.1

/-- Every subsequent parallel-boundary declaration preserves an
inherited source observation, independently of its higher generators. -/
theorem nativeC60AYBoundaryObserver_respects
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    {B : Type v} (obs : L.Total → B) :
    NativeC60AYRespects T (nativeC60AYBoundaryObserver S obs) := by
  intro x y g
  exact congrArg (fun endpoints : L.Total × L.Total => obs endpoints.1) (T.boundary g)

/-- Compatibility at each of the finitely many constructed layers. -/
def NativeC60AYFiniteObserverSound {B : Type v} :
    (L : NativeC60AXLayer.{u}) → (N : Nat) → NativeC60AXPlan L N →
      (L.Total → B) → Prop
  | _, 0, _, _ => True
  | L, N + 1, p, obs => NativeC60AYRespects p.1 obs ∧
      NativeC60AYFiniteObserverSound (nativeC60AXNext L p.1) N p.2
        (nativeC60AYBoundaryObserver p.1 obs)

/-- One induction treats all finite continuations, including later
nonstructural signatures, for the inherited boundary observer. -/
theorem nativeC60AYFinite_boundary_observer_sound
    (L : NativeC60AXLayer.{u}) (S : NativeC60AXSignature L)
    (N : Nat) (p : NativeC60AXPlan (nativeC60AXNext L S) N)
    {B : Type v} (obs : L.Total → B) :
    NativeC60AYFiniteObserverSound (nativeC60AXNext L S) N p
      (nativeC60AYBoundaryObserver S obs) := by
  induction N generalizing L with
  | zero => trivial
  | succ N ih =>
      exact ⟨nativeC60AYBoundaryObserver_respects S p.1 obs,
        ih (nativeC60AXNext L S) p.1 p.2
          (nativeC60AYBoundaryObserver S obs)⟩

/-- The first compatibility obligation cannot be erased by raising
the finite height. Every later inherited obligation follows from globularity. -/
theorem nativeC60AYFinite_observer_iff
    (L : NativeC60AXLayer.{u}) (N : Nat) (p : NativeC60AXPlan L (N + 1))
    {B : Type v} (obs : L.Total → B) :
    NativeC60AYFiniteObserverSound L (N + 1) p obs ↔
      NativeC60AYRespects p.1 obs :=
  ⟨fun h => h.1,
    fun h => ⟨h, nativeC60AYFinite_boundary_observer_sound L p.1 N p.2 obs⟩⟩

/-- An actual quotient factorization, not just a preservation assertion. -/
def nativeC60AYObserverDescend
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {B : Type v} (obs : L.Total → B) (h : NativeC60AYRespects S obs) :
    Quotient (nativeC60AXSetoid S) → B :=
  Quotient.lift obs (by
    rintro x y ⟨c⟩
    exact c.observer_sound obs h)

theorem nativeC60AYObserverDescend_mk
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {B : Type v} (obs : L.Total → B) (h : NativeC60AYRespects S obs)
    (x : L.Total) :
    nativeC60AYObserverDescend S obs h (Quotient.mk (nativeC60AXSetoid S) x) =
      obs x := rfl

/-- The descended observer is unique on the specified quotient. -/
theorem nativeC60AYObserverDescend_unique
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {B : Type v} (obs : L.Total → B) (h : NativeC60AYRespects S obs)
    (f : Quotient (nativeC60AXSetoid S) → B)
    (hf : ∀ x, f (Quotient.mk (nativeC60AXSetoid S) x) = obs x) :
    f = nativeC60AYObserverDescend S obs h := by
  funext q
  refine Quotient.inductionOn q ?_
  intro x
  exact hf x

/-- Explicit factorization maps and their representative equations at
EVERY stage, over the actual dependent sequence of quotient types. -/
def NativeC60AYFiniteDescentData {B : Type v} :
    (L : NativeC60AXLayer.{u}) → (N : Nat) → NativeC60AXPlan L N →
      (L.Total → B) → Type (max u v)
  | _, 0, _, _ => PUnit
  | L, N + 1, p, obs =>
      {f : Quotient (nativeC60AXSetoid p.1) → B //
        ∀ x, f (Quotient.mk (nativeC60AXSetoid p.1) x) = obs x} ×
      NativeC60AYFiniteDescentData (nativeC60AXNext L p.1) N p.2
        (nativeC60AYBoundaryObserver p.1 obs)

/-- Construct all finitely many maps; no choice of hypothetical
higher fillers or previously unspecified descent maps is assumed. -/
def nativeC60AYBuildFiniteDescents {B : Type v} :
    (L : NativeC60AXLayer.{u}) → (N : Nat) → (p : NativeC60AXPlan L N) →
    (obs : L.Total → B) → NativeC60AYFiniteObserverSound L N p obs →
      NativeC60AYFiniteDescentData L N p obs
  | _, 0, _, _, _ => PUnit.unit
  | L, N + 1, p, obs, h =>
      ⟨⟨nativeC60AYObserverDescend p.1 obs h.1, fun _ => rfl⟩,
        nativeC60AYBuildFiniteDescents (nativeC60AXNext L p.1) N p.2
          (nativeC60AYBoundaryObserver p.1 obs) h.2⟩

/-- Conversely, actual finite descent data enforces every required
compatibility, so the construction is an exact criterion. -/
theorem nativeC60AYFiniteDescents_sound
    (L : NativeC60AXLayer.{u}) (N : Nat) (p : NativeC60AXPlan L N)
    {B : Type v} (obs : L.Total → B)
    (d : NativeC60AYFiniteDescentData L N p obs) :
    NativeC60AYFiniteObserverSound L N p obs := by
  induction N generalizing L with
  | zero => trivial
  | succ N ih =>
      exact ⟨(nativeC60AXDescent_iff p.1 obs).mp ⟨d.1.1, d.1.2⟩,
        ih (nativeC60AXNext L p.1) p.2
          (nativeC60AYBoundaryObserver p.1 obs) d.2⟩

theorem nativeC60AYFiniteDescentData_iff
    (L : NativeC60AXLayer.{u}) (N : Nat) (p : NativeC60AXPlan L N)
    {B : Type v} (obs : L.Total → B) :
    Nonempty (NativeC60AYFiniteDescentData L N p obs) ↔
      NativeC60AYFiniteObserverSound L N p obs := by
  constructor
  · rintro ⟨d⟩
    exact nativeC60AYFiniteDescents_sound L N p obs d
  · intro h
    exact ⟨nativeC60AYBuildFiniteDescents L N p obs h⟩

section C60Physical

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

/-- Retain the original two C60 endpoints AND the original Peiffer value.
No abelianization and no reconstruction of proof syntax from its shadow. -/
def nativeK5AYInvariant (W : NativeK5StructuralThirteenCell p U V)
    (c : (nativeK5AXBaseLayer W).Total) :=
  (c.1, nativeK5AXPeiffer W c)

theorem nativeK5AYInvariant_respects (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60AYRespects (nativeK5AXKuuSignature W) (nativeK5AYInvariant W) := by
  intro x y g
  exact Prod.ext ((nativeK5AXKuuSignature W).boundary g)
    (nativeK5AXPeiffer_step_sound W (NativeC60AXStep.atom g))

/-- Every finite AX family retains the combined physical invariant. -/
theorem nativeK5AYFiniteInvariantSound
    (W : NativeK5StructuralThirteenCell p U V) (N : Nat) :
    NativeC60AYFiniteObserverSound (nativeK5AXBaseLayer W) N
      (nativeK5AXFiniteKuuPlan W N) (nativeK5AYInvariant W) := by
  cases N with
  | zero => trivial
  | succ N =>
      exact (nativeC60AYFinite_observer_iff (nativeK5AXBaseLayer W) N
        (nativeK5AXFiniteKuuPlan W (N + 1)) (nativeK5AYInvariant W)).mpr
          (nativeK5AYInvariant_respects W)

/-- Actual finite quotient maps on the original C60-rooted AX family. -/
def nativeK5AYFiniteDescents (W : NativeK5StructuralThirteenCell p U V) (N : Nat) :
    NativeC60AYFiniteDescentData (nativeK5AXBaseLayer W) N
      (nativeK5AXFiniteKuuPlan W N) (nativeK5AYInvariant W) :=
  nativeC60AYBuildFiniteDescents _ _ _ _ (nativeK5AYFiniteInvariantSound W N)

/-- Later optional comparisons need not be structural-only: any
explicit finite continuation preserves this inherited C60 observation. -/
theorem nativeK5AYAnyFiniteContinuationSound
    (W : NativeK5StructuralThirteenCell p U V) (N : Nat)
    (tail : NativeC60AXPlan
      (nativeC60AXNext (nativeK5AXBaseLayer W) (nativeK5AXKuuSignature W)) N) :
    NativeC60AYFiniteObserverSound (nativeK5AXBaseLayer W) (N + 1)
      ⟨nativeK5AXKuuSignature W, tail⟩ (nativeK5AYInvariant W) :=
  ⟨nativeK5AYInvariant_respects W,
    nativeC60AYFinite_boundary_observer_sound _ _ N tail (nativeK5AYInvariant W)⟩

def nativeK5AYAnyFiniteContinuationDescents
    (W : NativeK5StructuralThirteenCell p U V) (N : Nat)
    (tail : NativeC60AXPlan
      (nativeC60AXNext (nativeK5AXBaseLayer W) (nativeK5AXKuuSignature W)) N) :
    NativeC60AYFiniteDescentData (nativeK5AXBaseLayer W) (N + 1)
      ⟨nativeK5AXKuuSignature W, tail⟩ (nativeK5AYInvariant W) :=
  nativeC60AYBuildFiniteDescents _ _ _ _
    (nativeK5AYAnyFiniteContinuationSound W N tail)

/-- A raw syntactic observer, deliberately NOT quotient-invariant. -/
def nativeK5AYRawLeading (W : NativeK5StructuralThirteenCell p U V)
    (c : (nativeK5AXBaseLayer W).Total) : Bool :=
  nativeK5AXLeadingConservative W c.2.down

/-- Packing dependent endpoints does not erase the distinction
between the two genuine AU naturality terms at the AQ exchange. -/
theorem nativeK5AYPackedNaturality_ne (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5AXPack W (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])) ≠
      nativeK5AXPack W (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])) := by
  intro h
  have ht := congrArg (nativeK5AYRawLeading W) h
  change true = false at ht
  cases ht

/-- No structural-only comparison exists for this actual C60 pair.
This is relative to that signature, not a geometric no-go theorem. -/
theorem nativeK5AYNoStructuralNaturality (W : NativeK5StructuralThirteenCell p U V) :
    ¬ Nonempty (NativeC60AXStep
      (nativeC60AXStructuralSignature (nativeK5AXBaseLayer W))
      (nativeK5AXPack W (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))
      (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])))) := by
  rintro ⟨c⟩
  exact nativeK5AYPackedNaturality_ne W
    (nativeC60AXStructural_reflects (nativeK5AXBaseLayer W) c)

/-- The selected relative Kuu presentation supplies the comparison
that the structural-only presentation lacks. It need not be the only
possible choice of a nonstructural extension. -/
theorem nativeK5AYRelativeNaturalityContrast
    (W : NativeK5StructuralThirteenCell p U V) :
    (¬ Nonempty (NativeC60AXStep
      (nativeC60AXStructuralSignature (nativeK5AXBaseLayer W))
      (nativeK5AXPack W (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))
      (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))))) ∧
    Nonempty (NativeC60AXStep (nativeK5AXKuuSignature W)
      (nativeK5AXPack W (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))
      (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])))) :=
  ⟨nativeK5AYNoStructuralNaturality W,
    ⟨nativeK5AXDeclaredNaturality W (nativeK5AQExchange W [])⟩⟩

/-- Unlike the physical boundary/Peiffer invariant, the raw syntax
discriminator cannot descend through the declared Kuu comparison. -/
theorem nativeK5AYRaw_no_descent (W : NativeK5StructuralThirteenCell p U V) :
    ¬ (∃ f : Quotient (nativeC60AXSetoid (nativeK5AXKuuSignature W)) → Bool,
      ∀ x, f (Quotient.mk (nativeC60AXSetoid (nativeK5AXKuuSignature W)) x) =
        nativeK5AYRawLeading W x) := by
  intro hf
  -- Give the local theorem its full binder: with `have hs :=`, Lean
  -- keeps the implicit endpoints as metavariables instead of treating
  -- them as the universally quantified variables of `NativeC60AYRespects`.
  have hs : NativeC60AYRespects (nativeK5AXKuuSignature W)
      (nativeK5AYRawLeading W) :=
    (nativeC60AXDescent_iff (nativeK5AXKuuSignature W)
      (nativeK5AYRawLeading W)).mp hf
  have ht := (nativeK5AXDeclaredNaturality W (nativeK5AQExchange W [])).observer_sound
    (nativeK5AYRawLeading W) hs
  change true = false at ht
  cases ht

end C60Physical

section GenuineFiveStage

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- Finite descent maps at the actual five-stage C60 boundary. -/
def nativeC60AYFiveStageFiniteDescents (N : Nat) :=
  nativeK5AYFiniteDescents
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5) N

/-- Structural necessity also specializes to the actual five-stage
boundary, rather than only to an unrelated abstract layer. -/
theorem nativeC60AYFiveStageNoStructuralNaturality :
    let W := nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5
    ¬ Nonempty (NativeC60AXStep
      (nativeC60AXStructuralSignature (nativeK5AXBaseLayer W))
      (nativeK5AXPack W (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))
      (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])))) :=
  nativeK5AYNoStructuralNaturality
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

end GenuineFiveStage

#print axioms NativeC60AYRespects
#print axioms nativeC60AYBoundaryObserver
#print axioms nativeC60AYBoundaryObserver_respects
#print axioms NativeC60AYFiniteObserverSound
#print axioms nativeC60AYFinite_boundary_observer_sound
#print axioms nativeC60AYFinite_observer_iff
#print axioms nativeC60AYObserverDescend
#print axioms nativeC60AYObserverDescend_mk
#print axioms nativeC60AYObserverDescend_unique
#print axioms NativeC60AYFiniteDescentData
#print axioms nativeC60AYBuildFiniteDescents
#print axioms nativeC60AYFiniteDescents_sound
#print axioms nativeC60AYFiniteDescentData_iff
#print axioms nativeK5AYInvariant
#print axioms nativeK5AYInvariant_respects
#print axioms nativeK5AYFiniteInvariantSound
#print axioms nativeK5AYFiniteDescents
#print axioms nativeK5AYAnyFiniteContinuationSound
#print axioms nativeK5AYAnyFiniteContinuationDescents
#print axioms nativeK5AYRawLeading
#print axioms nativeK5AYPackedNaturality_ne
#print axioms nativeK5AYNoStructuralNaturality
#print axioms nativeK5AYRelativeNaturalityContrast
#print axioms nativeK5AYRaw_no_descent
#print axioms nativeC60AYFiveStageFiniteDescents
#print axioms nativeC60AYFiveStageNoStructuralNaturality

end
end Kuu.F112.Physical
