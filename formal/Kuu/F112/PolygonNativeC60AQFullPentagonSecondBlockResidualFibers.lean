import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteSplitCoherence

/-!
# F112-P94D3EL — second AQ coordinate agreement and residual-fiber preservation

EK constructed the true comparison between one-step and two-step
splittings of the actual finite AQ complementary kernel C_n.
Its first integer block is invariant. EL shows that the following
k integer coordinates are ALSO invariant after removing the first m.
The crucial nonformal input is EK's proof that the genuine Type-valued
18D defect section for the first m coordinates has zero next-k charge.

The first-stage residual in C_(n+m) is the original class x multiplied
by the inverse of its true EI section. Character evaluation on this
product, together with the finite-support Kronecker law, proves that
its next k coordinate values equal the original ones. Thus the EK
coherence comparison fixes BOTH finite integer blocks pointwise.

The remaining component lies in the genuine residual kernel
C_(n+(m+k)). The comparison restricts to a bijection on EACH
fixed-two-coordinate residual fiber, with the inverse induced
by its actual group-isomorphism inverse. This is a statement about
residual information and does not assert that the residual coordinate
is pointwise fixed; that stronger compatibility requires separate
section-concatenation analysis.

The source noncommutative C60 obstruction kernel is never assumed
abelian or free. No full infinite product, 19D filler, or Gray
structure is introduced. Retain strict Kuu, independent Kuu as
one presentation, 14D--18D Type-valued evidence, DS no-go,
all 107 public roots, pinned Lean/mathlib, append-only/same-root.
No sorry, admit or new axiom.
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

section AbstractResidualFiber

/-- A true group isomorphism that preserves two observed coordinates
restricts to a bijection of EACH residual fiber. No assumption
that the final residual coordinate is fixed pointwise is needed. -/
private theorem nativeC60ELFiberBijective
    {A B C : Type*} [Group A] [Group B] [Group C]
    (e : (A × (B × C)) ≃* (A × (B × C)))
    (ha : ∀ p, (e p).1 = p.1)
    (hb : ∀ p, (e p).2.1 = p.2.1)
    (a : A) (b : B) :
    Function.Bijective (fun c : C => (e (a, (b, c))).2.2) := by
  constructor
  · intro c d hcd
    have heq : e (a, (b, c)) = e (a, (b, d)) := by
      apply Prod.ext
      · rw [ha (a, (b, c)), ha (a, (b, d))]
      · apply Prod.ext
        · rw [hb (a, (b, c)), hb (a, (b, d))]
        · exact hcd
    have h := e.injective heq
    exact congrArg (fun p : A × (B × C) => p.2.2) h
  · intro c
    let p := e.symm (a, (b, c))
    have heq : e p = (a, (b, c)) := e.apply_symm_apply (a, (b, c))
    have hp1 : p.1 = a := (ha p).symm.trans (congrArg Prod.fst heq)
    have hp2 : p.2.1 = b :=
      (hb p).symm.trans (congrArg (fun q : A × (B × C) => q.2.1) heq)
    refine ⟨p.2.2, ?_⟩
    change (e (a, (b, p.2.2))).2.2 = c
    have hp : (a, (b, p.2.2)) = p := by
      apply Prod.ext
      · exact hp1.symm
      · apply Prod.ext
        · exact hp2.symm
        · rfl
    rw [hp, heq]

end AbstractResidualFiber

section SecondAQBlock

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The true cumulative EJ residual is exactly the inverse of the
first finite EI section times the source class, viewed in the ACTUAL
abelianization. This is not an abstract chosen complement. -/
theorem nativeC60ELFirstResidual_underlying (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker) :
    ((nativeC60EJCumulativeDirectProduct S F word r n m x).2).1 =
      ((nativeC60EITailFiniteSection S F word r n m
        (nativeC60EHTailReceiver S F word n m x))⁻¹ * x).1 := by
  rfl

/-- The genuine next k integer charges of the first-stage residual
are the next k charges of the original C60 AQ class. The first
m section is invisible to these coordinates by the actual EK
finite-support Kronecker calculation. -/
theorem nativeC60ELNextReceiver_residual (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker)
    (j : Fin k) :
    (nativeC60EHTailReceiver S F word (n + m) k
      ((nativeC60EJCumulativeDirectProduct S F word r n m x).2)) j =
    (nativeC60EHTailReceiver S F word n (m + k) x)
      (Fin.natAdd m j) := by
  let y := (nativeC60EJCumulativeDirectProduct S F word r n m x).2
  let v := nativeC60EHTailReceiver S F word n m x
  let s := nativeC60EITailFiniteSection S F word r n m v
  let iold : Fin ((n + m) + k) := ⟨(n + m) + j.val, by omega⟩
  let inew : Fin (n + (m + k)) := ⟨n + (m + j.val), by omega⟩
  have hsame :
      ((nativeC60EBAbelianReceiver S F word ((n + m) + k)) y.1) iold =
        ((nativeC60EBAbelianReceiver S F word (n + (m + k))) y.1) inew :=
    nativeC60EKReceiver_sameCoordinate S F word y.1
      ((n + m) + k) (n + (m + k)) iold inew (by dsimp [iold, inew]; omega)
  have hs :
      ((nativeC60EBAbelianReceiver S F word (n + (m + k))) s.1) inew = 1 := by
    have h := nativeC60EKSection_future_one S F word r n m k v j
    change ((nativeC60EBAbelianReceiver S F word (n + (m + k))) s.1)
      inew = 1 at h
    exact h
  have hy : y.1 = s.1⁻¹ * x.1 := by
    exact nativeC60ELFirstResidual_underlying S F word r n m x
  have hres :
      ((nativeC60EBAbelianReceiver S F word (n + (m + k))) y.1) inew =
        ((nativeC60EBAbelianReceiver S F word (n + (m + k))) x.1) inew := by
    rw [hy, map_mul, map_inv]
    simp only [Pi.mul_apply, Pi.inv_apply, hs, inv_one, one_mul]
  change ((nativeC60EBAbelianReceiver S F word ((n + m) + k)) y.1)
      iold =
    ((nativeC60EBAbelianReceiver S F word (n + (m + k))) x.1) inew
  exact hsame.trans hres

