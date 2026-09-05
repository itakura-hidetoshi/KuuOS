import KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91

namespace KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84
open KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87
open KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88
open KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91

universe u

/-!
# Canonical fibrations reflect thin 2-simplices v1.92

Version v1.91 identified the terminal right lifting property against the atomic
identity-triangle scaling enrichment with maximal scaling of the target.  The
terminal map is only the object-level shadow of a more general phenomenon.

For a scaled morphism `p : X -> Y`, the square against

```text
(Delta[2], minimal) -> (Delta[2], minimal + {id_2})
```

exists exactly when a chosen 2-simplex `sigma` of `X` has thin image in `Y`.
A lift must reuse the same underlying Yoneda map, and therefore exists exactly
when `sigma` itself is thin.  Consequently the atomic RLP is equivalent to
reflection of thin 2-simplices:

```text
HasLiftingProperty atomicTwoSimplexEnrichment p
  <->
forall sigma, thin (p sigma) -> thin sigma.
```

Since the atomic enrichment belongs to the canonical generated left class,
every canonical right map reflects thinness.  Thus the arbitrary-scaling
canonical presentation constrains not only fibrant objects but every fibration
in its right class.

The terminal case recovers v1.91 because every 2-simplex of the point is thin.
Finally, if the canonical presentation were below the standard A/B/C
presentation, every standard-right map would also have to reflect thinness.
Therefore any standard-right map that sends one non-thin triangle to a thin
triangle is a direct witness against that presentation order.
-/

/-! ## Thinness reflection -/

/-- A scaled morphism reflects thinness in degree two when a 2-simplex whose
image is thin was already thin in the source. -/
def ReflectsThinTwoSimplices
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y) : Prop :=
  ∀ σ : X.carrier.obj (op ⦋2⦌),
    Y.scaling.thin (p.map.app (op ⦋2⦌) σ) →
      X.scaling.thin σ

/-- Because every scaled morphism preserves thinness, reflection is equivalent
to exact preservation-and-reflection of the thin predicate. -/
theorem reflectsThinTwoSimplices_iff
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y) :
    ReflectsThinTwoSimplices p ↔
      ∀ σ : X.carrier.obj (op ⦋2⦌),
        X.scaling.thin σ ↔
          Y.scaling.thin (p.map.app (op ⦋2⦌) σ) := by
  constructor
  · intro hreflect σ
    constructor
    · exact p.scaled σ
    · exact hreflect σ
  · intro h σ hthin
    exact (h σ).2 hthin

/-! ## Exact atomic RLP characterization for an arbitrary right map -/

