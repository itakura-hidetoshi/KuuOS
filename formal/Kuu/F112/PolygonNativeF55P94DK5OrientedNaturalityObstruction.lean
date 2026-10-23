import Kuu.F112.PolygonNativeF55P94DK5GroupoidPeifferDescent
import Mathlib.Tactic

/-!
# F112-P94D3H — oriented K₅ P92B naturality-count obstruction

The actual K₅ shell has six ORIGINAL F55 pentagons, three NEW
P92B associator-naturality squares, and NINE genuinely dependent
F45/F54 face anchors. Their outward orientations are +,+,- for
the naturality squares, NOT +,+,+. The signed naturality count
is therefore +1, despite the FULL original F55 signed/odd shadow
of the nine oriented faces being zero.

Construct the independent integer N-count directly from the true
P94C3 noncommutative three-letter FreeAddGroup. Prove that:
* all ORIGINAL nine-constructor F55 source 3-cells have N-count 0;
* all P93C and P94A Type-valued 4-cell constructors preserve
  the N-count, including actual middle-four interchange;
* the N-count descends to the minimal normal word kernel generated
  by ALL genuinely typed P94A 4-cells (P94D3F);
* both distinct P94C2 groupoid completions preserve that count,
  including inverse cancellation and inverseRespect.

For the NINE ACTUAL outward-oriented, genuinely anchored K₅ faces,
form only a FORMAL noncommutative aggregate word. Its N-count is +1
and its complete old F55 shadow is zero. It is NOT asserted that
their F54 endpoints already admit a genuine global 3-pasting.

If a proposed global 4-cell has exactly this formal difference word,
it is impossible in the EXISTING P94A/P94C2 four-cell presentations.
This does not rule out an independently extended 4-dimensional
pentagonator presentation with an additional source generator or
corrected boundary. No Gray, sorry, admit or added logical axioms.
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

/-- The NEW associator-naturality integer coordinate, deliberately
independent of the full older F55 signed/odd physical shadow. -/
def nativeK5NaturalityCount : NativeF55P94CWord →+ ℤ :=
  FreeAddGroup.lift (fun
    | .pentagon => 0
    | .square => 0
    | .assocNaturality => 1)

theorem nativeK5NaturalityCount_pentagon :
    nativeK5NaturalityCount nativeK5PNPentagon = 0 := by
  simp [nativeK5NaturalityCount, nativeK5PNPentagon]

theorem nativeK5NaturalityCount_square :
    nativeK5NaturalityCount nativeK5PNSquare = 0 := by
  simp [nativeK5NaturalityCount, nativeK5PNSquare]

theorem nativeK5NaturalityCount_naturality :
    nativeK5NaturalityCount nativeK5PNNaturality = 1 := by
  simp [nativeK5NaturalityCount, nativeK5PNNaturality]

/-- Every actual ORIGINAL F55 3-cell, including inverses, pasted
histories and true binary contexts, has no NEW P92B naturality letter. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nCount_zero
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeK5NaturalityCount cell.p94cGroupWord = 0 := by
  induction cell with
  | ident route =>
      change nativeK5NaturalityCount 0 = 0
      exact map_zero _
  | pentagon _ _ _ _ =>
      change nativeK5NaturalityCount (FreeAddGroup.of .pentagon) = 0
      exact nativeK5NaturalityCount_pentagon
  | disjointSquare _ _ =>
      change nativeK5NaturalityCount (FreeAddGroup.of .square) = 0
      exact nativeK5NaturalityCount_square
  | symm w ih =>
      change nativeK5NaturalityCount (-w.p94cGroupWord) = 0
      simp only [map_neg, ih, neg_zero]
  | trans w z ihw ihz =>
      change nativeK5NaturalityCount (w.p94cGroupWord + z.p94cGroupWord) = 0
      simp only [map_add, ihw, ihz, add_zero]
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose earlier w ih => exact ih
  | postcompose w later ih => exact ih

