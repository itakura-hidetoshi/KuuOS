import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteRankDirectProduct
import Mathlib.LinearAlgebra.Finsupp.Defs
import Mathlib.Data.Finsupp.Basic

/-!
# F112-P94D3EG — infinitely many independent AQ obstructions after removing any finite rank

EA gave genuine complete 18D Type-valued pentagon defects δ_j with
independently detecting integer characters χ_i.
EB constructed finite-rank integer receivers, ED embedded the
countable free abelian group in the ACTUAL obstruction abelianization,
EE gave true group-homomorphic finite-rank sections, and EF made
their direct-product decompositions explicit.

EG proves that the COMPLEMENTARY KERNEL of EVERY finite receiver
still contains a genuine countably generated free abelian subgroup.
The index-shift j ↦ n + j on (ℕ →₀ ℤ) is an injective additive
homomorphism. ED embeds the shifted finite-support sequence in the
actual abelianization. Each of the first n coordinate receivers
evaluates to zero by the genuine finite-AQ Kronecker law, so the
embedding factors into the ACTUAL subgroup (χ_ab^n).ker.
The resulting additive group homomorphism is injective.

In particular, removing finitely many integer-valued contextual
obstructions does not exhaust the independently observed AQ defects.
The source kernel ker π_w remains NONCOMMUTATIVE: all additive
homomorphisms below land in the Additive presentation of its
actual ABELIANIZATION or its honest receiver kernel.

No infinite-product surjectivity, infinite direct-product splitting,
geometric 19D filler or Gray structure is claimed. Preserve strict
Kuu, independent Kuu as a presentation, DS no-go, the original
14D--18D Type-valued proof histories, all 107 public roots, pinned
Lean/mathlib, same-root and append-only constraints.
No new axiom, sorry or admit.
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

section FiniteRankComplementInfiniteFamily

/-- Shift a genuinely finitely supported integer sequence by n.
The zero-extension preserves finite support and addition. -/
def nativeC60EGTailShift (n : ℕ) :
    (ℕ →₀ ℤ) →+ (ℕ →₀ ℤ) :=
  (Finsupp.lmapDomain ℤ ℤ (fun j : ℕ => n + j)).toAddMonoidHom

/-- Every shifted sequence has zero coordinate strictly before n. -/
theorem nativeC60EGTailShift_initial_zero
    (n : ℕ) (v : ℕ →₀ ℤ) (i : Fin n) :
    nativeC60EGTailShift n v i.val = 0 := by
  change (Finsupp.mapDomain (fun j : ℕ => n + j) v) i.val = 0
  apply Finsupp.mapDomain_notin_range
  rintro ⟨j, hj⟩
  change n + j = i.val at hj
  have hi : i.val < n := i.isLt
  omega

