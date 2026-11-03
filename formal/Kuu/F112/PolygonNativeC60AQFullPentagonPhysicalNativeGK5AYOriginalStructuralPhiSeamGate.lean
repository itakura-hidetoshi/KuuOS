import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AXVerticalPrimitiveReflectionCertificates
import Mathlib.Tactic

/-!
F112-P94D3GK5AY — genuine P93C.old P92B.original versus GK5AI
constructor-recursive structural phi seam: local Type-valued 4-cell
certificates, exact reflection gates and noninjectivity obstructions.

The original P89→P93C OLD constructor targets P92B.original f/g,
whereas the independent GK5AN P89→P94A source map targets GK5AI's
structurally recursive phi(f)/phi(g). These are distinct proof-relevant
presentations. For a composite original F55 three-proof f there is
in general NO definitional equality P92B.original f = phi(f).

This module records the missing comparison as a dependent selected
P94A four-cell seam from the raw .original image of EACH genuine
F55 proof to its recursively translated phi proof. The seam is a
CONDITION, not an implicitly inhabited record or a new logical axiom.
Given it, an arbitrary genuine selected P93C 4-cell between two raw
.original endpoints is transported to a selected P94A comparison
between structurally translated source endpoints. The transport
visits the actual P93C 4-proof, including the P93C.old constructor,
not only its shadow or quotient class.

The exact local residual obstruction is a P93C four-proof between
raw original source endpoints with NO corresponding genuine P89
four-proof. Under the seam record this is a true GK5AQ BadPair at
phi source endpoints and hence a conditional obstruction to the
injectivity of the original P89→P94A four-class map. Conversely
injectivity implies source reflection for all raw P93C comparisons
under the seam. It remains possible that no such seam exists:
this work does NOT construct a universal seam, original P89
noninjectivity, or normalize arbitrary P94A proof histories.

A concrete north C60 ORIGINAL F55 right-unit composite shows
raw P92B.original proof ≠ constructor-recursive phi proof
by actual inductive-constructor separation. This does NOT assert
absence of a P94A 4-cell between these terms.

Strict 空 authority / independent Kuu→Qi only, original F54
two-Nat/category/Blocks history preserved, same public root107,
protected PR #1558 Draft/open. Lean v4.30.0-rc2 and pinned
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only; no Gray, sorry/admit/native_decide, new axioms or
unconditional source descent. Copyright (c) 2026
Hidetoshi Itakura / 板倉英俊. Apache-2.0.
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
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- The exact missing 4-cell seam connecting a raw original
P92B wrapper to GK5AI's recursive phi interpretation.
A field is a TRUE Type-valued 4-cell, NOT an equality of witnesses,
not a quotient relation, and not an axiom declaring its existence. -/
structure NativeGK5AYOriginalPhiSeam
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Type (max (max uD uE) (max vD vE)) where
  at :
    ∀ {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s),
      NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original f)
        (nativeGK5AIOriginalToP92Structural f)

/-- The seam record is inhabited iff EACH exact original F55
proof has a corresponding selected Type-valued P94A four-cell.
The backward direction uses an explicit classical choice of
proof terms; it does not prove this condition holds. -/
theorem nativeGK5AYSeam_nonempty_iff_pointwise
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Nonempty (NativeGK5AYOriginalPhiSeam first last) ↔
      ∀ {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
        (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s),
        Nonempty (NativeF55P94UnitFourCell
          (NativeF55P92AssocComparison.original f)
          (nativeGK5AIOriginalToP92Structural f)) := by
  classical
  constructor
  · rintro ⟨data⟩
    intro r s f
    exact ⟨data.at f⟩
  · intro h
    refine ⟨{ at := ?_ }⟩
    intro r s f
    exact Classical.choice (h f)

/-- Transport an ACTUAL chosen P93C four-proof between raw source
wrappers into the phi-image of genuine original F55 endpoints.
The two seam certificates are explicitly composed around P94A.old.
No false P92B.original f = phi(f) definitional equality is used. -/
def NativeGK5AYOriginalPhiSeam.transportP93
    (data : NativeGK5AYOriginalPhiSeam first last)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g) :=
  .trans (.trans (.symm (data.at f)) (.old w)) (data.at g)

