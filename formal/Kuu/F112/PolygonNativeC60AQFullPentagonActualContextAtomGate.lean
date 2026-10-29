import Kuu.F112.PolygonNativeC60AQFullPentagonCrossAtomDescentGate
import Kuu.F112.PolygonNativeC60AQFullPentagonNineteenGaugeNormalBoundary
import Kuu.F112.PolygonNativeC60AQFullPentagonKernelComparison

/-!
# F112-P94D3FA — real finite C60 AQ context transport versus 19D atom gate

DV constructs an actual, typed, complete-code 18D group homomorphism
  ORIGINAL FreeGroup → DISTINCT context-CLOSED 18D FreeGroup
for every finite C60 AQ context word. DW and DX prove that it descends
from the all-original-pentagon relative quotient to the full-closed
pentagon relative quotient. This is NOT an endomorphism of the original
code alphabet and never constructs an original geometric 19D filler.

EY/EZ independently retain all signed primitives actually occurring
inside a GIVEN original dependent 19D candidate path. FA proves:
* the exact original noncommutative pentagon ratio, transported by the
  ACTUAL DV map, is the ordered target signed-atom product;
* that total ratio always lies in DX's full closed-pentagon normal
  kernel (whether or not a hypothetical 19D path is supplied);
* the SOURCE path-selected atomic quotient descends through the same
  DV transport iff EVERY occurring original 19D atom defect maps
  into the target full closed-pentagon kernel;
* failure of that stronger descent is witnessed by an ACTUAL signed
  primitive occurrence inside precisely the candidate path;
* one bad atom yields a rigorous separation: the transported TOTAL
  pentagon ratio vanishes modulo the chosen closed-pentagon relations
  but the path-selected atomic quotient does not descend;
* regrouping the SAME chronological finite AQ context steps leaves
  the exact atomic test unchanged.

No claim that an atom failing this target-kernel test exists, and no
claim that all atoms satisfy it. No full-kernel equality, no erased
original raw Type-valued evidence, no new geometric 19D cell, no
commutativity, abelianization, Gray, axiom, sorry, or admit.
Preserve DS no-go, strict Kuu, independent Kuu presentation,
107 public roots, pinned Lean/mathlib and append-only/same-root.
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

section ActualFiniteC60AQContextAtomDescent

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Source is a particular GIVEN dependent original 19D candidate
path. Only the actually occurring original typed atoms are selected
as relations. This quotient is NOT a physical 19D filler. -/
abbrev NativeC60FAPathAtomQuotient
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    {x y : (nativeC60DSNineteenLayer S F).Total}
    (p : NativeC60AXStep T x y) :=
  NativeC60DTQuotient
    (nativeC60EYSelectedPairs T (nativeC60DSNineteenHolonomy S F)
      (nativeC60EYPathAtoms T p))

/-- Exactly the stronger ATOMIC compatibility condition for the ACTUAL
DV context transport to the independently constructed DX closed-target
quotient, retaining original dependent 19D occurrence provenance. -/
def nativeC60FAContextAtomCompatible
    (word : List Bool)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    {x y : (nativeC60DSNineteenLayer S F).Total}
    (p : NativeC60AXStep T x y) : Prop :=
  ∀ a : NativeC60EYPrimitive T, a ∈ nativeC60EYPathAtoms T p →
    (nativeC60DVFullWordTransport S F word)
      (nativeC60EYPrimitiveDefect T
        (nativeC60DSNineteenHolonomy S F) a) ∈
      nativeC60DXFullClosedPentagonNormalClosure S F

/-- The ACTUAL DV transport of ALL complete original dependent 18D
generator codes descends from the source path-atom quotient through
the separately selected full closed-pentagon quotient EXACTLY iff
EVERY original generator actually occurring in p passes the test. -/
theorem nativeC60FAContext_path_atom_factor_iff
    (word : List Bool)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    {x y : (nativeC60DSNineteenLayer S F).Total}
    (p : NativeC60AXStep T x y) :
    (∃ induced : NativeC60FAPathAtomQuotient S F T p →*
        NativeC60DXFullClosedPentagonQuotient S F,
      induced.comp (QuotientGroup.mk'
        (nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T
            (nativeC60DSNineteenHolonomy S F)
            (nativeC60EYPathAtoms T p)))) =
          (QuotientGroup.mk'
            (nativeC60DXFullClosedPentagonNormalClosure S F)).comp
              (nativeC60DVFullWordTransport S F word)) ↔
      nativeC60FAContextAtomCompatible S F word T p :=
  nativeC60FACrossSelected_factor_iff T
    (nativeC60DSNineteenHolonomy S F)
    (nativeC60EYPathAtoms T p)
    (nativeC60DVFullWordTransport S F word)
    (nativeC60DXFullClosedPentagonNormalClosure S F)

