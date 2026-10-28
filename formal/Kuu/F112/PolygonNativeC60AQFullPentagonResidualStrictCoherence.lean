import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteSectionConcatenation

/-!
# F112-P94D3EM — strict residual coherence of two finite AQ splittings

The concrete EI sections concatenate exactly via EM's finitely
supported integer identity. This proves the residual components of
the genuine EK one-step and two-step finite AQ splittings coincide,
not merely that their fixed-charge fibers are in bijection (EL).
Consequently the EK comparison group isomorphism is the identity.

All statements concern the actual complementary subgroups of the
ABELIANIZATION of the original noncommutative C60 AQ obstruction.
Preserve the strict Kuu, independent Kuu as one presentation, the
dependent 14D--18D evidence and DS complete-evidence no-go.
No infinite direct-product surjection or split, no original-kernel
commutativity, 19D filler or Gray structure is asserted.
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

section ResidualStrictCoherence

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The actual one-stage tail receiver is the concatenation of
the first finite block and the next receiver of its genuine
first-stage residual. There is no chosen quotient presentation. -/
theorem nativeC60EMReceiver_concat (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker) :
    nativeC60EHTailReceiver S F word n (m + k) x =
      Fin.append (nativeC60EHTailReceiver S F word n m x)
        (nativeC60EHTailReceiver S F word (n + m) k
          ((nativeC60EJCumulativeDirectProduct S F word r n m x).2)) := by
  funext i
  refine Fin.addCases (fun j => ?_) (fun j => ?_) i
  · simpa only [Fin.append_left] using
      (nativeC60EKReceiver_head S F word n m k x j).symm
  · simpa only [Fin.append_right] using
      (nativeC60ELNextReceiver_residual S F word r n m k x j).symm

/-- The residual obtained by two true finite deletions and the
one from a single deletion have identical UNDERLYING abelianized
classes. This proof computes the actual section products, rather
than postulating that residual fibers are identical. -/
theorem nativeC60EMCumulativeResidual_underlying (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker) :
    ((nativeC60EJCumulativeDirectProduct S F word r (n + m) k
      ((nativeC60EJCumulativeDirectProduct S F word r n m x).2)).2).1 =
    ((nativeC60EJCumulativeDirectProduct S F word r n (m + k) x).2).1 := by
  let y := (nativeC60EJCumulativeDirectProduct S F word r n m x).2
  let v := nativeC60EHTailReceiver S F word n m x
  let w := nativeC60EHTailReceiver S F word (n + m) k y
  let t := nativeC60EHTailReceiver S F word n (m + k) x
  let s1 := nativeC60EITailFiniteSection S F word r n m
  let s2 := nativeC60EITailFiniteSection S F word r (n + m) k
  let sFull := nativeC60EITailFiniteSection S F word r n (m + k)
  have hreceiver : t = Fin.append v w :=
    nativeC60EMReceiver_concat S F word r n m k x
  have hs :
      (sFull t).1 = (s1 v).1 * (s2 w).1 := by
    rw [hreceiver]
    have hh := congrArg
      (fun z : (nativeC60EBAbelianReceiver S F word n).ker => z.1)
      (nativeC60EMTailFiniteSection_concat S F word r n m k v w)
    change (sFull (Fin.append v w)).1 = (s1 v).1 * (s2 w).1 at hh
    exact hh
  have hy : y.1 = (s1 v).1⁻¹ * x.1 := by
    have hh := nativeC60ELFirstResidual_underlying S F word r n m x
    change y.1 = (s1 v).1⁻¹ * x.1 at hh
    exact hh
  have hsecond :
      ((nativeC60EJCumulativeDirectProduct S F word r (n + m) k y).2).1 =
        (s2 w).1⁻¹ * y.1 := by
    have hh := nativeC60ELFirstResidual_underlying S F word r (n + m) k y
    change ((nativeC60EJCumulativeDirectProduct S F word r (n + m) k y).2).1 =
      (s2 w).1⁻¹ * y.1 at hh
    exact hh
  have hone :
      ((nativeC60EJCumulativeDirectProduct S F word r n (m + k) x).2).1 =
        (sFull t).1⁻¹ * x.1 := by
    have hh := nativeC60ELFirstResidual_underlying S F word r n (m + k) x
    change ((nativeC60EJCumulativeDirectProduct S F word r n (m + k) x).2).1 =
      (sFull t).1⁻¹ * x.1 at hh
    exact hh
  calc
    ((nativeC60EJCumulativeDirectProduct S F word r (n + m) k y).2).1 =
        (s2 w).1⁻¹ * y.1 := hsecond
    _ = (s2 w).1⁻¹ * ((s1 v).1⁻¹ * x.1) := by rw [hy]
    _ = ((s1 v).1 * (s2 w).1)⁻¹ * x.1 := by
      simp only [mul_inv_rev, mul_assoc]
    _ = (sFull t).1⁻¹ * x.1 := by rw [hs]
    _ = ((nativeC60EJCumulativeDirectProduct S F word r n (m + k) x).2).1 :=
      hone.symm

