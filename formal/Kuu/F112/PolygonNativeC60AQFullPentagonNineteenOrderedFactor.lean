import Kuu.F112.PolygonNativeC60AQFullPentagonOrderedDefectFactor

/-!
# F112-P94D3EX — exact original C60 pentagon obstruction as an ordered factor

EW identifies an ACTUAL nonpreserving 19D primitive inside any
hypothetical genuine typed original C60 pentagon filler, retaining
its original complete 18D/17D/16D/15D/14D dependent evidence.

EX additionally computes the entire signed NONCOMMUTATIVE defect
of the provided finite 19D syntax as the genuine original 18D
free-word ratio:
    (original long 18D word)⁻¹ * (original short 18D word).
It is nonidentity by the already proven DS no-go. Moreover, an
occurring original generator, its sign and its exact left/right
ordered group context reconstruct this full defect. This is a
path-local factorization, not a canonical unique position and not
an assertion that the single generator is equal to the whole defect.

The original 19D physical geometric filler remains UNPROVED. Every
statement with a filler is conditional on an explicitly provided
dependent Type-valued path in a proposed signature. No Gray structure,
new group presentation, silent quotient, free/abelian source-kernel
claim or infinite product statement. Preserve strict Kuu, independent
Kuu as a presentation, DS no-go, all original 14D--18D proof
histories, 107 public roots, pinned Lean/mathlib, append-only/same-root.
No new axiom, sorry or admit.
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

section C60FullWordNoncommutativeFactor

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The ordered path defect of any actually supplied 19D pentagon
filler is EXACTLY the ratio of DS's two ORIGINAL full free words.
Neither word is replaced by a scalar or an unrelated target group. -/
theorem nativeC60EXPentagon_defect_eq_full_ratio
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) :
    nativeC60EXFoldDefect T (nativeC60DSNineteenHolonomy S F)
        filler =
      (nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k) := by
  exact nativeC60EXFoldDefect_eq_endpoints
    T (nativeC60DSNineteenHolonomy S F) filler

/-- DS's full original three-versus-two noncommutative difference
makes the entire ordered 19D path defect NONIDENTITY. This is
conditional on the supplied typed filler, never its construction. -/
theorem nativeC60EXPentagon_defect_ne_one
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) :
    nativeC60EXFoldDefect T (nativeC60DSNineteenHolonomy S F)
      filler ≠ 1 := by
  rw [nativeC60EXPentagon_defect_eq_full_ratio S F f g h k T filler]
  exact nativeC60EXAtomicDefect_ne_one
    T (nativeC60DSNineteenHolonomy S F)
    (nativeC60DSPentagon_free_ne S F f g h k)

/-- The particular 19D filler admits a complete ordered
prefix * signed-bad-atom * suffix factorization. The distinguished
atom is certified to actually occur inside the given Type-valued
signed path, with its original dependent endpoints retained. -/
theorem nativeC60EXPentagon_has_ordered_bad_factor
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) :
    NativeC60EXNoncommutativeFactor
      T (nativeC60DSNineteenHolonomy S F) filler :=
  nativeC60EXBadAtom_factor T (nativeC60DSNineteenHolonomy S F)
    (nativeC60EWPentagonFiller_badOnPath S F f g h k T filler)

/-- MAIN EX: exact original C60 noncommutative full free-word
difference equals left-context * (actual signed generator defect)
* right-context, with a genuine path-local occurrence certificate.
No commutative reordering, averaging or abelianization of the
complete original 18D evidence occurs anywhere in this statement. -/
theorem nativeC60EXPentagon_full_ratio_factor
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) :
    ∃ (x y : (nativeC60DSNineteenLayer S F).Total) (atom : T.Gen x y)
      (prefix middle suffix : NativeC60DTFullFree S F),
      NativeC60EWAtomOccursOn T atom filler ∧
      (middle =
          (nativeC60DSNineteenHolonomy S F x)⁻¹ *
            nativeC60DSNineteenHolonomy S F y ∨
       middle =
          ((nativeC60DSNineteenHolonomy S F x)⁻¹ *
            nativeC60DSNineteenHolonomy S F y)⁻¹) ∧
      middle ≠ 1 ∧
      (nativeC60DSFreeWord S F
          (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k) =
          prefix * middle * suffix := by
  obtain ⟨x, y, atom, prefix, middle, suffix, hocc, hsign,
      hnon, heq⟩ :=
    nativeC60EXPentagon_has_ordered_bad_factor
      S F f g h k T filler
  refine ⟨x, y, atom, prefix, middle, suffix,
    hocc, hsign, hnon, ?_⟩
  rw [← nativeC60EXPentagon_defect_eq_full_ratio S F f g h k T filler]
  exact heq

end C60FullWordNoncommutativeFactor

#print axioms nativeC60EXPentagon_defect_eq_full_ratio
#print axioms nativeC60EXPentagon_defect_ne_one
#print axioms nativeC60EXPentagon_has_ordered_bad_factor
#print axioms nativeC60EXPentagon_full_ratio_factor

end
end Kuu.F112.Physical
