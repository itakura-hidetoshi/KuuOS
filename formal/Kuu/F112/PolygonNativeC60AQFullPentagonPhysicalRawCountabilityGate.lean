import Mathlib.Tactic.DeriveCountable
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalSourceCardinality

/-!
# F112-P94D3FZ — proof-relevant source countability from actual
# dependent raw17D and recursive assoc/post/pre constructor syntax

The historical FY result requires original 18D source Countable
to conclude exact aleph-null normal rank. This module works toward
an explicit, type-preserving smallness gate from the actual lower
dependent evidence, not just the finite geometric size of C60.

Retain raw original 14D-17D proof witnesses and signed noncommutative
FreeGroup source. No new axioms, sorry/admit, Gray, universal 19D filler,
or unconditional countability claims. Pinned Lean/mathlib and 107
published roots remain invariant.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory Cardinal
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/- Derive countability from the ACTUAL indexed free path constructors
atom/refl/symm/trans. This is an additive instance for previously
defined raw syntax; the original inductive is not replaced. -/
deriving instance Countable for NativeC60AXStep

/- Derive countability for the ACTUAL indexed recursive 18D
assoc/post/pre construction, retaining every dependent path argument. -/
deriving instance Countable for NativeC60DREighteenAssocGen

section TypedCountabilityPropagation

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The true raw17D step TOTAL is countable once its original
dependent 17D endpoint codes and each corresponding exact step
fiber are countable, without truncating raw proof data. -/
theorem nativeC60FZRawSeventeenTotal_countable
    (hobjects : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hpaths : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
      Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)) :
    Countable (Σ a : (nativeC60DQSeventeenLayer S F).Total,
      Σ b : (nativeC60DQSeventeenLayer S F).Total,
        NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) := by
  letI : Countable (nativeC60DQSeventeenLayer S F).Total := hobjects
  letI : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
      Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) :=
    hpaths
  infer_instance

/-- Actual 18D layer objects are dependent raw17D paths, not a
numeric C60-vertex code or a quotient. -/
theorem nativeC60FZEighteenObject_countable_of_rawSeventeen
    (hobjects : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hpaths : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
      Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)) :
    Countable (nativeC60DREighteenLayer S F).Total := by
  have htotal := nativeC60FZRawSeventeenTotal_countable S F hobjects hpaths
  letI : Countable (nativeC60DQSeventeenLayer S F).Total := hobjects
  letI : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
    Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) :=
    hpaths
  change Countable
    (Σ endpoints : ((nativeC60DQSeventeenLayer S F).Total ×
      (nativeC60DQSeventeenLayer S F).Total),
      NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F)
        endpoints.1 endpoints.2)
  infer_instance

/-- Precise sufficient gate for the full original proof-relevant
18D alphabet: Countable endpoints and Countable indexed actual
assoc/post/pre generator fibers. It is NOT an assumption that the
finite C60 geometry makes arbitrary input Hom types countable. -/
theorem nativeC60FZFullOriginalEighteen_countable_of_countable_fibers
    (hobjects : Countable (nativeC60DREighteenLayer S F).Total)
    (hgen : ∀ x y : (nativeC60DREighteenLayer S F).Total,
      Countable ((nativeC60DREighteenAssocSignature S F).Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode S F) := by
  letI : Countable (nativeC60DREighteenLayer S F).Total := hobjects
  letI : ∀ x y : (nativeC60DREighteenLayer S F).Total,
    Countable ((nativeC60DREighteenAssocSignature S F).Gen x y) := hgen
  exact inferInstance

/-- Compose the exact 17D raw proof family gate with the 18D
recursive generator-family gate, without hiding either premise. -/
theorem nativeC60FZFullOriginalEighteen_countable_of_rawAndGen
    (hobjects : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hpaths : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
      Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b))
    (hgen : ∀ x y : (nativeC60DREighteenLayer S F).Total,
      Countable ((nativeC60DREighteenAssocSignature S F).Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode S F) :=
  nativeC60FZFullOriginalEighteen_countable_of_countable_fibers S F
    (nativeC60FZEighteenObject_countable_of_rawSeventeen S F hobjects hpaths)
    hgen

end TypedCountabilityPropagation

#print axioms nativeC60FZRawSeventeenTotal_countable
#print axioms nativeC60FZEighteenObject_countable_of_rawSeventeen
#print axioms nativeC60FZFullOriginalEighteen_countable_of_countable_fibers
#print axioms nativeC60FZFullOriginalEighteen_countable_of_rawAndGen

end
end Kuu.F112.Physical
