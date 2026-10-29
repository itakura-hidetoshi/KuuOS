import Kuu.F112.PolygonNativeC60AQFullPentagonPartitionLocalCriticalPairs

/-!
# F112-P94D3EV — actual C60 AQ action fibers and failure of raw-path faithfulness

ET constructs a genuine Type-valued syntax of finite local AQ
repartitions (adjacent split/merge, zero insertion/deletion).
EU proves that all parallel finite paths induce the same honest
integer-receiver and residual-C60-AQ-kernel group equivalence, while
the [] -> [0] -> [] loop is NOT the reflexive raw path.

EV makes the distinction mathematically explicit:
* Define the observational equivalence relation on the ORIGINAL
  Type-valued local paths, retaining their dependent endpoints.
* Prove that each parallel-path action fiber is semantically one class.
* Exhibit a concrete pair of distinct original raw paths in a
  single action fiber, uniformly in the actual C60 AQ signature.
* Prove no left inverse/decoder from the action of the original
  zero-loop paths can recover their raw Type-valued histories.

The observation relation is not silently imposed on raw proofs or on
any of the 14D--18D dependent evidence cells. Even in a semantic
quotient, the raw Type-valued path syntax is preserved separately.
This is NOT a geometric 19D filler, a Gray structure, an infinite
split, or a claim that the original noncommutative kernel is abelian.
Retain strict Kuu, independent Kuu as a presentation, historical
DS no-go, 107 public roots, pinned Lean/mathlib and same-root
append-only/overwrite-forbidden governance.
No new logical axioms, sorry or admit.
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

section C60ActualAQActionFibers

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The actual semantic equality of two ORIGINAL locally generated
Type-valued repartition paths, as equality of their genuine ER/EJ
group equivalences on integer charges and residual obstruction. -/
def nativeC60EVLocalActionEq (word : List Bool) (start : ℕ)
    {xs ys : List ℕ} (p q : NativeC60ETLocalPath xs ys) : Prop :=
  nativeC60ETLocalPathEquiv S F word start p =
    nativeC60ETLocalPathEquiv S F word start q

/-- The observational equivalence relation is precisely equality of
ACTUAL group actions, rather than equality of raw Type-valued histories. -/
def nativeC60EVLocalActionSetoid (word : List Bool) (start : ℕ)
    (xs ys : List ℕ) : Setoid (NativeC60ETLocalPath xs ys) where
  r := nativeC60EVLocalActionEq S F word start
  iseqv := ⟨by
      intro p
      rfl,
    by
      intro p q h
      exact h.symm,
    by
      intro p q t hpq hqt
      exact hpq.trans hqt⟩

/-- ES/ET imply that EVERY two parallel local histories have the same
semantic action; no equality of raw paths is deduced. -/
theorem nativeC60EVLocalActionEq_all_parallel (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p q : NativeC60ETLocalPath xs ys) :
    nativeC60EVLocalActionEq S F word start p q :=
  nativeC60ETLocalPathEquiv_independent S F word r start p q

/-- The explicit [] -> [0] -> [] nonreflexive Type-valued loop
and the reflexivity path lie in one ACTUAL AQ action fiber. -/
theorem nativeC60EVZeroActionFiber_nontrivial (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) :
    nativeC60EVLocalActionEq S F word start
        nativeC60EUZeroHistoryLoop (NativeC60ETLocalPath.refl []) ∧
    nativeC60EUZeroHistoryLoop ≠ NativeC60ETLocalPath.refl [] :=
  ⟨nativeC60EVLocalActionEq_all_parallel S F word r start
      nativeC60EUZeroHistoryLoop (NativeC60ETLocalPath.refl []),
    nativeC60EUZeroHistoryLoop_ne_refl⟩

/-- No ACTUAL C60 AQ semantic action can serve as an injective
encoding of ALL original finite Type-valued zero-loop histories:
a concrete pair of distinct witnesses has the same action. -/
theorem nativeC60EVZeroAction_not_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) :
    ¬ Function.Injective
      (fun p : NativeC60ETLocalPath [] [] =>
        nativeC60ETLocalPathEquiv S F word start p) := by
  intro hinj
  have heq :
      nativeC60ETLocalPathEquiv S F word start
        nativeC60EUZeroHistoryLoop =
      nativeC60ETLocalPathEquiv S F word start
        (NativeC60ETLocalPath.refl []) :=
    nativeC60EVLocalActionEq_all_parallel S F word r start
      nativeC60EUZeroHistoryLoop (NativeC60ETLocalPath.refl [])
  exact nativeC60EUZeroHistoryLoop_ne_refl (hinj heq)

/-- There is NO decoder which left-inverts the actual group-action
evaluation on every original []-based local history. The obstruction
does not depend on a proposed 19D signature or unproved filler. -/
theorem nativeC60EVZeroAction_no_history_decoder (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) :
    ¬ ∃ decoder :
      ((nativeC60EQChargeTower ([] : List ℕ) ×
          (nativeC60EBAbelianReceiver S F word
            (start + ([] : List ℕ).sum)).ker) ≃*
        (nativeC60EQChargeTower ([] : List ℕ) ×
          (nativeC60EBAbelianReceiver S F word
            (start + ([] : List ℕ).sum)).ker)) →
        NativeC60ETLocalPath [] [],
      ∀ p : NativeC60ETLocalPath [] [],
        decoder (nativeC60ETLocalPathEquiv S F word start p) = p := by
  rintro ⟨decoder, hdecode⟩
  apply (nativeC60EVZeroAction_not_injective S F word r start)
  intro p q hpq
  calc
    p = decoder (nativeC60ETLocalPathEquiv S F word start p) :=
      (hdecode p).symm
    _ = decoder (nativeC60ETLocalPathEquiv S F word start q) :=
      congrArg decoder hpq
    _ = q := hdecode q

/-- The quotient class of two parallel local paths is equal AFTER
explicitly selecting equality of actual AQ actions as the relation.
This makes no raw Type-valued proof identification. -/
theorem nativeC60EVLocalActionQuotient_singleton (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (xs ys : List ℕ)
    (p q : NativeC60ETLocalPath xs ys) :
    Quotient.mk (nativeC60EVLocalActionSetoid S F word start xs ys) p =
      Quotient.mk (nativeC60EVLocalActionSetoid S F word start xs ys) q :=
  Quotient.sound (nativeC60EVLocalActionEq_all_parallel S F word r start p q)

end C60ActualAQActionFibers

#print axioms nativeC60EVLocalActionEq
#print axioms nativeC60EVLocalActionSetoid
#print axioms nativeC60EVLocalActionEq_all_parallel
#print axioms nativeC60EVZeroActionFiber_nontrivial
#print axioms nativeC60EVZeroAction_not_injective
#print axioms nativeC60EVZeroAction_no_history_decoder
#print axioms nativeC60EVLocalActionQuotient_singleton

end
end Kuu.F112.Physical
