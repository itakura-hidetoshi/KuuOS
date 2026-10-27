import Kuu.F112.PolygonNativeC60InnerPrefixTypedCZTransport

/-!
# F112-P94D3DI — full original CN alphabet and inner-prefix parity naturality

DH proves true strict inner-prefix covariance of every original CZ witness.
DI now treats EVERY original CN parallel 16D certificate, not only the CZ
subfamily. A direct dependent generator shift preserves both original
14D/15D boundaries and the entire BV code. It takes the excluded original
CK atom to the actual excluded target CK atom. Thus it induces a map on the
COMPLETE CN fork alphabet and its noncommutative free group.

Using DF's actual whole-isotropy group equivalence, CO's faithful BW
holonomy, and CY's proven physical CN reconstruction, we identify DF
on every free generator with this original typed shift. The DC parity
index ignores only the finite outer prefix, never the full Type-valued
15D input; its value is therefore preserved on EVERY CN letter,
including all non-CZ letters mapped to false. This proves the entire
DC quotient square, hence DG's remaining kernel inclusion, without
assuming either assertion in advance.

Only the selected no-extra-relations strict Kuu presentation is covered.
No new geometrical 16-cell, no Gray, no axioms, sorry or admit.
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

section OriginalFullCNInnerPrefix

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

/-- Genuine original closed 16D generator inner-prefix, including the
two ORIGINAL, independently dependent 15D endpoints and primitive input.
This is the physical BV shift with endpoint conversion proved by DE/CU. -/
def nativeK5DIShiftGen
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool)
    (g : (nativeK5BCSignature W).Gen
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))
      (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))) :
    (nativeK5BCSignature W).Gen
      (nativeK5CHSource W (shift ++ inner) (nativeK5CKConservativeRefl W R))
      (nativeK5CHTarget W (shift ++ inner) (nativeK5CKConservativeRefl W R)) :=
  ⟨shift ++ g.1, g.2.1, g.2.2.1,
    ⟨g.2.2.2.1,
      ⟨(nativeK5DEInnerSource_prefix W inner shift
           (nativeK5CKConservativeRefl W R)).trans
          ((congrArg (nativeK5BCContext W shift) g.2.2.2.2.1).trans
            (nativeC60BCContextTotal_append (nativeK5BCFrame W)
              shift g.1 g.2.1).symm),
        (nativeK5DEInnerTarget_prefix W inner shift
           (nativeK5CKConservativeRefl W R)).trans
          ((congrArg (nativeK5BCContext W shift) g.2.2.2.2.2).trans
            (nativeC60BCContextTotal_append (nativeK5BCFrame W)
              shift g.1 g.2.2.1).symm)⟩⟩⟩

/-- The FULL original BV code, not only a numerical or Bool readout,
is exactly prefixed; the primitive 14D/15D witness remains untouched. -/
theorem nativeK5DIShiftGen_code
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool)
    (g : (nativeK5BCSignature W).Gen
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))
      (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))) :
    nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5DIShiftGen W R inner shift g) =
      nativeC60BWCodePrefix (nativeK5AXKuuSignature W) shift
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) g) := by
  rfl

/-- No original distinct 16D certificate collapses under an inner prefix. -/
theorem nativeK5DIShiftGen_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool) :
    Function.Injective (nativeK5DIShiftGen W R inner shift) := by
  intro g h heq
  apply nativeC60BVGeneratorCode_injective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
  have hc := congrArg
    (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W)) heq
  rw [nativeK5DIShiftGen_code W R inner shift g,
      nativeK5DIShiftGen_code W R inner shift h] at hc
  exact (nativeC60BWCodePrefix_injective
    (nativeK5AXKuuSignature W) shift) hc

/-- Crucially, the excluded original CK atom is mapped to the
ACTUAL excluded CK atom at the new physical inner 15D boundary. -/
theorem nativeK5DIShiftGen_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool) :
    nativeK5DIShiftGen W R inner shift
        (nativeK5CKAtomGenerator W R inner) =
      nativeK5CKAtomGenerator W R (shift ++ inner) := by
  apply nativeC60BVGeneratorCode_injective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
  exact (nativeK5DIShiftGen_code W R inner shift
    (nativeK5CKAtomGenerator W R inner)).trans
      (nativeK5DHBaseCode_inner_shift W R inner shift).symm

