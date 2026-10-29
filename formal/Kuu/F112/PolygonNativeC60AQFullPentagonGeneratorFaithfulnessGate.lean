import Kuu.F112.PolygonNativeC60AQFullPentagonEighteenObjectReflectionGate
import Kuu.F112.PolygonNativeC60AQFullPentagonCodeFiberKernel

/-!
# F112-P94D3FG — exact complete 18D generator faithfulness gate

FF proves that every ORIGINAL raw dependent 18D OBJECT (both genuine
17D lower endpoints and the entire original 17D raw proof term) is
reflected by real DV transport under an explicit original 17D
context-object injectivity hypothesis.

FG isolates the remaining, mathematically distinct, higher-GENERATOR
obligation. Under precisely the FF object gate, injectivity of the
ACTUAL complete dependent 18D code function is EQUIVALENT to the
family of injectivity obligations for original source/target-fixed
assoc/pre/post 18D generators. The latter is the ACTUAL existing
NativeC60DREighteenAssocGen, not a newly invented graph alphabet or
an unnamed faithful morphism.

The exact equivalence transports through pinned mathlib FreeGroup.map
to a criterion for injectivity of the entire ORIGINAL signed,
noncommutative 18D free-word map. Failure in this gate is not concealed
as loss of lower objects, nor does it follow from injectivity of
objects alone.

This file is a proof of the precise generator obstruction gate, NOT
a proof of its unconditional satisfaction for arbitrary C60 frames.
It preserves the complete original dependent 14D--18D Type-valued
proof history, the distinct closed target, DS no-go, strict Kuu
primary, independent Kuu as a presentation, 107 published roots,
no Gray, no original 19D geometric filler, no new axiom/sorry/admit.
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

section CompleteGeneratorGate

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- FULL 18D CODE REFLECTION from the actual FF lower-object theorem
and actual constructor-level dependent generator reflection. The
latter must be supplied and is not inferred from object injectivity. -/
theorem nativeC60FGCompleteCode_injective_of_gen
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word))
    (hgen : ∀ {x y : (nativeC60DREighteenLayer S F).Total},
      Function.Injective
        (fun g : (nativeC60DREighteenAssocSignature S F).Gen x y =>
          nativeC60DVTransportEighteenGen S F word g)) :
    Function.Injective (nativeC60DVTransportCompleteCode S F word) := by
  intro a b hab
  rcases a with ⟨x, y, g⟩
  rcases b with ⟨x', y', h⟩
  have hx :
      nativeC60DVTransportEighteenObj S F word x =
        nativeC60DVTransportEighteenObj S F word x' :=
    congrArg (fun code : NativeC60DVCompleteEighteenCode S F => code.1) hab
  have hxx : x = x' :=
    nativeC60FFDVTransportEighteenObj_injective S F word hctx hx
  cases hxx
  have hy :
      nativeC60DVTransportEighteenObj S F word y =
        nativeC60DVTransportEighteenObj S F word y' :=
    congrArg (fun code : NativeC60DVCompleteEighteenCode S F => code.2.1) hab
  have hyy : y = y' :=
    nativeC60FFDVTransportEighteenObj_injective S F word hctx hy
  cases hyy
  have htail :
      (⟨nativeC60DVTransportEighteenObj S F word y,
         nativeC60DVTransportEighteenGen S F word g⟩ :
         Σ z : (nativeC60DVClosedEighteenLayer S F).Total,
           (nativeC60DVClosedEighteenSignature S F).Gen
             (nativeC60DVTransportEighteenObj S F word x) z) =
      ⟨nativeC60DVTransportEighteenObj S F word y,
         nativeC60DVTransportEighteenGen S F word h⟩ :=
    eq_of_heq (Sigma.mk.inj hab).2
  have hgmap : nativeC60DVTransportEighteenGen S F word g =
      nativeC60DVTransportEighteenGen S F word h :=
    eq_of_heq (Sigma.mk.inj htail).2
  have gh : g = h := hgen hgmap
  cases gh
  rfl

/-- With the ACTUAL FF object condition, complete 18D code
injectivity is EXACTLY all fixed-boundary 18D generator injectivity.
This is neither a hidden axiom nor a declaration that the gate is
automatically satisfied. -/
theorem nativeC60FGCompleteCode_injective_iff_generators
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word)) :
    Function.Injective (nativeC60DVTransportCompleteCode S F word) ↔
      ∀ {x y : (nativeC60DREighteenLayer S F).Total},
        Function.Injective
          (fun g : (nativeC60DREighteenAssocSignature S F).Gen x y =>
            nativeC60DVTransportEighteenGen S F word g) := by
  constructor
  · intro hcode x y g h hgh
    apply nativeC60DSCode_injective S F
    apply hcode
    change (⟨nativeC60DVTransportEighteenObj S F word x,
      nativeC60DVTransportEighteenObj S F word y,
      nativeC60DVTransportEighteenGen S F word g⟩ :
        NativeC60DVCompleteEighteenCode S F) =
      ⟨nativeC60DVTransportEighteenObj S F word x,
        nativeC60DVTransportEighteenObj S F word y,
        nativeC60DVTransportEighteenGen S F word h⟩
    cases hgh
    rfl
  · intro hgen
    exact nativeC60FGCompleteCode_injective_of_gen S F word hctx hgen

/-- FC's pinned free-group equivalence lifts this exact ACTUAL
dependent 18D generator criterion to the whole ordered signed
noncommutative ORIGINAL 18D evidence, conditional on hctx. -/
theorem nativeC60FGFullFree_injective_iff_generators
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word)) :
    Function.Injective (nativeC60DVFullWordTransport S F word) ↔
      ∀ {x y : (nativeC60DREighteenLayer S F).Total},
        Function.Injective
          (fun g : (nativeC60DREighteenAssocSignature S F).Gen x y =>
            nativeC60DVTransportEighteenGen S F word g) := by
  exact (nativeC60FCTransport_injective_iff_code S F word).trans
    (nativeC60FGCompleteCode_injective_iff_generators S F word hctx)

end CompleteGeneratorGate

#print axioms nativeC60FGCompleteCode_injective_of_gen
#print axioms nativeC60FGCompleteCode_injective_iff_generators
#print axioms nativeC60FGFullFree_injective_iff_generators

end
end Kuu.F112.Physical
