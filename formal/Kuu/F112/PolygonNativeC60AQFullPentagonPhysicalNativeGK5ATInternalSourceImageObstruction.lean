import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ASSourceVertexObstructionLocalization
import Mathlib.Tactic

/-!
F112-P94D3GK5AT — exact phi-image membership for an INTERNAL selected
P92B witness of a genuine two-stage P94A four-cell comparison.

GK5AS localized reflection along chains whose vertices are already
ORIGINAL F55 Type-valued three-cell histories. A selected P94A
vertical composite, however, has an intermediate P92B proof term:
nothing in the P94A constructor says that middle proof is an
image of the original GK5AI structural map.

Here the image is defined by an actual dependent original witness,
NOT shadow equality, parity, quotient equality or a chosen inverse.
The structural image is closed under the genuine F55 identity,
symmetry, vertical composite and contextual operations. A true
two-stage selected P94A comparison of original endpoints either
reflects as an original P89 four-cell, OR has an exact obstruction:
(1) its internal P92B middle is not in the original phi-image, OR
(2) it is in that image, but one genuine local original F55 pair is
a GK5AQ P94A/P89 BadPair. Neither obstruction is asserted to exist
unconditionally for arbitrary original endpoints.

The true north C60 new assocNaturality P92B proof supplies a concrete
NON-image middle of an actual two-refl P94A composite, although that
entire selected proof has left/right context parity (0,0).
This has NO original F55 endpoints for that slot: it is NOT a
counterexample to P89→P94A injectivity.

This module handles one explicit vertical trans node, not an
unconditional normalization of all 19 P94A constructors or hidden
P93C histories. No old source signatures or history are altered.
Independent Kuu → Qi; strict 空 authority; public root 107.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, Gray or global gluing.
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

/-- Genuine image of the original nine-constructor F55 evidence in
the separately selected Type-valued P92B proof presentation. -/
def nativeGK5ATPhiImage
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (selected : NativeF55P92AssocComparison p r s) : Prop :=
  ∃ original : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s,
    nativeGK5AIOriginalToP92Structural original = selected

/-- A proof-relevant dependent fiber, retaining the actual original
F55 evidence and the precise equality to the selected proof term. -/
def nativeGK5ATPhiFiber
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (selected : NativeF55P92AssocComparison p r s) :=
  {original : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s //
    nativeGK5AIOriginalToP92Structural original = selected}

theorem nativeGK5ATPhiImage_iff_fiber
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (selected : NativeF55P92AssocComparison p r s) :
    nativeGK5ATPhiImage selected ↔
      Nonempty (nativeGK5ATPhiFiber selected) := by
  constructor
  · rintro ⟨original, h⟩
    exact ⟨⟨original, h⟩⟩
  · rintro ⟨⟨original, h⟩⟩
    exact ⟨original, h⟩

/-- Original source identity has a literal structural phi-preimage. -/
theorem nativeGK5ATPhiImage_ident
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK5ATPhiImage (NativeF55P92AssocComparison.refl r) := by
  exact ⟨.ident r, rfl⟩

/-- Exact source-image closure under the original F55 symm constructor. -/
theorem nativeGK5ATPhiImage_symm
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {selected : NativeF55P92AssocComparison p r s}
    (h : nativeGK5ATPhiImage selected) :
    nativeGK5ATPhiImage (NativeF55P92AssocComparison.symm selected) := by
  rcases h with ⟨original, rfl⟩
  exact ⟨.symm original, rfl⟩

/-- Exact source-image closure under vertical composition. -/
theorem nativeGK5ATPhiImage_trans
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {left : NativeF55P92AssocComparison p r s}
    {right : NativeF55P92AssocComparison p s t}
    (hl : nativeGK5ATPhiImage left)
    (hr : nativeGK5ATPhiImage right) :
    nativeGK5ATPhiImage (NativeF55P92AssocComparison.trans left right) := by
  rcases hl with ⟨u, rfl⟩
  rcases hr with ⟨v, rfl⟩
  exact ⟨.trans u v, rfl⟩

/-- Genuine original-source left contextualization preserves image
membership, without using equality of C60 observables. -/
theorem nativeGK5ATPhiImage_leftContext
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {selected : NativeF55P92AssocComparison p r s}
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (h : nativeGK5ATPhiImage selected) :
    nativeGK5ATPhiImage
      (NativeF55P92AssocComparison.leftContext selected later) := by
  rcases h with ⟨original, rfl⟩
  exact ⟨.leftContext original later, rfl⟩

/-- Genuine original-source right contextualization preserves image
membership, keeping both original F54 depth indices. -/
theorem nativeGK5ATPhiImage_rightContext
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {selected : NativeF55P92AssocComparison p r s}
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l mc pc ma pa)
    (h : nativeGK5ATPhiImage selected) :
    nativeGK5ATPhiImage
      (NativeF55P92AssocComparison.rightContext earlier selected) := by
  rcases h with ⟨original, rfl⟩
  exact ⟨.rightContext earlier original, rfl⟩

