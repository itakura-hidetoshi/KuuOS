import KUOS.DependentOriginationC60KuuPhysicalOverlapObstructionV5_259
import KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223

namespace KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60KuuPhysicalOverlapObstructionV5_259
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuObservedContextPentagonV5_257

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.260 / F106 — ACTUAL C60 incidence overlap categories and conditional restriction

The ORIGINAL geometric C60 has 60 dart vertices, 90 physical edges,
32 genuine polygon faces and 360 incidence flags (F69). F105's
different-patch descent deliberately left the common overlap O and
its restriction functors as external data.

This stage CONSTRUCTS the geometric overlap as an actual full
subcategory of the F69 incidence POSet: for every physical edge e,
its incidence star consists precisely of those genuine vertices,
edges and faces comparable with e. A finite family of physical
patch indices gives the INTERSECTION of their real incidence stars.
Overlap refinement J subset I induces a genuine Mathlib functor
O_I -> O_J (not an arbitrary assumed comparison).

Actual shared physical endpoints and actually incident polygon
faces provide explicit objects in pair overlaps; no invented
quadrilateral C60 surface faces or synthetic overlap sites appear.

The missing SEMANTIC action of actual F42/F51/F95 presentations
along arbitrary incidence morphisms remains an EXPLICIT input:
a functor from the SINGLE-patch star to the patch's own original
F95 Kuu quotient category. Without such data there is no
canonical nontrivial functor from geometry to source 3-Homs.
All multi-patch restrictions are DERIVED from genuine incidence
overlap refinement and those supplied single-patch semantics.

For any finite intersection the pairwise source charge defect
is an actual Int x Int difference on genuine overlap morphisms.
It obeys skew-symmetry and the triple cocycle without flatness.
Observed-object equality AND zero defect on every Hom guarantee
a true Mathlib F77 natural isomorphism; nonzero defect obstructs
zero-added-charge comparison. With supplied multi-patch
compatibility, the actual overlap natural comparisons satisfy
strict Cech cocycle coherence.

The F68 nonzero north-pentagon physical curvature and its
original F55 obstruction remain separate. This DOES NOT
assert a full C60 sheaf, a global F42 lift, or hyperdescent.
-/

/-! ## I. Native incidence stars and ALL finite geometric overlaps -/

/-- The exact incidence star of a real C60 physical edge:
an ORIGINAL cell is either a boundary cell or a coface of that edge. -/
def c60F106IncidenceStar
    (edge : TruncatedIcosahedralEdge)
    (site : C60F69PhysicalCellSite) : Prop :=
  site ≤ C60F69PhysicalCellSite.edge edge ∨
    C60F69PhysicalCellSite.edge edge ≤ site

/-- A finite chart collection has the INTERSECTION of all its
real edge-incidence stars. This is a genuine subtype of F69's
original partial-order category, including the empty family. -/
abbrev C60F106PhysicalOverlap
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (I : Finset (Fin n)) :=
  {site : C60F69PhysicalCellSite //
    ∀ i ∈ I, c60F106IncidenceStar (A.edge i) site}

/-- Physical overlap refinement is a real Mathlib functor.
If J subset I, a site of every star in I is still in every star
in J; there is NO new semantic functor assumed here. -/
def c60F106OverlapRestrict
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    {I J : Finset (Fin n)} (h : J ⊆ I) :
    C60F106PhysicalOverlap A I ⥤ C60F106PhysicalOverlap A J where
  obj X := ⟨X.1, fun i hi => X.2 i (h hi)⟩
  map := fun {_ _} f => CategoryTheory.homOfLE (CategoryTheory.leOfHom f)
  map_id := by
    intro X
    apply Subsingleton.elim
  map_comp := by
    intro X Y Z f g
    apply Subsingleton.elim

/-- Each REAL overlap restriction preserves the underlying
ORIGINAL physical cell, not merely its image in a synthetic nerve. -/
theorem c60F106OverlapRestrict_site
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    {I J : Finset (Fin n)} (h : J ⊆ I)
    (X : C60F106PhysicalOverlap A I) :
    ((c60F106OverlapRestrict A h).obj X).1 = X.1 := rfl

