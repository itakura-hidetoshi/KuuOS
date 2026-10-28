import Kuu.F112.PolygonNativeC60AQFullPentagonTailComplementNonFiniteGeneration

/-!
# F112-P94D3EI — finite-rank splitting inside each genuine AQ complementary kernel

EH proved that the honest kernel C_n of the first n abelianized C60
integer characters surjects onto every finite tail receiver Z^m.
EI strengthens these genuine quotient maps to split epimorphisms of
GROUPS, by shifting EE's finite integer extension into EG's
homomorphic embedding of the independent Type-valued 18D pentagon
defects INSIDE C_n.

For arbitrary natural n and m, including zero:
  C_n ≃* (Fin m → Multiplicative ℤ) × ker(τ_(n,m)).
The first factor is a genuine freely generated integer lattice.
The second is the ACTUAL subgroup kernel of the next m AQ character
coordinates. The isomorphism is explicit in both directions.

Only the actual abelianization of the source NONCOMMUTATIVE C60
obstruction kernel and its subgroups are treated as commutative.
Nothing proves the original obstruction kernel abelian or free,
nor any infinite-rank splitting, infinite-product surjectivity,
geometric 19D filler, or Gray reintroduction. Preserve strict Kuu,
independent Kuu as a presentation, the DS no-go, original 14D--18D
Type-valued evidence, 107 public roots, fixed Lean/mathlib and
same-root/append-only policies. No axiom, sorry or admit added.
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

section TailFiniteRankSplit

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- An actual GROUP-HOMOMORPHIC section of the next rank integer
coordinates into the honest kernel of the first n coordinates.
The finite vector is extended by zero and shifted before EG embeds
it into the genuine abelianized C60 AQ obstruction subgroup. -/
def nativeC60EITailFiniteSection (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ) :
    (Fin rank → Multiplicative ℤ) →*
      (nativeC60EBAbelianReceiver S F word n).ker where
  toFun v :=
    (nativeC60EGTailComplementEmbedding S F word r n
      (nativeC60EEFiniteExtension rank (fun i => (v i).toAdd))).toMul
  map_one' := by
    change (nativeC60EGTailComplementEmbedding S F word r n
      (nativeC60EEFiniteExtension rank (0 : Fin rank → ℤ))).toMul = 1
    rw [map_zero, map_zero]
    rfl
  map_mul' v w := by
    change (nativeC60EGTailComplementEmbedding S F word r n
      (nativeC60EEFiniteExtension rank
        ((fun i => (v i).toAdd) + (fun i => (w i).toAdd)))).toMul =
        (nativeC60EGTailComplementEmbedding S F word r n
          (nativeC60EEFiniteExtension rank (fun i => (v i).toAdd))).toMul *
        (nativeC60EGTailComplementEmbedding S F word r n
          (nativeC60EEFiniteExtension rank (fun i => (w i).toAdd))).toMul
    rw [map_add, map_add]
    rfl

/-- EH's exact Kronecker evaluation is the RIGHT-INVERSE identity
of the genuine group homomorphic section, not only an abstract
surjectivity claim or a set-theoretic choice of preimages. -/
theorem nativeC60EITailFiniteSection_rightInverse (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ) (v : Fin rank → Multiplicative ℤ) :
    (nativeC60EHTailReceiver S F word n rank)
      (nativeC60EITailFiniteSection S F word r n rank v) = v := by
  exact nativeC60EHTailReceiver_shiftedFiniteExtension
    S F word r n rank v

/-- MAIN EI SPLIT THEOREM: the next finite receiver of EVERY
honest AQ complement is a split epimorphism OF GROUPS. -/
theorem nativeC60EITailReceiver_split (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ) :
    (nativeC60EHTailReceiver S F word n rank).comp
      (nativeC60EITailFiniteSection S F word r n rank) =
        MonoidHom.id (Fin rank → Multiplicative ℤ) := by
  apply MonoidHom.ext
  intro v
  exact nativeC60EITailFiniteSection_rightInverse
    S F word r n rank v