/-- Every original CN alphabet letter, not merely a CZ-indexed one,
has an ACTUAL shifted typed certificate distinct from the right base. -/
def nativeK5DIShiftLetter
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool) :
    NativeC60CNForkAlphabet
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (nativeK5CKAtomGenerator W R inner) →
      NativeC60CNForkAlphabet
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (nativeK5CKAtomGenerator W R (shift ++ inner)) :=
  fun j => ⟨nativeK5DIShiftGen W R inner shift j.val, by
    intro h
    have hh : nativeK5DIShiftGen W R inner shift j.val =
        nativeK5DIShiftGen W R inner shift
          (nativeK5CKAtomGenerator W R inner) :=
      h.trans (nativeK5DIShiftGen_atom W R inner shift).symm
    exact j.property (nativeK5DIShiftGen_injective W R inner shift hh)⟩

theorem nativeK5DIShiftLetter_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool) :
    Function.Injective (nativeK5DIShiftLetter W R inner shift) := by
  intro j k h
  apply Subtype.ext
  exact nativeK5DIShiftGen_injective W R inner shift
    (congrArg Subtype.val h)

/-- EVERY original CN letter retains its complete 16D proof code. -/
theorem nativeK5DIShiftLetter_code
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)) :
    nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5DIShiftLetter W R inner shift j).val =
      nativeC60BWCodePrefix (nativeK5AXKuuSignature W) shift
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) j.val) :=
  nativeK5DIShiftGen_code W R inner shift j.val

/-- The ORIGINAL CZ core-depth discriminator ignores finite AQ context
prefixes, because those prefixes do NOT modify the Type-valued input. -/
theorem nativeK5DICZIndex_prefix
    (W : NativeK5StructuralThirteenCell p U V)
    (shift : List Bool)
    (code : NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)) :
    nativeK5CZCodeIndex W
        (nativeC60BWCodePrefix (nativeK5AXKuuSignature W) shift code) =
      nativeK5CZCodeIndex W code := by
  rfl

/-- In particular EVERY NON-CZ certificate remains non-CZ, and every
CZ certificate retains its ORIGINAL exact symm-depth before projection. -/
theorem nativeK5DIShiftLetter_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)) :
    nativeK5DCLetterParity W R (shift ++ inner)
        (nativeK5DIShiftLetter W R inner shift j) =
      nativeK5DCLetterParity W R inner j := by
  change
    (match nativeK5CZCodeIndex W
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5DIShiftLetter W R inner shift j).val) with
      | some n => decide (n % 2 = 1)
      | none => false) =
    (match nativeK5CZCodeIndex W
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) j.val) with
      | some n => decide (n % 2 = 1)
      | none => false)
  rw [nativeK5DIShiftLetter_code W R inner shift j,
      nativeK5DICZIndex_prefix]

/-- True BW covariance of one arbitrary CN mixed fork, including
its signed inverse of the ORIGINAL excluded base. -/
theorem nativeK5DIShiftLetter_CNEmbed
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)) :
    nativeC60BWFreePrefix (nativeK5AXKuuSignature W) shift
        (nativeC60CNEmbed (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner)
          (FreeGroup.of j)) =
      nativeC60CNEmbed (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R (shift ++ inner))
        (FreeGroup.of (nativeK5DIShiftLetter W R inner shift j)) := by
  simp only [nativeC60CNEmbed, FreeGroup.lift_apply_of,
    nativeC60BWFreePrefix, map_mul, map_inv, FreeGroup.map.of]
  change
    FreeGroup.of (nativeC60BWCodePrefix (nativeK5AXKuuSignature W) shift
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) j.val)) *
    (FreeGroup.of (nativeC60BWCodePrefix (nativeK5AXKuuSignature W) shift
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner))))⁻¹ =
    FreeGroup.of (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (nativeK5DIShiftLetter W R inner shift j).val) *
    (FreeGroup.of (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R (shift ++ inner))))⁻¹
  rw [nativeK5DIShiftLetter_code, nativeK5DHBaseCode_inner_shift]

