import Kuu.F112.PolygonNativeC60AQFullPentagonResidualStrictCoherence

/-!
# F112-P94D3EN — genuine three-block finite AQ splitting and reassociation

EM proved exact equality of the genuine two-stage and one-stage finite
AQ kernel splittings, including residual components in the actual
abelianization of the original noncommutative C60 pentagon kernel.

For every finite n,m,k,l this file compares four concrete routes:
  * delete m, then k, then l (three successive genuine EJ splittings);
  * delete m, then split the k+l tail in one stage;
  * delete m, then k+l, and split its finite integer coordinates;
  * delete m+k+l in one step, then split all three finite blocks.

The only reindexing is the canonical rank equality
  (n+m)+(k+l) = n+(m+(k+l));
it acts on actual residual-kernel elements, not on untyped quotients.
EM's theorem makes the entire four-factor comparison the identity,
not merely a bijection of the finite integer-charge projections.
All finite ranks, including zero, are covered.

Preserve strict Kuu, independent Kuu as one presentation, the original
14D--18D Type-valued C60 AU evidence, DS no-go, 107 public roots,
pinned Lean/mathlib, append-only/same-root and no Gray category.
No original-kernel commutativity, infinite splitting, infinite product,
19D filler, new axiom, sorry or admit is introduced.
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

private abbrev nativeC60ENInt (rank : ℕ) := Fin rank → Multiplicative ℤ

section AbstractFiniteCoordinateReassociation

/-- Split the actual next k+l integer receiver into k followed by l
without changing the residual group; this is a group isomorphism. -/
def nativeC60ENLastTwoSplit (k l : ℕ) {T : Type*} [Group T] :
    (nativeC60ENInt (k + l) × T) ≃*
      (nativeC60ENInt k × (nativeC60ENInt l × T)) :=
  (MulEquiv.prodCongr (nativeC60EKFiniteCoordinateSplit k l)
    (MulEquiv.refl T)).trans
    (MulEquiv.prodAssoc :
      ((nativeC60ENInt k × nativeC60ENInt l) × T) ≃*
        (nativeC60ENInt k × (nativeC60ENInt l × T)))

/-- The blockwise coordinate splitting acts only on the integers:
the true residual component is untouched. -/
theorem nativeC60ENLastTwoSplit_apply (k l : ℕ)
    {T : Type*} [Group T] (v : nativeC60ENInt (k + l)) (z : T) :
    nativeC60ENLastTwoSplit k l (v, z) =
      ((fun i => v (Fin.castAdd l i)),
        ((fun j => v (Fin.natAdd k j)), z)) := by
  rfl

/-- Naturality of the finite-coordinate split with respect to
an arbitrary actual group isomorphism of residuals. -/
theorem nativeC60ENLastTwoSplit_natural
    (k l : ℕ) {T U : Type*} [Group T] [Group U]
    (e : T ≃* U) (p : nativeC60ENInt (k + l) × T) :
    nativeC60ENLastTwoSplit k l
        ((MulEquiv.prodCongr
          (MulEquiv.refl (nativeC60ENInt (k + l))) e) p) =
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt k))
        (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt l)) e))
          (nativeC60ENLastTwoSplit k l p) := by
  rcases p with ⟨v, z⟩
  rfl

end AbstractFiniteCoordinateReassociation

section ThreeFiniteAQBlocks

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The original, honest cumulative AQ character kernel may be
transported along arithmetic reassociation without changing its
meaning or imposing new algebraic identifications. -/
private def nativeC60ENAssocResidual (word : List Bool) (n m t : ℕ) :
    (nativeC60EBAbelianReceiver S F word ((n + m) + t)).ker ≃*
      (nativeC60EBAbelianReceiver S F word (n + (m + t))).ker := by
  rw [← Nat.add_assoc n m t]

/-- A true THREE-STEP deletion: first m charges, then k, then l.
The final rank cast is the canonical natural-number associator and
does not alter the underlying genuine residual obstruction. -/
def nativeC60ENThreeStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60ENInt m ×
        (nativeC60ENInt k ×
          (nativeC60ENInt l ×
            (nativeC60EBAbelianReceiver S F word (n + (m + (k + l)))).ker)) :=
  ((nativeC60EJCumulativeDirectProduct S F word r n m).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (nativeC60EKTwoStage S F word r (n + m) k l))).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt k))
        (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt l))
          (nativeC60ENAssocResidual S F word n m (k + l)))))