/-- Restriction of an actual physical overlap is independent of
inserting an intermediate finite subcover, on EVERY real cell. -/
theorem c60F106OverlapRestrict_trans_obj
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    {I J K : Finset (Fin n)} (hJI : J ⊆ I) (hKJ : K ⊆ J)
    (X : C60F106PhysicalOverlap A I) :
    ((c60F106OverlapRestrict A hJI ⋙
      c60F106OverlapRestrict A hKJ).obj X) =
    (c60F106OverlapRestrict A (Finset.Subset.trans hKJ hJI)).obj X := rfl

/-- Physical refinement also preserves ALL incidence arrows:
the triangle of native overlap functors commutes on actual Hom. -/
theorem c60F106OverlapRestrict_trans_map
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    {I J K : Finset (Fin n)} (hJI : J ⊆ I) (hKJ : K ⊆ J)
    {X Y : C60F106PhysicalOverlap A I} (f : X ⟶ Y) :
    (c60F106OverlapRestrict A hJI ⋙
      c60F106OverlapRestrict A hKJ).map f =
    (c60F106OverlapRestrict A (Finset.Subset.trans hKJ hJI)).map f := by
  apply Subsingleton.elim

/-- The genuine one-patch star is a subcover of ANY overlap
whose selected patch index occurs in the finite intersection. -/
theorem c60F106Singleton_subset
    {n : Nat} (I : Finset (Fin n))
    (i : Fin n) (hi : i ∈ I) :
    ({i} : Finset (Fin n)) ⊆ I := by
  intro j hj
  have hji : j = i := Finset.mem_singleton.mp hj
  subst j
  exact hi

/-- The singleton-patch restriction is forced by the exact
finite incidence-star intersection, NOT a fabricated patch map. -/
def c60F106ToSingleton
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (I : Finset (Fin n)) (i : Fin n) (hi : i ∈ I) :
    C60F106PhysicalOverlap A I ⥤
      C60F106PhysicalOverlap A ({i} : Finset (Fin n)) :=
  c60F106OverlapRestrict A (c60F106Singleton_subset I i hi)

/-! ## II. Concrete NONEMPTY physical overlaps: endpoints and faces -/

/-- Two genuine C60 edges sharing one actual dart endpoint have
a NONEMPTY geometric pair intersection in the physical F69 nerve. -/
theorem c60F106SharedEndpoint_overlap_nonempty
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (i j : Fin n) (v : IcosahedralDart)
    (hi : v = (truncatedIcosahedralEdgeEndpoints (A.edge i)).1 ∨
      v = (truncatedIcosahedralEdgeEndpoints (A.edge i)).2)
    (hj : v = (truncatedIcosahedralEdgeEndpoints (A.edge j)).1 ∨
      v = (truncatedIcosahedralEdgeEndpoints (A.edge j)).2) :
    Nonempty (C60F106PhysicalOverlap A ({i, j} : Finset (Fin n))) := by
  refine ⟨⟨.vertex v, ?_⟩⟩
  intro k hk
  rcases Finset.mem_insert.mp hk with hki | hkj
  · subst k
    exact Or.inl (c60F69PhysicalVertexEdge v (A.edge i) hi)
  · have hkj' : k = j := Finset.mem_singleton.mp hkj
    subst k
    exact Or.inl (c60F69PhysicalVertexEdge v (A.edge j) hj)

/-- If two ACTUAL C60 edges border the same original pentagon or
hexagon, that polygon face lies in their common incidence star.
No imaginary quadrilateral face was added. -/
theorem c60F106SharedFace_overlap_nonempty
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (i j : Fin n) (face : TruncatedIcosahedralSeedFace)
    (hi : truncatedEdgeOnSeedFace (A.edge i) face)
    (hj : truncatedEdgeOnSeedFace (A.edge j) face) :
    Nonempty (C60F106PhysicalOverlap A ({i, j} : Finset (Fin n))) := by
  refine ⟨⟨.face face, ?_⟩⟩
  intro k hk
  rcases Finset.mem_insert.mp hk with hki | hkj
  · subst k
    exact Or.inr (c60F69PhysicalEdgeFace (A.edge i) face hi)
  · have hkj' : k = j := Finset.mem_singleton.mp hkj
    subst k
    exact Or.inr (c60F69PhysicalEdgeFace (A.edge j) face hj)

