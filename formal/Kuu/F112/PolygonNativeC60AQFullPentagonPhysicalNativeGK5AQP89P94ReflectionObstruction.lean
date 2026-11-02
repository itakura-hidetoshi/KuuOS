import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5APContextUnitIndependence
import Mathlib.Tactic

/-!
F112-P94D3GK5AQ — original P89→P94A reflection obstruction and
the exact difference between generator minimality and quotient faithfulness.

GK5AN constructed a genuine original P89-four-proof quotient map to
the independently chosen P94A presentation and proved injectivity
IFF full reflection of selected P94A four-cell comparisons of
GK5AI source images to original P89 four-cell witnesses.
GK5AO/GK5AP then proved that all THREE selected P94A primitive
unit families are individually indispensable within that presentation.
This does NOT entail that P89→P94A is nonfaithful: unlike P93,
the original P89 ALREADY CONTAINS the three P80 unit generators.

Here a precise, source-typed BAD PAIR is defined: TWO genuine
original F55 proof terms with the same typed F54 boundaries,
whose structural images have a selected P94A four-cell comparison,
but for which there is NO original P89 four-cell certificate.
We prove that nonemptiness of this obstruction is exactly the
failure of faithfulness, that it is symmetric and stable under
original P89 comparison, that it has equal FULL signed pentagon,
square and odd-phase shadow coordinates, and that none of the
original P80 primitive witnesses is such a bad pair.

An independent, already established genuinely physical north C60
triple exhibits a DIFFERENT obstruction: new P92B assocNaturality
has no original F55 3-proof preimage. Thus no global right inverse
to the source structural 3-proof map exists on that typed slot;
this is a barrier to naive witness-by-witness lifting, NOT a proof
of noninjectivity of P89→P94A. Genuine selected four-cell
comparison remains a separate requirement.

All statements are about the ORIGINAL indexed Type-valued
F54/F55/P89 histories and the EXACT chosen P92B/P94A.
No old source rewriting, no new axioms, no sorry/native_decide,
no Gray or unconditional higher gluing. Independent Kuu → Qi only,
strict 空 authority, append-only, public root 107 unchanged.
Pinned Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protect #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A precise nonreflection witness at the same ORIGINAL dependent F54
route endpoints. Requires an ACTUAL P94A Type four-cell comparison
of structural phi-images AND the absence of a P89 Type four-cell.
This is not merely equality of observable charges. -/
def nativeGK5AQBadPair
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) : Prop :=
  Nonempty (NativeF55P94UnitFourCell
    (nativeGK5AIOriginalToP92Structural f)
    (nativeGK5AIOriginalToP92Structural g)) ∧
    ¬ Nonempty (NativeF55P89InterchangeFourCell f g)

/-- Bad-pair relation is invariant under reversing the genuine 4-cell
witness, and the source no-witness condition is reversed as well. -/
theorem nativeGK5AQBadPair_symm
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5AQBadPair first last f g ↔
      nativeGK5AQBadPair first last g f := by
  constructor
  · rintro ⟨⟨w⟩, hno⟩
    refine ⟨⟨.symm w⟩, ?_⟩
    rintro ⟨h⟩
    exact hno ⟨.symm h⟩
  · rintro ⟨⟨w⟩, hno⟩
    refine ⟨⟨.symm w⟩, ?_⟩
    rintro ⟨h⟩
    exact hno ⟨.symm h⟩

/-- Exactly the kernel-pair EXCESS: equality after the selected
P94A quotient map but inequality of genuine original P89 classes. -/
theorem nativeGK5AQBadPair_iff_class_gap
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5AQBadPair first last f g ↔
      (nativeF55P94UnitFourClass first last
          (nativeGK5AIOriginalToP92Structural f) =
        nativeF55P94UnitFourClass first last
          (nativeGK5AIOriginalToP92Structural g)) ∧
      (nativeF55P89FourClass first last f ≠
        nativeF55P89FourClass first last g) := by
  constructor
  · rintro ⟨htarget, hnotsource⟩
    constructor
    · exact (nativeF55P94UnitFourClass_eq_iff first last _ _).2 htarget
    · intro heq
      exact hnotsource ((nativeF55P89FourClass_eq_iff first last f g).1 heq)
  · rintro ⟨heq, hne⟩
    constructor
    · exact (nativeF55P94UnitFourClass_eq_iff first last _ _).1 heq
    · intro hsource
      exact hne ((nativeF55P89FourClass_eq_iff first last f g).2 hsource)

/-- Even a true nonreflection counterexample would be invisible to
ALL three original signed shadow coordinates, by P94A soundness
and exact GK5AI structural shadow preservation. -/
theorem nativeGK5AQBadPair_shadow_eq
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (h : nativeGK5AQBadPair first last f g) :
    f.nativeShadow = g.nativeShadow := by
  rcases h.1 with ⟨w⟩
  calc
    f.nativeShadow =
      (nativeGK5AIOriginalToP92Structural f).nativeShadow :=
        (nativeGK5AJStructuralShadow first last f).symm
    _ = (nativeGK5AIOriginalToP92Structural g).nativeShadow :=
        w.shadow_sound
    _ = g.nativeShadow :=
        nativeGK5AJStructuralShadow first last g

