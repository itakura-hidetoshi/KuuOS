import Kuu.F112.PolygonNativeC60AQFullPentagonIndependentContextCharges
import Mathlib.GroupTheory.Abelianization.Defs
import Mathlib.Algebra.Group.TypeTags.Basic

/-!
# F112-P94D3EB — arbitrary finite-rank abelian quotients of genuine AQ obstruction kernels

EA supplied a countable family of actual complete 18D Type-valued
pentagon defects in the kernel of the image-to-full quotient comparison.
Its integer characters evaluate those defects by the exact Kronecker rule.

EB combines the first n characters into a genuine homomorphism from the
NONCOMMUTATIVE kernel into the finite product of multiplicative integers.
For every integer vector, the ordered product of the first n contextual
defects with those (possibly negative) exponents gives a preimage.
An ordered List.prod, NOT a commutative Finset.prod, preserves the original
group structure. Only the target receiver is commutative.

We prove surjectivity for every finite n, including n=0, then factor
the receiver through the actual abelianization and prove its surjectivity.
A physical C60 AU 16D zigzag supplies the genuinely typed seed.
Nothing here claims that the kernel is abelian or free abelian, or that
a geometric 19D C60 cell exists. DS no-go, strict Kuu, independent
presentation, original 14D--18D evidence, 107 public roots and the
non-Gray rule remain unchanged.
No sorry, admit or new axioms.
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

section FiniteRankAQObstruction

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Each EA character restricted to the ACTUAL noncommutative
kernel of the image-to-full normal-closure quotient comparison. -/
def nativeC60EBKernelCharacter (word : List Bool) (i : ℕ) :
    (nativeC60DZImageToFull S F word).ker →* Multiplicative ℤ :=
  (nativeC60EAImageCharacter S F word i).comp
    ((nativeC60DZImageToFull S F word).ker).subtype

/-- The first n independent integer characters, assembled into the
genuine multiplicative finite-coordinate receiver. No abelianity
hypothesis is placed on its source kernel. -/
def nativeC60EBFiniteReceiver (word : List Bool) (n : ℕ) :
    (nativeC60DZImageToFull S F word).ker →*
      (Fin n → Multiplicative ℤ) where
  toFun x i := nativeC60EBKernelCharacter S F word i.val x
  map_one' := by
    funext i
    exact map_one (nativeC60EBKernelCharacter S F word i.val)
  map_mul' x y := by
    funext i
    exact map_mul (nativeC60EBKernelCharacter S F word i.val) x y

/-- An actual dependent 18D EA defect, accompanied by its proof
of membership in the full-quotient comparison kernel. -/
def nativeC60EBKernelGenerator (word : List Bool) (j : ℕ)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    (nativeC60DZImageToFull S F word).ker :=
  ⟨nativeC60EAOutsideClass S F word j r,
    nativeC60EAOutsideClass_mem_kernel S F word j r⟩

