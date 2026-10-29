import Kuu.F112.PolygonNativeC60AQFullPentagonClosedFreeSeparation

/-!
# F112-P94D3FB — actual DV transport detects the original 18D pentagon

FA proved that DV's ACTUALLY CONSTRUCTED typed complete-code
transport, ORIGINAL 18D FreeGroup -> separately context-CLOSED 18D
FreeGroup, kills original pentagon differences only AFTER the
chosen DX closed-pentagon normal quotient.

FB proves the complementary assertion BEFORE QUOTIENT:
* For ANY original four composable raw17D witnesses and ANY finite
  chronological C60 AQ context word, the FULL target 18D free words
  of the actually transported long and short pentagon are unequal.
* Their exact signed noncommutative difference is NONIDENTITY in the
  target original closed free group, yet belongs to the explicit DX
  normal kernel and maps to 1 in its separate quotient.
* The actual DV map of the whole original full 18D code group
  CANNOT factor from DT's source all-pentagon quotient into the
  UNQUOTIENTED full closed 18D free evidence group. It DOES factor
  into the independently selected DX relative quotient (already DX).
* Even after original finite AQ context transport, any actually
  SUPPLIED dependent Type-valued candidate 19D pentagon filler
  contains a specific occurring typed primitive whose source and
  target give DISTINCT transported complete 18D free evidence.
  This is a conditional theorem; it does NOT construct a filler.
* No candidate 19D signature whose atoms ALL preserve this actual
  transported complete free evidence can fill the original pentagon.

No map from closed target grammar back to the original raw alphabet
is asserted; no injectivity of the complete DV free-group transport
on ALL words is claimed. The original DS no-go and the existence of
a merely declared relative 19D comparison stay distinct.
Preserve strict Kuu, independent Kuu as a presentation, 14D--18D
proof histories, 107 published roots, no Gray/abelianization, pinned
Lean/mathlib, append-only/tighten-only/same-root; no sorry/new axiom.
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

section ActualC60FiniteContextFreeSeparation

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- MAIN FB: the ACTUAL finite-AQ 17D/18D DV transport of the
complete ORIGINAL noncommutative long/short pentagon 18D words
remains unequal in the unmodified closed-target FreeGroup.
We use DV naturality and DX's exact dependent transported routes,
then the target free-group proof independent of any injectivity
assumption about the transport on all source words. -/
theorem nativeC60FBActualTransportPentagon_free_ne
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    (nativeC60DVFullWordTransport S F word)
      (nativeC60DSFreeWord S F
        (nativeC60DRPentagonLong S F f g h k)) ≠
    (nativeC60DVFullWordTransport S F word)
      (nativeC60DSFreeWord S F
        (nativeC60DRPentagonShort S F f g h k)) := by
  rw [nativeC60DVFullWordTransport_natural S F word
      (nativeC60DRPentagonLong S F f g h k),
    nativeC60DVFullWordTransport_natural S F word
      (nativeC60DRPentagonShort S F f g h k),
    nativeC60DXTransportPentagonLong S F word f g h k,
    nativeC60DXTransportPentagonShort S F word f g h k]
  exact nativeC60FBClosedPentagon_free_ne S F
    (nativeC60DVSeventeenWordMap S F word f)
    (nativeC60DVSeventeenWordMap S F word g)
    (nativeC60DVSeventeenWordMap S F word h)
    (nativeC60DVSeventeenWordMap S F word k)