/-- Original P89 equivalences may be added at EITHER END of a bad
pair: a true new selected identification cannot be repaired by
changing only the representatives in the original P89 classes. -/
theorem nativeGK5AQBadPair_transport
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f f' g' g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (hleft : NativeF55P89InterchangeFourCell f f')
    (hbad : nativeGK5AQBadPair first last f' g')
    (hright : NativeF55P89InterchangeFourCell g' g) :
    nativeGK5AQBadPair first last f g := by
  rcases hbad with ⟨⟨w⟩, hno⟩
  constructor
  · exact ⟨NativeF55P94UnitFourCell.trans
      (NativeF55P94UnitFourCell.trans
        (nativeGK5ANP89ToP94 _ hleft) w)
      (nativeGK5ANP89ToP94 _ hright)⟩
  · rintro ⟨fg⟩
    exact hno ⟨NativeF55P89InterchangeFourCell.trans
      (NativeF55P89InterchangeFourCell.trans (.symm hleft) fg)
      (.symm hright)⟩

/-- EXACT existence criterion for a true original P89→P94A
faithfulness obstruction, not a claim that it currently occurs. -/
theorem nativeGK5AQBadPair_exists_iff_not_injective
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (∃ f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s,
      nativeGK5AQBadPair first last f g) ↔
      ¬ Function.Injective
        (nativeGK5ANP89ToP94FourClassMap first last r s) := by
  constructor
  · rintro ⟨f, g, ⟨hp94, hnotsource⟩⟩ hinj
    have href := (nativeGK5ANP89ToP94_injective_iff_reflect
      first last r s).1 hinj
    exact hnotsource (href f g hp94)
  · intro hnot
    by_contra hnopair
    apply hnot
    apply (nativeGK5ANP89ToP94_injective_iff_reflect
      first last r s).2
    intro f g hp94
    by_contra hnotsource
    exact hnopair ⟨f, g, hp94, hnotsource⟩

/-- The ORIGINAL P80 primitive unit certificates were already
present as P89 proof evidence BEFORE any selected P94A extension.
No such genuine primitive pair can be a P89→P94A obstruction. -/
theorem nativeGK5AQPrimitive_not_bad
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5ALPrimitiveUnitFourCell f g) :
    ¬ nativeGK5AQBadPair first last f g := by
  intro h
  exact h.2 ⟨NativeF55P89InterchangeFourCell.old w.toP87⟩

/-- All THREE original P80 primitive families have a genuine P89
4-cell and the corresponding selected P94A four-cell under phi,
without invoking P93 or equality of numeric shadows. -/
theorem nativeGK5AQPrimitive_both_witnesses
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5ALPrimitiveUnitFourCell f g) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∧
    Nonempty (NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g)) := by
  let oldWitness : NativeF55P89InterchangeFourCell f g := .old w.toP87
  exact ⟨⟨oldWitness⟩, ⟨nativeGK5ANP89ToP94 _ oldWitness⟩⟩

/-- The original P92A north C60 unit associator-naturality slot
is empty while P92B admits an honest new typed witness there.
This is a genuinely SOURCE-TYPE obstruction, NOT a kernel-pair
counterexample to the P89→P94A quotient map. -/
private abbrev nativeGK5AQNorthUnitAssocOriginal :=
  NativeF55P90AssocNaturalityCell
    (nativeF54P92UnitRoute northNativeF45FirstStage)
    (nativeF54P92UnitRoute northNativeF45SecondStage)
    (nativeF54P92UnitRoute northNativeF45ThirdStage)

private abbrev nativeGK5AQNorthUnitAssocSelected :=
  NativeF55P92AssocComparison (.pentagon .north)
    (nativeF54P90AssocNaturalityLeftRoute
      (nativeF54P92UnitRoute northNativeF45FirstStage)
      (nativeF54P92UnitRoute northNativeF45SecondStage)
      (nativeF54P92UnitRoute northNativeF45ThirdStage))
    (nativeF54P90AssocNaturalityRightRoute
      (nativeF54P92UnitRoute northNativeF45FirstStage)
      (nativeF54P92UnitRoute northNativeF45SecondStage)
      (nativeF54P92UnitRoute northNativeF45ThirdStage))

/-- Structural phi cannot be surjective on even the genuine
north three-stage associator-naturality evidence type. -/
theorem nativeGK5AQNorthStructuralPhi_not_surjective :
    ¬ Function.Surjective
      (fun old : nativeGK5AQNorthUnitAssocOriginal =>
        nativeGK5AIOriginalToP92Structural old) := by
  intro hsurj
  rcases hsurj nativeGK5AINorthAddedUnitAssocCell with ⟨old, h⟩
  exact nativeGK5AINorthAddedUnitAssoc_noOriginalPreimage ⟨old, h⟩

/-- In particular no witness-level *total* old-source reconstruction
function can exist for that genuinely typed north slot, even
before requiring it to be a section of the structural map. -/
theorem nativeGK5AQNorthNoTotalEvidenceRecovery :
    ¬ (nativeGK5AQNorthUnitAssocSelected →
      nativeGK5AQNorthUnitAssocOriginal) := by
  intro recover
  have old := recover nativeGK5AINorthAddedUnitAssocCell
  exact (nativeF55P92_original_unit_naturality_no_filler
    northNativeF45FirstStage
    northNativeF45SecondStage
    northNativeF45ThirdStage) ⟨old⟩

#print axioms nativeGK5AQBadPair
#print axioms nativeGK5AQBadPair_symm
#print axioms nativeGK5AQBadPair_iff_class_gap
#print axioms nativeGK5AQBadPair_shadow_eq
#print axioms nativeGK5AQBadPair_transport
#print axioms nativeGK5AQBadPair_exists_iff_not_injective
#print axioms nativeGK5AQPrimitive_not_bad
#print axioms nativeGK5AQPrimitive_both_witnesses
#print axioms nativeGK5AQNorthStructuralPhi_not_surjective
#print axioms nativeGK5AQNorthNoTotalEvidenceRecovery

end
end Kuu.F112.Physical
