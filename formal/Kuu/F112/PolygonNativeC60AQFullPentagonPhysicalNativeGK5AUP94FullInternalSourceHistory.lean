import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ATInternalSourceImageObstruction
import Mathlib.Tactic

/-!
F112-P94D3GK5AU — constructor-complete, proof-history-sensitive phi-source
obstruction tracing across genuine P93C and P94A Type-valued four-cells.

Unlike GK5AT's one explicit two-stage P94A trans, these TWO recursive
predicates visit ALL 16 historical P93C constructors and ALL 19 P94A
constructors, following their actual proof terms, not quotient equality
or equal shadows. The positive "hole" means a particular raw P92B
three-proof on a constructor boundary or generator input has no
ORIGINAL F55 phi-preimage. It is source-saturation failure, NOT by
itself a P89/P94A BadPair or failure of original P89 injectivity.

The P93C .old constructor retains its original P89 witness; we
separately audit the raw selected .original endpoints, because a
P89 witness does not magically identify .original with the recursive
GK5AI phi image. The P94A .old node visits its nested P93C history.
New unit generators are examined with their actual P92B boundaries.
No global normal form or unconditional reflection is assumed.

A hole-free trans has a genuine dependent original F55 fiber
over its ACTUAL intermediate P92B proof. Thus GK5AT's exact
two-step reflection/BadPair dichotomy becomes available for any
hole-free trans, and clean local reflection yields source descent.
North C60 explicitly has a P93C-in-P94A hole despite zero parity.

Strict 空 authority; independent Kuu → Qi; append-only, same public
root 107, protected PR #1558 untouched. Lean v4.30.0-rc2;
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry/admit/native_decide, new axioms, or Gray reconstruction.
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
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55P92AssocComparison p r s}

/-- A proof-term-recursive source hole in ANY of P93C's SIXTEEN
constructors, including their hidden raw P92B generator arguments.
Every comparison's own two typed endpoints are audited. -/
def nativeGK5AUP93CSourceHole
    (w : NativeF55P93AssocFourCell f g) : Prop :=
  (¬ nativeGK5ATPhiImage f) ∨
  (¬ nativeGK5ATPhiImage g) ∨
  (match w with
    | .old _ => False
    | .refl _ => False
    | .symm inner => nativeGK5AUP93CSourceHole inner
    | .trans left right =>
        nativeGK5AUP93CSourceHole left ∨
        nativeGK5AUP93CSourceHole right
    | .verticalLeftUnit _ => False
    | .verticalRightUnit _ => False
    | .verticalAssoc u v z =>
        (¬ nativeGK5ATPhiImage u) ∨
        (¬ nativeGK5ATPhiImage v) ∨
        (¬ nativeGK5ATPhiImage z)
    | .leftWhisker prior inner =>
        (¬ nativeGK5ATPhiImage prior) ∨
        nativeGK5AUP93CSourceHole inner
    | .rightWhisker inner suffix =>
        nativeGK5AUP93CSourceHole inner ∨
        (¬ nativeGK5ATPhiImage suffix)
    | .leftContext inner _ => nativeGK5AUP93CSourceHole inner
    | .rightContext _ inner => nativeGK5AUP93CSourceHole inner
    | .precompose _ inner => nativeGK5AUP93CSourceHole inner
    | .postcompose inner _ => nativeGK5AUP93CSourceHole inner
    | .horizontalLeft inner other =>
        nativeGK5AUP93CSourceHole inner ∨
        (¬ nativeGK5ATPhiImage other)
    | .horizontalRight other inner =>
        (¬ nativeGK5ATPhiImage other) ∨
        nativeGK5AUP93CSourceHole inner
    | .interchange u v z t =>
        (¬ nativeGK5ATPhiImage u) ∨
        (¬ nativeGK5ATPhiImage v) ∨
        (¬ nativeGK5ATPhiImage z) ∨
        (¬ nativeGK5ATPhiImage t))

