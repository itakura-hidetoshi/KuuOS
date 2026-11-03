import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AUP94FullInternalSourceHistory
import Mathlib.Tactic

/-!
F112-P94D3GK5AV — exact source-vertex two-edge reconstruction for
P93C vertical histories nested inside genuine P94A .old proof terms.

GK5AU recursively audited ALL 19 P94A and ALL 16 embedded P93C
constructors for exact F55 phi-source holes. This module takes the
NEXT nontrivial step: source-saturation of an ACTUAL P93C vertical
trans, even hidden under P94A .old, produces a genuine proof-relevant
original F55 witness for the selected internal P92B midpoint.
This witness constructs a real GK5AS source-vertex TWO-EDGE chain
whose selected edges are precisely the given P94A comparison halves
(after exact dependent equality transport, not shadow equality).

The two-edge chain is then localized by the existing GK5AS
P89-reflection-or-bad-step theorem. Absence of its actual BadStep
is a sufficient original P89 descent hypothesis. A chosen original
north C60 P92B assocNaturality remains a non-source inner midpoint
of a selected P93C two-refl, even though its P94A old wrapper has
left/right parity (0,0). This is NOT a GK5AQ source BadPair.

No global normalization or reflection of the other P94A generators
is asserted. Independent Kuu -> Qi; strict 空 authority, public
root 107 unchanged; #1558 Draft/open; pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry/admit/native_decide, new axioms, Gray or global gluing.
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

/-- A missing original F55 source at the RIGHT endpoint is a
source hole for EVERY one of the sixteen P93C constructors. -/
theorem nativeGK5AVP93C_hole_of_missing_right
    (w : NativeF55P93AssocFourCell f g)
    (missing : ¬ nativeGK5ATPhiImage g) :
    nativeGK5AUP93CSourceHole w := by
  cases w <;> exact Or.inr (Or.inl missing)

/-- The symmetric exact left-endpoint source hole for P93C. -/
theorem nativeGK5AVP93C_hole_of_missing_left
    (w : NativeF55P93AssocFourCell f g)
    (missing : ¬ nativeGK5ATPhiImage f) :
    nativeGK5AUP93CSourceHole w := by
  cases w <;> exact Or.inl missing

/-- Source-saturation of a GENUINE selected P93C vertical composite
forces an original F55 proof-relevant dependent phi-fiber over its
ACTUAL internal P92B midpoint. No quotient or numerical shadow. -/
theorem nativeGK5AVP93C_clean_trans_middle_fiber
    {middle : NativeF55P92AssocComparison p r s}
    (left : NativeF55P93AssocFourCell f middle)
    (right : NativeF55P93AssocFourCell middle g)
    (clean : ¬ nativeGK5AUP93CSourceHole
      (NativeF55P93AssocFourCell.trans left right)) :
    Nonempty (nativeGK5ATPhiFiber middle) := by
  classical
  apply (nativeGK5ATPhiImage_iff_fiber middle).mp
  by_contra missing
  have hLeft : nativeGK5AUP93CSourceHole left :=
    nativeGK5AVP93C_hole_of_missing_right left missing
  exact clean (Or.inr (Or.inr (Or.inl hLeft)))

/-- The P94A .old wrapper does NOT erase P93C's internal vertical
source-saturation requirement: its midpoint must still have a
true original F55 phi-fiber. -/
theorem nativeGK5AVP94OldP93C_clean_trans_middle_fiber
    {middle : NativeF55P92AssocComparison p r s}
    (left : NativeF55P93AssocFourCell f middle)
    (right : NativeF55P93AssocFourCell middle g)
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.old
        (NativeF55P93AssocFourCell.trans left right))) :
    Nonempty (nativeGK5ATPhiFiber middle) := by
  apply nativeGK5AVP93C_clean_trans_middle_fiber left right
  intro h
  exact clean (Or.inr (Or.inr h))

/-- A selected TWO-STEP P94A comparison with an ACTUAL original
F55 middle phi-preimage produces a genuine two-edge GK5AS
source-vertex chain, not just an externally source-labeled endpoint
pair. The actual supplied selected halves are transported by the
precise equality phi(sourceMid) = middle. -/
def nativeGK5AVTwoStepSourceChain
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (sourceF sourceG : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    {middle : NativeF55P92AssocComparison p u v}
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural sourceF) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural sourceG))
    (sourceMid : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (hmid : nativeGK5AIOriginalToP92Structural sourceMid = middle) :
    NativeGK5ASSourceVertexChain sourceF sourceG := by
  have l : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural sourceF)
      (nativeGK5AIOriginalToP92Structural sourceMid) := by
    rw [hmid]
    exact left
  have t : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural sourceMid)
      (nativeGK5AIOriginalToP92Structural sourceG) := by
    rw [hmid]
    exact right
  exact .step l (.step t (.nil sourceG))

/-- A source-saturated selected P94A vertical trans of ORIGINAL
endpoints has an actual original middle phi-source and an exact
two-edge source-vertex chain. GK5AS localizes any missing P89
reflection at a REAL edge of THAT chain. -/
theorem nativeGK5AVP94CleanTrans_sourceChain_reflect_or_bad
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (sourceF sourceG : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (middle : NativeF55P92AssocComparison p u v)
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural sourceF) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural sourceG))
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.trans left right)) :
    ∃ sourceMid : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v,
      ∃ hmid : nativeGK5AIOriginalToP92Structural sourceMid = middle,
      Nonempty (NativeF55P89InterchangeFourCell sourceF sourceG) ∨
        (nativeGK5AVTwoStepSourceChain sourceF sourceG
          left right sourceMid hmid).HasBadStep := by
  classical
  rcases (nativeGK5AU_clean_trans_middle_fiber left right clean) with
    ⟨⟨sourceMid, hmid⟩⟩
  refine ⟨sourceMid, hmid, ?_⟩
  exact (nativeGK5AVTwoStepSourceChain
    sourceF sourceG left right sourceMid hmid).reflects_or_badStep

