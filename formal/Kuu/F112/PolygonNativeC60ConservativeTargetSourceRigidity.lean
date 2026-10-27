import Kuu.F112.PolygonNativeC60ConservativeSourceTargetRigidity

/-!
# F112-P94D3CU — dual conservative target/source rigidity

CT proves that an original conservative C60 BC SOURCE determines a
unique target 15D object, while preserving distinct generator witnesses.
CU proves the NON-ASSUMED DUAL: fixing the original conservative BC
TARGET likewise determines the unique source 15D object.

An exact target-first AU naturality term contains:
* BOTH original raw 14D boundaries, which CJ uses to recover its full
  physical finite AQ context word and CI uses to recover each raw input;
* the FIRST whiskered 15D input constructor, whose outer-conservative
  tag is invariant under the actual original 14D context action.

For any two conservative original inputs, both source-first and
target-first terms are independent of raw conservative proof syntax at
fixed original 14D endpoints. Thus an actual conservative target
rigidly determines the original source, and both directions together
classify all positive BC primitives incident to the physical
conservative comparison pair as parallel ORIGINAL 15D arrows.

This is NOT uniqueness of generator certificates, a kernel-triviality
proof, free-group completeness, geometric 16D coherence, full P92B
descent or global Peiffer. No Gray, axioms, sorry/admit or root changes.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section PhysicalC60

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- Examine the FIRST original 15D subcomparison of a target-first
AU naturality path, never its charge or scalar Peiffer observation. -/
def nativeK5CUTargetFirstConservative
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} :
    NativeK5AQFifteenCell W R S → Bool
  | .trans first _ => nativeK5CHOuterConservative W first
  | _ => false

/-- The first original 15D constructor passes faithfully through
each actual original 14D frame, not through a hypothetical inverse. -/
theorem nativeK5CUTargetFirst_whisker
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CUTargetFirstConservative W
        (nativeK5AQWhiskerCell W side cell) =
      nativeK5CUTargetFirstConservative W cell := by
  cases cell with
  | conservative _ => rfl
  | exchange _ => rfl
  | symm _ => rfl
  | trans first second =>
      change nativeK5CHOuterConservative W
          (nativeK5AQWhiskerCell W side first) =
        nativeK5CHOuterConservative W first
      exact nativeK5CTOuterConservative_whisker W side first

/-- Induction along every actual finite AQ physical context word. -/
theorem nativeK5CUTargetFirst_context
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CUTargetFirstConservative W
        (nativeK5AQContextCell W word cell) =
      nativeK5CUTargetFirstConservative W cell := by
  induction word with
  | nil => rfl
  | cons side rest ih =>
      change nativeK5CUTargetFirstConservative W
          (nativeK5AQWhiskerCell W side
            (nativeK5AQContextCell W rest cell)) = _
      rw [nativeK5CUTargetFirst_whisker W side, ih]

/-- Read the entire original target-first proof as a dependent 15D
object and retain the first constructor witness. -/
def nativeK5CUTotalFirstConservative
    (W : NativeK5StructuralThirteenCell p U V)
    (z : (nativeK5AXBaseLayer W).Total) : Bool :=
  nativeK5CUTargetFirstConservative W z.2.down

/-- Actual AU target-first naturality retains EXACTLY the input 15D
outer constructor through both real original whiskerings and context. -/
theorem nativeK5CUTargetFirst_eq_input_outer
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CUTotalFirstConservative W (nativeK5CHTarget W word cell) =
      nativeK5CHOuterConservative W cell := by
  unfold nativeK5CHTarget
  rw [nativeK5BCContext_pack W word _]
  change nativeK5CUTargetFirstConservative W
      (nativeK5AQContextCell W word
        (nativeK5AUNaturalityViaTarget W cell)) = _
  rw [nativeK5CUTargetFirst_context W word]
  change nativeK5CHOuterConservative W
      (nativeK5AQWhiskerCell W true
        (nativeK5AQWhiskerCell W false cell)) = _
  rw [nativeK5CTOuterConservative_whisker,
    nativeK5CTOuterConservative_whisker]