/-- The actual DV image of the original COMPLETE long⁻¹ * short
noncommutative ratio is nonidentity even after any finite C60 AQ
context transport. This is stronger than the original source-only
DS nonidentity and does not identify the two alphabets. -/
theorem nativeC60FBActualTransportPentagon_ratio_ne_one
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
          (nativeC60DRPentagonShort S F f g h k)) ≠ 1 := by
  intro hr
  let τ := nativeC60DVFullWordTransport S F word
  let wl := nativeC60DSFreeWord S F
    (nativeC60DRPentagonLong S F f g h k)
  let wr := nativeC60DSFreeWord S F
    (nativeC60DRPentagonShort S F f g h k)
  have hratio : (τ wl)⁻¹ * τ wr = 1 := by
    simpa only [τ, wl, wr, map_mul, map_inv] using hr
  have hshortlong : τ wr = τ wl := by
    calc
      τ wr = τ wl * ((τ wl)⁻¹ * τ wr) := by group
      _ = τ wl * 1 := congrArg (fun t : NativeC60DVClosedFullFree S F =>
        τ wl * t) hratio
      _ = τ wl := mul_one _
  exact (nativeC60FBActualTransportPentagon_free_ne S F
    word f g h k) hshortlong.symm

/-- The original ratio is killed in the explicitly selected
DX relative quotient but NOT in the target unmodified free group.
These are two distinct mathematical claims, both exact. -/
theorem nativeC60FBActualTransport_ratio_kernel_boundary
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    let defect := (nativeC60DSFreeWord S F
        (nativeC60DRPentagonLong S F f g h k))⁻¹ *
      nativeC60DSFreeWord S F
        (nativeC60DRPentagonShort S F f g h k)
    (nativeC60DVFullWordTransport S F word) defect ≠ 1 ∧
    (nativeC60DVFullWordTransport S F word) defect ∈
      nativeC60DXFullClosedPentagonNormalClosure S F ∧
    (QuotientGroup.mk' (nativeC60DXFullClosedPentagonNormalClosure S F))
      ((nativeC60DVFullWordTransport S F word) defect) = 1 := by
  dsimp only
  exact ⟨nativeC60FBActualTransportPentagon_ratio_ne_one
      S F word f g h k,
    nativeC60FAActualContext_pentagon_ratio_mem_full
      S F word f g h k,
    nativeC60FAActualContext_pentagon_ratio_quotient_one
      S F word f g h k⟩

/-- Despite DX's true quotient descent, the ACTUAL DV complete
18D transport cannot descend from the original all-pentagon
relative quotient into the UNQUOTIENTED closed-target FreeGroup:
the actual source pentagon pair still has distinct image words. -/
theorem nativeC60FBActualTransport_no_unquotiented_factor
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    ¬ ∃ induced : NativeC60DTPentagonQuotient S F →*
          NativeC60DVClosedFullFree S F,
        induced.comp (QuotientGroup.mk'
          (nativeC60DTPentagonNormalClosure S F)) =
          nativeC60DVFullWordTransport S F word := by
  intro hfactor
  have hall := (nativeC60DTQuotient_factor_iff
    (nativeC60DTPentagonPairs S F)
    (nativeC60DVFullWordTransport S F word)).mp hfactor
  have heq := hall _
    (nativeC60DTPentagon_pair_mem S F f g h k)
  exact (nativeC60FBActualTransportPentagon_free_ne
    S F word f g h k) (by simpa using heq)

/-- The ACTUAL DV transport does descend into the explicitly
chosen full-closed pentagon quotient (DX), while it DOES NOT factor
into the original unquotiented full-closed FreeGroup. -/
theorem nativeC60FBActualTransport_exact_relative_boundary
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    (∃ induced : NativeC60DTPentagonQuotient S F →*
        NativeC60DXFullClosedPentagonQuotient S F,
      induced.comp (QuotientGroup.mk'
        (nativeC60DTPentagonNormalClosure S F)) =
        (QuotientGroup.mk'
          (nativeC60DXFullClosedPentagonNormalClosure S F)).comp
            (nativeC60DVFullWordTransport S F word)) ∧
    ¬ ∃ induced : NativeC60DTPentagonQuotient S F →*
        NativeC60DVClosedFullFree S F,
      induced.comp (QuotientGroup.mk'
        (nativeC60DTPentagonNormalClosure S F)) =
          nativeC60DVFullWordTransport S F word :=
  ⟨nativeC60DXSourceToFullQuotient_factor S F word,
    nativeC60FBActualTransport_no_unquotiented_factor
      S F word f g h k⟩

/-- If an ACTUAL 19D candidate filler is supplied, a primitive
occurring INSIDE ITS ORIGINAL DEPENDENT SIGNED PATH must change
the complete 18D FREE holonomy even AFTER DV finite AQ context
transport into its distinct closed target free group. -/
theorem nativeC60FBActualTransportFiller_bad_atom
    (word : List Bool)
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
    ∃ (x y : (nativeC60DSNineteenLayer S F).Total)
      (atom : T.Gen x y),
      NativeC60EWAtomOccursOn T atom filler ∧
      (nativeC60DVFullWordTransport S F word)
        (nativeC60DSNineteenHolonomy S F x) ≠
      (nativeC60DVFullWordTransport S F word)
        (nativeC60DSNineteenHolonomy S F y) := by
  let obs : (nativeC60DSNineteenLayer S F).Total →
      NativeC60DVClosedFullFree S F :=
    fun x => (nativeC60DVFullWordTransport S F word)
      (nativeC60DSNineteenHolonomy S F x)
  have hne : obs
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k)) ≠
      obs (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k)) := by
    exact nativeC60FBActualTransportPentagon_free_ne
      S F word f g h k
  obtain ⟨x, y, atom, hocc, hbad⟩ :=
    nativeC60EWBadOnPath_exact_atom T obs
      (nativeC60EWBadOnPath_of_endpoint_ne T obs filler hne)
  exact ⟨x, y, atom, hocc, hbad⟩

