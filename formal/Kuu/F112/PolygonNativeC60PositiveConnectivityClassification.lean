import Kuu.F112.PolygonNativeC60PhysicalPositiveDiamondExistenceObstruction

/-!
# F112-P94D3CH — original-15D syntactic positive-connectivity classification

CG proves that every genuine context-closed BC positive generator starts at
a source-first AU naturality term with TRUE leading-conservative syntax, and
that the actual physical exchange target has FALSE syntax.

Here the classification is extended to EVERY original, dependent AQ 15D
witness. A target-first AU term has TRUE leading syntax precisely for an
outer conservative constructor; exchange, reversal and composition give
FALSE. This exact computation remains valid in EVERY finite actual C60
14D whiskering context.

Therefore a positive BC successor of the target-first term NECESSARILY
has conservative outer syntax. We derive separate unconditional no-go
statements for exchange, symm and trans and any positive nonempty tail.

A conservative tag alone is NOT promoted to sufficient evidence: the
necessary-and-sufficient criterion quantifies an ACTUAL next original
15D AQ witness, its full AU source/target proof terms, and their exact
contextual dependent boundary equalities. An explicitly constructed
follow-on BC generator proves the converse under that certificate.

This neither forbids mixed-sign paths nor postulates a geometric 16D
filler, unrestricted Peiffer interchange, Gray categories, or a global
strict 3/n-category. No new axioms, sorry/admit, or public roots.
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

/-- Exact outer-constructor classifier on ORIGINAL proof-relevant 15D
AQ evidence; the scalar Peiffer observer is deliberately not involved. -/
def nativeK5CHOuterConservative
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} :
    NativeK5AQFifteenCell W R S → Bool
  | .conservative _ => true
  | .exchange _ => false
  | .symm _ => false
  | .trans _ _ => false

/-- The original, dependent AU source-first 15D term after a genuinely
physical finite context; no boundary is erased or quotient-selected. -/
def nativeK5CHSource
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (nativeK5AXBaseLayer W).Total :=
  nativeK5BCContext W word
    (nativeK5AXPack W (nativeK5AUNaturalityViaSource W cell))

/-- The corresponding target-first 15D term, with the SAME original
R/S boundary and the same genuinely applied finite context. -/
def nativeK5CHTarget
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (nativeK5AXBaseLayer W).Total :=
  nativeK5BCContext W word
    (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W cell))

/-- An actual, not merely possible, positive 16D BC generator for EVERY
original 15D AQ witness and EVERY finite actual 14D context. -/
def nativeK5CHPositiveGenerator
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (nativeK5BCSignature W).Gen
      (nativeK5CHSource W word cell)
      (nativeK5CHTarget W word cell) :=
  nativeC60BCGen (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    word ⟨R, S, cell, rfl, rfl⟩

/-- All source-first terms begin with the conservative Peiffer
comparison even when their INPUT cell is exchange/symm/trans. -/
theorem nativeK5CHSource_leading_true
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5AYRawLeading W (nativeK5CHSource W word cell) = true := by
  unfold nativeK5CHSource
  rw [nativeK5BCContext_pack W word _]
  change nativeK5AXLeadingConservative W
      (nativeK5AQContextCell W word
        (nativeK5AUNaturalityViaSource W cell)) = true
  rw [nativeK5BCLeading_context W word]
  rfl

/-- Complete four-constructor classification of the target-first side.
In particular, the outer conservative branch is TRUE for every input
core witness, while exchange, symm, and trans are FALSE, regardless of
their children. Finite physical context does not change the answer. -/
theorem nativeK5CHTarget_leading_eq_outer
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5AYRawLeading W (nativeK5CHTarget W word cell) =
      nativeK5CHOuterConservative W cell := by
  unfold nativeK5CHTarget
  rw [nativeK5BCContext_pack W word _]
  change nativeK5AXLeadingConservative W
      (nativeK5AQContextCell W word
        (nativeK5AUNaturalityViaTarget W cell)) =
      nativeK5CHOuterConservative W cell
  rw [nativeK5BCLeading_context W word]
  cases cell <;> rfl

/-- The leading TRUE tag is NECESSARY for any further positively
oriented BC generator. This is not a general existence theorem. -/
theorem nativeK5CHSuccessor_requires_conservative
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (next : (nativeK5AXBaseLayer W).Total)
    (h : Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CHTarget W word cell) next)) :
    nativeK5CHOuterConservative W cell = true := by
  rcases h with ⟨g⟩
  have ht := nativeK5CGAll_positive_sources_true W g
  rw [nativeK5CHTarget_leading_eq_outer W word cell] at ht
  exact ht

