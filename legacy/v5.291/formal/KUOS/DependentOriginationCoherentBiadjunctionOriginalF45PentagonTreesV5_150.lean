import KUOS.DependentOriginationCoherentBiadjunctionFourfoldPentagonV5_150
import KUOS.DependentOriginationCoherentBiadjunctionBracketTreeRegroupingV5_149

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F53-B / v5.150 — the ACTUAL five old F45 binary trees of a pentagon

F53-A proves a FIVE-VERTEX, FIVE-EDGE genuine associativity pentagon
in the original F44 quotient. Here each of the four inputs is not a
synthetic category arrow: it is a genuine F52 Type-valued binary
tree with an ARBITRARY finite number of ORIGINAL F45 leaves, exact
F19/F28 primitive step counts, typed intermediate Blocks and
original F45 execution-order choices.

All FIVE separately parenthesized actual trees are constructed and
their interpretations identified with F53-A's five typed classes.
The THREE-edge and TWO-edge routes coincide after the exact
independent natural-number casts, and each projected source/target
Type-valued original axis history is invariant at the endpoint.

This is generated exchange-quotient coherence, not a free higher
3-cell or an identification of otherwise distinct original
same-axis primitive operations.
-/

universe uD vD uE vE uD' vD' uE' vE'
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section FourOriginalTrees

variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)

/-- ACTUAL original-F45 tree pentagon vertex 0. -/
def OriginalF45BracketTree.pentagon0 :
    OriginalF45BracketTree (((n₁ + n₂) + n₃) + n₄) (((m₁ + m₂) + m₃) + m₄)
      p₀ q₀ p₄ q₄ :=
  OriginalF45BracketTree.node
    (OriginalF45BracketTree.node (OriginalF45BracketTree.node t₁ t₂) t₃) t₄

/-- The genuine F44 quotient interpretation of vertex 0 is
exactly the corresponding original F53 five-vertex composition. -/
theorem OriginalF45BracketTree.pentagon0_toClass :
    (OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄).toExchangeClass =
      ExchangeClass.pentagon0
        t₁.toExchangeClass t₂.toExchangeClass
        t₃.toExchangeClass t₄.toExchangeClass :=
  rfl

/-- ACTUAL original-F45 tree pentagon vertex 1. -/
def OriginalF45BracketTree.pentagon1 :
    OriginalF45BracketTree ((n₁ + (n₂ + n₃)) + n₄) ((m₁ + (m₂ + m₃)) + m₄)
      p₀ q₀ p₄ q₄ :=
  OriginalF45BracketTree.node
    (OriginalF45BracketTree.node t₁ (OriginalF45BracketTree.node t₂ t₃)) t₄

/-- The genuine F44 quotient interpretation of vertex 1 is
exactly the corresponding original F53 five-vertex composition. -/
theorem OriginalF45BracketTree.pentagon1_toClass :
    (OriginalF45BracketTree.pentagon1 t₁ t₂ t₃ t₄).toExchangeClass =
      ExchangeClass.pentagon1
        t₁.toExchangeClass t₂.toExchangeClass
        t₃.toExchangeClass t₄.toExchangeClass :=
  rfl

/-- ACTUAL original-F45 tree pentagon vertex 2. -/
def OriginalF45BracketTree.pentagon2 :
    OriginalF45BracketTree (n₁ + ((n₂ + n₃) + n₄)) (m₁ + ((m₂ + m₃) + m₄))
      p₀ q₀ p₄ q₄ :=
  OriginalF45BracketTree.node t₁
    (OriginalF45BracketTree.node (OriginalF45BracketTree.node t₂ t₃) t₄)

/-- The genuine F44 quotient interpretation of vertex 2 is
exactly the corresponding original F53 five-vertex composition. -/
theorem OriginalF45BracketTree.pentagon2_toClass :
    (OriginalF45BracketTree.pentagon2 t₁ t₂ t₃ t₄).toExchangeClass =
      ExchangeClass.pentagon2
        t₁.toExchangeClass t₂.toExchangeClass
        t₃.toExchangeClass t₄.toExchangeClass :=
  rfl

/-- ACTUAL original-F45 tree pentagon vertex 3. -/
def OriginalF45BracketTree.pentagon3 :
    OriginalF45BracketTree (n₁ + (n₂ + (n₃ + n₄))) (m₁ + (m₂ + (m₃ + m₄)))
      p₀ q₀ p₄ q₄ :=
  OriginalF45BracketTree.node t₁
    (OriginalF45BracketTree.node t₂ (OriginalF45BracketTree.node t₃ t₄))