/-- P93C includes genuine original P89 witnesses and a newly
declared middle-four interchange, neither of which alters N count.
All recursive context/whisker constructors are checked individually. -/
theorem NativeF55P93AssocFourCell.nCount_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
    nativeK5NaturalityCount f.p94cGroupWord =
      nativeK5NaturalityCount g.p94cGroupWord := by
  induction w with
  | old witness =>
      simp only [NativeF55P92AssocComparison.p94cGroupWord,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nCount_zero]
  | refl cell => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord, map_add]
  | verticalRightUnit f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord, map_add]
  | verticalAssoc f g h =>
      change nativeK5NaturalityCount
          ((f.p94cGroupWord + g.p94cGroupWord) + h.p94cGroupWord) =
        nativeK5NaturalityCount
          (f.p94cGroupWord + (g.p94cGroupWord + h.p94cGroupWord))
      exact congrArg nativeK5NaturalityCount (add_assoc _ _ _)
  | leftWhisker prior witness ih =>
      simpa only [NativeF55P92AssocComparison.p94cGroupWord, map_add] using
        congrArg (fun z : ℤ => nativeK5NaturalityCount prior.p94cGroupWord + z) ih
  | rightWhisker witness suffix ih =>
      simpa only [NativeF55P92AssocComparison.p94cGroupWord, map_add] using
        congrArg (fun z : ℤ => z + nativeK5NaturalityCount suffix.p94cGroupWord) ih
  | leftContext witness later ih => exact ih
  | rightContext earlier witness ih => exact ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih
  | horizontalLeft witness g ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_p94cGroupWord,
        map_add] using congrArg
          (fun z : ℤ => z + nativeK5NaturalityCount g.p94cGroupWord) ih
  | horizontalRight f witness ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_p94cGroupWord,
        map_add] using congrArg
          (fun z : ℤ => nativeK5NaturalityCount f.p94cGroupWord + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      change nativeK5NaturalityCount
          ((f₁.p94cGroupWord + f₂.p94cGroupWord) +
            (g₁.p94cGroupWord + g₂.p94cGroupWord)) =
        nativeK5NaturalityCount
          ((f₁.p94cGroupWord + g₁.p94cGroupWord) +
            (f₂.p94cGroupWord + g₂.p94cGroupWord))
      simp only [map_add]
      abel

/-- All genuine P94A 4-cell generators preserve the independent
N-coordinate, not merely the old (P,S,odd-phase) shadow. -/
theorem NativeF55P94UnitFourCell.nCount_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) :
    nativeK5NaturalityCount f.p94cGroupWord =
      nativeK5NaturalityCount g.p94cGroupWord := by
  induction w with
  | old witness => exact witness.nCount_sound
  | refl cell => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord, map_add]
  | verticalRightUnit f =>
      simp [NativeF55P92AssocComparison.p94cGroupWord, map_add]
  | verticalAssoc f g h =>
      change nativeK5NaturalityCount
          ((f.p94cGroupWord + g.p94cGroupWord) + h.p94cGroupWord) =
        nativeK5NaturalityCount
          (f.p94cGroupWord + (g.p94cGroupWord + h.p94cGroupWord))
      exact congrArg nativeK5NaturalityCount (add_assoc _ _ _)
  | leftWhisker prior witness ih =>
      simpa only [NativeF55P92AssocComparison.p94cGroupWord, map_add] using
        congrArg (fun z : ℤ => nativeK5NaturalityCount prior.p94cGroupWord + z) ih
  | rightWhisker witness suffix ih =>
      simpa only [NativeF55P92AssocComparison.p94cGroupWord, map_add] using
        congrArg (fun z : ℤ => z + nativeK5NaturalityCount suffix.p94cGroupWord) ih
  | leftContext witness later ih => exact ih
  | rightContext earlier witness ih => exact ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih
  | horizontalLeft witness g ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_p94cGroupWord,
        map_add] using congrArg
          (fun z : ℤ => z + nativeK5NaturalityCount g.p94cGroupWord) ih
  | horizontalRight f witness ih =>
      simpa only [NativeF55P92AssocComparison.horizontal_p94cGroupWord,
        map_add] using congrArg
          (fun z : ℤ => nativeK5NaturalityCount f.p94cGroupWord + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      change nativeK5NaturalityCount
          ((f₁.p94cGroupWord + f₂.p94cGroupWord) +
            (g₁.p94cGroupWord + g₂.p94cGroupWord)) =
        nativeK5NaturalityCount
          ((f₁.p94cGroupWord + g₁.p94cGroupWord) +
            (f₂.p94cGroupWord + g₂.p94cGroupWord))
      simp only [map_add]
      abel
  | horizontalUnit u v =>
      simp [NativeF55P92AssocComparison.horizontal_p94cGroupWord,
        NativeF55P92AssocComparison.p94cGroupWord]
  | leftContextUnit route later => rfl
  | rightContextUnit earlier route => rfl

/-- Genuine 4-cell word defects lie in the exact N-count kernel,
and hence the entire minimal NORMAL closure of ALL typed 4-cells
also lies in it; no shadow-derived 4-cell is fabricated. -/
theorem nativeK5P94ATypedNormalClosure_le_NCount_ker :
    nativeK5P94ATypedNormalClosure D E ≤ nativeK5NaturalityCount.ker := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  rcases hw with ⟨ev⟩
  cases ev with
  | ofFourCell four =>
      change nativeK5NaturalityCount (_ - _) = 0
      rw [map_sub, sub_eq_zero]
      exact four.nCount_sound

/-- An actual descended N-count on the noncommutative P94A
all-TYPE-valued-four-cell word correction quotient. -/
def nativeK5P94ATypedNCount :
    NativeK5P94ATypedCorrectedWord D E →+ ℤ :=
  QuotientAddGroup.lift (nativeK5P94ATypedNormalClosure D E)
    nativeK5NaturalityCount nativeK5P94ATypedNormalClosure_le_NCount_ker

theorem nativeK5P94ATypedNCount_spec (w : NativeF55P94CWord) :
    nativeK5P94ATypedNCount
      (nativeK5P94ATypedClass (D := D) (E := E) w) =
        nativeK5NaturalityCount w :=
  QuotientAddGroup.lift_mk' (nativeK5P94ATypedNormalClosure D E)
    nativeK5P94ATypedNormalClosure_le_NCount_ker w

/-- The two genuinely distinct P94C2 groupoid four-cell syntaxes
also preserve N-count, using their full generator-wise P94D3G
typed-word descent rather than any numerical shadow shortcut. -/
theorem NativeF55P94GroupFourCell.nCount_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94GroupFourCell f g) :
    nativeK5NaturalityCount f.p94cGroupWord =
      nativeK5NaturalityCount g.p94cGroupWord := by
  have h := congrArg (nativeK5P94ATypedNCount (D := D) (E := E))
    w.p94aTypedWord_sound
  simpa only [nativeK5P94ATypedNCount_spec] using h