/-- For any constructor giving FALSE, no independent next positive
BC generator can follow. The target 15D proof itself is retained. -/
theorem nativeK5CHNo_positive_successor_of_false
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (next : (nativeK5AXBaseLayer W).Total)
    (hfalse : nativeK5CHOuterConservative W cell = false) :
    ¬ Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CHTarget W word cell) next) := by
  intro h
  have ht := nativeK5CHSuccessor_requires_conservative W word cell next h
  rw [hfalse] at ht
  cases ht

/-- No positive successor of ANY original indexed 15D exchange,
not merely the physical exchange at the empty word studied in CG. -/
theorem nativeK5CHExchange_no_positive_successor
    (W : NativeK5StructuralThirteenCell p U V)
    (word index : List Bool)
    (next : (nativeK5AXBaseLayer W).Total) :
    ¬ Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CHTarget W word (nativeK5AQExchange W index)) next) :=
  nativeK5CHNo_positive_successor_of_false W word
    (nativeK5AQExchange W index) next rfl

/-- Explicit case: reversal of ANY original dependent 15D witness. -/
theorem nativeK5CHSymm_no_positive_successor
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (next : (nativeK5AXBaseLayer W).Total) :
    ¬ Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CHTarget W word (.symm cell)) next) :=
  nativeK5CHNo_positive_successor_of_false W word (.symm cell) next rfl

/-- Explicit case: composition of ANY two composable original
15D witnesses, even when the left or right input is conservative. -/
theorem nativeK5CHTrans_no_positive_successor
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S T : NativeK5FifteenFourteenFiber W}
    (left : NativeK5AQFifteenCell W R S)
    (right : NativeK5AQFifteenCell W S T)
    (next : (nativeK5AXBaseLayer W).Total) :
    ¬ Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CHTarget W word (.trans left right)) next) :=
  nativeK5CHNo_positive_successor_of_false W word (.trans left right) next rfl

/-- The above typed obstruction also eliminates positive chains of
arbitrary nonzero finite length, without banning inverse/mixed paths. -/
theorem nativeK5CHNo_nonempty_positive_tail_of_false
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (next : (nativeK5AXBaseLayer W).Total)
    (tail : List (nativeK5AXBaseLayer W).Total)
    (hfalse : nativeK5CHOuterConservative W cell = false) :
    ¬ Nonempty (NativeC60BZPositiveChain
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CHTarget W word cell) (next :: tail)) := by
  rintro ⟨chain⟩
  cases chain with
  | cons g _ =>
      exact nativeK5CHNo_positive_successor_of_false W word
        cell next hfalse ⟨g⟩

