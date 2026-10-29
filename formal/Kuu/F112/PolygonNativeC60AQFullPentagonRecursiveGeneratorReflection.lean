import Kuu.F112.PolygonNativeC60AQFullPentagonConstructorPathInjectivity

/-!
# F112-P94D3FH — variable-inner dependent 18D generator reflection

FG proves that the ORIGINAL full DV 18D code separately reflects all
assoc raw17D arguments, post suffixes and pre prefixes under the exact
17D context-object injectivity gate. FH addresses the previously
unexamined VARIABLE recursive inner generator of post and pre.

These theorems extract the complete inner 18D target generator CODE
from the actual unquotiented post/pre target syntax, without projecting
to a parity or abelian trace. They prove a precise recursive
faithfulness transfer: when the map is faithful on a fixed original
inner 18D boundary fiber, it is faithful jointly on that variable
inner generator and the entire variable original 17D whiskering path.
The latter is independently recovered from the original full 18D
object under exactly the FF context-object injectivity gate.

These are conditional recursive transfer theorems, NOT an assumption
that arbitrary physical C60 contexts satisfy the lower-object gate,
NOR a proof of unconditional full DV 18D code injectivity.
The original versus context-closed target alphabets, DS no-go,
107 published roots, strict Kuu primary, independent Kuu as one
presentation, and no Gray/no original geometric 19D filler remain.
No axioms, sorry, admit or erasure of Type-valued proof histories.
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

section GenuineRecursiveEighteenGenerators

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Recover the *entire* dependent INNER 18D generator code from
an actual target post-whiskering generator. This is a dependent
Sigma code, not a quotient or a lossy invariant. -/
def nativeC60FHClosedPostInnerCode
    (code : NativeC60DVCompleteEighteenCode S F) :
    Option (NativeC60DVCompleteEighteenCode S F) :=
  match code.2.2 with
  | .post r _ => some ⟨_, _, r⟩
  | _ => none

/-- The analogous full dependent inner code for pre-whiskering. -/
def nativeC60FHClosedPreInnerCode
    (code : NativeC60DVCompleteEighteenCode S F) :
    Option (NativeC60DVCompleteEighteenCode S F) :=
  match code.2.2 with
  | .pre _ r => some ⟨_, _, r⟩
  | _ => none

/-- Post-whiskering with BOTH the original inner 18D generator and
the original 17D suffix allowed to vary, over fixed exact lower
p/q endpoints. Codomain is the genuine full DV dependent 18D code. -/
def nativeC60FHPostPairTransport (word : List Bool)
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F a b}
    (t : (nativeC60DREighteenAssocSignature S F).Gen
            (nativeC60DRPackSeventeen S F p)
            (nativeC60DRPackSeventeen S F q) ×
          NativeC60FGOriginal17Step S F b c) :
    NativeC60DVCompleteEighteenCode S F :=
  nativeC60DVTransportCompleteCode S F word
    (nativeC60DSCode S F (.post t.1 t.2))

/-- Pre-whiskering with BOTH the 17D prefix and the recursive inner
18D generator allowed to vary, retaining the original endpoints. -/
def nativeC60FHPrePairTransport (word : List Bool)
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F b c}
    (t : NativeC60FGOriginal17Step S F a b ×
          (nativeC60DREighteenAssocSignature S F).Gen
            (nativeC60DRPackSeventeen S F p)
            (nativeC60DRPackSeventeen S F q)) :
    NativeC60DVCompleteEighteenCode S F :=
  nativeC60DVTransportCompleteCode S F word
    (nativeC60DSCode S F (.pre t.1 t.2))

/-- TRUE recursive post-reflection: a known faithful ORIGINAL inner
fiber induces joint faithfulness in a VARIABLE recursive 18D
generator and an arbitrary compatible 17D suffix. The source
18D object reflects the suffix; the target post constructor
recovers the full unquotiented transported INNER dependent code. -/
theorem nativeC60FHPostPairTransport_injective_of_inner
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word))
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F a b}
    (hinner : Function.Injective
      (fun r : (nativeC60DREighteenAssocSignature S F).Gen
          (nativeC60DRPackSeventeen S F p)
          (nativeC60DRPackSeventeen S F q) =>
        nativeC60DVTransportCompleteCode S F word
          (nativeC60DSCode S F r))) :
    Function.Injective
      (nativeC60FHPostPairTransport S F word
        (a := a) (b := b) (c := c) (p := p) (q := q)) := by
  rintro ⟨r, h⟩ ⟨s, k⟩ heq
  have hsrc :
      nativeC60DRPackSeventeen S F (.trans p h) =
        nativeC60DRPackSeventeen S F (.trans p k) := by
    apply nativeC60FFDVTransportEighteenObj_injective S F word hctx
    exact congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
      code.1) heq
  have hraw :
      NativeC60AXStep.trans p h = NativeC60AXStep.trans p k :=
    eq_of_heq (Sigma.mk.inj hsrc).2
  have hh : h = k := by
    injection hraw
  have hinnerImage := congrArg (nativeC60FHClosedPostInnerCode S F) heq
  change
      some (nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F r)) =
      some (nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F s)) at hinnerImage
  have hr : r = s := hinner (Option.some.inj hinnerImage)
  cases hr
  cases hh
  rfl

/-- TRUE recursive pre-reflection: a known faithful ORIGINAL inner
fiber induces joint faithfulness in both a VARIABLE 17D prefix and
a VARIABLE recursive 18D generator. The entire original raw proof
prefix is reflected, not just its lower holonomy. -/
theorem nativeC60FHPrePairTransport_injective_of_inner
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word))
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F b c}
    (hinner : Function.Injective
      (fun r : (nativeC60DREighteenAssocSignature S F).Gen
          (nativeC60DRPackSeventeen S F p)
          (nativeC60DRPackSeventeen S F q) =>
        nativeC60DVTransportCompleteCode S F word
          (nativeC60DSCode S F r))) :
    Function.Injective
      (nativeC60FHPrePairTransport S F word
        (a := a) (b := b) (c := c) (p := p) (q := q)) := by
  rintro ⟨h, r⟩ ⟨k, s⟩ heq
  have hsrc :
      nativeC60DRPackSeventeen S F (.trans h p) =
        nativeC60DRPackSeventeen S F (.trans k p) := by
    apply nativeC60FFDVTransportEighteenObj_injective S F word hctx
    exact congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
      code.1) heq
  have hraw :
      NativeC60AXStep.trans h p = NativeC60AXStep.trans k p :=
    eq_of_heq (Sigma.mk.inj hsrc).2
  have hh : h = k := by
    injection hraw
  have hinnerImage := congrArg (nativeC60FHClosedPreInnerCode S F) heq
  change
      some (nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F r)) =
      some (nativeC60DVTransportCompleteCode S F word
        (nativeC60DSCode S F s)) at hinnerImage
  have hr : r = s := hinner (Option.some.inj hinnerImage)
  cases hr
  cases hh
  rfl

end GenuineRecursiveEighteenGenerators

#print axioms nativeC60FHClosedPostInnerCode
#print axioms nativeC60FHClosedPreInnerCode
#print axioms nativeC60FHPostPairTransport
#print axioms nativeC60FHPrePairTransport
#print axioms nativeC60FHPostPairTransport_injective_of_inner
#print axioms nativeC60FHPrePairTransport_injective_of_inner

end
end Kuu.F112.Physical
