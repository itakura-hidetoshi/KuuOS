import Kuu.F112.PolygonNativeC60StrictCompositionKernelCocycle

/-!
# F112-P94D3DM — actual whole strict inner-prefix coherence from original CN/BV

DL isolates the exact noncommutative strict composition defect and proves
the COMPLETE original BV code of every two-stage CN letter coincides with
the single ordered-prefix letter. This module upgrades that proof-code
coincidence to equality of genuine CN letters and then to equality of the
ACTUAL strict automorphisms, not merely their partial DC parity or the
kernel quotient.

At a given genuine 14D fiber and two independent Type-valued 15D
boundaries, finite prefix concatenation only reassociates the same word.
We first eliminate the dependent associator explicitly; the original
16D code remains unchanged and BV's generator-code injectivity gives
the same genuine CN alphabet letter, including its excluded CK atom.

DI already identifies EACH genuine DF strict inner-prefix group
equivalence with the complete free CN generator shift. Hence the two
successive strict transports and the single combined strict transport
agree on every original CN generator. FreeGroup.ext_hom extends this
equality to arbitrary signed noncommutative words, and CY's proved
surjective actual free-isotropy equivalence extends it to EVERY
original strict automorphism.

Consequently DL's actual ORIGINAL strict defect is unconditionally one.
This proof does not use the noninjective DC parity quotient to infer
strict equality; it relies on genuine 16D proof codes, original CY and
exact dependent strict group transport. Neither this strict equality nor
the proof witnesses introduce new geometric sixteen-cell relations.

Finite C60 gauge context, strict Kuu and independent Kuu presentation
distinction, all 107 published roots, existing no-go and original
Type-valued 14D/15D/16D evidence are preserved. No Gray, new axioms,
sorry or admit. Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section PhysicalStrictC60Composition

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

/-- An equality of ORIGINAL context words transports a genuine typed
CN letter without changing the underlying dependent proof certificate.
Only propositional equality of the prefix WORD is eliminated. -/
theorem nativeK5DMContextReassoc_CNLetter
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    {a b : List Bool} (h : a = b)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R a))
    (k : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R b))
    (hcode : nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) k.val =
      nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) j.val) :
    (h.symm ▸ k) = j := by
  cases h
  apply Subtype.ext
  exact nativeC60BVGeneratorCode_injective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) hcode

/-- Full ORIGINAL typed CN letters compose in the correct noncommutative
AQ order. This is stronger than DL's mere equality of BV codes:
it is equality of genuine 16D generators with exact 15D endpoints. -/
theorem nativeK5DMShiftLetter_twoStep
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift more : List Bool)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)) :
    ((List.append_assoc more shift inner).symm ▸
      nativeK5DIShiftLetter W R (shift ++ inner) more
        (nativeK5DIShiftLetter W R inner shift j)) =
      nativeK5DIShiftLetter W R inner (more ++ shift) j := by
  exact nativeK5DMContextReassoc_CNLetter W R
    (List.append_assoc more shift inner)
    (nativeK5DIShiftLetter W R inner (more ++ shift) j)
    (nativeK5DIShiftLetter W R (shift ++ inner) more
      (nativeK5DIShiftLetter W R inner shift j))
    (nativeK5DLShiftLetter_twoStep_BVCode W R inner shift more j)

/-- Context equality reindexes an ORIGINAL strict group equivalence;
application commutes with dependent equality transport. -/
theorem nativeK5DMContextReassoc_StrictApply
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {a b : List Bool} (h : a = b)
    (e : nativeK5DBIsotropy W R inner outer ≃*
      nativeK5DBIsotropy W R b outer)
    (z : nativeK5DBIsotropy W R inner outer) :
    (h.symm ▸ e) z = (h.symm ▸ (e z)) := by
  cases h
  rfl

/-- Exact naturality of the TRUE CY free-isotropy identification
under equality of the original finite inner AQ context word. -/
theorem nativeK5DMContextReassoc_CY
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (outer : List Bool)
    {a b : List Bool} (h : a = b)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R b)) :
    (h.symm ▸
      nativeK5CYPhysicalFreeIsotropy W R b outer (FreeGroup.of j)) =
      nativeK5CYPhysicalFreeIsotropy W R a outer
        (FreeGroup.of (h.symm ▸ j)) := by
  cases h
  rfl

