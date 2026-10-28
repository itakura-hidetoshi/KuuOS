import Kuu.F112.PolygonNativeC60AQFullPentagonStrictSeparation

/-!
# F112-P94D3DZ — exact quotient obstruction and infinite-order C60 AQ witness

DY proved strict inclusion of the transported ORIGINAL pentagon normal
kernel inside the independent FULL context-closed pentagon normal kernel.

DZ makes the resulting irreversible loss of Type-valued 18D evidence
explicit in the two ACTUAL quotient group presentations:

* Construct the canonical SURJECTIVE group homomorphism from the
  DW transported-original quotient onto the DX full-closed quotient.
* Construct the original full-context integer character DESCENDED to
  the DW quotient, and show an actual DY pentagon defect has charge 1.
* The same defect is a NONIDENTITY element of the first quotient, but
  maps to identity in the second: the canonical map is NOT injective.
* Its arbitrary NATURAL powers are ALL in the kernel of the canonical
  quotient map, but are pairwise DISTINCT in the source quotient.
  This gives a concrete INFINITE obstruction, not merely one defect.
* No map from the full-closed quotient can recover the integer
  character of the first quotient through the canonical projection.
* Identify the full quotient with a quotient of the image quotient
  by the whole newly imposed normal subgroup (third isomorphism).
* Specialize the infinite obstruction to genuine physical C60 AU
  16D zigzag / dependent 17D generators at ANY finite AQ tree.

This is a precise relative algebraic Type-valued presentation result.
No geometric original C60 19D filler is produced or inferred.
Strict Kuu is primary, independent Kuu is a presentation; original
14D-18D evidence, DS no-go, 107 public roots, and no-Gray are retained.
No new axioms, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

