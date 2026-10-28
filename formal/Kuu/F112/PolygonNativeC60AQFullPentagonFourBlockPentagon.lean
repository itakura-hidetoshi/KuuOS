import Kuu.F112.PolygonNativeC60AQFullPentagonThreeBlockAssociativity

/-!
# F112-P94D3EO — four finite AQ blocks and the honest pentagon of reassociation

EN established strict three-block splitting coherence in the actual
character kernel of the abelianization of the noncommutative original
C60 Type-valued pentagon obstruction kernel. EO retains the concrete
EJ/EN finite AQ splitting and constructs the two paths around the
five-vertex associativity pentagon for four ordered factors.

The four factors are the genuine m-, k-, l-charge groups and
(q-charge group × actual cumulative residual kernel C_(n+m+k+l+q)).
The residual obstruction is thus an actual, typed factor of every
pentagon vertex. No informal quotient identification is made.

The three-edge and two-edge pentagon composites coincide as group
isomorphisms. Their precomposition with the SAME genuine C60 AQ split
agrees with EN's actual grouped finite-deletion route, so the
comparison fixes every integer coordinate AND each actual residual
kernel element. All results include zero ranks and arbitrary natural
n,m,k,l,q.

The strict Kuu core and independent-Kuu presentation, historical
14D--18D Type-valued evidence and DS complete-evidence no-go,
107 public roots, no-Gray policy, pinned Lean/mathlib, append-only
and same-root rules are unchanged. No 19D geometric Type-valued
filler, original noncommutative-kernel abelianity, or infinite-product
splitting is claimed. No new axiom, sorry or admit.
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

private abbrev nativeC60EOInt (rank : ℕ) := Fin rank → Multiplicative ℤ

section TypedGroupPentagon

variable {A B C D : Type*} [Group A] [Group B] [Group C] [Group D]

/-- Three-edge Mac Lane pentagon path
  (((A × B) × C) × D)
    → ((A × (B × C)) × D)
    → (A × ((B × C) × D))
    → (A × (B × (C × D))).
Each map is a genuine multiplication-preserving equivalence. -/
def nativeC60EOPentagonThreeEdges :
    (((A × B) × C) × D) ≃* (A × (B × (C × D))) :=
  ((MulEquiv.prodCongr
      (MulEquiv.prodAssoc : ((A × B) × C) ≃* (A × (B × C)))
      (MulEquiv.refl D)).trans
    (MulEquiv.prodAssoc :
      ((A × (B × C)) × D) ≃* (A × ((B × C) × D)))).trans
    (MulEquiv.prodCongr (MulEquiv.refl A)
      (MulEquiv.prodAssoc :
        ((B × C) × D) ≃* (B × (C × D))))

/-- Two-edge path across the other side of the same five vertices:
  (((A × B) × C) × D)
    → ((A × B) × (C × D))
    → (A × (B × (C × D))). -/
def nativeC60EOPentagonTwoEdges :
    (((A × B) × C) × D) ≃* (A × (B × (C × D))) :=
  (MulEquiv.prodAssoc :
    (((A × B) × C) × D) ≃* ((A × B) × (C × D))).trans
    (MulEquiv.prodAssoc :
      ((A × B) × (C × D)) ≃* (A × (B × (C × D))))

/-- THE FIVE-VERTEX PENTAGON COMMUTES, strictly as an equality
of group equivalences, not merely equality of integer projections. -/
theorem nativeC60EOPentagon_twoPaths :
    (nativeC60EOPentagonThreeEdges :
      (((A × B) × C) × D) ≃* (A × (B × (C × D)))) =
    nativeC60EOPentagonTwoEdges := by
  apply MulEquiv.ext
  rintro ⟨⟨⟨a, b⟩, c⟩, d⟩
  rfl

/-- Both pentagon paths retain each of the four original factors
literally, including an arbitrary nontrivial group in the D slot. -/
theorem nativeC60EOPentagon_apply
    (a : A) (b : B) (c : C) (d : D) :
    (nativeC60EOPentagonThreeEdges
      (((a, b), c), d) :
      A × (B × (C × D))) = (a, (b, (c, d))) := by
  rfl

end TypedGroupPentagon

