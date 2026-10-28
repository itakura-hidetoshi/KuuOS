import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteRankSplitQuotients

/-!
# F112-P94D3EF — explicit finite-rank direct-product decomposition of genuine AQ obstruction abelianization

EE constructed a HOMOMORPHIC section of every finite integer receiver
of the ACTUAL abelianization of the noncommutative transported-to-full
C60 AQ pentagon obstruction kernel. EF constructs the corresponding
explicit MulEquiv, in both directions, including the true complementary
kernel of the finite integer character.

For an abelian A and a split f : A →* B, with section s : B →* A:
  A ≃* B × f.ker
  x ↦ (f x, (s (f x))⁻¹ * x)
  (b,k) ↦ s b * k
The residual is certified to lie in f.ker. Left/right inverses and
multiplicativity are proved, not merely the bijection of underlying sets.
The only commutativity premise is on A, the *actual abelianization*;
nothing asserts that the ORIGINAL obstruction kernel commutes.

For every finite n, the C60 specialization makes
  Abelianization(ker π_w) ≃*
    (Fin n → Multiplicative ℤ) × ker(χ_ab^n).
The Fin n integer coordinate factor is the multiplicative presentation
of ℤ^n, hence a genuine finite-rank free abelian direct factor.
The n=0 case is also covered. No infinite product splitting or
geometric 19D Type-valued filler is asserted.

The DS no-go, strict Kuu, independent Kuu presentation, original
14D--18D dependent evidence, 107 public roots, no-Gray boundary,
fixed Lean/mathlib, same-root and append-only constraints are retained.
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

universe u v uD vD uE vE

section AbstractAbelianSplit

/-- Explicit canonical direct-product isomorphism for a split
homomorphism whose SOURCE is an abelian group. No commutativity of
the target group is required as an additional premise. -/
def nativeC60EFAbelianSplitEquiv
    {A : Type u} {B : Type v}
    [CommGroup A] [Group B]
    (f : A →* B) (s : B →* A)
    (hs : f.comp s = MonoidHom.id B) :
    A ≃* B × f.ker where
  toFun x :=
    (f x, ⟨(s (f x))⁻¹ * x, by
      change f ((s (f x))⁻¹ * x) = 1
      rw [map_mul, map_inv]
      have hh := DFunLike.congr_fun hs (f x)
      change f (s (f x)) = f x at hh
      rw [hh]
      exact inv_mul_cancel (f x)⟩)
  invFun p := s p.1 * p.2.1
  left_inv x := by
    change s (f x) * ((s (f x))⁻¹ * x) = x
    group
  right_inv p := by
    rcases p with ⟨b, ⟨k, hk⟩⟩
    have hsection : f (s b) = b := by
      have hh := DFunLike.congr_fun hs b
      change f (s b) = b at hh
      exact hh
    have hker : f k = 1 := MonoidHom.mem_ker.mp hk
    have himage : f (s b * k) = b := by
      rw [map_mul, hker, mul_one]
      exact hsection
    apply Prod.ext
    · change f (s b * k) = b
      exact himage
    · apply Subtype.ext
      change (s (f (s b * k)))⁻¹ * (s b * k) = k
      rw [himage]
      group
  map_mul' x y := by
    apply Prod.ext
    · change f (x * y) = f x * f y
      exact map_mul f x y
    · apply Subtype.ext
      change (s (f (x * y)))⁻¹ * (x * y) =
        ((s (f x))⁻¹ * x) * ((s (f y))⁻¹ * y)
      simp only [map_mul, mul_inv_rev]
      ac_rfl

end AbstractAbelianSplit

section FiniteRankC60AbelianSplitting

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- MAIN EF THEOREM: a genuine group isomorphism between the
abelianization of the original noncommutative C60 AQ comparison
kernel and the direct product of the finite integer receiver with
the actual kernel of that receiver. -/
def nativeC60EFFiniteRankDecomposition (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    Abelianization ((nativeC60DZImageToFull S F word).ker) ≃*
      (Fin n → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F word n).ker :=
  nativeC60EFAbelianSplitEquiv
    (nativeC60EBAbelianReceiver S F word n)
    (nativeC60EEFiniteSection S F word r n)
    (nativeC60EEFiniteReceiver_split S F word r n)

/-- The first coordinate of the actual group isomorphism is
precisely the EB integer-character receiver. -/
theorem nativeC60EFFiniteRankDecomposition_fst
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ)
    (x : Abelianization ((nativeC60DZImageToFull S F word).ker)) :
    (nativeC60EFFiniteRankDecomposition S F word r n x).1 =
      (nativeC60EBAbelianReceiver S F word n) x :=
  rfl

/-- The complementary factor of the forward isomorphism retains
the full abelianized obstruction class after removing its observed
finite-rank component. -/
theorem nativeC60EFFiniteRankDecomposition_residual
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ)
    (x : Abelianization ((nativeC60DZImageToFull S F word).ker)) :
    (nativeC60EFFiniteRankDecomposition S F word r n x).2.1 =
      (nativeC60EEFiniteSection S F word r n
        ((nativeC60EBAbelianReceiver S F word n) x))⁻¹ * x :=
  rfl

/-- The inverse group isomorphism is ACTUAL recombination:
section of the finite integer coordinate times the complementary
kernel element, not an externally chosen set-theoretic preimage. -/
theorem nativeC60EFFiniteRankDecomposition_symm
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ)
    (v : Fin n → Multiplicative ℤ)
    (k : (nativeC60EBAbelianReceiver S F word n).ker) :
    (nativeC60EFFiniteRankDecomposition S F word r n).symm (v, k) =
      nativeC60EEFiniteSection S F word r n v * k.1 :=
  rfl

/-- A true receiver-kernel class has zero finite-rank coordinate
under the EF decomposition. -/
theorem nativeC60EFFiniteRankDecomposition_ker_fst
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ)
    (k : (nativeC60EBAbelianReceiver S F word n).ker) :
    (nativeC60EFFiniteRankDecomposition S F word r n k.1).1 = 1 := by
  rw [nativeC60EFFiniteRankDecomposition_fst]
  exact MonoidHom.mem_ker.mp k.2

end FiniteRankC60AbelianSplitting

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

/-- Physical C60 AU proof data gives the explicit actual
finite-rank direct-product isomorphism, including the fully typed
source/target history of its independent context defects. -/
def nativeK5EFPhysicalAQ_finiteRankDecomposition
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (rank : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    Abelianization
      ((nativeC60DZImageToFull S F (nativeK5DOTreeWord tree)).ker) ≃*
      (Fin rank → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F
          (nativeK5DOTreeWord tree) rank).ker :=
  nativeC60EFFiniteRankDecomposition
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) rank

end PhysicalC60AU

#print axioms nativeC60EFAbelianSplitEquiv
#print axioms nativeC60EFFiniteRankDecomposition
#print axioms nativeC60EFFiniteRankDecomposition_fst
#print axioms nativeC60EFFiniteRankDecomposition_residual
#print axioms nativeC60EFFiniteRankDecomposition_symm
#print axioms nativeC60EFFiniteRankDecomposition_ker_fst
#print axioms nativeK5EFPhysicalAQ_finiteRankDecomposition

end
end Kuu.F112.Physical
