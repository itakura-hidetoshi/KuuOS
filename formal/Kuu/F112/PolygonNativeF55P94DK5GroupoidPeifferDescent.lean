import Kuu.F112.PolygonNativeF55P94DK5AllTypedFourCellWordKernel
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Tactic

/-!
# F112-P94D3G — genuine P94C2 groupoid completion descends to the P94A typed word kernel

P94D3F constructed the minimal normal subgroup of the genuinely
type-indexed P94A 4-cell word defects, with full F55 shadow descent.

This file tests BOTH distinct P94C2 Type-valued groupoid-completion
presentations. Every actual P94C2 4-cell, including formal 3-proof
inverse cancellation, has equal images in the existing P94A normal
WORD quotient. This does NOT assert the new inverse 4-cell witnesses
already exist in P94A's Type-valued source.

For the P94CGroup source with inverseRespect, a separate NORMAL
closure of all source 4-cell word defects is proven EQUAL to the
P94A normal word closure: at the coarse three-letter group-word
level the inverse-completion requires no new relators. The distinct
Type-valued four-cell presentations remain distinct.

The full typed P94A normal relation subgroup is equipped with
its ambient free-group conjugation action, inclusion boundary,
Peiffer law and an explicit Type-valued crossed-module certificate.
Both P94C2 proof languages map actual source four-cell differences
into this relation subgroup.

No equivalence of the two Type-valued groupoids, global strict
3/n-category, genuine K5 nine-face global sphere or independent
pentagonator is asserted. No Gray, sorry, admit, or new axioms.
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

/-- All actual P94C2 four-cells in the groupoid completion with
independently adjoined inverse cancellation preserve the P94A
type-generated noncommutative word quotient. Proof by induction
on the full Type-valued 18-constructor source, not by shadows. -/
theorem NativeF55P94GroupFourCell.p94aTypedWord_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94GroupFourCell f g) :
    nativeK5P94ATypedClass (D := D) (E := E) f.p94cGroupWord =
      nativeK5P94ATypedClass (D := D) (E := E) g.p94cGroupWord := by
  induction w with
  | old witness => exact nativeK5P94ATypedFourCell_word_descends witness
  | refl cell => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord]
  | verticalRightUnit f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord]
  | verticalAssoc f g h =>
      exact congrArg (nativeK5P94ATypedClass (D := D) (E := E))
        (add_assoc f.p94cGroupWord g.p94cGroupWord h.p94cGroupWord)
  | leftWhisker prior witness ih =>
      simpa only [NativeF55P92AssocComparison.p94cGroupWord, map_add] using
        congrArg
          (fun z : NativeK5P94ATypedCorrectedWord D E =>
            nativeK5P94ATypedClass (D := D) (E := E) prior.p94cGroupWord + z) ih
  | rightWhisker witness suffix ih =>
      simpa only [NativeF55P92AssocComparison.p94cGroupWord, map_add] using
        congrArg
          (fun z : NativeK5P94ATypedCorrectedWord D E =>
            z + nativeK5P94ATypedClass (D := D) (E := E) suffix.p94cGroupWord) ih
  | leftContext witness later ih => exact ih
  | rightContext earlier witness ih => exact ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih
  | horizontalLeft witness g ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_p94cGroupWord,
        map_add] using
        congrArg
          (fun z : NativeK5P94ATypedCorrectedWord D E =>
            z + nativeK5P94ATypedClass (D := D) (E := E) g.p94cGroupWord) ih
  | horizontalRight f witness ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_p94cGroupWord,
        map_add] using
        congrArg
          (fun z : NativeK5P94ATypedCorrectedWord D E =>
            nativeK5P94ATypedClass (D := D) (E := E) f.p94cGroupWord + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      exact nativeK5P94ATypedFourCell_word_descends
        (NativeF55P94UnitFourCell.interchange f₁ f₂ g₁ g₂)
  | inverseLeft f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord]
  | inverseRight f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord]