section GenuineFourAQBlocks

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A ONE-STAGE genuine EJ/EN split, with four explicitly recovered
integer blocks and the ACTUAL cumulative AQ residual kernel.
The final q and l blocks are split by the true Fin tuple map. -/
def nativeC60EOOneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60EOInt m ×
        (nativeC60EOInt k ×
          (nativeC60EOInt l ×
            (nativeC60EOInt q ×
              (nativeC60EBAbelianReceiver S F word
                (n + (m + (k + (l + q))))).ker))) :=
  (nativeC60ENOneStage S F word r n m k (l + q)).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EOInt m))
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EOInt k))
        (nativeC60ENLastTwoSplit l q)))

/-- A genuine GROUPED finite deletion route, first taking the m,
then k, then (l+q) actual character blocks before splitting the
last finite receiver into l and q. -/
def nativeC60EOGroupedStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60EOInt m ×
        (nativeC60EOInt k ×
          (nativeC60EOInt l ×
            (nativeC60EOInt q ×
              (nativeC60EBAbelianReceiver S F word
                (n + (m + (k + (l + q))))).ker))) :=
  (nativeC60ENThreeStage S F word r n m k (l + q)).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EOInt m))
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EOInt k))
        (nativeC60ENLastTwoSplit l q)))

/-- EN's genuine three-block result makes the two paths through
the actual finite C60 AQ splitting agree INCLUDING the residual. -/
theorem nativeC60EOGroupedStage_eq_oneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    nativeC60EOGroupedStage S F word r n m k l q =
      nativeC60EOOneStage S F word r n m k l q := by
  simpa only [nativeC60EOGroupedStage, nativeC60EOOneStage,
    nativeC60ENThreeStage_eq_oneStage]

/-- Regard the honest one-stage split in the FIRST pentagon vertex,
by inverting the genuine group product associator on all four typed
factors. This is only a change of parentheses, not a new quotient. -/
def nativeC60EOLeftBracketedStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      (((nativeC60EOInt m × nativeC60EOInt k) × nativeC60EOInt l) ×
        (nativeC60EOInt q ×
          (nativeC60EBAbelianReceiver S F word
            (n + (m + (k + (l + q))))).ker)) :=
  (nativeC60EOOneStage S F word r n m k l q).trans
    nativeC60EOPentagonTwoEdges.symm