section CanonicalQuotientObstruction

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The canonical homomorphism between the actual TWO quotient
presentations. DY proves that it loses nontrivial information. -/
def nativeC60DZImageToFull (word : List Bool) :
    NativeC60DWContextPentagonQuotient S F word →*
      NativeC60DXFullClosedPentagonQuotient S F :=
  QuotientGroup.lift
    (nativeC60DWContextPentagonNormalClosure S F word)
    (QuotientGroup.mk' (nativeC60DXFullClosedPentagonNormalClosure S F))
    (by
      rw [QuotientGroup.ker_mk']
      exact nativeC60DXImageKernel_le_full S F word)

/-- The comparison computes on EVERY complete noncommutative 18D word
without forgetting its original dependent generator code. -/
theorem nativeC60DZImageToFull_mk (word : List Bool)
    (x : NativeC60DVClosedFullFree S F) :
    (nativeC60DZImageToFull S F word)
        ((QuotientGroup.mk'
          (nativeC60DWContextPentagonNormalClosure S F word)) x) =
      (QuotientGroup.mk'
        (nativeC60DXFullClosedPentagonNormalClosure S F)) x :=
  rfl

/-- The comparison is SURJECTIVE (every fully-closed class is hit),
independently of the later strict-kernel obstruction. -/
theorem nativeC60DZImageToFull_surjective (word : List Bool) :
    Function.Surjective (nativeC60DZImageToFull S F word) := by
  intro y
  obtain ⟨x, rfl⟩ :=
    (QuotientGroup.mk'_surjective
      (nativeC60DXFullClosedPentagonNormalClosure S F)) y
  exact ⟨(QuotientGroup.mk'
    (nativeC60DWContextPentagonNormalClosure S F word)) x,
      nativeC60DZImageToFull_mk S F word x⟩

/-- DY's genuine full-code character descends through ALL transported
original pentagon relations, but not all full-closed relations. -/
def nativeC60DZImageCharacter (word : List Bool) :
    NativeC60DWContextPentagonQuotient S F word →* Multiplicative ℤ :=
  QuotientGroup.lift
    (nativeC60DWContextPentagonNormalClosure S F word)
    (nativeC60DYCharacter S F word)
    (nativeC60DYImageKernel_le_character_ker S F word)

theorem nativeC60DZImageCharacter_mk (word : List Bool)
    (x : NativeC60DVClosedFullFree S F) :
    (nativeC60DZImageCharacter S F word)
      ((QuotientGroup.mk'
        (nativeC60DWContextPentagonNormalClosure S F word)) x) =
      (nativeC60DYCharacter S F word) x :=
  rfl

/-- The ACTUAL DY defect, not an invented independent 18D generator,
viewed as a class of the original-image quotient. -/
def nativeC60DZOutsideDefectClass (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    NativeC60DWContextPentagonQuotient S F word :=
  (QuotientGroup.mk'
    (nativeC60DWContextPentagonNormalClosure S F word))
    (nativeC60DYOutsidePentagonDefect S F word r)

/-- It remains a NONIDENTITY class before the extra full-context
pentagon relations are imposed. -/
theorem nativeC60DZOutsideDefectClass_ne_one (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    nativeC60DZOutsideDefectClass S F word r ≠ 1 := by
  intro h
  have hm : nativeC60DYOutsidePentagonDefect S F word r ∈
      nativeC60DWContextPentagonNormalClosure S F word :=
    (QuotientGroup.eq_one_iff _).mp h
  exact nativeC60DYOutsidePentagon_not_mem_image S F word r hm

/-- The SAME actual class becomes the IDENTITY in the full target
presentation; the information loss is exhibited by explicit code. -/
theorem nativeC60DZImageToFull_defect_one (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    (nativeC60DZImageToFull S F word)
      (nativeC60DZOutsideDefectClass S F word r) = 1 := by
  rw [nativeC60DZOutsideDefectClass,
    nativeC60DZImageToFull_mk S F word]
  exact (QuotientGroup.eq_one_iff _).mpr
    (nativeC60DYOutsidePentagon_mem_full S F word r)

/-- The quotient invariant detects the SAME actual 18D pentagon
difference by the nonzero integral generator 1. -/
theorem nativeC60DZImageCharacter_defect_one (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    (nativeC60DZImageCharacter S F word)
      (nativeC60DZOutsideDefectClass S F word r) =
        Multiplicative.ofAdd (1 : ℤ) := by
  rw [nativeC60DZOutsideDefectClass,
    nativeC60DZImageCharacter_mk S F word]
  exact nativeC60DYOutsidePentagon_charge_one S F word r

/-- The canonical surjection cannot preserve FULL quotient evidence:
one explicit nonidentity class lies in its kernel. -/
theorem nativeC60DZImageToFull_not_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    ¬ Function.Injective (nativeC60DZImageToFull S F word) := by
  intro hinj
  exact (nativeC60DZOutsideDefectClass_ne_one S F word r)
    (hinj (by rw [nativeC60DZImageToFull_defect_one S F word r, map_one]))

/-- The canonical comparison carries an exact THIRD-ISOMORPHISM
presentation: quotient by the image of the full normal subgroup. -/
def nativeC60DZThirdIsomorphism (word : List Bool) :
    (NativeC60DWContextPentagonQuotient S F word ⧸
      (nativeC60DXFullClosedPentagonNormalClosure S F).map
        (QuotientGroup.mk'
          (nativeC60DWContextPentagonNormalClosure S F word))) ≃*
      NativeC60DXFullClosedPentagonQuotient S F :=
  QuotientGroup.quotientQuotientEquivQuotient
    (nativeC60DWContextPentagonNormalClosure S F word)
    (nativeC60DXFullClosedPentagonNormalClosure S F)
    (nativeC60DXImageKernel_le_full S F word)

/-- Integer powers of the actual nonzero character generator have
exactly the stated integer value. No torsion-freeness is postulated. -/
theorem nativeC60DZIntegerGeneratorPower (n : ℕ) :
    Multiplicative.toAdd ((Multiplicative.ofAdd (1 : ℤ)) ^ n) =
      (n : ℤ) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [pow_succ]
      change Multiplicative.toAdd
        ((Multiplicative.ofAdd (1 : ℤ)) ^ n) + 1 = (Nat.succ n : ℤ)
      omega

/-- Every natural power of the actual defect remains lost by
the target full-closed quotient, including arbitrary long powers. -/
theorem nativeC60DZDefectPower_mem_kernel (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    (nativeC60DZOutsideDefectClass S F word r) ^ n ∈
      (nativeC60DZImageToFull S F word).ker := by
  apply MonoidHom.mem_ker.mpr
  rw [map_pow, nativeC60DZImageToFull_defect_one S F word r, one_pow]

/-- INFINITE obstruction: all natural powers of the same genuine
context-pentagon class are pairwise distinct in the source quotient. -/
theorem nativeC60DZDefectPower_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    Function.Injective
      (fun n : ℕ => (nativeC60DZOutsideDefectClass S F word r) ^ n) := by
  intro m n h
  have hh := congrArg (nativeC60DZImageCharacter S F word) h
  rw [map_pow, map_pow,
    nativeC60DZImageCharacter_defect_one S F word r,
    nativeC60DZImageCharacter_defect_one S F word r] at hh
  have hi := congrArg Multiplicative.toAdd hh
  rw [nativeC60DZIntegerGeneratorPower m,
    nativeC60DZIntegerGeneratorPower n] at hi
  exact_mod_cast hi

/-- The integer-valued source quotient character CANNOT factor back
through the full target quotient: an ACTUAL typed 18D pentagon
generator has charge 1 but maps to 1 in the target. -/
theorem nativeC60DZCharacter_no_full_descent (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    ¬ ∃ χfull : NativeC60DXFullClosedPentagonQuotient S F →* Multiplicative ℤ,
      χfull.comp (nativeC60DZImageToFull S F word) =
        nativeC60DZImageCharacter S F word := by
  rintro ⟨χfull, hcomp⟩
  have hs := DFunLike.congr_fun hcomp
    (nativeC60DZOutsideDefectClass S F word r)
  have hbad : (1 : Multiplicative ℤ) = Multiplicative.ofAdd (1 : ℤ) := by
    calc
      (1 : Multiplicative ℤ) =
          χfull ((nativeC60DZImageToFull S F word)
            (nativeC60DZOutsideDefectClass S F word r)) := by
              rw [nativeC60DZImageToFull_defect_one S F word r, map_one]
      _ = (nativeC60DZImageCharacter S F word)
            (nativeC60DZOutsideDefectClass S F word r) := hs
      _ = Multiplicative.ofAdd (1 : ℤ) :=
        nativeC60DZImageCharacter_defect_one S F word r
  have hn := congrArg Multiplicative.toAdd hbad
  norm_num at hn

end CanonicalQuotientObstruction

section PhysicalC60AU

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

/-- A genuine C60 AU witness supplies infinitely many pairwise
distinct classes in the kernel of the canonical full quotient map. -/
theorem nativeK5DZPhysicalAQ_infinite_obstruction
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    Function.Injective (fun n : ℕ =>
      (nativeC60DZOutsideDefectClass S F (nativeK5DOTreeWord tree)
        (nativeC60DYOriginalZigzagGen S F
          (nativeK5CEPhysicalAUGenerator W))) ^ n) := by
  dsimp only
  exact nativeC60DZDefectPower_injective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W))

end PhysicalC60AU

#print axioms nativeC60DZImageToFull
#print axioms nativeC60DZImageToFull_mk
#print axioms nativeC60DZImageToFull_surjective
#print axioms nativeC60DZImageCharacter
#print axioms nativeC60DZOutsideDefectClass
#print axioms nativeC60DZOutsideDefectClass_ne_one
#print axioms nativeC60DZImageToFull_defect_one
#print axioms nativeC60DZImageCharacter_defect_one
#print axioms nativeC60DZImageToFull_not_injective
#print axioms nativeC60DZThirdIsomorphism
#print axioms nativeC60DZIntegerGeneratorPower
#print axioms nativeC60DZDefectPower_mem_kernel
#print axioms nativeC60DZDefectPower_injective
#print axioms nativeC60DZCharacter_no_full_descent
#print axioms nativeK5DZPhysicalAQ_infinite_obstruction

end
end Kuu.F112.Physical
