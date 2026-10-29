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
  by
    rcases code with ⟨x, y, g⟩
    cases g with
    | assoc _ _ _ => exact none
    | post r h => exact some ⟨_, _, r⟩
    | pre h r => exact none

/-- The analogous full dependent inner code for pre-whiskering. -/
def nativeC60FHClosedPreInnerCode
    (code : NativeC60DVCompleteEighteenCode S F) :
    Option (NativeC60DVCompleteEighteenCode S F) :=
  by
    rcases code with ⟨x, y, g⟩
    cases g with
    | assoc _ _ _ => exact none
    | post r h => exact none
    | pre h r => exact some ⟨_, _, r⟩

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

/-!
# F112-P94D3FI — complete dependent generator induction

Close the FH recursive-inner hypothesis by induction on the ACTUAL
original DR 18D generator, against an independently variable COMPLETE
code. Both lower endpoints and every intermediate dependent boundary
may vary. FF reflects entire raw17D objects, FH extracts complete
recursive inner codes, and FG separates different constructors.

The resulting full-code injectivity is equivalent to the original
17D context-object injectivity, by FD's reflexive-associator witness.
FC lifts this exact criterion through pinned mathlib FreeGroup.map.
There is no claim that arbitrary physical singleton frames satisfy
this criterion. Original and context-closed target remain distinct;
DS no-go, original 19D geometric-filler obstruction, strict Kuu,
independent Kuu presentation, 107 roots and no Gray are preserved.
The complete preceding FH declarations remain unchanged.
-/

namespace Kuu.F112.Physical

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe u

section CompleteDependentGeneratorInduction

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A raw composite is decoded into BOTH entire original packed
subpaths, including its hidden intermediate proof-carrying object. -/
def nativeC60FIRawTransParts
    (obj : (nativeC60DREighteenLayer S F).Total) :
    Option ((nativeC60DREighteenLayer S F).Total ×
      (nativeC60DREighteenLayer S F).Total) := by
  rcases obj with ⟨⟨a, b⟩, p⟩
  cases p with
  | atom _ => exact none
  | refl _ => exact none
  | symm _ => exact none
  | trans p q => exact some
      (nativeC60DRPackSeventeen S F p, nativeC60DRPackSeventeen S F q)