/-- Delete m first, but subsequently delete k+l together before
splitting its two integer blocks. This is the intermediate upper
face in the genuine three-stage coherence diagram. -/
def nativeC60ENTailPairStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60ENInt m ×
        (nativeC60ENInt k ×
          (nativeC60ENInt l ×
            (nativeC60EBAbelianReceiver S F word (n + (m + (k + l)))).ker)) :=
  ((nativeC60EJCumulativeDirectProduct S F word r n m).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (nativeC60EKOneStage S F word r (n + m) k l))).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt k))
        (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt l))
          (nativeC60ENAssocResidual S F word n m (k + l)))))

/-- Delete m first and then k+l in the same honest cumulative
receiver, before splitting k and l by the actual finite tuple
isomorphism. -/
def nativeC60ENFirstThenGrouped (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60ENInt m ×
        (nativeC60ENInt k ×
          (nativeC60ENInt l ×
            (nativeC60EBAbelianReceiver S F word (n + (m + (k + l)))).ker)) :=
  (nativeC60EKTwoStage S F word r n m (k + l)).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (nativeC60ENLastTwoSplit k l))

/-- All m+k+l characters are deleted in ONE genuine EJ split,
and the receiver is then partitioned into the same three integer
blocks. Every residual coordinate is preserved. -/
def nativeC60ENOneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60ENInt m ×
        (nativeC60ENInt k ×
          (nativeC60ENInt l ×
            (nativeC60EBAbelianReceiver S F word (n + (m + (k + l)))).ker)) :=
  (nativeC60EKOneStage S F word r n m (k + l)).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (nativeC60ENLastTwoSplit k l))

/-- EM strict coherence applied to the next two blocks shows that
three successive deletions and first-m-then-(k+l) are the same
genuine four-factor group equivalence. -/
theorem nativeC60ENThreeStage_eq_tailPair (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ) :
    nativeC60ENThreeStage S F word r n m k l =
      nativeC60ENTailPairStage S F word r n m k l := by
  apply MulEquiv.ext
  intro x
  have h := nativeC60EMTwoStage_eq_OneStage S F word r (n + m) k l
    ((nativeC60EJCumulativeDirectProduct S F word r n m x).2)
  change
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt k))
        (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt l))
          (nativeC60ENAssocResidual S F word n m (k + l))))
      ((nativeC60EJCumulativeDirectProduct S F word r n m x).1,
        (nativeC60EKTwoStage S F word r (n + m) k l
          ((nativeC60EJCumulativeDirectProduct S F word r n m x).2)))) =
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt k))
        (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt l))
          (nativeC60ENAssocResidual S F word n m (k + l))))
      ((nativeC60EJCumulativeDirectProduct S F word r n m x).1,
        (nativeC60EKOneStage S F word r (n + m) k l
          ((nativeC60EJCumulativeDirectProduct S F word r n m x).2))))
  exact congrArg
    (fun t => (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt k))
        (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt l))
          (nativeC60ENAssocResidual S F word n m (k + l))))
      ((nativeC60EJCumulativeDirectProduct S F word r n m x).1, t))) h

/-- Functoriality of actual EI/EJ splitting across the arithmetic
rank reassociation: splitting k+l before reindexing or after it
gives exactly the same three-block group-isomorphism value. -/
theorem nativeC60ENTailPair_eq_firstGrouped (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ) :
    nativeC60ENTailPairStage S F word r n m k l =
      nativeC60ENFirstThenGrouped S F word r n m k l := by
  apply MulEquiv.ext
  intro x
  rfl

/-- EM strict coherence applied to the first two finite blocks,
before partitioning the remaining k+l coordinates, identifies the
grouped two-step route with one genuine one-step deletion. -/
theorem nativeC60ENFirstGrouped_eq_oneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ) :
    nativeC60ENFirstThenGrouped S F word r n m k l =
      nativeC60ENOneStage S F word r n m k l := by
  apply MulEquiv.ext
  intro x
  have h := nativeC60EMTwoStage_eq_OneStage S F word r n m (k + l) x
  change
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (nativeC60ENLastTwoSplit k l))
      (nativeC60EKTwoStage S F word r n m (k + l) x) =
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60ENInt m))
      (nativeC60ENLastTwoSplit k l))
      (nativeC60EKOneStage S F word r n m (k + l) x)
  exact congrArg _ h