/-- Equality of exact TARGET-FIRST original 15D proofs forces equality
of their outer input constructor, not merely of a Peiffer shadow. -/
theorem nativeK5CUTarget_eq_forces_outer
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (other : NativeK5AQFifteenCell W R' S')
    (htgt : nativeK5CHTarget W xs cell =
      nativeK5CHTarget W ys other) :
    nativeK5CHOuterConservative W cell =
      nativeK5CHOuterConservative W other := by
  have h := congrArg (nativeK5CUTotalFirstConservative W) htgt
  rwa [nativeK5CUTargetFirst_eq_input_outer,
    nativeK5CUTargetFirst_eq_input_outer] at h

/-- Recover the FULL original context word and both original 14D
endpoints directly from equality of physical target-first 15D cells.
No constructor/proof relevance is erased. -/
theorem nativeK5CUTarget_eq_forces_word_and_endpoints
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (other : NativeK5AQFifteenCell W R' S')
    (htgt : nativeK5CHTarget W xs cell =
      nativeK5CHTarget W ys other) :
    xs = ys ∧ R = R' ∧ S = S' := by
  have hs := congrArg (fun z : (nativeK5AXBaseLayer W).Total => z.1.1.down) htgt
  have ht := congrArg (fun z : (nativeK5AXBaseLayer W).Total => z.1.2.down) htgt
  unfold nativeK5CHTarget at hs ht
  rw [nativeK5BCContext_pack W xs _, nativeK5BCContext_pack W ys _] at hs ht
  change nativeK5AQContext W xs (nativeK5CJStart W R) =
    nativeK5AQContext W ys (nativeK5CJStart W R') at hs
  change nativeK5AQContext W xs (nativeK5CJFinish W S) =
    nativeK5AQContext W ys (nativeK5CJFinish W S') at ht
  have hw : xs = ys :=
    nativeK5CJContext_words_unique W xs ys R S R' S' hs ht
  subst ys
  have hs0 : nativeK5CJStart W R = nativeK5CJStart W R' :=
    nativeK5CIContext_injective W xs hs
  have ht0 : nativeK5CJFinish W S = nativeK5CJFinish W S' :=
    nativeK5CIContext_injective W xs ht
  have hR : R = R' :=
    nativeK5CIWhisker_injective W false
      (nativeK5CIWhisker_injective W true hs0)
  have hS : S = S' :=
    nativeK5CIWhisker_injective W true
      (nativeK5CIWhisker_injective W false ht0)
  exact ⟨rfl, hR, hS⟩

/-- Raw conservative original 15D witnesses with the SAME original
14D boundaries induce the SAME source-first naturality term,
without equating their original 15D proof certificates themselves. -/
theorem nativeK5CUConservative_source_independent
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell other : NativeK5AQFifteenCell W R S)
    (hc : nativeK5CHOuterConservative W cell = true)
    (hd : nativeK5CHOuterConservative W other = true) :
    nativeK5CHSource W word cell = nativeK5CHSource W word other := by
  cases cell with
  | conservative c =>
      cases other with
      | conservative d => rfl
      | exchange _ => cases hd
      | symm _ => cases hd
      | trans _ _ => cases hd
  | exchange _ => cases hc
  | symm _ => cases hc
  | trans _ _ => cases hc

/-- A fixed conservative physical TARGET determines its unique
SOURCE FIRST 15D object, despite multiple original generator witnesses. -/
theorem nativeK5CUConservative_target_determines_source
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (other : NativeK5AQFifteenCell W R' S')
    (hcons : nativeK5CHOuterConservative W cell = true)
    (htgt : nativeK5CHTarget W xs cell =
      nativeK5CHTarget W ys other) :
    nativeK5CHSource W xs cell = nativeK5CHSource W ys other := by
  obtain ⟨hw, hR, hS⟩ :=
    nativeK5CUTarget_eq_forces_word_and_endpoints W xs ys cell other htgt
  subst ys
  subst R'
  subst S'
  have hother : nativeK5CHOuterConservative W other = true := by
    rw [← nativeK5CUTarget_eq_forces_outer W xs xs cell other htgt]
    exact hcons
  exact nativeK5CUConservative_source_independent W xs cell other hcons hother

/-- Conservative original 15D comparisons now have exactly the same
source equality relation as target equality, in arbitrary contexts. -/
theorem nativeK5CUConservative_boundary_equivalence
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (other : NativeK5AQFifteenCell W R' S')
    (hcons : nativeK5CHOuterConservative W cell = true) :
    (nativeK5CHSource W xs cell = nativeK5CHSource W ys other) ↔
      (nativeK5CHTarget W xs cell = nativeK5CHTarget W ys other) := by
  constructor
  · exact nativeK5CTConservative_source_determines_target W xs ys cell other hcons
  · exact nativeK5CUConservative_target_determines_source W xs ys cell other hcons

/-- Original physical C60 conservative TARGET cannot have an incoming
positive BC generator from any different ORIGINAL 15D source. -/
theorem nativeK5CUPhysical_unique_source_from_conservative_target
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool)
    {source : (nativeK5AXBaseLayer W).Total}
    (g : (nativeK5BCSignature W).Gen source
      (nativeK5CHTarget W word (nativeK5CKConservativeRefl W R))) :
    source = nativeK5CHSource W word (nativeK5CKConservativeRefl W R) := by
  rcases g with ⟨ys, x, y, ⟨gen, hsrc, htgt⟩⟩
  rcases gen with ⟨R', S', other, hfrom, hto⟩
  have ht : nativeK5CHTarget W word (nativeK5CKConservativeRefl W R) =
      nativeK5CHTarget W ys other := by
    calc
      _ = nativeK5BCContext W ys y := htgt
      _ = nativeK5BCContext W ys
          (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W other)) :=
        congrArg (nativeK5BCContext W ys) hto
      _ = _ := rfl
  have hs := nativeK5CUConservative_target_determines_source W word ys
    (nativeK5CKConservativeRefl W R) other (by rfl) ht
  calc
    source = nativeK5BCContext W ys x := hsrc
    _ = nativeK5BCContext W ys
        (nativeK5AXPack W (nativeK5AUNaturalityViaSource W other)) :=
      congrArg (nativeK5BCContext W ys) hfrom
    _ = nativeK5CHSource W ys other := rfl
    _ = nativeK5CHSource W word (nativeK5CKConservativeRefl W R) := hs.symm

