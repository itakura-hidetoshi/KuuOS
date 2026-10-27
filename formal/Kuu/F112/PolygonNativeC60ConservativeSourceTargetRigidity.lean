import Kuu.F112.PolygonNativeC60OffTargetStrictKernelAction

/-!
# F112-P94D3CT — conservative-base target rigidity in original C60

CS proves a genuine strict kernel loop and nontrivial conjugation from an
off-target pair of original dependent 16D generators, *if* such a pair
exists. CT tests this conditional hypothesis in the actual C60
conservative-atom presentation.

A source-first AU 15D term retains:
- both exact original 14D endpoints, which jointly recover the whole
  finite physical AQ context word by CJ;
- the outer 15D constructor of the original input inside the second
  component of its typed naturality path.

Original physical 14D context whiskerings act injectively on the
boundary proofs (CI), while outer-conservative classification is
invariant under every original 15D whiskering. Once the source of
a genuine positive BC generator is fixed to CK's conservative base,
the context, original 14D endpoints, and conservative constructor
are forced. Its target is therefore unique, although the ORIGINAL
proof-relevant generator certificates remain distinct.

Consequently, CS's DIFFERENT-TERMINAL conditional witness cannot be
instantiated at the actual physical conservative base. This does NOT
prove that the true CP strict isotropy kernel is trivial: more complex
typed signed closed loops, potentially involving different source
and target certificates, remain unclassified. No new geometric
16-cell equality, Gray, axiom, sorry/admit, or public proof root.

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

/-- The original 15D OUTER constructor is conserved by each actual
physical 14D whiskering even though its conservative inner proof
tree can be normalized to a new atom. -/
theorem nativeK5CTOuterConservative_whisker
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CHOuterConservative W (nativeK5AQWhiskerCell W side cell) =
      nativeK5CHOuterConservative W cell := by
  cases cell <;> rfl

/-- Every finite physical C60 context preserves the original outer
15D constructor classifier; this does NOT identify raw proof trees. -/
theorem nativeK5CTOuterConservative_context
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CHOuterConservative W (nativeK5AQContextCell W word cell) =
      nativeK5CHOuterConservative W cell := by
  induction word with
  | nil => rfl
  | cons side rest ih =>
      change nativeK5CHOuterConservative W
        (nativeK5AQWhiskerCell W side (nativeK5AQContextCell W rest cell)) = _
      rw [nativeK5CTOuterConservative_whisker W side, ih]

/-- Read the OUTER constructor of the SECOND original 15D segment of
a source-first naturality path. This retains the original typed tree
rather than scalar holonomy or a graph approximation. -/
def nativeK5CTSourceSecondConservative
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} :
    NativeK5AQFifteenCell W R S → Bool
  | .trans _ second => nativeK5CHOuterConservative W second
  | _ => false

/-- The source-second constructor predicate commutes with actual
physical whiskerings, even on nested signed 15D syntax. -/
theorem nativeK5CTSourceSecond_whisker
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CTSourceSecondConservative W
        (nativeK5AQWhiskerCell W side cell) =
      nativeK5CTSourceSecondConservative W cell := by
  cases cell with
  | conservative _ => rfl
  | exchange _ => rfl
  | symm _ => rfl
  | trans first second =>
      change nativeK5CHOuterConservative W
        (nativeK5AQWhiskerCell W side second) =
          nativeK5CHOuterConservative W second
      exact nativeK5CTOuterConservative_whisker W side second

/-- The same predicate persists through arbitrary finite original
14D AQ context actions on the complete dependent 15D path. -/
theorem nativeK5CTSourceSecond_context
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CTSourceSecondConservative W
        (nativeK5AQContextCell W word cell) =
      nativeK5CTSourceSecondConservative W cell := by
  induction word with
  | nil => rfl
  | cons side rest ih =>
      change nativeK5CTSourceSecondConservative W
        (nativeK5AQWhiskerCell W side
          (nativeK5AQContextCell W rest cell)) = _
      rw [nativeK5CTSourceSecond_whisker W side, ih]