/-- All four genuine flags at a C60 edge are visible in its
physical star: the two endpoint vertices and two distinct
incident polygonal faces. -/
theorem c60F106AllPhysicalFlags_in_star
    (edge : TruncatedIcosahedralEdge) (endpoint side : Bool) :
    c60F106IncidenceStar edge
      (.vertex ((c60F46PhysicalFourFlagSquare edge).vertex endpoint)) ∧
    c60F106IncidenceStar edge
      (.face (c60F48AdjacentRealFace edge side)) := by
  constructor
  · exact Or.inl (c60F69PhysicalVertexEdge
      _ edge (c60F69ActualFlagEndpoint edge endpoint))
  · exact Or.inr (c60F69PhysicalEdgeFace
      edge _ (c60F48AdjacentRealFace_incident edge side))

/-! ## III. Actual overlap restriction to ORIGINAL F95 local quotient categories -/

/-- Additional SEMANTIC information not supplied by incidence alone:
a genuine functor from each one-edge physical star category to
its independently typed original F95 quotient Hom category.
This explicitly prevents claiming an unproved F42/F55 lift. -/
structure C60F106SingletonF95Semantics
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n) where
  patch : (i : Fin n) →
    C60F106PhysicalOverlap A ({i} : Finset (Fin n)) ⥤
      C60F95LocalKuuQuotient (A.p i) (A.q i)

/-- On a genuine finite multi-edge overlap, the restriction
to patch i is now DERIVED, not supplied independently for
every intersection: native geometric refinement followed by
the supplied SINGLE-PATCH semantic functor. -/
def c60F106PhysicalToF95
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) (i : Fin n) (hi : i ∈ I) :
    C60F106PhysicalOverlap A I ⥤
      C60F95LocalKuuQuotient (A.p i) (A.q i) :=
  c60F106ToSingleton A I i hi ⋙ S.patch i

/-- Each actual geometric-overlap restriction is interpreted by
the ORIGINAL F95-to-F77 quotient observer of that precise
physical edge; the original two integer charges are retained. -/
def c60F106PhysicalObserved
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) (i : Fin n) (hi : i ∈ I) :
    C60F106PhysicalOverlap A I ⥤ C60F77NativeQuotient :=
  c60F106PhysicalToF95 A S I i hi ⋙
    c60F95DescendedToF77 (A.p i) (A.q i)

/-! ## IV. Actual overlap charge defects and conditional NatIso descent -/

/-- Signed BOTH-coordinate integer-charge disagreement for true
overlap incidence ARROWS, with no flatness or object assumption. -/
def c60F106PhysicalChargeDefect
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) (i j : Fin n)
    (hi : i ∈ I) (hj : j ∈ I)
    {X Y : C60F106PhysicalOverlap A I} (f : X ⟶ Y) : Int × Int :=
  (c60F77QuotientToStrictCharge.map
    ((c60F106PhysicalObserved A S I i hi).map f)).charge -
  (c60F77QuotientToStrictCharge.map
    ((c60F106PhysicalObserved A S I j hj).map f)).charge

/-- Unconditional antisymmetry of the REAL overlap defect. -/
theorem c60F106PhysicalChargeDefect_skew
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) (i j : Fin n)
    (hi : i ∈ I) (hj : j ∈ I)
    {X Y : C60F106PhysicalOverlap A I} (f : X ⟶ Y) :
    c60F106PhysicalChargeDefect A S I i j hi hj f =
      -c60F106PhysicalChargeDefect A S I j i hj hi f := by
  unfold c60F106PhysicalChargeDefect
  abel

/-- An honest signed 1-cocycle for the three RESTRICTED F95
observations on any genuinely common C60 physical overlap.
It holds independently of any gluing/existence hypotheses. -/
theorem c60F106PhysicalChargeDefect_cocycle
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) (i j k : Fin n)
    (hi : i ∈ I) (hj : j ∈ I) (hk : k ∈ I)
    {X Y : C60F106PhysicalOverlap A I} (f : X ⟶ Y) :
    c60F106PhysicalChargeDefect A S I i j hi hj f +
      c60F106PhysicalChargeDefect A S I j k hj hk f =
        c60F106PhysicalChargeDefect A S I i k hi hk f := by
  unfold c60F106PhysicalChargeDefect
  abel