/-- A proof-term-recursive source hole in ALL NINETEEN P94A
constructors, recursively reopening the actual embedded P93C
certificate at .old, plus all raw middle/whisker/interchange
arguments. This is a Prop about Type-valued evidence, not a
quotient/shadow criterion. -/
def nativeGK5AUP94SourceHole
    (w : NativeF55P94UnitFourCell f g) : Prop :=
  (¬ nativeGK5ATPhiImage f) ∨
  (¬ nativeGK5ATPhiImage g) ∨
  (match w with
    | .old historical => nativeGK5AUP93CSourceHole historical
    | .refl _ => False
    | .symm inner => nativeGK5AUP94SourceHole inner
    | .trans left right =>
        nativeGK5AUP94SourceHole left ∨
        nativeGK5AUP94SourceHole right
    | .verticalLeftUnit _ => False
    | .verticalRightUnit _ => False
    | .verticalAssoc u v z =>
        (¬ nativeGK5ATPhiImage u) ∨
        (¬ nativeGK5ATPhiImage v) ∨
        (¬ nativeGK5ATPhiImage z)
    | .leftWhisker prior inner =>
        (¬ nativeGK5ATPhiImage prior) ∨
        nativeGK5AUP94SourceHole inner
    | .rightWhisker inner suffix =>
        nativeGK5AUP94SourceHole inner ∨
        (¬ nativeGK5ATPhiImage suffix)
    | .leftContext inner _ => nativeGK5AUP94SourceHole inner
    | .rightContext _ inner => nativeGK5AUP94SourceHole inner
    | .precompose _ inner => nativeGK5AUP94SourceHole inner
    | .postcompose inner _ => nativeGK5AUP94SourceHole inner
    | .horizontalLeft inner other =>
        nativeGK5AUP94SourceHole inner ∨
        (¬ nativeGK5ATPhiImage other)
    | .horizontalRight other inner =>
        (¬ nativeGK5ATPhiImage other) ∨
        nativeGK5AUP94SourceHole inner
    | .interchange u v z t =>
        (¬ nativeGK5ATPhiImage u) ∨
        (¬ nativeGK5ATPhiImage v) ∨
        (¬ nativeGK5ATPhiImage z) ∨
        (¬ nativeGK5ATPhiImage t)
    | .horizontalUnit _ _ => False
    | .leftContextUnit _ _ => False
    | .rightContextUnit _ _ => False)

/-- A clean four-cell requires absence of every precisely indexed
internal selected-proof hole; it is NOT a proof of P89 reflection. -/
def nativeGK5AUP94SourceSaturated
    (w : NativeF55P94UnitFourCell f g) : Prop :=
  ¬ nativeGK5AUP94SourceHole w

/-- A P93C hole remains visible inside its genuine P94A .old embedding. -/
theorem nativeGK5AUP93C_hole_embeds
    (w : NativeF55P93AssocFourCell f g)
    (h : nativeGK5AUP93CSourceHole w) :
    nativeGK5AUP94SourceHole (NativeF55P94UnitFourCell.old w) := by
  exact Or.inr (Or.inr h)

/-- Any source-saturated P94A proof has exact phi-image endpoints,
not merely matching additive shadows. -/
theorem nativeGK5AUP94_saturated_endpoint_images
    (w : NativeF55P94UnitFourCell f g)
    (clean : nativeGK5AUP94SourceSaturated w) :
    nativeGK5ATPhiImage f ∧ nativeGK5ATPhiImage g := by
  classical
  constructor
  · by_contra hf
    exact clean (Or.inl hf)
  · by_contra hg
    exact clean (Or.inr (Or.inl hg))

/-- The ACTUAL middle of any P94A trans with no history hole
has an original F55 proof-relevant dependent phi-fiber. -/
theorem nativeGK5AU_clean_trans_middle_fiber
    {middle : NativeF55P92AssocComparison p r s}
    (left : NativeF55P94UnitFourCell f middle)
    (right : NativeF55P94UnitFourCell middle g)
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.trans left right)) :
    Nonempty (nativeGK5ATPhiFiber middle) := by
  classical
  apply (nativeGK5ATPhiImage_iff_fiber middle).mp
  by_contra missing
  have holeLeft : nativeGK5AUP94SourceHole left :=
    Or.inr (Or.inl missing)
  have hole : nativeGK5AUP94SourceHole
      (NativeF55P94UnitFourCell.trans left right) :=
    Or.inr (Or.inr (Or.inl holeLeft))
  exact clean hole

