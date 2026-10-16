import KUOS.DependentOriginationGlobalDuskinLocalTwoCellComparisonV1_24

namespace KUOS.DependentOriginationPresentationIndependentInvariantV1_25

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Simplicial
open Opposite
open scoped Bicategory
open KUOS.DependentOriginationInfinityTwoYonedaV1_18
open KUOS.DependentOriginationCompleteSegalInfinityTwoV1_20
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinLocalMappingComparisonV1_23
open KUOS.DependentOriginationGlobalDuskinLocalTwoCellComparisonV1_24

universe u v w z

/-!
# Presentation-independent invariant kernel v1.25

The previous layers compare two concrete higher-categorical presentations of the
same bicategory:

* the local presentation `mappingNerve X Y = N(B(X,Y))`;
* the global scaled Duskin presentation.

The correct next step is not to declare either presentation to be the invariant.
The presentation-independent carrier is the intrinsic bicategorical data itself:

```text
objects                  B
mapping invariant        B(X,Y)
1-cell equivalence       adjoint equivalence / isomorphism in B(X,Y)
2-cell invertibility     IsIso
```

This file proves that the local nerve and the global Duskin data commute with
that intrinsic carrier in dimensions one and two.  Consequently every
observable that factors through the intrinsic carrier has the same value in
both presentations.

At object level, under the already explicit hypotheses of object univalence and
global edge representability, paths, local equivalence vertices, and global
Duskin equivalence edges all detect the same intrinsic adjoint-equivalence
relation.

This is a genuine presentation-independent invariant *kernel*.  It is not yet a
proof that the complete local and global `(∞,2)` presentations are equivalent in
all simplicial degrees.
-/

/-! ## Intrinsic bicategorical carrier -/

/-- The presentation-independent mapping invariant between two objects is the native hom-category. -/
abbrev PresentationIndependentMappingInvariant
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) :=
  X ⟶ Y

/-- Intrinsic object equivalence, before choosing any simplicial presentation. -/
def IntrinsicObjectEquivalent
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) : Prop :=
  Nonempty (X ≌ Y)

/-- A 1-morphism is intrinsically an equivalence when it is the forward map of an adjoint equivalence. -/
def IntrinsicEquivalenceOneCell
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (f : X ⟶ Y) : Prop :=
  ∃ q : X ≌ Y, q.hom = f

/-- Parallel 1-morphisms are intrinsically equivalent when they are isomorphic in the hom-category. -/
def IntrinsicOneCellsEquivalent
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (f g : X ⟶ Y) : Prop :=
  Nonempty (f ≅ g)

/-- Intrinsic invertibility of a bicategorical 2-cell. -/
def IntrinsicInvertibleTwoCell
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B} {f g : X ⟶ Y}
    (α : f ⟶ g) : Prop :=
  IsIso α

/-! ## Local and global observations into the same invariant -/

/-- Read a local mapping-nerve vertex as the intrinsic 1-morphism it represents. -/
def localOneCellInvariant
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (x : MappingNerveVertex X Y) :
    PresentationIndependentMappingInvariant X Y :=
  mappingNerveVertexEquiv X Y x

/-- Read a fixed-endpoint global Duskin edge as the intrinsic 1-morphism it represents. -/
def globalOneCellInvariant
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y) :
    PresentationIndependentMappingInvariant X Y :=
  e.toArrow

/-- The local image of a global edge and the global edge itself have the same intrinsic 1-cell. -/
@[simp] theorem globalEdge_localVertex_invariant_agree
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (e : GlobalDuskinEdgeOver B X Y) :
    localOneCellInvariant e.toMappingVertex = globalOneCellInvariant e := by
  simpa [localOneCellInvariant, globalOneCellInvariant] using
    (GlobalDuskinEdgeOver.mappingNerveVertexEquiv_toMappingVertex e)