/-- The TWO original DF strict transport routes are EXACTLY EQUAL
on every physically named ORIGINAL CN generator. This is the key
upgrade from the DL complete BV code theorem to the actual strict
group, using the original DI generator transport and CY. -/
theorem nativeK5DMStrict_comp_letter
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)) :
    nativeK5DLTwoStageStrict W R inner outer shift more
        (nativeK5CYPhysicalFreeIsotropy W R inner outer (FreeGroup.of j)) =
      nativeK5DLOneStageStrict W R inner outer shift more
        (nativeK5CYPhysicalFreeIsotropy W R inner outer (FreeGroup.of j)) := by
  let h := List.append_assoc more shift inner
  let source := nativeK5CYPhysicalFreeIsotropy W R inner outer
  let firstShift := nativeK5DIShiftLetter W R inner shift j
  let secondShift := nativeK5DIShiftLetter W R (shift ++ inner) more firstShift
  let combinedShift := nativeK5DIShiftLetter W R inner (more ++ shift) j
  calc
    nativeK5DLTwoStageStrict W R inner outer shift more
        (source (FreeGroup.of j)) =
      (h.symm ▸
        (nativeK5DFInnerPrefixStrictEquiv W R (shift ++ inner) outer more
          (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift
            (source (FreeGroup.of j))))) := by
      change (h.symm ▸
        ((nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).trans
          (nativeK5DFInnerPrefixStrictEquiv W R (shift ++ inner) outer more)))
            (source (FreeGroup.of j)) = _
      exact nativeK5DMContextReassoc_StrictApply W R inner outer h _ _
    _ = (h.symm ▸
      (nativeK5CYPhysicalFreeIsotropy W R (more ++ (shift ++ inner)) outer
        (FreeGroup.of secondShift))) := by
      rw [nativeK5DIInnerPrefixStrict_letter W R inner outer shift j,
        nativeK5DIInnerPrefixStrict_letter W R (shift ++ inner) outer more firstShift]
    _ = nativeK5CYPhysicalFreeIsotropy W R ((more ++ shift) ++ inner) outer
        (FreeGroup.of (h.symm ▸ secondShift)) :=
      nativeK5DMContextReassoc_CY W R outer h secondShift
    _ = nativeK5CYPhysicalFreeIsotropy W R ((more ++ shift) ++ inner) outer
        (FreeGroup.of combinedShift) := by
      rw [nativeK5DMShiftLetter_twoStep W R inner shift more j]
    _ = nativeK5DLOneStageStrict W R inner outer shift more
        (source (FreeGroup.of j)) :=
      (nativeK5DIInnerPrefixStrict_letter W R inner outer (more ++ shift) j).symm

/-- The two ORIGINAL strict-group maps coincide on the WHOLE genuine
noncommutative CN free group, not only on named generators or parity
classes. FreeGroup.ext_hom preserves signed inverses and ordering. -/
theorem nativeK5DMStrict_comp_CN_hom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool) :
    (nativeK5DLTwoStageStrict W R inner outer shift more).toMonoidHom.comp
        (nativeK5CYPhysicalFreeIsotropy W R inner outer).toMonoidHom =
      (nativeK5DLOneStageStrict W R inner outer shift more).toMonoidHom.comp
        (nativeK5CYPhysicalFreeIsotropy W R inner outer).toMonoidHom := by
  apply FreeGroup.ext_hom
  intro j
  exact nativeK5DMStrict_comp_letter W R inner outer shift more j

/-- MAIN DM: the genuine DF inner-prefix strict isomorphisms obey
the finite ordered AQ composition law on EVERY actual C60 strict
automorphism, not only after quotienting by DC parity.
No geometric extra 16-cell has been inserted. -/
theorem nativeK5DMInnerPrefixStrict_comp
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool) :
    nativeK5DLTwoStageStrict W R inner outer shift more =
      nativeK5DLOneStageStrict W R inner outer shift more := by
  apply MulEquiv.ext
  intro z
  obtain ⟨x, rfl⟩ := (nativeK5CYPhysicalFreeIsotropy W R inner outer).surjective z
  exact DFunLike.congr_fun (nativeK5DMStrict_comp_CN_hom W R inner outer shift more) x

/-- The previously classified ORIGINAL noncommutative strict composition
cocycle is unconditionally trivial for genuine finite inner AQ shifts
of the selected no-extra-relations C60 strict presentation. -/
theorem nativeK5DMStrictCompositionDefect_eq_one
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DLStrictCompositionDefect W R inner outer shift more z = 1 := by
  apply (nativeK5DLStrictCompositionDefect_zero_iff W R inner outer shift more z).mpr
  exact DFunLike.congr_fun (nativeK5DMInnerPrefixStrict_comp W R inner outer shift more) z

/-- Same strict equality implies full original noncommutative BW
holonomy equality at the exact target 15D source proof boundary.
The proof does not use the coarser DC FreeGroup Bool quotient. -/
theorem nativeK5DMInnerPrefixStrict_comp_BW
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CHSource W ((more ++ shift) ++ inner)
          (nativeK5CKConservativeRefl W R))
        (nativeK5DLTwoStageStrict W R inner outer shift more z) =
      nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CHSource W ((more ++ shift) ++ inner)
          (nativeK5CKConservativeRefl W R))
        (nativeK5DLOneStageStrict W R inner outer shift more z) := by
  rw [nativeK5DMInnerPrefixStrict_comp W R inner outer shift more]

end PhysicalStrictC60Composition

#print axioms nativeK5DMContextReassoc_CNLetter
#print axioms nativeK5DMShiftLetter_twoStep
#print axioms nativeK5DMContextReassoc_StrictApply
#print axioms nativeK5DMContextReassoc_CY
#print axioms nativeK5DMStrict_comp_letter
#print axioms nativeK5DMStrict_comp_CN_hom
#print axioms nativeK5DMInnerPrefixStrict_comp
#print axioms nativeK5DMStrictCompositionDefect_eq_one
#print axioms nativeK5DMInnerPrefixStrict_comp_BW

end
end Kuu.F112.Physical
