import Kuu.F112.PolygonNativeF55P94DK5TypedFiveCellInterchanger
import Mathlib.Tactic

/-!
# F112-P94D3Y — two quotient horizontal composites, five-cell naturality

The genuinely Type-valued five-cell grammar of P94D3Y includes
exactly-typed 4-cell congruence and 3-cell whiskering. Use these
actual evidence terms to show BOTH D3X horizontal composites
respect independent five-cell transformations in either argument.
Consequently both operations descend to proof-relevant 5-cell
quotient classes. The freely adjoined interchanger gives a
provable equality of the two operations ON THAT NEW QUOTIENT.

An explicit five-stage native K5 independent pentagonator enters
the source of the new 5-cell interchanger. The full noncommutative
Peiffer relation still obeys its exact original horizontal law.

No equality of raw 4-cell terms, no old P92B descent, no original
strictification, no Gray and no 6-cell/pentagon identity is asserted.
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

section HorizontalFiveNaturality

variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {h k : NativeF55StructuralComparison p s t}

/-- Source-typed FIVE-dimensional left naturality for the
target-whiskered horizontal 4-cell composite. -/
def NativeK5StructuralFiveCell.horizontalViaTarget_left
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (beta : NativeK5StructuralFourCell p h k) :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaTarget beta)
      (alpha'.horizontalViaTarget beta) :=
  .verticalLeft (.postcompose w h) (.precompose g beta)

/-- FIVE-dimensional right naturality for target-whiskered
horizontal 4-cell pasting; no boundary group equality is used
to manufacture the evidence. -/
def NativeK5StructuralFiveCell.horizontalViaTarget_right
    (alpha : NativeK5StructuralFourCell p f g)
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p beta beta') :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaTarget beta)
      (alpha.horizontalViaTarget beta') :=
  .verticalRight (.postcompose alpha h) (.precompose g w)

/-- Source-typed left naturality for the alternative source-
whiskered four-cell composite, with its EXACT order. -/
def NativeK5StructuralFiveCell.horizontalViaSource_left
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (beta : NativeK5StructuralFourCell p h k) :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaSource beta)
      (alpha'.horizontalViaSource beta) :=
  .verticalRight (.precompose f beta) (.postcompose w k)

/-- Source-typed right naturality for the source-whiskered
horizontal four-cell composite. -/
def NativeK5StructuralFiveCell.horizontalViaSource_right
    (alpha : NativeK5StructuralFourCell p f g)
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p beta beta') :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaSource beta)
      (alpha.horizontalViaSource beta') :=
  .verticalLeft (.precompose f w) (.postcompose alpha k)

/-- ACTUAL 5-cell congruence makes target-whiskered 4-cell
horizontal composition well-defined on two independent 5-cell
quotient classes. This is not just Peiffer image equality. -/
def nativeK5FiveCellHorizontalViaTarget
    (alpha : NativeK5FiveCellFourClasses f g)
    (beta : NativeK5FiveCellFourClasses h k) :
    NativeK5FiveCellFourClasses (.trans f h) (.trans g k) :=
  Quot.liftOn₂ alpha beta
    (fun a b => nativeK5FiveCellFourClass (a.horizontalViaTarget b))
    (by
      intro a b b' hb
      rcases hb with ⟨w⟩
      exact Quot.sound
        ⟨NativeK5StructuralFiveCell.horizontalViaTarget_right a w⟩)
    (by
      intro a a' b ha
      rcases ha with ⟨w⟩
      exact Quot.sound
        ⟨NativeK5StructuralFiveCell.horizontalViaTarget_left w b⟩)

/-- The alternative source-whiskered horizontal composite ALSO
descends through independently typed five-cell evidence. -/
def nativeK5FiveCellHorizontalViaSource
    (alpha : NativeK5FiveCellFourClasses f g)
    (beta : NativeK5FiveCellFourClasses h k) :
    NativeK5FiveCellFourClasses (.trans f h) (.trans g k) :=
  Quot.liftOn₂ alpha beta
    (fun a b => nativeK5FiveCellFourClass (a.horizontalViaSource b))
    (by
      intro a b b' hb
      rcases hb with ⟨w⟩
      exact Quot.sound
        ⟨NativeK5StructuralFiveCell.horizontalViaSource_right a w⟩)
    (by
      intro a a' b ha
      rcases ha with ⟨w⟩
      exact Quot.sound
        ⟨NativeK5StructuralFiveCell.horizontalViaSource_left w b⟩)

/-- The two genuine horizontal constructions coincide ON THE NEW
source-evidence 5-cell QUOTIENT, by exactly the chosen interchanger
generator. This is NOT an equality of their raw Type-valued terms. -/
theorem nativeK5FiveCellHorizontal_interchange
    (alpha : NativeK5FiveCellFourClasses f g)
    (beta : NativeK5FiveCellFourClasses h k) :
    nativeK5FiveCellHorizontalViaTarget alpha beta =
      nativeK5FiveCellHorizontalViaSource alpha beta := by
  refine Quot.inductionOn alpha (fun a => ?_)
  refine Quot.inductionOn beta (fun b => ?_)
  change nativeK5FiveCellFourClass (a.horizontalViaTarget b) =
    nativeK5FiveCellFourClass (a.horizontalViaSource b)
  exact Quot.sound ⟨nativeK5TypedInterchanger a b⟩

/-- The quotient horizontal composite still obeys the full
noncommutative Peiffer action by the right 3-cell boundary. -/
theorem nativeK5FiveCellHorizontal_peiffer
    (alpha : NativeK5FiveCellFourClasses f g)
    (beta : NativeK5FiveCellFourClasses h k) :
    nativeK5FiveCellFourToPeiffer
        (nativeK5FiveCellHorizontalViaTarget alpha beta) =
      nativeK5FiveCellFourToPeiffer alpha +
        nativeK5UniversalPeifferAct g.p94cGroupWord
          (nativeK5FiveCellFourToPeiffer beta) := by
  refine Quot.inductionOn alpha (fun a => ?_)
  refine Quot.inductionOn beta (fun b => ?_)
  exact a.horizontalViaTarget_relator b

end HorizontalFiveNaturality

section OriginalPentagonator

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

/-- A FIVE-CELL WITH REAL K5 SOURCE: one genuine independent
nine-face pentagonator plus an arbitrary adjacent genuinely typed
four-cell. Exists IN THE NEW PRESENTATION via its explicit,
independent interchanger constructor, NOT in the older grammar. -/
def nativeK5PentagonatorTypedFiveInterchanger
    {h k : NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)}
    (beta : NativeK5StructuralFourCell p h k) :
    NativeK5StructuralFiveCell p
      ((nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5).horizontalViaTarget beta)
      ((nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5).horizontalViaSource beta) :=
  nativeK5TypedInterchanger
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5) beta

/-- Two independent typed pentagonators provide a concrete
higher interchanger instance at the genuine five-stage F45 route. -/
def nativeK5PentagonatorSelfTypedFiveInterchanger :
    NativeK5StructuralFiveCell p
      ((nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5).horizontalViaTarget
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5))
      ((nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5).horizontalViaSource
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)) :=
  nativeK5PentagonatorTypedFiveInterchanger t1 t2 t3 t4 t5
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)