/-- A genuine split section is injective: the complete finite
integer lattice is an actual subgroup of the complementary kernel. -/
theorem nativeC60EITailFiniteSection_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ) :
    Function.Injective (nativeC60EITailFiniteSection S F word r n rank) := by
  intro v w h
  have heq := congrArg (nativeC60EHTailReceiver S F word n rank) h
  simpa only [nativeC60EITailFiniteSection_rightInverse S F word r n rank]
    using heq

/-- MAIN EI DIRECT-PRODUCT THEOREM. EF's previously verified
multiplicative equivalence applies to the ACTUAL commutative
receiver-kernel C_n, using EI's new group-homomorphic section.
The second factor is not an abstract placeholder: it is precisely
the kernel of the genuine EH tail-coordinate receiver. -/
def nativeC60EITailDirectProduct (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      (Fin rank → Multiplicative ℤ) ×
        (nativeC60EHTailReceiver S F word n rank).ker :=
  nativeC60EFAbelianSplitEquiv
    (nativeC60EHTailReceiver S F word n rank)
    (nativeC60EITailFiniteSection S F word r n rank)
    (nativeC60EITailReceiver_split S F word r n rank)

/-- The first coordinate is exactly the genuine EH receiver. -/
theorem nativeC60EITailDirectProduct_fst (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker) :
    (nativeC60EITailDirectProduct S F word r n rank x).1 =
      nativeC60EHTailReceiver S F word n rank x := rfl

/-- The complementary coordinate is the ACTUAL residual after
subtracting the split finite-rank receiver component. -/
theorem nativeC60EITailDirectProduct_residual (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker) :
    (nativeC60EITailDirectProduct S F word r n rank x).2.1 =
      (nativeC60EITailFiniteSection S F word r n rank
        (nativeC60EHTailReceiver S F word n rank x))⁻¹ * x := rfl

/-- The inverse map is a concrete multiplication of the new
section and the residual class inside the ACTUAL kernel C_n. -/
theorem nativeC60EITailDirectProduct_symm (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ)
    (v : Fin rank → Multiplicative ℤ)
    (k : (nativeC60EHTailReceiver S F word n rank).ker) :
    (nativeC60EITailDirectProduct S F word r n rank).symm (v, k) =
      nativeC60EITailFiniteSection S F word r n rank v * k.1 := rfl

/-- Every class already in the next tail kernel has zero
finite-rank component in the true direct-product isomorphism. -/
theorem nativeC60EITailDirectProduct_ker_fst (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ)
    (k : (nativeC60EHTailReceiver S F word n rank).ker) :
    (nativeC60EITailDirectProduct S F word r n rank k.1).1 = 1 := by
  rw [nativeC60EITailDirectProduct_fst]
  exact MonoidHom.mem_ker.mp k.2

end TailFiniteRankSplit

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

/-- For every physically chosen C60 AU Type-valued witness and every
finite AQ context tree, the genuine abelianized comparison kernel
complement has a complete finite-rank direct-product splitting.
The underlying 16D zigzag and 18D defect history are preserved. -/
def nativeK5EIPhysicalAQ_tailDirectProduct
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (n rank : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    (nativeC60EBAbelianReceiver S F
      (nativeK5DOTreeWord tree) n).ker ≃*
      (Fin rank → Multiplicative ℤ) ×
        (nativeC60EHTailReceiver S F
          (nativeK5DOTreeWord tree) n rank).ker :=
  nativeC60EITailDirectProduct
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) n rank

end PhysicalC60AU

#print axioms nativeC60EITailFiniteSection
#print axioms nativeC60EITailFiniteSection_rightInverse
#print axioms nativeC60EITailReceiver_split
#print axioms nativeC60EITailFiniteSection_injective
#print axioms nativeC60EITailDirectProduct
#print axioms nativeC60EITailDirectProduct_fst
#print axioms nativeC60EITailDirectProduct_residual
#print axioms nativeC60EITailDirectProduct_symm
#print axioms nativeC60EITailDirectProduct_ker_fst
#print axioms nativeK5EIPhysicalAQ_tailDirectProduct

end
end Kuu.F112.Physical