/-- The actual SECOND integer block agrees across the sequential
and one-stage EJ splittings, including zero ranks. -/
theorem nativeC60ELCoherence_second (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker)
    (j : Fin k) :
    ((nativeC60EKTwoStage S F word r n m k x).2.1) j =
      ((nativeC60EKOneStage S F word r n m k x).2.1) j := by
  change ((nativeC60EJCumulativeDirectProduct S F word r (n + m) k
      ((nativeC60EJCumulativeDirectProduct S F word r n m x).2)).1) j =
    ((nativeC60EJCumulativeDirectProduct S F word r n (m + k) x).1)
      (Fin.natAdd m j)
  rw [nativeC60EJCumulativeDirectProduct_fst,
    nativeC60EJCumulativeDirectProduct_fst]
  exact nativeC60ELNextReceiver_residual S F word r n m k x j

/-- EK's true coherence group isomorphism preserves EVERY
second-block integer charge, not just its initial coordinates. -/
theorem nativeC60ELComparison_second (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (p : (Fin m → Multiplicative ℤ) ×
      ((Fin k → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker))
    (j : Fin k) :
    ((nativeC60EKCoherenceComparison S F word r n m k p).2.1) j =
      p.2.1 j := by
  change ((nativeC60EKTwoStage S F word r n m k)
    ((nativeC60EKOneStage S F word r n m k).symm p)).2.1 j =
      p.2.1 j
  rw [nativeC60ELCoherence_second S F word r n m k
    ((nativeC60EKOneStage S F word r n m k).symm p) j]
  rw [MulEquiv.apply_symm_apply]

/-- The canonical EK comparison fixes the FULL pair of actually
observed integer vectors. Only its genuine residual-kernel
coordinate is free to vary. -/
theorem nativeC60ELComparison_integerProjection (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (p : (Fin m → Multiplicative ℤ) ×
      ((Fin k → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker)) :
    (nativeC60EKCoherenceComparison S F word r n m k p).1 = p.1 ∧
      (nativeC60EKCoherenceComparison S F word r n m k p).2.1 = p.2.1 := by
  constructor
  · funext i
    exact nativeC60EKComparison_head S F word r n m k p i
  · funext j
    exact nativeC60ELComparison_second S F word r n m k p j

/-- MAIN EL RESIDUAL RESULT: For each fixed pair of physically
observed finite integer charge vectors, EK's true comparison
induces a BIJECTION of the remaining honest obstruction-kernel
classes. No residual class is lost, merged, or fabricated. -/
theorem nativeC60ELComparison_residualFiber_bijective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (v : Fin m → Multiplicative ℤ)
    (w : Fin k → Multiplicative ℤ) :
    Function.Bijective (fun z :
      (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker =>
      (nativeC60EKCoherenceComparison S F word r n m k
        (v, (w, z))).2.2) := by
  apply nativeC60ELFiberBijective
    (nativeC60EKCoherenceComparison S F word r n m k)
  · intro p
    exact (nativeC60ELComparison_integerProjection S F word r n m k p).1
  · intro p
    exact (nativeC60ELComparison_integerProjection S F word r n m k p).2

end SecondAQBlock

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

/-- Every genuine physical C60 AU Type-valued AQ context
inherits EL's exact SECOND integer block coherence. -/
theorem nativeK5ELPhysicalAQ_secondBlock
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (n m k : ℕ)
    (x : (nativeC60EBAbelianReceiver (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (nativeK5DOTreeWord tree) n).ker)
    (j : Fin k) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let r := nativeC60DYOriginalZigzagGen S F (nativeK5CEPhysicalAUGenerator W)
    ((nativeC60EKTwoStage S F (nativeK5DOTreeWord tree) r n m k x).2.1) j =
      ((nativeC60EKOneStage S F (nativeK5DOTreeWord tree) r n m k x).2.1) j := by
  dsimp only
  exact nativeC60ELCoherence_second
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) n m k x j

end PhysicalC60AU

#print axioms nativeC60ELFirstResidual_underlying
#print axioms nativeC60ELNextReceiver_residual
#print axioms nativeC60ELCoherence_second
#print axioms nativeC60ELComparison_second
#print axioms nativeC60ELComparison_integerProjection
#print axioms nativeC60ELComparison_residualFiber_bijective
#print axioms nativeK5ELPhysicalAQ_secondBlock

end
end Kuu.F112.Physical
