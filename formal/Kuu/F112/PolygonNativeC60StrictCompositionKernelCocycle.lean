import Kuu.F112.PolygonNativeC60ParityQuotientComposition
import Mathlib.Tactic.Group

/-!
# F112-P94D3DL — full strict inner-prefix composition defect and kernel cocycle

DK constructs canonical composition for the genuine DC strict kernel
quotients but does NOT identify their underlying two-stage and one-stage
DF whole-group automorphisms. DL keeps this distinction explicit.

For two group maps A,B with identical original DC quotient, define
the *actual strict* defect δ(x) = A(x) * B(x)⁻¹.
We prove this exact defect belongs to the ORIGINAL target quotient
kernel, is normalized, and obeys the NONABELIAN crossed cocycle law

  δ(x*y) = δ(x) * B(x) * δ(y) * B(x)⁻¹.

Vanishing pointwise is equivalent to exact equality of strict group
homomorphisms, never merely equality of observed quotients.

Specialize to the complete original C60 14D/15D Type-valued evidence
and its selected no-extra-relations strict 16D presentation. Reassociate
finite AQ words by actual List.append_assoc without reordering either
prefix. The true two-stage DF equivalence and the one-stage DF
equivalence take values in the SAME exact strict target group. Their
defect lies in the genuine DC kernel by DK/DI. Its vanishing is
equivalent to equality of the FULL noncommutative BW holonomy, because
CO proved faithfulness on these original strict automorphisms.

Finally we prove the exact 16D BV proof-code of every actual original
CN generator is equal after two consecutive inner shifts and a single
combined inner shift. The code still carries the original dependent
15D source/target proof and underlying 14D boundaries; this is not a
new geometric 16-cell comparison. We do not infer unproved raw strict
composition from equality of coarse parity alone.

Strict Kuu retained, independent Kuu is a presentation, Gray never
reintroduced, no new axioms/sorry/admit, 107 published roots retained.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDL vDL wDL uD vD uE vE

section GenericNoncommutativeDefect

variable {G : Type uDL} {H : Type vDL} {Q : Type wDL}
variable [Group G] [Group H] [Group Q]

/-- Difference of two actual strict group maps, formed INSIDE the
original target group. Unlike a quotient-valued measurement, this
keeps the exact noncommutative order of the two routes. -/
def nativeC60DLStrictDefect
    (a b : G →* H) (z : G) : H :=
  a z * (b z)⁻¹

/-- Both strict routes agree exactly at the original identity. -/
theorem nativeC60DLStrictDefect_one
    (a b : G →* H) :
    nativeC60DLStrictDefect a b 1 = 1 := by
  simp [nativeC60DLStrictDefect]

/-- The true multiplicative discrepancy obeys a nonabelian crossed
cocycle law, twisted by conjugation through the second strict route.
No abelianization, integer charge or graph proxy is involved. -/
theorem nativeC60DLStrictDefect_mul
    (a b : G →* H) (x y : G) :
    nativeC60DLStrictDefect a b (x * y) =
      nativeC60DLStrictDefect a b x * b x *
        nativeC60DLStrictDefect a b y * (b x)⁻¹ := by
  dsimp only [nativeC60DLStrictDefect]
  simp only [map_mul]
  group

/-- Exact inverse coherence, obtained in the ORIGINAL target group
without any assumption of commutativity of the gauge holonomy. -/
theorem nativeC60DLStrictDefect_inv
    (a b : G →* H) (x : G) :
    nativeC60DLStrictDefect a b x⁻¹ =
      (b x)⁻¹ * (nativeC60DLStrictDefect a b x)⁻¹ * b x := by
  dsimp only [nativeC60DLStrictDefect]
  simp only [map_inv]
  group

/-- Kernel containment is an output of parity compatibility, not an
assumption of full strict composition. -/
theorem nativeC60DLStrictDefect_mem_ker
    (q : H →* Q) (a b : G →* H)
    (h : q.comp a = q.comp b) (z : G) :
    nativeC60DLStrictDefect a b z ∈ q.ker := by
  apply (MonoidHom.mem_ker).mpr
  change q (a z * (b z)⁻¹) = 1
  rw [map_mul, map_inv]
  have hz := DFunLike.congr_fun h z
  change q (a z) = q (b z) at hz
  rw [hz]
  exact mul_inv_cancel _

/-- The only exact obstruction to identifying the two ORIGINAL strict
arrows is their real noncommutative discrepancy being the identity. -/
theorem nativeC60DLStrictDefect_eq_one_iff
    (a b : G →* H) (z : G) :
    nativeC60DLStrictDefect a b z = 1 ↔ a z = b z := by
  change a z * (b z)⁻¹ = 1 ↔ a z = b z
  constructor
  · intro hz
    calc
      a z = (a z * (b z)⁻¹) * b z := by group
      _ = 1 * b z := by rw [hz]
      _ = b z := one_mul _
  · intro hz
    rw [hz]
    exact mul_inv_cancel _