/-- A P93C.old of a TRUE original P89 four-cell remains a
genuine chosen P93C certificate. Its transport across the
NONTRIVIAL seam is an actual selected P94A four-proof with
recursive phi endpoints, not merely an equality of shadows. -/
def NativeGK5AYOriginalPhiSeam.transportP89Old
    (data : NativeGK5AYOriginalPhiSeam first last)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55P89InterchangeFourCell f g) :
    NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g) :=
  data.transportP93 (.old w)

/-- At fixed dependent F54 source endpoints, raw P93C reflection
means EVERY actual P93C comparison of raw .original source terms
is supported by a GENUINE original P89 Type-valued four-proof. -/
def nativeGK5AYRawP93Reflects
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) : Prop :=
  ∀ {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s),
    Nonempty (NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) →
    Nonempty (NativeF55P89InterchangeFourCell f g)

/-- Raw P93C nonreflection: an actual P93C comparison of
two genuinely old F55 wrappers, but no original P89 four-cell.
This is NOT automatically a GK5AQ BadPair at phi endpoints. -/
def nativeGK5AYRawP93Obstruction
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) : Prop :=
  ∃ (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s),
    Nonempty (NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) ∧
    ¬ Nonempty (NativeF55P89InterchangeFourCell f g)

/-- Exact local reflection iff absence of genuine raw P93C
nonreflection witnesses; does not assume a universal seam. -/
theorem nativeGK5AYRawP93Reflects_iff_no_obstruction
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeGK5AYRawP93Reflects first last ↔
      ¬ nativeGK5AYRawP93Obstruction first last := by
  classical
  constructor
  · intro h
    rintro ⟨r, s, f, g, hw, hno⟩
    exact hno (h f g hw)
  · intro h
    intro r s f g hw
    by_contra hno
    exact h ⟨r, s, f, g, hw, hno⟩

/-- With an ACTUAL seam, one raw P93C four-proof between old
original wrappers has a GK5AQ BadPair at true phi source
endpoints EXACTLY when there is no original P89 four-proof. -/
theorem nativeGK5AYRawP93_bad_iff_noP89
    (data : NativeGK5AYOriginalPhiSeam first last)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    nativeGK5AQBadPair first last f g ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell f g) := by
  constructor
  · exact fun bad => bad.2
  · exact fun missing => ⟨⟨data.transportP93 w⟩, missing⟩

/-- The seam upgrades a precisely SOURCE-typed raw P93C
obstruction to a genuine source GK5AQ BadPair, without asserting
that any such obstruction actually exists. -/
theorem nativeGK5AYRawObstruction_to_GK5AQ
    (data : NativeGK5AYOriginalPhiSeam first last)
    (h : nativeGK5AYRawP93Obstruction first last) :
    ∃ (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
      (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s),
      nativeGK5AQBadPair first last f g := by
  rcases h with ⟨r, s, f, g, ⟨w⟩, missing⟩
  exact ⟨r, s, f, g, ⟨⟨data.transportP93 w⟩, missing⟩⟩

/-- Under an actual seam, a raw P93C obstruction makes the
original P89→chosen P94A four-class map noninjective AT ITS
PRECISE original source F54 route slot. This is CONDITIONAL:
no noninjective pair is constructed without the obstruction. -/
theorem nativeGK5AYRawObstruction_forces_noninjective
    (data : NativeGK5AYOriginalPhiSeam first last)
    (h : nativeGK5AYRawP93Obstruction first last) :
    ∃ (r s : KuuNativeF45Tree.DepthRotationRoute p first last),
      ¬ Function.Injective
        (nativeGK5ANP89ToP94FourClassMap first last r s) := by
  rcases nativeGK5AYRawObstruction_to_GK5AQ data h with
    ⟨r, s, f, g, bad⟩
  exact ⟨r, s, (nativeGK5AQBadPair_exists_iff_not_injective
    first last r s).mp ⟨f, g, bad⟩⟩

/-- Conversely, INJECTIVITY of the actual source P89→P94A
four-class map in a fixed F54 slot, plus a genuine seam, forces
reflection of ALL actual chosen raw P93C comparisons of
original F55 wrappers in that slot. -/
theorem nativeGK5AYRawReflects_of_injective
    (data : NativeGK5AYOriginalPhiSeam first last)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (hinj : Function.Injective
      (nativeGK5ANP89ToP94FourClassMap first last r s))
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (w : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    Nonempty (NativeF55P89InterchangeFourCell f g) := by
  exact (nativeGK5ANP89ToP94_injective_iff_reflect first last r s).mp
    hinj f g ⟨data.transportP93 w⟩

/-- A REAL original P89 four-proof never becomes a BadPair
by wrapping its P93C.old witness and transporting through a
genuine seam; source and selected 4-cells both exist. -/
theorem nativeGK5AYOldP89SourceAndSelected
    (data : NativeGK5AYOriginalPhiSeam first last)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55P89InterchangeFourCell f g) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∧
    Nonempty (NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g)) ∧
    ¬ nativeGK5AQBadPair first last f g := by
  exact ⟨⟨w⟩, ⟨data.transportP89Old w⟩,
    fun bad => bad.2 ⟨w⟩⟩

