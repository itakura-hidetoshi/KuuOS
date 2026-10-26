import Kuu.Strict
import Kuu.F112.PolygonNativeC60FiniteTwoSidedGaugeHolonomy
import Mathlib.CategoryTheory.Discrete.Basic
import Mathlib.CategoryTheory.SingleObj

/-!
# F112-P94D3AZ — finite C60 realization in the existing strict Kuu kernel

The signature consists of ACTUAL AX dependent comparison terms, not the C60
incidence graph. Kuu.Space imposes the declared unit/composition/inverse laws
and selected parallel higher comparisons. No observer kernel defines these
relations. Raw terms remain available; their structural parenthesizations are
not falsely claimed to stay distinct inside the strict quotient.

Every finite AX plan receives actual strict category carriers, realization
maps, and both-boundary functors. Kuu.Strict supplies the strict comparison
calculus and comparison descent. Noncommutative holonomy factors precisely
when it respects the independently declared higher relations.

This reconnects finite C60 constructions to strict Kuu. It is NOT yet a
cross-dimensional strict 3/n-category: horizontal higher composition and its
interchange, original geometric 16-cell coherence, full P92B descent, and
hyperdescent remain separate obligations. No Gray or new axioms.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w uD vD uE vE

/-- A signature-indexed carrier. Keeping the signature in the type, rather
than unfolding to L.Total, makes the Quiver instance synthesizable and
prevents comparisons from two different signatures being conflated. -/
structure NativeC60AZStrictObj {L : NativeC60AXLayer.{u}}
    (_S : NativeC60AXSignature L) where
  val : L.Total

instance nativeC60AZStrictQuiver {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) : Quiver (NativeC60AZStrictObj S) where
  Hom x y := NativeC60AXStep S x.val y.val

/-- Encode an existing dependent proof as a one-letter typed path. -/
def nativeC60AZRawArrow {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) {x y : L.Total}
    (c : NativeC60AXStep S x y) :
    Quiver.Path (⟨x⟩ : NativeC60AZStrictObj S)
      (⟨y⟩ : NativeC60AZStrictObj S) :=
  Quiver.Hom.toPath c

/-- Optional equalities only between comparisons with the same exact boundary. -/
def NativeC60AZParallelRelation {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) : Type u :=
  ∀ {x y : L.Total}, NativeC60AXStep S x y → NativeC60AXStep S x y → Prop

/-- Declared laws, independent of numerical or group-valued evaluation. -/
inductive NativeC60AZStrictRel {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) :
    {x y : NativeC60AZStrictObj S} →
      Quiver.Path x y → Quiver.Path x y → Prop where
  | ident (x : L.Total) : NativeC60AZStrictRel S R
      (nativeC60AZRawArrow S (.refl x))
        (𝟙 (⟨x⟩ : Kuu.Raw (NativeC60AZStrictObj S)))
  | compose {x y z : L.Total} (c : NativeC60AXStep S x y)
      (d : NativeC60AXStep S y z) : NativeC60AZStrictRel S R
      (nativeC60AZRawArrow S (.trans c d))
      (nativeC60AZRawArrow S c ≫ nativeC60AZRawArrow S d)
  | inverseLeft {x y : L.Total} (c : NativeC60AXStep S x y) :
      NativeC60AZStrictRel S R
        (nativeC60AZRawArrow S c ≫ nativeC60AZRawArrow S (.symm c))
        (𝟙 (⟨x⟩ : Kuu.Raw (NativeC60AZStrictObj S)))
  | inverseRight {x y : L.Total} (c : NativeC60AXStep S x y) :
      NativeC60AZStrictRel S R
        (nativeC60AZRawArrow S (.symm c) ≫ nativeC60AZRawArrow S c)
        (𝟙 (⟨y⟩ : Kuu.Raw (NativeC60AZStrictObj S)))
  | declared {x y : L.Total} {c d : NativeC60AXStep S x y} (h : R c d) :
      NativeC60AZStrictRel S R (nativeC60AZRawArrow S c) (nativeC60AZRawArrow S d)

