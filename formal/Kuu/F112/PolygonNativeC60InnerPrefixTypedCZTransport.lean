import Kuu.F112.PolygonNativeC60InnerPrefixParityObstruction

/-!
# F112-P94D3DH — genuine original CZ certificates under strict inner-prefix transport

DG reduces full inner-prefix DC parity naturality to kernel inclusion
and two true original proof-bearing symm-depth tests. DH discharges
the two tests by tracking the ORIGINAL 14D/15D witness and the complete
16D generator code, rather than inspecting only scalar parity values.

Under arbitrary finite inner shift, BV/CU preserve both precise dependent
15D boundaries and shift the original BC generator provenance. The
actual physical conservative atom generator and every genuine CZ symm-depth
generator have exactly covariant complete BW codes. The noncommutative
CN mixed-fork free word therefore has exact prefix covariance, and
CD's original strict free-holonomy faithfulness upgrades this to
equality of ACTUAL strict automorphisms through DF's genuine group
equivalence. Thus the full native FreeGroup Nat proof-witness family
is transported strictly (not merely its measured parity).

Consequently the two DG original proof-bearing witness tests hold
unconditionally for all genuine finite AQ inner and outer contexts.
Full naturality then has exactly ONE remaining obstruction, kernel
inclusion; it is not asserted without proof. It must be discharged
using the entire original CN alphabet, including non-CZ proofs.

No synthetic geometric 16D filler, Gray, new axioms, sorry or admit.
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

/-- The genuine native Type-valued conservative proof depth does not
depend on its finite AQ frame word. No identification of proof trees. -/
theorem nativeK5DHCodeIndex_prefix
    (W : NativeK5StructuralThirteenCell p U V)
    (shift : List Bool)
    (code : NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)) :
    nativeK5CZCodeIndex W (nativeC60BWCodePrefix
        (nativeK5AXKuuSignature W) shift code) =
      nativeK5CZCodeIndex W code := by
  rcases code with ⟨word, data⟩
  rfl

/-- Complete 16D proof code of each original CZ n-generator, not
only its parity, persists under physical finite inner framing. -/
theorem nativeK5DHCZCode_inner_shift
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool) (n : Nat) :
    nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5CZGenerator W R (shift ++ inner) n) =
      nativeC60BWCodePrefix (nativeK5AXKuuSignature W) shift
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CZGenerator W R inner n)) :=
  nativeK5DEOriginalPositiveCode_prefix W inner shift (nativeK5CZCell W R n)

/-- Even the distinguished excluded original CN base retains its
FULL original proof provenance; no new generator selection. -/
theorem nativeK5DHBaseCode_inner_shift
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool) :
    nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5CKAtomGenerator W R (shift ++ inner)) =
      nativeC60BWCodePrefix (nativeK5AXKuuSignature W) shift
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner)) := by
  rfl

/-- Exact NONCOMMUTATIVE original CN mixed-fork word equality.
This includes the inverse base generator, so retaining just the
symm-depth parity would have been insufficient. -/
theorem nativeK5DHCZCNFree_inner_shift
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool) (n : Nat) :
    nativeC60BWFreePrefix (nativeK5AXKuuSignature W) shift
      (nativeC60CNEmbed (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner)
        (FreeGroup.of (nativeK5CZLetter W R inner n))) =
      nativeC60CNEmbed (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R (shift ++ inner))
        (FreeGroup.of (nativeK5CZLetter W R (shift ++ inner) n)) := by
  simp only [nativeC60CNEmbed, FreeGroup.lift_apply_of,
    nativeC60BWFreePrefix, map_mul, map_inv, FreeGroup.map.of]
  change
    FreeGroup.of (nativeC60BWCodePrefix (nativeK5AXKuuSignature W) shift
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CZGenerator W R inner n))) *
    (FreeGroup.of (nativeC60BWCodePrefix (nativeK5AXKuuSignature W) shift
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner))))⁻¹ =
    FreeGroup.of (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CZGenerator W R (shift ++ inner) n)) *
    (FreeGroup.of (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R (shift ++ inner))))⁻¹
  rw [nativeK5DHCZCode_inner_shift, nativeK5DHBaseCode_inner_shift]

/-- MAIN typed DH strict transport theorem. All genuinely independent
original n-times-symm 15D certificates produce EXACTLY THE SAME
actual strict automorphism after the true DF inner-prefix group
equivalence as the original prefixed CZ certificate.
The proof uses BW free-word equality AND CO's faithfulness
on actual strict automorphisms, not a quotient defined by parity. -/
theorem nativeK5DHInnerPrefixStrict_CZ
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) (n : Nat) :
    nativeK5DFInnerPrefixStrictEquiv W R inner outer shift
        (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n)) =
      nativeK5CZFreeNatEmbed W R (shift ++ inner) outer (FreeGroup.of n) := by
  let S := nativeK5AXKuuSignature W
  let F := nativeK5BCFrame W
  let base := nativeK5CKAtomGenerator W R inner
  let targetBase := nativeK5CKAtomGenerator W R (shift ++ inner)
  apply nativeC60COHolonomy_injective S F outer
    (nativeK5CHSource W (shift ++ inner) (nativeK5CKConservativeRefl W R))
  rw [nativeK5DFInnerPrefixStrictEquiv_BW]
  change
    nativeC60BWFreePrefix S (outer ++ shift)
      (nativeC60CNEmbed S F base
        ((FreeGroup.map (nativeK5CZLetter W R inner)) (FreeGroup.of n))) =
    nativeC60COHolonomy S F outer _ 
      (nativeC60COEmbed S F outer targetBase
        ((FreeGroup.map (nativeK5CZLetter W R (shift ++ inner))) (FreeGroup.of n)))
  rw [FreeGroup.map.of, FreeGroup.map.of, nativeC60COEmbed_holonomy_apply]
  calc
    nativeC60BWFreePrefix S (outer ++ shift)
        (nativeC60CNEmbed S F base
          (FreeGroup.of (nativeK5CZLetter W R inner n))) =
      nativeC60BWFreePrefix S outer
        (nativeC60BWFreePrefix S shift
          (nativeC60CNEmbed S F base
            (FreeGroup.of (nativeK5CZLetter W R inner n)))) := by
        exact (DFunLike.congr_fun
          (nativeC60DDFreePrefix_append S outer shift) _).symm
    _ = nativeC60BWFreePrefix S outer
        (nativeC60CNEmbed S F targetBase
          (FreeGroup.of (nativeK5CZLetter W R (shift ++ inner) n))) := by
      exact congrArg (nativeC60BWFreePrefix S outer)
        (nativeK5DHCZCNFree_inner_shift W R inner shift n)