/-- Stronger exact obstruction: non-descent is EQUIVALENT to an actual
SIGNED primitive occurrence inside the EXACT original 19D path whose
transported complete 18D defect is absent from the chosen DX kernel.
The signed source witness is retained; an unrelated ambient T atom
does NOT suffice. -/
theorem nativeC60FAContext_path_failure_iff_signed_bad
    (word : List Bool)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    {x y : (nativeC60DSNineteenLayer S F).Total}
    (p : NativeC60AXStep T x y) :
    (¬ ∃ induced : NativeC60FAPathAtomQuotient S F T p →*
        NativeC60DXFullClosedPentagonQuotient S F,
      induced.comp (QuotientGroup.mk'
        (nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T
            (nativeC60DSNineteenHolonomy S F)
            (nativeC60EYPathAtoms T p)))) =
          (QuotientGroup.mk'
            (nativeC60DXFullClosedPentagonNormalClosure S F)).comp
              (nativeC60DVFullWordTransport S F word)) ↔
      ∃ atom : NativeC60EYSignedPrimitive T,
        atom ∈ nativeC60EYSignedAtoms T p ∧
        (nativeC60DVFullWordTransport S F word)
          (nativeC60EYPrimitiveDefect T
            (nativeC60DSNineteenHolonomy S F)
            atom.primitive) ∉
          nativeC60DXFullClosedPentagonNormalClosure S F := by
  have h := nativeC60FACrossSelected_failure_iff_bad_atom
    T (nativeC60DSNineteenHolonomy S F)
    (nativeC60EYPathAtoms T p)
    (nativeC60DVFullWordTransport S F word)
    (nativeC60DXFullClosedPentagonNormalClosure S F)
  constructor
  · intro hno
    obtain ⟨a, ⟨z, hz, heq⟩, hbad⟩ := h.mp hno
    subst a
    exact ⟨z, hz, hbad⟩
  · rintro ⟨z, hz, hbad⟩
    exact h.mpr ⟨z.primitive, ⟨z, hz, rfl⟩, hbad⟩