/-- TWO nonexclusive sources of obstruction for a SELECTED P94A
vertical trans node: a missing middle original F55 source, or a
genuine selected-but-not-P89-reflectable local original pair.
The second branch explicitly requires a GK5AQ BadPair witness. -/
def nativeGK5ATTwoStepObstruction
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (middle : NativeF55P92AssocComparison p r s) : Prop :=
  (¬ nativeGK5ATPhiImage middle) ∨
    ∃ mid : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s,
      nativeGK5AIOriginalToP92Structural mid = middle ∧
      (nativeGK5AQBadPair first last f mid ∨
       nativeGK5AQBadPair first last mid g)

/-- An ACTUAL selected P94A two-step comparison gives an original P89
comparison or a localized source-image / nonreflection obstruction.
Crucially, its arbitrary selected P92B middle is NOT silently assumed
to possess an original F55 preimage. -/
theorem nativeGK5ATTwoStep_reflect_or_obstruction
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (middle : NativeF55P92AssocComparison p r s)
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural g)) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∨
      nativeGK5ATTwoStepObstruction f g middle := by
  classical
  by_cases hm : nativeGK5ATPhiImage middle
  · rcases hm with ⟨mid, hmid⟩
    by_cases hl : Nonempty (NativeF55P89InterchangeFourCell f mid)
    · by_cases hr : Nonempty (NativeF55P89InterchangeFourCell mid g)
      · rcases hl with ⟨wl⟩
        rcases hr with ⟨wr⟩
        exact .inl ⟨.trans wl wr⟩
      · have wright : NativeF55P94UnitFourCell
            (nativeGK5AIOriginalToP92Structural mid)
            (nativeGK5AIOriginalToP92Structural g) := by
          rw [hmid]
          exact right
        exact .inr (.inr ⟨mid, hmid, .inr ⟨⟨wright⟩, hr⟩⟩)
    · have wleft : NativeF55P94UnitFourCell
          (nativeGK5AIOriginalToP92Structural f)
          (nativeGK5AIOriginalToP92Structural mid) := by
        rw [hmid]
        exact left
      exact .inr (.inr ⟨mid, hmid, .inl ⟨⟨wleft⟩, hl⟩⟩)
  · exact .inr (.inl hm)

/-- Conditional localization of any TRUE GK5AQ bad pair across a
given selected two-stage factorization. Not an existence claim of
such a nonreflecting pair. -/
theorem nativeGK5ATBadPair_forces_internalObstruction
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (middle : NativeF55P92AssocComparison p r s)
    (left : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f) middle)
    (right : NativeF55P94UnitFourCell
      middle (nativeGK5AIOriginalToP92Structural g))
    (bad : nativeGK5AQBadPair first last f g) :
    nativeGK5ATTwoStepObstruction f g middle := by
  rcases nativeGK5ATTwoStep_reflect_or_obstruction
      f g middle left right with hsource | hobstruction
  · exact False.elim (bad.2 hsource)
  · exact hobstruction

/-- Actual north C60 selected assocNaturality has no original F55
phi-fiber, by the existing original ordered-context no-go. -/
theorem nativeGK5ATNorthAddedAssoc_noPhiImage :
    ¬ nativeGK5ATPhiImage nativeGK5AINorthAddedUnitAssocCell := by
  rintro ⟨old, h⟩
  exact nativeGK5AINorthAddedUnitAssoc_noOriginalPreimage ⟨old, h⟩

/-- A genuine selected P94A FOUR proof with a visible internal P92B
middle: two P94A reflexive generators composed vertically. -/
def nativeGK5ATNorthDoubleRefl :
    NativeF55P94UnitFourCell
      nativeGK5AINorthAddedUnitAssocCell
      nativeGK5AINorthAddedUnitAssocCell :=
  .trans (.refl nativeGK5AINorthAddedUnitAssocCell)
    (.refl nativeGK5AINorthAddedUnitAssocCell)

/-- Concrete original-source obstruction INSIDE a real selected
P94A composite. Every selected left/right count parity is zero
at this slot, but even the intermediate P92B Type-valued witness
has no original F55 source. This is NOT a P89 noninjectivity proof. -/
theorem nativeGK5ATNorthDoubleRefl_nonimage_middle_zeroGrade :
    (¬ Nonempty
      (nativeGK5ATPhiFiber nativeGK5AINorthAddedUnitAssocCell)) ∧
    (((nativeGK5ATNorthDoubleRefl.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
    (((nativeGK5ATNorthDoubleRefl.gk5apRightUnitCount : Nat) : ZMod 2) = 0) := by
  constructor
  · rintro ⟨⟨old, h⟩⟩
    exact nativeGK5ATNorthAddedAssoc_noPhiImage ⟨old, h⟩
  · exact nativeGK5ASNorthAssocLoop_zeroGrade nativeGK5ATNorthDoubleRefl

#print axioms nativeGK5ATPhiImage_iff_fiber
#print axioms nativeGK5ATPhiImage_ident
#print axioms nativeGK5ATPhiImage_symm
#print axioms nativeGK5ATPhiImage_trans
#print axioms nativeGK5ATPhiImage_leftContext
#print axioms nativeGK5ATPhiImage_rightContext
#print axioms nativeGK5ATTwoStep_reflect_or_obstruction
#print axioms nativeGK5ATBadPair_forces_internalObstruction
#print axioms nativeGK5ATNorthAddedAssoc_noPhiImage
#print axioms nativeGK5ATNorthDoubleRefl
#print axioms nativeGK5ATNorthDoubleRefl_nonimage_middle_zeroGrade

end
end Kuu.F112.Physical