/-- The entire original assoc code is determined by its raw source,
with ALL four endpoints and ALL three paths allowed to vary. -/
theorem nativeC60FIAssocCode_eq_of_source
    {a b c d a' b' c' d' : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60FGOriginal17Step S F a b)
    (g : NativeC60FGOriginal17Step S F b c)
    (h : NativeC60FGOriginal17Step S F c d)
    (f' : NativeC60FGOriginal17Step S F a' b')
    (g' : NativeC60FGOriginal17Step S F b' c')
    (h' : NativeC60FGOriginal17Step S F c' d')
    (hsrc : nativeC60DRPackSeventeen S F (.trans (.trans f g) h) =
      nativeC60DRPackSeventeen S F (.trans (.trans f' g') h')) :
    nativeC60DSCode S F (.assoc f g h) =
      nativeC60DSCode S F (.assoc f' g' h') := by
  have hparts :
      (nativeC60DRPackSeventeen S F (.trans f g),
        nativeC60DRPackSeventeen S F h) =
      (nativeC60DRPackSeventeen S F (.trans f' g'),
        nativeC60DRPackSeventeen S F h') :=
    Option.some.inj (congrArg (nativeC60FIRawTransParts S F) hsrc)
  have hfg :
      (nativeC60DRPackSeventeen S F f, nativeC60DRPackSeventeen S F g) =
      (nativeC60DRPackSeventeen S F f', nativeC60DRPackSeventeen S F g') :=
    Option.some.inj
      (congrArg (nativeC60FIRawTransParts S F) (Prod.mk.inj hparts).1)
  have hf := (Prod.mk.inj hfg).1
  have hg := (Prod.mk.inj hfg).2
  have hh := (Prod.mk.inj hparts).2
  have ha : a = a' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.1) hf
  have hb : b = b' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.2) hf
  have hc : c = c' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.2) hg
  have hd : d = d' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.2) hh
  cases ha
  cases hb
  cases hc
  cases hd
  have hff : f = f' := eq_of_heq (Sigma.mk.inj hf).2
  have hgg : g = g' := eq_of_heq (Sigma.mk.inj hg).2
  have hhh : h = h' := eq_of_heq (Sigma.mk.inj hh).2
  cases hff
  cases hgg
  cases hhh
  rfl

/-- Reassemble post codes after recovering a complete inner code
and complete suffix. No hidden source/target equality is assumed. -/
theorem nativeC60FIPostCode_congr
    {a b c a' b' c' : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F a b}
    {p' q' : NativeC60FGOriginal17Step S F a' b'}
    {r : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p) (nativeC60DRPackSeventeen S F q)}
    {s : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p') (nativeC60DRPackSeventeen S F q')}
    {h : NativeC60FGOriginal17Step S F b c}
    {k : NativeC60FGOriginal17Step S F b' c'}
    (hr : nativeC60DSCode S F r = nativeC60DSCode S F s)
    (hh : nativeC60DRPackSeventeen S F h = nativeC60DRPackSeventeen S F k) :
    nativeC60DSCode S F (.post r h) = nativeC60DSCode S F (.post s k) := by
  have hp := congrArg (fun code : NativeC60DSCompleteEighteenCode S F =>
    code.1) hr
  have hq := congrArg (fun code : NativeC60DSCompleteEighteenCode S F =>
    code.2.1) hr
  have ha : a = a' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.1) hp
  have hb : b = b' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.2) hp
  have hc : c = c' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.2) hh
  cases ha
  cases hb
  cases hc
  have hpp : p = p' := eq_of_heq (Sigma.mk.inj hp).2
  have hqq : q = q' := eq_of_heq (Sigma.mk.inj hq).2
  have hhk : h = k := eq_of_heq (Sigma.mk.inj hh).2
  cases hpp
  cases hqq
  cases hhk
  have hrs : r = s := nativeC60DSCode_injective S F hr
  cases hrs
  rfl

/-- Reassemble pre codes with variable complete inner boundary and
variable prefix. The endpoint substitutions precede fiber equality. -/
theorem nativeC60FIPreCode_congr
    {a b c a' b' c' : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FGOriginal17Step S F b c}
    {p' q' : NativeC60FGOriginal17Step S F b' c'}
    {r : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p) (nativeC60DRPackSeventeen S F q)}
    {s : (nativeC60DREighteenAssocSignature S F).Gen
      (nativeC60DRPackSeventeen S F p') (nativeC60DRPackSeventeen S F q')}
    {h : NativeC60FGOriginal17Step S F a b}
    {k : NativeC60FGOriginal17Step S F a' b'}
    (hr : nativeC60DSCode S F r = nativeC60DSCode S F s)
    (hh : nativeC60DRPackSeventeen S F h = nativeC60DRPackSeventeen S F k) :
    nativeC60DSCode S F (.pre h r) = nativeC60DSCode S F (.pre k s) := by
  have hp := congrArg (fun code : NativeC60DSCompleteEighteenCode S F =>
    code.1) hr
  have hq := congrArg (fun code : NativeC60DSCompleteEighteenCode S F =>
    code.2.1) hr
  have ha : a = a' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.1) hh
  have hb : b = b' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.1) hp
  have hc : c = c' :=
    congrArg (fun z : (nativeC60DREighteenLayer S F).Total => z.1.2) hp
  cases ha
  cases hb
  cases hc
  have hpp : p = p' := eq_of_heq (Sigma.mk.inj hp).2
  have hqq : q = q' := eq_of_heq (Sigma.mk.inj hq).2
  have hhk : h = k := eq_of_heq (Sigma.mk.inj hh).2
  cases hpp
  cases hqq
  cases hhk
  have hrs : r = s := nativeC60DSCode_injective S F hr
  cases hrs
  rfl

/-- Structural induction reflects each actual original generator
against an independently varying COMPLETE code. This closes FH's
inner-fiber obligation without assuming any generator faithfulness. -/
theorem nativeC60FICompleteCode_reflection
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word))
    {x y : (nativeC60DREighteenLayer S F).Total}
    (g : (nativeC60DREighteenAssocSignature S F).Gen x y) :
    ∀ code : NativeC60DSCompleteEighteenCode S F,
      nativeC60DVTransportCompleteCode S F word (nativeC60DSCode S F g) =
        nativeC60DVTransportCompleteCode S F word code →
      nativeC60DSCode S F g = code := by
  induction g with
  | assoc f g h =>
      rintro ⟨x', y', s⟩ heq
      cases s with
      | assoc f' g' h' =>
          apply nativeC60FIAssocCode_eq_of_source S F f g h f' g' h'
          apply nativeC60FFDVTransportEighteenObj_injective S F word hctx
          exact congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
            code.1) heq
      | post s k =>
          have htag := nativeC60FGCollision_preserves_constructor S F word heq
          cases htag
      | pre k s =>
          have htag := nativeC60FGCollision_preserves_constructor S F word heq
          cases htag
  | post r h ih =>
      rintro ⟨x', y', s⟩ heq
      cases s with
      | assoc f' g' h' =>
          have htag := nativeC60FGCollision_preserves_constructor S F word heq
          cases htag
      | post s k =>
          have hinner := congrArg (nativeC60FHClosedPostInnerCode S F) heq
          change
            some (nativeC60DVTransportCompleteCode S F word
              (nativeC60DSCode S F r)) =
            some (nativeC60DVTransportCompleteCode S F word
              (nativeC60DSCode S F s)) at hinner
          have hr := ih (nativeC60DSCode S F s) (Option.some.inj hinner)
          have hsrc := nativeC60FFDVTransportEighteenObj_injective S F word hctx
            (congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
              code.1) heq)
          have hparts := Option.some.inj
            (congrArg (nativeC60FIRawTransParts S F) hsrc)
          exact nativeC60FIPostCode_congr S F hr (Prod.mk.inj hparts).2
      | pre k s =>
          have htag := nativeC60FGCollision_preserves_constructor S F word heq
          cases htag
  | pre h r ih =>
      rintro ⟨x', y', s⟩ heq
      cases s with
      | assoc f' g' h' =>
          have htag := nativeC60FGCollision_preserves_constructor S F word heq
          cases htag
      | post s k =>
          have htag := nativeC60FGCollision_preserves_constructor S F word heq
          cases htag
      | pre k s =>
          have hinner := congrArg (nativeC60FHClosedPreInnerCode S F) heq
          change
            some (nativeC60DVTransportCompleteCode S F word
              (nativeC60DSCode S F r)) =
            some (nativeC60DVTransportCompleteCode S F word
              (nativeC60DSCode S F s)) at hinner
          have hr := ih (nativeC60DSCode S F s) (Option.some.inj hinner)
          have hsrc := nativeC60FFDVTransportEighteenObj_injective S F word hctx
            (congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
              code.1) heq)
          have hparts := Option.some.inj
            (congrArg (nativeC60FIRawTransParts S F) hsrc)
          exact nativeC60FIPreCode_congr S F hr (Prod.mk.inj hparts).1

/-- Full dependent code faithfulness from the single lower-object
gate. No extra recursive inner-generator assumption remains. -/
theorem nativeC60FICompleteCode_injective_of_context
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word)) :
    Function.Injective (nativeC60DVTransportCompleteCode S F word) := by
  intro a b heq
  rcases a with ⟨x, y, g⟩
  exact nativeC60FICompleteCode_reflection S F word hctx g b heq