/-- Genuine original 18D pentagon defect, BEFORE any hypothetical
19D filler, always transports into the full CLOSED-grammar pentagon
normal kernel. This is a consequence of DW and DX, not of a
source path-atom compatibility assumption. -/
theorem nativeC60FAActualContext_pentagon_ratio_mem_full
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    (nativeC60DVFullWordTransport S F word)
      ((nativeC60DSFreeWord S F
          (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k)) ∈
      nativeC60DXFullClosedPentagonNormalClosure S F := by
  have hsource := nativeC60EYNineteen_ratio_mem_DT S F f g h k
  have himage := nativeC60DWContextPentagon_normalKernel_mem
    S F word hsource
  exact (nativeC60DXImageKernel_le_full S F word) himage

/-- The original complete 18D ratio is therefore zero only in the
SEPARATELY chosen closed target quotient. No original free-word
equality or geometric original 19D filling is implied. -/
theorem nativeC60FAActualContext_pentagon_ratio_quotient_one
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    (QuotientGroup.mk' (nativeC60DXFullClosedPentagonNormalClosure S F))
      ((nativeC60DVFullWordTransport S F word)
        ((nativeC60DSFreeWord S F
            (nativeC60DRPentagonLong S F f g h k))⁻¹ *
          nativeC60DSFreeWord S F
            (nativeC60DRPentagonShort S F f g h k))) = 1 := by
  apply MonoidHom.mem_ker.mp
  rw [QuotientGroup.ker_mk'
    (nativeC60DXFullClosedPentagonNormalClosure S F)]
  exact nativeC60FAActualContext_pentagon_ratio_mem_full
    S F word f g h k

/-- On any ACTUALLY SUPPLIED candidate 19D path, the actual DV
transport of the true full noncommutative pentagon ratio equals
the signed ordered product of ALL original typed primitive defects,
now evaluated in the DISTINCT context-closed 18D full FreeGroup. -/
theorem nativeC60FAActualContext_pentagon_signed_product
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (p : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) :
    (nativeC60DVFullWordTransport S F word)
      ((nativeC60DSFreeWord S F
          (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k)) =
      ((nativeC60EYSignedAtoms T p).map
        (nativeC60EYSignedDefect T
          (fun a => (nativeC60DVFullWordTransport S F word)
            (nativeC60DSNineteenHolonomy S F a)))).prod := by
  calc
    _ = (nativeC60DVFullWordTransport S F word)
        (nativeC60EXFoldDefect T
          (nativeC60DSNineteenHolonomy S F) p) := by
            rw [nativeC60EXPentagon_defect_eq_full_ratio S F f g h k T p]
    _ = _ := (nativeC60FAOrdered_signed_product_transport T
      (nativeC60DSNineteenHolonomy S F)
      (nativeC60DVFullWordTransport S F word) p).symm

/-- SINGLE ACTUAL ATOM OBSTRUCTION: even though the true original
pentagon total automatically lands in the full target kernel,
failure of ONE original typed generator of the candidate filler
to map into that kernel prevents the STRONGER source path-atom
quotient from descending. The two separate assertions coexist. -/
theorem nativeC60FAActualContext_bad_atom_separates
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (p : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k)))
    (atom : NativeC60EYSignedPrimitive T)
    (hocc : atom ∈ nativeC60EYSignedAtoms T p)
    (hbad : (nativeC60DVFullWordTransport S F word)
        (nativeC60EYPrimitiveDefect T
          (nativeC60DSNineteenHolonomy S F) atom.primitive) ∉
        nativeC60DXFullClosedPentagonNormalClosure S F) :
    ((nativeC60DVFullWordTransport S F word)
      ((nativeC60DSFreeWord S F
          (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k)) ∈
      nativeC60DXFullClosedPentagonNormalClosure S F) ∧
    ¬ ∃ induced : NativeC60FAPathAtomQuotient S F T p →*
        NativeC60DXFullClosedPentagonQuotient S F,
      induced.comp (QuotientGroup.mk'
        (nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T
            (nativeC60DSNineteenHolonomy S F)
            (nativeC60EYPathAtoms T p)))) =
          (QuotientGroup.mk'
            (nativeC60DXFullClosedPentagonNormalClosure S F)).comp
              (nativeC60DVFullWordTransport S F word) := by
  refine ⟨nativeC60FAActualContext_pentagon_ratio_mem_full
      S F word f g h k, ?_⟩
  exact (nativeC60FAContext_path_failure_iff_signed_bad
    S F word T p).mpr ⟨atom, hocc, hbad⟩

/-- The ORIGINAL all-pentagon quotient always descends along DV to
the full closed target (DX), while descent of the quite DIFFERENT
path-selected atomic quotient has the precise additional FA test.
Neither a 19D filler nor the atomic gate follows from global descent. -/
theorem nativeC60FAActualContext_global_and_path_gate
    (word : List Bool)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    {x y : (nativeC60DSNineteenLayer S F).Total}
    (p : NativeC60AXStep T x y) :
    (∃ induced : NativeC60DTPentagonQuotient S F →*
        NativeC60DXFullClosedPentagonQuotient S F,
      induced.comp (QuotientGroup.mk'
        (nativeC60DTPentagonNormalClosure S F)) =
          (QuotientGroup.mk'
            (nativeC60DXFullClosedPentagonNormalClosure S F)).comp
              (nativeC60DVFullWordTransport S F word)) ∧
    ((∃ induced : NativeC60FAPathAtomQuotient S F T p →*
        NativeC60DXFullClosedPentagonQuotient S F,
      induced.comp (QuotientGroup.mk'
        (nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T
            (nativeC60DSNineteenHolonomy S F)
            (nativeC60EYPathAtoms T p)))) =
          (QuotientGroup.mk'
            (nativeC60DXFullClosedPentagonNormalClosure S F)).comp
              (nativeC60DVFullWordTransport S F word)) ↔
      nativeC60FAContextAtomCompatible S F word T p) :=
  ⟨nativeC60DXSourceToFullQuotient_factor S F word,
    nativeC60FAContext_path_atom_factor_iff S F word T p⟩

/-- Finite genuine AQ context TREES with the SAME ordered chronological
steps give the SAME exact original-to-closed atom compatibility gate.
No composition-order loss or 19D geometry is inferred. -/
theorem nativeC60FAActualTree_atom_gate_refinement
    {left right : NativeK5DOContextTree}
    (h : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    {x y : (nativeC60DSNineteenLayer S F).Total}
    (p : NativeC60AXStep T x y) :
    nativeC60FAContextAtomCompatible S F (nativeK5DOTreeWord left) T p ↔
      nativeC60FAContextAtomCompatible S F
        (nativeK5DOTreeWord right) T p := by
  rw [nativeK5DOTreeWord_eq_of_steps_eq h]

end ActualFiniteC60AQContextAtomDescent

#print axioms NativeC60FAPathAtomQuotient
#print axioms nativeC60FAContextAtomCompatible
#print axioms nativeC60FAContext_path_atom_factor_iff
#print axioms nativeC60FAContext_path_failure_iff_signed_bad
#print axioms nativeC60FAActualContext_pentagon_ratio_mem_full
#print axioms nativeC60FAActualContext_pentagon_ratio_quotient_one
#print axioms nativeC60FAActualContext_pentagon_signed_product
#print axioms nativeC60FAActualContext_bad_atom_separates
#print axioms nativeC60FAActualContext_global_and_path_gate
#print axioms nativeC60FAActualTree_atom_gate_refinement

end
end Kuu.F112.Physical
