import Kuu.F112.PolygonNativeF55P94DFiniteCoherenceObstruction
import Mathlib.Tactic

/-!
# F112-P94D3AX — finite relative extensions rooted in the original C60

The root is the actual C60 dependent 14-cell fiber and AQ Type-valued
15-cell syntax, not an arbitrary empty-higher countermodel. A finite
DEPENDENT sequence of declared signatures constructs successive layers.
Each new cell compares cells of the previous layer, and every primitive
must have exactly matching lower boundaries. Thus the natural-number
index counts successive cell dimensions, not conservative closure depth.

Kuu is used only as an OPTIONAL, explicitly declared presentation change:
AU's two naturality proofs at the physical exchange are syntactically
DISTINCT. One may adjoin their comparison, preserving the actual C60
boundary and the noncommutative Peiffer observation. This is a relative
presentation extension, NOT a proof that the old geometric 16-cell
already exists. Kuu is not PEmpty, not a new C60 vertex, and not a unique
presentation of emptiness. All raw proofs and prior obstructions survive.

The finite plan adds only the declared primitives, identity, reversal
and composition. It does not automatically fill all parallel boundaries,
assert strict n-category laws, or establish hyperdescent.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- One layer with proof-relevant cells over exact lower endpoints. -/
structure NativeC60AXLayer where
  Obj : Type u
  Hom : Obj → Obj → Type u

/-- All cells, still storing their two lower endpoints. -/
def NativeC60AXLayer.Total (L : NativeC60AXLayer.{u}) : Type u :=
  Σ endpoints : L.Obj × L.Obj, L.Hom endpoints.1 endpoints.2

/-- Only declared comparisons may be primitive. Their two lower
boundaries must agree, independently of any group-valued observation. -/
structure NativeC60AXSignature (L : NativeC60AXLayer.{u}) where
  Gen : L.Total → L.Total → Type u
  boundary : ∀ {x y}, Gen x y → x.1 = y.1

/-- Free Type-valued comparison SYNTAX over the declared primitives.
No groupoid laws are imposed as equalities between these proof terms. -/
inductive NativeC60AXStep {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) : L.Total → L.Total → Type u where
  | atom {x y} (g : S.Gen x y) : NativeC60AXStep S x y
  | refl (x) : NativeC60AXStep S x x
  | symm {x y} (h : NativeC60AXStep S x y) : NativeC60AXStep S y x
  | trans {x y z} (h : NativeC60AXStep S x y)
      (k : NativeC60AXStep S y z) : NativeC60AXStep S x z

/-- Every generated cell is globular, by induction on its actual
syntax, not because its numerical or group-valued shadows coincide. -/
theorem NativeC60AXStep.boundary
    {L : NativeC60AXLayer.{u}} {S : NativeC60AXSignature L}
    {x y : L.Total} (h : NativeC60AXStep S x y) : x.1 = y.1 := by
  induction h with
  | atom g => exact S.boundary g
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih ik => exact ih.trans ik

theorem NativeC60AXStep.globular
    {L : NativeC60AXLayer.{u}} {S : NativeC60AXSignature L}
    {x y : L.Total} (h : NativeC60AXStep S x y) :
    x.1.1 = y.1.1 ∧ x.1.2 = y.1.2 :=
  ⟨congrArg Prod.fst h.boundary, congrArg Prod.snd h.boundary⟩

/-- The next layer is CONSTRUCTED; its higher cells are not an
unspecified field of a hypothetical complete tower. -/
def nativeC60AXNext (L : NativeC60AXLayer.{u})
    (S : NativeC60AXSignature L) : NativeC60AXLayer.{u} where
  Obj := L.Total
  Hom := NativeC60AXStep S

/-- The universal evaluator for the free comparison syntax into any
Type-valued receiver with the same four operations. -/
def NativeC60AXStep.fold
    {L : NativeC60AXLayer.{u}} {S : NativeC60AXSignature L}
    {K : L.Total → L.Total → Type v}
    (gen : ∀ {x y}, S.Gen x y → K x y)
    (ident : ∀ x, K x x)
    (inverse : ∀ {x y}, K x y → K y x)
    (compose : ∀ {x y z}, K x y → K y z → K x z)
    {x y : L.Total} : NativeC60AXStep S x y → K x y
  | .atom g => gen g
  | .refl a => ident a
  | .symm h => inverse (h.fold gen ident inverse compose)
  | .trans h k => compose (h.fold gen ident inverse compose)
      (k.fold gen ident inverse compose)

