import Kuu.F112.PolygonNativeC60FiniteStrictKuu

/-!
# F112-P94D3BA — cross-level strict boundary transport

AZ constructs strict categories at every finite stage. BA constructs their
strict-arrow interface: each quotient arrow has an actual AX representative,
and an upper readout factors uniquely through this interface exactly when it
respects the independently declared strict identifications.

The unchanged injective raw-object embedding of the next stage cannot itself
factor through this map: refl and trans(refl,refl) already give a counterexample.
This is an obstruction to that PARTICULAR interface, not a no-go for strict
n-categories. A compatible observer retains both endpoints and the full lower
strict arrow and descends through every finite continuation. Its discrete
codomain is an observer, not a replacement for the proof-relevant higher core.

No new dimension-by-dimension generators, universal fillers or Gray structures.
The missing cross-dimensional horizontal composition/interchange is not claimed.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- Compress a path of actual AX terms into one actual AX term. -/
def nativeC60BAFold {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) {a : NativeC60AZStrictObj S} :
    {b : NativeC60AZStrictObj S} → Quiver.Path a b → NativeC60AXStep S a.val b.val
  | _, .nil => .refl a.val
  | _, .cons p c => .trans (nativeC60BAFold S p) c

/-- Compression changes parentheses, not the realized strict arrow. -/
theorem nativeC60BAFold_spec {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    {a b : NativeC60AZStrictObj S} (p : Quiver.Path a b) :
    nativeC60AZStrictStep S R (nativeC60BAFold S p) =
      (nativeC60AZStrictProject S R).map p := by
  induction p with
  | nil => exact nativeC60AZStrictStep_refl S R _
  | cons p c ih =>
      calc
        nativeC60AZStrictStep S R (nativeC60BAFold S (p.cons c)) =
            nativeC60AZStrictStep S R (nativeC60BAFold S p) ≫
              nativeC60AZStrictStep S R c := nativeC60AZStrictStep_comp S R _ _
        _ = (nativeC60AZStrictProject S R).map p ≫
              (nativeC60AZStrictProject S R).map (nativeC60AZRawArrow S c) :=
            congrArg (fun k => k ≫ nativeC60AZStrictStep S R c) ih
        _ = (nativeC60AZStrictProject S R).map (p.cons c) :=
            ((nativeC60AZStrictProject S R).map_comp p (nativeC60AZRawArrow S c)).symm

/-- Every strict arrow is represented by one actual dependent comparison. -/
theorem nativeC60BAStep_surjective {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (x y : L.Total) : Function.Surjective
      (fun c : NativeC60AXStep S x y => nativeC60AZStrictStep S R c) := by
  intro f
  refine Quot.inductionOn f ?_
  intro p
  exact ⟨nativeC60BAFold S p, nativeC60BAFold_spec S R p⟩

/-- Both exact lower endpoints plus the entire strict arrow, not a scalar shadow. -/
def NativeC60BAStrictArrows {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) : Type u :=
  Σ xy : L.Total × L.Total,
    (nativeC60AZStrictProject S R).obj ⟨xy.1⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨xy.2⟩

def nativeC60BARealize {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) :
    (nativeC60AXNext L S).Total → NativeC60BAStrictArrows S R :=
  fun c => ⟨c.1, nativeC60AZStrictStep S R c.2⟩

theorem nativeC60BARealize_boundary {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (c : (nativeC60AXNext L S).Total) :
    (nativeC60BARealize S R c).1 = c.1 := rfl

theorem nativeC60BARealize_surjective {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) :
    Function.Surjective (nativeC60BARealize S R) := by
  rintro ⟨⟨x, y⟩, f⟩
  obtain ⟨c, hc⟩ := nativeC60BAStep_surjective S R x y f
  refine ⟨⟨(x, y), c⟩, ?_⟩
  exact congrArg (fun k : (nativeC60AZStrictProject S R).obj ⟨x⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨y⟩ =>
        (⟨(x, y), k⟩ : NativeC60BAStrictArrows S R)) hc

/-- A condition on a readout of the existing strict quotient. It does not
redefine the quotient using the readout's kernel. -/
def NativeC60BARespectsStrict {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    {B : Type v} (obs : (nativeC60AXNext L S).Total → B) : Prop :=
  ∀ c d, nativeC60BARealize S R c = nativeC60BARealize S R d → obs c = obs d

/-- Representative readout; the following theorem states exactly when it factors. -/
def nativeC60BADescend {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    {B : Type v} (obs : (nativeC60AXNext L S).Total → B) :
    NativeC60BAStrictArrows S R → B :=
  fun q => obs (Classical.choose (nativeC60BARealize_surjective S R q))

theorem nativeC60BADescend_spec {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    {B : Type v} (obs : (nativeC60AXNext L S).Total → B)
    (h : NativeC60BARespectsStrict S R obs) (c : (nativeC60AXNext L S).Total) :
    nativeC60BADescend S R obs (nativeC60BARealize S R c) = obs c := by
  apply h
  exact Classical.choose_spec (nativeC60BARealize_surjective S R (nativeC60BARealize S R c))

/-- The precise, unique-factorization criterion for cross-level readouts. -/
theorem nativeC60BADescent_unique_iff {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    {B : Type v} (obs : (nativeC60AXNext L S).Total → B) :
    (∃! f : NativeC60BAStrictArrows S R → B,
      ∀ c, f (nativeC60BARealize S R c) = obs c) ↔ NativeC60BARespectsStrict S R obs := by
  constructor
  · rintro ⟨f, hf, _⟩ c d hcd
    calc
      obs c = f (nativeC60BARealize S R c) := (hf c).symm
      _ = f (nativeC60BARealize S R d) := congrArg f hcd
      _ = obs d := hf d
  · intro h
    refine ⟨nativeC60BADescend S R obs, nativeC60BADescend_spec S R obs h, ?_⟩
    intro f hf
    funext q
    obtain ⟨c, rfl⟩ := nativeC60BARealize_surjective S R q
    exact (hf c).trans (nativeC60BADescend_spec S R obs h c).symm

/-- A raw syntactic discriminator, kept outside the strict quotient. -/
def nativeC60BARawUnitTag {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (c : (nativeC60AXNext L S).Total) : Bool :=
  c.2.fold (K := fun _ _ => Bool)
    (fun {_ _} _ => false)
    (fun _ => true)
    (fun _ => false)
    (fun _ _ => false)

theorem nativeC60BARawUnit_ne {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (x : L.Total) :
    (⟨(x, x), NativeC60AXStep.refl x⟩ : (nativeC60AXNext L S).Total) ≠
      ⟨(x, x), NativeC60AXStep.trans (.refl x) (.refl x)⟩ := by
  intro h
  have ht := congrArg (nativeC60BARawUnitTag S) h
  change true = false at ht
  cases ht

/-- The strict unit law identifies these two raw representatives. -/
theorem nativeC60BAUnit_realize_eq {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) (x : L.Total) :
    nativeC60BARealize S R ⟨(x, x), .refl x⟩ =
      nativeC60BARealize S R ⟨(x, x), .trans (.refl x) (.refl x)⟩ := by
  have h : nativeC60AZStrictStep S R (.refl x) =
      nativeC60AZStrictStep S R (.trans (.refl x) (.refl x)) := by
    simp only [nativeC60AZStrictStep_comp, nativeC60AZStrictStep_refl, Category.id_comp]
  exact congrArg (fun k : (nativeC60AZStrictProject S R).obj ⟨x⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨x⟩ =>
        (⟨(x, x), k⟩ : NativeC60BAStrictArrows S R)) h

/-- Injective raw readouts cannot pass through this non-injective strict map.
This is not a claim that all strict higher presentations are impossible. -/
theorem nativeC60BAInjective_no_descent {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) (x : L.Total)
    {B : Type v} (obs : (nativeC60AXNext L S).Total → B) (hi : Function.Injective obs) :
    ¬ ∃ f : NativeC60BAStrictArrows S R → B,
      ∀ c, f (nativeC60BARealize S R c) = obs c := by
  rintro ⟨f, hf⟩
  apply nativeC60BARawUnit_ne S x
  apply hi
  calc
    obs ⟨(x, x), .refl x⟩ = f (nativeC60BARealize S R ⟨(x, x), .refl x⟩) := (hf _).symm
    _ = f (nativeC60BARealize S R ⟨(x, x), .trans (.refl x) (.refl x)⟩) :=
      congrArg f (nativeC60BAUnit_realize_eq S R x)
    _ = obs ⟨(x, x), .trans (.refl x) (.refl x)⟩ := hf _

/-- The actual AZ next category retains raw objects injectively. Therefore
its object assignment is not already a descent along the previous strict map. -/
theorem nativeC60BAUpperObject_no_descent {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    (U : NativeC60AZParallelRelation T) (x : L.Total) :
    ¬ ∃ f : NativeC60BAStrictArrows S R → NativeC60AZStrictSpace T U,
      ∀ c, f (nativeC60BARealize S R c) = (nativeC60AZStrictProject T U).obj ⟨c⟩ :=
  nativeC60BAInjective_no_descent S R x
    (fun c => (nativeC60AZStrictProject T U).obj ⟨c⟩)
    (nativeC60AZStrictObj_injective T U)

/-- The selected next signature conserves the full lower strict arrow, with
both dependent endpoints retained and their transport proved explicitly. -/
theorem nativeC60BABridge_respects {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S)) :
    NativeC60AYRespects T (nativeC60BARealize S (nativeC60AZHigherRelations S T)) := by
  intro a b g
  rcases a with ⟨xy, c⟩
  rcases b with ⟨xy', d⟩
  have hb : xy = xy' := T.boundary g
  cases hb
  have hc : nativeC60AZStrictStep S (nativeC60AZHigherRelations S T) c =
      nativeC60AZStrictStep S (nativeC60AZHigherRelations S T) d :=
    nativeC60AZStrictStep_declared S (nativeC60AZHigherRelations S T) ⟨g⟩
  exact congrArg (fun k :
      (nativeC60AZStrictProject S (nativeC60AZHigherRelations S T)).obj ⟨xy.1⟩ ⟶
        (nativeC60AZStrictProject S (nativeC60AZHigherRelations S T)).obj ⟨xy.2⟩ =>
      (⟨xy, k⟩ : NativeC60BAStrictArrows S (nativeC60AZHigherRelations S T))) hc

def nativeC60BABridgePrefunctor {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S)) :
    NativeC60AZStrictObj T ⥤q
      Discrete (NativeC60BAStrictArrows S (nativeC60AZHigherRelations S T)) where
  obj c := Discrete.mk (nativeC60BARealize S (nativeC60AZHigherRelations S T) c.val)
  map h := eqToHom (congrArg Discrete.mk
    (h.observer_sound (nativeC60BARealize S (nativeC60AZHigherRelations S T))
      (nativeC60BABridge_respects S T)))

/-- A strict functor carrying the compatible cross-level boundary observation.
The higher category is not replaced by this discrete observation target. -/
def nativeC60BAStrictBridge {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    (U : NativeC60AZParallelRelation T) :
    NativeC60AZStrictSpace T U ⥤
      Discrete (NativeC60BAStrictArrows S (nativeC60AZHigherRelations S T)) :=
  Kuu.descend (nativeC60AZStrictRelations T U)
    (Paths.lift (nativeC60BABridgePrefunctor S T))
    (by intro x y f g h; exact Subsingleton.elim _ _)

theorem nativeC60BAStrictBridge_obj {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    (U : NativeC60AZParallelRelation T) (c : (nativeC60AXNext L S).Total) :
    (nativeC60BAStrictBridge S T U).obj ((nativeC60AZStrictProject T U).obj ⟨c⟩) =
      Discrete.mk (nativeC60BARealize S (nativeC60AZHigherRelations S T) c) := rfl

/-- All finite tails preserve the inherited full strict-arrow boundary. -/
theorem nativeC60BAFiniteBridgeSound {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    (N : Nat) (tail : NativeC60AXPlan (nativeC60AXNext (nativeC60AXNext L S) T) N) :
    NativeC60AYFiniteObserverSound (nativeC60AXNext L S) (N + 1) ⟨T, tail⟩
      (nativeC60BARealize S (nativeC60AZHigherRelations S T)) :=
  ⟨nativeC60BABridge_respects S T,
    nativeC60AYFinite_boundary_observer_sound _ T N tail
      (nativeC60BARealize S (nativeC60AZHigherRelations S T))⟩

def nativeC60BAFiniteBridgeDescents {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    (N : Nat) (tail : NativeC60AXPlan (nativeC60AXNext (nativeC60AXNext L S) T) N) :
    NativeC60AYFiniteDescentData (nativeC60AXNext L S) (N + 1) ⟨T, tail⟩
      (nativeC60BARealize S (nativeC60AZHigherRelations S T)) :=
  nativeC60AYBuildFiniteDescents _ _ _ _ (nativeC60BAFiniteBridgeSound S T N tail)

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

def nativeK5BAFiniteStrictBoundaryDescents (W : NativeK5StructuralThirteenCell p U V)
    (T : NativeC60AXSignature
      (nativeC60AXNext (nativeK5AXBaseLayer W) (nativeK5AXKuuSignature W)))
    (N : Nat) (tail : NativeC60AXPlan
      (nativeC60AXNext
        (nativeC60AXNext (nativeK5AXBaseLayer W) (nativeK5AXKuuSignature W)) T) N) :=
  nativeC60BAFiniteBridgeDescents (nativeK5AXKuuSignature W) T N tail

/-- The obstruction uses an actual AQ exchange at the original C60 base. -/
theorem nativeK5BAUpperObject_no_descent (W : NativeK5StructuralThirteenCell p U V)
    (T : NativeC60AXSignature
      (nativeC60AXNext (nativeK5AXBaseLayer W) (nativeK5AXKuuSignature W)))
    (R : NativeC60AZParallelRelation T) :
    ¬ ∃ f : NativeC60BAStrictArrows (nativeK5AXKuuSignature W)
          (nativeC60AZHigherRelations (nativeK5AXKuuSignature W) T) →
        NativeC60AZStrictSpace T R,
      ∀ c, f (nativeC60BARealize (nativeK5AXKuuSignature W)
          (nativeC60AZHigherRelations (nativeK5AXKuuSignature W) T) c) =
        (nativeC60AZStrictProject T R).obj ⟨c⟩ :=
  nativeC60BAUpperObject_no_descent (nativeK5AXKuuSignature W)
    (nativeC60AZHigherRelations (nativeK5AXKuuSignature W) T) T R
    (nativeK5AXPack W (nativeK5AQExchange W []))

end PhysicalC60

#print axioms nativeC60BAFold
#print axioms nativeC60BAFold_spec
#print axioms nativeC60BAStep_surjective
#print axioms NativeC60BAStrictArrows
#print axioms nativeC60BARealize
#print axioms nativeC60BARealize_boundary
#print axioms nativeC60BARealize_surjective
#print axioms NativeC60BARespectsStrict
#print axioms nativeC60BADescend
#print axioms nativeC60BADescend_spec
#print axioms nativeC60BADescent_unique_iff
#print axioms nativeC60BARawUnitTag
#print axioms nativeC60BARawUnit_ne
#print axioms nativeC60BAUnit_realize_eq
#print axioms nativeC60BAInjective_no_descent
#print axioms nativeC60BAUpperObject_no_descent
#print axioms nativeC60BABridge_respects
#print axioms nativeC60BABridgePrefunctor
#print axioms nativeC60BAStrictBridge
#print axioms nativeC60BAStrictBridge_obj
#print axioms nativeC60BAFiniteBridgeSound
#print axioms nativeC60BAFiniteBridgeDescents
#print axioms nativeK5BAFiniteStrictBoundaryDescents
#print axioms nativeK5BAUpperObject_no_descent

end
end Kuu.F112.Physical
