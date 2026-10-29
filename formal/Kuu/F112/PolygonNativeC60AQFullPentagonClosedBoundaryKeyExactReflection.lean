import Kuu.F112.PolygonNativeC60AQFullPentagonBoundaryKeyFiniteNormalGate

/-!
# F112-P94D3FT — TRUE 18D closed-target boundary-key reflection

FS defined a proof-bearing boundary-key on genuine context-CLOSED 18D
dependent codes, retaining the ENTIRE post/pre/.../assoc constructor
spine, source and target packed raw17D paths, and fully dependent
post/pre inner 18D codes. FS proved that genuine DV image collisions
PRESERVE this key; the reverse was explicitly not asserted.

FT closes that gap at the ACTUAL separately declared closed 18D
target, by syntactic dependent constructor reflection:
* an assoc code is determined by the complete nested raw17D
  trans(trans f g) h stored in its true source object;
* a post code is determined by the entire inner 18D code (from the
  FS/FH postInner field), and its genuine 17D suffix (from its source
  raw trans);
* a pre code is determined analogously by the inner 18D code and
  its genuine 17D prefix;
* distinct constructors have distinct original COMPLETE spines.

This proves unconditional injectivity of the FS closed code
boundary-key, not an assumption that arbitrary ORIGINAL C60 context
maps are faithful. Hence true original complete DV code images
coincide IFF their FULL observed dependent boundary keys coincide,
and the original noncommutative DV whole kernel is exactly the normal
closure of ALL key-equal original two-letter differences. Unique
receiver descent onto the ACTUAL target IMAGE likewise needs ONLY
key-equal generator compatibility.

Important: equality of keys determines the same RECEIVING 18D
code, NOT equality of original raw17D source witnesses. The physical
old FJ nonfaithfulness remains. Actual finite/minimal independent
kernel presentations and true geometric 19D fillers are NOT proved.
Preserve DS/FJ/FN old no-go, distinct FK/FL/FM presentations,
107 public roots, strict Kuu primary / independent Kuu presentation,
pinned mathlib and Lean, no Gray and append-only operation.
No new axioms, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v

section ClosedDependentGeneratorReconstruction

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

abbrev NativeC60FTClosed17Step
    (a b : (nativeC60DQSeventeenLayer S F).Total) : Type u :=
  NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b

/-- Retain every dependent endpoint and the original closed-target
generator syntax in its complete receiving 18D code. -/
def nativeC60FTClosedCode
    {x y : (nativeC60DVClosedEighteenLayer S F).Total}
    (g : (nativeC60DVClosedEighteenSignature S F).Gen x y) :
    NativeC60DVCompleteEighteenCode S F :=
  ⟨x, y, g⟩

/-- Packing a receiving 18D generator code NEVER identifies
distinct generators at fixed exact dependent endpoints. -/
theorem nativeC60FTClosedCode_injective
    {x y : (nativeC60DVClosedEighteenLayer S F).Total} :
    Function.Injective (fun (g : (nativeC60DVClosedEighteenSignature S F).Gen x y) =>
      nativeC60FTClosedCode S F g) := by
  intro g h heq
  have hpair : (⟨y, g⟩ : Σ z : (nativeC60DVClosedEighteenLayer S F).Total,
      (nativeC60DVClosedEighteenSignature S F).Gen x z) =
      ⟨y, h⟩ := eq_of_heq (Sigma.mk.inj heq).2
  exact eq_of_heq (Sigma.mk.inj hpair).2

/-- Decode the true receiving RAW 17D trans node into both
complete packed paths, including the original lower object. -/
def nativeC60FTClosedRawTransParts
    (obj : (nativeC60DVClosedEighteenLayer S F).Total) :
    Option ((nativeC60DVClosedEighteenLayer S F).Total ×
      (nativeC60DVClosedEighteenLayer S F).Total) := by
  rcases obj with ⟨⟨a, b⟩, p⟩
  cases p with
  | atom _ => exact none
  | refl _ => exact none
  | symm _ => exact none
  | trans p q =>
      exact some (nativeC60DVPackClosedSeventeen S F p,
        nativeC60DVPackClosedSeventeen S F q)

