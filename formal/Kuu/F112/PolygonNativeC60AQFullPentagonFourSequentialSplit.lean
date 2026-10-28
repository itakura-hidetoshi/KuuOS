import Kuu.F112.PolygonNativeC60AQFullPentagonFourBlockPentagon

/-!
# F112-P94D3EP — four genuinely sequential finite AQ splits

EO proved the associative pentagon over the actual abelianized C60 AQ
obstruction kernel. EP now takes the four steps individually, rather
than only splitting a last finite receiver into two coordinates.

For any natural n,m,k,l,q, including zero, the four-stage map begins
with EJ's actual C_n ≃* Z^m × C_(n+m). It then applies EN's ACTUAL
three consecutive EJ splittings of the C_(n+m) residual for k,l,q.
The final rank transport is explicitly restricted to the equality
(n+m)+(k+(l+q)) = n+(m+(k+(l+q))) and changes no kernel elements.

EM, EN and EO prove exact equality with the single cumulative EJ
split, followed by its genuine Fin coordinate partition; all four
charge blocks and the actual residual subgroup are fixed pointwise.
Neither original noncommutative kernel abelianity nor an infinite
rank splitting or 19D Type-valued geometric filler is asserted.

Retain strict Kuu, independent Kuu as one presentation, DS no-go,
14D--18D Type-valued C60 AU proof histories, 107 public roots,
no Gray, pinned Lean 4.30.0-rc2 / mathlib 5450b53e5..., and
append-only / same-root / overwrite-forbidden constraints.
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

private abbrev nativeC60EPInt (rank : ℕ) := Fin rank → Multiplicative ℤ

section FourActualAQSplittings

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Reassociate ONLY the finite cumulative-rank index of the honest
kernel, without adding a nonphysical quotient or an observation axiom. -/
private def nativeC60EPResidualAssoc (word : List Bool)
    (n m t : ℕ) :
    (nativeC60EBAbelianReceiver S F word ((n + m) + t)).ker ≃*
      (nativeC60EBAbelianReceiver S F word (n + (m + t))).ker := by
  rw [← Nat.add_assoc n m t]

/-- Four consecutive actual EJ splits: m, followed by k, l and q.
The EN three-stage map on C_(n+m) is by definition made of the
real EJ splittings for k, l and q, not a chosen representative. -/
def nativeC60EPFourStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60EPInt m ×
        (nativeC60EPInt k ×
          (nativeC60EPInt l ×
            (nativeC60EPInt q ×
              (nativeC60EBAbelianReceiver S F word
                (n + (m + (k + (l + q))))).ker))) :=
  ((nativeC60EJCumulativeDirectProduct S F word r n m).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt m))
      (nativeC60ENThreeStage S F word r (n + m) k l q))).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt m))
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt k))
        (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt l))
          (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt q))
            (nativeC60EPResidualAssoc S F word n m (k + (l + q)))))))

/-- The same actual C_n first split, followed by EN's one-stage
description of the k+l+q tail, with the identical honest rank cast. -/
def nativeC60EPTailOneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      nativeC60EPInt m ×
        (nativeC60EPInt k ×
          (nativeC60EPInt l ×
            (nativeC60EPInt q ×
              (nativeC60EBAbelianReceiver S F word
                (n + (m + (k + (l + q))))).ker))) :=
  ((nativeC60EJCumulativeDirectProduct S F word r n m).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt m))
      (nativeC60ENOneStage S F word r (n + m) k l q))).trans
    (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt m))
      (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt k))
        (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt l))
          (MulEquiv.prodCongr (MulEquiv.refl (nativeC60EPInt q))
            (nativeC60EPResidualAssoc S F word n m (k + (l + q)))))))

/-- EN's proven three-step coherence, applied to the REAL C_(n+m)
tail, makes all four steps agree with first-m then bundled-tail. -/
theorem nativeC60EPFourStage_eq_tailOneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    nativeC60EPFourStage S F word r n m k l q =
      nativeC60EPTailOneStage S F word r n m k l q := by
  unfold nativeC60EPFourStage nativeC60EPTailOneStage
  rw [nativeC60ENThreeStage_eq_oneStage S F word r (n + m) k l q]

/-- The m-then-bundled-tail route strictly agrees with EO's
single cumulative rank split, without changing any integer coordinate
or residual subgroup element. -/
theorem nativeC60EPTailOneStage_eq_oneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    nativeC60EPTailOneStage S F word r n m k l q =
      nativeC60EOOneStage S F word r n m k l q := by
  apply MulEquiv.ext
  intro x
  have h := nativeC60EMTwoStage_eq_OneStage
    S F word r n m (k + (l + q)) x
  have hk := nativeC60EMTwoStage_eq_OneStage
    S F word r (n + m) k (l + q)
      ((nativeC60EJCumulativeDirectProduct S F word r n m x).2)
  simp only [nativeC60EPTailOneStage, nativeC60EOOneStage,
    nativeC60ENOneStage, nativeC60EKOneStage,
    nativeC60EOGroupedStage, nativeC60ENLastTwoSplit,
    nativeC60EKFiniteCoordinateSplit,
    nativeC60EKTwoStage, nativeC60EJCumulativeDirectProduct,
    nativeC60EPResidualAssoc,
    MulEquiv.trans_apply, MulEquiv.prodCongr_apply] at *
  exact h

