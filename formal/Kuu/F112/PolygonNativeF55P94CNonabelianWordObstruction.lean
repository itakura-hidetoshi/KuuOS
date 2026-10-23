import Kuu.F112.PolygonNativeF55P94CGroupoidFourPresentation
import Mathlib.GroupTheory.FreeGroup.Basic
import Mathlib.Tactic

/-!
# F112-P94C3 — a genuine noncommutative F55 three-proof word receiver

Extract the ORDERED raw word of actual original nine-constructor F55
pentagon/square 3-proofs and the NEW P92B naturality generator into
mathlib's FREE (nonabelian) additive group on three constructor tags.

The exact full signed (pentagon, exchange square, odd C60 ZMod2) shadow
is the homomorphic ABELIAN image of that ordered group word.
Prove that the two differently ordered abstract words P+S and S+P
have the SAME full shadow but are NOT equal in the free group, using
the two noncommuting transpositions of S3 as a finite group receiver.

The original F55 four-stage pentagon / C60 six-sector square cells
map to the named free generators, rather than fictitious atoms.
The freeness/word receiver is deliberately *pre-four-cell-quotient*:
P94A's strict interchange can force relations absent in the bare free
group, so no claim that this invariant descends to P94A/P94C2.
Next: compute the ACTUAL five-stage associahedron critical relators
and their normal closure, rather than deriving 4-witnesses from shadows.

No Gray, new axioms, sorry/admit or changes to previous presentations.
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

inductive NativeF55P94CWordLetter where
  | pentagon
  | square
  | assocNaturality
  deriving DecidableEq

/-- Genuine nonabelian additive free group (NOT a free abelian group). -/
abbrev NativeF55P94CWord := FreeAddGroup NativeF55P94CWordLetter

/-- Group homomorphism to the entire pre-existing F55 physical shadow. -/
def nativeF55P94CWordToShadow :
    NativeF55P94CWord →+ KuuNativeF55Shadow :=
  FreeAddGroup.lift (fun
    | .pentagon => (((1 : Int), (0 : Int)), (0 : ZMod 2))
    | .square => (((0 : Int), (1 : Int)), (1 : ZMod 2))
    | .assocNaturality => 0)

/-- Read the exact ORDERED generator word of an ORIGINAL raw F55
source three-cell. Context transports do not reorder generators;
vertical concatenation is NONCOMMUTATIVE group addition. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p94cGroupWord
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    NativeF55P94CWord :=
  match cell with
  | .ident _ => 0
  | .pentagon _ _ _ _ => FreeAddGroup.of .pentagon
  | .disjointSquare _ _ => FreeAddGroup.of .square
  | .symm w => -w.p94cGroupWord
  | .trans w z => w.p94cGroupWord + z.p94cGroupWord
  | .leftContext w _ => w.p94cGroupWord
  | .rightContext _ w => w.p94cGroupWord
  | .precompose _ w => w.p94cGroupWord
  | .postcompose w _ => w.p94cGroupWord

/-- The complete F55 signed/odd charge is abelianization of the
noncommutative ordered ORIGINAL nine-constructor witness history. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p94cGroupWord_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeF55P94CWordToShadow cell.p94cGroupWord = cell.nativeShadow := by
  induction cell with
  | ident route =>
      change nativeF55P94CWordToShadow 0 = (0 : KuuNativeF55Shadow)
      exact map_zero _
  | pentagon _ _ _ _ =>
      change nativeF55P94CWordToShadow (FreeAddGroup.of .pentagon) =
        (((1 : Int), (0 : Int)), (0 : ZMod 2))
      simp [nativeF55P94CWordToShadow]
  | disjointSquare _ _ =>
      change nativeF55P94CWordToShadow (FreeAddGroup.of .square) =
        (((0 : Int), (1 : Int)), (1 : ZMod 2))
      simp [nativeF55P94CWordToShadow]
  | symm w ih =>
      change nativeF55P94CWordToShadow (-w.p94cGroupWord) = -w.nativeShadow
      simpa only [map_neg] using congrArg
        (fun z : KuuNativeF55Shadow => -z) ih
  | trans w z ihw ihz =>
      change nativeF55P94CWordToShadow (w.p94cGroupWord + z.p94cGroupWord) =
        w.nativeShadow + z.nativeShadow
      simpa only [map_add] using congrArg₂
        (fun u v : KuuNativeF55Shadow => u + v) ihw ihz
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose earlier w ih => exact ih
  | postcompose w later ih => exact ih

/-- Include new P92B associator naturality as a third independent
noncommutative source-letter with the explicitly selected zero
full-charge value, never identify it with the original F55 syntax. -/
def NativeF55P92AssocComparison.p94cGroupWord
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    NativeF55P94CWord :=
  match cell with
  | .original w => w.p94cGroupWord
  | .assocNaturality _ _ _ => FreeAddGroup.of .assocNaturality
  | .refl _ => 0
  | .symm w => -w.p94cGroupWord
  | .trans w z => w.p94cGroupWord + z.p94cGroupWord
  | .leftContext w _ => w.p94cGroupWord
  | .rightContext _ w => w.p94cGroupWord
  | .precompose _ w => w.p94cGroupWord
  | .postcompose w _ => w.p94cGroupWord