/-- Read a local mapping-nerve edge as the intrinsic bicategorical 2-morphism it represents. -/
def localTwoCellInvariant
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B} {f g : X ⟶ Y}
    (e : MappingNerveEdge X Y f g) : f ⟶ g :=
  CategoryTheory.nerve.homEquiv e

/-- Read a global Duskin 2-simplex as its intrinsic normal-lax comparison 2-cell. -/
def globalTwoCellInvariant
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) :
    duskinTriangleCompositeArrow σ ⟶ duskinTriangleLongArrow σ :=
  duskinComparison σ

/-- The local edge extracted from a global triangle and the global comparison have the same intrinsic 2-cell. -/
@[simp] theorem globalTriangle_localEdge_invariant_agree
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2) :
    localTwoCellInvariant (duskinComparisonMappingEdge σ) = globalTwoCellInvariant σ := by
  simpa [localTwoCellInvariant, globalTwoCellInvariant] using
    (duskinComparisonMappingEdge_hom σ)

/-! ## Universal observable independence -/

/--
Every observable on the intrinsic 1-cell carrier has identical values on the
local and global presentations of the same global edge.
-/
theorem oneCellObservable_presentationIndependent
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    {Z : Sort z}
    (F : PresentationIndependentMappingInvariant X Y → Z)
    (e : GlobalDuskinEdgeOver B X Y) :
    F (localOneCellInvariant e.toMappingVertex) =
      F (globalOneCellInvariant e) := by
  exact congrArg F (globalEdge_localVertex_invariant_agree e)

/--
Every observable on the intrinsic 2-cell carrier has identical values on the
local and global presentations of the same Duskin comparison cell.
-/
theorem twoCellObservable_presentationIndependent
    {B : Type u} [Bicategory.{w, v} B]
    {Z : Sort z}
    (σ : DuskinSimplex B 2)
    (F : (duskinTriangleCompositeArrow σ ⟶ duskinTriangleLongArrow σ) → Z) :
    F (localTwoCellInvariant (duskinComparisonMappingEdge σ)) =
      F (globalTwoCellInvariant σ) := by
  exact congrArg F (globalTriangle_localEdge_invariant_agree σ)

/-- The proposition-valued form of one-cell presentation independence. -/
theorem oneCellPredicate_presentationIndependent
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (P : PresentationIndependentMappingInvariant X Y → Prop)
    (e : GlobalDuskinEdgeOver B X Y) :
    P (localOneCellInvariant e.toMappingVertex) ↔
      P (globalOneCellInvariant e) := by
  rw [globalEdge_localVertex_invariant_agree]

/-- The proposition-valued form of two-cell presentation independence. -/
theorem twoCellPredicate_presentationIndependent
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2)
    (P : (duskinTriangleCompositeArrow σ ⟶ duskinTriangleLongArrow σ) → Prop) :
    P (localTwoCellInvariant (duskinComparisonMappingEdge σ)) ↔
      P (globalTwoCellInvariant σ) := by
  rw [globalTriangle_localEdge_invariant_agree]

/-! ## Intrinsic invertibility and global scaling -/

/--
For a nondegenerate Duskin triangle, global scaling is exactly intrinsic
invertibility of the comparison 2-cell.  The statement no longer mentions the
local nerve at all.
-/
theorem nondegenerate_globalThin_iff_intrinsicInvertible
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2)
    (hnd : ¬ IsDegenerateDuskinTwoSimplex σ) :
    (duskinScaling B).thin σ ↔
      IntrinsicInvertibleTwoCell (globalTwoCellInvariant σ) := by
  change
    (IsIso (duskinComparison σ) ∨ IsDegenerateDuskinTwoSimplex σ) ↔
      IsIso (duskinComparison σ)
  constructor
  · intro h
    rcases h with h | h
    · exact h
    · exact False.elim (hnd h)
  · intro h
    exact Or.inl h