abbrev NativeC60AZStrictSpace {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) :=
  Kuu.Space (NativeC60AZStrictObj S) (NativeC60AZStrictRel S R)

def nativeC60AZStrictProject {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) :
    Kuu.Raw (NativeC60AZStrictObj S) ⥤ NativeC60AZStrictSpace S R :=
  Kuu.project (NativeC60AZStrictObj S) (NativeC60AZStrictRel S R)

def nativeC60AZStrictStep {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    {x y : L.Total} (c : NativeC60AXStep S x y) :
    (nativeC60AZStrictProject S R).obj ⟨x⟩ ⟶ (nativeC60AZStrictProject S R).obj ⟨y⟩ :=
  (nativeC60AZStrictProject S R).map (nativeC60AZRawArrow S c)

section StrictRealization

variable {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
variable (R : NativeC60AZParallelRelation S)

theorem nativeC60AZStrictStep_refl (x : L.Total) :
    nativeC60AZStrictStep S R (.refl x) = 𝟙 ((nativeC60AZStrictProject S R).obj ⟨x⟩) := by
  calc
    _ = (nativeC60AZStrictProject S R).map (𝟙 (⟨x⟩ : Kuu.Raw (NativeC60AZStrictObj S))) :=
      Kuu.declared_replacement (NativeC60AZStrictRel S R) (.ident x)
    _ = _ := (nativeC60AZStrictProject S R).map_id ⟨x⟩

theorem nativeC60AZStrictStep_comp {x y z : L.Total}
    (c : NativeC60AXStep S x y) (d : NativeC60AXStep S y z) :
    nativeC60AZStrictStep S R (.trans c d) =
      nativeC60AZStrictStep S R c ≫ nativeC60AZStrictStep S R d := by
  calc
    _ = (nativeC60AZStrictProject S R).map
        (nativeC60AZRawArrow S c ≫ nativeC60AZRawArrow S d) :=
      Kuu.declared_replacement (NativeC60AZStrictRel S R) (.compose c d)
    _ = _ := (nativeC60AZStrictProject S R).map_comp _ _

theorem nativeC60AZStrictStep_inv_left {x y : L.Total} (c : NativeC60AXStep S x y) :
    nativeC60AZStrictStep S R c ≫ nativeC60AZStrictStep S R (.symm c) =
      𝟙 ((nativeC60AZStrictProject S R).obj ⟨x⟩) := by
  calc
    _ = (nativeC60AZStrictProject S R).map
        (nativeC60AZRawArrow S c ≫ nativeC60AZRawArrow S (.symm c)) :=
      ((nativeC60AZStrictProject S R).map_comp _ _).symm
    _ = (nativeC60AZStrictProject S R).map (𝟙 (⟨x⟩ : Kuu.Raw (NativeC60AZStrictObj S))) :=
      Kuu.declared_replacement (NativeC60AZStrictRel S R) (.inverseLeft c)
    _ = _ := (nativeC60AZStrictProject S R).map_id ⟨x⟩

theorem nativeC60AZStrictStep_inv_right {x y : L.Total} (c : NativeC60AXStep S x y) :
    nativeC60AZStrictStep S R (.symm c) ≫ nativeC60AZStrictStep S R c =
      𝟙 ((nativeC60AZStrictProject S R).obj ⟨y⟩) := by
  calc
    _ = (nativeC60AZStrictProject S R).map
        (nativeC60AZRawArrow S (.symm c) ≫ nativeC60AZRawArrow S c) :=
      ((nativeC60AZStrictProject S R).map_comp _ _).symm
    _ = (nativeC60AZStrictProject S R).map (𝟙 (⟨y⟩ : Kuu.Raw (NativeC60AZStrictObj S))) :=
      Kuu.declared_replacement (NativeC60AZStrictRel S R) (.inverseRight c)
    _ = _ := (nativeC60AZStrictProject S R).map_id ⟨y⟩

theorem nativeC60AZStrictStep_declared {x y : L.Total}
    {c d : NativeC60AXStep S x y} (h : R c d) :
    nativeC60AZStrictStep S R c = nativeC60AZStrictStep S R d :=
  Kuu.declared_replacement (NativeC60AZStrictRel S R) (.declared h)

/-- Exact compositional closure, not the kernel of an observer. -/
theorem nativeC60AZStrictStep_exact {x y : L.Total} (c d : NativeC60AXStep S x y) :
    nativeC60AZStrictStep S R c = nativeC60AZStrictStep S R d ↔
      Kuu.Replaceable (NativeC60AZStrictRel S R)
        (nativeC60AZRawArrow S c) (nativeC60AZRawArrow S d) :=
  Kuu.project_exact (NativeC60AZStrictRel S R) _ _

/-- The previous raw cells, including their boundaries, remain distinct objects. -/
theorem nativeC60AZStrictObj_injective :
    Function.Injective (fun x : L.Total => (nativeC60AZStrictProject S R).obj ⟨x⟩) := by
  intro x y h
  exact congrArg (fun z : NativeC60AZStrictSpace S R => z.as.val) h

/-- Realization has strict associativity; raw parenthesizations need not be equal. -/
theorem nativeC60AZStrictStep_assoc {a b c d : L.Total}
    (f : NativeC60AXStep S a b) (g : NativeC60AXStep S b c)
    (h : NativeC60AXStep S c d) :
    nativeC60AZStrictStep S R (.trans (.trans f g) h) =
      nativeC60AZStrictStep S R (.trans f (.trans g h)) := by
  simp only [nativeC60AZStrictStep_comp, Category.assoc]

/-- A genuine functor reads BOTH original lower endpoints. -/
def nativeC60AZBoundaryPrefunctor :
    NativeC60AZStrictObj S ⥤q Discrete (L.Obj × L.Obj) where
  obj x := Discrete.mk x.val.1
  map c := eqToHom (congrArg Discrete.mk c.boundary)

def nativeC60AZStrictBoundary :
    NativeC60AZStrictSpace S R ⥤ Discrete (L.Obj × L.Obj) :=
  Kuu.descend (NativeC60AZStrictRel S R)
    (Paths.lift (nativeC60AZBoundaryPrefunctor S))
    (by intro x y f g h; exact Subsingleton.elim _ _)

theorem nativeC60AZStrictBoundary_obj (x : L.Total) :
    (nativeC60AZStrictBoundary S R).obj ((nativeC60AZStrictProject S R).obj ⟨x⟩) =
      Discrete.mk x.1 := rfl

/-- Necessary AND sufficient factorization through this declared strict quotient. -/
theorem nativeC60AZStrictObserver_iff {C : Type v} [Category.{w} C]
    (F : Kuu.Raw (NativeC60AZStrictObj S) ⥤ C) :
    (∃ G : NativeC60AZStrictSpace S R ⥤ C,
      nativeC60AZStrictProject S R ⋙ G = F) ↔
        Kuu.Respects (NativeC60AZStrictRel S R) F := by
  constructor
  · rintro ⟨H, hF⟩ x y f g hr
    have heq := congrArg (fun k => H.map k)
      (Kuu.declared_replacement (NativeC60AZStrictRel S R) hr)
    rw [← hF]
    exact heq
  · intro h
    exact ⟨Kuu.descend _ F h, Kuu.descend_spec _ F h⟩

theorem nativeC60AZStrictObserver_unique {C : Type v} [Category.{w} C]
    (F : Kuu.Raw (NativeC60AZStrictObj S) ⥤ C)
    (h : Kuu.Respects (NativeC60AZStrictRel S R) F) :
    ∃! G : NativeC60AZStrictSpace S R ⥤ C,
      nativeC60AZStrictProject S R ⋙ G = F :=
  Kuu.observer_existsUnique _ F h

/-- Actual connection to Kuu.Strict, not merely an import. -/
def nativeC60AZStrictComparison {C : Type v} [Category.{w} C]
    {F G : NativeC60AZStrictSpace S R ⥤ C}
    (a : nativeC60AZStrictProject S R ⋙ F ⟶ nativeC60AZStrictProject S R ⋙ G) : F ⟶ G :=
  Kuu.descendComparison (NativeC60AZStrictRel S R) a

theorem nativeC60AZStrictComparison_comp {C : Type v} [Category.{w} C]
    {F G H : NativeC60AZStrictSpace S R ⥤ C}
    (a : nativeC60AZStrictProject S R ⋙ F ⟶ nativeC60AZStrictProject S R ⋙ G)
    (b : nativeC60AZStrictProject S R ⋙ G ⟶ nativeC60AZStrictProject S R ⋙ H) :
    nativeC60AZStrictComparison S R (a ≫ b) =
      nativeC60AZStrictComparison S R a ≫ nativeC60AZStrictComparison S R b :=
  Kuu.descendComparison_comp (NativeC60AZStrictRel S R) a b

theorem nativeC60AZStrictComparison_id {C : Type v} [Category.{w} C]
    (F : NativeC60AZStrictSpace S R ⥤ C) :
    nativeC60AZStrictComparison S R (𝟙 (nativeC60AZStrictProject S R ⋙ F)) = 𝟙 F :=
  Kuu.descendComparison_id (NativeC60AZStrictRel S R) F

/-- Strict TWO-dimensional comparison interchange on the constructed carrier.
This is not the missing cross-dimensional strict-three interchange. -/
theorem nativeC60AZStrictInterchange
    {C : Type uD} [Category.{vD} C] {D : Type uE} [Category.{vE} D]
    {F G H : NativeC60AZStrictSpace S R ⥤ C} {I J K : C ⥤ D}
    (a : F ⟶ G) (b : G ⟶ H) (c : I ⟶ J) (d : J ⟶ K) :
    (a ≫ b) ◫ (c ≫ d) = (a ◫ c) ≫ (b ◫ d) :=
  Kuu.two_interchange a b c d

end StrictRealization

section NoncommutativeReceivers

variable {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
variable (R : NativeC60AZParallelRelation S)
variable {G : Type v} [Group G]
variable (weight : ∀ {x y}, S.Gen x y → G)

/-- Opposite multiplication accounts for mathlib SingleObj's composition order. -/
def nativeC60AZHolonomyPrefunctor :
    NativeC60AZStrictObj S ⥤q SingleObj Gᵐᵒᵖ where
  obj _ := SingleObj.star _
  map c := MulOpposite.op (nativeC60AZHolonomy S weight c)

def nativeC60AZRawHolonomy : Kuu.Raw (NativeC60AZStrictObj S) ⥤ SingleObj Gᵐᵒᵖ :=
  Paths.lift (nativeC60AZHolonomyPrefunctor S weight)

theorem nativeC60AZRawHolonomy_arrow {x y : L.Total} (c : NativeC60AXStep S x y) :
    (nativeC60AZRawHolonomy S weight).map (nativeC60AZRawArrow S c) =
      MulOpposite.op (nativeC60AZHolonomy S weight c) :=
  Paths.lift_toPath (nativeC60AZHolonomyPrefunctor S weight) c

def NativeC60AZWeightsRespect : Prop :=
  ∀ {x y : L.Total} (c d : NativeC60AXStep S x y),
    R c d → nativeC60AZHolonomy S weight c = nativeC60AZHolonomy S weight d

/-- Structural laws hold in every group; selected higher relations require proof. -/
theorem nativeC60AZRawHolonomy_respects_iff :
    Kuu.Respects (NativeC60AZStrictRel S R) (nativeC60AZRawHolonomy S weight) ↔
      NativeC60AZWeightsRespect S R weight := by
  constructor
  · intro h x y c d hcd
    have hh := h _ _ _ _ (NativeC60AZStrictRel.declared hcd)
    rw [nativeC60AZRawHolonomy_arrow, nativeC60AZRawHolonomy_arrow] at hh
    exact congrArg MulOpposite.unop hh
  · intro h x y f g rel
    cases rel with
    | ident a =>
        rw [nativeC60AZRawHolonomy_arrow, (nativeC60AZRawHolonomy S weight).map_id]
        rfl
    | compose c d =>
        rw [(nativeC60AZRawHolonomy S weight).map_comp,
          nativeC60AZRawHolonomy_arrow, nativeC60AZRawHolonomy_arrow,
          nativeC60AZRawHolonomy_arrow]
        rfl
    | inverseLeft c =>
        rw [(nativeC60AZRawHolonomy S weight).map_comp,
          nativeC60AZRawHolonomy_arrow, nativeC60AZRawHolonomy_arrow,
          (nativeC60AZRawHolonomy S weight).map_id]
        change MulOpposite.op (nativeC60AZHolonomy S weight c *
          (nativeC60AZHolonomy S weight c)⁻¹) = MulOpposite.op (1 : G)
        rw [mul_inv_cancel]
    | inverseRight c =>
        rw [(nativeC60AZRawHolonomy S weight).map_comp,
          nativeC60AZRawHolonomy_arrow, nativeC60AZRawHolonomy_arrow,
          (nativeC60AZRawHolonomy S weight).map_id]
        change MulOpposite.op ((nativeC60AZHolonomy S weight c)⁻¹ *
          nativeC60AZHolonomy S weight c) = MulOpposite.op (1 : G)
        rw [inv_mul_cancel]
    | declared hcd =>
        rw [nativeC60AZRawHolonomy_arrow, nativeC60AZRawHolonomy_arrow]
        exact congrArg MulOpposite.op (h _ _ hcd)

def nativeC60AZStrictHolonomy (h : NativeC60AZWeightsRespect S R weight) :
    NativeC60AZStrictSpace S R ⥤ SingleObj Gᵐᵒᵖ :=
  Kuu.descend (NativeC60AZStrictRel S R) (nativeC60AZRawHolonomy S weight)
    ((nativeC60AZRawHolonomy_respects_iff S R weight).mpr h)

theorem nativeC60AZStrictHolonomy_arrow (h : NativeC60AZWeightsRespect S R weight)
    {x y : L.Total} (c : NativeC60AXStep S x y) :
    (nativeC60AZStrictHolonomy S R weight h).map (nativeC60AZStrictStep S R c) =
      MulOpposite.op (nativeC60AZHolonomy S weight c) :=
  nativeC60AZRawHolonomy_arrow S weight c

theorem nativeC60AZStrictHolonomy_iff :
    (∃ F : NativeC60AZStrictSpace S R ⥤ SingleObj Gᵐᵒᵖ,
      nativeC60AZStrictProject S R ⋙ F = nativeC60AZRawHolonomy S weight) ↔
      NativeC60AZWeightsRespect S R weight :=
  (nativeC60AZStrictObserver_iff S R _).trans
    (nativeC60AZRawHolonomy_respects_iff S R weight)

end NoncommutativeReceivers

/-- Read the NEXT actual signature, with the same dependent endpoints. -/
def nativeC60AZHigherRelations {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S)) : NativeC60AZParallelRelation S :=
  fun {x y} c d => Nonempty (T.Gen ⟨(x, y), c⟩ ⟨(x, y), d⟩)

/-- Equality of packed boundaries suffices to recover the common-boundary form;
no next generator is silently omitted because of dependent indexing. -/
theorem nativeC60AZHigherHolonomy_iff {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    {G : Type v} [Group G] (weight : ∀ {x y}, S.Gen x y → G) :
    NativeC60AZWeightsRespect S (nativeC60AZHigherRelations S T) weight ↔
      NativeC60AYRespects T (nativeC60AZInternalObserver S weight) := by
  constructor
  · intro h a b g
    rcases a with ⟨ab, c⟩
    rcases b with ⟨ab', d⟩
    have hb : ab = ab' := T.boundary g
    cases hb
    exact h c d ⟨g⟩
  · intro h x y c d hcd
    rcases hcd with ⟨g⟩
    exact h g

/-- A finite plan's final stage adds no unrequested higher relation.
False here means no optional declaration, not an identification of Kuu with absence. -/
def nativeC60AZNextRelations {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) :
    (N : Nat) → NativeC60AXPlan (nativeC60AXNext L S) N → NativeC60AZParallelRelation S
  | 0, _ => fun {a b : L.Total}
      (_c : NativeC60AXStep S a b) (_d : NativeC60AXStep S a b) => False
  | _ + 1, p => nativeC60AZHigherRelations S p.1

/-- Actual strict carrier, realization, and lower-boundary functor, not a
hypothetically supplied globally strict higher category. -/
structure NativeC60AZStrictModel {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) where
  carrier : Cat.{u, u}
  obj : L.Total → carrier
  map : ∀ {x y}, NativeC60AXStep S x y → (obj x ⟶ obj y)
  map_refl : ∀ x, map (.refl x) = 𝟙 (obj x)
  map_trans : ∀ {x y z} (c : NativeC60AXStep S x y) (d : NativeC60AXStep S y z),
    map (.trans c d) = map c ≫ map d
  map_inv_left : ∀ {x y} (c : NativeC60AXStep S x y), map c ≫ map (.symm c) = 𝟙 (obj x)
  map_inv_right : ∀ {x y} (c : NativeC60AXStep S x y), map (.symm c) ≫ map c = 𝟙 (obj y)
  map_declared : ∀ {x y} {c d : NativeC60AXStep S x y}, R c d → map c = map d
  boundary : carrier ⥤ Discrete (L.Obj × L.Obj)
  boundary_obj : ∀ x, boundary.obj (obj x) = Discrete.mk x.1

def nativeC60AZBuildStrictModel {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S) :
    NativeC60AZStrictModel S R where
  carrier := Cat.of (NativeC60AZStrictSpace S R)
  obj := fun x => (nativeC60AZStrictProject S R).obj ⟨x⟩
  map := nativeC60AZStrictStep S R
  map_refl := nativeC60AZStrictStep_refl S R
  map_trans := nativeC60AZStrictStep_comp S R
  map_inv_left := nativeC60AZStrictStep_inv_left S R
  map_inv_right := nativeC60AZStrictStep_inv_right S R
  map_declared := nativeC60AZStrictStep_declared S R
  boundary := nativeC60AZStrictBoundary S R
  boundary_obj := nativeC60AZStrictBoundary_obj S R

/-- A genuinely dependent sequence of constructed strict realizations.
This does not assert the still-missing cross-dimensional interchange. -/
def NativeC60AZFiniteStrictModels :
    (L : NativeC60AXLayer.{u}) → (N : Nat) → NativeC60AXPlan L N → Type (u + 1)
  | _, 0, _ => PUnit
  | L, N + 1, p =>
      NativeC60AZStrictModel p.1 (nativeC60AZNextRelations p.1 N p.2) ×
        NativeC60AZFiniteStrictModels (nativeC60AXNext L p.1) N p.2

def nativeC60AZFiniteStrictModels :
    (L : NativeC60AXLayer.{u}) → (N : Nat) → (p : NativeC60AXPlan L N) →
      NativeC60AZFiniteStrictModels L N p
  | _, 0, _ => PUnit.unit
  | L, N + 1, p =>
      ⟨nativeC60AZBuildStrictModel p.1 (nativeC60AZNextRelations p.1 N p.2),
        nativeC60AZFiniteStrictModels (nativeC60AXNext L p.1) N p.2⟩

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

/-- Every finite original C60 plan, including independently selected Kuu data. -/
def nativeK5AZFiniteStrictModels (W : NativeK5StructuralThirteenCell p U V)
    (N : Nat) (plan : NativeC60AXPlan (nativeK5AXBaseLayer W) N) :
    NativeC60AZFiniteStrictModels (nativeK5AXBaseLayer W) N plan :=
  nativeC60AZFiniteStrictModels _ _ plan

/-- Concrete nontrivial physical label survives the STRUCTURAL strict laws.
No assertion that arbitrary optional higher relations preserve this label. -/
theorem nativeK5AZStrictPhysicalLabel_survives (W : NativeK5StructuralThirteenCell p U V) :
    let S := nativeK5AXKuuSignature W
    let R : NativeC60AZParallelRelation S := fun {_ _} _ _ => False
    let weight : ∀ {x y}, S.Gen x y → NativeK5ASPeifferKernel W :=
      nativeC60AZConstantWeight S (nativeK5ASPhysicalDefect W [])
    let h : NativeC60AZWeightsRespect S R weight := by intro x y c d h; exact h.elim
    (nativeC60AZStrictHolonomy S R weight h).map
      (nativeC60AZStrictStep S R
        (nativeK5AXDeclaredNaturality W (nativeK5AQExchange W []))) ≠ 1 := by
  dsimp only
  rw [nativeC60AZStrictHolonomy_arrow]
  change (MulOpposite.op (nativeK5ASPhysicalDefect W []) :
    (NativeK5ASPeifferKernel W)ᵐᵒᵖ) ≠ 1
  intro heq
  exact nativeK5ASPhysicalDefect_base_ne_one W
    (congrArg MulOpposite.unop heq)

end PhysicalC60

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

def nativeC60AZFiveStageStrictModels (N : Nat) :=
  nativeK5AZFiniteStrictModels
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5) N
    (nativeC60AXFiveStageFinitePlan t1 t2 t3 t4 t5 N)

end GenuineFiveStage

#print axioms NativeC60AZStrictObj
#print axioms nativeC60AZStrictQuiver
#print axioms nativeC60AZRawArrow
#print axioms NativeC60AZParallelRelation
#print axioms NativeC60AZStrictRel
#print axioms NativeC60AZStrictSpace
#print axioms nativeC60AZStrictProject
#print axioms nativeC60AZStrictStep
#print axioms nativeC60AZStrictStep_refl
#print axioms nativeC60AZStrictStep_comp
#print axioms nativeC60AZStrictStep_inv_left
#print axioms nativeC60AZStrictStep_inv_right
#print axioms nativeC60AZStrictStep_declared
#print axioms nativeC60AZStrictStep_exact
#print axioms nativeC60AZStrictObj_injective
#print axioms nativeC60AZStrictStep_assoc
#print axioms nativeC60AZBoundaryPrefunctor
#print axioms nativeC60AZStrictBoundary
#print axioms nativeC60AZStrictBoundary_obj
#print axioms nativeC60AZStrictObserver_iff
#print axioms nativeC60AZStrictObserver_unique
#print axioms nativeC60AZStrictComparison
#print axioms nativeC60AZStrictComparison_comp
#print axioms nativeC60AZStrictComparison_id
#print axioms nativeC60AZStrictInterchange
#print axioms nativeC60AZHolonomyPrefunctor
#print axioms nativeC60AZRawHolonomy
#print axioms nativeC60AZRawHolonomy_arrow
#print axioms NativeC60AZWeightsRespect
#print axioms nativeC60AZRawHolonomy_respects_iff
#print axioms nativeC60AZStrictHolonomy
#print axioms nativeC60AZStrictHolonomy_arrow
#print axioms nativeC60AZStrictHolonomy_iff
#print axioms nativeC60AZHigherRelations
#print axioms nativeC60AZHigherHolonomy_iff
#print axioms nativeC60AZNextRelations
#print axioms NativeC60AZStrictModel
#print axioms nativeC60AZBuildStrictModel
#print axioms NativeC60AZFiniteStrictModels
#print axioms nativeC60AZFiniteStrictModels
#print axioms nativeK5AZFiniteStrictModels
#print axioms nativeK5AZStrictPhysicalLabel_survives
#print axioms nativeC60AZFiveStageStrictModels

end
end Kuu.F112.Physical