/-- The exact inverse of CT's physical no-offtarget theorem:
there is no original incoming positive primitive at the selected
conservative terminal with any alternative source. -/
theorem nativeK5CUPhysical_no_offsource_primitive
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool)
    (source : (nativeK5AXBaseLayer W).Total)
    (hc : source ≠
      nativeK5CHSource W word (nativeK5CKConservativeRefl W R)) :
    ¬ Nonempty ((nativeK5BCSignature W).Gen source
      (nativeK5CHTarget W word (nativeK5CKConservativeRefl W R))) := by
  rintro ⟨g⟩
  exact hc (nativeK5CUPhysical_unique_source_from_conservative_target W R word g)

/-- The original physical CK conservative pair is a rigid adjacent
15D boundary on BOTH ends: arbitrary outgoing and incoming primitive
certificates meeting its source/target are necessarily PARALLEL.
Nothing here equates the distinct certificates. -/
theorem nativeK5CUPhysical_conservative_incidence_parallel
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool)
    {next previous : (nativeK5AXBaseLayer W).Total}
    (outgoing : (nativeK5BCSignature W).Gen
      (nativeK5CHSource W word (nativeK5CKConservativeRefl W R)) next)
    (incoming : (nativeK5BCSignature W).Gen previous
      (nativeK5CHTarget W word (nativeK5CKConservativeRefl W R))) :
    next = nativeK5CHTarget W word (nativeK5CKConservativeRefl W R) ∧
      previous = nativeK5CHSource W word (nativeK5CKConservativeRefl W R) :=
  ⟨nativeK5CTPhysical_unique_target_from_conservative_base W R word outgoing,
    nativeK5CUPhysical_unique_source_from_conservative_target W R word incoming⟩