/-- The same thinness test expressed through the local mapping presentation. -/
theorem nondegenerate_globalThin_iff_localInvariantInvertible
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2)
    (hnd : ¬ IsDegenerateDuskinTwoSimplex σ) :
    (duskinScaling B).thin σ ↔
      IntrinsicInvertibleTwoCell
        (localTwoCellInvariant (duskinComparisonMappingEdge σ)) := by
  simpa [IntrinsicInvertibleTwoCell, localTwoCellInvariant] using
    (nondegenerate_duskinThin_iff_localMappingComparisonIso σ hnd)

/-! ## Local presentation recovers intrinsic 1-cell isomorphism exactly -/

/-- A local mapping presentation witnesses an invertible 2-cell between `f` and `g`. -/
def HasLocalInvertibleMappingEdge
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (f g : X ⟶ Y) : Prop :=
  ∃ e : MappingNerveEdge X Y f g,
    IntrinsicInvertibleTwoCell (localTwoCellInvariant e)

/-- Local invertible mapping edges detect exactly isomorphism in the intrinsic hom-category. -/
theorem hasLocalInvertibleMappingEdge_iff_intrinsicOneCellsEquivalent
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (f g : X ⟶ Y) :
    HasLocalInvertibleMappingEdge f g ↔
      IntrinsicOneCellsEquivalent f g := by
  constructor
  · rintro ⟨e, he⟩
    change IsIso (CategoryTheory.nerve.homEquiv e) at he
    letI : IsIso (CategoryTheory.nerve.homEquiv e) := he
    exact ⟨asIso (CategoryTheory.nerve.homEquiv e)⟩
  · rintro ⟨i⟩
    refine ⟨localMappingEdgeOfTwoMorphism i.hom, ?_⟩
    change IsIso
      (CategoryTheory.nerve.homEquiv
        (localMappingEdgeOfTwoMorphism i.hom))
    simpa using (inferInstance : IsIso i.hom)

/-- Every nondegenerate globally thin triangle therefore witnesses intrinsic 1-cell equivalence. -/
theorem nondegenerate_globalThin_implies_intrinsicOneCellsEquivalent
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2)
    (hnd : ¬ IsDegenerateDuskinTwoSimplex σ)
    (hthin : (duskinScaling B).thin σ) :
    IntrinsicOneCellsEquivalent
      (duskinTriangleCompositeArrow σ)
      (duskinTriangleLongArrow σ) := by
  have hi : IsIso (duskinComparison σ) := by
    exact (nondegenerate_globalThin_iff_intrinsicInvertible σ hnd).mp hthin
  letI : IsIso (duskinComparison σ) := hi
  exact ⟨asIso (duskinComparison σ)⟩

/-- Hence every nondegenerate globally thin triangle produces an invertible local mapping edge. -/
theorem nondegenerate_globalThin_implies_localInvertibleMappingEdge
    {B : Type u} [Bicategory.{w, v} B]
    (σ : DuskinSimplex B 2)
    (hnd : ¬ IsDegenerateDuskinTwoSimplex σ)
    (hthin : (duskinScaling B).thin σ) :
    HasLocalInvertibleMappingEdge
      (duskinTriangleCompositeArrow σ)
      (duskinTriangleLongArrow σ) := by
  exact
    (hasLocalInvertibleMappingEdge_iff_intrinsicOneCellsEquivalent
      (duskinTriangleCompositeArrow σ)
      (duskinTriangleLongArrow σ)).mpr
      (nondegenerate_globalThin_implies_intrinsicOneCellsEquivalent σ hnd hthin)

/-! ## Object-equivalence invariant across paths, local vertices, and global edges -/

/-- The local mapping presentation contains a vertex representing an adjoint equivalence. -/
def HasLocalEquivalenceVertex
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) : Prop :=
  ∃ x : MappingNerveVertex X Y,
    IntrinsicEquivalenceOneCell (localOneCellInvariant x)