/-- The SECOND, independently completed P94C2 presentation has
a genuine inverseRespect 4-cell generator. The new generator
preserves the same noncommutative word quotient by map_neg. -/
theorem NativeF55P94CGroupFourCell.p94aTypedWord_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94CGroupFourCell f g) :
    nativeK5P94ATypedClass (D := D) (E := E) f.p94cGroupWord =
      nativeK5P94ATypedClass (D := D) (E := E) g.p94cGroupWord := by
  induction w with
  | old witness => exact nativeK5P94ATypedFourCell_word_descends witness
  | refl cell => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | inverseLeft f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord]
  | inverseRight f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord]
  | inverseRespect witness ih =>
      simpa only [NativeF55P92AssocComparison.p94cGroupWord, map_neg] using
        congrArg
          (fun z : NativeK5P94ATypedCorrectedWord D E => -z) ih
  | leftWhisker prior witness ih =>
      simpa only [NativeF55P92AssocComparison.p94cGroupWord, map_add] using
        congrArg
          (fun z : NativeK5P94ATypedCorrectedWord D E =>
            nativeK5P94ATypedClass (D := D) (E := E) prior.p94cGroupWord + z) ih
  | rightWhisker witness suffix ih =>
      simpa only [NativeF55P92AssocComparison.p94cGroupWord, map_add] using
        congrArg
          (fun z : NativeK5P94ATypedCorrectedWord D E =>
            z + nativeK5P94ATypedClass (D := D) (E := E) suffix.p94cGroupWord) ih
  | leftContext witness later ih => exact ih
  | rightContext earlier witness ih => exact ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih
  | horizontalLeft witness g ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_p94cGroupWord,
        map_add] using
        congrArg
          (fun z : NativeK5P94ATypedCorrectedWord D E =>
            z + nativeK5P94ATypedClass (D := D) (E := E) g.p94cGroupWord) ih
  | horizontalRight f witness ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_p94cGroupWord,
        map_add] using
        congrArg
          (fun z : NativeK5P94ATypedCorrectedWord D E =>
            nativeK5P94ATypedClass (D := D) (E := E) f.p94cGroupWord + z) ih

/-- A map from the actual independent P94C2 first groupoid 3-hom
classes to the all-P94A normal WORD quotient: witness-descended. -/
def nativeK5P94GroupFourToP94ATypedWord
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P94GroupFourClasses first last r s →
      NativeK5P94ATypedCorrectedWord D E :=
  Quot.lift
    (fun raw => nativeK5P94ATypedClass (D := D) (E := E) raw.p94cGroupWord)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.p94aTypedWord_sound)

/-- The second P94C2 groupoid also has an actual descended
noncommutative word map, respecting every inverseRespect witness. -/
def nativeK5P94CGroupFourToP94ATypedWord
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P94CGroupFourClasses first last r s →
      NativeK5P94ATypedCorrectedWord D E :=
  Quot.lift
    (fun raw => nativeK5P94ATypedClass (D := D) (E := E) raw.p94cGroupWord)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.p94aTypedWord_sound)

/-- Exact noncommutative kernel membership for an arbitrary actual
groupoid-completion 4-cell, not merely equal signed charges. -/
theorem NativeF55P94GroupFourCell.p94aTypedRelator_mem
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94GroupFourCell f g) :
    f.p94cGroupWord - g.p94cGroupWord ∈
      nativeK5P94ATypedNormalClosure D E :=
  (QuotientAddGroup.eq_iff_sub_mem).1 w.p94aTypedWord_sound

theorem NativeF55P94CGroupFourCell.p94aTypedRelator_mem
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94CGroupFourCell f g) :
    f.p94cGroupWord - g.p94cGroupWord ∈
      nativeK5P94ATypedNormalClosure D E :=
  (QuotientAddGroup.eq_iff_sub_mem).1 w.p94aTypedWord_sound

/-- The second groupoid's independently selected Type-valued
four-cell evidence generates a second, nontrivial normal kernel. -/
inductive NativeK5P94CGroupTypedWordRelator
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    NativeF55P94CWord → Type (max (max uD uE) (max vD vE)) where
  | ofFourCell
      {p : Polygon} {a b : D} {x y : E}
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (four : NativeF55P94CGroupFourCell f g) :
      NativeK5P94CGroupTypedWordRelator D E
        (f.p94cGroupWord - g.p94cGroupWord)

def nativeK5P94CGroupTypedRelators
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] : Set NativeF55P94CWord :=
  {w | Nonempty (NativeK5P94CGroupTypedWordRelator D E w)}

def nativeK5P94CGroupTypedNormalClosure
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    AddSubgroup NativeF55P94CWord :=
  AddSubgroup.normalClosure (nativeK5P94CGroupTypedRelators D E)