/-- ALL strict defects vanish iff the two entire ORIGINAL group maps
are equal. Agreement only after a noninjective quotient is weaker. -/
theorem nativeC60DLStrictDefect_trivial_iff
    (a b : G →* H) :
    (∀ z : G, nativeC60DLStrictDefect a b z = 1) ↔ a = b := by
  constructor
  · intro hz
    apply MonoidHom.ext
    intro z
    exact (nativeC60DLStrictDefect_eq_one_iff a b z).mp (hz z)
  · intro hab z
    subst b
    exact (nativeC60DLStrictDefect_eq_one_iff a a z).mpr rfl

end GenericNoncommutativeDefect

section GenuinePhysicalC60

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

/-- Genuine first-then-second DF strict isomorphism, reindexed only
along the original associative equality of finite AQ prefix WORDS.
We never commute the words and never forget the original typed 15D
source or target. -/
def nativeK5DLTwoStageStrict
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool) :
    nativeK5DBIsotropy W R inner outer ≃*
      nativeK5DBIsotropy W R ((more ++ shift) ++ inner) outer := by
  simpa only [List.append_assoc] using
    ((nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).trans
      (nativeK5DFInnerPrefixStrictEquiv W R (shift ++ inner) outer more))

/-- The genuine one-stage DF strict equivalence for the SAME exact
ordered list of AQ context generators. -/
def nativeK5DLOneStageStrict
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool) :
    nativeK5DBIsotropy W R inner outer ≃*
      nativeK5DBIsotropy W R ((more ++ shift) ++ inner) outer :=
  nativeK5DFInnerPrefixStrictEquiv W R inner outer (more ++ shift)

/-- Retain the actual original DC free-group readout for the two-stage
strict arrow; the proof is DK's physically established genuine two-step
naturality with only list reassociation at the *type* boundary. -/
theorem nativeK5DLTwoStageStrict_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer
        (nativeK5DLTwoStageStrict W R inner outer shift more z) =
      nativeK5DCParityQuotient W R inner outer z := by
  simpa only [nativeK5DLTwoStageStrict, List.append_assoc] using
    (nativeK5DKInnerPrefix_strict_twostep_parity W R inner outer shift more z)

/-- The direct route is parity-natural by DI on the whole original CN
alphabet; no new quotient relations have been imposed. -/
theorem nativeK5DLOneStageStrict_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer
        (nativeK5DLOneStageStrict W R inner outer shift more z) =
      nativeK5DCParityQuotient W R inner outer z := by
  have h := DFunLike.congr_fun
    (nativeK5DIInnerPrefix_full_parity W R inner outer (more ++ shift)) z
  change nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer
      (nativeK5DLOneStageStrict W R inner outer shift more z) =
        nativeK5DCParityQuotient W R inner outer z at h
  exact h

/-- Parity of the WHOLE ORIGINAL two-stage strict group map agrees
with the direct one-stage map, as an equality of true group homs. -/
theorem nativeK5DLStrictRoutes_parity_hom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool) :
    (nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer).comp
        (nativeK5DLTwoStageStrict W R inner outer shift more).toMonoidHom =
      (nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer).comp
        (nativeK5DLOneStageStrict W R inner outer shift more).toMonoidHom := by
  apply MonoidHom.ext
  intro z
  change nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer
      (nativeK5DLTwoStageStrict W R inner outer shift more z) =
    nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer
      (nativeK5DLOneStageStrict W R inner outer shift more z)
  exact (nativeK5DLTwoStageStrict_parity W R inner outer shift more z).trans
    (nativeK5DLOneStageStrict_parity W R inner outer shift more z).symm

/-- ACTUAL ORIGINAL strict composition defect in the final C60
conservative isotropy group, before applying ANY quotient. -/
def nativeK5DLStrictCompositionDefect
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
      nativeK5DBIsotropy W R ((more ++ shift) ++ inner) outer :=
  nativeC60DLStrictDefect
    (nativeK5DLTwoStageStrict W R inner outer shift more).toMonoidHom
    (nativeK5DLOneStageStrict W R inner outer shift more).toMonoidHom z

/-- The strict difference belongs to the ORIGINAL DC quotient kernel
at the fully typed final 15D boundary, not a guessed observer kernel. -/
theorem nativeK5DLStrictCompositionDefect_mem_ker
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DLStrictCompositionDefect W R inner outer shift more z ∈
      (nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer).ker :=
  nativeC60DLStrictDefect_mem_ker
    (nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer)
    (nativeK5DLTwoStageStrict W R inner outer shift more).toMonoidHom
    (nativeK5DLOneStageStrict W R inner outer shift more).toMonoidHom
    (nativeK5DLStrictRoutes_parity_hom W R inner outer shift more) z