/-- Local equivalence vertices detect exactly intrinsic adjoint equivalence of objects. -/
theorem hasLocalEquivalenceVertex_iff_intrinsicObjectEquivalent
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) :
    HasLocalEquivalenceVertex X Y ↔ IntrinsicObjectEquivalent X Y := by
  constructor
  · rintro ⟨x, q, hq⟩
    exact ⟨q⟩
  · rintro ⟨q⟩
    refine ⟨(mappingNerveVertexEquiv X Y).symm q.hom, q, ?_⟩
    exact (Equiv.apply_symm_apply (mappingNerveVertexEquiv X Y) q.hom).symm

/-- The global Duskin presentation contains a fixed-endpoint equivalence edge. -/
def HasGlobalDuskinEquivalenceEdge
    {B : Type u} [Bicategory.{w, v} B]
    (X Y : B) : Prop :=
  ∃ e : GlobalDuskinEdgeOver B X Y,
    IsGlobalDuskinEquivalenceEdge e

/-- Under exact edge representability, global equivalence edges detect exactly intrinsic object equivalence. -/
theorem hasGlobalDuskinEquivalenceEdge_iff_intrinsicObjectEquivalent
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y) :
    HasGlobalDuskinEquivalenceEdge X Y ↔ IntrinsicObjectEquivalent X Y := by
  constructor
  · rintro ⟨e, q, hq⟩
    exact ⟨q⟩
  · rintro ⟨q⟩
    exact
      ⟨globalEdgeOfEquivalence R q,
        globalEdgeOfEquivalence_isEquivalenceEdge R q⟩

/-- Local and global object-equivalence witnesses agree once global edges are representable. -/
theorem local_global_objectEquivalenceInvariant_agree
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y) :
    HasLocalEquivalenceVertex X Y ↔
      HasGlobalDuskinEquivalenceEdge X Y := by
  exact
    (hasLocalEquivalenceVertex_iff_intrinsicObjectEquivalent X Y).trans
      (hasGlobalDuskinEquivalenceEdge_iff_intrinsicObjectEquivalent R).symm

/-- Under object univalence, equality paths detect exactly intrinsic adjoint equivalence. -/
theorem objectPath_iff_intrinsicObjectEquivalent
    {B : Type u} [Bicategory.{w, v} B]
    (U : ObjectUnivalence B)
    (X Y : B) :
    (X = Y) ↔ IntrinsicObjectEquivalent X Y := by
  constructor
  · intro p
    exact ⟨U.pathEquiv X Y p⟩
  · rintro ⟨q⟩
    exact (U.pathEquiv X Y).symm q

/-- Under univalence, paths and local equivalence vertices detect the same invariant. -/
theorem objectPath_iff_localEquivalenceVertex
    {B : Type u} [Bicategory.{w, v} B]
    (U : ObjectUnivalence B)
    (X Y : B) :
    (X = Y) ↔ HasLocalEquivalenceVertex X Y := by
  exact
    (objectPath_iff_intrinsicObjectEquivalent U X Y).trans
      (hasLocalEquivalenceVertex_iff_intrinsicObjectEquivalent X Y).symm

/-- Under univalence and edge representability, paths and global equivalence edges agree. -/
theorem objectPath_iff_globalDuskinEquivalenceEdge
    {B : Type u} [Bicategory.{w, v} B]
    (U : ObjectUnivalence B)
    {X Y : B}
    (R : GlobalDuskinEdgeRepresentability B X Y) :
    (X = Y) ↔ HasGlobalDuskinEquivalenceEdge X Y := by
  exact
    (objectPath_iff_intrinsicObjectEquivalent U X Y).trans
      (hasGlobalDuskinEquivalenceEdge_iff_intrinsicObjectEquivalent R).symm

/-! ## Bundled invariant certificates -/