instance nativeK5P94CGroupTypedNormalClosure_normal
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    (nativeK5P94CGroupTypedNormalClosure D E).Normal := by
  unfold nativeK5P94CGroupTypedNormalClosure
  infer_instance

/-- P94C2 adds Type-valued inverse-coherence generators,
but their coarse noncommutative word relators are already
in the smallest P94A typed normal subgroup. Conversely, each
P94A 4-cell is a real old constructor in this groupoid.
This proves EXACT equality of these two algebraic normal kernels;
it does NOT claim Type-valued presentation equivalence. -/
theorem nativeK5P94CGroupTypedNormalClosure_eq_P94A :
    nativeK5P94CGroupTypedNormalClosure D E =
      nativeK5P94ATypedNormalClosure D E := by
  apply le_antisymm
  · apply AddSubgroup.normalClosure_le_normal
    intro w hw
    rcases hw with ⟨ev⟩
    cases ev with
    | ofFourCell four => exact four.p94aTypedRelator_mem
  · apply AddSubgroup.normalClosure_le_normal
    intro w hw
    rcases hw with ⟨ev⟩
    cases ev with
    | ofFourCell four =>
        apply AddSubgroup.subset_normalClosure
        exact ⟨NativeK5P94CGroupTypedWordRelator.ofFourCell (.old four)⟩

/-- Peiffer RELATION module for every actually typed P94A four-cell,
not only the first north C60 P/N witness of P94D3D. -/
abbrev NativeK5P94ATypedPeifferKernel
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :=
  nativeK5P94ATypedNormalClosure D E

def nativeK5P94ATypedPeifferBoundary :
    NativeK5P94ATypedPeifferKernel D E →+ NativeF55P94CWord :=
  (nativeK5P94ATypedNormalClosure D E).subtype

/-- Conjugation = algebraic whiskering, closed by ACTUAL
mathlib normality of the all-typed four-cell relator subgroup. -/
def nativeK5P94ATypedPeifferAct
    (g : NativeF55P94CWord)
    (r : NativeK5P94ATypedPeifferKernel D E) :
    NativeK5P94ATypedPeifferKernel D E :=
  ⟨g + (r : NativeF55P94CWord) - g, by
    have h :
        g + (r : NativeF55P94CWord) + -g ∈
          nativeK5P94ATypedNormalClosure D E :=
      (inferInstance :
        (nativeK5P94ATypedNormalClosure D E).Normal).conj_mem
          (r : NativeF55P94CWord) r.property g
    simpa only [sub_eq_add_neg] using h⟩

theorem nativeK5P94ATypedPeifferAct_zero (g : NativeF55P94CWord) :
    nativeK5P94ATypedPeifferAct (D := D) (E := E) g 0 = 0 := by
  apply Subtype.ext
  change g + (0 : NativeF55P94CWord) - g = 0
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

theorem nativeK5P94ATypedPeifferAct_add
    (g : NativeF55P94CWord)
    (r s : NativeK5P94ATypedPeifferKernel D E) :
    nativeK5P94ATypedPeifferAct g (r + s) =
      nativeK5P94ATypedPeifferAct g r +
        nativeK5P94ATypedPeifferAct g s := by
  apply Subtype.ext
  change g + ((r : NativeF55P94CWord) + (s : NativeF55P94CWord)) - g =
    (g + (r : NativeF55P94CWord) - g) +
      (g + (s : NativeF55P94CWord) - g)
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

theorem nativeK5P94ATypedPeifferAct_identity
    (r : NativeK5P94ATypedPeifferKernel D E) :
    nativeK5P94ATypedPeifferAct (0 : NativeF55P94CWord) r = r := by
  apply Subtype.ext
  change (0 : NativeF55P94CWord) + r - 0 = r
  simp

theorem nativeK5P94ATypedPeifferAct_comp
    (g h : NativeF55P94CWord)
    (r : NativeK5P94ATypedPeifferKernel D E) :
    nativeK5P94ATypedPeifferAct (g + h) r =
      nativeK5P94ATypedPeifferAct g
        (nativeK5P94ATypedPeifferAct h r) := by
  apply Subtype.ext
  change (g + h) + (r : NativeF55P94CWord) - (g + h) =
    g + (h + (r : NativeF55P94CWord) - h) - g
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

