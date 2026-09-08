import KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106
import Mathlib.CategoryTheory.Limits.Preserves.Ulift

namespace KUOS.DependentOriginationDoubleDeloopingUniverseTransportV1_106_1

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106

universe u

noncomputable section

/-!
# Universe transport for the concrete B²ℕ standard-right separator v1.106.1

The concrete arithmetic separator proved in v1.95--v1.106 lives in universe
zero.  This file begins the strictly structural transport needed to reuse that
certificate in an arbitrary simplicial-set universe without rebuilding any of
the B²ℕ cocycle arithmetic.

The transport is pointwise `ULift`.  Thinness is transported by `down`, so no
new mathematical scaling condition is introduced.  We package this as a fully
faithful functor on `ScaledSSet`, prove that fully faithful functors preserve a
lifting property between maps in their image, and prove that thinness
reflection is invariant under this lift.

The second part identifies lifted low-universe standard simplices and horns
with their native high-universe counterparts.  The identification is the
unique one preserving the underlying simplex-category morphism under
`stdSimplex.objEquiv`; hence it is independent of presentation choices.
-/

/-! ## Pointwise ULift of scaled simplicial sets -/

/-- Transport a scaling through the pointwise universe lift of its carrier. -/
def uliftScaling
    {X : SSet.{0}}
    (sX : ScaledSimplicialSet X) :
    ScaledSimplicialSet ((SSet.uliftFunctor.{u, 0}).obj X) where
  thin := fun t => sX.thin t.down
  thin_sigma_zero := by
    intro x
    exact sX.thin_sigma_zero x.down
  thin_sigma_one := by
    intro x
    exact sX.thin_sigma_one x.down

/-- Object part of the universe lift on scaled simplicial sets. -/
def scaledUliftObj (X : ScaledSSet.{0}) : ScaledSSet.{u} :=
  ScaledSSet.of
    ((SSet.uliftFunctor.{u, 0}).obj X.carrier)
    (uliftScaling X.scaling)

/-- Morphism part of the universe lift on scaled simplicial sets. -/
def scaledUliftMap
    {X Y : ScaledSSet.{0}}
    (f : X ⟶ Y) :
    scaledUliftObj.{u} X ⟶ scaledUliftObj.{u} Y where
  map := (SSet.uliftFunctor.{u, 0}).map f.map
  scaled := by
    intro t ht
    change Y.scaling.thin (f.map.app (op ⦋2⦌) t.down)
    exact f.scaled t.down ht

/-- Pointwise `ULift` as a functor on explicitly scaled simplicial sets. -/
def scaledUliftFunctor : ScaledSSet.{0} ⥤ ScaledSSet.{u} where
  obj := scaledUliftObj
  map := scaledUliftMap
  map_id := by
    intro X
    apply ScaledSSet.ScaledMap.ext
    exact (SSet.uliftFunctor.{u, 0}).map_id X.carrier
  map_comp := by
    intro X Y Z f g
    apply ScaledSSet.ScaledMap.ext
    exact (SSet.uliftFunctor.{u, 0}).map_comp f.map g.map

/-- A high-universe map between two lifted scaled objects has a unique
low-universe preimage.  Scaledness descends because thinness was defined by
`ULift.down`. -/
def scaledUliftFullyFaithful :
    (scaledUliftFunctor.{u}).FullyFaithful where
  preimage {X Y} f :=
    { map := (SSet.uliftFunctor.{u, 0}).preimage f.map
      scaled := by
        intro t ht
        have hf := f.scaled (ULift.up t) ht
        change
          Y.scaling.thin
            ((f.map.app (op ⦋2⦌) (ULift.up t)).down) at hf
        have hmap := congr_app
          ((SSet.uliftFunctor.{u, 0}).map_preimage f.map)
          (op ⦋2⦌)
        have happ := ConcreteCategory.congr_hom hmap (ULift.up t)
        have hdown := congrArg ULift.down happ
        change
          Y.scaling.thin
            (((SSet.uliftFunctor.{u, 0}).preimage f.map).app
              (op ⦋2⦌) t)
        rw [hdown]
        exact hf }
  map_preimage := by
    intro X Y f
    apply ScaledSSet.ScaledMap.ext
    exact (SSet.uliftFunctor.{u, 0}).map_preimage f.map
  preimage_map := by
    intro X Y f
    apply ScaledSSet.ScaledMap.ext
    exact (SSet.uliftFunctor.{u, 0}).preimage_map f.map