/-- TRUE finite-context action has a strict ORIGINAL typed nested-word
formula on the source-first AU 15D object. No empty/identity
context shortcut or forgetting of a previous frame. -/
theorem nativeK5CUPhysical_source_frame_append
    (W : NativeK5StructuralThirteenCell p U V)
    (inner outer : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5BCContext W outer (nativeK5CHSource W inner cell) =
      nativeK5CHSource W (outer ++ inner) cell := by
  unfold nativeK5CHSource nativeK5BCContext
  exact (nativeC60BCContextTotal_append (nativeK5BCFrame W) outer inner
    (nativeK5AXPack W (nativeK5AUNaturalityViaSource W cell))).symm

/-- Both sides of the proof-bearing original naturality square receive
the same exact concatenated context, without imposing interchange. -/
theorem nativeK5CUPhysical_target_frame_append
    (W : NativeK5StructuralThirteenCell p U V)
    (inner outer : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5BCContext W outer (nativeK5CHTarget W inner cell) =
      nativeK5CHTarget W (outer ++ inner) cell := by
  unfold nativeK5CHTarget nativeK5BCContext
  exact (nativeC60BCContextTotal_append (nativeK5BCFrame W) outer inner
    (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W cell))).symm

/-- The rigidity remains valid at the actual outer-AQ-framed strict
isotropy basepoint, the object used by the original CO/CP/CQ/CR series. -/
theorem nativeK5CUPhysical_framed_incidence_parallel
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {next previous : (nativeK5AXBaseLayer W).Total}
    (outgoing : (nativeK5BCSignature W).Gen
      (nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))) next)
    (incoming : (nativeK5BCSignature W).Gen previous
      (nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)))) :
    next = nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)) ∧
      previous = nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) := by
  rw [nativeK5CUPhysical_source_frame_append W inner outer] at outgoing
  rw [nativeK5CUPhysical_target_frame_append W inner outer] at incoming
  obtain ⟨hnext, hprev⟩ :=
    nativeK5CUPhysical_conservative_incidence_parallel W R
      (outer ++ inner) outgoing incoming
  constructor
  · rw [nativeK5CUPhysical_target_frame_append W inner outer]
    exact hnext
  · rw [nativeK5CUPhysical_source_frame_append W inner outer]
    exact hprev

end PhysicalC60

#print axioms nativeK5CUTargetFirst_whisker
#print axioms nativeK5CUTargetFirst_context
#print axioms nativeK5CUTargetFirst_eq_input_outer
#print axioms nativeK5CUTarget_eq_forces_outer
#print axioms nativeK5CUTarget_eq_forces_word_and_endpoints
#print axioms nativeK5CUConservative_source_independent
#print axioms nativeK5CUConservative_target_determines_source
#print axioms nativeK5CUConservative_boundary_equivalence
#print axioms nativeK5CUPhysical_unique_source_from_conservative_target
#print axioms nativeK5CUPhysical_no_offsource_primitive
#print axioms nativeK5CUPhysical_conservative_incidence_parallel
#print axioms nativeK5CUPhysical_source_frame_append
#print axioms nativeK5CUPhysical_target_frame_append
#print axioms nativeK5CUPhysical_framed_incidence_parallel

end
end Kuu.F112.Physical