/-- Preserving the declared generators suffices for preserving every
finite composition and reversal, without erasing proof-relevant cells. -/
theorem NativeC60AXStep.observer_sound
    {L : NativeC60AXLayer.{u}} {S : NativeC60AXSignature L}
    {B : Type v} (obs : L.Total → B)
    (hgen : ∀ {x y}, S.Gen x y → obs x = obs y)
    {x y : L.Total} (h : NativeC60AXStep S x y) : obs x = obs y := by
  induction h with
  | atom g => exact hgen g
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih ik => exact ih.trans ik

/-- A relative Kuu quotient: generated replacement, not universal
identification of all parallel or equal-shadow proof terms. -/
def nativeC60AXSetoid {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) : Setoid L.Total where
  r := fun x y => Nonempty (NativeC60AXStep S x y)
  iseqv := ⟨fun x => ⟨.refl x⟩,
    fun h => h.elim (fun c => ⟨.symm c⟩),
    fun h k => h.elim (fun c => k.elim (fun d => ⟨.trans c d⟩))⟩

/-- Exact descent criterion for the DECLARED signature. -/
theorem nativeC60AXDescent_iff
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {B : Type v} (obs : L.Total → B) :
    (∃ f : Quotient (nativeC60AXSetoid S) → B,
      ∀ x, f (Quotient.mk (nativeC60AXSetoid S) x) = obs x) ↔
    (∀ {x y}, S.Gen x y → obs x = obs y) := by
  constructor
  · rintro ⟨f, hf⟩ x y g
    calc
      obs x = f (Quotient.mk (nativeC60AXSetoid S) x) := (hf x).symm
      _ = f (Quotient.mk (nativeC60AXSetoid S) y) :=
        congrArg f (Quotient.sound ⟨NativeC60AXStep.atom g⟩)
      _ = obs y := hf y
  · intro hg
    refine ⟨Quotient.lift obs ?_, ?_⟩
    · rintro x y ⟨c⟩
      exact c.observer_sound obs hg
    · intro x
      rfl

/-- Source and target jointly descend, with no loss of lower
boundary information through the optional presentation change. -/
def nativeC60AXBoundaryDescend {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) :
    Quotient (nativeC60AXSetoid S) → L.Obj × L.Obj :=
  Quotient.lift (fun x => x.1) (by
    rintro x y ⟨c⟩
    exact c.boundary)