/-- Even an actual P89.old selected P93C proof can have a GK5AU
source-hole if one of its selected raw .original endpoints is NOT
in the recursive phi-image. The old 4-cell does NOT manufacture
a missing original 3-cell phi-preimage. -/
theorem nativeGK5AYOldRawNonimage_is_internal_hole
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55P89InterchangeFourCell f g)
    (missing : ¬ nativeGK5ATPhiImage
      (NativeF55P92AssocComparison.original f)) :
    nativeGK5AUP94SourceHole
      (NativeF55P94UnitFourCell.old
        (NativeF55P93AssocFourCell.old w)) :=
  nativeGK5AUP94_hole_of_missing_left _ missing

/-- The REAL north-C60 original right-unit F55 source has a
composite F55 proof. P92B.original wraps the WHOLE composite;
recursive phi instead exposes its selected trans and refl.
They are distinct Type-valued raw P92B proof constructors.
There is NO asserted negation of a possible connecting 4-cell. -/
theorem nativeGK5AYNorthRawOriginal_ne_structuralPhi :
    (NativeF55P92AssocComparison.original
      nativeGK5AINorthPentagonWithIdentity) ≠
      nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity := by
  intro h
  cases h

private def nativeGK5AYNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def nativeGK5AYNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- A supplied north seam is a REAL selected 4-cell between two
raw Type-valued P92B 3-proofs already proved UNEQUAL above.
Consequently a seam cannot be replaced by raw 3-proof equality. -/
theorem nativeGK5AYNorthSeam_is_not_raw_equality
    (data : NativeGK5AYOriginalPhiSeam
      nativeGK5AYNorthFirst nativeGK5AYNorthLast) :
    ((NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity) ≠
      nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity) ∧
    Nonempty (NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity)) :=
  ⟨nativeGK5AYNorthRawOriginal_ne_structuralPhi,
    ⟨data.at nativeGK5AINorthPentagonWithIdentity⟩⟩

#print axioms NativeGK5AYOriginalPhiSeam
#print axioms nativeGK5AYSeam_nonempty_iff_pointwise
#print axioms NativeGK5AYOriginalPhiSeam.transportP93
#print axioms NativeGK5AYOriginalPhiSeam.transportP89Old
#print axioms nativeGK5AYRawP93Reflects
#print axioms nativeGK5AYRawP93Obstruction
#print axioms nativeGK5AYRawP93Reflects_iff_no_obstruction
#print axioms nativeGK5AYRawP93_bad_iff_noP89
#print axioms nativeGK5AYRawObstruction_to_GK5AQ
#print axioms nativeGK5AYRawObstruction_forces_noninjective
#print axioms nativeGK5AYRawReflects_of_injective
#print axioms nativeGK5AYOldP89SourceAndSelected
#print axioms nativeGK5AYOldRawNonimage_is_internal_hole
#print axioms nativeGK5AYNorthRawOriginal_ne_structuralPhi
#print axioms nativeGK5AYNorthSeam_is_not_raw_equality

end
end Kuu.F112.Physical
