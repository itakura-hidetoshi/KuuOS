import Kuu.F112.PolygonNativeC60AQFullPentagonLocalActionFibers
import Kuu.F112.PolygonNativeC60EighteenFullWordNineteenObstruction

/-!
# F112-P94D3EV — exact higher evidence obstruction beyond local AQ coherence

EU proved stepwise local generation of EVERY ES finite AQ repartition path,
including full genuine integer and residual-kernel action equality.
EV proves that this action is not faithful on the underlying
Type-valued local history. DS independently proved the ORIGINAL full
noncommutative 18D pentagon free words are unequal and a candidate
19D signature preserving ALL complete 18D words cannot fill the
pentagon between their actual dependent source/target witnesses.

This file connects the two compatible facts without conflating them:
* Any proposed genuinely typed 19D filler forces a specific primitive
  19D generator to change the ORIGINAL full 18D free holonomy, not
  merely an abstract loss-of-faithfulness assertion.
* Every global ES path still has its constructive local AQ realization
  while a full-evidence-compatible 19D pentagon filler is prohibited.
* Even if the local path action is independent of rebracketing,
  no original 19D geometric cell is inferred.

The candidate 19D signature is universally quantified, NOT created
as a new cell. Distinct original 14D--18D Type-valued evidence, strict
Kuu, independent Kuu as one presentation, DS no-go and all 107 public
roots remain intact. No Gray category, infinite rank/product result,
source-kernel commutativity/free abelianity, new axiom, sorry or admit.
Pinned Lean/mathlib; append-only/same-root.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

section GenuineC60AQTowerAndEvidence

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- If any candidate Type-valued 19D signature actually fills
the original pentagon, there exists a SPECIFIC original
primitive 19D generator which violates full signed noncommutative
18D holonomy preservation. This locates the obstruction at an
actual generator rather than postulating a missing filler. -/
theorem nativeC60EVFiller_has_nonpreserving_generator
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonShort S F f g h k))) :
    ∃ (x y : (nativeC60DSNineteenLayer S F).Total)
      (atom : T.Gen x y),
      nativeC60DSNineteenHolonomy S F x ≠
        nativeC60DSNineteenHolonomy S F y := by
  classical
  by_contra hnot
  have hc : NativeC60DSNineteenCompatible S F T := by
    intro x y atom
    by_contra hneq
    apply hnot
    exact ⟨x, y, atom, hneq⟩
  exact (nativeC60DSAnyNineteenFiller_forces_BV_loss
    S F f g h k T filler) hc

/-- An actual ES path can ALWAYS be localized as genuine ET
adjacent/zero moves, but this does not supply a compatible 19D
filler on the ORIGINAL full 18D evidence. The two facts are
proved together at the SAME C60 AQ signature and finite context. -/
theorem nativeC60EVLocalCoherence_with_fullEvidence_noGo
    (word : List Bool) (start : ℕ)
    {v w : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen v w)
    {xs ys : List ℕ} (p : NativeC60ESPartitionPath xs ys)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (hc : NativeC60DSNineteenCompatible S F T) :
    (∃ q : NativeC60ETLocalPath xs ys,
      nativeC60ETLocalPathEquiv S F word start q =
        nativeC60ESPathEquiv S F word start p) ∧
    ¬ Nonempty (NativeC60AXStep T
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonShort S F f g h k))) :=
  ⟨nativeC60EUGlobalPath_hasLocalRealization S F word r start p,
    nativeC60DSNoCompatibleNineteenPentagonFiller
      S F f g h k T hc⟩

/-- Explicitly test the boundary even when two genuinely local
C60 AQ paths have EQUAL actions. A hypothetical selected 19D
filler, if it exists at all, must contain a generator violating
the independently retained full 18D noncommutative evidence. -/
theorem nativeC60EVLocalEquality_and_filler_loss
    (word : List Bool) (start : ℕ)
    {v w : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen v w)
    {xs ys : List ℕ} (p q : NativeC60ETLocalPath xs ys)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonShort S F f g h k))) :
    nativeC60EVLocalActionEq S F word start p q ∧
    ∃ (x y : (nativeC60DSNineteenLayer S F).Total)
      (atom : T.Gen x y),
      nativeC60DSNineteenHolonomy S F x ≠
        nativeC60DSNineteenHolonomy S F y :=
  ⟨nativeC60EVLocalActionEq_all_parallel S F word r start p q,
    nativeC60EVFiller_has_nonpreserving_generator S F f g h k T filler⟩

end GenuineC60AQTowerAndEvidence

#print axioms nativeC60EVFiller_has_nonpreserving_generator
#print axioms nativeC60EVLocalCoherence_with_fullEvidence_noGo
#print axioms nativeC60EVLocalEquality_and_filler_loss

end
end Kuu.F112.Physical