/-- Not merely the two classes: every signed, reduced or unreduced
original CZ free word is transported to the true strict group image
of its WHOLE original Type-valued 15D proof family. -/
theorem nativeK5DHInnerPrefixStrict_CZ_hom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).toMonoidHom.comp
      (nativeK5CZFreeNatEmbed W R inner outer) =
      nativeK5CZFreeNatEmbed W R (shift ++ inner) outer := by
  apply FreeGroup.ext_hom
  intro n
  exact nativeK5DHInnerPrefixStrict_CZ W R inner outer shift n

/-- The DC coarse partial invariant of EVERY original CZ free word
is preserved by the TRUE strict inner-prefix group equivalence,
without erasing complete noncommutative 16D evidence. -/
theorem nativeK5DHInnerPrefixStrict_CZ_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) (z : FreeGroup Nat) :
    nativeK5DGInnerPrefixTransportedParity W R inner outer shift
        (nativeK5CZFreeNatEmbed W R inner outer z) =
      nativeK5DCParityQuotient W R inner outer
        (nativeK5CZFreeNatEmbed W R inner outer z) := by
  change nativeK5DCParityQuotient W R (shift ++ inner) outer
        (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift
          (nativeK5CZFreeNatEmbed W R inner outer z)) =
      nativeK5DCParityQuotient W R inner outer
        (nativeK5CZFreeNatEmbed W R inner outer z)
  have h := DFunLike.congr_fun
    (nativeK5DHInnerPrefixStrict_CZ_hom W R inner outer shift) z
  change nativeK5DFInnerPrefixStrictEquiv W R inner outer shift
      (nativeK5CZFreeNatEmbed W R inner outer z) =
    nativeK5CZFreeNatEmbed W R (shift ++ inner) outer z at h
  rw [h]
  exact (nativeK5DETwoInnerTypedCZ_parity_word
    W R inner outer (shift ++ inner) outer z).symm

/-- FIRST original proof-bearing DG test: n=0 is truly preserved,
including its original full CN/BW signed-loop provenance. -/
theorem nativeK5DHOriginalParityTestZero_preserved
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DGInnerPrefixTransportedParity W R inner outer shift
        (nativeK5DGOriginalParityTestZero W R inner outer) =
      FreeGroup.of false := by
  change nativeK5DGInnerPrefixTransportedParity W R inner outer shift
    (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of 0)) = _
  rw [nativeK5DHInnerPrefixStrict_CZ_parity]
  exact nativeK5DCParityQuotient_CZ W R inner outer 0

/-- SECOND original proof-bearing DG test: n=1 is truly preserved
without identifying n=1 with n=0 in the original strict isotropy. -/
theorem nativeK5DHOriginalParityTestOne_preserved
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DGInnerPrefixTransportedParity W R inner outer shift
        (nativeK5DGOriginalParityTestOne W R inner outer) =
      FreeGroup.of true := by
  change nativeK5DGInnerPrefixTransportedParity W R inner outer shift
    (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of 1)) = _
  rw [nativeK5DHInnerPrefixStrict_CZ_parity]
  exact nativeK5DCParityQuotient_CZ W R inner outer 1

/-- DG's three obligations collapse to ONE EXACT remaining
obstruction for every physical finite inner/outer AQ context:
the original DC quotient kernel must be preserved by DF.
No silent claim that the kernel inclusion has already been proved. -/
theorem nativeK5DHInnerPrefix_full_parity_iff_kernel
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DGInnerPrefixTransportedParity W R inner outer shift =
        nativeK5DCParityQuotient W R inner outer ↔
      (nativeK5DCParityQuotient W R inner outer).ker ≤
        (nativeK5DGInnerPrefixTransportedParity W R inner outer shift).ker := by
  rw [nativeK5DGInnerPrefix_full_parity_iff]
  constructor
  · exact fun h => h.1
  · intro hk
    exact ⟨hk, nativeK5DHOriginalParityTestZero_preserved W R inner outer shift,
      nativeK5DHOriginalParityTestOne_preserved W R inner outer shift⟩

end GenuinePhysicalC60

#print axioms nativeK5DHCodeIndex_prefix
#print axioms nativeK5DHCZCode_inner_shift
#print axioms nativeK5DHBaseCode_inner_shift
#print axioms nativeK5DHCZCNFree_inner_shift
#print axioms nativeK5DHInnerPrefixStrict_CZ
#print axioms nativeK5DHInnerPrefixStrict_CZ_hom
#print axioms nativeK5DHInnerPrefixStrict_CZ_parity
#print axioms nativeK5DHOriginalParityTestZero_preserved
#print axioms nativeK5DHOriginalParityTestOne_preserved
#print axioms nativeK5DHInnerPrefix_full_parity_iff_kernel

end
end Kuu.F112.Physical