/-- ACTUAL closed-target primitive assoc is completely determined
by its nested source raw17D proof, without any C60 frame hypothesis. -/
theorem nativeC60FTClosedAssocCode_eq_of_source
    {a b c d a' b' c' d' : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60FTClosed17Step S F a b)
    (g : NativeC60FTClosed17Step S F b c)
    (h : NativeC60FTClosed17Step S F c d)
    (f' : NativeC60FTClosed17Step S F a' b')
    (g' : NativeC60FTClosed17Step S F b' c')
    (h' : NativeC60FTClosed17Step S F c' d')
    (hsrc : nativeC60DVPackClosedSeventeen S F (.trans (.trans f g) h) =
      nativeC60DVPackClosedSeventeen S F (.trans (.trans f' g') h')) :
    nativeC60FTClosedCode S F (.assoc f g h) =
      nativeC60FTClosedCode S F (.assoc f' g' h') := by
  have hparts :
      (nativeC60DVPackClosedSeventeen S F (.trans f g),
        nativeC60DVPackClosedSeventeen S F h) =
      (nativeC60DVPackClosedSeventeen S F (.trans f' g'),
        nativeC60DVPackClosedSeventeen S F h') :=
    Option.some.inj (congrArg (nativeC60FTClosedRawTransParts S F) hsrc)
  have hfg :
      (nativeC60DVPackClosedSeventeen S F f,
        nativeC60DVPackClosedSeventeen S F g) =
      (nativeC60DVPackClosedSeventeen S F f',
        nativeC60DVPackClosedSeventeen S F g') :=
    Option.some.inj
      (congrArg (nativeC60FTClosedRawTransParts S F) (Prod.mk.inj hparts).1)
  have hf := (Prod.mk.inj hfg).1
  have hg := (Prod.mk.inj hfg).2
  have hh := (Prod.mk.inj hparts).2
  have ha : a = a' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.1) hf
  have hb : b = b' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.2) hf
  have hc : c = c' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.2) hg
  have hd : d = d' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.2) hh
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

/-- Reconstruct the entire receiving post generator from its exact
inner complete code and complete raw17D suffix, with variable
dependent boundaries: no frame injectivity is assumed. -/
theorem nativeC60FTClosedPostCode_congr
    {a b c a' b' c' : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FTClosed17Step S F a b}
    {p' q' : NativeC60FTClosed17Step S F a' b'}
    {r : (nativeC60DVClosedEighteenSignature S F).Gen
      (nativeC60DVPackClosedSeventeen S F p)
      (nativeC60DVPackClosedSeventeen S F q)}
    {s : (nativeC60DVClosedEighteenSignature S F).Gen
      (nativeC60DVPackClosedSeventeen S F p')
      (nativeC60DVPackClosedSeventeen S F q')}
    {h : NativeC60FTClosed17Step S F b c}
    {k : NativeC60FTClosed17Step S F b' c'}
    (hr : nativeC60FTClosedCode S F r = nativeC60FTClosedCode S F s)
    (hh : nativeC60DVPackClosedSeventeen S F h =
      nativeC60DVPackClosedSeventeen S F k) :
    nativeC60FTClosedCode S F (.post r h) =
      nativeC60FTClosedCode S F (.post s k) := by
  have hp := congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
    code.1) hr
  have hq := congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
    code.2.1) hr
  have ha : a = a' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.1) hp
  have hb : b = b' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.2) hp
  have hc : c = c' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.2) hh
  cases ha
  cases hb
  cases hc
  have hpp : p = p' := eq_of_heq (Sigma.mk.inj hp).2
  have hqq : q = q' := eq_of_heq (Sigma.mk.inj hq).2
  have hhk : h = k := eq_of_heq (Sigma.mk.inj hh).2
  cases hpp
  cases hqq
  cases hhk
  have hrs : r = s := nativeC60FTClosedCode_injective S F hr
  cases hrs
  rfl

/-- Reconstruct the entire receiving pre generator from its exact
inner complete code and raw17D prefix: all dependent endpoints vary. -/
theorem nativeC60FTClosedPreCode_congr
    {a b c a' b' c' : (nativeC60DQSeventeenLayer S F).Total}
    {p q : NativeC60FTClosed17Step S F b c}
    {p' q' : NativeC60FTClosed17Step S F b' c'}
    {r : (nativeC60DVClosedEighteenSignature S F).Gen
      (nativeC60DVPackClosedSeventeen S F p)
      (nativeC60DVPackClosedSeventeen S F q)}
    {s : (nativeC60DVClosedEighteenSignature S F).Gen
      (nativeC60DVPackClosedSeventeen S F p')
      (nativeC60DVPackClosedSeventeen S F q')}
    {h : NativeC60FTClosed17Step S F a b}
    {k : NativeC60FTClosed17Step S F a' b'}
    (hr : nativeC60FTClosedCode S F r = nativeC60FTClosedCode S F s)
    (hh : nativeC60DVPackClosedSeventeen S F h =
      nativeC60DVPackClosedSeventeen S F k) :
    nativeC60FTClosedCode S F (.pre h r) =
      nativeC60FTClosedCode S F (.pre k s) := by
  have hp := congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
    code.1) hr
  have hq := congrArg (fun code : NativeC60DVCompleteEighteenCode S F =>
    code.2.1) hr
  have ha : a = a' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.1) hh
  have hb : b = b' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.1) hp
  have hc : c = c' :=
    congrArg (fun z : (nativeC60DVClosedEighteenLayer S F).Total => z.1.2) hp
  cases ha
  cases hb
  cases hc
  have hpp : p = p' := eq_of_heq (Sigma.mk.inj hp).2
  have hqq : q = q' := eq_of_heq (Sigma.mk.inj hq).2
  have hhk : h = k := eq_of_heq (Sigma.mk.inj hh).2
  cases hpp
  cases hqq
  cases hhk
  have hrs : r = s := nativeC60FTClosedCode_injective S F hr
  cases hrs
  rfl

/-- Main FT target theorem. The complete boundary-key constructed
at FS is faithful on the ACTUAL separately context-closed 18D
dependent generator alphabet, without ANY injectivity hypothesis
on the original C60 frame. -/
theorem nativeC60FTClosedObservedKey_injective :
    Function.Injective (nativeC60FSObservedKey S F) := by
  rintro ⟨x, y, r⟩ ⟨x', y', s⟩ heq
  cases r with
  | assoc f g h =>
      cases s with
      | assoc f' g' h' =>
          apply nativeC60FTClosedAssocCode_eq_of_source S F
            f g h f' g' h'
          exact congrArg
            (fun k : NativeC60FSBoundaryKey S F => k.source) heq
      | post s k =>
          have hspine := congrArg
            (fun k : NativeC60FSBoundaryKey S F => k.spine) heq
          cases hspine
      | pre k s =>
          have hspine := congrArg
            (fun k : NativeC60FSBoundaryKey S F => k.spine) heq
          cases hspine
  | post r h =>
      cases s with
      | assoc f' g' h' =>
          have hspine := congrArg
            (fun k : NativeC60FSBoundaryKey S F => k.spine) heq
          cases hspine
      | post s k =>
          have hinner := congrArg
            (fun k : NativeC60FSBoundaryKey S F => k.postInner) heq
          change some (nativeC60FTClosedCode S F r) =
            some (nativeC60FTClosedCode S F s) at hinner
          have hr := Option.some.inj hinner
          have hsrc :
              (nativeC60FTClosedCode S F (.post r h)).1 =
                (nativeC60FTClosedCode S F (.post s k)).1 :=
            congrArg (fun z : NativeC60FSBoundaryKey S F => z.source) heq
          have hparts := Option.some.inj
            (congrArg (nativeC60FTClosedRawTransParts S F) hsrc)
          exact nativeC60FTClosedPostCode_congr S F hr (Prod.mk.inj hparts).2
      | pre k s =>
          have hspine := congrArg
            (fun k : NativeC60FSBoundaryKey S F => k.spine) heq
          cases hspine
  | pre h r =>
      cases s with
      | assoc f' g' h' =>
          have hspine := congrArg
            (fun k : NativeC60FSBoundaryKey S F => k.spine) heq
          cases hspine
      | post s k =>
          have hspine := congrArg
            (fun k : NativeC60FSBoundaryKey S F => k.spine) heq
          cases hspine
      | pre k s =>
          have hinner := congrArg
            (fun k : NativeC60FSBoundaryKey S F => k.preInner) heq
          change some (nativeC60FTClosedCode S F r) =
            some (nativeC60FTClosedCode S F s) at hinner
          have hr := Option.some.inj hinner
          have hsrc :
              (nativeC60FTClosedCode S F (.pre h r)).1 =
                (nativeC60FTClosedCode S F (.pre k s)).1 :=
            congrArg (fun z : NativeC60FSBoundaryKey S F => z.source) heq
          have hparts := Option.some.inj
            (congrArg (nativeC60FTClosedRawTransParts S F) hsrc)
          exact nativeC60FTClosedPreCode_congr S F hr (Prod.mk.inj hparts).1

end ClosedDependentGeneratorReconstruction

section ExactOriginalImageFiberBoundaryKeys

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The former FS NECESSARY boundary-key criterion is now an
UNCONDITIONAL IFF for the ACTUAL dependent 18D transport into
its separately context-closed target. It is NOT a statement of
injectivity on original raw17D source proofs. -/
theorem nativeC60FTFullCode_image_eq_iff_boundaryKey_eq
    (word : List Bool)
    (a b : NativeC60DSCompleteEighteenCode S F) :
    nativeC60DVTransportCompleteCode S F word a =
      nativeC60DVTransportCompleteCode S F word b ↔
    nativeC60FSSourceKey S F word a =
      nativeC60FSSourceKey S F word b := by
  constructor
  · exact nativeC60FSSourceKey_eq_of_collision S F word
  · exact nativeC60FTClosedObservedKey_injective S F

/-- Key-only collision pair presentation of ORIGINAL 18D code
letters: no extra input transport-equality premise is needed. -/
def nativeC60FTKeyEqualPairs (word : List Bool) :
    Set (NativeC60DTFullFree S F × NativeC60DTFullFree S F) :=
  {pair | ∃ a b : NativeC60DSCompleteEighteenCode S F,
    nativeC60FSSourceKey S F word a =
      nativeC60FSSourceKey S F word b ∧
    pair = (FreeGroup.of a, FreeGroup.of b)}

/-- Every original full-code DV collision and ONLY that collision
is now captured by the original source code's observed real
Type-valued boundary KEY equality. -/
theorem nativeC60FTFullPairs_eq_keyEqualPairs (word : List Bool) :
    nativeC60FOFiberPairs (nativeC60DVTransportCompleteCode S F word) =
      nativeC60FTKeyEqualPairs S F word := by
  ext p
  constructor
  · rintro ⟨a, b, hab, rfl⟩
    exact ⟨a, b,
      (nativeC60FTFullCode_image_eq_iff_boundaryKey_eq S F word a b).mp hab,
      rfl⟩
  · rintro ⟨a, b, hkey, rfl⟩
    exact ⟨a, b,
      (nativeC60FTFullCode_image_eq_iff_boundaryKey_eq S F word a b).mpr hkey,
      rfl⟩

/-- FT sharpens FS/FO: the WHOLE actual ORIGINAL noncommutative 18D
transport kernel is generated by key-equality signed two-letter
relations WITHOUT any residual code-image-equality guard. -/
theorem nativeC60FTFullKernel_eq_keyEqualNormalClosure (word : List Bool) :
    (nativeC60DVFullWordTransport S F word).ker =
      nativeC60DTNormalClosure (nativeC60FTKeyEqualPairs S F word) := by
  calc
    (nativeC60DVFullWordTransport S F word).ker =
        nativeC60FOFullKernelNormalClosure S F word :=
      nativeC60FOFullTransport_kernel_eq_normalClosure S F word
    _ = nativeC60DTNormalClosure (nativeC60FTKeyEqualPairs S F word) := by
      change nativeC60DTNormalClosure
        (nativeC60FOFiberPairs (nativeC60DVTransportCompleteCode S F word)) =
          nativeC60DTNormalClosure (nativeC60FTKeyEqualPairs S F word)
      rw [nativeC60FTFullPairs_eq_keyEqualPairs S F word]

/-- Exactly the KEY equality, with no separately required code
transport equality, characterizes original 18D group receiver
factorization uniquely on the TRUE DV target image subgroup. -/
theorem nativeC60FTReceiver_keyEqual_iff
    {G : Type v} [Group G]
    (word : List Bool) (receiver : NativeC60DTFullFree S F →* G) :
    (∃! induced : NativeC60FPFullImage S F word →* G,
      induced.comp (nativeC60DVFullWordTransport S F word).rangeRestrict =
        receiver) ↔
      ∀ a b : NativeC60DSCompleteEighteenCode S F,
        nativeC60FSSourceKey S F word a =
          nativeC60FSSourceKey S F word b →
        receiver (FreeGroup.of a) = receiver (FreeGroup.of b) := by
  rw [nativeC60FPFullReceiver_image_unique_iff S F word receiver]
  constructor
  · intro hall a b hkey
    exact hall a b
      ((nativeC60FTFullCode_image_eq_iff_boundaryKey_eq S F word a b).mpr hkey)
  · intro hkeys a b hab
    exact hkeys a b
      ((nativeC60FTFullCode_image_eq_iff_boundaryKey_eq S F word a b).mp hab)

/-- The FQ chosen source-fiber ROOT has identical complete dependent
boundary key; conversely the key determines exactly the ACTUAL
target code fiber, so no stronger original raw17D equality is implied. -/
theorem nativeC60FTFullRoot_key_iff_image
    (word : List Bool)
    (a b : NativeC60DSCompleteEighteenCode S F) :
    nativeC60FSSourceKey S F word a =
      nativeC60FSSourceKey S F word b ↔
      nativeC60FQLetterRoot
          (nativeC60DVTransportCompleteCode S F word) a =
        nativeC60FQLetterRoot
          (nativeC60DVTransportCompleteCode S F word) b := by
  constructor
  · intro hab
    exact nativeC60FQLetterRoot_eq_of_image_eq
      (nativeC60DVTransportCompleteCode S F word)
      ((nativeC60FTFullCode_image_eq_iff_boundaryKey_eq S F word a b).mpr hab)
  · intro hroot
    have ha := nativeC60FQLetterRoot_image
      (nativeC60DVTransportCompleteCode S F word) a
    have hb := nativeC60FQLetterRoot_image
      (nativeC60DVTransportCompleteCode S F word) b
    have hab : nativeC60DVTransportCompleteCode S F word a =
        nativeC60DVTransportCompleteCode S F word b := by
      calc
        nativeC60DVTransportCompleteCode S F word a =
          nativeC60DVTransportCompleteCode S F word
            (nativeC60FQLetterRoot
              (nativeC60DVTransportCompleteCode S F word) a) := ha.symm
        _ = nativeC60DVTransportCompleteCode S F word
            (nativeC60FQLetterRoot
              (nativeC60DVTransportCompleteCode S F word) b) := by
                rw [hroot]
        _ = nativeC60DVTransportCompleteCode S F word b := hb
    exact (nativeC60FTFullCode_image_eq_iff_boundaryKey_eq S F word a b).mp hab

end ExactOriginalImageFiberBoundaryKeys

#print axioms nativeC60FTClosedCode_injective
#print axioms nativeC60FTClosedRawTransParts
#print axioms nativeC60FTClosedAssocCode_eq_of_source
#print axioms nativeC60FTClosedPostCode_congr
#print axioms nativeC60FTClosedPreCode_congr
#print axioms nativeC60FTClosedObservedKey_injective
#print axioms nativeC60FTFullCode_image_eq_iff_boundaryKey_eq
#print axioms nativeC60FTFullPairs_eq_keyEqualPairs
#print axioms nativeC60FTFullKernel_eq_keyEqualNormalClosure
#print axioms nativeC60FTReceiver_keyEqual_iff
#print axioms nativeC60FTFullRoot_key_iff_image

end
end Kuu.F112.Physical
