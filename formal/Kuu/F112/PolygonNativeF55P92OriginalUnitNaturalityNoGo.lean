import Kuu.F112.PolygonNativeF55P91HorizontalRouteCongruence

/-!
# F112-P92A — genuine original-F55 source NO-GO for associator naturality

The original F54 syntax has actual zero-edge RotationChain.refl route
atoms distinct from all nontrivial primitive local rotations. We
record ordered noncommutative left/right-context Bool words for each
such atom, keeping genuine original source information.
The two primitive original F55 generators (pentagon, square) contain
NO zero-chain atoms. All seven other original F55 generators preserve
the word invariant, including arbitrary contexts and route whiskering.

For any three properly dependent original F45 stages, the genuine
P90B source triple-associator naturality with identity-chain inputs
has distinct left/right word lists. Hence NO original nine-constructor
F55 Type-valued comparison exists for those inputs. This is a
presentation-specific no-go, NOT a universal no-go for strict 3/n
categories. The original nonzero C60 odd exchange phase is retained.

P91C constructed two total quotient-level triple routes; these are
provably unequal on original unit inputs, rather than being assumed
equal from interchange or selected shadow evaluation.
No Gray, axioms, sorry/admit, or removal of 107 public roots.
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

/-- True original F54 zero-chain atoms, recorded with the complete
ordered left/right binary F45 context in which they occur. -/
def KuuNativeF45Tree.DepthRotationRoute.p92UnitContextWords
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    List (List Bool) := by
  induction route with
  | chain path =>
      cases path with
      | refl => exact [([] : List Bool)]
      | snoc path edge => exact []
  | castDepths hn hm tree => exact []
  | trans left right ihLeft ihRight => exact ihLeft ++ ihRight
  | leftContext path later ih =>
      exact ih.map (fun word => false :: word)
  | rightContext earlier path ih =>
      exact ih.map (fun word => true :: word)

/-- Complete, truly typed preservation by EVERY original nine-
constructor F55 3-cell, independent of charge/phase shadow. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p92UnitContextWords_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    r.p92UnitContextWords = s.p92UnitContextWords := by
  induction cell with
  | ident route => rfl
  | pentagon t₁ t₂ t₃ t₄ => rfl
  | disjointSquare left right => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih =>
      change (List.map (fun word : List Bool => false :: word) _) =
        List.map (fun word : List Bool => false :: word) _
      exact congrArg (List.map (fun word : List Bool => false :: word)) ih
  | rightContext earlier cell ih =>
      change (List.map (fun word : List Bool => true :: word) _) =
        List.map (fun word : List Bool => true :: word) _
      exact congrArg (List.map (fun word : List Bool => true :: word)) ih
  | precompose prior cell ih =>
      change prior.p92UnitContextWords ++ _ = prior.p92UnitContextWords ++ _
      exact congrArg (fun words : List (List Bool) =>
        prior.p92UnitContextWords ++ words) ih
  | postcompose cell suffix ih =>
      change _ ++ suffix.p92UnitContextWords = _ ++ suffix.p92UnitContextWords
      exact congrArg (fun words : List (List Bool) =>
        words ++ suffix.p92UnitContextWords) ih

/-- Actual independent original F54 zero-edge rotation chain. -/
def nativeF54P92UnitRoute
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeF45Tree.DepthRotationRoute p tree tree :=
  .chain (.refl tree)

theorem nativeF54P92UnitRoute_words
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (nativeF54P92UnitRoute tree).p92UnitContextWords =
      [([] : List Bool)] := by
  rfl

/-- Exact original left-to-right contexts for three genuine unit
F54 routes under P90B left bracketing, any depths or Blocks. -/
theorem nativeF55P92_unit_assoc_left_words
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (nativeF54P90AssocNaturalityLeftRoute
      (nativeF54P92UnitRoute t₁)
      (nativeF54P92UnitRoute t₂)
      (nativeF54P92UnitRoute t₃)).p92UnitContextWords =
      [[false, false], [false, true], [true]] := by
  rfl