/-- Read the ORIGINAL proof-relevant 15D source term, including its
actual Type-valued witness and both original 14D endpoints. -/
def nativeK5CTTotalSecondConservative
    (W : NativeK5StructuralThirteenCell p U V)
    (z : (nativeK5AXBaseLayer W).Total) : Bool :=
  nativeK5CTSourceSecondConservative W z.2.down

/-- The source-first side remembers exactly the input's original outer
15D constructor after every independently selected physical AQ word. -/
theorem nativeK5CTSourceSecond_eq_input_outer
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CTTotalSecondConservative W (nativeK5CHSource W word cell) =
      nativeK5CHOuterConservative W cell := by
  unfold nativeK5CHSource
  rw [nativeK5BCContext_pack W word _]
  change nativeK5CTSourceSecondConservative W
    (nativeK5AQContextCell W word (nativeK5AUNaturalityViaSource W cell)) = _
  rw [nativeK5CTSourceSecond_context W word]
  change nativeK5CHOuterConservative W
    (nativeK5AQWhiskerCell W false
      (nativeK5AQWhiskerCell W true cell)) = _
  rw [nativeK5CTOuterConservative_whisker,
    nativeK5CTOuterConservative_whisker]

/-- Equal genuine SOURCE-FIRST C60 typed 15D boundaries force equal
original outer-constructor kinds, not merely matching Peiffer values. -/
theorem nativeK5CTSource_eq_forces_outer
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (other : NativeK5AQFifteenCell W R' S')
    (hsrc : nativeK5CHSource W xs cell =
      nativeK5CHSource W ys other) :
    nativeK5CHOuterConservative W cell =
      nativeK5CHOuterConservative W other := by
  have h := congrArg (nativeK5CTTotalSecondConservative W) hsrc
  rwa [nativeK5CTSourceSecond_eq_input_outer,
       nativeK5CTSourceSecond_eq_input_outer] at h

/-- BOTH original fourteen-dimensional boundary endpoints of a
source-first equality force its actual finite AQ context word, and
then recover the two source-typed 14D input objects via CI injectivity.
No numerical fingerprint alone is asserted sufficient. -/
theorem nativeK5CTSource_eq_forces_word_and_endpoints
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (other : NativeK5AQFifteenCell W R' S')
    (hsrc : nativeK5CHSource W xs cell =
      nativeK5CHSource W ys other) :
    xs = ys ∧ R = R' ∧ S = S' := by
  have hs := congrArg (fun z : (nativeK5AXBaseLayer W).Total => z.1.1.down) hsrc
  have ht := congrArg (fun z : (nativeK5AXBaseLayer W).Total => z.1.2.down) hsrc
  unfold nativeK5CHSource at hs ht
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

/-- All ORIGINAL 15D conservative constructor certificates with the
same exact original 14D endpoints induce the SAME target-first typed
naturality term. Their distinct raw input proofs are NOT identified. -/
theorem nativeK5CTConservative_target_independent
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell other : NativeK5AQFifteenCell W R S)
    (hc : nativeK5CHOuterConservative W cell = true)
    (hd : nativeK5CHOuterConservative W other = true) :
    nativeK5CHTarget W word cell = nativeK5CHTarget W word other := by
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

/-- A conservative source-first boundary completely determines the
ACTUAL original target-first 15D boundary, even when arbitrary
proof-relevant input certificates share its source. This is not
a claim that those distinct input certificates themselves coincide. -/
theorem nativeK5CTConservative_source_determines_target
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (other : NativeK5AQFifteenCell W R' S')
    (hcons : nativeK5CHOuterConservative W cell = true)
    (hsrc : nativeK5CHSource W xs cell =
      nativeK5CHSource W ys other) :
    nativeK5CHTarget W xs cell = nativeK5CHTarget W ys other := by
  obtain ⟨hw, hR, hS⟩ :=
    nativeK5CTSource_eq_forces_word_and_endpoints W xs ys cell other hsrc
  subst ys
  subst R'
  subst S'
  have hother : nativeK5CHOuterConservative W other = true := by
    rw [← nativeK5CTSource_eq_forces_outer W xs xs cell other hsrc]
    exact hcons
  exact nativeK5CTConservative_target_independent W xs cell other hcons hother