/-- This new higher K5 interchanger enforces quotient equality
between the two 4-cell compositions. The P94D3U mod-three
obstruction and old word-faithful non-descent are unchanged. -/
theorem nativeK5PentagonatorSelf_fiveQuotientCoherence :
    nativeK5FiveCellFourClass
      ((nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5).horizontalViaTarget
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)) =
    nativeK5FiveCellFourClass
      ((nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5).horizontalViaSource
        (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5)) :=
  Quot.sound ⟨nativeK5PentagonatorSelfTypedFiveInterchanger t1 t2 t3 t4 t5⟩

end OriginalPentagonator

#print axioms NativeK5StructuralFiveCell.horizontalViaTarget_left
#print axioms NativeK5StructuralFiveCell.horizontalViaTarget_right
#print axioms NativeK5StructuralFiveCell.horizontalViaSource_left
#print axioms NativeK5StructuralFiveCell.horizontalViaSource_right
#print axioms nativeK5FiveCellHorizontalViaTarget
#print axioms nativeK5FiveCellHorizontalViaSource
#print axioms nativeK5FiveCellHorizontal_interchange
#print axioms nativeK5FiveCellHorizontal_peiffer
#print axioms nativeK5PentagonatorTypedFiveInterchanger
#print axioms nativeK5PentagonatorSelfTypedFiveInterchanger
#print axioms nativeK5PentagonatorSelf_fiveQuotientCoherence

end
end Kuu.F112.Physical
