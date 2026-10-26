import Kuu.F112.PolygonNativeC60TypedSignedCancellation

/-!
# F112-P94D3CB — fully typed signed reduced-word reflection

CA constructed genuine arbitrary finite signed BC 16D paths and proved that
every typed adjacent inverse cancellation is sound in the EXISTING selected
no-extra-relations strict Kuu quotient under any finite AQ context.

CB removes BZ's fixed intermediate 15D skeleton restriction for ALL
ALREADY REDUCED SIGNED higher paths (not merely positive paths).
The entire provenance code of a BC generator contains its original lower
source, lower target, primitive 16D proof and finite frame prefix. Thus
equal code letters determine their original dependent intermediate objects
even when two candidate paths initially have different skeletons.

The proof has two independent parts:
(1) complete signed code lists are injective on true DEPENDENT typed paths,
    with no a priori assumption of equal intermediate 15D objects;
(2) Mathlib FreeGroup.Red Church–Rosser uniqueness identifies two
    already-reduced signed code lists whenever their free words agree.
The existing BW invariant translates strict equality into free equality.
Consequently all-finite-AQ strict equality reflects the EXACT typed path
for arbitrary-length signed REDUCED paths with common original endpoints.

A second result gives an exact necessary-and-sufficient reflection theorem
for general paths once actual typed reductions to reduced paths are
supplied. The existence of such typed normalizations for EVERY arbitrary
path remains the next separate global typed free-groupoid lifting problem;
CB makes no circular assumption that free-group equality alone constructs
the missing endpoint-preserving reductions.

No new axioms, sorry/admit, Gray, geometric 16-cell, universal horizontal
Peiffer interchange, strict 3/n-category or alteration of public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

/-- A signed BC letter determines the original LOWER source 15D object,
using its actual contextual prefix and the generator's indexed witness. -/
theorem nativeC60CBGen_source
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    a = nativeC60BCContextTotal F
      (nativeC60BVGeneratorCode S F g).1
      (nativeC60BVGeneratorCode S F g).2.1 := by
  rcases g with ⟨steps, x, y, ⟨gen, hx, hy⟩⟩
  exact hx

/-- The same complete code determines the original LOWER target
15D object. In negative orientation this becomes the next step's source. -/
theorem nativeC60CBGen_target
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    b = nativeC60BCContextTotal F
      (nativeC60BVGeneratorCode S F g).1
      (nativeC60BVGeneratorCode S F g).2.2.1 := by
  rcases g with ⟨steps, x, y, ⟨gen, hx, hy⟩⟩
  exact hy