/-- The shift never identifies distinct finite-support sequences. -/
theorem nativeC60EGTailShift_injective (n : ℕ) :
    Function.Injective (nativeC60EGTailShift n) := by
  intro v w h
  have hshift : Function.Injective (fun j : ℕ => n + j) := by
    intro i j hij
    change n + i = n + j at hij
    omega
  change (Finsupp.mapDomain (fun j : ℕ => n + j) v) =
    (Finsupp.mapDomain (fun j : ℕ => n + j) w) at h
  exact (Finsupp.mapDomain_injective hshift) h

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Embed all genuinely shifted, complete Type-valued AQ defects
in the abelianization of the source noncommutative quotient kernel. -/
def nativeC60EGShiftedAbelianEmbedding (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    (ℕ →₀ ℤ) →+
      Additive (Abelianization ((nativeC60DZImageToFull S F word).ker)) :=
  (nativeC60EDFiniteSupportEmbedding S F word r).comp
    (nativeC60EGTailShift n)

/-- Faithfulness is inherited from ED and the injective index-shift. -/
theorem nativeC60EGShiftedAbelianEmbedding_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    Function.Injective (nativeC60EGShiftedAbelianEmbedding S F word r n) := by
  intro v w h
  have hh : nativeC60EGTailShift n v = nativeC60EGTailShift n w :=
    nativeC60EDFiniteSupportEmbedding_injective S F word r h
  exact nativeC60EGTailShift_injective n hh

/-- Every shifted defect combination is invisible to all of the
first n integer coordinates, hence lies in the genuine receiver kernel.
This is a calculation IN THE ABELIANIZATION, not in the source kernel. -/
theorem nativeC60EGShiftedAbelian_receiver_one (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) (v : ℕ →₀ ℤ) :
    (nativeC60EBAbelianReceiver S F word n)
      ((nativeC60EGShiftedAbelianEmbedding S F word r n v).toMul) = 1 := by
  funext i
  change ((nativeC60EBAbelianReceiver S F word n)
      ((nativeC60EDFiniteSupportEmbedding S F word r
        (nativeC60EGTailShift n v)).toMul)) i = 1
  rw [nativeC60EEReceiver_coordinate S F word n
    (nativeC60EDFiniteSupportEmbedding S F word r
      (nativeC60EGTailShift n v)) i]
  rw [nativeC60EDCoordinate_finiteSupport S F word r
    (nativeC60EGTailShift n v) i.val]
  rw [nativeC60EGTailShift_initial_zero n v i]
  rfl

/-- An ACTUAL additive homomorphism into the additive presentation
of the receiver's honest subgroup kernel. All membership proofs
use the concrete quotient character, with no extra closure axiom. -/
def nativeC60EGTailComplementEmbedding (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    (ℕ →₀ ℤ) →+
      Additive ((nativeC60EBAbelianReceiver S F word n).ker) where
  toFun v := Additive.ofMul
    ⟨(nativeC60EGShiftedAbelianEmbedding S F word r n v).toMul,
      MonoidHom.mem_ker.mpr
        (nativeC60EGShiftedAbelian_receiver_one S F word r n v)⟩
  map_zero' := by
    apply Additive.ext
    apply Subtype.ext
    change ((nativeC60EGShiftedAbelianEmbedding S F word r n)
      (0 : ℕ →₀ ℤ)).toMul = 1
    rw [map_zero]
    rfl
  map_add' v w := by
    apply Additive.ext
    apply Subtype.ext
    change ((nativeC60EGShiftedAbelianEmbedding S F word r n)
      (v + w)).toMul =
      ((nativeC60EGShiftedAbelianEmbedding S F word r n v).toMul) *
      ((nativeC60EGShiftedAbelianEmbedding S F word r n w).toMul)
    rw [map_add]
    rfl

/-- MAIN EG THEOREM: the genuine complementary kernel contains a
faithful countable free abelian group even AFTER deleting the
first n independent integer coordinates for ARBITRARY finite n. -/
theorem nativeC60EGTailComplementEmbedding_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    Function.Injective (nativeC60EGTailComplementEmbedding S F word r n) := by
  intro v w h
  have hh := congrArg
    (fun x : Additive ((nativeC60EBAbelianReceiver S F word n).ker) => x.toMul.1) h
  change ((nativeC60EGShiftedAbelianEmbedding S F word r n v).toMul) =
    ((nativeC60EGShiftedAbelianEmbedding S F word r n w).toMul) at hh
  have heq := congrArg Additive.ofMul hh
  exact nativeC60EGShiftedAbelianEmbedding_injective S F word r n heq

/-- EF's actual direct-product decomposition recognizes the entire
shifted family as a pure complementary-kernel component: its
finite-rank projection vanishes identically. -/
theorem nativeC60EGTail_finiteRankDecomposition_fst (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) (v : ℕ →₀ ℤ) :
    (nativeC60EFFiniteRankDecomposition S F word r n
      ((nativeC60EGShiftedAbelianEmbedding S F word r n v).toMul)).1 = 1 := by
  rw [nativeC60EFFiniteRankDecomposition_fst]
  exact nativeC60EGShiftedAbelian_receiver_one S F word r n v

end FiniteRankComplementInfiniteFamily

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

/-- Genuine physical C60 AU supplies a countably generated free
abelian subgroup of the complementary AQ obstruction receiver kernel
for EVERY finite n and EVERY actual finite AQ context tree. -/
theorem nativeK5EGPhysicalAQ_tailComplement_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (rank : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    Function.Injective
      (nativeC60EGTailComplementEmbedding S F
        (nativeK5DOTreeWord tree)
        (nativeC60DYOriginalZigzagGen S F
          (nativeK5CEPhysicalAUGenerator W)) rank) := by
  dsimp only
  exact nativeC60EGTailComplementEmbedding_injective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) rank

end PhysicalC60AU

#print axioms nativeC60EGTailShift
#print axioms nativeC60EGTailShift_initial_zero
#print axioms nativeC60EGTailShift_injective
#print axioms nativeC60EGShiftedAbelianEmbedding
#print axioms nativeC60EGShiftedAbelianEmbedding_injective
#print axioms nativeC60EGShiftedAbelian_receiver_one
#print axioms nativeC60EGTailComplementEmbedding
#print axioms nativeC60EGTailComplementEmbedding_injective
#print axioms nativeC60EGTail_finiteRankDecomposition_fst
#print axioms nativeK5EGPhysicalAQ_tailComplement_injective

end
end Kuu.F112.Physical