instance scaledUliftFunctor_full : (scaledUliftFunctor.{u}).Full :=
  (scaledUliftFullyFaithful.{u}).full

instance scaledUliftFunctor_faithful : (scaledUliftFunctor.{u}).Faithful :=
  (scaledUliftFullyFaithful.{u}).faithful

/-! ## Lifting and thin-reflection transport -/

/-- A fully faithful functor preserves a lifting property between maps in its
image.  This is the only categorical fact needed to transport the low-universe
B²ℕ right-lifting certificate itself. -/
theorem hasLiftingProperty_map_of_full_faithful
    {C : Type*} [Category* C]
    {D : Type*} [Category* D]
    (F : C ⥤ D) [F.Full] [F.Faithful]
    {A B X Y : C}
    {i : A ⟶ B} {p : X ⟶ Y}
    (h : HasLiftingProperty i p) :
    HasLiftingProperty (F.map i) (F.map p) := by
  refine ⟨?_⟩
  intro f g sq
  let f₀ : A ⟶ X := F.preimage f
  let g₀ : B ⟶ Y := F.preimage g
  let sq₀ : CommSq f₀ i p g₀ :=
    { w := by
        apply F.map_injective
        simpa [f₀, g₀] using sq.w }
  rcases (h.sq_hasLift sq₀).exists_lift with ⟨L⟩
  exact CommSq.HasLift.mk'
    { l := F.map L.l
      fac_left := by
        rw [← F.map_comp, L.fac_left]
        exact F.map_preimage f
      fac_right := by
        rw [← F.map_comp, L.fac_right]
        exact F.map_preimage g }

/-- Thinness reflection is unchanged by the pointwise scaled universe lift. -/
theorem reflectsThinTwoSimplices_scaledUlift_map_iff
    {X Y : ScaledSSet.{0}}
    (f : X ⟶ Y) :
    ReflectsThinTwoSimplices ((scaledUliftFunctor.{u}).map f) ↔
      ReflectsThinTwoSimplices f := by
  constructor
  · intro h σ hσ
    have hs := h (ULift.up σ)
    change X.scaling.thin σ at hs
    apply hs
    change Y.scaling.thin (f.map.app (op ⦋2⦌) σ)
    exact hσ
  · intro h σ hσ
    change X.scaling.thin σ.down
    apply h σ.down
    change Y.scaling.thin (f.map.app (op ⦋2⦌) σ.down) at hσ
    exact hσ

/-! ## Native standard simplex universe identification -/

/-- On each simplicial degree, a lifted low-universe standard simplex and the
native high-universe standard simplex represent the same simplex-category
morphism. -/
def stdSimplexUliftObjEquiv
    (n : Nat) (J : SimplexCategoryᵒᵖ) :
    ((SSet.uliftFunctor.{u, 0}).obj (Δ[n] : SSet.{0})).obj J ≃
      (Δ[n] : SSet.{u}).obj J :=
  (Equiv.ulift.trans SSet.stdSimplex.objEquiv.{0}).trans
    SSet.stdSimplex.objEquiv.{u}.symm

/-- The degreewise equivalences assemble to the canonical simplicial
isomorphism from the lifted low standard simplex to the native high standard
simplex. -/
def stdSimplexUliftIso (n : Nat) :
    (SSet.uliftFunctor.{u, 0}).obj (Δ[n] : SSet.{0}) ≅
      (Δ[n] : SSet.{u}) :=
  NatIso.ofComponents
    (fun J => Equiv.toIso (stdSimplexUliftObjEquiv.{u} n J))
    (fun f => by
      ext x
      rfl)

