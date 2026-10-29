import Kuu.F112.PolygonNativeC60AQFullPentagonActualTransportSeparation
import Mathlib.GroupTheory.FreeGroup.Basic

/-!
# F112-P94D3FC — exact complete typed-code fiber and free-word kernel gate

DV transports every ORIGINAL dependent C60 18D generator code into the
distinct, explicitly context-closed 18D generator alphabet. The
original code and the target code retain full typed endpoints, but an
arbitrary C60 frame is NOT assumed injective on all underlying objects.
Therefore a blanket assertion of code-map or whole FreeGroup
injectivity would be unjustified.

FC proves the EXACT criterion in the pinned mathlib free-group API:
* DV's actual complete-code transport equals FreeGroup.map on the
  entire typed generator-code function, not merely a scalar observer.
* The complete group hom is injective IFF the true dependent code
  transport is injective.
* For EVERY finite signed complete-code word the target is the exact
  signed word of transported codes, with chronological order intact;
  target-word reduction is thus the precise kernel membership test.
* If distinct original dependent codes collide after context
  transport, the explicit original noncommutative two-letter
  difference of those codes is NONIDENTITY in the source FreeGroup
  and maps to the identity in the target.
* Conversely ANY nontrivial group-kernel element forces a collision
  of two distinct original complete dependent codes. Thus failure of
  global faithfulness has a concrete code-fiber certificate.

No global code injectivity, frame injectivity, geometric C60 19D
filler, or entire-kernel normal-closure classification is assumed or
claimed by this file. Source and closed target are different groups.
Preserve DS complete-evidence no-go, 14D--18D Type-valued history,
strict Kuu primary, independent Kuu as a presentation, 107 roots,
no Gray, pinned Lean/mathlib, append-only/tighten-only/same-root.
No new axiom, sorry, or admit.
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

section CompleteTypedCodeFiber

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The actual 18D dependent full-code hom is exactly mathlib's
free-group functorial map of the explicit DV code function. This is
NOT an arbitrary hom invented to force a desired property. -/
theorem nativeC60FCTransport_eq_freeMap (word : List Bool) :
    nativeC60DVFullWordTransport S F word =
      FreeGroup.map (nativeC60DVTransportCompleteCode S F word) := by
  rw [FreeGroup.map_eq_lift]
  rfl

/-- MAIN FC: genuine DV full 18D word transport is injective
PRECISELY WHEN its explicitly constructed complete dependent code
function is injective. Neither condition is asserted unconditionally.
The forward direction uses independent FreeGroup.of injectivity;
the reverse direction uses pinned FreeGroup.map_injective. -/
theorem nativeC60FCTransport_injective_iff_code
    (word : List Bool) :
    Function.Injective (nativeC60DVFullWordTransport S F word) ↔
      Function.Injective
        (nativeC60DVTransportCompleteCode S F word) := by
  constructor
  · intro hinj a b hab
    apply FreeGroup.of_injective
    apply hinj
    rw [nativeC60FCTransport_eq_freeMap S F word]
    simpa only [FreeGroup.map.of] using
      (congrArg (fun z : NativeC60DVCompleteEighteenCode S F =>
        (FreeGroup.of z : NativeC60DVClosedFullFree S F)) hab)
  · intro hinj
    rw [nativeC60FCTransport_eq_freeMap S F word]
    exact FreeGroup.map_injective hinj

/-- Exact complete-code transport for ANY finite ORIGINAL signed
18D word: the map acts separately on each ORIGINAL typed generator,
preserving sign and order before any legitimate free reduction. -/
theorem nativeC60FCTransport_signedWord
    (word : List Bool)
    (xs : List (NativeC60DSCompleteEighteenCode S F × Bool)) :
    (nativeC60DVFullWordTransport S F word) (FreeGroup.mk xs) =
      FreeGroup.mk (xs.map (fun z =>
        (nativeC60DVTransportCompleteCode S F word z.1, z.2))) := by
  rw [nativeC60FCTransport_eq_freeMap S F word]
  exact FreeGroup.map.mk

/-- Exact arbitrary signed original free-word KERNEL TEST. It
inspects the entire target typed signed free word, not the sign sum,
word length, scalar shadow, or any chosen 19D quotient. -/
theorem nativeC60FCTransport_signedWord_mem_ker_iff
    (word : List Bool)
    (xs : List (NativeC60DSCompleteEighteenCode S F × Bool)) :
    FreeGroup.mk xs ∈ (nativeC60DVFullWordTransport S F word).ker ↔
      FreeGroup.mk (xs.map (fun z =>
        (nativeC60DVTransportCompleteCode S F word z.1, z.2))) =
        (1 : NativeC60DVClosedFullFree S F) := by
  constructor
  · intro h
    have hz := MonoidHom.mem_ker.mp h
    simpa only [nativeC60FCTransport_signedWord S F word xs] using hz
  · intro h
    apply MonoidHom.mem_ker.mpr
    simpa only [nativeC60FCTransport_signedWord S F word xs] using h

/-- A candidate two-code fiber collision is represented in the
ORIGINAL complete-dependent-code free group by its genuinely
noncommutative two-letter ratio. -/
def nativeC60FCCodeFiberDefect
    (a b : NativeC60DSCompleteEighteenCode S F) :
    NativeC60DTFullFree S F :=
  FreeGroup.of a * (FreeGroup.of b)⁻¹

