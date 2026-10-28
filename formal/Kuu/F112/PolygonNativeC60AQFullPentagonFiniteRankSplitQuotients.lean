import Kuu.F112.PolygonNativeC60AQFullPentagonFreeAbelianEmbedding
import Mathlib.LinearAlgebra.Finsupp.Pi
import Mathlib.LinearAlgebra.Finsupp.Defs
import Mathlib.Data.Finsupp.Basic

/-!
# F112-P94D3EE — genuinely split finite-rank quotients of C60 AQ obstruction abelianizations

EB: every finite-rank multiplicative integer receiver of the actual
(noncommutative) image-to-full pentagon kernel and its abelianization
is surjective, by genuine dependent 18D C60 pentagon evidence.
ED: the genuine abelianization contains an explicit countably generated
free abelian subgroup with coordinate recovery from EA characters.

EE constructs an actual GROUP-HOMOMORPHIC section to the EB
abelianization receiver, for EVERY finite n including n = 0.
A finite integer vector extends by zero to a genuinely finite-support
integer sequence via the pinned mathlib Finsupp.lmapDomain along
Fin.val : Fin n → ℕ. ED embeds that finite-support sequence in the
true abelianization, not in the original noncommutative kernel.

We prove coordinate identity, section homomorphism, section
injectivity and a RIGHT-INVERSE identity of true MonoidHom objects:
  χ_ab^n ∘ s_n = id_(Fin n → Multiplicative ℤ).
The image of s_n is a genuine finite-rank free abelian direct factor
by this retraction; no infinite-rank splitting, global infinite
product surjectivity, or abelianity of the original kernel is asserted.

The genuine C60 AU zigzag is preserved. No 19D geometric filling,
Gray category or new evidence identification. Strict Kuu and the
independent-Kuu presentation, DS no-go, original Type-valued
14D--18D history, 107 public roots and pinned mathlib are preserved.
No new axiom, sorry, or admit.
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

section FiniteRankSplitAbelianQuotients

/-- Extend a finite integer vector to a finitely supported integer
sequence, with all new coordinates zero. The map is Z-linear. -/
def nativeC60EEFiniteExtension (n : ℕ) :
    (Fin n → ℤ) →ₗ[ℤ] (ℕ →₀ ℤ) :=
  (Finsupp.lmapDomain ℤ ℤ (fun j : Fin n => j.val)).comp
    (Finsupp.linearEquivFunOnFinite ℤ ℤ (Fin n)).symm.toLinearMap