/-- GK5AT upgrades from a particular two-step proof to ANY two-step
node whose FULL (not just external) P94A history is source-saturated:
original P89 descent, or a real local GK5AQ BadPair at a genuine
original middle preimage. No fabricated global source normal form. -/
theorem nativeGK5AU_clean_trans_reflect_or_local_bad
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (origF origG : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (middle : NativeF55P92AssocComparison p u v)
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural origF) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural origG))
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.trans left right)) :
    Nonempty (NativeF55P89InterchangeFourCell origF origG) ∨
    ∃ mid : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v,
      nativeGK5AIOriginalToP92Structural mid = middle ∧
      (nativeGK5AQBadPair first last origF mid ∨
       nativeGK5AQBadPair first last mid origG) := by
  have hm : nativeGK5ATPhiImage middle :=
    (nativeGK5ATPhiImage_iff_fiber middle).mpr
      (nativeGK5AU_clean_trans_middle_fiber left right clean)
  rcases nativeGK5ATTwoStep_reflect_or_obstruction
      origF origG middle left right with reflection | obstruction
  · exact .inl reflection
  · rcases obstruction with noImage | localBad
    · exact False.elim (noImage hm)
    · exact .inr localBad

/-- Source-saturation together with the absence of BOTH genuine
localized source BadPairs is sufficient for P89 descent of a
selected two-stage P94A proof of original endpoints. -/
theorem nativeGK5AU_clean_trans_descends
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (origF origG : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (middle : NativeF55P92AssocComparison p u v)
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural origF) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural origG))
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.trans left right))
    (noLocal : ∀ mid : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v,
      nativeGK5AIOriginalToP92Structural mid = middle →
      ¬ (nativeGK5AQBadPair first last origF mid ∨
         nativeGK5AQBadPair first last mid origG)) :
    Nonempty (NativeF55P89InterchangeFourCell origF origG) := by
  rcases nativeGK5AU_clean_trans_reflect_or_local_bad
      origF origG middle left right clean with reflection | localBad
  · exact reflection
  · rcases localBad with ⟨mid, hmid, bad⟩
    exact False.elim (noLocal mid hmid bad)

/-- An internal non-image middle forces a hole regardless of the
outer endpoints or any parity invariant of their selected proof. -/
theorem nativeGK5AU_trans_nonimage_middle_hole
    {middle : NativeF55P92AssocComparison p r s}
    (left : NativeF55P94UnitFourCell f middle)
    (right : NativeF55P94UnitFourCell middle g)
    (missing : ¬ nativeGK5ATPhiImage middle) :
    nativeGK5AUP94SourceHole
      (NativeF55P94UnitFourCell.trans left right) := by
  have leftHole : nativeGK5AUP94SourceHole left :=
    Or.inr (Or.inl missing)
  exact Or.inr (Or.inr (Or.inl leftHole))

/-- The real north selected associator-naturality is absent from phi
even INSIDE a reflexive P93C certificate embedded by P94A .old. -/
def nativeGK5AUNorthNestedP93C :
    NativeF55P94UnitFourCell
      nativeGK5AINorthAddedUnitAssocCell
      nativeGK5AINorthAddedUnitAssocCell :=
  .old (.refl nativeGK5AINorthAddedUnitAssocCell)

/-- Independent internal P93C/P94A source hole and zero left/right
context parity coexist for the same true north C60 4-proof term.
This is NOT evidence for a P89 noninjective source pair. -/
theorem nativeGK5AUNorth_nestedP93C_hole_zeroGrade :
    nativeGK5AUP94SourceHole nativeGK5AUNorthNestedP93C ∧
    (((nativeGK5AUNorthNestedP93C.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
    (((nativeGK5AUNorthNestedP93C.gk5apRightUnitCount : Nat) : ZMod 2) = 0) := by
  constructor
  · have p93Hole : nativeGK5AUP93CSourceHole
        (NativeF55P93AssocFourCell.refl
          nativeGK5AINorthAddedUnitAssocCell) :=
      Or.inl nativeGK5ATNorthAddedAssoc_noPhiImage
    exact nativeGK5AUP93C_hole_embeds _ p93Hole
  · exact nativeGK5ASNorthAssocLoop_zeroGrade nativeGK5AUNorthNestedP93C

#print axioms nativeGK5AUP93CSourceHole
#print axioms nativeGK5AUP94SourceHole
#print axioms nativeGK5AUP94SourceSaturated
#print axioms nativeGK5AUP93C_hole_embeds
#print axioms nativeGK5AUP94_saturated_endpoint_images
#print axioms nativeGK5AU_clean_trans_middle_fiber
#print axioms nativeGK5AU_clean_trans_reflect_or_local_bad
#print axioms nativeGK5AU_clean_trans_descends
#print axioms nativeGK5AU_trans_nonimage_middle_hole
#print axioms nativeGK5AUNorthNestedP93C
#print axioms nativeGK5AUNorth_nestedP93C_hole_zeroGrade

end
end Kuu.F112.Physical