/-- P92B's free ordered witness refines its entire old F55
full shadow without pretending that matching charges imply a 4-cell. -/
theorem NativeF55P92AssocComparison.p94cGroupWord_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    nativeF55P94CWordToShadow cell.p94cGroupWord = cell.nativeShadow := by
  induction cell with
  | original old => exact old.p94cGroupWord_shadow
  | assocNaturality u v w =>
      change nativeF55P94CWordToShadow (FreeAddGroup.of .assocNaturality) =
        (0 : KuuNativeF55Shadow)
      simp [nativeF55P94CWordToShadow]
  | refl route =>
      change nativeF55P94CWordToShadow 0 = (0 : KuuNativeF55Shadow)
      exact map_zero _
  | symm w ih =>
      change nativeF55P94CWordToShadow (-w.p94cGroupWord) = -w.nativeShadow
      simpa only [map_neg] using congrArg
        (fun z : KuuNativeF55Shadow => -z) ih
  | trans w z ihw ihz =>
      change nativeF55P94CWordToShadow (w.p94cGroupWord + z.p94cGroupWord) =
        w.nativeShadow + z.nativeShadow
      simpa only [map_add] using congrArg₂
        (fun u v : KuuNativeF55Shadow => u + v) ihw ihz
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose earlier w ih => exact ih
  | postcompose w later ih => exact ih

/-- A noncommutative finite group receiver: actual transpositions
(01), (12) in S3 do NOT commute. -/
def nativeF55P94CWordToS3 :
    NativeF55P94CWord →+ Additive (Equiv.Perm (Fin 3)) :=
  FreeAddGroup.lift (fun
    | .pentagon => Additive.ofMul (Equiv.swap (0 : Fin 3) (1 : Fin 3))
    | .square => Additive.ofMul (Equiv.swap (1 : Fin 3) (2 : Fin 3))
    | .assocNaturality => 0)

/-- A closed finite S3 calculation proves the abstract two-letter
F55 word algebra is genuinely noncommutative (not an abelian shadow). -/
theorem nativeF55P94CWord_noncommuting_letters :
    (FreeAddGroup.of .pentagon : NativeF55P94CWord) +
      FreeAddGroup.of .square ≠
    (FreeAddGroup.of .square : NativeF55P94CWord) +
      FreeAddGroup.of .pentagon := by
  intro h
  have hh := congrArg nativeF55P94CWordToS3 h
  simp only [map_add, FreeAddGroup.lift_apply_of] at hh
  change
    Equiv.swap (0 : Fin 3) (1 : Fin 3) *
      Equiv.swap (1 : Fin 3) (2 : Fin 3) =
    Equiv.swap (1 : Fin 3) (2 : Fin 3) *
      Equiv.swap (0 : Fin 3) (1 : Fin 3) at hh
  have hne :
      Equiv.swap (0 : Fin 3) (1 : Fin 3) *
        Equiv.swap (1 : Fin 3) (2 : Fin 3) ≠
      Equiv.swap (1 : Fin 3) (2 : Fin 3) *
        Equiv.swap (0 : Fin 3) (1 : Fin 3) := by
    decide
  exact hne hh

/-- The same abstract noncommuting words agree under ALL THREE
signed/odd original F55 shadow coordinates: equality of observations
is only a NECESSARY check, never a nonabelian 4D coherence witness. -/
theorem nativeF55P94CWord_order_lost_by_shadow :
    nativeF55P94CWordToShadow
      ((FreeAddGroup.of .pentagon : NativeF55P94CWord) +
        FreeAddGroup.of .square) =
    nativeF55P94CWordToShadow
      ((FreeAddGroup.of .square : NativeF55P94CWord) +
        FreeAddGroup.of .pentagon) := by
  simp only [map_add, FreeAddGroup.lift_apply_of]
  exact add_comm _ _

/-- The concrete arbitrary-depth ORIGINAL pentagon generator is
indeed the free-group pentagon letter, with genuine F54 typed source. -/
theorem nativeF55P94CPentagonThreeCell_groupWord
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    (nativeF55P94CPentagonThreeCell t₁ t₂ t₃ t₄).p94cGroupWord =
      (FreeAddGroup.of .pentagon : NativeF55P94CWord) := rfl

/-- Actual original C60 top-six-sector square contributes the
distinct exchange/square letter and retains the odd ZMod2 phase. -/
theorem northHexagonNativeF55P92_original_square_groupWord :
    (NativeF55P92AssocComparison.original
      northHexagonNativeF55SquareCell).p94cGroupWord =
      (FreeAddGroup.of .square : NativeF55P94CWord) := rfl

#print axioms NativeF55P94CWord
#print axioms nativeF55P94CWordToShadow
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p94cGroupWord
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p94cGroupWord_shadow
#print axioms NativeF55P92AssocComparison.p94cGroupWord
#print axioms NativeF55P92AssocComparison.p94cGroupWord_shadow
#print axioms nativeF55P94CWordToS3
#print axioms nativeF55P94CWord_noncommuting_letters
#print axioms nativeF55P94CWord_order_lost_by_shadow
#print axioms nativeF55P94CPentagonThreeCell_groupWord
#print axioms northHexagonNativeF55P92_original_square_groupWord

end
end Kuu.F112.Physical