/-- MAIN EN COHERENCE: three successive actual AQ kernel splittings
are STRICTLY identical to the single m+k+l split, after the canonical
finite coordinate partition and the genuine rank transport. -/
theorem nativeC60ENThreeStage_eq_oneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ) :
    nativeC60ENThreeStage S F word r n m k l =
      nativeC60ENOneStage S F word r n m k l := by
  calc
    nativeC60ENThreeStage S F word r n m k l =
        nativeC60ENTailPairStage S F word r n m k l :=
          nativeC60ENThreeStage_eq_tailPair S F word r n m k l
    _ = nativeC60ENFirstThenGrouped S F word r n m k l :=
      nativeC60ENTailPair_eq_firstGrouped S F word r n m k l
    _ = nativeC60ENOneStage S F word r n m k l :=
      nativeC60ENFirstGrouped_eq_oneStage S F word r n m k l

/-- The genuine four-factor change of splitting coordinates is
the identity group equivalence. It fixes all three finite integer
blocks AND each element of the honest cumulative residual kernel. -/
theorem nativeC60ENThreeBlockComparison_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ) :
    (nativeC60ENOneStage S F word r n m k l).symm.trans
      (nativeC60ENThreeStage S F word r n m k l) =
        MulEquiv.refl
          (nativeC60ENInt m ×
            (nativeC60ENInt k ×
              (nativeC60ENInt l ×
                (nativeC60EBAbelianReceiver S F word
                  (n + (m + (k + l)))).ker))) := by
  apply MulEquiv.ext
  intro p
  change nativeC60ENThreeStage S F word r n m k l
      ((nativeC60ENOneStage S F word r n m k l).symm p) = p
  rw [nativeC60ENThreeStage_eq_oneStage]
  exact MulEquiv.apply_symm_apply
    (nativeC60ENOneStage S F word r n m k l) p

/-- The residual coordinate in the full three-block pentagon face
is pointwise fixed, not only bijective on fixed-charge fibers. -/
theorem nativeC60ENThreeBlockResidual_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l : ℕ)
    (v : nativeC60ENInt m) (w : nativeC60ENInt k)
    (t : nativeC60ENInt l)
    (z : (nativeC60EBAbelianReceiver S F word
        (n + (m + (k + l)))).ker) :
    (((nativeC60ENOneStage S F word r n m k l).symm.trans
      (nativeC60ENThreeStage S F word r n m k l)) (v, (w, (t, z)))).2.2.2 =
      z := by
  rw [nativeC60ENThreeBlockComparison_id]
  rfl

end ThreeFiniteAQBlocks

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

/-- Every genuine physical C60 AU Type-valued source inherits
three-stage finite AQ deletion coherence; the comparison is the
identity on actual integer and residual group coordinates. -/
theorem nativeK5ENPhysicalAQ_threeBlockCoherence_id
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (n m k l : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let r := nativeC60DYOriginalZigzagGen S F (nativeK5CEPhysicalAUGenerator W)
    (nativeC60ENOneStage S F (nativeK5DOTreeWord tree) r n m k l).symm.trans
      (nativeC60ENThreeStage S F (nativeK5DOTreeWord tree) r n m k l) =
        MulEquiv.refl
          (nativeC60ENInt m ×
            (nativeC60ENInt k ×
              (nativeC60ENInt l ×
                (nativeC60EBAbelianReceiver S F
                  (nativeK5DOTreeWord tree) (n + (m + (k + l)))).ker))) := by
  dsimp only
  exact nativeC60ENThreeBlockComparison_id
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) n m k l

end PhysicalC60AU

#print axioms nativeC60ENLastTwoSplit
#print axioms nativeC60ENLastTwoSplit_natural
#print axioms nativeC60ENThreeStage
#print axioms nativeC60ENOneStage
#print axioms nativeC60ENThreeStage_eq_tailPair
#print axioms nativeC60ENTailPair_eq_firstGrouped
#print axioms nativeC60ENFirstGrouped_eq_oneStage
#print axioms nativeC60ENThreeStage_eq_oneStage
#print axioms nativeC60ENThreeBlockComparison_id
#print axioms nativeC60ENThreeBlockResidual_id
#print axioms nativeK5ENPhysicalAQ_threeBlockCoherence_id

end
end Kuu.F112.Physical