theorem NativeF55P94CGroupFourCell.nCount_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94CGroupFourCell f g) :
    nativeK5NaturalityCount f.p94cGroupWord =
      nativeK5NaturalityCount g.p94cGroupWord := by
  have h := congrArg (nativeK5P94ATypedNCount (D := D) (E := E))
    w.p94aTypedWord_sound
  simpa only [nativeK5P94ATypedNCount_spec] using h

/-- N count descends further to each genuinely typed P94C2
proof-relevant 3-Hom quotient, without equating the two groupoids. -/
def nativeK5P94CGroupNCount
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P94CGroupFourClasses first last r s → ℤ :=
  Quot.lift
    (fun raw => nativeK5NaturalityCount raw.p94cGroupWord)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.nCount_sound)

section FiveNativeStages

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- The N-count for a GENUINE oriented anchored K₅ face,
not a guessed number on an abstract polygon. -/
def nativeK5AnchoredFaceNCount (tag : NativeK5FaceTag) : ℤ :=
  nativeK5NaturalityCount
    (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.2.2.p94cGroupWord

/-- P94D3A's exact OUTWARD orientation reverses square 2
and three pentagons. This is not the +3 naive naturality count. -/
def nativeK5FaceExpectedNCount : NativeK5FaceTag → ℤ
  | .square0 | .square1 => 1
  | .square2 => -1
  | .pentagon3 | .pentagon4 | .pentagon5
  | .pentagon6 | .pentagon7 | .pentagon8 => 0

theorem nativeK5AnchoredFaceNCount_exact (tag : NativeK5FaceTag) :
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 tag =
      nativeK5FaceExpectedNCount tag := by
  cases tag with
  | square0 =>
      change nativeK5NaturalityCount (FreeAddGroup.of .assocNaturality) = 1
      exact nativeK5NaturalityCount_naturality
  | square1 =>
      change nativeK5NaturalityCount (FreeAddGroup.of .assocNaturality) = 1
      exact nativeK5NaturalityCount_naturality
  | square2 =>
      change nativeK5NaturalityCount (-(FreeAddGroup.of .assocNaturality)) = -1
      simp [nativeK5NaturalityCount]
  | pentagon3 =>
      change nativeK5NaturalityCount (FreeAddGroup.of .pentagon) = 0
      exact nativeK5NaturalityCount_pentagon
  | pentagon4 =>
      change nativeK5NaturalityCount (FreeAddGroup.of .pentagon) = 0
      exact nativeK5NaturalityCount_pentagon
  | pentagon5 =>
      change nativeK5NaturalityCount (-(FreeAddGroup.of .pentagon)) = 0
      simp [nativeK5NaturalityCount]
  | pentagon6 =>
      change nativeK5NaturalityCount (FreeAddGroup.of .pentagon) = 0
      exact nativeK5NaturalityCount_pentagon
  | pentagon7 =>
      change nativeK5NaturalityCount (-(FreeAddGroup.of .pentagon)) = 0
      simp [nativeK5NaturalityCount]
  | pentagon8 =>
      change nativeK5NaturalityCount (-(FreeAddGroup.of .pentagon)) = 0
      simp [nativeK5NaturalityCount]

/-- An algebraic nine-face word in the free NONCOMMUTATIVE group.
These nine honest anchored Type-valued P92B certificates have
DIFFERENT original F54 boundaries: this word is NOT a falsely
claimed global three-cell pasting. The order is explicitly fixed. -/
def nativeK5NineAnchoredFaceFormalWord : NativeF55P94CWord :=
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square0).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square1).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon3).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon5).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon6).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon7).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon8).2.2.2.p94cGroupWord