/-- Distinct original complete Type-valued codes have a NONTRIVIAL
difference word in the unmodified universal FreeGroup. -/
theorem nativeC60FCCodeFiberDefect_ne_one
    {a b : NativeC60DSCompleteEighteenCode S F}
    (hne : a ≠ b) :
    nativeC60FCCodeFiberDefect S F a b ≠ 1 := by
  intro h
  change (FreeGroup.of a : NativeC60DTFullFree S F) *
    (FreeGroup.of b)⁻¹ = 1 at h
  exact hne (FreeGroup.of_injective (eq_of_mul_inv_eq_one h))

/-- An ACTUAL complete-code collision after the explicit DV context
map creates an original nontrivial word IN THE KERNEL of that actual
full 18D group hom. -/
theorem nativeC60FCCodeFiberDefect_maps_one
    (word : List Bool)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (hab : nativeC60DVTransportCompleteCode S F word a =
      nativeC60DVTransportCompleteCode S F word b) :
    (nativeC60DVFullWordTransport S F word)
      (nativeC60FCCodeFiberDefect S F a b) = 1 := by
  change (nativeC60DVFullWordTransport S F word)
    (FreeGroup.of a * (FreeGroup.of b)⁻¹) = 1
  rw [map_mul, map_inv,
      nativeC60DVFullWordTransport_of S F word a,
      nativeC60DVFullWordTransport_of S F word b, hab]
  exact mul_inv_cancel _

/-- The whole DV free evidence is nonfaithful IFF a pair of
DIFFERENT ORIGINAL dependent typed 18D codes collides in the
explicit context target. This is an existential equivalence, not an
unconditional assertion that such a collision exists. -/
theorem nativeC60FCTransport_not_injective_iff_collision
    (word : List Bool) :
    (¬ Function.Injective (nativeC60DVFullWordTransport S F word)) ↔
      ∃ a b : NativeC60DSCompleteEighteenCode S F,
        a ≠ b ∧
        nativeC60DVTransportCompleteCode S F word a =
          nativeC60DVTransportCompleteCode S F word b := by
  classical
  constructor
  · intro hno
    by_contra hnone
    have hc : Function.Injective
        (nativeC60DVTransportCompleteCode S F word) := by
      intro a b hab
      by_contra hne
      exact hnone ⟨a, b, hne, hab⟩
    exact hno ((nativeC60FCTransport_injective_iff_code
      S F word).mpr hc)
  · rintro ⟨a, b, hne, hab⟩ hinj
    exact hne ((nativeC60FCTransport_injective_iff_code
      S F word).mp hinj hab)

/-- COMPLETE FINITE FIBER OBSTRUCTION:
an arbitrary nontrivial original signed complete free word is killed
by the ACTUAL DV map IFF at least one pair of distinct ORIGINAL
dependent 18D codes has the same target context image. The forward
implication detects SOME code fiber collision; it does not claim the
witness word must have length two. The reverse implication explicitly
constructs a nontrivial two-letter kernel element. -/
theorem nativeC60FCNontrivialKernel_iff_code_collision
    (word : List Bool) :
    (∃ z : NativeC60DTFullFree S F,
      z ≠ 1 ∧ (nativeC60DVFullWordTransport S F word) z = 1) ↔
      ∃ a b : NativeC60DSCompleteEighteenCode S F,
        a ≠ b ∧
        nativeC60DVTransportCompleteCode S F word a =
          nativeC60DVTransportCompleteCode S F word b := by
  constructor
  · rintro ⟨z, hnon, hzero⟩
    apply (nativeC60FCTransport_not_injective_iff_collision S F word).mp
    intro hinj
    apply hnon
    apply hinj
    simpa only [map_one] using hzero
  · rintro ⟨a, b, hne, hab⟩
    exact ⟨nativeC60FCCodeFiberDefect S F a b,
      nativeC60FCCodeFiberDefect_ne_one S F hne,
      nativeC60FCCodeFiberDefect_maps_one S F word hab⟩

/-- A positive hypothesis of exact code-fiber faithfulness gives a
global original signed 18D free-word equality reflection. This is
a conditional honest preservation statement, not a claim that all
arbitrary C60 frame contexts satisfy the hypothesis. -/
theorem nativeC60FCFullWord_eq_of_transport_eq
    (word : List Bool)
    (hcodes : Function.Injective
      (nativeC60DVTransportCompleteCode S F word))
    (x y : NativeC60DTFullFree S F)
    (heq : (nativeC60DVFullWordTransport S F word) x =
      (nativeC60DVFullWordTransport S F word) y) :
    x = y :=
  (nativeC60FCTransport_injective_iff_code S F word).mpr hcodes heq

end CompleteTypedCodeFiber

#print axioms nativeC60FCTransport_eq_freeMap
#print axioms nativeC60FCTransport_injective_iff_code
#print axioms nativeC60FCTransport_signedWord
#print axioms nativeC60FCTransport_signedWord_mem_ker_iff
#print axioms nativeC60FCCodeFiberDefect_ne_one
#print axioms nativeC60FCCodeFiberDefect_maps_one
#print axioms nativeC60FCTransport_not_injective_iff_collision
#print axioms nativeC60FCNontrivialKernel_iff_code_collision
#print axioms nativeC60FCFullWord_eq_of_transport_eq

end
end Kuu.F112.Physical