/-- At an original finite coordinate, zero-extension recovers
exactly the corresponding integer coefficient. -/
theorem nativeC60EEFiniteExtension_apply (n : ℕ)
    (v : Fin n → ℤ) (i : Fin n) :
    nativeC60EEFiniteExtension n v i.val = v i := by
  change (Finsupp.mapDomain (fun j : Fin n => j.val)
    ((Finsupp.linearEquivFunOnFinite ℤ ℤ (Fin n)).symm v)) i.val = v i
  rw [Finsupp.mapDomain_apply_of_injective Fin.val_injective]
  rfl

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- An actual group homomorphism FROM the finite integer receiver
INTO the abelianization of the genuine noncommutative obstruction
kernel. No ordered-product conversion in the source kernel is used:
the multiplication takes place only after actual abelianization. -/
def nativeC60EEFiniteSection (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    (Fin n → Multiplicative ℤ) →*
      Abelianization ((nativeC60DZImageToFull S F word).ker) where
  toFun v :=
    (nativeC60EDFiniteSupportEmbedding S F word r
      (nativeC60EEFiniteExtension n (fun i => (v i).toAdd))).toMul
  map_one' := by
    change (nativeC60EDFiniteSupportEmbedding S F word r
      (nativeC60EEFiniteExtension n (0 : Fin n → ℤ))).toMul = 1
    rw [map_zero, map_zero]
    rfl
  map_mul' v w := by
    change (nativeC60EDFiniteSupportEmbedding S F word r
      (nativeC60EEFiniteExtension n
        ((fun i => (v i).toAdd) + (fun i => (w i).toAdd)))).toMul =
      (nativeC60EDFiniteSupportEmbedding S F word r
        (nativeC60EEFiniteExtension n (fun i => (v i).toAdd))).toMul *
      (nativeC60EDFiniteSupportEmbedding S F word r
        (nativeC60EEFiniteExtension n (fun i => (w i).toAdd))).toMul
    rw [map_add, map_add]
    rfl

/-- Coordinate evaluation of the EB receiver on the genuine
abelianization equals the ED descended character. -/
theorem nativeC60EEReceiver_coordinate (word : List Bool)
    (n : ℕ)
    (x : Additive (Abelianization ((nativeC60DZImageToFull S F word).ker)))
    (i : Fin n) :
    ((nativeC60EBAbelianReceiver S F word n) x.toMul) i =
      Multiplicative.ofAdd (nativeC60EDAbelianizedCoordinate S F word i.val x) := by
  rfl

/-- The EB finite receiver evaluated on the EE section reproduces
ANY finite vector, including all zero, positive, and negative charges. -/
theorem nativeC60EEFiniteSection_rightInverse (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) (v : Fin n → Multiplicative ℤ) :
    (nativeC60EBAbelianReceiver S F word n)
      (nativeC60EEFiniteSection S F word r n v) = v := by
  funext i
  rw [nativeC60EEReceiver_coordinate S F word n
    (nativeC60EDFiniteSupportEmbedding S F word r
      (nativeC60EEFiniteExtension n (fun j => (v j).toAdd))) i]
  rw [nativeC60EDCoordinate_finiteSupport S F word r
    (nativeC60EEFiniteExtension n (fun j => (v j).toAdd)) i.val]
  rw [nativeC60EEFiniteExtension_apply]
  exact Multiplicative.ofAdd_toAdd (v i)

/-- MAIN EE THEOREM: an actual split epimorphism of GROUPS, not
just a set-theoretic right inverse, for every finite rank.
The original kernel is never declared commutative. -/
theorem nativeC60EEFiniteReceiver_split (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).comp
      (nativeC60EEFiniteSection S F word r n) =
        MonoidHom.id (Fin n → Multiplicative ℤ) := by
  apply MonoidHom.ext
  intro v
  exact nativeC60EEFiniteSection_rightInverse S F word r n v

/-- A right inverse gives an actual injective finite-rank integer
subgroup; this assertion is internal to the genuine abelianization. -/
theorem nativeC60EEFiniteSection_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    Function.Injective (nativeC60EEFiniteSection S F word r n) := by
  intro v w h
  have heq := congrArg (nativeC60EBAbelianReceiver S F word n) h
  simpa only [nativeC60EEFiniteSection_rightInverse S F word r n] using heq

end FiniteRankSplitAbelianQuotients

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

/-- Genuine physical C60 AU Type-valued witnesses induce a split
finite-rank integer quotient of the actual AQ kernel abelianization. -/
theorem nativeK5EEPhysicalAQ_finiteRank_split
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (rank : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    (nativeC60EBAbelianReceiver S F (nativeK5DOTreeWord tree) rank).comp
      (nativeC60EEFiniteSection S F (nativeK5DOTreeWord tree)
        (nativeC60DYOriginalZigzagGen S F
          (nativeK5CEPhysicalAUGenerator W)) rank) =
      MonoidHom.id (Fin rank → Multiplicative ℤ) := by
  dsimp only
  exact nativeC60EEFiniteReceiver_split
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) rank

end PhysicalC60AU

#print axioms nativeC60EEFiniteExtension
#print axioms nativeC60EEFiniteExtension_apply
#print axioms nativeC60EEFiniteSection
#print axioms nativeC60EEReceiver_coordinate
#print axioms nativeC60EEFiniteSection_rightInverse
#print axioms nativeC60EEFiniteReceiver_split
#print axioms nativeC60EEFiniteSection_injective
#print axioms nativeK5EEPhysicalAQ_finiteRank_split

end
end Kuu.F112.Physical
