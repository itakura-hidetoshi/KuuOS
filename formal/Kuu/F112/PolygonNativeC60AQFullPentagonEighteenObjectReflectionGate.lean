import Kuu.F112.PolygonNativeC60AQFullPentagonRawSeventeenPathReflection

/-!
# F112-P94D3FF — from original raw 17D reflection to entire 18D objects

The actual DV 18D object map acts on the complete dependent object
code consisting of the ORIGINAL 17D raw comparison and both of its
original full lower proof-carrying endpoints. This file establishes
the sufficient condition for its injectivity: the actual finite
DR seventeen-dimensional object context action must be injective.

This is stronger than the FE reflexive-associator code sector: all
original raw 17D proof terms (atoms, identities, inverses and
composites) are reflected, without quotienting to Peiffer, BV
holonomy, scalar parity or a chosen 19D target. In particular both
physical Bool singleton DR frame components admit explicit sufficient
conditions for all finite AQ words to preserve full 18D objects.

Crucially, injectivity of full 18D OBJECTS is not silently identified
with injectivity of arbitrary assoc/pre/post 18D GENERATOR CODES.
That next constructor-recursion obligation is left explicit.
No new axioms/sorry/admit. Keep strict Kuu primary, independent
Kuu as one presentation, 107 public roots, DS complete-evidence
no-go, no Gray, original versus closed 18D targets separate.
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

section ActualDependentSeventeenReflection

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A real original 17D raw proof cannot collapse under the ACTUAL
finite DV context word when the underlying full proof-carrying
17D object action is injective. -/
theorem nativeC60FFDVSeventeenWordMap_injective
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word))
    {a b : (nativeC60DQSeventeenLayer S F).Total} :
    Function.Injective (fun p :
      NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b =>
      nativeC60DVSeventeenWordMap S F word p) :=
  nativeC60FFBCOriginalStep_injective
    (nativeC60DQTriangleSeventeenSignature S F)
    (nativeC60DRSeventeenFrame S F) word hctx

/-- ALL original 18D objects, including their genuinely dependent
two original 17D endpoints AND the complete original raw 17D path,
are reflected by actual DV transport provided the original 17D
context object action is injective. This does not replace objects
with closed quotient classes. -/
theorem nativeC60FFDVTransportEighteenObj_injective
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word)) :
    Function.Injective (nativeC60DVTransportEighteenObj S F word) := by
  intro x y h
  rcases x with ⟨⟨a, b⟩, p⟩
  rcases y with ⟨⟨a', b'⟩, q⟩
  have hpair :
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word a,
       nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word b) =
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word a',
       nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word b') :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1) h
  have ha : a = a' := hctx (Prod.mk.inj hpair).1
  have hb : b = b' := hctx (Prod.mk.inj hpair).2
  cases ha
  cases hb
  have hpath : nativeC60DVSeventeenWordMap S F word p =
      nativeC60DVSeventeenWordMap S F word q :=
    eq_of_heq (Sigma.mk.inj h).2
  have hp : p = q :=
    (nativeC60FFDVSeventeenWordMap_injective S F word hctx) hpath
  cases hp
  rfl

/-- At the EMPTY AQ context, no lower proof information can be
lost: the entire actual original 18D object map is injective
unconditionally, even for arbitrary C60 frames. -/
theorem nativeC60FFDVTransportEighteenObj_nil_injective :
    Function.Injective (nativeC60DVTransportEighteenObj S F []) := by
  apply nativeC60FFDVTransportEighteenObj_injective S F []
  intro a b h
  exact h

/-- Explicit two-singleton SUFFICIENT conditions, carried at the
full dependent Hom level, ensure injectivity on EVERY original 18D
object after EVERY actual finite C60 AQ context word. -/
theorem nativeC60FFAllDVTransportEighteenObj_injective_of_frame_parts
    (hobj : ∀ side : Bool,
      Function.Injective (nativeC60DRSeventeenFrame S F side).onObj)
    (hcell : ∀ (side : Bool)
      {a b : (nativeC60DQSeventeenLayer S F).Obj},
        Function.Injective (fun p :
          (nativeC60DQSeventeenLayer S F).Hom a b =>
          (nativeC60DRSeventeenFrame S F side).onCell p)) :
    ∀ word : List Bool,
      Function.Injective (nativeC60DVTransportEighteenObj S F word) := by
  intro word
  exact nativeC60FFDVTransportEighteenObj_injective S F word
    (nativeC60FEAllSeventeenContexts_injective_of_frame_parts
      S F hobj hcell word)

end ActualDependentSeventeenReflection

#print axioms nativeC60FFDVSeventeenWordMap_injective
#print axioms nativeC60FFDVTransportEighteenObj_injective
#print axioms nativeC60FFDVTransportEighteenObj_nil_injective
#print axioms nativeC60FFAllDVTransportEighteenObj_injective_of_frame_parts

end
end Kuu.F112.Physical
