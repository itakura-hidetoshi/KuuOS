import Kuu.F112.PolygonNativeC60AQFullPentagonPathLocalObstruction

/-!
# F112-P94D3EW — exact path-local C60 pentagon full-evidence obstruction

DS constructed the ORIGINAL noncommutative FreeGroup word of every
complete original 18D Type-valued generator (including its dependent
17D/16D/15D/14D evidence), and proved that the long and short typed
pentagon routes have DIFFERENT full free words, for any original
four composable raw17D witnesses. EW puts that obstruction INSIDE
the particular candidate 19D filler path, not merely somewhere in
an unbounded optional signature.

For any ACTUALLY PROVIDED 19D filler p:
1. A specific atom of p (possibly occurring beneath symm/trans)
   fails to preserve the complete original 18D free receiver.
2. The dependent endpoints, concrete primitive g, and its typed
   occurrence INSIDE p are retained in a proof certificate.
3. It is impossible for all original generators USED BY p to
   preserve full free evidence.
4. Independent genuine C60 AQ finite local repartitioning, while
   semantically coherent, does not erase the above path-local gate.

This is a conditional obstruction theorem, never an assertion that
an original geometric 19D filler exists. The 19D signature is explicit
arbitrary INPUT, not a new signature or logical axiom. No new quotient
of original Type-valued evidence and no Gray reconstruction. Retain
strict Kuu, independent Kuu presentation, DS no-go, 107 public roots,
pinned Lean/mathlib, append-only/same-root. No sorry or admit.
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

section ActualC60EighteenToNineteen

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A GIVEN candidate 19D pentagon filler contains an atom which
fails to preserve the exact original noncommutative 18D free word.
This certificate is *internal to that precise filler path*. -/
theorem nativeC60EWPentagonFiller_badOnPath
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) :
    NativeC60EWBadAtomOn T (nativeC60DSNineteenHolonomy S F) filler := by
  apply nativeC60EWBadOnPath_of_endpoint_ne
  exact nativeC60DSPentagon_free_ne S F f g h k

/-- STRONGER THAN EV: the violating generator is guaranteed to
OCCUR in the actual filler. Existence somewhere in the optional
signature would be insufficient for local obstruction analysis. -/
theorem nativeC60EWPentagonFiller_exact_bad_atom
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) :
    ∃ (x y : (nativeC60DSNineteenLayer S F).Total) (atom : T.Gen x y),
      NativeC60EWAtomOccursOn T atom filler ∧
      nativeC60DSNineteenHolonomy S F x ≠
        nativeC60DSNineteenHolonomy S F y :=
  nativeC60EWBadOnPath_exact_atom T (nativeC60DSNineteenHolonomy S F)
    (nativeC60EWPentagonFiller_badOnPath S F f g h k T filler)

/-- No actual 19D filler can be composed solely from generators
preserving the full ORIGINAL 18D evidence. This test concerns only
atoms of the GIVEN finite signed path; unrelated primitives of T
do not enter the condition. -/
theorem nativeC60EWPentagonFiller_not_all_used_good
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) :
    ¬ (∀ (x y : (nativeC60DSNineteenLayer S F).Total)
        (atom : T.Gen x y),
          NativeC60EWAtomOccursOn T atom filler →
            nativeC60DSNineteenHolonomy S F x =
              nativeC60DSNineteenHolonomy S F y) := by
  intro allgood
  obtain ⟨x, y, atom, hOccurs, hbad⟩ :=
    nativeC60EWPentagonFiller_exact_bad_atom S F f g h k T filler
  exact hbad (allgood x y atom hOccurs)

/-- Actual original finite C60 AQ LOCAL rebracketings remain
semantically coherent, while the particular 19D filler (IF
PROVIDED) must contain a nonpreserving original 18D generator.
These are compatible but separate conclusions, not an inference
from AQ equality to a missing 19D Type-valued cell. -/
theorem nativeC60EWLocalAQ_with_pathSpecificEvidenceGate
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
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) :
    (∃ q : NativeC60ETLocalPath xs ys,
      nativeC60ETLocalPathEquiv S F word start q =
        nativeC60ESPathEquiv S F word start p) ∧
    (∃ (x y : (nativeC60DSNineteenLayer S F).Total) (atom : T.Gen x y),
      NativeC60EWAtomOccursOn T atom filler ∧
      nativeC60DSNineteenHolonomy S F x ≠
        nativeC60DSNineteenHolonomy S F y) :=
  ⟨nativeC60EUGlobalPath_hasLocalRealization S F word r start p,
    nativeC60EWPentagonFiller_exact_bad_atom S F f g h k T filler⟩

end ActualC60EighteenToNineteen

#print axioms nativeC60EWPentagonFiller_badOnPath
#print axioms nativeC60EWPentagonFiller_exact_bad_atom
#print axioms nativeC60EWPentagonFiller_not_all_used_good
#print axioms nativeC60EWLocalAQ_with_pathSpecificEvidenceGate

end
end Kuu.F112.Physical