/-- Hence a candidate original 19D signature whose EACH primitive
preserves full DV-transported 18D free evidence can NOT have any
original typed pentagon filler. This is a stronger transported
no-go, not a declaration of a new original 19D geometry. -/
theorem nativeC60FBNoTransportCompatibleNineteenFiller
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (hc : ∀ {x y : (nativeC60DSNineteenLayer S F).Total}
       (_ : T.Gen x y),
      (nativeC60DVFullWordTransport S F word)
        (nativeC60DSNineteenHolonomy S F x) =
      (nativeC60DVFullWordTransport S F word)
        (nativeC60DSNineteenHolonomy S F y)) :
    ¬ Nonempty (NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k))) := by
  rintro ⟨filler⟩
  obtain ⟨x, y, atom, _, hbad⟩ :=
    nativeC60FBActualTransportFiller_bad_atom
      S F word f g h k T filler
  exact hbad (hc atom)

/-- The stronger free-evidence separation persists under ANY actual
finite AQ context tree; no finite rebracketing of its steps makes the
original long and short complete transported 18D words equal. -/
theorem nativeC60FBActualTree_pentagon_free_ne
    (tree : NativeK5DOContextTree)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    (nativeC60DVFullWordTransport S F (nativeK5DOTreeWord tree))
      (nativeC60DSFreeWord S F
        (nativeC60DRPentagonLong S F f g h k)) ≠
    (nativeC60DVFullWordTransport S F (nativeK5DOTreeWord tree))
      (nativeC60DSFreeWord S F
        (nativeC60DRPentagonShort S F f g h k)) :=
  nativeC60FBActualTransportPentagon_free_ne
    S F (nativeK5DOTreeWord tree) f g h k

end ActualC60FiniteContextFreeSeparation

#print axioms nativeC60FBActualTransportPentagon_free_ne
#print axioms nativeC60FBActualTransportPentagon_ratio_ne_one
#print axioms nativeC60FBActualTransport_ratio_kernel_boundary
#print axioms nativeC60FBActualTransport_no_unquotiented_factor
#print axioms nativeC60FBActualTransport_exact_relative_boundary
#print axioms nativeC60FBActualTransportFiller_bad_atom
#print axioms nativeC60FBNoTransportCompatibleNineteenFiller
#print axioms nativeC60FBActualTree_pentagon_free_ne

end
end Kuu.F112.Physical