/-- Exact noncommutative covariance for every signed ORIGINAL CN word. -/
theorem nativeK5DIShiftLetter_CNEmbed_hom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner shift : List Bool) :
    (nativeC60BWFreePrefix (nativeK5AXKuuSignature W) shift).comp
        (nativeC60CNEmbed (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner)) =
      (nativeC60CNEmbed (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R (shift ++ inner))).comp
          (FreeGroup.map (nativeK5DIShiftLetter W R inner shift)) := by
  apply FreeGroup.ext_hom
  intro j
  exact nativeK5DIShiftLetter_CNEmbed W R inner shift j

/-- The WHOLE-GROUP DF equivalence sends EACH original CN strict
generator to its genuine shifted CN certificate, in the original
strict Aut group, not merely in a quotient of the BW receiver. -/
theorem nativeK5DIInnerPrefixStrict_letter
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)) :
    nativeK5DFInnerPrefixStrictEquiv W R inner outer shift
        (nativeK5CYPhysicalFreeIsotropy W R inner outer (FreeGroup.of j)) =
      nativeK5CYPhysicalFreeIsotropy W R (shift ++ inner) outer
        (FreeGroup.of (nativeK5DIShiftLetter W R inner shift j)) := by
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
        (nativeC60CORetraction S F outer base
          (nativeC60COEmbed S F outer base (FreeGroup.of j)))) =
    nativeC60COHolonomy S F outer
      (nativeK5CHSource W (shift ++ inner) (nativeK5CKConservativeRefl W R))
      (nativeC60COEmbed S F outer targetBase
        (FreeGroup.of (nativeK5DIShiftLetter W R inner shift j)))
  rw [nativeC60CORetraction_embed, nativeC60COEmbed_holonomy_apply]
  calc
    nativeC60BWFreePrefix S (outer ++ shift)
        (nativeC60CNEmbed S F base (FreeGroup.of j)) =
      nativeC60BWFreePrefix S outer
        (nativeC60BWFreePrefix S shift
          (nativeC60CNEmbed S F base (FreeGroup.of j))) := by
      exact (DFunLike.congr_fun
        (nativeC60DDFreePrefix_append S outer shift) _).symm
    _ = nativeC60BWFreePrefix S outer
        (nativeC60CNEmbed S F targetBase
          (FreeGroup.of (nativeK5DIShiftLetter W R inner shift j))) := by
      exact congrArg (nativeC60BWFreePrefix S outer)
        (nativeK5DIShiftLetter_CNEmbed W R inner shift j)

/-- DF agrees with the FULL genuine CN free-word map, not merely
with the DH selected Nat family of CZ symm-depth generators. -/
theorem nativeK5DIInnerPrefixStrict_CN_hom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).toMonoidHom.comp
        (nativeK5CYPhysicalFreeIsotropy W R inner outer).toMonoidHom =
      (nativeK5CYPhysicalFreeIsotropy W R (shift ++ inner) outer).toMonoidHom.comp
        (FreeGroup.map (nativeK5DIShiftLetter W R inner shift)) := by
  apply FreeGroup.ext_hom
  intro j
  exact nativeK5DIInnerPrefixStrict_letter W R inner outer shift j