theorem nativeK5P94ATypedPeifferBoundary_equivariant
    (g : NativeF55P94CWord)
    (r : NativeK5P94ATypedPeifferKernel D E) :
    nativeK5P94ATypedPeifferBoundary
        (nativeK5P94ATypedPeifferAct g r) =
      g + nativeK5P94ATypedPeifferBoundary r - g := rfl

/-- The full typed Peiffer identity is PROVED in the actual
noncommutative group, no assumed abelianization or new axiom. -/
theorem nativeK5P94ATypedPeiffer_identity
    (r s : NativeK5P94ATypedPeifferKernel D E) :
    nativeK5P94ATypedPeifferAct
        (nativeK5P94ATypedPeifferBoundary r) s =
      r + s - r := by
  apply Subtype.ext
  rfl

/-- Type-valued crossed-module package for the full typed P94A
word-relator kernel. Its scope is the algebraic normal inclusion,
not an independent K5 four-dimensional pentagonator. -/
structure NativeK5P94ATypedCrossedModuleData
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] where
  boundary : NativeK5P94ATypedPeifferKernel D E →+ NativeF55P94CWord
  act : NativeF55P94CWord →
    NativeK5P94ATypedPeifferKernel D E →
      NativeK5P94ATypedPeifferKernel D E
  act_identity : ∀ r, act 0 r = r
  act_comp : ∀ g h r, act (g + h) r = act g (act h r)
  act_zero : ∀ g, act g 0 = 0
  act_add : ∀ g r s, act g (r + s) = act g r + act g s
  boundary_equivariant : ∀ g r,
    boundary (act g r) = g + boundary r - g
  peiffer : ∀ r s, act (boundary r) s = r + s - r

def nativeK5P94ATypedCrossedModule :
    NativeK5P94ATypedCrossedModuleData D E :=
  { boundary := nativeK5P94ATypedPeifferBoundary
    act := nativeK5P94ATypedPeifferAct
    act_identity := nativeK5P94ATypedPeifferAct_identity
    act_comp := nativeK5P94ATypedPeifferAct_comp
    act_zero := nativeK5P94ATypedPeifferAct_zero
    act_add := nativeK5P94ATypedPeifferAct_add
    boundary_equivariant := nativeK5P94ATypedPeifferBoundary_equivariant
    peiffer := nativeK5P94ATypedPeiffer_identity }

/-- Attach the actual P94C2 Type-valued four-cell to its canonical
element of the FULL typed Peiffer relation subgroup. -/
def NativeF55P94CGroupFourCell.peifferRelator
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (four : NativeF55P94CGroupFourCell f g) :
    NativeK5P94ATypedPeifferKernel D E :=
  ⟨f.p94cGroupWord - g.p94cGroupWord, four.p94aTypedRelator_mem⟩

theorem NativeF55P94CGroupFourCell.peifferRelator_boundary
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (four : NativeF55P94CGroupFourCell f g) :
    nativeK5P94ATypedPeifferBoundary four.peifferRelator =
      f.p94cGroupWord - g.p94cGroupWord := rfl

#print axioms NativeF55P94GroupFourCell.p94aTypedWord_sound
#print axioms NativeF55P94CGroupFourCell.p94aTypedWord_sound
#print axioms nativeK5P94GroupFourToP94ATypedWord
#print axioms nativeK5P94CGroupFourToP94ATypedWord
#print axioms NativeF55P94GroupFourCell.p94aTypedRelator_mem
#print axioms NativeF55P94CGroupFourCell.p94aTypedRelator_mem
#print axioms nativeK5P94CGroupTypedNormalClosure_eq_P94A
#print axioms nativeK5P94ATypedPeifferAct
#print axioms nativeK5P94ATypedPeifferAct_zero
#print axioms nativeK5P94ATypedPeifferAct_add
#print axioms nativeK5P94ATypedPeifferAct_identity
#print axioms nativeK5P94ATypedPeifferAct_comp
#print axioms nativeK5P94ATypedPeifferBoundary_equivariant
#print axioms nativeK5P94ATypedPeiffer_identity
#print axioms nativeK5P94ATypedCrossedModule
#print axioms NativeF55P94CGroupFourCell.peifferRelator_boundary

end
end Kuu.F112.Physical
