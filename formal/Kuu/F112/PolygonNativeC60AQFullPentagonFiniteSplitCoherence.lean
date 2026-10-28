import Kuu.F112.PolygonNativeC60AQFullPentagonCumulativeTailKernel
import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.Algebra.Group.Prod

/-!
# F112-P94D3EK — coherent two-step versus one-step finite AQ kernel splitting

EJ proved genuine split group isomorphisms
  C_n ≃* Z^m × C_(n+m),
for every finite n,m, where C_n is the ACTUAL character kernel
inside the abelianization of the original noncommutative C60
Type-valued pentagon obstruction kernel.

EK compares two finite removal protocols:
  (1) n → n+m → n+(m+k), producing Z^m × (Z^k × C_(n+(m+k)));
  (2) n → n+(m+k), producing Z^(m+k) × C_(n+(m+k)).
The one-stage protocol uses the actual finite-coordinate splitting
Fin (m+k) into the initial m and the following k coordinates,
NOT a new formal quotient.

Both protocols are explicit group isomorphisms, and the canonical
comparison is their actual change of coordinates. The comparison
triangle strictly commutes. The first block is proved to equal the
actual EH/EE integer charges on the original obstruction kernel.
The second block is also checked using the vanishing of all later
coordinates of EI's genuinely finitely supported section.

All results are at arbitrary finite ranks including zero. The
original noncommutative obstruction kernel is NEVER assumed
abelian/free, and no infinite direct-product split or geometric
19D Type-valued filler is claimed. Preserve strict Kuu and
independent Kuu as one presentation, original 14D--18D evidence,
DS complete-evidence no-go, C60 gauge context, no Gray, public
107 roots, append-only/same-root and pinned Lean/mathlib.
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

section FiniteTupleSplit

/-- The genuine finite-coordinate concatenation as a multiplicative
equivalence, on the same integer-valued receiver groups used in EH.
Both inverse and multiplicativity are explicit and include m=0/k=0. -/
def nativeC60EKFiniteCoordinateSplit (m k : ℕ) :
    (Fin (m + k) → Multiplicative ℤ) ≃*
      (Fin m → Multiplicative ℤ) × (Fin k → Multiplicative ℤ) where
  toFun v := (fun i => v (Fin.castAdd k i), fun j => v (Fin.natAdd m j))
  invFun p := Fin.append p.1 p.2
  left_inv v := by
    funext i
    refine Fin.addCases (fun j => ?_) (fun j => ?_) i
    · exact Fin.append_left _ _ j
    · exact Fin.append_right _ _ j
  right_inv p := by
    rcases p with ⟨v, w⟩
    apply Prod.ext
    · funext i
      exact Fin.append_left v w i
    · funext j
      exact Fin.append_right v w j
  map_mul' v w := by
    apply Prod.ext
    · funext i
      rfl
    · funext j
      rfl

end FiniteTupleSplit

