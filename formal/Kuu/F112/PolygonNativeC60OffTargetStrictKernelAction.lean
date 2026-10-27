import Kuu.F112.PolygonNativeC60TypedKernelCompleteness
import Mathlib.Tactic.Group

/-!
# F112-P94D3CS — actual off-target typed forks in the C60 strict kernel

CR identifies an exact original signed-chain existence criterion for a
nontrivial kernel. CS isolates a new, CHECKABLE finite two-edge witness.

Fix an original dependent BC generator base : a ⟶ b. If there are
two DISTINCT actual dependent BC generators g,h : a ⟶ c with c ≠ b,
the signed loop g ; h⁻¹ has full nontrivial BW holonomy, while the
CN decoder centred on base annihilates both distinct off-target codes.
Hence this loop is a NONIDENTITY element in the TRUE CO strict isotropy
retraction kernel under EVERY finite outer AQ context.

Moreover, the true kernel loop does not commute with a lifted genuine
CN fork letter. Reduced four-letter free words prove noncommutation,
so the ACTUAL CP conjugation action is nontrivial under precisely this
typed alternative-terminal hypothesis. No assumed abelianization or
additional geometric relation is used.

Independently, CJ's physical all-context positive-successor no-go
implies that no original positive BC primitive is a self loop; no two
same-sign positive or negative primitives can be consecutive. These
are exact typed 15D restrictions, not graph-theoretic replacements.

Existence of physical g,h,c with the alternative terminal c ≠ b is
NOT assumed or asserted. The theorem is a conditional genuine C60
construction and a sharply localized geometric obstruction.
No Gray, new axioms, sorry/admit, or public proof roots.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

section OriginalCode

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Decode the exact ORIGINAL dependent target 15D object from
the entire BC code (context, lower endpoints, and original generator). -/
def nativeC60CSCodeTarget (code : NativeC60BVGeneratorCode S) : L.Total :=
  nativeC60BCContextTotal F code.1 code.2.2.1