/-- Complete signed generator-code lists determine the ENTIRE original
dependent higher path. This holds without any fixed intermediate-object
skeleton and works across both orientations and all finite lengths.
The endpoints of the whole paths are fixed, not their interiors. -/
theorem nativeC60CBChainCodes_eq_implies_eq
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    ∀ {a b : L.Total} (p q : NativeC60CASignedChain S F a b),
      nativeC60CAChainSignedCodes S F p =
        nativeC60CAChainSignedCodes S F q → p = q := by
  intro a b p
  induction p with
  | nil _ =>
      intro q hcodes
      cases q with
      | nil _ => rfl
      | pos _ _ => cases hcodes
      | neg _ _ => cases hcodes
  | pos g tail ih =>
      intro q hcodes
      cases q with
      | nil _ =>
          cases hcodes
      | neg g' rest =>
          change (nativeC60BVGeneratorCode S F g, true) ::
              nativeC60CAChainSignedCodes S F tail =
            (nativeC60BVGeneratorCode S F g', false) ::
              nativeC60CAChainSignedCodes S F rest at hcodes
          injection hcodes with hhead htail
          have hs : (true : Bool) = false := congrArg Prod.snd hhead
          cases hs
      | pos g' rest =>
          change (nativeC60BVGeneratorCode S F g, true) ::
              nativeC60CAChainSignedCodes S F tail =
            (nativeC60BVGeneratorCode S F g', true) ::
              nativeC60CAChainSignedCodes S F rest at hcodes
          injection hcodes with hhead htail
          have hc : nativeC60BVGeneratorCode S F g =
              nativeC60BVGeneratorCode S F g' := congrArg Prod.fst hhead
          have hmid :=
            (nativeC60CBGen_target S F g).trans
              ((congrArg
                (fun code : NativeC60BVGeneratorCode S =>
                  nativeC60BCContextTotal F code.1 code.2.2.1)
                hc).trans (nativeC60CBGen_target S F g').symm)
          cases hmid
          have hg : g = g' :=
            nativeC60BVGeneratorCode_injective S F hc
          cases hg
          have hrest : tail = rest := ih rest htail
          cases hrest
          rfl
  | neg g tail ih =>
      intro q hcodes
      cases q with
      | nil _ =>
          cases hcodes
      | pos g' rest =>
          change (nativeC60BVGeneratorCode S F g, false) ::
              nativeC60CAChainSignedCodes S F tail =
            (nativeC60BVGeneratorCode S F g', true) ::
              nativeC60CAChainSignedCodes S F rest at hcodes
          injection hcodes with hhead htail
          have hs : (false : Bool) = true := congrArg Prod.snd hhead
          cases hs
      | neg g' rest =>
          change (nativeC60BVGeneratorCode S F g, false) ::
              nativeC60CAChainSignedCodes S F tail =
            (nativeC60BVGeneratorCode S F g', false) ::
              nativeC60CAChainSignedCodes S F rest at hcodes
          injection hcodes with hhead htail
          have hc : nativeC60BVGeneratorCode S F g =
              nativeC60BVGeneratorCode S F g' := congrArg Prod.fst hhead
          have hmid :=
            (nativeC60CBGen_source S F g).trans
              ((congrArg
                (fun code : NativeC60BVGeneratorCode S =>
                  nativeC60BCContextTotal F code.1 code.2.1)
                hc).trans (nativeC60CBGen_source S F g').symm)
          cases hmid
          have hg : g = g' :=
            nativeC60BVGeneratorCode_injective S F hc
          cases hg
          have hrest : tail = rest := ih rest htail
          cases hrest
          rfl

/-- The first signed chain criterion without any a priori restriction
on its original intermediate 15D skeleton. Unlike BZ, signs may mix. -/
theorem nativeC60CBChainReduced_strict_frame_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (p q : NativeC60CASignedChain S F a b)
    (hp : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F p))
    (hq : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F q)) :
    nativeC60CAChainStrictFrame S F word p =
      nativeC60CAChainStrictFrame S F word q ↔ p = q := by
  constructor
  · intro heq
    have hr := nativeC60CA_strict_eq_implies_reduced_eq S F word p q heq
    have hf := (nativeC60CAChain_reduced_eq_iff S F p q).mp hr
    have hcodes := nativeC60BYReducedSignedWord_unique S
      (nativeC60CAChainSignedCodes S F p)
      (nativeC60CAChainSignedCodes S F q) hp hq hf
    exact nativeC60CBChainCodes_eq_implies_eq S F p q hcodes
  · rintro rfl
    rfl

/-- The converse free-word => strict equality is already unconditional
ON THE SUBTYPE OF REDUCED GENUINE SIGNED CHAINS, with no fixed internal
15D skeleton, under EVERY finite original AQ context. -/
theorem nativeC60CBChainReduced_free_eq_iff_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (p q : NativeC60CASignedChain S F a b)
    (hp : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F p))
    (hq : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F q)) :
    FreeGroup.mk (nativeC60CAChainSignedCodes S F p) =
        FreeGroup.mk (nativeC60CAChainSignedCodes S F q) ↔
      nativeC60CAChainStrictFrame S F word p =
        nativeC60CAChainStrictFrame S F word q := by
  constructor
  · intro hfree
    have hcodes := nativeC60BYReducedSignedWord_unique S
      (nativeC60CAChainSignedCodes S F p)
      (nativeC60CAChainSignedCodes S F q) hp hq hfree
    have hpaths := nativeC60CBChainCodes_eq_implies_eq S F p q hcodes
    exact (nativeC60CBChainReduced_strict_frame_eq_iff
      S F word p q hp hq).mpr hpaths
  · intro hstrict
    exact (nativeC60CAChain_reduced_eq_iff S F p q).mp
      (nativeC60CA_strict_eq_implies_reduced_eq S F word p q hstrict)

/-- An exact selected strict-Kuu reflection criterion for arbitrary
mixed-sign paths, GIVEN explicit typed cancellation witnesses to
reduced paths. The reductions may delete different intermediate 15D
objects; the reduct paths only share original endpoints. -/
theorem nativeC60CBNormalized_strict_frame_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (p q p' q' : NativeC60CASignedChain S F a b)
    (hp : Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F a b =>
        NativeC60CAElementaryCancel S F x y) p p')
    (hq : Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F a b =>
        NativeC60CAElementaryCancel S F x y) q q')
    (hredp : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F p'))
    (hredq : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F q')) :
    nativeC60CAChainStrictFrame S F word p =
      nativeC60CAChainStrictFrame S F word q ↔ p' = q' := by
  have hep := nativeC60CAFiniteCancellation_sound S F word hp
  have heq := nativeC60CAFiniteCancellation_sound S F word hq
  constructor
  · intro h
    exact (nativeC60CBChainReduced_strict_frame_eq_iff
      S F word p' q' hredp hredq).mp
        (hep.symm.trans (h.trans heq))
  · intro h
    cases h
    exact hep.trans heq.symm

/-- Under endpoint-preserving typed normalization witnesses,
the NONCOMMUTATIVE complete free group is faithful on original strict
Kuu higher Hom arrows for arbitrary (possibly different-skeleton)
signed 16D proofs, including all finite genuine AQ contexts. -/
theorem nativeC60CBNormalized_free_eq_iff_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (p q p' q' : NativeC60CASignedChain S F a b)
    (hp : Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F a b =>
        NativeC60CAElementaryCancel S F x y) p p')
    (hq : Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F a b =>
        NativeC60CAElementaryCancel S F x y) q q')
    (hredp : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F p'))
    (hredq : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F q')) :
    FreeGroup.mk (nativeC60CAChainSignedCodes S F p) =
        FreeGroup.mk (nativeC60CAChainSignedCodes S F q) ↔
      nativeC60CAChainStrictFrame S F word p =
        nativeC60CAChainStrictFrame S F word q := by
  have hep := nativeC60CAFiniteCancellation_sound S F word hp
  have heq := nativeC60CAFiniteCancellation_sound S F word hq
  have hpfree : FreeGroup.mk (nativeC60CAChainSignedCodes S F p) =
      FreeGroup.mk (nativeC60CAChainSignedCodes S F p') :=
    (nativeC60CAChain_reduced_eq_iff S F p p').mp
      (nativeC60CA_strict_eq_implies_reduced_eq S F word p p' hep)
  have hqfree : FreeGroup.mk (nativeC60CAChainSignedCodes S F q) =
      FreeGroup.mk (nativeC60CAChainSignedCodes S F q') :=
    (nativeC60CAChain_reduced_eq_iff S F q q').mp
      (nativeC60CA_strict_eq_implies_reduced_eq S F word q q' heq)
  constructor
  · intro hfree
    have hnfree := hpfree.symm.trans (hfree.trans hqfree)
    have hnormalized := (nativeC60CBChainReduced_free_eq_iff_strict
      S F word p' q' hredp hredq).mp hnfree
    exact hep.trans (hnormalized.trans heq.symm)
  · intro hstrict
    exact (nativeC60CAChain_reduced_eq_iff S F p q).mp
      (nativeC60CA_strict_eq_implies_reduced_eq S F word p q hstrict)

#print axioms nativeC60CBGen_source
#print axioms nativeC60CBGen_target
#print axioms nativeC60CBChainCodes_eq_implies_eq
#print axioms nativeC60CBChainReduced_strict_frame_eq_iff
#print axioms nativeC60CBChainReduced_free_eq_iff_strict
#print axioms nativeC60CBNormalized_strict_frame_eq_iff
#print axioms nativeC60CBNormalized_free_eq_iff_strict

end
end Kuu.F112.Physical