/-- The simplex universe identification preserves every vertex value. -/
@[simp]
theorem stdSimplexUliftIso_hom_apply
    {n d : Nat}
    (x : ((SSet.uliftFunctor.{u, 0}).obj
      (Δ[n] : SSet.{0})).obj (op ⦋d⦌))
    (j : Fin (d + 1)) :
    ((stdSimplexUliftIso.{u} n).hom.app (op ⦋d⦌) x) j =
      x.down j := by
  rfl

/-- The inverse simplex universe identification also preserves every vertex
value. -/
@[simp]
theorem stdSimplexUliftIso_inv_apply
    {n d : Nat}
    (x : (Δ[n] : SSet.{u}).obj (op ⦋d⦌))
    (j : Fin (d + 1)) :
    (((stdSimplexUliftIso.{u} n).inv.app (op ⦋d⦌) x).down) j =
      x j := by
  rfl

/-! ## Native horn universe identification -/

/-- Degreewise universe identification for one standard horn. -/
def hornUliftObjEquiv
    (n : Nat) (i : Fin (n + 1)) (J : SimplexCategoryᵒᵖ) :
    ((SSet.uliftFunctor.{u, 0}).obj
      (Λ[n, i] : SSet.{0})).obj J ≃
      (Λ[n, i] : SSet.{u}).obj J where
  toFun x :=
    ⟨(stdSimplexUliftIso.{u} n).hom.app J (ULift.up x.down.1), by
      rw [SSet.mem_horn_iff] at x.down.2 ⊢
      change
        Set.range
            (SSet.stdSimplex.objEquiv.{0} x.down.1).toOrderHom ∪ {i} ≠
          Set.univ at x.down.2
      change
        Set.range
            (SSet.stdSimplex.objEquiv.{0} x.down.1).toOrderHom ∪ {i} ≠
          Set.univ
      exact x.down.2⟩
  invFun x :=
    ULift.up
      ⟨((stdSimplexUliftIso.{u} n).inv.app J x.1).down, by
        rw [SSet.mem_horn_iff] at x.2 ⊢
        change
          Set.range
              (SSet.stdSimplex.objEquiv.{u} x.1).toOrderHom ∪ {i} ≠
            Set.univ at x.2
        change
          Set.range
              (SSet.stdSimplex.objEquiv.{u} x.1).toOrderHom ∪ {i} ≠
            Set.univ
        exact x.2⟩
  left_inv x := by
    apply ULift.ext
    apply Subtype.ext
    simpa using congrArg ULift.down
      ((stdSimplexUliftIso.{u} n).inv_hom_id_app J (ULift.up x.down.1))
  right_inv x := by
    apply Subtype.ext
    simpa using
      ConcreteCategory.congr_hom
        ((stdSimplexUliftIso.{u} n).hom_inv_id_app J) x.1

/-- The horn degreewise equivalences are natural in the simplex degree. -/
def hornUliftIso
    (n : Nat) (i : Fin (n + 1)) :
    (SSet.uliftFunctor.{u, 0}).obj (Λ[n, i] : SSet.{0}) ≅
      (Λ[n, i] : SSet.{u}) :=
  NatIso.ofComponents
    (fun J => Equiv.toIso (hornUliftObjEquiv.{u} n i J))
    (fun f => by
      ext x
      apply Subtype.ext
      rfl)

/-- The horn universe identification commutes with the horn inclusion into the
standard simplex. -/
theorem hornUliftIso_hom_ι
    (n : Nat) (i : Fin (n + 1)) :
    (hornUliftIso.{u} n i).hom ≫
        (SSet.horn.{u} n i).ι =
      (SSet.uliftFunctor.{u, 0}).map
          ((SSet.horn.{0} n i).ι) ≫
        (stdSimplexUliftIso.{u} n).hom := by
  apply SSet.hom_ext
  intro J
  apply ConcreteCategory.hom_ext
  intro x
  rfl