/-- The atomic identity-triangle enrichment has RLP against `p` exactly when
`p` reflects thin 2-simplices. -/
theorem atomicTwoSimplexRLP_iff_reflectsThinTwoSimplices
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y) :
    HasLiftingProperty atomicTwoSimplexEnrichment p ↔
      ReflectsThinTwoSimplices p := by
  constructor
  · intro h σ hσ
    let f : minimallyScaledSimplex 2 ⟶ X :=
      { map := SSet.yonedaEquiv.symm σ
        scaled := minimalScaling_map X.scaling _ }
    let g : scaledSimplex atomicTwoSimplexScaling ⟶ Y :=
      { map := f.map ≫ p.map
        scaled := by
          intro t ht
          change
            (minimalScaling (Δ[2] : SSet.{u})).thin t ∨
              t = identityTwoSimplex at ht
          rcases ht with hmin | hident
          · exact p.scaled _ (f.scaled t hmin)
          · subst t
            simpa [f, identityTwoSimplex,
              SSet.yonedaEquiv_symm_app_objEquiv_symm] using hσ }
    let sq : CommSq f atomicTwoSimplexEnrichment p g :=
      { w := by
          apply ScaledSSet.ScaledMap.ext
          set_option backward.isDefEq.respectTransparency false in
            change
              f.map ≫ p.map =
                𝟙 (scaledSimplex atomicTwoSimplexScaling).carrier ≫
                  (f.map ≫ p.map)
          simp only [Category.id_comp]
          rfl }
    rcases (h.sq_hasLift sq).exists_lift with ⟨L⟩
    have hLmap : L.l.map = f.map := by
      have hmap := congrArg ScaledSSet.ScaledMap.map L.fac_left
      set_option backward.isDefEq.respectTransparency false in
        change
          (𝟙 (scaledSimplex atomicTwoSimplexScaling).carrier ≫ L.l.map) =
            f.map at hmap
      simpa only [Category.id_comp] using hmap
    have hthin :=
      L.l.scaled identityTwoSimplex atomicTwoSimplexScaling_identity_thin
    rw [hLmap] at hthin
    have hthin' :
        X.scaling.thin
          ((SSet.yonedaEquiv.symm σ).app (op ⦋2⦌) identityTwoSimplex) := by
      set_option backward.isDefEq.respectTransparency false in
        exact hthin
    simpa [identityTwoSimplex,
      SSet.yonedaEquiv_symm_app_objEquiv_symm] using hthin'
  · intro hreflect
    refine ⟨?_⟩
    intro f g sq
    have hsqmap : f.map ≫ p.map = g.map := by
      have hmap := congrArg ScaledSSet.ScaledMap.map sq.w
      set_option backward.isDefEq.respectTransparency false in
        change
          f.map ≫ p.map =
            𝟙 (scaledSimplex atomicTwoSimplexScaling).carrier ≫ g.map at hmap
      simpa only [Category.id_comp] using hmap
    let l : scaledSimplex atomicTwoSimplexScaling ⟶ X :=
      { map := f.map
        scaled := by
          intro t ht
          change
            (minimalScaling (Δ[2] : SSet.{u})).thin t ∨
              t = identityTwoSimplex at ht
          rcases ht with hmin | hident
          · exact f.scaled t hmin
          · subst t
            apply hreflect
              (f.map.app (op ⦋2⦌) identityTwoSimplex)
            have hthin :=
              g.scaled identityTwoSimplex
                atomicTwoSimplexScaling_identity_thin
            rw [← hsqmap] at hthin
            set_option backward.isDefEq.respectTransparency false in
              change
                Y.scaling.thin
                  (p.map.app (op ⦋2⦌)
                    (f.map.app (op ⦋2⦌) identityTwoSimplex)) at hthin
            exact hthin }
    exact CommSq.HasLift.mk'
      { l := l
        fac_left := by
          apply ScaledSSet.ScaledMap.ext
          set_option backward.isDefEq.respectTransparency false in
            change
              𝟙 (scaledSimplex atomicTwoSimplexScaling).carrier ≫ f.map =
                f.map
          simp only [Category.id_comp]
        fac_right := by
          apply ScaledSSet.ScaledMap.ext
          set_option backward.isDefEq.respectTransparency false in
            change f.map ≫ p.map = g.map
          exact hsqmap }

/-! ## Canonical right maps are thin-reflecting -/

/-- Every map in the right orthogonal of the canonical generated left class
reflects thin 2-simplices. -/
theorem canonicalGeneratedRight_reflectsThinTwoSimplices
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hp :
      (canonicalGeneratedScaledAnodyne :
        MorphismProperty (ScaledSSet.{u})).rlp p) :
    ReflectsThinTwoSimplices p := by
  apply (atomicTwoSimplexRLP_iff_reflectsThinTwoSimplices p).1
  exact hp atomicTwoSimplexEnrichment
    atomicTwoSimplexEnrichment_mem_canonicalGenerated

/-- The same conclusion can be read directly from the literal canonical
attachment-generator right class, because its RLP is the generated RLP. -/
theorem canonicalAttachmentRight_reflectsThinTwoSimplices
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hp :
      (scaledHornAttachmentGenerators :
        MorphismProperty (ScaledSSet.{u})).rlp p) :
    ReflectsThinTwoSimplices p := by
  apply canonicalGeneratedRight_reflectsThinTwoSimplices
  rw [canonicalGeneratedScaledAnodyne_rlp]
  exact hp

/-- Package thin-reflecting scaled maps as a morphism property. -/
def thinReflectingTwoSimplexMaps :
    MorphismProperty (ScaledSSet.{u}) :=
  fun _ _ p => ReflectsThinTwoSimplices p