/-- The exact residual coordinates of EK's actual two-stage and
one-stage group isomorphisms coincide; the equality is of genuine
subgroup elements, not merely of their observed integer charges. -/
theorem nativeC60EMTwoStage_residual (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker) :
    (nativeC60EKTwoStage S F word r n m k x).2.2 =
      (nativeC60EKOneStage S F word r n m k x).2.2 := by
  apply Subtype.ext
  have h := nativeC60EMCumulativeResidual_underlying S F word r n m k x
  first
  | simpa [nativeC60EKTwoStage, nativeC60EKOneStage, Nat.add_assoc] using h
  | 
    cases Nat.add_assoc n m k
    simpa [nativeC60EKTwoStage, nativeC60EKOneStage] using h

/-- EM upgrades EK/EL's coordinate and fiber results to exact
agreement of the entire actual two-stage and one-stage split. -/
theorem nativeC60EMTwoStage_eq_OneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker) :
    nativeC60EKTwoStage S F word r n m k x =
      nativeC60EKOneStage S F word r n m k x := by
  apply Prod.ext
  · funext i
    exact nativeC60EKCoherence_head S F word r n m k x i
  · apply Prod.ext
    · funext j
      exact nativeC60ELCoherence_second S F word r n m k x j
    · exact nativeC60EMTwoStage_residual S F word r n m k x

/-- MAIN EM THEOREM: EK's concrete comparison is the identity
group isomorphism on both finite charge blocks and the true
residual kernel, rather than an arbitrary fiberwise bijection. -/
theorem nativeC60EMCoherenceComparison_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ) :
    nativeC60EKCoherenceComparison S F word r n m k =
      MulEquiv.refl ((Fin m → Multiplicative ℤ) ×
        ((Fin k → Multiplicative ℤ) ×
          (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker)) := by
  apply MulEquiv.ext
  intro p
  change nativeC60EKTwoStage S F word r n m k
    ((nativeC60EKOneStage S F word r n m k).symm p) = p
  rw [nativeC60EMTwoStage_eq_OneStage]
  exact MulEquiv.apply_symm_apply
    (nativeC60EKOneStage S F word r n m k) p

/-- All fixed-charge residual fibers are preserved pointwise. -/
theorem nativeC60EMResidualFiber_id (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (v : Fin m → Multiplicative ℤ)
    (w : Fin k → Multiplicative ℤ)
    (z : (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker) :
    (nativeC60EKCoherenceComparison S F word r n m k (v, (w, z))).2.2 =
      z := by
  rw [nativeC60EMCoherenceComparison_id]
  rfl

end ResidualStrictCoherence

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

/-- The physical C60 AU Type-valued context inherits the genuine
identity coherence for finite integer AQ deletions. -/
theorem nativeK5EMPhysicalAQ_coherence_id
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (n m k : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let r := nativeC60DYOriginalZigzagGen S F
      (nativeK5CEPhysicalAUGenerator W)
    nativeC60EKCoherenceComparison S F (nativeK5DOTreeWord tree)
      r n m k =
      MulEquiv.refl ((Fin m → Multiplicative ℤ) ×
        ((Fin k → Multiplicative ℤ) ×
          (nativeC60EBAbelianReceiver S F
            (nativeK5DOTreeWord tree) (n + (m + k))).ker)) := by
  dsimp only
  exact nativeC60EMCoherenceComparison_id
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) n m k

end PhysicalC60AU

#print axioms nativeC60EMReceiver_concat
#print axioms nativeC60EMCumulativeResidual_underlying
#print axioms nativeC60EMTwoStage_residual
#print axioms nativeC60EMTwoStage_eq_OneStage
#print axioms nativeC60EMCoherenceComparison_id
#print axioms nativeC60EMResidualFiber_id
#print axioms nativeK5EMPhysicalAQ_coherence_id

end
end Kuu.F112.Physical