/-- The inverse horn universe identification satisfies the inverse inclusion
square. -/
theorem hornUliftIso_inv_ι
    (n : Nat) (i : Fin (n + 1)) :
    (hornUliftIso.{u} n i).inv ≫
        (SSet.uliftFunctor.{u, 0}).map
          ((SSet.horn.{0} n i).ι) =
      (SSet.horn.{u} n i).ι ≫
        (stdSimplexUliftIso.{u} n).inv := by
  apply SSet.hom_ext
  intro J
  apply ConcreteCategory.hom_ext
  intro x
  rfl

/-! ## Minimal scaling is invariant under the universe lift and isomorphism -/

/-- Pointwise ULift of the minimal scaling is exactly the minimal scaling of
the lifted carrier, at the predicate level. -/
theorem uliftScaling_minimal_iff
    {X : SSet.{0}}
    (t : ((SSet.uliftFunctor.{u, 0}).obj X).obj (op ⦋2⦌)) :
    (uliftScaling (minimalScaling X)).thin t ↔
      (minimalScaling ((SSet.uliftFunctor.{u, 0}).obj X)).thin t := by
  constructor
  · intro ht
    rcases ht with ⟨x, hx⟩ | ⟨x, hx⟩
    · left
      refine ⟨ULift.up x, ?_⟩
      apply ULift.ext
      exact hx
    · right
      refine ⟨ULift.up x, ?_⟩
      apply ULift.ext
      exact hx
  · intro ht
    rcases ht with ⟨x, hx⟩ | ⟨x, hx⟩
    · left
      refine ⟨x.down, ?_⟩
      exact congrArg ULift.down hx
    · right
      refine ⟨x.down, ?_⟩
      exact congrArg ULift.down hx

/-- A simplicial isomorphism transports the minimal scaling forward. -/
theorem minimalScaling_iso_hom
    {X Y : SSet.{u}}
    (e : X ≅ Y)
    (t : X.obj (op ⦋2⦌))
    (ht : (minimalScaling X).thin t) :
    (minimalScaling Y).thin (e.hom.app (op ⦋2⦌) t) := by
  rcases ht with ⟨x, rfl⟩ | ⟨x, rfl⟩
  · left
    refine ⟨e.hom.app (op ⦋1⦌) x, ?_⟩
    exact (SSet.σ_naturality_apply e.hom 0 x).symm
  · right
    refine ⟨e.hom.app (op ⦋1⦌) x, ?_⟩
    exact (SSet.σ_naturality_apply e.hom 1 x).symm

/-- Minimal thinness is preserved and reflected by a simplicial isomorphism. -/
theorem minimalScaling_iso_iff
    {X Y : SSet.{u}}
    (e : X ≅ Y)
    (t : X.obj (op ⦋2⦌)) :
    (minimalScaling X).thin t ↔
      (minimalScaling Y).thin (e.hom.app (op ⦋2⦌) t) := by
  constructor
  · exact minimalScaling_iso_hom e t
  · intro ht
    have hback :=
      minimalScaling_iso_hom e.symm
        (e.hom.app (op ⦋2⦌) t) ht
    simpa using hback

/-- Lift a carrier isomorphism to an isomorphism of scaled objects once both
carrier directions are known to preserve thinness. -/
def scaledIsoOfCarrierIso
    {X Y : ScaledSSet.{u}}
    (e : X.carrier ≅ Y.carrier)
    (hhom : IsScaledMap X.scaling Y.scaling e.hom)
    (hinv : IsScaledMap Y.scaling X.scaling e.inv) :
    X ≅ Y where
  hom := ⟨e.hom, hhom⟩
  inv := ⟨e.inv, hinv⟩
  hom_inv_id := by
    apply ScaledSSet.ScaledMap.ext
    exact e.hom_inv_id
  inv_hom_id := by
    apply ScaledSSet.ScaledMap.ext
    exact e.inv_hom_id

end

end KUOS.DependentOriginationDoubleDeloopingUniverseTransportV1_106_1