/-- The complete canonical right class is contained in the property of
thin-reflecting maps. -/
theorem canonicalGeneratedRight_le_thinReflectingTwoSimplexMaps :
    (canonicalGeneratedScaledAnodyne :
      MorphismProperty (ScaledSSet.{u})).rlp ≤
      thinReflectingTwoSimplexMaps := by
  intro X Y p hp
  exact canonicalGeneratedRight_reflectsThinTwoSimplices hp

/-! ## The terminal case is exactly v1.91 -/

/-- Reflection along the terminal map is equivalent to every source
2-simplex being thin, since the point has maximal scaling. -/
theorem reflectsThinTwoSimplices_toPoint_iff_all_two_simplices_thin
    (X : ScaledSSet.{u}) :
    ReflectsThinTwoSimplices (ScaledSSet.toPoint X) ↔
      ∀ σ : X.carrier.obj (op ⦋2⦌), X.scaling.thin σ := by
  constructor
  · intro hreflect σ
    apply hreflect σ
    exact ScaledSimplicialSet.maximal_thin _ _
  · intro hall σ _
    exact hall σ

/-- The v1.91 terminal atomic-RLP theorem is recovered by specializing the
general thin-reflection characterization. -/
theorem atomicTwoSimplexRLP_toPoint_iff_all_two_simplices_thin
    (X : ScaledSSet.{u}) :
    HasLiftingProperty
        atomicTwoSimplexEnrichment
        (ScaledSSet.toPoint X) ↔
      ∀ σ : X.carrier.obj (op ⦋2⦌), X.scaling.thin σ := by
  rw [atomicTwoSimplexRLP_iff_reflectsThinTwoSimplices,
    reflectsThinTwoSimplices_toPoint_iff_all_two_simplices_thin]

/-! ## A stronger standard/canonical separation criterion -/

/-- If the canonical presentation were below standard A/B/C, then every
standard-right map would have to reflect thin 2-simplices, not merely terminal
maps. -/
theorem standardRight_reflectsThinTwoSimplices_of_canonical_le_standard
    (horder :
      (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
        standardABCPresentation)
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hstd :
      (KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58.standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})).rlp p) :
    ReflectsThinTwoSimplices p := by
  have hgen :
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤
        (KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58.standardGeneratedScaledAnodyneABC :
          MorphismProperty (ScaledSSet.{u})) :=
    canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated.1
      horder
  have hright :
      (KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58.standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})).rlp ≤
        (scaledHornAttachmentGenerators :
          MorphismProperty (ScaledSSet.{u})).rlp :=
    MorphismProperty.antitone_rlp hgen
  exact canonicalAttachmentRight_reflectsThinTwoSimplices
    (hright p hstd)

/-- Hence any standard-right map carrying one non-thin source triangle to a
thin target triangle disproves `canonical ≤ standard`. -/
theorem not_canonicalKuuOS_le_standardABC_of_standardRLP_nonreflecting
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hstd :
      (KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58.standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})).rlp p)
    (σ : X.carrier.obj (op ⦋2⦌))
    (himage : Y.scaling.thin (p.map.app (op ⦋2⦌) σ))
    (hsource : ¬ X.scaling.thin σ) :
    ¬ ((canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
      standardABCPresentation) := by
  intro horder
  have hreflect :=
    standardRight_reflectsThinTwoSimplices_of_canonical_le_standard
      horder hstd
  exact hsource (hreflect σ himage)

/-!
The right-class audit is now exact:

```text
atomic scaling enrichment i_2
  RLP against p
    <-> p reflects thin 2-simplices

atomic i_2 in canonicalGenerated
  => every canonical right map reflects thinness

p = X -> *
  => every 2-simplex of X is thin
  => v1.91 maximal-scaling theorem

canonical <= standard
  => standard right <= canonical right
  => every standard-right map reflects thinness.
```

Thus a separation witness need not be a terminal object.  Any standard A/B/C
fibration that fails to reflect thinness in degree two is enough to prove that
the canonical arbitrary-scaling presentation is strictly too strong in the
forward comparison direction.
-/

end KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92