/-- The original four individual finite EJ splittings and ONE
genuine cumulative split yield the identical full five-factor
group isomorphism, including the exact residual obstruction. -/
theorem nativeC60EPFourStage_eq_oneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    nativeC60EPFourStage S F word r n m k l q =
      nativeC60EOOneStage S F word r n m k l q := by
  exact (nativeC60EPFourStage_eq_tailOneStage
    S F word r n m k l q).trans
    (nativeC60EPTailOneStage_eq_oneStage S F word r n m k l q)

/-- No ambiguity is left between the true four-step procedure
and either route of EO's five-vertex typed product pentagon. -/
theorem nativeC60EPFourStage_eq_threeEdgePentagon (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    nativeC60EPFourStage S F word r n m k l q =
      nativeC60EOThreeEdgeAQ S F word r n m k l q := by
  calc
    nativeC60EPFourStage S F word r n m k l q =
        nativeC60EOOneStage S F word r n m k l q :=
          nativeC60EPFourStage_eq_oneStage S F word r n m k l q
    _ = nativeC60EOGroupedStage S F word r n m k l q :=
      (nativeC60EOGroupedStage_eq_oneStage S F word r n m k l q).symm
    _ = nativeC60EOThreeEdgeAQ S F word r n m k l q :=
      (nativeC60EOThreeEdgeAQ_eq_groupedStage S F word r n m k l q).symm

/-- Consequently the full four-stage-versus-one-stage coordinate
change is strictly the identity as a MulEquiv, rather than a fiber
bijection or a mere equality of charge projections. -/
theorem nativeC60EPFourStageComparison_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ) :
    (nativeC60EOOneStage S F word r n m k l q).symm.trans
      (nativeC60EPFourStage S F word r n m k l q) =
        MulEquiv.refl
          (nativeC60EPInt m ×
            (nativeC60EPInt k ×
              (nativeC60EPInt l ×
                (nativeC60EPInt q ×
                  (nativeC60EBAbelianReceiver S F word
                    (n + (m + (k + (l + q))))).ker)))) := by
  apply MulEquiv.ext
  intro p
  change nativeC60EPFourStage S F word r n m k l q
      ((nativeC60EOOneStage S F word r n m k l q).symm p) = p
  rw [nativeC60EPFourStage_eq_oneStage]
  exact MulEquiv.apply_symm_apply _ _

/-- Each actual residual class survives the four sequential steps
pointwise, after comparison with one-step finite removal. -/
theorem nativeC60EPFourStageResidual_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k l q : ℕ)
    (v : nativeC60EPInt m) (w : nativeC60EPInt k)
    (t : nativeC60EPInt l) (s : nativeC60EPInt q)
    (z : (nativeC60EBAbelianReceiver S F word
      (n + (m + (k + (l + q))))).ker) :
    (((nativeC60EOOneStage S F word r n m k l q).symm.trans
      (nativeC60EPFourStage S F word r n m k l q))
      (v, (w, (t, (s, z))))).2.2.2.2 = z := by
  rw [nativeC60EPFourStageComparison_id]
  rfl

end FourActualAQSplittings

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

/-- Fully physical dependent C60 AU proof data supports the actual
four-step finite AQ coherence with no new geometric filler. -/
theorem nativeK5EPPhysicalAQ_fourStageCoherence_id
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (n m k l q : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let r := nativeC60DYOriginalZigzagGen S F
      (nativeK5CEPhysicalAUGenerator W)
    (nativeC60EOOneStage S F (nativeK5DOTreeWord tree) r n m k l q).symm.trans
      (nativeC60EPFourStage S F (nativeK5DOTreeWord tree) r n m k l q) =
        MulEquiv.refl
          (nativeC60EPInt m ×
            (nativeC60EPInt k ×
              (nativeC60EPInt l ×
                (nativeC60EPInt q ×
                  (nativeC60EBAbelianReceiver S F
                    (nativeK5DOTreeWord tree)
                    (n + (m + (k + (l + q))))).ker)))) := by
  dsimp only
  exact nativeC60EPFourStageComparison_id
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) n m k l q

end PhysicalC60AU

#print axioms nativeC60EPFourStage
#print axioms nativeC60EPTailOneStage
#print axioms nativeC60EPFourStage_eq_tailOneStage
#print axioms nativeC60EPTailOneStage_eq_oneStage
#print axioms nativeC60EPFourStage_eq_oneStage
#print axioms nativeC60EPFourStage_eq_threeEdgePentagon
#print axioms nativeC60EPFourStageComparison_id
#print axioms nativeC60EPFourStageResidual_id
#print axioms nativeK5EPPhysicalAQ_fourStageCoherence_id

end
end Kuu.F112.Physical
