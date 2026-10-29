import Kuu.F112.PolygonNativeC60AQFullPentagonConstructorSectorSeparation

/-!
# F112-P94D3FG — actual assoc/post/pre source-path argument injectivity

FF showed the original complete 18D OBJECT map injective under real
17D context-object injectivity. Its first 18D object includes the
entire ORIGINAL raw17D source proof, with no quotient.

We now use that real dependent 18D object to show all three original
18D generator constructors reflect equality of their actual
17D raw-path arguments:
* assoc: all three source paths jointly injective at fixed lower
  endpoint sequence, by the raw source word ((f·g)·h);
* post: the genuine post-whiskering 17D suffix is injective for each
  fixed original inner 18D generator;
* pre: the genuine pre-whiskering 17D prefix is injective for each
  fixed original inner 18D generator.

These are positive nontrivial injections in the ACTUAL complete DV
18D dependent code space. They do not infer injectivity of varying
inner pre/post 18D recursive generator data from object injectivity
alone. Those inner fibers are the remaining explicit FG obstruction.
No erased original lower Type-valued histories, no abelian shadow,
Gray, unproved geometric 19D filler or new axiom/sorry/admit.
107 roots, strict Kuu primary, independent Kuu presentation, DS no-go.
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

section GenuineEighteenConstructorPaths

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

abbrev NativeC60FGOriginal17Step
    (a b : (nativeC60DQSeventeenLayer S F).Total) : Type u :=
  NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b

/-- Actual full dependent 18D transport of an original triple of
composable 17D proofs, as an ORIGINAL assoc generator certificate. -/
def nativeC60FGAssocTripleTransport (word : List Bool)
    {a b c d : (nativeC60DQSeventeenLayer S F).Total}
    (t : (NativeC60FGOriginal17Step S F a b ×
      NativeC60FGOriginal17Step S F b c) ×
      NativeC60FGOriginal17Step S F c d) :
    NativeC60DVCompleteEighteenCode S F :=
  nativeC60DVTransportCompleteCode S F word
    (nativeC60DSCode S F
      (.assoc t.1.1 t.1.2 t.2))

/-- The genuine original three-input assoc sector is injective
as a triple of ALL THREE raw17D proofs at fixed exact dependent
lower endpoints. The proof uses the original source 18D object,
not a parity, a list of faces, or a quotient. -/
theorem nativeC60FGAssocTripleTransport_injective
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word))
    {a b c d : (nativeC60DQSeventeenLayer S F).Total} :
    Function.Injective
      (nativeC60FGAssocTripleTransport S F word
        (a := a) (b := b) (c := c) (d := d)) := by
  rintro ⟨⟨f, g⟩, h⟩ ⟨⟨f', g'⟩, h'⟩ heq
  have hsrc :
      nativeC60DRPackSeventeen S F (.trans (.trans f g) h) =
        nativeC60DRPackSeventeen S F (.trans (.trans f' g') h') := by
    apply nativeC60FFDVTransportEighteenObj_injective S F word hctx
    exact congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
      code.1) heq
  have hraw :
      NativeC60AXStep.trans (NativeC60AXStep.trans f g) h =
        NativeC60AXStep.trans (NativeC60AXStep.trans f' g') h' :=
    eq_of_heq (Sigma.mk.inj hsrc).2
  have hfg : NativeC60AXStep.trans f g = NativeC60AXStep.trans f' g' := by
    injection hraw
  have hh : h = h' := by
    injection hraw
  have hf : f = f' := by
    injection hfg
  have hg : g = g' := by
    injection hfg
  cases hf
  cases hg
  cases hh
  rfl

/-- The genuine 18D post-whiskering map is faithful in its entire
original 17D suffix, for fixed original recursive inner generator.
No recursive generator injectivity is silently asserted. -/
theorem nativeC60FGPostSuffixTransport_injective
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word))
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F a b}
    (r : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p)
      (nativeC60DRPackSeventeen S F q)) :
    Function.Injective
      (fun h : NativeC60FGOriginal17Step S F b c =>
        nativeC60DVTransportCompleteCode S F word
          (nativeC60DSCode S F (.post r h))) := by
  intro h k heq
  have hsrc :
      nativeC60DRPackSeventeen S F (.trans p h) =
        nativeC60DRPackSeventeen S F (.trans p k) := by
    apply nativeC60FFDVTransportEighteenObj_injective S F word hctx
    exact congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
      code.1) heq
  have hraw : NativeC60AXStep.trans p h =
      NativeC60AXStep.trans p k :=
    eq_of_heq (Sigma.mk.inj hsrc).2
  have hh : h = k := by
    injection hraw
  cases hh
  rfl

/-- The genuine 18D pre-whiskering map is faithful in its entire
original 17D prefix, with fixed recursive inner 18D generator.
Again, no unproven recursive-generator faithfulness is assumed. -/
theorem nativeC60FGPrePrefixTransport_injective
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word))
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F b c}
    (r : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p)
      (nativeC60DRPackSeventeen S F q)) :
    Function.Injective
      (fun h : NativeC60FGOriginal17Step S F a b =>
        nativeC60DVTransportCompleteCode S F word
          (nativeC60DSCode S F (.pre h r))) := by
  intro h k heq
  have hsrc :
      nativeC60DRPackSeventeen S F (.trans h p) =
        nativeC60DRPackSeventeen S F (.trans k p) := by
    apply nativeC60FFDVTransportEighteenObj_injective S F word hctx
    exact congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
      code.1) heq
  have hraw : NativeC60AXStep.trans h p =
      NativeC60AXStep.trans k p :=
    eq_of_heq (Sigma.mk.inj hsrc).2
  have hh : h = k := by
    injection hraw
  cases hh
  rfl

end GenuineEighteenConstructorPaths

#print axioms nativeC60FGAssocTripleTransport
#print axioms nativeC60FGAssocTripleTransport_injective
#print axioms nativeC60FGPostSuffixTransport_injective
#print axioms nativeC60FGPrePrefixTransport_injective

end
end Kuu.F112.Physical