/-- Exact original contexts for the right-associated source route. -/
theorem nativeF55P92_unit_assoc_right_words
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (nativeF54P90AssocNaturalityRightRoute
      (nativeF54P92UnitRoute t₁)
      (nativeF54P92UnitRoute t₂)
      (nativeF54P92UnitRoute t₃)).p92UnitContextWords =
      [[false], [true, false], [true, true]] := by
  rfl

/-- No inhabitant of the ORIGINAL nine-constructor F55
associator-naturality slot for any triple of true native unit routes. -/
theorem nativeF55P92_original_unit_naturality_no_filler
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    ¬ Nonempty
      (NativeF55P90AssocNaturalityCell
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃)) := by
  rintro ⟨cell⟩
  have h := cell.p92UnitContextWords_sound
  rw [nativeF55P92_unit_assoc_left_words,
    nativeF55P92_unit_assoc_right_words] at h
  exact (by decide : ([[false, false], [false, true], [true]] : List (List Bool)) ≠ [[false], [true, false], [true, true]]) h

/-- The particular original-F55 witness route quotient P91B cannot
have strict triple-horizontal associator naturality, EVEN for raw
F54 unit inputs. No general strict 3-category impossibility claim. -/
theorem nativeF55P92_original_unit_triple_classes_ne
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    nativeF55P91TripleLeftClass
      (nativeF55P91FullWitnessRouteClass t₁ t₁ (nativeF54P92UnitRoute t₁))
      (nativeF55P91FullWitnessRouteClass t₂ t₂ (nativeF54P92UnitRoute t₂))
      (nativeF55P91FullWitnessRouteClass t₃ t₃ (nativeF54P92UnitRoute t₃)) ≠
    nativeF55P91TripleRightClass
      (nativeF55P91FullWitnessRouteClass t₁ t₁ (nativeF54P92UnitRoute t₁))
      (nativeF55P91FullWitnessRouteClass t₂ t₂ (nativeF54P92UnitRoute t₂))
      (nativeF55P91FullWitnessRouteClass t₃ t₃ (nativeF54P92UnitRoute t₃)) := by
  intro h
  have hcell := (nativeF55P91TripleClass_eq_iff_original_filler
    (nativeF54P92UnitRoute t₁)
    (nativeF54P92UnitRoute t₂)
    (nativeF54P92UnitRoute t₃)).1 h
  exact (nativeF55P92_original_unit_naturality_no_filler t₁ t₂ t₃) hcell

/-- ACTUAL north C60 pentagon 3-stage dependent F45 source example. -/
theorem northNativeF55P92_original_unit_naturality_no_filler :
    ¬ Nonempty
      (NativeF55P90AssocNaturalityCell
        (nativeF54P92UnitRoute northNativeF45FirstStage)
        (nativeF54P92UnitRoute northNativeF45SecondStage)
        (nativeF54P92UnitRoute northNativeF45ThirdStage)) :=
  nativeF55P92_original_unit_naturality_no_filler
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage

/-- This source obstruction retains the original C60 odd square phase. -/
theorem northHexagonNativeF55P92_odd_square_preserved :
    northHexagonNativeF55SquareCell.nativeShadow.2 ≠
      (0 : ZMod 2) :=
  northHexagonNativeF55SquareCell_phase_nonzero

#print axioms KuuNativeF45Tree.DepthRotationRoute.p92UnitContextWords
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p92UnitContextWords_sound
#print axioms nativeF54P92UnitRoute
#print axioms nativeF54P92UnitRoute_words
#print axioms nativeF55P92_unit_assoc_left_words
#print axioms nativeF55P92_unit_assoc_right_words
#print axioms nativeF55P92_original_unit_naturality_no_filler
#print axioms nativeF55P92_original_unit_triple_classes_ne
#print axioms northNativeF55P92_original_unit_naturality_no_filler
#print axioms northHexagonNativeF55P92_odd_square_preserved

end
end Kuu.F112.Physical