/--
The automatic two-skeleton presentation-independent kernel supplied by every
bicategory.  It records the commuting one- and two-cell observations and the
intrinsic interpretation of nondegenerate scaling.
-/
structure PresentationIndependentTwoSkeletonKernel
    (B : Type u) [Bicategory.{w, v} B] : Prop where
  one_cell_agreement :
    ∀ {X Y : B} (e : GlobalDuskinEdgeOver B X Y),
      localOneCellInvariant e.toMappingVertex = globalOneCellInvariant e
  two_cell_agreement :
    ∀ σ : DuskinSimplex B 2,
      localTwoCellInvariant (duskinComparisonMappingEdge σ) = globalTwoCellInvariant σ
  nondegenerate_scaling_intrinsic :
    ∀ σ : DuskinSimplex B 2,
      ¬ IsDegenerateDuskinTwoSimplex σ →
      ((duskinScaling B).thin σ ↔
        IntrinsicInvertibleTwoCell (globalTwoCellInvariant σ))

/-- Every bicategory canonically has the two-skeleton presentation-independent invariant kernel. -/
def presentationIndependentTwoSkeletonKernel
    (B : Type u) [Bicategory.{w, v} B] :
    PresentationIndependentTwoSkeletonKernel B where
  one_cell_agreement := globalEdge_localVertex_invariant_agree
  two_cell_agreement := globalTriangle_localEdge_invariant_agree
  nondegenerate_scaling_intrinsic := nondegenerate_globalThin_iff_intrinsicInvertible

/--
A complete object-level presentation-independent kernel: paths, local
mapping-nerve equivalence vertices, and global Duskin equivalence edges all
classify the same object-equivalence relation.
-/
structure PresentationIndependentCompleteObjectKernel
    (B : Type u) [Bicategory.{w, v} B] : Prop where
  path_iff_local :
    ∀ X Y : B, (X = Y) ↔ HasLocalEquivalenceVertex X Y
  path_iff_global :
    ∀ X Y : B, (X = Y) ↔ HasGlobalDuskinEquivalenceEdge X Y
  local_iff_global :
    ∀ X Y : B,
      HasLocalEquivalenceVertex X Y ↔ HasGlobalDuskinEquivalenceEdge X Y

/-- Object univalence plus all-pairs edge representability yields the complete object invariant kernel. -/
def presentationIndependentCompleteObjectKernel
    {B : Type u} [Bicategory.{w, v} B]
    (U : ObjectUnivalence B)
    (C : GlobalDuskinLocalOneSkeletonComparison B) :
    PresentationIndependentCompleteObjectKernel B where
  path_iff_local := objectPath_iff_localEquivalenceVertex U
  path_iff_global := fun X Y =>
    objectPath_iff_globalDuskinEquivalenceEdge U (C.edge_representability X Y)
  local_iff_global := fun X Y =>
    local_global_objectEquivalenceInvariant_agree (C.edge_representability X Y)

/-!
The proved invariant chain after v1.25 is:

```text
                          intrinsic bicategory B
                                   |
                 +-----------------+-----------------+
                 |                                   |
        local mapping nerve                    global Duskin
                 |                                   |
      vertex -> 1-morphism             fixed edge -> 1-morphism
        edge -> 2-morphism        triangle comparison -> 2-morphism
                 |                                   |
                 +--------- same intrinsic data -----+

nondegenerate global thinness
  <-> intrinsic comparison 2-cell is invertible

ObjectUnivalence + global edge representability
  -> path existence
     <-> local equivalence vertex
     <-> intrinsic adjoint equivalence
     <-> global Duskin equivalence edge
```

The universal observable theorems are the key presentation-independent
statement: any invariant defined *after* passing to the intrinsic bicategorical
carrier is automatically insensitive to whether the input was presented
locally or globally.

Still open:

* reverse representability of all local 2-cells by controlled global triangles;
* a global mapping simplicial object in every degree;
* a full local/global simplicial equivalence compatible with composition,
  scaling, and scaled horn fillers;
* model-independent invariance under equivalence between genuinely different
  bicategory presentations, rather than two presentations of the same `B`.
-/

end KUOS.DependentOriginationPresentationIndependentInvariantV1_25
