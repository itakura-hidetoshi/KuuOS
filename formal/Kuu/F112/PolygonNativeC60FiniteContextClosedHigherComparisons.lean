import Kuu.F112.PolygonNativeC60FiniteStrictHorizontalPeiffer

/-!
# F112-P94D3BC — genuine C60 context-closed typed higher comparisons

AQ supplies ACTUAL dependent 14D left/right whiskerings and transports
ACTUAL 15D evidence; AT proves their ordered noncommutative Peiffer action;
AU constructs the still-distinct 15D naturality routes; AX supplies their
optional 16D comparison. This file transports the latter to arbitrary finite
C60 contexts by a minimally adjoined, explicitly context-closed signature.

The closure contains ONLY transported declared generators, and their free
reversal/composition; it does not equate all parallel cells or equal-shadow
proofs. Its finite context action is constructed on Type-valued AX syntax.
Peiffer remains invariant under all such contextual generators, by the
ORIGINAL AT conjugation law, and hence descends through every finite tail.

No universal geometric 16-cell, full horizontal bicategory, global strict
3/n-category, Gray reintroduction, new logical axioms or sorry/admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- A genuine endpoint-dependent operation on LOWER cells, not a mere map of
the homology/Peiffer shadow. -/
structure NativeC60BCFrame (L : NativeC60AXLayer.{u}) where
  onObj : L.Obj → L.Obj
  onCell : ∀ {a b : L.Obj}, L.Hom a b → L.Hom (onObj a) (onObj b)

def NativeC60BCFrame.mapTotal {L : NativeC60AXLayer.{u}}
    (C : NativeC60BCFrame L) : L.Total → L.Total
  | ⟨(a, b), c⟩ => ⟨(C.onObj a, C.onObj b), C.onCell c⟩

/-- The head context acts OUTERMOST, as in the genuine AQ definition. -/
def nativeC60BCContextTotal {L : NativeC60AXLayer.{u}}
    (F : Bool → NativeC60BCFrame L) : List Bool → L.Total → L.Total
  | [], x => x
  | side :: rest, x =>
      (F side).mapTotal (nativeC60BCContextTotal F rest x)

theorem nativeC60BCContextTotal_append {L : NativeC60AXLayer.{u}}
    (F : Bool → NativeC60BCFrame L)
    (xs ys : List Bool) (x : L.Total) :
    nativeC60BCContextTotal F (xs ++ ys) x =
      nativeC60BCContextTotal F xs (nativeC60BCContextTotal F ys x) := by
  induction xs with
  | nil => rfl
  | cons side rest ih =>
      exact congrArg (NativeC60BCFrame.mapTotal (F side)) ih

theorem nativeC60BCContextTotal_boundary {L : NativeC60AXLayer.{u}}
    (F : Bool → NativeC60BCFrame L)
    (steps : List Bool) {x y : L.Total} (h : x.1 = y.1) :
    (nativeC60BCContextTotal F steps x).1 =
      (nativeC60BCContextTotal F steps y).1 := by
  induction steps with
  | nil => exact h
  | cons side rest ih =>
      exact congrArg
        (fun z : L.Obj × L.Obj =>
          ((F side).onObj z.1, (F side).onObj z.2)) ih