/-- The genuine F44 quotient interpretation of vertex 3 is
exactly the corresponding original F53 five-vertex composition. -/
theorem OriginalF45BracketTree.pentagon3_toClass :
    (OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass =
      ExchangeClass.pentagon3
        t₁.toExchangeClass t₂.toExchangeClass
        t₃.toExchangeClass t₄.toExchangeClass :=
  rfl

/-- ACTUAL original-F45 tree pentagon vertex 4. -/
def OriginalF45BracketTree.pentagon4 :
    OriginalF45BracketTree ((n₁ + n₂) + (n₃ + n₄)) ((m₁ + m₂) + (m₃ + m₄))
      p₀ q₀ p₄ q₄ :=
  OriginalF45BracketTree.node
    (OriginalF45BracketTree.node t₁ t₂) (OriginalF45BracketTree.node t₃ t₄)

/-- The genuine F44 quotient interpretation of vertex 4 is
exactly the corresponding original F53 five-vertex composition. -/
theorem OriginalF45BracketTree.pentagon4_toClass :
    (OriginalF45BracketTree.pentagon4 t₁ t₂ t₃ t₄).toExchangeClass =
      ExchangeClass.pentagon4
        t₁.toExchangeClass t₂.toExchangeClass
        t₃.toExchangeClass t₄.toExchangeClass :=
  rfl

/-- The actual FOUR-subtree original-F45 LONG pentagon route:
three genuine typed associators in the original F44 quotient
connect the left-deep tree to the right-deep tree. -/
theorem OriginalF45BracketTree.pentagonLong :
    (OriginalF45BracketTree.castDepths
      (F53Depth.long n₁ n₂ n₃ n₄)
      (F53Depth.long m₁ m₂ m₃ m₄)
      (OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)).toExchangeClass =
    (OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass := by
  calc
    _ = ExchangeClass.castDepths
        (F53Depth.long n₁ n₂ n₃ n₄)
        (F53Depth.long m₁ m₂ m₃ m₄)
        (ExchangeClass.pentagon0
          t₁.toExchangeClass t₂.toExchangeClass
          t₃.toExchangeClass t₄.toExchangeClass) := by
          rw [OriginalF45BracketTree.castDepths_toExchangeClass,
            OriginalF45BracketTree.pentagon0_toClass]
    _ = ExchangeClass.pentagon3
          t₁.toExchangeClass t₂.toExchangeClass
          t₃.toExchangeClass t₄.toExchangeClass :=
      ExchangeClass.pentagonLong _ _ _ _
    _ = _ := (OriginalF45BracketTree.pentagon3_toClass t₁ t₂ t₃ t₄).symm

/-- The actual FOUR-subtree original-F45 SHORT pentagon route:
two genuine F44 associators have the very same right-deep endpoint. -/
theorem OriginalF45BracketTree.pentagonShort :
    (OriginalF45BracketTree.castDepths
      (F53Depth.short n₁ n₂ n₃ n₄)
      (F53Depth.short m₁ m₂ m₃ m₄)
      (OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)).toExchangeClass =
    (OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass := by
  calc
    _ = ExchangeClass.castDepths
        (F53Depth.short n₁ n₂ n₃ n₄)
        (F53Depth.short m₁ m₂ m₃ m₄)
        (ExchangeClass.pentagon0
          t₁.toExchangeClass t₂.toExchangeClass
          t₃.toExchangeClass t₄.toExchangeClass) := by
          rw [OriginalF45BracketTree.castDepths_toExchangeClass,
            OriginalF45BracketTree.pentagon0_toClass]
    _ = ExchangeClass.pentagon3
          t₁.toExchangeClass t₂.toExchangeClass
          t₃.toExchangeClass t₄.toExchangeClass :=
      ExchangeClass.pentagonShort _ _ _ _
    _ = _ := (OriginalF45BracketTree.pentagon3_toClass t₁ t₂ t₃ t₄).symm

/-- The LONG route also preserves the COMPLETE two original
proof-relevant F19/F28 primitive-step histories on the nose,
with both genuinely necessary natural-number reindexing casts. -/
theorem OriginalF45BracketTree.pentagonLong_axisHistories :
    (OriginalF45BracketTree.castDepths
      (F53Depth.long n₁ n₂ n₃ n₄)
      (F53Depth.long m₁ m₂ m₃ m₄)
      (OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)).axisHistories =
    (OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).axisHistories := by
  have heq := OriginalF45BracketTree.pentagonLong t₁ t₂ t₃ t₄
  have hh := congrArg ExchangeClass.axisTraces heq
  simpa only [OriginalF45BracketTree.toExchangeClass_axisTraces] using hh

/-- The short route preserves the same two complete original
within-axis primitive histories, independently of parentheses. -/
theorem OriginalF45BracketTree.pentagonShort_axisHistories :
    (OriginalF45BracketTree.castDepths
      (F53Depth.short n₁ n₂ n₃ n₄)
      (F53Depth.short m₁ m₂ m₃ m₄)
      (OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄)).axisHistories =
    (OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).axisHistories := by
  have heq := OriginalF45BracketTree.pentagonShort t₁ t₂ t₃ t₄
  have hh := congrArg ExchangeClass.axisTraces heq
  simpa only [OriginalF45BracketTree.toExchangeClass_axisTraces] using hh

end FourOriginalTrees

/-!
The FUNCTORIAL extension: a genuine functor on either original axis
commutes with all native dependent two-depth index casts; therefore
transporting an F53 pentagon by two unrelated honest functors still
satisfies the same long and short original F44 quotient equations.
-/

/-- All genuinely typed F19/F28 depth casts commute exactly with
two unrelated honest original-category functors. -/
theorem ExchangeClass.mapBoth_castDepths
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hn : n = n') (hm : m = m')
    (h : ExchangeClass n m ma mb pa pb) :
    ExchangeClass.mapBoth H K (ExchangeClass.castDepths hn hm h) =
      ExchangeClass.castDepths hn hm (ExchangeClass.mapBoth H K h) := by
  cases hn
  cases hm
  rfl

/-- The entire ORIGINAL F53 long pentagon proof survives genuine
functorial transport on BOTH independently typed axes. -/
theorem ExchangeClass.mapBoth_pentagonLong
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
    (h₁ : ExchangeClass n₁ m₁ p₀ p₁ q₀ q₁)
    (h₂ : ExchangeClass n₂ m₂ p₁ p₂ q₁ q₂)
    (h₃ : ExchangeClass n₃ m₃ p₂ p₃ q₂ q₃)
    (h₄ : ExchangeClass n₄ m₄ p₃ p₄ q₃ q₄) :
    ExchangeClass.castDepths
      (F53Depth.long n₁ n₂ n₃ n₄)
      (F53Depth.long m₁ m₂ m₃ m₄)
      (ExchangeClass.mapBoth H K (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄)) =
    ExchangeClass.mapBoth H K (ExchangeClass.pentagon3 h₁ h₂ h₃ h₄) := by
  calc
    _ = ExchangeClass.mapBoth H K
      (ExchangeClass.castDepths
        (F53Depth.long n₁ n₂ n₃ n₄)
        (F53Depth.long m₁ m₂ m₃ m₄)
        (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄)) :=
      (ExchangeClass.mapBoth_castDepths H K _ _ _).symm
    _ = _ := congrArg (ExchangeClass.mapBoth H K)
      (ExchangeClass.pentagonLong h₁ h₂ h₃ h₄)

/-- The entire ORIGINAL F53 short pentagon proof survives genuine
functorial transport on BOTH independently typed axes. -/
theorem ExchangeClass.mapBoth_pentagonShort
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
    (h₁ : ExchangeClass n₁ m₁ p₀ p₁ q₀ q₁)
    (h₂ : ExchangeClass n₂ m₂ p₁ p₂ q₁ q₂)
    (h₃ : ExchangeClass n₃ m₃ p₂ p₃ q₂ q₃)
    (h₄ : ExchangeClass n₄ m₄ p₃ p₄ q₃ q₄) :
    ExchangeClass.castDepths
      (F53Depth.short n₁ n₂ n₃ n₄)
      (F53Depth.short m₁ m₂ m₃ m₄)
      (ExchangeClass.mapBoth H K (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄)) =
    ExchangeClass.mapBoth H K (ExchangeClass.pentagon3 h₁ h₂ h₃ h₄) := by
  calc
    _ = ExchangeClass.mapBoth H K
      (ExchangeClass.castDepths
        (F53Depth.short n₁ n₂ n₃ n₄)
        (F53Depth.short m₁ m₂ m₃ m₄)
        (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄)) :=
      (ExchangeClass.mapBoth_castDepths H K _ _ _).symm
    _ = _ := congrArg (ExchangeClass.mapBoth H K)
      (ExchangeClass.pentagonShort h₁ h₂ h₃ h₄)

#print axioms OriginalF45BracketTree.pentagon0
#print axioms OriginalF45BracketTree.pentagon1
#print axioms OriginalF45BracketTree.pentagon2
#print axioms OriginalF45BracketTree.pentagon3
#print axioms OriginalF45BracketTree.pentagon4
#print axioms OriginalF45BracketTree.pentagon0_toClass
#print axioms OriginalF45BracketTree.pentagon1_toClass
#print axioms OriginalF45BracketTree.pentagon2_toClass
#print axioms OriginalF45BracketTree.pentagon3_toClass
#print axioms OriginalF45BracketTree.pentagon4_toClass
#print axioms OriginalF45BracketTree.pentagonLong
#print axioms OriginalF45BracketTree.pentagonShort
#print axioms OriginalF45BracketTree.pentagonLong_axisHistories
#print axioms OriginalF45BracketTree.pentagonShort_axisHistories
#print axioms ExchangeClass.mapBoth_castDepths
#print axioms ExchangeClass.mapBoth_pentagonLong
#print axioms ExchangeClass.mapBoth_pentagonShort

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
