import Kuu.F112.PolygonNativeC60AQFullPentagonFourSequentialSplit

/-!
# F112-P94D3EQ — arbitrary finite lists of genuine AQ block deletions

EP established strict coherence of four sequential finite rank AQ
deletions. EQ does not assume a fixed number of steps: the input is
an arbitrary LIST of finite natural-number block ranks, including
the empty list and zero-sized blocks.

Each recursive step is literally EJ's already proved genuine
  C_n ≃* (Fin m → Multiplicative ℤ) × C_(n+m).
The final nested tower is constructed by structural recursion on
the input list. Its last factor is the ACTUAL kernel of the original
abelianized C60 AQ receiver at the cumulative rank, not an assumed
complement, quotient, or free abelian replacement.

The original noncommutative AQ obstruction kernel is never declared
commutative or free. No infinite-rank splitting, full infinite-product
surjectivity, 19D C60 geometric filler or Gray structure is inferred.
Preserve strict Kuu, independent Kuu as one presentation, DS no-go,
14D--18D original Type-valued proof histories, 107 public roots,
pinned Lean/mathlib and append-only/same-root policy.
No new axiom, sorry or admit. Copyright Hidetoshi Itakura / 板倉英俊.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

section ArbitraryFiniteAQBlocks

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- An ordered, arbitrarily long but FINITE list of true integer
blocks, ending in the honest C60 AQ residual kernel. The index of
this residual is accumulated one block at a time. -/
def nativeC60EQBlocks (word : List Bool) (start : ℕ) :
    List ℕ → Type _
  | [] => (nativeC60EBAbelianReceiver S F word start).ker
  | rank :: tail =>
      (Fin rank → Multiplicative ℤ) ×
        nativeC60EQBlocks word (start + rank) tail

/-- The nested block tower is a group at every finite length.
At its terminal vertex the group is the ACTUAL abelianization
character kernel, which already has its inherited group structure. -/
instance nativeC60EQBlocksGroup (word : List Bool)
    (start : ℕ) (ranks : List ℕ) :
    Group (nativeC60EQBlocks S F word start ranks) := by
  induction ranks generalizing start with
  | nil =>
      change Group ((nativeC60EBAbelianReceiver S F word start).ker)
      infer_instance
  | cons rank tail ih =>
      change Group ((Fin rank → Multiplicative ℤ) ×
        nativeC60EQBlocks S F word (start + rank) tail)
      letI : Group (nativeC60EQBlocks S F word (start + rank) tail) :=
        ih (start + rank)
      infer_instance

/-- Cumulative rank calculated by the actual ordered finite
deletion procedure. No infinite sum or completion is involved. -/
def nativeC60EQFinalRank (start : ℕ) : List ℕ → ℕ
  | [] => start
  | rank :: tail => nativeC60EQFinalRank (start + rank) tail

/-- The iterated rank is precisely the ordinary finite List.sum.
In particular, no rank is lost under repeated adjoining of blocks. -/
theorem nativeC60EQFinalRank_eq_sum (start : ℕ) (ranks : List ℕ) :
    nativeC60EQFinalRank start ranks = start + ranks.sum := by
  induction ranks generalizing start with
  | nil =>
      simp [nativeC60EQFinalRank]
  | cons rank tail ih =>
      change nativeC60EQFinalRank (start + rank) tail =
        start + (rank + tail.sum)
      rw [ih]
      omega

/-- THE ACTUAL ARBITRARY-LENGTH AQ SPLIT: a finite ordered list
of block ranks yields a genuine group isomorphism by composing
the verified EJ splitting at each step; no chosen set-theoretic
preimages and no extra splitting hypothesis are used. -/
def nativeC60EQIteratedDirectProduct (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) :
    (ranks : List ℕ) →
      (nativeC60EBAbelianReceiver S F word start).ker ≃*
        nativeC60EQBlocks S F word start ranks
  | [] => MulEquiv.refl _
  | rank :: tail =>
      (nativeC60EJCumulativeDirectProduct S F word r start rank).trans
        (MulEquiv.prodCongr
          (MulEquiv.refl (Fin rank → Multiplicative ℤ))
          (nativeC60EQIteratedDirectProduct word r (start + rank) tail))

/-- The first observed finite block is EXACTLY the genuine EH
tail character receiver; later splitting steps never alter it. -/
theorem nativeC60EQIteratedDirectProduct_head (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start rank : ℕ) (tail : List ℕ)
    (x : (nativeC60EBAbelianReceiver S F word start).ker) :
    (nativeC60EQIteratedDirectProduct S F word r start
      (rank :: tail) x).1 =
        nativeC60EHTailReceiver S F word start rank x := by
  change (nativeC60EJCumulativeDirectProduct S F word r
    start rank x).1 = nativeC60EHTailReceiver S F word start rank x
  exact nativeC60EJCumulativeDirectProduct_fst S F word r start rank x

/-- Every honest list splitting has an explicit inverse; the
reverse procedure recombines actual EJ sections and residuals
back into precisely the original C60 AQ kernel class. -/
theorem nativeC60EQIteratedDirectProduct_inverse (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (ranks : List ℕ)
    (x : (nativeC60EBAbelianReceiver S F word start).ker) :
    (nativeC60EQIteratedDirectProduct S F word r start ranks).symm
      (nativeC60EQIteratedDirectProduct S F word r start ranks x) = x :=
  (nativeC60EQIteratedDirectProduct S F word r start ranks).symm_apply_apply x

/-- For every arbitrarily long finite rank list, the actual
cumulative residual kernel remains non-finitely generated.
This restates EH at the independently verified final rank; it
does NOT assert infinite direct-product surjectivity. -/
theorem nativeC60EQFiniteListResidual_not_fg (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (ranks : List ℕ) :
    ¬ Group.FG
      ((nativeC60EBAbelianReceiver S F word
        (nativeC60EQFinalRank start ranks)).ker) :=
  nativeC60EHTailComplement_not_fg S F word r
    (nativeC60EQFinalRank start ranks)

end ArbitraryFiniteAQBlocks

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

/-- Every genuine physical C60 AU Type-valued context inherits
actual nested finite AQ decompositions for an ARBITRARY finite
ordered list of integer block ranks (not a fixed iteration count). -/
def nativeK5EQPhysicalAQ_finiteListSplit
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree)
    (start : ℕ) (ranks : List ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    (nativeC60EBAbelianReceiver S F
      (nativeK5DOTreeWord tree) start).ker ≃*
      nativeC60EQBlocks S F (nativeK5DOTreeWord tree) start ranks :=
  nativeC60EQIteratedDirectProduct
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) start ranks

end PhysicalC60AU

#print axioms nativeC60EQBlocks
#print axioms nativeC60EQFinalRank_eq_sum
#print axioms nativeC60EQIteratedDirectProduct
#print axioms nativeC60EQIteratedDirectProduct_head
#print axioms nativeC60EQIteratedDirectProduct_inverse
#print axioms nativeC60EQFiniteListResidual_not_fg
#print axioms nativeK5EQPhysicalAQ_finiteListSplit

end
end Kuu.F112.Physical