/-- The real physical obstruction has the nonabelian crossed cocycle
law in the ORIGINAL whole strict automorphism group, with conjugation
by the direct original DF transport. -/
theorem nativeK5DLStrictCompositionDefect_mul
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z z' : nativeK5DBIsotropy W R inner outer) :
    nativeK5DLStrictCompositionDefect W R inner outer shift more (z * z') =
      nativeK5DLStrictCompositionDefect W R inner outer shift more z *
        nativeK5DLOneStageStrict W R inner outer shift more z *
        nativeK5DLStrictCompositionDefect W R inner outer shift more z' *
        (nativeK5DLOneStageStrict W R inner outer shift more z)⁻¹ :=
  nativeC60DLStrictDefect_mul
    (nativeK5DLTwoStageStrict W R inner outer shift more).toMonoidHom
    (nativeK5DLOneStageStrict W R inner outer shift more).toMonoidHom z z'

/-- EXACT necessary/sufficient condition to eliminate the strict
composition obstruction, pointwise in the original 14D/15D evidence. -/
theorem nativeK5DLStrictCompositionDefect_zero_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DLStrictCompositionDefect W R inner outer shift more z = 1 ↔
      nativeK5DLTwoStageStrict W R inner outer shift more z =
        nativeK5DLOneStageStrict W R inner outer shift more z :=
  nativeC60DLStrictDefect_eq_one_iff
    (nativeK5DLTwoStageStrict W R inner outer shift more).toMonoidHom
    (nativeK5DLOneStageStrict W R inner outer shift more).toMonoidHom z

/-- The obstruction vanishes for EVERY actual original strict loop
if and only if the two actual whole strict transport group maps agree. -/
theorem nativeK5DLStrictCompositionDefect_trivial_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool) :
    (∀ z : nativeK5DBIsotropy W R inner outer,
       nativeK5DLStrictCompositionDefect W R inner outer shift more z = 1) ↔
      nativeK5DLTwoStageStrict W R inner outer shift more =
        nativeK5DLOneStageStrict W R inner outer shift more := by
  constructor
  · intro hz
    apply MulEquiv.ext
    intro z
    exact (nativeK5DLStrictCompositionDefect_zero_iff
      W R inner outer shift more z).mp (hz z)
  · intro h z
    apply (nativeK5DLStrictCompositionDefect_zero_iff
      W R inner outer shift more z).mpr
    exact DFunLike.congr_fun h z

/-- The remaining defect can be detected or ruled out by the
FULL ORIGINAL noncommutative BW strict holonomy. CO's injectivity
makes this a complete strict test, not parity observation alone. -/
theorem nativeK5DLStrictCompositionDefect_zero_iff_BW
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DLStrictCompositionDefect W R inner outer shift more z = 1 ↔
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
  rw [nativeK5DLStrictCompositionDefect_zero_iff]
  constructor
  · exact fun h => congrArg
      (nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CHSource W ((more ++ shift) ++ inner)
          (nativeK5CKConservativeRefl W R))) h
  · exact fun h => (nativeC60COHolonomy_injective
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
      (nativeK5CHSource W ((more ++ shift) ++ inner)
        (nativeK5CKConservativeRefl W R))) h

/-- On every ORIGINAL CN alphabet generator, two consecutive physical
AQ inner shifts preserve exactly the same COMPLETE BV/16D proof
certificate as one shift with the correctly ordered concatenation.
This retains both original 14D/15D boundaries and is stronger than
the coarse parity equality of DK. -/
theorem nativeK5DLShiftLetter_twoStep_BVCode
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift more : List Bool)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)) :
    nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5DIShiftLetter W R (shift ++ inner) more
          (nativeK5DIShiftLetter W R inner shift j)).val =
      nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5DIShiftLetter W R inner (more ++ shift) j).val := by
  rw [nativeK5DIShiftLetter_code W R (shift ++ inner) more
        (nativeK5DIShiftLetter W R inner shift j),
      nativeK5DIShiftLetter_code W R inner shift j,
      nativeK5DIShiftLetter_code W R inner (more ++ shift) j]
  exact (nativeC60DDCodePrefix_append
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) more shift
    (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) j.val)).symm

end GenuinePhysicalC60

#print axioms nativeC60DLStrictDefect
#print axioms nativeC60DLStrictDefect_one
#print axioms nativeC60DLStrictDefect_mul
#print axioms nativeC60DLStrictDefect_inv
#print axioms nativeC60DLStrictDefect_mem_ker
#print axioms nativeC60DLStrictDefect_eq_one_iff
#print axioms nativeC60DLStrictDefect_trivial_iff
#print axioms nativeK5DLTwoStageStrict
#print axioms nativeK5DLOneStageStrict
#print axioms nativeK5DLTwoStageStrict_parity
#print axioms nativeK5DLOneStageStrict_parity
#print axioms nativeK5DLStrictRoutes_parity_hom
#print axioms nativeK5DLStrictCompositionDefect
#print axioms nativeK5DLStrictCompositionDefect_mem_ker
#print axioms nativeK5DLStrictCompositionDefect_mul
#print axioms nativeK5DLStrictCompositionDefect_zero_iff
#print axioms nativeK5DLStrictCompositionDefect_trivial_iff
#print axioms nativeK5DLStrictCompositionDefect_zero_iff_BW
#print axioms nativeK5DLShiftLetter_twoStep_BVCode

end
end Kuu.F112.Physical