/-- EXACT positive-successor criterion. The right-hand side is a
certificate in the ORIGINAL dependent C60 15D syntax: an independent
witness with two original 14D endpoints, a finite 14D context, and
TWO exact 15D endpoint equalities. No scalar/Peiffer equality is used
to invent a 16D edge. This remains valid even for conservative inputs. -/
theorem nativeK5CHSuccessor_iff_boundary_certificate
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (next : (nativeK5AXBaseLayer W).Total) :
    Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CHTarget W word cell) next) ↔
    ∃ (outer : List Bool) (R' S' : NativeK5FifteenFourteenFiber W)
      (following : NativeK5AQFifteenCell W R' S'),
      nativeK5CHTarget W word cell =
        nativeK5CHSource W outer following ∧
      next = nativeK5CHTarget W outer following := by
  constructor
  · rintro ⟨g⟩
    rcases g with ⟨outer, a, b, ⟨g₀, hx, hy⟩⟩
    rcases g₀ with ⟨R', S', following, hsrc, htgt⟩
    refine ⟨outer, R', S', following, ?_, ?_⟩
    · calc
        nativeK5CHTarget W word cell =
            nativeK5BCContext W outer a := hx
        _ = nativeK5CHSource W outer following :=
          congrArg (nativeK5BCContext W outer) hsrc
    · calc
        next = nativeK5BCContext W outer b := hy
        _ = nativeK5CHTarget W outer following :=
          congrArg (nativeK5BCContext W outer) htgt
  · rintro ⟨outer, R', S', following, hx, hy⟩
    rw [hx, hy]
    exact ⟨nativeK5CHPositiveGenerator W outer following⟩

/-- Dropping only the choice of the NEXT target gives a useful precise
existence test: an outgoing generator exists exactly when the present
target is an ACTUAL source-first contextual AU term. This is strictly
more information than the Boolean necessary condition. -/
theorem nativeK5CHAny_successor_iff_original_source_match
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (∃ next : (nativeK5AXBaseLayer W).Total,
      Nonempty ((nativeK5BCSignature W).Gen
        (nativeK5CHTarget W word cell) next)) ↔
    ∃ (outer : List Bool) (R' S' : NativeK5FifteenFourteenFiber W)
      (following : NativeK5AQFifteenCell W R' S'),
      nativeK5CHTarget W word cell =
        nativeK5CHSource W outer following := by
  constructor
  · rintro ⟨next, h⟩
    obtain ⟨outer, R', S', following, hsrc, _⟩ :=
      (nativeK5CHSuccessor_iff_boundary_certificate W word cell next).mp h
    exact ⟨outer, R', S', following, hsrc⟩
  · rintro ⟨outer, R', S', following, hsrc⟩
    refine ⟨nativeK5CHTarget W outer following, ?_⟩
    exact (nativeK5CHSuccessor_iff_boundary_certificate W word
      cell _).mpr ⟨outer, R', S', following, hsrc, rfl⟩

/-- A FALSE-tag target cannot be either of the two actual 15D
midpoints of a fully positively-oriented 16D CF diamond. This
generalizes CG's concrete physical exchange restriction to all
exchange, reversal, and composition inputs. -/
theorem nativeK5CHFalse_target_not_positive_diamond_midpoint
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (hfalse : nativeK5CHOuterConservative W cell = false)
    (q : NativeC60CFTypedDiamond
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :
    q.leftMid ≠ nativeK5CHTarget W word cell ∧
      q.rightMid ≠ nativeK5CHTarget W word cell := by
  have ht : nativeK5AYRawLeading W
      (nativeK5CHTarget W word cell) = false := by
    rw [nativeK5CHTarget_leading_eq_outer W word cell]
    exact hfalse
  obtain ⟨hl, hr⟩ := nativeK5CGEvery_diamond_midpoints_true W q
  constructor
  · intro heq
    rw [heq, ht] at hl
    cases hl
  · intro heq
    rw [heq, ht] at hr
    cases hr

end PhysicalC60

#print axioms nativeK5CHSource_leading_true
#print axioms nativeK5CHTarget_leading_eq_outer
#print axioms nativeK5CHSuccessor_requires_conservative
#print axioms nativeK5CHExchange_no_positive_successor
#print axioms nativeK5CHSymm_no_positive_successor
#print axioms nativeK5CHTrans_no_positive_successor
#print axioms nativeK5CHNo_nonempty_positive_tail_of_false
#print axioms nativeK5CHSuccessor_iff_boundary_certificate
#print axioms nativeK5CHAny_successor_iff_original_source_match
#print axioms nativeK5CHFalse_target_not_positive_diamond_midpoint

end
end Kuu.F112.Physical