/-- The only new higher primitives are contextual images of an ACTUAL
selected AX generator, with BOTH original endpoint equalities carried. -/
def nativeC60BCClosedSignature {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AXSignature L where
  Gen := fun x y =>
    Σ steps : List Bool, Σ a : L.Total, Σ b : L.Total,
      {g : S.Gen a b //
        x = nativeC60BCContextTotal F steps a ∧
        y = nativeC60BCContextTotal F steps b}
  boundary := by
    intro x y gen
    rcases gen with ⟨steps, a, b, ⟨g, hx, hy⟩⟩
    rw [hx, hy]
    exact nativeC60BCContextTotal_boundary F steps (S.boundary g)

/-- Inject the ORIGINAL declared primitive, after any ACTUAL typed context. -/
def nativeC60BCGen {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (steps : List Bool) {a b : L.Total} (g : S.Gen a b) :
    (nativeC60BCClosedSignature S F).Gen
      (nativeC60BCContextTotal F steps a) (nativeC60BCContextTotal F steps b) :=
  ⟨steps, a, b, ⟨g, rfl, rfl⟩⟩

/-- The signature is CLOSED under every further finite context, rather
than adding a separate dimension or separately chosen generator each time. -/
def nativeC60BCShiftGen {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (outer : List Bool) {x y : L.Total}
    (gen : (nativeC60BCClosedSignature S F).Gen x y) :
    (nativeC60BCClosedSignature S F).Gen
      (nativeC60BCContextTotal F outer x)
      (nativeC60BCContextTotal F outer y) := by
  rcases gen with ⟨inner, a, b, ⟨g, hx, hy⟩⟩
  refine ⟨outer ++ inner, a, b, ⟨g, ?_, ?_⟩⟩
  · calc
      nativeC60BCContextTotal F outer x =
          nativeC60BCContextTotal F outer (nativeC60BCContextTotal F inner a) :=
        congrArg (nativeC60BCContextTotal F outer) hx
      _ = nativeC60BCContextTotal F (outer ++ inner) a :=
        (nativeC60BCContextTotal_append F outer inner a).symm
  · calc
      nativeC60BCContextTotal F outer y =
          nativeC60BCContextTotal F outer (nativeC60BCContextTotal F inner b) :=
        congrArg (nativeC60BCContextTotal F outer) hy
      _ = nativeC60BCContextTotal F (outer ++ inner) b :=
        (nativeC60BCContextTotal_append F outer inner b).symm

/-- Transport every actual original AX Type-valued comparison through a
finite C60 context, INTO the independent context-closed 16D presentation. -/
def nativeC60BCMapOriginalStep {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (steps : List Bool) {a b : L.Total}
    (c : NativeC60AXStep S a b) :
    NativeC60AXStep (nativeC60BCClosedSignature S F)
      (nativeC60BCContextTotal F steps a)
      (nativeC60BCContextTotal F steps b) :=
  c.fold
    (K := fun x y => NativeC60AXStep (nativeC60BCClosedSignature S F)
      (nativeC60BCContextTotal F steps x)
      (nativeC60BCContextTotal F steps y))
    (fun {_ _} g => .atom (nativeC60BCGen S F steps g))
    (fun _ => .refl _)
    (fun c => .symm c)
    (fun c d => .trans c d)

/-- The same construction is an ACTION on the NEW closed 16D proof grammar:
the additional generators already contain their required context index. -/
def nativeC60BCMapClosedStep {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (steps : List Bool) {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    NativeC60AXStep (nativeC60BCClosedSignature S F)
      (nativeC60BCContextTotal F steps a)
      (nativeC60BCContextTotal F steps b) :=
  c.fold
    (K := fun x y => NativeC60AXStep (nativeC60BCClosedSignature S F)
      (nativeC60BCContextTotal F steps x)
      (nativeC60BCContextTotal F steps y))
    (fun {_ _} g => .atom (nativeC60BCShiftGen S F steps g))
    (fun _ => .refl _)
    (fun c => .symm c)
    (fun c d => .trans c d)

/-- Finite 16D context whiskering is strictly compositional at the FREE
proof-language level, without inventing a geometric Peiffer filler. -/
theorem nativeC60BCMapClosedStep_trans {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (steps : List Bool) {a b c : L.Total}
    (h : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (k : NativeC60AXStep (nativeC60BCClosedSignature S F) b c) :
    nativeC60BCMapClosedStep S F steps (.trans h k) =
      .trans (nativeC60BCMapClosedStep S F steps h)
        (nativeC60BCMapClosedStep S F steps k) := rfl

theorem nativeC60BCMapClosedStep_symm {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (steps : List Bool) {a b : L.Total}
    (h : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BCMapClosedStep S F steps (.symm h) =
      .symm (nativeC60BCMapClosedStep S F steps h) := rfl

/-- Any observer of the ORIGINAL comparison syntax that is compatible
with all context actions remains compatible with the contextual closure.
No evaluator defines which generators the closure contains. -/
theorem nativeC60BCClosedObserver_sound {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {B : Type v} (obs : L.Total → B)
    (hbase : NativeC60AYRespects S obs)
    (hcontext : ∀ (steps : List Bool) {a b : L.Total},
      obs a = obs b →
        obs (nativeC60BCContextTotal F steps a) =
          obs (nativeC60BCContextTotal F steps b)) :
    NativeC60AYRespects (nativeC60BCClosedSignature S F) obs := by
  intro x y gen
  rcases gen with ⟨steps, a, b, ⟨g, hx, hy⟩⟩
  rw [hx, hy]
  exact hcontext steps (hbase g)

/-- Exact, rather than merely sufficient, condition for an observer to
descend through the independently declared C60 context closure. -/
theorem nativeC60BCClosedObserver_iff {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {B : Type v} (obs : L.Total → B) :
    NativeC60AYRespects (nativeC60BCClosedSignature S F) obs ↔
      ∀ (steps : List Bool) {a b : L.Total} (g : S.Gen a b),
        obs (nativeC60BCContextTotal F steps a) =
          obs (nativeC60BCContextTotal F steps b) := by
  constructor
  · intro h steps a b g
    exact h (nativeC60BCGen S F steps g)
  · intro h x y gen
    rcases gen with ⟨steps, a, b, ⟨g, hx, hy⟩⟩
    rw [hx, hy]
    exact h steps g

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

/-- ACTUAL AQ 14D geometric whiskering, including its Type-valued 15D
proof transport, interpreted as a boundary-preserving frame on the AX layer. -/
def nativeK5BCFrame (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) : NativeC60BCFrame (nativeK5AXBaseLayer W) where
  onObj a := ⟨nativeK5AQWhisker W side a.down⟩
  onCell := by
    intro a b cell
    exact ⟨nativeK5AQWhiskerCell W side cell.down⟩

/-- The context operates on ORIGINAL, proof-carrying 15D cells, not on
a derived scalar or an externally manufactured graph. -/
def nativeK5BCContext (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    (nativeK5AXBaseLayer W).Total → (nativeK5AXBaseLayer W).Total :=
  nativeC60BCContextTotal (nativeK5BCFrame W) steps

theorem nativeK5BCContext_pack (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5BCContext W steps (nativeK5AXPack W cell) =
      nativeK5AXPack W (nativeK5AQContextCell W steps cell) := by
  induction steps with
  | nil => rfl
  | cons side rest ih =>
      change (nativeK5BCFrame W side).mapTotal
          (nativeK5BCContext W rest (nativeK5AXPack W cell)) =
        nativeK5AXPack W
          (nativeK5AQWhiskerCell W side (nativeK5AQContextCell W rest cell))
      rw [ih]
      rfl

/-- The BC signature consists of the original physically named AU 16D
naturality comparisons under arbitrary ACTUAL C60 14D contexts. -/
def nativeK5BCSignature (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60AXSignature (nativeK5AXBaseLayer W) :=
  nativeC60BCClosedSignature (nativeK5AXKuuSignature W) (nativeK5BCFrame W)

/-- GENUINE typed 16D evidence in this EXPLICITLY EXTENDED presentation.
These are *not* claimed to be pre-existing geometric 16-cells. -/
def nativeK5BCContextualNaturality (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    NativeC60AXStep (nativeK5BCSignature W)
      (nativeK5BCContext W steps
        (nativeK5AXPack W (nativeK5AUNaturalityViaSource W cell)))
      (nativeK5BCContext W steps
        (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W cell))) :=
  nativeC60BCMapOriginalStep (nativeK5AXKuuSignature W)
    (nativeK5BCFrame W) steps (nativeK5AXDeclaredNaturality W cell)

/-- The CONTEXTUAL 16D comparison has the exact original 14D boundary
on the two ACTUALLY CONSTRUCTED 15D naturality terms. -/
theorem nativeK5BCContextualNaturality_boundary
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (nativeK5AXPack W
      (nativeK5AQContextCell W steps (nativeK5AUNaturalityViaSource W cell))).1 =
    (nativeK5AXPack W
      (nativeK5AQContextCell W steps (nativeK5AUNaturalityViaTarget W cell))).1 := by
  have h := (nativeK5BCContextualNaturality W steps cell).boundary
  simpa only [nativeK5BCContext_pack] using h

/-- The newly built 16D context action remains INSIDE the same physical
context-closed signature at arbitrary finite context length. -/
def nativeK5BCClosedContextStep (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    {a b : (nativeK5AXBaseLayer W).Total}
    (c : NativeC60AXStep (nativeK5BCSignature W) a b) :
    NativeC60AXStep (nativeK5BCSignature W)
      (nativeK5BCContext W steps a)
      (nativeK5BCContext W steps b) :=
  nativeC60BCMapClosedStep (nativeK5AXKuuSignature W) (nativeK5BCFrame W) steps c

/-- Actual Peiffer kernel value after a finite CONTEXT on the typed 15D
witness. The acting group element is the true noncommutative AT gauge word. -/
theorem nativeK5BCContext_pack_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5AXPeiffer W (nativeK5BCContext W steps (nativeK5AXPack W cell)) =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W steps)
        (nativeK5AXPeiffer W (nativeK5AXPack W cell)) := by
  rw [nativeK5BCContext_pack]
  change nativeK5ATCellDefect W (nativeK5AQContextCell W steps cell) =
    nativeK5ASPeifferAct W (nativeK5ATGaugeWord W steps)
      (nativeK5ATCellDefect W cell)
  exact nativeK5ATCellDefect_context W steps cell

theorem nativeK5BCContext_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    (c : (nativeK5AXBaseLayer W).Total) :
    nativeK5AXPeiffer W (nativeK5BCContext W steps c) =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W steps)
        (nativeK5AXPeiffer W c) := by
  rcases c with ⟨⟨⟨R⟩, ⟨S⟩⟩, ⟨cell⟩⟩
  exact nativeK5BCContext_pack_peiffer W steps cell

/-- Context closure CONSERVES the physical nonabelian Peiffer value
because the gauge action is applied to equal original kernel values.
This is not an abelianization of the critical exchange. -/
theorem nativeK5BCSignature_peiffer
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60AYRespects (nativeK5BCSignature W) (nativeK5AXPeiffer W) := by
  apply nativeC60BCClosedObserver_sound
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) (nativeK5AXPeiffer W)
  · intro a b g
    exact nativeK5AXPeiffer_step_sound W (.atom g)
  · intro steps a b h
    change nativeK5AXPeiffer W (nativeK5BCContext W steps a) =
      nativeK5AXPeiffer W (nativeK5BCContext W steps b)
    rw [nativeK5BCContext_peiffer W steps a,
      nativeK5BCContext_peiffer W steps b]
    exact congrArg (nativeK5ASPeifferAct W (nativeK5ATGaugeWord W steps)) h

/-- Every ACTUAL newly constructed 16D contextual comparison has
the same physical noncommutative Peiffer value at both 15D endpoints. -/
theorem nativeK5BCContextualNaturality_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5AXPeiffer W
      (nativeK5BCContext W steps
        (nativeK5AXPack W (nativeK5AUNaturalityViaSource W cell))) =
    nativeK5AXPeiffer W
      (nativeK5BCContext W steps
        (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W cell))) :=
  (nativeK5BCContextualNaturality W steps cell).observer_sound
    (nativeK5AXPeiffer W) (nativeK5BCSignature_peiffer W)

/-- The original AX raw discriminator is invariant under BOTH actually
constructed AQ whiskerings: no contextual action erases the first
conservative-vs-exchange constructor of a 15D witness. -/
theorem nativeK5BCLeading_whisker
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5AXLeadingConservative W (nativeK5AQWhiskerCell W side cell) =
      nativeK5AXLeadingConservative W cell := by
  cases cell with
  | conservative base => rfl
  | exchange steps => rfl
  | symm h => rfl
  | trans h k =>
      cases h <;> rfl

theorem nativeK5BCLeading_context
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5AXLeadingConservative W (nativeK5AQContextCell W steps cell) =
      nativeK5AXLeadingConservative W cell := by
  induction steps with
  | nil => rfl
  | cons side rest ih =>
      change nativeK5AXLeadingConservative W
        (nativeK5AQWhiskerCell W side (nativeK5AQContextCell W rest cell)) =
          nativeK5AXLeadingConservative W cell
      rw [nativeK5BCLeading_whisker W side _, ih]

/-- Although their noncommutative Peiffer evaluations agree, the actual
two 15D AU naturality routes at the original AQ physical exchange remain
DISTINCT raw proof terms after ANY finite word of genuine 14D contexts. -/
theorem nativeK5BCContextualNaturality_raw_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5AQContextCell W steps
        (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])) ≠
      nativeK5AQContextCell W steps
        (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])) := by
  intro heq
  have ht := congrArg (nativeK5AXLeadingConservative W) heq
  rw [nativeK5BCLeading_context W steps,
      nativeK5BCLeading_context W steps] at ht
  change true = false at ht
  cases ht

theorem nativeK5BCContextualPacked_raw_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5BCContext W steps
        (nativeK5AXPack W
          (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W []))) ≠
      nativeK5BCContext W steps
        (nativeK5AXPack W
          (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))) := by
  rw [nativeK5BCContext_pack, nativeK5BCContext_pack]
  intro h
  apply nativeK5BCContextualNaturality_raw_ne W steps
  -- A Sigma's proof component is DEPENDENT on its endpoint pair.
  -- Ordinary congrArg to a nondependent codomain cannot project it.
  cases h
  rfl

/-- Any further finite tower of independently specified AX signatures
inherits the ENTIRE original Peiffer boundary of this physical extension,
not a new numerical equality used to invent cells. -/
def nativeK5BCFinitePeifferDescents
    (W : NativeK5StructuralThirteenCell p U V)
    (N : Nat)
    (tail : NativeC60AXPlan
      (nativeC60AXNext (nativeK5AXBaseLayer W) (nativeK5BCSignature W)) N) :
    NativeC60AYFiniteDescentData (nativeK5AXBaseLayer W) (N + 1)
      ⟨nativeK5BCSignature W, tail⟩ (nativeK5AXPeiffer W) :=
  nativeC60AYBuildFiniteDescents _ _ _ _
    ⟨nativeK5BCSignature_peiffer W,
      nativeC60AYFinite_boundary_observer_sound _ (nativeK5BCSignature W) N tail
        (nativeK5AXPeiffer W)⟩

end PhysicalC60

#print axioms NativeC60BCFrame
#print axioms NativeC60BCFrame.mapTotal
#print axioms nativeC60BCContextTotal
#print axioms nativeC60BCContextTotal_append
#print axioms nativeC60BCContextTotal_boundary
#print axioms nativeC60BCClosedSignature
#print axioms nativeC60BCGen
#print axioms nativeC60BCShiftGen
#print axioms nativeC60BCMapOriginalStep
#print axioms nativeC60BCMapClosedStep
#print axioms nativeC60BCMapClosedStep_trans
#print axioms nativeC60BCMapClosedStep_symm
#print axioms nativeC60BCClosedObserver_sound
#print axioms nativeC60BCClosedObserver_iff
#print axioms nativeK5BCFrame
#print axioms nativeK5BCContext
#print axioms nativeK5BCContext_pack
#print axioms nativeK5BCSignature
#print axioms nativeK5BCContextualNaturality
#print axioms nativeK5BCContextualNaturality_boundary
#print axioms nativeK5BCClosedContextStep
#print axioms nativeK5BCContext_pack_peiffer
#print axioms nativeK5BCContext_peiffer
#print axioms nativeK5BCSignature_peiffer
#print axioms nativeK5BCContextualNaturality_peiffer
#print axioms nativeK5BCLeading_whisker
#print axioms nativeK5BCLeading_context
#print axioms nativeK5BCContextualNaturality_raw_ne
#print axioms nativeK5BCContextualPacked_raw_ne
#print axioms nativeK5BCFinitePeifferDescents

end
end Kuu.F112.Physical