theorem nativeC60AXBoundaryDescend_mk {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (x : L.Total) :
    nativeC60AXBoundaryDescend S (Quotient.mk (nativeC60AXSetoid S) x) =
      x.1 := rfl

/-- Choosing no additional primitives still permits structural
identity/reversal/composition. This is NOT the meaning of Kuu. -/
def nativeC60AXStructuralSignature (L : NativeC60AXLayer.{u}) :
    NativeC60AXSignature L where
  Gen := fun _ _ => PEmpty
  boundary := fun g => g.elim

/-- In the absence of new primitives, distinct previous cells are
not identified merely because they are parallel or share an observer. -/
theorem nativeC60AXStructural_reflects
    (L : NativeC60AXLayer.{u}) {x y : L.Total}
    (c : NativeC60AXStep (nativeC60AXStructuralSignature L) x y) : x = y := by
  exact c.observer_sound id (by intro x y g; exact g.elim)

/-- A finite DEPENDENT plan: each next signature is specified over
exactly the layer constructed at the preceding step. -/
def NativeC60AXPlan (L : NativeC60AXLayer.{u}) : Nat → Type (u + 1)
  | 0 => PUnit
  | n + 1 => Σ S : NativeC60AXSignature L,
      NativeC60AXPlan (nativeC60AXNext L S) n

/-- All finite structural extensions exist constructively, while
nonstructural comparisons remain explicit optional input. -/
def nativeC60AXStructuralPlan (L : NativeC60AXLayer.{u}) :
    (n : Nat) → NativeC60AXPlan L n
  | 0 => PUnit.unit
  | n + 1 => ⟨nativeC60AXStructuralSignature L,
      nativeC60AXStructuralPlan
        (nativeC60AXNext L (nativeC60AXStructuralSignature L)) n⟩

/-- The final constructed layer at any FINITE depth. -/
def nativeC60AXTop : (L : NativeC60AXLayer.{u}) → (n : Nat) →
    NativeC60AXPlan L n → NativeC60AXLayer.{u}
  | L, 0, _ => L
  | L, n + 1, p => nativeC60AXTop (nativeC60AXNext L p.1) n p.2

/-- Exact globular boundary preservation required at every step of
the finite dependent plan, not just its first higher dimension. -/
def NativeC60AXPlan.BoundarySound :
    (L : NativeC60AXLayer.{u}) → (n : Nat) → NativeC60AXPlan L n → Prop
  | _, 0, _ => True
  | L, n + 1, p =>
      (∀ {x y : L.Total}, NativeC60AXStep p.1 x y → x.1 = y.1) ∧
      NativeC60AXPlan.BoundarySound (nativeC60AXNext L p.1) n p.2

/-- ONE induction proves globularity for every finite height and
for every explicitly supplied sequence of compatible signatures. -/
theorem nativeC60AXFinite_boundary_sound
    (L : NativeC60AXLayer.{u}) (n : Nat) (p : NativeC60AXPlan L n) :
    NativeC60AXPlan.BoundarySound L n p := by
  induction n generalizing L with
  | zero => trivial
  | succ n ih => exact ⟨fun c => c.boundary, ih _ p.2⟩

/-- Universe bookkeeping preserves all original objects and proofs. -/
def nativeC60AXLayerOf (A : Type u) (Edge : A → A → Type v) :
    NativeC60AXLayer.{max u v} where
  Obj := ULift.{v} A
  Hom := fun x y => ULift.{u} (Edge x.down y.down)

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

/-- The ONLY root used by the physical finite construction: the
original C60 14-cell fiber over W and its actual AQ 15-cell grammar. -/
def nativeK5AXBaseLayer (W : NativeK5StructuralThirteenCell p U V) :=
  nativeC60AXLayerOf (NativeK5FifteenFourteenFiber W) (NativeK5AQFifteenCell W)

/-- Pack an existing proof, keeping both exact original endpoints. -/
def nativeK5AXPack (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} (c : NativeK5AQFifteenCell W R S) :
    (nativeK5AXBaseLayer W).Total :=
  ⟨(ULift.up R, ULift.up S), ULift.up c⟩

/-- A syntactic test, NOT a scalar observer defining equivalence. -/
def nativeK5AXLeadingConservative (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} : NativeK5AQFifteenCell W R S → Bool
  | .trans (.conservative _) _ => true
  | _ => false

/-- At the actual C60 exchange, AU's two naturality proofs really
are distinct raw 15-cell terms. Peiffer equality does not equate them. -/
theorem nativeK5AXNaturality_raw_ne (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5AUNaturalityViaSource W (nativeK5AQExchange W []) ≠
      nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []) := by
  intro h
  have ht := congrArg (nativeK5AXLeadingConservative W) h
  change true = false at ht
  cases ht

/-- OPTIONAL Kuu-compatible declaration: compare only the named AU
naturality boundaries, not every parallel pair and not every equal
Peiffer shadow. This independently extends the presentation. -/
def nativeK5AXKuuSignature (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60AXSignature (nativeK5AXBaseLayer W) where
  Gen := fun x y => Σ R : NativeK5FifteenFourteenFiber W,
    Σ S : NativeK5FifteenFourteenFiber W,
      {c : NativeK5AQFifteenCell W R S //
        x = nativeK5AXPack W (nativeK5AUNaturalityViaSource W c) ∧
        y = nativeK5AXPack W (nativeK5AUNaturalityViaTarget W c)}
  boundary := by
    intro x y g
    rcases g with ⟨R, S, c, hx, hy⟩
    rw [hx, hy]
    rfl

/-- The comparison EXISTS in the explicitly extended presentation,
not automatically as an original geometric C60 16-cell. -/
def nativeK5AXDeclaredNaturality (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} (c : NativeK5AQFifteenCell W R S) :
    NativeC60AXStep (nativeK5AXKuuSignature W)
      (nativeK5AXPack W (nativeK5AUNaturalityViaSource W c))
      (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W c)) :=
  .atom ⟨R, S, c, rfl, rfl⟩

/-- All original lower C60 endpoints are retained by the optional
relative comparison, independently of observations or quotienting. -/
theorem nativeK5AXDeclaredNaturality_boundary
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} (c : NativeK5AQFifteenCell W R S) :
    (nativeK5AXPack W (nativeK5AUNaturalityViaSource W c)).1 =
      (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W c)).1 :=
  (nativeK5AXDeclaredNaturality W c).boundary

/-- The original noncommutative Peiffer observation is read from
actual proof terms; the raw syntax is not reconstructed from it. -/
def nativeK5AXPeiffer (W : NativeK5StructuralThirteenCell p U V) :
    (nativeK5AXBaseLayer W).Total → NativeK5ASPeifferKernel W :=
  fun c => nativeK5ATCellDefect W c.2.down

/-- The declared Kuu comparisons preserve Peiffer, as do ALL of
 their finite compositions and reversals. No abelianization is used. -/
theorem nativeK5AXPeiffer_step_sound
    (W : NativeK5StructuralThirteenCell p U V)
    {x y : (nativeK5AXBaseLayer W).Total}
    (c : NativeC60AXStep (nativeK5AXKuuSignature W) x y) :
    nativeK5AXPeiffer W x = nativeK5AXPeiffer W y := by
  apply c.observer_sound (nativeK5AXPeiffer W)
  intro x y g
  rcases g with ⟨R, S, cell, hx, hy⟩
  rw [hx, hy]
  exact nativeK5AUNaturality_defect_eq W cell