/-- EA's Kronecker pairing, now on the ACTUAL kernel subtype. -/
theorem nativeC60EBKernelCharacter_generator (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (i j : ℕ) :
    (nativeC60EBKernelCharacter S F word i)
      (nativeC60EBKernelGenerator S F word j r) =
        (if i = j then Multiplicative.ofAdd (1 : ℤ) else 1) := by
  change (nativeC60EAImageCharacter S F word i)
    (nativeC60EAOutsideClass S F word j r) = _
  exact nativeC60EACharacter_orthogonal S F word r i j

/-- The chosen multiplicative integer unit has EXACT arbitrary
integer powers, including all negative integers. -/
theorem nativeC60EBIntegerUnit_zpow (z : ℤ) :
    (Multiplicative.ofAdd (1 : ℤ)) ^ z = Multiplicative.ofAdd z := by
  calc
    (Multiplicative.ofAdd (1 : ℤ)) ^ z =
        Multiplicative.ofAdd (z • (1 : ℤ)) :=
          (ofAdd_zsmul z (1 : ℤ)).symm
    _ = Multiplicative.ofAdd z := by simp [Int.zsmul_eq_mul]

/-- Every signed power of a true kernel defect has exactly its own
integer coordinate and vanishes at all different coordinates. -/
theorem nativeC60EBKernelCharacter_generator_zpow (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (i j : ℕ) (z : ℤ) :
    (nativeC60EBKernelCharacter S F word i)
      ((nativeC60EBKernelGenerator S F word j r) ^ z) =
        (if i = j then Multiplicative.ofAdd z else 1) := by
  rw [map_zpow, nativeC60EBKernelCharacter_generator S F word r i j]
  by_cases h : i = j
  · simp only [if_pos h]
    exact nativeC60EBIntegerUnit_zpow z
  · simp [h]

/-- A fixed order 0,1,...,n-1 in the NONCOMMUTATIVE kernel.
No reordering or unjustified commutative product is performed. -/
def nativeC60EBOrderedLift (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) (v : Fin n → Multiplicative ℤ) :
    (nativeC60DZImageToFull S F word).ker :=
  ((List.finRange n).map (fun j =>
    (nativeC60EBKernelGenerator S F word j.val r) ^
      (Multiplicative.toAdd (v j)))).prod

/-- Character evaluation commutes with ORDERED list multiplication.
The only simplification is each Kronecker character, never a
commutativity assertion about the kernel itself. -/
private theorem nativeC60EBOrderedPrefix_character (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) (v : Fin n → Multiplicative ℤ) (i : Fin n) :
    ∀ l : List (Fin n),
      (nativeC60EBKernelCharacter S F word i.val)
        ((l.map (fun j =>
          (nativeC60EBKernelGenerator S F word j.val r) ^
            (Multiplicative.toAdd (v j)))).prod) =
      (l.map (fun j => if i = j then v j else 1)).prod := by
  intro l
  induction l with
  | nil =>
      simp
  | cons j tail ih =>
      change (nativeC60EBKernelCharacter S F word i.val)
          (((nativeC60EBKernelGenerator S F word j.val r) ^
            (Multiplicative.toAdd (v j))) *
            ((tail.map (fun k =>
              (nativeC60EBKernelGenerator S F word k.val r) ^
                (Multiplicative.toAdd (v k)))).prod)) =
        (if i = j then v j else 1) *
          (tail.map (fun k => if i = k then v k else 1)).prod
      rw [map_mul, ih]
      have hcoordinate :
          (nativeC60EBKernelCharacter S F word i.val)
            ((nativeC60EBKernelGenerator S F word j.val r) ^
              (Multiplicative.toAdd (v j))) =
              (if i = j then v j else 1) := by
        rw [nativeC60EBKernelCharacter_generator_zpow S F word r
          i.val j.val (Multiplicative.toAdd (v j))]
        by_cases h : i = j
        · subst j
          simp
        · have hv : i.val ≠ j.val := by
            intro heq
            exact h (Fin.ext heq)
          simp [h, hv]
      rw [hcoordinate]

/-- A list with no repetitions contains either the single diagonal
charge at i, or none. This identity is solely in the COMMUTATIVE
integer receiver, not in the original obstruction kernel. -/
private theorem nativeC60EBDeltaList_prod (n : ℕ)
    (v : Fin n → Multiplicative ℤ) (i : Fin n) :
    ∀ l : List (Fin n), l.Nodup →
      (l.map (fun j => if i = j then v j else 1)).prod =
        (if i ∈ l then v i else 1) := by
  intro l
  induction l with
  | nil =>
      intro _
      simp
  | cons j tail ih =>
      intro hd
      have hnot : j ∉ tail := (List.nodup_cons.mp hd).1
      have htail : tail.Nodup := (List.nodup_cons.mp hd).2
      change (if i = j then v j else 1) *
          (tail.map (fun k => if i = k then v k else 1)).prod =
            (if i ∈ j :: tail then v i else 1)
      rw [ih htail]
      by_cases h : i = j
      · subst j
        simp [hnot]
      · simp [h]

/-- Constructive right inverse on the underlying sets:
ANY finite integer vector is realized by the explicitly ordered
product of signed powers of genuine closed-context 18D defects. -/
theorem nativeC60EBFiniteReceiver_orderedLift (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) (v : Fin n → Multiplicative ℤ) :
    (nativeC60EBFiniteReceiver S F word n)
      (nativeC60EBOrderedLift S F word r n v) = v := by
  funext i
  change (nativeC60EBKernelCharacter S F word i.val)
      (((List.finRange n).map (fun j =>
        (nativeC60EBKernelGenerator S F word j.val r) ^
          (Multiplicative.toAdd (v j)))).prod) = v i
  rw [nativeC60EBOrderedPrefix_character S F word r n v i
    (List.finRange n)]
  rw [nativeC60EBDeltaList_prod n v i (List.finRange n)
    (List.nodup_finRange n)]
  simp

/-- MAIN EB THEOREM: the original noncommutative obstruction kernel
has an ACTUAL surjective character receiver of every finite rank. -/
theorem nativeC60EBFiniteReceiver_surjective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    Function.Surjective (nativeC60EBFiniteReceiver S F word n) := by
  intro v
  exact ⟨nativeC60EBOrderedLift S F word r n v,
    nativeC60EBFiniteReceiver_orderedLift S F word r n v⟩

/-- The receiver factors canonically through the actual abelianization:
no abelianity assumption on the source was ever used. -/
def nativeC60EBAbelianReceiver (word : List Bool) (n : ℕ) :
    Abelianization ((nativeC60DZImageToFull S F word).ker) →*
      (Fin n → Multiplicative ℤ) :=
  Abelianization.lift (nativeC60EBFiniteReceiver S F word n)

/-- Every finite-rank free abelian group is thus also an ACTUAL quotient
of the abelianization of the original (possibly noncommutative) kernel. -/
theorem nativeC60EBAbelianReceiver_surjective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    Function.Surjective (nativeC60EBAbelianReceiver S F word n) := by
  intro v
  obtain ⟨k, hk⟩ :=
    nativeC60EBFiniteReceiver_surjective S F word r n v
  refine ⟨Abelianization.of k, ?_⟩
  simpa [nativeC60EBAbelianReceiver] using hk

end FiniteRankAQObstruction

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

/-- The genuine C60 AU zigzag yields surjections to every Z^n,
for ANY actual finite AQ context tree. -/
theorem nativeK5EBPhysicalAQ_finiteRank_surjective
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (rank : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    Function.Surjective
      (nativeC60EBFiniteReceiver S F (nativeK5DOTreeWord tree) rank) := by
  dsimp only
  exact nativeC60EBFiniteReceiver_surjective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) rank

/-- The same physical C60 family also survives abelianization
with a surjective finite-rank integer receiver. -/
theorem nativeK5EBPhysicalAQ_abelianFiniteRank_surjective
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (rank : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    Function.Surjective
      (nativeC60EBAbelianReceiver S F (nativeK5DOTreeWord tree) rank) := by
  dsimp only
  exact nativeC60EBAbelianReceiver_surjective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) rank

end PhysicalC60AU

#print axioms nativeC60EBKernelCharacter
#print axioms nativeC60EBFiniteReceiver
#print axioms nativeC60EBKernelGenerator
#print axioms nativeC60EBKernelCharacter_generator
#print axioms nativeC60EBIntegerUnit_zpow
#print axioms nativeC60EBKernelCharacter_generator_zpow
#print axioms nativeC60EBOrderedLift
#print axioms nativeC60EBFiniteReceiver_orderedLift
#print axioms nativeC60EBFiniteReceiver_surjective
#print axioms nativeC60EBAbelianReceiver
#print axioms nativeC60EBAbelianReceiver_surjective
#print axioms nativeK5EBPhysicalAQ_finiteRank_surjective
#print axioms nativeK5EBPhysicalAQ_abelianFiniteRank_surjective

end
end Kuu.F112.Physical