/-- Exact criterion, not an unconditional frame assertion: full DV
18D codes are faithful precisely when the actual 17D object context is. -/
theorem nativeC60FICompleteCode_injective_iff_context
    (word : List Bool) :
    Function.Injective (nativeC60DVTransportCompleteCode S F word) ↔
      Function.Injective (nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word) := by
  constructor
  · intro hcode a b hab
    apply nativeC60FDAssocReflCode_injective S F
    exact hcode (nativeC60FDContextCollision_codes S F word hab)
  · exact nativeC60FICompleteCode_injective_of_context S F word

/-- Pinned mathlib's free-group reflection transfers the complete-code
criterion to ALL original ordered signed noncommutative 18D words. -/
theorem nativeC60FIFullFree_injective_iff_context
    (word : List Bool) :
    Function.Injective (nativeC60DVFullWordTransport S F word) ↔
      Function.Injective (nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word) :=
  (nativeC60FCTransport_injective_iff_code S F word).trans
    (nativeC60FICompleteCode_injective_iff_context S F word)

/-- Empty-context full noncommutative transport is faithful without
any physical-frame assumption; the closed target is still distinct. -/
theorem nativeC60FIFullFree_nil_injective :
    Function.Injective (nativeC60DVFullWordTransport S F []) := by
  apply (nativeC60FIFullFree_injective_iff_context S F []).mpr
  intro a b hab
  exact hab

/-- Faithfulness at EVERY finite AQ word is exactly the TWO actual
singleton 17D frame obligations. Their truth is not postulated here. -/
theorem nativeC60FIAllFullFree_injective_iff_singletons :
    (∀ word : List Bool,
      Function.Injective (nativeC60DVFullWordTransport S F word)) ↔
      Function.Injective ((nativeC60DRSeventeenFrame S F false).mapTotal) ∧
      Function.Injective ((nativeC60DRSeventeenFrame S F true).mapTotal) := by
  constructor
  · intro hall
    apply (nativeC60FEAllBCContexts_injective_iff_singletons
      (nativeC60DRSeventeenFrame S F)).mp
    intro word
    exact (nativeC60FIFullFree_injective_iff_context S F word).mp (hall word)
  · intro hframes word
    apply (nativeC60FIFullFree_injective_iff_context S F word).mpr
    exact (nativeC60FEAllBCContexts_injective_iff_singletons
      (nativeC60DRSeventeenFrame S F)).mpr hframes word

end CompleteDependentGeneratorInduction

#print axioms nativeC60FIRawTransParts
#print axioms nativeC60FIAssocCode_eq_of_source
#print axioms nativeC60FIPostCode_congr
#print axioms nativeC60FIPreCode_congr
#print axioms nativeC60FICompleteCode_reflection
#print axioms nativeC60FICompleteCode_injective_of_context
#print axioms nativeC60FICompleteCode_injective_iff_context
#print axioms nativeC60FIFullFree_injective_iff_context
#print axioms nativeC60FIFullFree_nil_injective
#print axioms nativeC60FIAllFullFree_injective_iff_singletons

end
end Kuu.F112.Physical