/-- Peiffer descends through this PARTICULAR optional Kuu quotient;
it does not authorize arbitrary further identifications. -/
def nativeK5AXPeifferDescend (W : NativeK5StructuralThirteenCell p U V) :
    Quotient (nativeC60AXSetoid (nativeK5AXKuuSignature W)) →
      NativeK5ASPeifferKernel W :=
  Quotient.lift (nativeK5AXPeiffer W) (by
    rintro x y ⟨c⟩
    exact nativeK5AXPeiffer_step_sound W c)

/-- A family for EVERY finite height. At height zero the original
C60 14D/15D base is unchanged. At positive height the optional first
comparison is named explicitly; later layers add only structural
syntax, unless a different dependent plan is explicitly supplied. -/
def nativeK5AXFiniteKuuPlan (W : NativeK5StructuralThirteenCell p U V) :
    (N : Nat) → NativeC60AXPlan (nativeK5AXBaseLayer W) N
  | 0 => PUnit.unit
  | N + 1 => ⟨nativeK5AXKuuSignature W,
      nativeC60AXStructuralPlan
        (nativeC60AXNext (nativeK5AXBaseLayer W) (nativeK5AXKuuSignature W)) N⟩

/-- The concrete C60-rooted family has exact lower-boundary
compatibility in every one of its finitely many constructed layers. -/
theorem nativeK5AXFiniteKuuPlan_globular
    (W : NativeK5StructuralThirteenCell p U V) (N : Nat) :
    NativeC60AXPlan.BoundarySound (nativeK5AXBaseLayer W) N
      (nativeK5AXFiniteKuuPlan W N) :=
  nativeC60AXFinite_boundary_sound _ _ _

/-- The structural-only alternative remains available; Kuu's
optional new comparison is not forced on every presentation. -/
def nativeK5AXFiniteStructuralPlan (W : NativeK5StructuralThirteenCell p U V)
    (N : Nat) : NativeC60AXPlan (nativeK5AXBaseLayer W) N :=
  nativeC60AXStructuralPlan _ N

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

/-- Explicit finite family on the genuine five-stage C60 K5 data,
not on a replacement abstract world or graph. -/
def nativeC60AXFiveStageFinitePlan (N : Nat) :=
  nativeK5AXFiniteKuuPlan
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5) N

/-- The constructed family preserves the actual dependent boundaries
for every finite N at the genuine C60 five-stage instance. -/
theorem nativeC60AXFiveStageFinitePlan_globular (N : Nat) :
    NativeC60AXPlan.BoundarySound
      (nativeK5AXBaseLayer
        (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)) N
      (nativeC60AXFiveStageFinitePlan t1 t2 t3 t4 t5 N) :=
  nativeK5AXFiniteKuuPlan_globular _ N

end GenuineFiveStage

#print axioms NativeC60AXLayer
#print axioms NativeC60AXLayer.Total
#print axioms NativeC60AXSignature
#print axioms NativeC60AXStep
#print axioms NativeC60AXStep.boundary
#print axioms NativeC60AXStep.globular
#print axioms nativeC60AXNext
#print axioms NativeC60AXStep.fold
#print axioms NativeC60AXStep.observer_sound
#print axioms nativeC60AXSetoid
#print axioms nativeC60AXDescent_iff
#print axioms nativeC60AXBoundaryDescend
#print axioms nativeC60AXBoundaryDescend_mk
#print axioms nativeC60AXStructuralSignature
#print axioms nativeC60AXStructural_reflects
#print axioms NativeC60AXPlan
#print axioms nativeC60AXStructuralPlan
#print axioms nativeC60AXTop
#print axioms NativeC60AXPlan.BoundarySound
#print axioms nativeC60AXFinite_boundary_sound
#print axioms nativeC60AXLayerOf
#print axioms nativeK5AXBaseLayer
#print axioms nativeK5AXPack
#print axioms nativeK5AXLeadingConservative
#print axioms nativeK5AXNaturality_raw_ne
#print axioms nativeK5AXKuuSignature
#print axioms nativeK5AXDeclaredNaturality
#print axioms nativeK5AXDeclaredNaturality_boundary
#print axioms nativeK5AXPeiffer
#print axioms nativeK5AXPeiffer_step_sound
#print axioms nativeK5AXPeifferDescend
#print axioms nativeK5AXFiniteKuuPlan
#print axioms nativeK5AXFiniteKuuPlan_globular
#print axioms nativeK5AXFiniteStructuralPlan
#print axioms nativeC60AXFiveStageFinitePlan
#print axioms nativeC60AXFiveStageFinitePlan_globular

end
end Kuu.F112.Physical