/-- The defect zero test is exactly equality of both ORIGINAL
integral charges on the genuinely shared F69 incidence Hom. -/
theorem c60F106PhysicalChargeDefect_zero_iff
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) (i j : Fin n)
    (hi : i ∈ I) (hj : j ∈ I)
    {X Y : C60F106PhysicalOverlap A I} (f : X ⟶ Y) :
    c60F106PhysicalChargeDefect A S I i j hi hj f = (0 : Int × Int) ↔
      (c60F77QuotientToStrictCharge.map
        ((c60F106PhysicalObserved A S I i hi).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F106PhysicalObserved A S I j hj).map f)).charge :=
  sub_eq_zero

/-- Under equality of OBSERVED F77 objects and genuine zero
charge defect on every overlap 3-arrow, construct a proper
Mathlib natural isomorphism. We never equate original F42 objects. -/
def c60F106ConditionalPhysicalNatIso
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) (i j : Fin n)
    (hi : i ∈ I) (hj : j ∈ I)
    (hObj : ∀ X : C60F106PhysicalOverlap A I,
      (c60F106PhysicalObserved A S I i hi).obj X =
        (c60F106PhysicalObserved A S I j hj).obj X)
    (hDef : ∀ {X Y : C60F106PhysicalOverlap A I} (f : X ⟶ Y),
      c60F106PhysicalChargeDefect A S I i j hi hj f = (0 : Int × Int)) :
    c60F106PhysicalObserved A S I i hi ≅
      c60F106PhysicalObserved A S I j hj :=
  NatIso.ofComponents
    (fun X => eqToIso (hObj X))
    (by
      intro X Y f
      change
        (c60F106PhysicalObserved A S I i hi).map f ≫ eqToHom (hObj Y) =
          eqToHom (hObj X) ≫ (c60F106PhysicalObserved A S I j hj).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact (c60F106PhysicalChargeDefect_zero_iff A S I i j hi hj f).mp
        (hDef f))

/-- Any actual conditional physical-overlap comparison adds zero
integer charge but does not assume the INPUT charge is zero. -/
theorem c60F106ConditionalPhysicalNatIso_charge_zero
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) (i j : Fin n)
    (hi : i ∈ I) (hj : j ∈ I)
    (hObj : ∀ X : C60F106PhysicalOverlap A I,
      (c60F106PhysicalObserved A S I i hi).obj X =
        (c60F106PhysicalObserved A S I j hj).obj X)
    (hDef : ∀ {X Y : C60F106PhysicalOverlap A I} (f : X ⟶ Y),
      c60F106PhysicalChargeDefect A S I i j hi hj f = (0 : Int × Int))
    (X : C60F106PhysicalOverlap A I) :
    (c60F77QuotientToStrictCharge.map
      ((c60F106ConditionalPhysicalNatIso A S I i j hi hj hObj hDef).hom.app X)).charge =
        (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map (eqToHom (hObj X))).charge =
      (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

/-- Nonzero defect on ONE real incidence arrow obstructs a
zero-added-charge comparison on the actual geometric overlap. -/
theorem c60F106NonzeroIncidenceDefect_obstruction
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) (i j : Fin n)
    (hi : i ∈ I) (hj : j ∈ I)
    {X Y : C60F106PhysicalOverlap A I} (f : X ⟶ Y)
    (hω : c60F106PhysicalChargeDefect A S I i j hi hj f ≠
      (0 : Int × Int)) :
    ¬ ∃ θ : c60F106PhysicalObserved A S I i hi ≅
        c60F106PhysicalObserved A S I j hj,
      ∀ Z : C60F106PhysicalOverlap A I,
        (c60F77QuotientToStrictCharge.map (θ.hom.app Z)).charge =
          (0 : Int × Int) := by
  intro h
  rcases h with ⟨θ, hθ⟩
  have hn :=
    congrArg
      (fun g :
        (c60F106PhysicalObserved A S I i hi).obj X ⟶
          (c60F106PhysicalObserved A S I j hj).obj Y =>
        (c60F77QuotientToStrictCharge.map g).charge)
      (θ.hom.naturality f)
  have heq :
      (c60F77QuotientToStrictCharge.map
        ((c60F106PhysicalObserved A S I i hi).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F106PhysicalObserved A S I j hj).map f)).charge := by
    simpa only [c60F80QuotientThree_comp_charge,
      hθ X, hθ Y, add_zero, zero_add] using hn
  exact hω ((c60F106PhysicalChargeDefect_zero_iff
    A S I i j hi hj f).mpr heq)