/-- The THREE-edge pentagon path, precomposed with the actual
C60 AQ finite splitting into the first pentagon vertex. -/
def nativeC60EOThreeEdgeAQ (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60EOInt m ×
        (nativeC60EOInt k ×
          (nativeC60EOInt l ×
            (nativeC60EOInt q ×
              (nativeC60EBAbelianReceiver S F word
                (n + (m + (k + (l + q))))).ker))) :=
  (nativeC60EOLeftBracketedStage S F word r n m k l q).trans
    nativeC60EOPentagonThreeEdges

/-- The TWO-edge pentagon path from the same genuine left-bracketed
C60 AQ splitting, with identical Type-valued source data. -/
def nativeC60EOTwoEdgeAQ (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60EOInt m ×
        (nativeC60EOInt k ×
          (nativeC60EOInt l ×
            (nativeC60EOInt q ×
              (nativeC60EBAbelianReceiver S F word
                (n + (m + (k + (l + q))))).ker))) :=
  (nativeC60EOLeftBracketedStage S F word r n m k l q).trans
    nativeC60EOPentagonTwoEdges

/-- The true two-edge pentagon path is exactly the genuine
one-stage four-block splitting, not merely abstractly isomorphic. -/
theorem nativeC60EOTwoEdgeAQ_eq_oneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    nativeC60EOTwoEdgeAQ S F word r n m k l q =
      nativeC60EOOneStage S F word r n m k l q := by
  apply MulEquiv.ext
  intro x
  change
    nativeC60EOPentagonTwoEdges
      ((nativeC60EOPentagonTwoEdges).symm
        (nativeC60EOOneStage S F word r n m k l q x)) =
    nativeC60EOOneStage S F word r n m k l q x
  exact MulEquiv.apply_symm_apply _ _

/-- MAIN EO PENTAGON: the entire group-isomorphism square/pentagon
commutes over the actual C60 AQ residual, including EVERY charge
and EACH genuine residual obstruction element. -/
theorem nativeC60EOPentagonAQ_twoPaths (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    nativeC60EOThreeEdgeAQ S F word r n m k l q =
      nativeC60EOTwoEdgeAQ S F word r n m k l q := by
  apply MulEquiv.ext
  intro x
  change nativeC60EOPentagonThreeEdges
      (nativeC60EOLeftBracketedStage S F word r n m k l q x) =
    nativeC60EOPentagonTwoEdges
      (nativeC60EOLeftBracketedStage S F word r n m k l q x)
  exact DFunLike.congr_fun
    (nativeC60EOPentagon_twoPaths) _

/-- Reassociation is strictly independent of path AND matches EN's
actual sequential finite deletion, on the full honest kernel. -/
theorem nativeC60EOThreeEdgeAQ_eq_groupedStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    nativeC60EOThreeEdgeAQ S F word r n m k l q =
      nativeC60EOGroupedStage S F word r n m k l q := by
  calc
    nativeC60EOThreeEdgeAQ S F word r n m k l q =
        nativeC60EOTwoEdgeAQ S F word r n m k l q :=
      nativeC60EOPentagonAQ_twoPaths S F word r n m k l q
    _ = nativeC60EOOneStage S F word r n m k l q :=
      nativeC60EOTwoEdgeAQ_eq_oneStage S F word r n m k l q
    _ = nativeC60EOGroupedStage S F word r n m k l q :=
      (nativeC60EOGroupedStage_eq_oneStage S F word r n m k l q).symm

/-- The comparison automorphism from three-edge path to the
actual sequential AQ route is IDENTICAL on all finite integer
blocks and on the honest cumulative residual-kernel factor. -/
theorem nativeC60EOThreeEdgeComparison_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    (nativeC60EOGroupedStage S F word r n m k l q).symm.trans
      (nativeC60EOThreeEdgeAQ S F word r n m k l q) =
        MulEquiv.refl
          (nativeC60EOInt m ×
            (nativeC60EOInt k ×
              (nativeC60EOInt l ×
                (nativeC60EOInt q ×
                  (nativeC60EBAbelianReceiver S F word
                    (n + (m + (k + (l + q))))).ker)))) := by
  apply MulEquiv.ext
  intro p
  change nativeC60EOThreeEdgeAQ S F word r n m k l q
    ((nativeC60EOGroupedStage S F word r n m k l q).symm p) = p
  rw [nativeC60EOThreeEdgeAQ_eq_groupedStage]
  exact MulEquiv.apply_symm_apply _ _

/-- The pentagon does not move even one member of an actual fixed
four-charge residual fiber: identity as an element of C_(n+total). -/
theorem nativeC60EOPentagonResidual_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ)
    (v : nativeC60EOInt m) (w : nativeC60EOInt k)
    (t : nativeC60EOInt l) (s : nativeC60EOInt q)
    (z : (nativeC60EBAbelianReceiver S F word
      (n + (m + (k + (l + q))))).ker) :
    (((nativeC60EOGroupedStage S F word r n m k l q).symm.trans
        (nativeC60EOThreeEdgeAQ S F word r n m k l q))
      (v, (w, (t, (s, z))))).2.2.2.2 = z := by
  rw [nativeC60EOThreeEdgeComparison_id]
  rfl

end GenuineFourAQBlocks

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

/-- The actual physical C60 AU Type-valued witness induces strict
four-block AQ reassociation coherence, with full residual preservation. -/
theorem nativeK5EOPhysicalAQ_pentagon
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (n m k l q : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let r := nativeC60DYOriginalZigzagGen S F
      (nativeK5CEPhysicalAUGenerator W)
    nativeC60EOThreeEdgeAQ S F (nativeK5DOTreeWord tree) r n m k l q =
      nativeC60EOTwoEdgeAQ S F (nativeK5DOTreeWord tree) r n m k l q := by
  dsimp only
  exact nativeC60EOPentagonAQ_twoPaths
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) n m k l q

end PhysicalC60AU

#print axioms nativeC60EOPentagonThreeEdges
#print axioms nativeC60EOPentagonTwoEdges
#print axioms nativeC60EOPentagon_twoPaths
#print axioms nativeC60EOOneStage
#print axioms nativeC60EOGroupedStage
#print axioms nativeC60EOGroupedStage_eq_oneStage
#print axioms nativeC60EOPentagonAQ_twoPaths
#print axioms nativeC60EOThreeEdgeAQ_eq_groupedStage
#print axioms nativeC60EOThreeEdgeComparison_id
#print axioms nativeC60EOPentagonResidual_id
#print axioms nativeK5EOPhysicalAQ_pentagon

end
end Kuu.F112.Physical