/-- A BC code determines its genuine original target even if the
context is not injective on its raw underlying fourteen-cell values. -/
theorem nativeC60CSCodeTarget_apply {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60CSCodeTarget S F (nativeC60BVGeneratorCode S F g) = b := by
  rcases g with ⟨w, x, y, ⟨gen, hx, hy⟩⟩
  exact hy.symm

/-- Different actual typed terminal 15D objects cannot share the same
COMPLETE BC generator provenance code. -/
theorem nativeC60CSCodeTarget_eq
    {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b)
    (h : (nativeC60BCClosedSignature S F).Gen a c)
    (heq : nativeC60BVGeneratorCode S F g =
      nativeC60BVGeneratorCode S F h) : b = c := by
  calc
    b = nativeC60CSCodeTarget S F
      (nativeC60BVGeneratorCode S F g) :=
        (nativeC60CSCodeTarget_apply S F g).symm
    _ = nativeC60CSCodeTarget S F
      (nativeC60BVGeneratorCode S F h) := congrArg (nativeC60CSCodeTarget S F) heq
    _ = c := nativeC60CSCodeTarget_apply S F h

/-- A generator with the same source but another ORIGINAL 15D terminal
is outside the CN alphabet for the chosen base, as checked on whole
provenance codes rather than a scalar observer. -/
theorem nativeC60CSOffTargetCode_ne_parallel
    {a b c : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (g : (nativeC60BCClosedSignature S F).Gen a c)
    (hc : c ≠ b)
    (j : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60BVGeneratorCode S F j ≠ nativeC60BVGeneratorCode S F g := by
  intro heq
  exact hc (nativeC60CSCodeTarget_eq S F j g heq).symm

/-- The ACTUAL CN decoder annihilates every off-target primitive:
this is about the existing freely generated code alphabet, not a
new imposed geometric quotient. -/
theorem nativeC60CSOffTarget_decode_zero
    {a b c : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (g : (nativeC60BCClosedSignature S F).Gen a c)
    (hc : c ≠ b) :
    nativeC60CNDecodeLetter S F base
      (nativeC60BVGeneratorCode S F g) = 1 := by
  classical
  have hn : ¬ ∃ j : NativeC60CNForkAlphabet S F base,
      nativeC60CNLetterCode S F base j = nativeC60BVGeneratorCode S F g := by
    rintro ⟨j, hj⟩
    exact nativeC60CSOffTargetCode_ne_parallel S F base g hc j.val hj
  simp only [nativeC60CNDecodeLetter, dif_neg hn]

/-- The mixed-sign original two-edge loop of off-target parallel
generators is decoded to identity even though its BW word need
not be identity. -/
theorem nativeC60CSOffTargetFork_decode_zero
    {a b c : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (g h : (nativeC60BCClosedSignature S F).Gen a c)
    (hc : c ≠ b) :
    nativeC60CNRetraction S F base
      (nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h)) = 1 := by
  change nativeC60CNRetraction S F base
    (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
      (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹) = 1
  rw [map_mul, map_inv]
  change nativeC60CNDecodeLetter S F base (nativeC60BVGeneratorCode S F g) *
    (nativeC60CNDecodeLetter S F base (nativeC60BVGeneratorCode S F h))⁻¹ = 1
  rw [nativeC60CSOffTarget_decode_zero S F base g hc,
    nativeC60CSOffTarget_decode_zero S F base h hc]
  simp

/-- CONCRETE actual strict kernel nonidentity witness, built from
two original dependent BC generators of an alternative target, with
all original 15D sources/targets and every finite outer AQ context. -/
theorem nativeC60CSOffTargetFork_kernel_nontrivial
    (word : List Bool) {a b c : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (g h : (nativeC60BCClosedSignature S F).Gen a c)
    (hc : c ≠ b) (hgh : g ≠ h) :
    ∃ k : NativeC60CPKernel S F word base, k ≠ 1 := by
  have hmem : nativeC60CORawLoop S F word
      (nativeC60CKMixedFork S F g h) ∈
      NativeC60CPKernel S F word base := by
    apply (nativeC60CQRawLoop_mem_kernel_iff S F word base
      (nativeC60CKMixedFork S F g h)).mpr
    exact nativeC60CSOffTargetFork_decode_zero S F base g h hc
  have hne : nativeC60CORawLoop S F word
      (nativeC60CKMixedFork S F g h) ≠ 1 :=
    nativeC60CQRawLoop_ne_one_of_full S F word
      (nativeC60CKMixedFork S F g h)
      (nativeC60CKDistinct_fork_nontrivial S F g h hgh)
  refine ⟨⟨nativeC60CORawLoop S F word
    (nativeC60CKMixedFork S F g h), hmem⟩, ?_⟩
  intro hk
  apply hne
  simpa only [Subgroup.coe_one] using congrArg Subtype.val hk

end OriginalCode

section FreeGroupComparison

variable {α : Type u}

/-- Noncommutation of two genuine signed free forks when the two
four-letter words are REDUCED and have different original first letters.
No abelian invariant is used; the proof retains the entire signed word. -/
theorem nativeC60CSFourLetterForks_noncommute
    (A B C D : α) (hAB : A ≠ B) (hCD : C ≠ D)
    (hBC : B ≠ C) (hDA : D ≠ A) (hAC : A ≠ C) :
    (FreeGroup.of A * (FreeGroup.of B)⁻¹) *
        (FreeGroup.of C * (FreeGroup.of D)⁻¹) ≠
      (FreeGroup.of C * (FreeGroup.of D)⁻¹) *
        (FreeGroup.of A * (FreeGroup.of B)⁻¹) := by
  change FreeGroup.mk [(A, true), (B, false), (C, true), (D, false)] ≠
    FreeGroup.mk [(C, true), (D, false), (A, true), (B, false)]
  intro heq
  have hleft : FreeGroup.IsReduced
      [(A, true), (B, false), (C, true), (D, false)] := by
    rw [FreeGroup.isReduced_cons_cons]
    refine ⟨fun h => (hAB h).elim, ?_⟩
    rw [FreeGroup.isReduced_cons_cons]
    refine ⟨fun h => (hBC h).elim, ?_⟩
    rw [FreeGroup.isReduced_cons_cons]
    exact ⟨fun h => (hCD h).elim, FreeGroup.IsReduced.singleton⟩
  have hright : FreeGroup.IsReduced
      [(C, true), (D, false), (A, true), (B, false)] := by
    rw [FreeGroup.isReduced_cons_cons]
    refine ⟨fun h => (hCD h).elim, ?_⟩
    rw [FreeGroup.isReduced_cons_cons]
    refine ⟨fun h => (hDA h).elim, ?_⟩
    rw [FreeGroup.isReduced_cons_cons]
    exact ⟨fun h => (hAB h).elim, FreeGroup.IsReduced.singleton⟩
  obtain ⟨zs, hx, hy⟩ := FreeGroup.Red.exact.mp heq
  have hwords :
      [(A, true), (B, false), (C, true), (D, false)] =
        [(C, true), (D, false), (A, true), (B, false)] :=
    ((FreeGroup.IsReduced.red_iff_eq hleft).mp hx).symm.trans
      ((FreeGroup.IsReduced.red_iff_eq hright).mp hy)
  exact hAC (congrArg Prod.fst (List.cons.inj hwords).1)

end FreeGroupComparison

section ActualAction

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- An off-target signed true-kernel loop DOES NOT commute with any
selected original CN fork letter. Different terminal 15D types make
cross-alphabet cancellation impossible in the reduced four-letter words. -/
theorem nativeC60CSOffTargetFork_free_noncommute
    {a b c : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (j : NativeC60CNForkAlphabet S F base)
    (g h : (nativeC60BCClosedSignature S F).Gen a c)
    (hc : c ≠ b) (hgh : g ≠ h) :
    nativeC60CNEmbed S F base (FreeGroup.of j) *
        nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h) ≠
      nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h) *
        nativeC60CNEmbed S F base (FreeGroup.of j) := by
  have hCD : nativeC60BVGeneratorCode S F g ≠
      nativeC60BVGeneratorCode S F h := by
    intro hcode
    exact hgh (nativeC60BVGeneratorCode_injective S F hcode)
  have hBC : nativeC60BVGeneratorCode S F base ≠
      nativeC60BVGeneratorCode S F g :=
    nativeC60CSOffTargetCode_ne_parallel S F base g hc base
  have hDA : nativeC60BVGeneratorCode S F h ≠
      nativeC60CNLetterCode S F base j :=
    (nativeC60CSOffTargetCode_ne_parallel S F base h hc j.val).symm
  have hAC : nativeC60CNLetterCode S F base j ≠
      nativeC60BVGeneratorCode S F g :=
    nativeC60CSOffTargetCode_ne_parallel S F base g hc j.val
  have h := nativeC60CSFourLetterForks_noncommute
    (nativeC60CNLetterCode S F base j)
    (nativeC60BVGeneratorCode S F base)
    (nativeC60BVGeneratorCode S F g)
    (nativeC60BVGeneratorCode S F h)
    (nativeC60CNLetterCode_ne_base S F base j)
    hCD hBC hDA hAC
  change (FreeGroup.of (nativeC60CNLetterCode S F base j) *
      (FreeGroup.of (nativeC60BVGeneratorCode S F base))⁻¹) *
    (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
      (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹) ≠
    (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
      (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹) *
    (FreeGroup.of (nativeC60CNLetterCode S F base j) *
      (FreeGroup.of (nativeC60BVGeneratorCode S F base))⁻¹)
  exact h

/-- Genuine nontriviality of the ACTUAL CP kernel conjugation action,
using the independent true-kernel original typed loop and the original
free-fork letter. This is not an action on code observations. -/
theorem nativeC60CSOffTargetFork_action_nontrivial
    (word : List Bool) {a b c : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (j : NativeC60CNForkAlphabet S F base)
    (g h : (nativeC60BCClosedSignature S F).Gen a c)
    (hc : c ≠ b) (hgh : g ≠ h) :
    nativeC60CPAction S F word base (FreeGroup.of j) ≠ 1 := by
  have hmem : nativeC60CORawLoop S F word
      (nativeC60CKMixedFork S F g h) ∈ NativeC60CPKernel S F word base := by
    apply (nativeC60CQRawLoop_mem_kernel_iff S F word base
      (nativeC60CKMixedFork S F g h)).mpr
    exact nativeC60CSOffTargetFork_decode_zero S F base g h hc
  let k : NativeC60CPKernel S F word base :=
    ⟨nativeC60CORawLoop S F word (nativeC60CKMixedFork S F g h), hmem⟩
  apply nativeC60CQGenericAction_nontrivial_of_noncommute
    (nativeC60CORetraction S F word base)
    (nativeC60COEmbed S F word base) (FreeGroup.of j) k
  intro heq
  have h := congrArg (nativeC60COHolonomy S F word a) heq
  change nativeC60COHolonomy S F word a
      (nativeC60COEmbed S F word base (FreeGroup.of j) *
        nativeC60CORawLoop S F word (nativeC60CKMixedFork S F g h)) =
    nativeC60COHolonomy S F word a
      (nativeC60CORawLoop S F word (nativeC60CKMixedFork S F g h) *
        nativeC60COEmbed S F word base (FreeGroup.of j)) at h
  simp only [map_mul, nativeC60COEmbed_holonomy_apply,
    nativeC60CORawLoop_holonomy] at h
  have hdown := congrArg (nativeC60BXFreeUnprefix S word) h
  simp only [map_mul, nativeC60BXFreeUnprefix_prefix] at hdown
  exact (nativeC60CSOffTargetFork_free_noncommute S F base j g h hc hgh) hdown

end ActualAction

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

/-- PHYSICAL unconditional all-context no-go: a primitive at an
actual original proof-bearing 15D object can never be a self-loop. -/
theorem nativeK5CSNo_positive_self_primitive
    (W : NativeK5StructuralThirteenCell p U V)
    {a : (nativeK5AXBaseLayer W).Total}
    (loop : (nativeK5BCSignature W).Gen a a) : False :=
  (nativeK5CJNo_composable_positive_generators W loop) ⟨loop⟩

/-- Two consecutive original positive typed 16D primitives cannot
compose, regardless of independent genuine finite AQ contexts. -/
theorem nativeK5CSNo_adjacent_positive
    (W : NativeK5StructuralThirteenCell p U V)
    {a b c : (nativeK5AXBaseLayer W).Total}
    (first : (nativeK5BCSignature W).Gen a b)
    (second : (nativeK5BCSignature W).Gen b c) : False :=
  (nativeK5CJNo_composable_positive_generators W first) ⟨second⟩

/-- The DUAL: two consecutive actual NEGATIVE dependent generators
cannot compose; their reversed positive certificates would violate CJ. -/
theorem nativeK5CSNo_adjacent_negative
    (W : NativeK5StructuralThirteenCell p U V)
    {a b c : (nativeK5AXBaseLayer W).Total}
    (first : (nativeK5BCSignature W).Gen b a)
    (second : (nativeK5BCSignature W).Gen c b) : False :=
  nativeK5CSNo_adjacent_positive W second first

/-- An actual original positive BC source cannot simultaneously be
the target of any other positive BC primitive, so a based signed loop
cannot begin with a negative step. -/
theorem nativeK5CSNo_incoming_at_positive_base
    (W : NativeK5StructuralThirteenCell p U V)
    {a b c : (nativeK5AXBaseLayer W).Total}
    (base : (nativeK5BCSignature W).Gen a b)
    (incoming : (nativeK5BCSignature W).Gen c a) : False :=
  nativeK5CSNo_adjacent_positive W incoming base

/-- Genuine PHYSICAL C60 obstruction: a second, unequal parallel
primitive pair out of the same original 15D source, but with a
different original 15D target, forces a NONTRIVIAL actual kernel
in EVERY independently chosen outer finite AQ context. -/
theorem nativeK5CSPhysical_offtarget_kernel_nontrivial
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (c : (nativeK5AXBaseLayer W).Total)
    (g h : (nativeK5BCSignature W).Gen
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) c)
    (hc : c ≠ nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))
    (hgh : g ≠ h) :
    ∃ k : NativeC60CPKernel
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner), k ≠ 1 :=
  nativeC60CSOffTargetFork_kernel_nontrivial
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    outer (nativeK5CKAtomGenerator W R inner) g h hc hgh

/-- The SAME genuine off-target physical fork makes the actual
noncommutative free-fork action nontrivial at EVERY outer context. -/
theorem nativeK5CSPhysical_offtarget_action_nontrivial
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (c : (nativeK5AXBaseLayer W).Total)
    (g h : (nativeK5BCSignature W).Gen
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) c)
    (hc : c ≠ nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))
    (hgh : g ≠ h) :
    nativeC60CPAction (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner)
        (FreeGroup.of (nativeK5CNReflLetter W R inner)) ≠ 1 :=
  nativeC60CSOffTargetFork_action_nontrivial
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    outer (nativeK5CKAtomGenerator W R inner)
    (nativeK5CNReflLetter W R inner) g h hc hgh

end PhysicalC60

#print axioms nativeC60CSCodeTarget_apply
#print axioms nativeC60CSCodeTarget_eq
#print axioms nativeC60CSOffTargetCode_ne_parallel
#print axioms nativeC60CSOffTarget_decode_zero
#print axioms nativeC60CSOffTargetFork_decode_zero
#print axioms nativeC60CSOffTargetFork_kernel_nontrivial
#print axioms nativeC60CSFourLetterForks_noncommute
#print axioms nativeC60CSOffTargetFork_free_noncommute
#print axioms nativeC60CSOffTargetFork_action_nontrivial
#print axioms nativeK5CSNo_positive_self_primitive
#print axioms nativeK5CSNo_adjacent_positive
#print axioms nativeK5CSNo_adjacent_negative
#print axioms nativeK5CSNo_incoming_at_positive_base
#print axioms nativeK5CSPhysical_offtarget_kernel_nontrivial
#print axioms nativeK5CSPhysical_offtarget_action_nontrivial

end
end Kuu.F112.Physical