section FiniteRankC60Coherence

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A TWO-STEP true group isomorphism, obtained by reusing EJ
first for m genuine AQ coordinates and then for k more. -/
def nativeC60EKTwoStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      (Fin m → Multiplicative ℤ) ×
        ((Fin k → Multiplicative ℤ) ×
          (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker) := by
  let residualAssoc :
      (nativeC60EBAbelianReceiver S F word ((n + m) + k)).ker ≃*
        (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker := by
    rw [← Nat.add_assoc n m k]
    exact MulEquiv.refl _
  exact
    ((nativeC60EJCumulativeDirectProduct S F word r n m).trans
      (MulEquiv.prodCongr
        (MulEquiv.refl (Fin m → Multiplicative ℤ))
        (nativeC60EJCumulativeDirectProduct S F word r (n + m) k))).trans
      (MulEquiv.prodCongr
        (MulEquiv.refl (Fin m → Multiplicative ℤ))
        (MulEquiv.prodCongr
          (MulEquiv.refl (Fin k → Multiplicative ℤ))
          residualAssoc))

/-- A ONE-STEP true group isomorphism, using the actual m+k
receiver, split by the canonical finite tuple equivalence and the
strict associativity map on multiplicative direct products. -/
def nativeC60EKOneStage (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      (Fin m → Multiplicative ℤ) ×
        ((Fin k → Multiplicative ℤ) ×
          (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker) :=
  ((nativeC60EJCumulativeDirectProduct S F word r n (m + k)).trans
    (MulEquiv.prodCongr
      (nativeC60EKFiniteCoordinateSplit m k)
      (MulEquiv.refl
        ((nativeC60EBAbelianReceiver S F word (n + (m + k))).ker)))).trans
          (MulEquiv.prodAssoc :
            ((Fin m → Multiplicative ℤ) × (Fin k → Multiplicative ℤ)) ×
              (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker ≃*
            (Fin m → Multiplicative ℤ) ×
              ((Fin k → Multiplicative ℤ) ×
                (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker))

/-- The actual change of coordinates from the single deletion to
the sequential deletion; it is a bona fide GROUP ISOMORPHISM,
not a set-theoretic or merely existential comparison. -/
def nativeC60EKCoherenceComparison (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ) :
    ((Fin m → Multiplicative ℤ) ×
      ((Fin k → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker)) ≃*
    ((Fin m → Multiplicative ℤ) ×
      ((Fin k → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker)) :=
  (nativeC60EKOneStage S F word r n m k).symm.trans
    (nativeC60EKTwoStage S F word r n m k)

/-- The finite AQ coherence diagram STRICTLY COMMUTES as an
equality of genuine group isomorphisms, not only of carrier sets.
No assumption of strict equality of the two residual constructions
is hidden: the actual canonical comparison appears explicitly. -/
theorem nativeC60EKCoherence_triangle (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ) :
    (nativeC60EKOneStage S F word r n m k).trans
      (nativeC60EKCoherenceComparison S F word r n m k) =
        nativeC60EKTwoStage S F word r n m k := by
  apply MulEquiv.ext
  intro x
  change (nativeC60EKCoherenceComparison S F word r n m k)
      (nativeC60EKOneStage S F word r n m k x) =
        nativeC60EKTwoStage S F word r n m k x
  change (nativeC60EKTwoStage S F word r n m k)
      ((nativeC60EKOneStage S F word r n m k).symm
        (nativeC60EKOneStage S F word r n m k x)) =
          nativeC60EKTwoStage S F word r n m k x
  rw [MulEquiv.symm_apply_apply]

/-- The same actual abelianized AQ character at one integer
index agrees across arbitrary finite receiver lengths. This is
a direct consequence of ED/EE's genuine coordinate identity. -/
theorem nativeC60EKReceiver_sameCoordinate (word : List Bool)
    (x : Abelianization ((nativeC60DZImageToFull S F word).ker))
    (p q : ℕ) (i : Fin p) (j : Fin q)
    (h : i.val = j.val) :
    ((nativeC60EBAbelianReceiver S F word p) x) i =
      ((nativeC60EBAbelianReceiver S F word q) x) j := by
  have hfirst :=
    nativeC60EEReceiver_coordinate S F word p (Additive.ofMul x) i
  have hsecond :=
    nativeC60EEReceiver_coordinate S F word q (Additive.ofMul x) j
  rw [h] at hfirst
  exact hfirst.trans hsecond.symm

/-- The first block of an m+k receiver is exactly the actual
EH first-m receiver, for every original class x in C_n. -/
theorem nativeC60EKReceiver_head (word : List Bool)
    (n m k : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker)
    (i : Fin m) :
    (nativeC60EHTailReceiver S F word n m x) i =
      (nativeC60EHTailReceiver S F word n (m + k) x)
        (Fin.castAdd k i) := by
  change ((nativeC60EBAbelianReceiver S F word (n + m)) x.1)
      (⟨n + i.val, by omega⟩ : Fin (n + m)) =
    ((nativeC60EBAbelianReceiver S F word (n + (m + k))) x.1)
      (⟨n + i.val, by omega⟩ : Fin (n + (m + k)))
  exact nativeC60EKReceiver_sameCoordinate S F word x.1 (n + m)
    (n + (m + k)) _ _ rfl

/-- The first integer block agrees literally between both
finite deletion procedures, not just through an abstract
conjugating isomorphism. -/
theorem nativeC60EKCoherence_head (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker)
    (i : Fin m) :
    ((nativeC60EKTwoStage S F word r n m k x).1) i =
      ((nativeC60EKOneStage S F word r n m k x).1) i := by
  change ((nativeC60EJCumulativeDirectProduct S F word r n m x).1) i =
    ((nativeC60EJCumulativeDirectProduct S F word r n (m + k) x).1)
      (Fin.castAdd k i)
  rw [nativeC60EJCumulativeDirectProduct_fst,
    nativeC60EJCumulativeDirectProduct_fst]
  exact nativeC60EKReceiver_head S F word n m k x i

/-- The group isomorphism comparing the two constructions
preserves the ACTUAL first m coordinate values. -/
theorem nativeC60EKComparison_head (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (p : (Fin m → Multiplicative ℤ) ×
      ((Fin k → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F word (n + (m + k))).ker))
    (i : Fin m) :
    ((nativeC60EKCoherenceComparison S F word r n m k p).1) i =
      p.1 i := by
  change ((nativeC60EKTwoStage S F word r n m k)
    ((nativeC60EKOneStage S F word r n m k).symm p)).1 i = p.1 i
  rw [nativeC60EKCoherence_head S F word r n m k
    ((nativeC60EKOneStage S F word r n m k).symm p) i]
  rw [MulEquiv.apply_symm_apply]

/-- A zero-extended finite integer vector has no coefficient
beyond its original m coordinates. This is a genuine FINITE
support statement at arbitrary m,k, not a full infinite product. -/
theorem nativeC60EKFiniteExtension_future_zero (m k : ℕ)
    (v : Fin m → ℤ) (j : Fin k) :
    nativeC60EEFiniteExtension m v (m + j.val) = 0 := by
  change (Finsupp.mapDomain (fun i : Fin m => i.val)
    ((Finsupp.linearEquivFunOnFinite ℤ ℤ (Fin m)).symm v))
      (m + j.val) = 0
  apply Finsupp.mapDomain_notin_range
  rintro ⟨i, hi⟩
  change i.val = m + j.val at hi
  have him : i.val < m := i.isLt
  omega

/-- EI's section for the first m coordinates is TRULY invisible
to every following k-th coordinate. This uses the actual ED
abelianized C60 AQ character and the finite-support map. -/
theorem nativeC60EKSection_future_one (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ) (v : Fin m → Multiplicative ℤ) (j : Fin k) :
    ((nativeC60EHTailReceiver S F word n (m + k))
      (nativeC60EITailFiniteSection S F word r n m v))
      (Fin.natAdd m j) = 1 := by
  change ((nativeC60EBAbelianReceiver S F word (n + (m + k)))
      ((nativeC60EDFiniteSupportEmbedding S F word r
        (nativeC60EGTailShift n
          (nativeC60EEFiniteExtension m (fun i => (v i).toAdd)))).toMul))
      (⟨n + (m + j.val), by omega⟩ : Fin (n + (m + k))) = 1
  rw [nativeC60EEReceiver_coordinate S F word (n + (m + k))
    (nativeC60EDFiniteSupportEmbedding S F word r
      (nativeC60EGTailShift n
        (nativeC60EEFiniteExtension m (fun i => (v i).toAdd))))
    (⟨n + (m + j.val), by omega⟩ : Fin (n + (m + k)))]
  rw [nativeC60EDCoordinate_finiteSupport S F word r
    (nativeC60EGTailShift n
      (nativeC60EEFiniteExtension m (fun i => (v i).toAdd)))
    (n + (m + j.val))]
  rw [nativeC60EHTailShift_apply n
    (nativeC60EEFiniteExtension m (fun i => (v i).toAdd))
    (m + j.val)]
  rw [nativeC60EKFiniteExtension_future_zero m k
    (fun i => (v i).toAdd) j]
  rfl

end FiniteRankC60Coherence

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

/-- The physically chosen C60 AU source carries both honest
finite AQ split isomorphisms and their canonical group
isomorphism comparison for any actual context tree. -/
def nativeK5EKPhysicalAQ_splitComparison
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (n m k : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    ((Fin m → Multiplicative ℤ) ×
      ((Fin k → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F
          (nativeK5DOTreeWord tree) (n + (m + k))).ker)) ≃*
    ((Fin m → Multiplicative ℤ) ×
      ((Fin k → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F
          (nativeK5DOTreeWord tree) (n + (m + k))).ker)) :=
  nativeC60EKCoherenceComparison
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) n m k

end PhysicalC60AU

#print axioms nativeC60EKFiniteCoordinateSplit
#print axioms nativeC60EKTwoStage
#print axioms nativeC60EKOneStage
#print axioms nativeC60EKCoherenceComparison
#print axioms nativeC60EKCoherence_triangle
#print axioms nativeC60EKReceiver_sameCoordinate
#print axioms nativeC60EKReceiver_head
#print axioms nativeC60EKCoherence_head
#print axioms nativeC60EKComparison_head
#print axioms nativeC60EKFiniteExtension_future_zero
#print axioms nativeC60EKSection_future_one
#print axioms nativeK5EKPhysicalAQ_splitComparison

end
end Kuu.F112.Physical