/-- The genuine nine-face formal word has SIGNED N-charge +1,
not +3: square0=+1, square1=+1, square2=-1. -/
theorem nativeK5NineAnchoredFaceFormalWord_NCount_one :
    nativeK5NaturalityCount
      (nativeK5NineAnchoredFaceFormalWord t1 t2 t3 t4 t5) = 1 := by
  simp only [nativeK5NineAnchoredFaceFormalWord, map_add]
  simp [← nativeK5AnchoredFaceNCount, nativeK5AnchoredFaceNCount_exact,
    nativeK5FaceExpectedNCount]

/-- ALL old F55 signed/odd shadow coordinates vanish on precisely
the same nine oriented actual source faces, although N-charge
survives in the new independent coordinate. -/
theorem nativeK5NineAnchoredFaceFormalWord_shadow_zero :
    nativeF55P94CWordToShadow
      (nativeK5NineAnchoredFaceFormalWord t1 t2 t3 t4 t5) = 0 := by
  simp only [nativeK5NineAnchoredFaceFormalWord, map_add,
    NativeF55P92AssocComparison.p94cGroupWord_shadow]
  simp [nativeK5AnchoredFace_fullShadow, nativeK5CandidateFaceShadow,
    nativeK5FaceTagFin]

/-- No actual P94A four-cell word congruence can kill the
oriented formal nine-face word: its new integral obstruction is 1. -/
theorem nativeK5NineAnchoredFaceFormalWord_not_mem_P94ATyped :
    nativeK5NineAnchoredFaceFormalWord t1 t2 t3 t4 t5 ∉
      nativeK5P94ATypedNormalClosure D E := by
  intro h
  have hz := nativeK5P94ATypedNormalClosure_le_NCount_ker (D := D) (E := E) h
  change nativeK5NaturalityCount
    (nativeK5NineAnchoredFaceFormalWord t1 t2 t3 t4 t5) = 0 at hz
  rw [nativeK5NineAnchoredFaceFormalWord_NCount_one] at hz
  norm_num at hz

/-- In particular, the corrected noncommutative word quotient does
NOT identify the formal oriented nine-face word with zero. -/
theorem nativeK5NineAnchoredFaceFormalWord_quotient_nonzero :
    nativeK5P94ATypedClass (D := D) (E := E)
      (nativeK5NineAnchoredFaceFormalWord t1 t2 t3 t4 t5) ≠ 0 := by
  intro h
  have hh := congrArg (nativeK5P94ATypedNCount (D := D) (E := E)) h
  simpa only [nativeK5P94ATypedNCount_spec, map_zero,
    nativeK5NineAnchoredFaceFormalWord_NCount_one] using hh

/-- Conditional, precisely scoped 4D filling obstruction.
If some genuinely typed P94C2 comparison had THIS exact nine-face
word as its boundary defect, the existing P94C2 four-cell grammar
would contradict the proven independent N-count. The global
F54 3-pasting itself is still unconstructed. -/
theorem nativeK5NineAnchoredFaceFormalWord_no_P94C2_boundary
    {first : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {last : KuuNativeF45Tree p n₂ m₂ p₀ q₀ p₁ q₁}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (four : NativeF55P94CGroupFourCell f g)
    (hword : f.p94cGroupWord - g.p94cGroupWord =
      nativeK5NineAnchoredFaceFormalWord t1 t2 t3 t4 t5) : False := by
  have hmem := four.p94aTypedRelator_mem
  rw [hword] at hmem
  exact nativeK5NineAnchoredFaceFormalWord_not_mem_P94ATyped
    t1 t2 t3 t4 t5 hmem

end FiveNativeStages

#print axioms nativeK5NaturalityCount
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nCount_zero
#print axioms NativeF55P93AssocFourCell.nCount_sound
#print axioms NativeF55P94UnitFourCell.nCount_sound
#print axioms nativeK5P94ATypedNormalClosure_le_NCount_ker
#print axioms nativeK5P94ATypedNCount_spec
#print axioms NativeF55P94GroupFourCell.nCount_sound
#print axioms NativeF55P94CGroupFourCell.nCount_sound
#print axioms nativeK5P94CGroupNCount
#print axioms nativeK5AnchoredFaceNCount_exact
#print axioms nativeK5NineAnchoredFaceFormalWord_NCount_one
#print axioms nativeK5NineAnchoredFaceFormalWord_shadow_zero
#print axioms nativeK5NineAnchoredFaceFormalWord_not_mem_P94ATyped
#print axioms nativeK5NineAnchoredFaceFormalWord_quotient_nonzero
#print axioms nativeK5NineAnchoredFaceFormalWord_no_P94C2_boundary

end
end Kuu.F112.Physical
