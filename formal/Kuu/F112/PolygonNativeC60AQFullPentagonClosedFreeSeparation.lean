import Kuu.F112.PolygonNativeC60AQFullPentagonActualContextAtomGate

/-!
# F112-P94D3FB — full target closed 18D noncommutative pentagon separation

DX constructed an ACTUAL context-closed 17D grammar with its own
dependent 18D associator / left- and right-whiskering generators and
the FULL noncommutative free group of those generator codes. Previous
DX/FA quotient theorems identify the pentagon long and short words
ONLY in an explicitly selected relative quotient.

FB now proves they are UNEQUAL in that original unquotiented
context-closed free evidence group for EVERY genuinely typed closed
17D four-path input. The long route has three positive COMPLETE
18D codes and the short route has two. DS's generic reduced positive
word uniqueness applies without any distinct-letter assumption.
Nothing is reduced to a scalar word-length observer: the group is
still the universal FreeGroup of the entire dependent generator
alphabet, and the five raw typed codes remain visibly present.

The all-closed-pentagon normal kernel is nontrivial for EVERY supplied
four-path input, and the exact closed-pentagon quotient cannot
retract faithfully to that original closed free evidence group.
The quotient is a selected relative algebraic presentation, not a
new original geometric 19D filler or an equality of Type-valued
18D witnesses. No new axioms/sorry/admit, no Gray or abelianization.
Strict Kuu primary, independent Kuu one presentation, DS no-go,
107 public roots, pinned Lean/mathlib, append-only/same-root.
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

section FullClosedPentagonFreeSeparation

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Store the ACTUAL dependent target closed-18D generator and BOTH
full target raw17D endpoints, not a coarse-grained graph label. -/
def nativeC60FBClosedCode
    {x y : (nativeC60DVClosedEighteenLayer S F).Total}
    (g : (nativeC60DVClosedEighteenSignature S F).Gen x y) :
    NativeC60DVCompleteEighteenCode S F :=
  ⟨x, y, g⟩

/-- The full CLOSED-target pentagon LONG path is exactly the
positive THREE-letter word of complete dependent target 18D codes. -/
theorem nativeC60FBClosedPentagon_long_free
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    nativeC60DVClosedFreeWord S F
      (nativeC60DXClosedPentagonLong S F f g h k) =
      (FreeGroup.of (nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.post (.assoc f g h) k)) *
       FreeGroup.of (nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.assoc f (.trans g h) k))) *
       FreeGroup.of (nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.pre f (.assoc g h k))) := rfl

/-- The independently defined full CLOSED-target pentagon SHORT path
is its exact positive TWO-letter complete dependent code word. -/
theorem nativeC60FBClosedPentagon_short_free
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    nativeC60DVClosedFreeWord S F
      (nativeC60DXClosedPentagonShort S F f g h k) =
      FreeGroup.of (nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.assoc (.trans f g) h k)) *
       FreeGroup.of (nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.assoc f g (.trans h k))) := rfl

/-- MAIN FB: even with arbitrary closed 17D dependent input paths,
including repeated paths or repeated 18D letters, the two full
noncommutative target words are UNEQUAL. DS's actual reduced
free-group representatives imply 3 positive letters ≠ 2 positive
letters, without assuming anything about letter equality. -/
theorem nativeC60FBClosedPentagon_free_ne
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    nativeC60DVClosedFreeWord S F
      (nativeC60DXClosedPentagonLong S F f g h k) ≠
    nativeC60DVClosedFreeWord S F
      (nativeC60DXClosedPentagonShort S F f g h k) := by
  rw [nativeC60FBClosedPentagon_long_free S F f g h k,
      nativeC60FBClosedPentagon_short_free S F f g h k]
  change FreeGroup.mk
      [(nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.post (.assoc f g h) k), true),
       (nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.assoc f (.trans g h) k), true),
       (nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.pre f (.assoc g h k)), true)] ≠
    FreeGroup.mk
      [(nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.assoc (.trans f g) h k), true),
       (nativeC60FBClosedCode S F
          (NativeC60DVClosedEighteenGen.assoc f g (.trans h k)), true)]
  exact nativeC60DSThree_positive_ne_two _ _ _ _ _

/-- The exact full CLOSED pentagon normal kernel is nontrivial:
the forced relation kills a genuine nonidentity full FreeGroup word,
not a fake scalar or a strict proof-irrelevance identification. -/
theorem nativeC60FBClosedPentagon_kernel_nontrivial
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    nativeC60DXFullClosedPentagonNormalClosure S F ≠ ⊥ := by
  intro hbot
  have hmem : nativeC60DVClosedFreeWord S F
      (nativeC60DXClosedPentagonLong S F f g h k) *
      (nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonShort S F f g h k))⁻¹ ∈
      (⊥ : Subgroup (NativeC60DVClosedFullFree S F)) := by
    rw [← hbot]
    exact nativeC60DXFullClosedPentagon_defect_mem S F f g h k
  have hone : nativeC60DVClosedFreeWord S F
      (nativeC60DXClosedPentagonLong S F f g h k) *
      (nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonShort S F f g h k))⁻¹ = 1 := by
    simpa using hmem
  exact nativeC60FBClosedPentagon_free_ne S F f g h k
    (eq_of_mul_inv_eq_one hone)

/-- No receiver that retains ALL complete closed-target 18D FreeGroup
information can retract from the selected full closed-pentagon
quotient. The original distinct target words become equal only
AFTER the explicitly chosen relative relation is imposed. -/
theorem nativeC60FBClosedPentagon_no_full_retraction
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    ¬ ∃ retraction : NativeC60DXFullClosedPentagonQuotient S F →*
          NativeC60DVClosedFullFree S F,
        retraction.comp (QuotientGroup.mk'
          (nativeC60DXFullClosedPentagonNormalClosure S F)) =
          MonoidHom.id (NativeC60DVClosedFullFree S F) := by
  rintro ⟨retraction, hcomp⟩
  have hall := (nativeC60DTQuotient_factor_iff
    (nativeC60DXFullClosedPentagonPairs S F)
    (MonoidHom.id (NativeC60DVClosedFullFree S F))).mp
      ⟨retraction, hcomp⟩
  have heq := hall _
    (nativeC60DXFullClosedPentagon_pair_mem S F f g h k)
  exact nativeC60FBClosedPentagon_free_ne S F f g h k (by simpa using heq)

end FullClosedPentagonFreeSeparation

#print axioms nativeC60FBClosedCode
#print axioms nativeC60FBClosedPentagon_long_free
#print axioms nativeC60FBClosedPentagon_short_free
#print axioms nativeC60FBClosedPentagon_free_ne
#print axioms nativeC60FBClosedPentagon_kernel_nontrivial
#print axioms nativeC60FBClosedPentagon_no_full_retraction

end
end Kuu.F112.Physical