/-- The same source-vertex reconstruction is available when the
actual comparison is buried as a P93C .trans inside P94A .old.
It uses the independent P93C source-fiber theorem, not an
unjustified assumption that .old proves an original P89 comparison. -/
theorem nativeGK5AVP93CInsideP94_sourceChain_reflect_or_bad
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (sourceF sourceG : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (middle : NativeF55P92AssocComparison p u v)
    (left : NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural sourceF) middle)
    (right : NativeF55P93AssocFourCell
      middle (nativeGK5AIOriginalToP92Structural sourceG))
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.old
        (NativeF55P93AssocFourCell.trans left right))) :
    ∃ sourceMid : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v,
      ∃ hmid : nativeGK5AIOriginalToP92Structural sourceMid = middle,
      Nonempty (NativeF55P89InterchangeFourCell sourceF sourceG) ∨
        (nativeGK5AVTwoStepSourceChain sourceF sourceG
          (.old left) (.old right) sourceMid hmid).HasBadStep := by
  classical
  rcases nativeGK5AVP94OldP93C_clean_trans_middle_fiber left right clean
    with ⟨⟨sourceMid, hmid⟩⟩
  refine ⟨sourceMid, hmid, ?_⟩
  exact (nativeGK5AVTwoStepSourceChain
    sourceF sourceG (.old left) (.old right) sourceMid hmid).reflects_or_badStep

/-- Source descent when the explicitly constructed genuine two-edge
selected chain has NO local P89/P94A BadStep. This is a genuine
conditional P89 four-cell witness, not an ambient quotient equality. -/
theorem nativeGK5AVP93CInsideP94_descends_of_noBad
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (sourceF sourceG sourceMid :
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (middle : NativeF55P92AssocComparison p u v)
    (left : NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural sourceF) middle)
    (right : NativeF55P93AssocFourCell
      middle (nativeGK5AIOriginalToP92Structural sourceG))
    (hmid : nativeGK5AIOriginalToP92Structural sourceMid = middle)
    (noBad : ¬ (nativeGK5AVTwoStepSourceChain sourceF sourceG
      (NativeF55P94UnitFourCell.old left)
      (NativeF55P94UnitFourCell.old right) sourceMid hmid).HasBadStep) :
    Nonempty (NativeF55P89InterchangeFourCell sourceF sourceG) :=
  (nativeGK5AVTwoStepSourceChain sourceF sourceG
      (.old left) (.old right) sourceMid hmid).reflects_of_no_badStep noBad

/-- An ACTUAL two-step P93C proof with a non-source midpoint, nested
in the P94A old constructor. Its whole selected P94A proof has
left/right parity zero, but the exact original phi-fiber is empty.
This is NOT an original P89/P94A noninjectivity witness. -/
def nativeGK5AVNorthNestedP93CDoubleRefl :
    NativeF55P94UnitFourCell
      nativeGK5AINorthAddedUnitAssocCell
      nativeGK5AINorthAddedUnitAssocCell :=
  .old (.trans (.refl nativeGK5AINorthAddedUnitAssocCell)
    (.refl nativeGK5AINorthAddedUnitAssocCell))

theorem nativeGK5AVNorthNestedP93CDoubleRefl_obstruction_zeroGrade :
    (¬ nativeGK5AUP94SourceSaturated
      nativeGK5AVNorthNestedP93CDoubleRefl) ∧
    (¬ Nonempty (nativeGK5ATPhiFiber nativeGK5AINorthAddedUnitAssocCell)) ∧
    (((nativeGK5AVNorthNestedP93CDoubleRefl.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
    (((nativeGK5AVNorthNestedP93CDoubleRefl.gk5apRightUnitCount : Nat) : ZMod 2) = 0) := by
  constructor
  · intro clean
    have h : nativeGK5AUP94SourceHole nativeGK5AVNorthNestedP93CDoubleRefl :=
      nativeGK5AUP94_hole_of_missing_left _
        nativeGK5ATNorthAddedAssoc_noPhiImage
    exact clean h
  · constructor
    · rintro ⟨⟨old, h⟩⟩
      exact nativeGK5ATNorthAddedAssoc_noPhiImage ⟨old, h⟩
    · exact nativeGK5ASNorthAssocLoop_zeroGrade nativeGK5AVNorthNestedP93CDoubleRefl

#print axioms nativeGK5AVP93C_hole_of_missing_right
#print axioms nativeGK5AVP93C_hole_of_missing_left
#print axioms nativeGK5AVP93C_clean_trans_middle_fiber
#print axioms nativeGK5AVP94OldP93C_clean_trans_middle_fiber
#print axioms nativeGK5AVTwoStepSourceChain
#print axioms nativeGK5AVP94CleanTrans_sourceChain_reflect_or_bad
#print axioms nativeGK5AVP93CInsideP94_sourceChain_reflect_or_bad
#print axioms nativeGK5AVP93CInsideP94_descends_of_noBad
#print axioms nativeGK5AVNorthNestedP93CDoubleRefl
#print axioms nativeGK5AVNorthNestedP93CDoubleRefl_obstruction_zeroGrade

end
end Kuu.F112.Physical