/-! ## V. Conditional strict triple-overlap Čech comparison -/

/-- The exact extra compatibility needed to glue ALL indexed
physical-edge observations over one REAL finite intersection.
Geometry alone does NOT imply this semantic compatibility. -/
structure C60F106PhysicalOverlapCompatibility
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n)) : Prop where
  obj :
    ∀ (i j : Fin n) (hi : i ∈ I) (hj : j ∈ I)
      (X : C60F106PhysicalOverlap A I),
      (c60F106PhysicalObserved A S I i hi).obj X =
        (c60F106PhysicalObserved A S I j hj).obj X
  charge :
    ∀ (i j : Fin n) (hi : i ∈ I) (hj : j ∈ I)
      {X Y : C60F106PhysicalOverlap A I} (f : X ⟶ Y),
      c60F106PhysicalChargeDefect A S I i j hi hj f = (0 : Int × Int)

/-- Actual observed F77 NatIso from the true common physical
incidence category, conditional on the explicit F95 semantics
and compatibility of its independently typed patch observations. -/
def c60F106PhysicalTransition
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n))
    (h : C60F106PhysicalOverlapCompatibility A S I)
    (i j : Fin n) (hi : i ∈ I) (hj : j ∈ I) :
    c60F106PhysicalObserved A S I i hi ≅
      c60F106PhysicalObserved A S I j hj :=
  c60F106ConditionalPhysicalNatIso A S I i j hi hj
    (h.obj i j hi hj) (h.charge i j hi hj)

/-- Every conditional physical transition is zero-ADDED-charge,
not zero original charge. -/
theorem c60F106PhysicalTransition_charge_zero
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n))
    (h : C60F106PhysicalOverlapCompatibility A S I)
    (i j : Fin n) (hi : i ∈ I) (hj : j ∈ I)
    (X : C60F106PhysicalOverlap A I) :
    (c60F77QuotientToStrictCharge.map
      ((c60F106PhysicalTransition A S I h i j hi hj).hom.app X)).charge =
        (0 : Int × Int) :=
  c60F106ConditionalPhysicalNatIso_charge_zero A S I i j hi hj
    (h.obj i j hi hj) (h.charge i j hi hj) X

/-- The genuinely common incidence overlap carries a strict
Čech 1-cocycle on all THREE locally compatible C60 patches.
The equality is in the Mathlib functor CATEGORY. -/
theorem c60F106PhysicalTransition_cocycle
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (S : C60F106SingletonF95Semantics A)
    (I : Finset (Fin n))
    (h : C60F106PhysicalOverlapCompatibility A S I)
    (i j k : Fin n) (hi : i ∈ I) (hj : j ∈ I) (hk : k ∈ I) :
    (c60F106PhysicalTransition A S I h i j hi hj).hom ≫
      (c60F106PhysicalTransition A S I h j k hj hk).hom =
        (c60F106PhysicalTransition A S I h i k hi hk).hom := by
  apply c60F103ZeroChargeNatTrans_unique
  · intro X
    change
      (c60F77QuotientToStrictCharge.map
        (eqToHom (h.obj i j hi hj X) ≫
          eqToHom (h.obj j k hj hk X))).charge = (0 : Int × Int)
    simp only [c60F80QuotientThree_comp_charge,
      c60F82Quotient_eqToHom_charge_zero, zero_add]
  · intro X
    exact c60F106PhysicalTransition_charge_zero A S I h i k hi hk X

#print axioms c60F106OverlapRestrict_site
#print axioms c60F106OverlapRestrict_trans_obj
#print axioms c60F106OverlapRestrict_trans_map
#print axioms c60F106SharedEndpoint_overlap_nonempty
#print axioms c60F106SharedFace_overlap_nonempty
#print axioms c60F106AllPhysicalFlags_in_star
#print axioms c60F106PhysicalChargeDefect_skew
#print axioms c60F106PhysicalChargeDefect_cocycle
#print axioms c60F106PhysicalChargeDefect_zero_iff
#print axioms c60F106ConditionalPhysicalNatIso
#print axioms c60F106ConditionalPhysicalNatIso_charge_zero
#print axioms c60F106NonzeroIncidenceDefect_obstruction
#print axioms c60F106PhysicalTransition
#print axioms c60F106PhysicalTransition_charge_zero
#print axioms c60F106PhysicalTransition_cocycle

end
end KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