/-- For CK's ACTUAL physical conservative base, no independent
context-closed BC primitive out of its source can have any alternative
original 15D terminal. All its full generators remain proof-distinct. -/
theorem nativeK5CTPhysical_unique_target_from_conservative_base
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool)
    {target : (nativeK5AXBaseLayer W).Total}
    (g : (nativeK5BCSignature W).Gen
      (nativeK5CHSource W word (nativeK5CKConservativeRefl W R)) target) :
    target = nativeK5CHTarget W word (nativeK5CKConservativeRefl W R) := by
  rcases g with ⟨ys, x, y, ⟨gen, hsrc, htgt⟩⟩
  rcases gen with ⟨R', S', other, hfrom, hto⟩
  have hs : nativeK5CHSource W word (nativeK5CKConservativeRefl W R) =
      nativeK5CHSource W ys other := by
    calc
      _ = nativeK5BCContext W ys x := hsrc
      _ = nativeK5BCContext W ys
          (nativeK5AXPack W (nativeK5AUNaturalityViaSource W other)) :=
        congrArg (nativeK5BCContext W ys) hfrom
      _ = _ := rfl
  have ht := nativeK5CTConservative_source_determines_target W word ys
    (nativeK5CKConservativeRefl W R) other (by rfl) hs
  calc
    target = nativeK5BCContext W ys y := htgt
    _ = nativeK5BCContext W ys
        (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W other)) :=
      congrArg (nativeK5BCContext W ys) hto
    _ = nativeK5CHTarget W ys other := rfl
    _ = nativeK5CHTarget W word (nativeK5CKConservativeRefl W R) := ht.symm

/-- CT DISCHARGES THE CS GEOMETRIC ALTERNATIVE-TERMINAL OBSTRUCTION
NEGATIVELY: the required off-target primitive cannot exist for the
selected genuine physical C60 conservative base, at any finite context.
This does NOT force the whole actual strict retraction kernel to vanish. -/
theorem nativeK5CTPhysical_no_offtarget_primitive
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool)
    (target : (nativeK5AXBaseLayer W).Total)
    (hc : target ≠
      nativeK5CHTarget W word (nativeK5CKConservativeRefl W R)) :
    ¬ Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CHSource W word (nativeK5CKConservativeRefl W R)) target) := by
  rintro ⟨g⟩
  exact hc (nativeK5CTPhysical_unique_target_from_conservative_base W R word g)

/-- In particular, the pair of physical off-target generators used in
CS's CONDITIONAL nontrivial-kernel and conjugation theorems is impossible.
The conditional general theorems remain correct and are not deleted. -/
theorem nativeK5CTPhysical_no_offtarget_pair
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool)
    (target : (nativeK5AXBaseLayer W).Total)
    (g h : (nativeK5BCSignature W).Gen
      (nativeK5CHSource W word (nativeK5CKConservativeRefl W R)) target)
    (hc : target ≠
      nativeK5CHTarget W word (nativeK5CKConservativeRefl W R)) :
    False :=
  nativeK5CTPhysical_no_offtarget_primitive W R word target hc ⟨g⟩

end PhysicalC60

#print axioms nativeK5CTOuterConservative_whisker
#print axioms nativeK5CTOuterConservative_context
#print axioms nativeK5CTSourceSecond_whisker
#print axioms nativeK5CTSourceSecond_context
#print axioms nativeK5CTSourceSecond_eq_input_outer
#print axioms nativeK5CTSource_eq_forces_outer
#print axioms nativeK5CTSource_eq_forces_word_and_endpoints
#print axioms nativeK5CTConservative_target_independent
#print axioms nativeK5CTConservative_source_determines_target
#print axioms nativeK5CTPhysical_unique_target_from_conservative_base
#print axioms nativeK5CTPhysical_no_offtarget_primitive
#print axioms nativeK5CTPhysical_no_offtarget_pair

end
end Kuu.F112.Physical