/-- The full chosen DC gauge parity commutes with the ORIGINAL
whole-group DF strict isomorphism: test every CN letter, then extend
by free-group universality and true CY surjectivity. -/
theorem nativeK5DIInnerPrefix_full_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DGInnerPrefixTransportedParity W R inner outer shift =
      nativeK5DCParityQuotient W R inner outer := by
  let source := nativeK5CYPhysicalFreeIsotropy W R inner outer
  have hletters :
      (nativeK5DGInnerPrefixTransportedParity W R inner outer shift).comp
          source.toMonoidHom =
        (nativeK5DCParityQuotient W R inner outer).comp
          source.toMonoidHom := by
    apply FreeGroup.ext_hom
    intro j
    change nativeK5DGInnerPrefixTransportedParity W R inner outer shift
        (source (FreeGroup.of j)) =
      nativeK5DCParityQuotient W R inner outer (source (FreeGroup.of j))
    calc
      nativeK5DGInnerPrefixTransportedParity W R inner outer shift
          (source (FreeGroup.of j)) =
        nativeK5DCParityQuotient W R (shift ++ inner) outer
          (nativeK5CYPhysicalFreeIsotropy W R (shift ++ inner) outer
            (FreeGroup.of (nativeK5DIShiftLetter W R inner shift j))) := by
        change nativeK5DCParityQuotient W R (shift ++ inner) outer
            (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift
              (source (FreeGroup.of j))) = _
        rw [nativeK5DIInnerPrefixStrict_letter]
      _ = FreeGroup.of (nativeK5DCLetterParity W R (shift ++ inner)
            (nativeK5DIShiftLetter W R inner shift j)) := by
        change (FreeGroup.map (nativeK5DCLetterParity W R (shift ++ inner)))
          (nativeC60CORetraction (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) outer
            (nativeK5CKAtomGenerator W R (shift ++ inner))
            (nativeC60COEmbed (nativeK5AXKuuSignature W)
              (nativeK5BCFrame W) outer
              (nativeK5CKAtomGenerator W R (shift ++ inner))
              (FreeGroup.of (nativeK5DIShiftLetter W R inner shift j)))) = _
        rw [nativeC60CORetraction_embed, FreeGroup.map.of]
      _ = FreeGroup.of (nativeK5DCLetterParity W R inner j) :=
        congrArg FreeGroup.of (nativeK5DIShiftLetter_parity W R inner shift j)
      _ = nativeK5DCParityQuotient W R inner outer (source (FreeGroup.of j)) := by
        change _ = (FreeGroup.map (nativeK5DCLetterParity W R inner))
          (nativeC60CORetraction (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) outer
            (nativeK5CKAtomGenerator W R inner)
            (nativeC60COEmbed (nativeK5AXKuuSignature W)
              (nativeK5BCFrame W) outer
              (nativeK5CKAtomGenerator W R inner) (FreeGroup.of j)))
        rw [nativeC60CORetraction_embed, FreeGroup.map.of]
  apply MonoidHom.ext
  intro z
  obtain ⟨x, rfl⟩ := source.surjective z
  exact DFunLike.congr_fun hletters x

/-- The previously open DG/DH quotient-kernel inclusion now follows
unconditionally from the FULL original CN generator parity theorem. -/
theorem nativeK5DIInnerPrefix_kernel_le
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    (nativeK5DCParityQuotient W R inner outer).ker ≤
      (nativeK5DGInnerPrefixTransportedParity W R inner outer shift).ker := by
  rw [nativeK5DIInnerPrefix_full_parity W R inner outer shift]

end OriginalFullCNInnerPrefix

#print axioms nativeK5DIShiftGen
#print axioms nativeK5DIShiftGen_code
#print axioms nativeK5DIShiftGen_injective
#print axioms nativeK5DIShiftGen_atom
#print axioms nativeK5DIShiftLetter
#print axioms nativeK5DIShiftLetter_injective
#print axioms nativeK5DIShiftLetter_code
#print axioms nativeK5DICZIndex_prefix
#print axioms nativeK5DIShiftLetter_parity
#print axioms nativeK5DIShiftLetter_CNEmbed
#print axioms nativeK5DIShiftLetter_CNEmbed_hom
#print axioms nativeK5DIInnerPrefixStrict_letter
#print axioms nativeK5DIInnerPrefixStrict_CN_hom
#print axioms nativeK5DIInnerPrefix_full_parity
#print axioms nativeK5DIInnerPrefix_kernel_le

end
end Kuu.F112.Physical
