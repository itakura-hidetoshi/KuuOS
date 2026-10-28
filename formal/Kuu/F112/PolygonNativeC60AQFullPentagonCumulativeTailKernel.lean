import Kuu.F112.PolygonNativeC60AQFullPentagonTailComplementDirectProduct
import Mathlib.Algebra.Group.Prod

/-!
# F112-P94D3EJ — cumulative removal of finite AQ integer coordinates

EI gave a genuine split finite-rank group isomorphism
  C_n ≃* Z^m × ker(tau_(n,m)),
where C_n is the honest kernel of the first n characters on the
ABELIANIZATION of the original noncommutative C60 AQ obstruction
kernel. EJ proves that the residual kernel is precisely, up to an
explicit group isomorphism, C_(n+m), the kernel of the first n+m
original characters. This is a cumulative algebraic comparison,
not a geometric 19D filler or a new identification of proof histories.

The proof splits a Fin (n+m) coordinate into i < n and i >= n:
the former vanishes by membership in C_n, the latter by the true
EH tail receiver. Conversely C_(n+m) implies both membership in
C_n and vanishing of the tail receiver, by the ED/EE exact character
formula and the actual 18D AQ Kronecker evaluations. No new
axiom or unsupported quotient equality is introduced.

EJ composes the verified EF/EI group isomorphism with this true
residual kernel isomorphism, obtaining for EVERY finite n,m:
  C_n ≃* (Fin m → Multiplicative ℤ) × C_(n+m).
The residual kernel ker(tau_(n,m)) is non-finitely generated via
EH and the actual isomorphism. No full infinite product
surjectivity, infinite-rank splitting, or freedom/commutativity
of the original kernel is inferred. Preserve strict Kuu and the
independent-Kuu presentation, DS complete-evidence no-go,
original 14D--18D Type-valued evidence, C60 gauge experiment,
107 public roots, pinned Lean/mathlib, same-root/append-only,
and no Gray category. No sorry or admit.
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

section CumulativeAQKernel

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The first n character coordinates agree pointwise with
their restriction from n+m coordinates on the ACTUAL abelianization.
This follows from EE's universal character evaluation, rather than
assuming that two quotient homomorphisms are definitionally equal. -/
theorem nativeC60EJReceiver_firstCoordinate
    (word : List Bool) (n rank : ℕ)
    (x : Abelianization ((nativeC60DZImageToFull S F word).ker))
    (i : Fin n) :
    ((nativeC60EBAbelianReceiver S F word n) x) i =
      ((nativeC60EBAbelianReceiver S F word (n + rank)) x)
        ⟨i.val, by omega⟩ := by
  have hfirst :=
    nativeC60EEReceiver_coordinate S F word n (Additive.ofMul x) i
  have hlarge :=
    nativeC60EEReceiver_coordinate S F word (n + rank) (Additive.ofMul x)
      (⟨i.val, by omega⟩ : Fin (n + rank))
  exact hfirst.trans hlarge.symm

/-- If every first n+m charge vanishes, so do the first n charges. -/
theorem nativeC60EJFirstZero_of_fullZero
    (word : List Bool) (n rank : ℕ)
    (x : Abelianization ((nativeC60DZImageToFull S F word).ker))
    (hx : (nativeC60EBAbelianReceiver S F word (n + rank)) x = 1) :
    (nativeC60EBAbelianReceiver S F word n) x = 1 := by
  funext i
  change ((nativeC60EBAbelianReceiver S F word n) x) i = 1
  rw [nativeC60EJReceiver_firstCoordinate S F word n rank x i]
  have h := congrFun hx (⟨i.val, by omega⟩ : Fin (n + rank))
  simpa only [Pi.one_apply] using h

/-- All n+m charges vanishing also kills the tail receiver when
the same class is viewed in the first-n kernel. -/
theorem nativeC60EJTailZero_of_fullZero
    (word : List Bool) (n rank : ℕ)
    (x : Abelianization ((nativeC60DZImageToFull S F word).ker))
    (hx : (nativeC60EBAbelianReceiver S F word (n + rank)) x = 1) :
    (nativeC60EHTailReceiver S F word n rank
      (⟨x, MonoidHom.mem_ker.mpr
        (nativeC60EJFirstZero_of_fullZero S F word n rank x hx)⟩ :
          (nativeC60EBAbelianReceiver S F word n).ker)) = 1 := by
  funext i
  change ((nativeC60EBAbelianReceiver S F word (n + rank)) x)
    ⟨n + i.val, by omega⟩ = 1
  have h := congrFun hx (⟨n + i.val, by omega⟩ : Fin (n + rank))
  simpa only [Pi.one_apply] using h

/-- Conversely, a class in the actual first-n kernel with vanishing
next rank integer receiver has every one of its n+rank characters
equal to zero. The proof explicitly handles both finite intervals. -/
theorem nativeC60EJFullZero_of_firstAndTail
    (word : List Bool) (n rank : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker)
    (hx : (nativeC60EHTailReceiver S F word n rank) x = 1) :
    (nativeC60EBAbelianReceiver S F word (n + rank)) x.1 = 1 := by
  funext k
  change ((nativeC60EBAbelianReceiver S F word (n + rank)) x.1) k = 1
  by_cases hk : k.val < n
  · let i : Fin n := ⟨k.val, hk⟩
    have hfirst : ((nativeC60EBAbelianReceiver S F word n) x.1) i = 1 := by
      have h := congrFun (MonoidHom.mem_ker.mp x.2) i
      simpa only [Pi.one_apply] using h
    have hstable := nativeC60EJReceiver_firstCoordinate S F word n rank x.1 i
    have htarget :
        ((nativeC60EBAbelianReceiver S F word (n + rank)) x.1)
          (⟨i.val, by omega⟩ : Fin (n + rank)) = 1 :=
      hstable.symm.trans hfirst
    have hindex : (⟨i.val, by omega⟩ : Fin (n + rank)) = k := Fin.ext rfl
    rw [hindex] at htarget
    exact htarget
  · have hge : n ≤ k.val := Nat.le_of_not_lt hk
    let i : Fin rank := ⟨k.val - n, by omega⟩
    have htail :
        ((nativeC60EBAbelianReceiver S F word (n + rank)) x.1)
          (⟨n + i.val, by omega⟩ : Fin (n + rank)) = 1 := by
      have h := congrFun hx i
      change ((nativeC60EBAbelianReceiver S F word (n + rank)) x.1)
        (⟨n + i.val, by omega⟩ : Fin (n + rank)) = 1 at h
      exact h
    have hindex : (⟨n + i.val, by omega⟩ : Fin (n + rank)) = k := by
      apply Fin.ext
      dsimp [i]
      omega
    rw [hindex] at htail
    exact htail

/-- MAIN EJ KERNEL COMPARISON: the genuine double kernel of
the next tail receiver and the original cumulative n+rank kernel
are isomorphic as GROUPS. No quotient replacement is postulated:
both sides have literally the same underlying abelianization element,
with their respective honest membership proofs. -/
def nativeC60EJResidualKernelEquiv (word : List Bool)
    (n rank : ℕ) :
    (nativeC60EHTailReceiver S F word n rank).ker ≃*
      (nativeC60EBAbelianReceiver S F word (n + rank)).ker where
  toFun x :=
    ⟨x.1.1, MonoidHom.mem_ker.mpr
      (nativeC60EJFullZero_of_firstAndTail S F word n rank
        x.1 (MonoidHom.mem_ker.mp x.2))⟩
  invFun y :=
    ⟨⟨y.1, MonoidHom.mem_ker.mpr
       (nativeC60EJFirstZero_of_fullZero S F word n rank
         y.1 (MonoidHom.mem_ker.mp y.2))⟩,
      MonoidHom.mem_ker.mpr
        (nativeC60EJTailZero_of_fullZero S F word n rank
          y.1 (MonoidHom.mem_ker.mp y.2))⟩
  left_inv x := by
    apply Subtype.ext
    apply Subtype.ext
    rfl
  right_inv y := by
    apply Subtype.ext
    rfl
  map_mul' x y := by
    apply Subtype.ext
    rfl

/-- Cumulative finite deletion: EI's genuine finite split and
EJ's actual residual comparison jointly give the explicit
finite-rank integer factor and the FULL n+rank complement. -/
def nativeC60EJCumulativeDirectProduct (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker ≃*
      (Fin rank → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F word (n + rank)).ker :=
  (nativeC60EITailDirectProduct S F word r n rank).trans
    (MulEquiv.prodCongr
      (MulEquiv.refl (Fin rank → Multiplicative ℤ))
      (nativeC60EJResidualKernelEquiv S F word n rank))

/-- The first coordinate of the true cumulative decomposition
is precisely EH's observation of the next rank integer charges. -/
theorem nativeC60EJCumulativeDirectProduct_fst (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ)
    (x : (nativeC60EBAbelianReceiver S F word n).ker) :
    (nativeC60EJCumulativeDirectProduct S F word r n rank x).1 =
      nativeC60EHTailReceiver S F word n rank x := by
  rfl

/-- The doubly observed residual kernel cannot become finitely
generated: EJ identifies it with C_(n+rank), to which EH applies.
This is nonfinite generation of the actual double subgroup kernel,
not an assumption that the original noncommutative kernel is free. -/
theorem nativeC60EJResidualKernel_not_fg (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ) :
    ¬ Group.FG ((nativeC60EHTailReceiver S F word n rank).ker) := by
  intro hfg
  letI : Group.FG ((nativeC60EHTailReceiver S F word n rank).ker) := hfg
  have hsurj : Function.Surjective
      (nativeC60EJResidualKernelEquiv S F word n rank).toMonoidHom :=
    (nativeC60EJResidualKernelEquiv S F word n rank).surjective
  have hfgFull : Group.FG
      ((nativeC60EBAbelianReceiver S F word (n + rank)).ker) :=
    Group.fg_of_surjective hsurj
  exact (nativeC60EHTailComplement_not_fg S F word r (n + rank)) hfgFull

end CumulativeAQKernel

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

/-- A true physically typed C60 AU context has cumulative finite
AQ direct-product decompositions for every finite n and rank. -/
def nativeK5EJPhysicalAQ_cumulativeDirectProduct
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (n rank : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    (nativeC60EBAbelianReceiver S F
      (nativeK5DOTreeWord tree) n).ker ≃*
      (Fin rank → Multiplicative ℤ) ×
        (nativeC60EBAbelianReceiver S F
          (nativeK5DOTreeWord tree) (n + rank)).ker :=
  nativeC60EJCumulativeDirectProduct
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) n rank

/-- The fully typed physical C60 AU residual, after deleting first
n and then rank many independent charges, is still not FG. -/
theorem nativeK5EJPhysicalAQ_residualKernel_not_fg
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (n rank : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    ¬ Group.FG
      ((nativeC60EHTailReceiver S F
        (nativeK5DOTreeWord tree) n rank).ker) := by
  dsimp only
  exact nativeC60EJResidualKernel_not_fg
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) n rank

end PhysicalC60AU

#print axioms nativeC60EJReceiver_firstCoordinate
#print axioms nativeC60EJFirstZero_of_fullZero
#print axioms nativeC60EJTailZero_of_fullZero
#print axioms nativeC60EJFullZero_of_firstAndTail
#print axioms nativeC60EJResidualKernelEquiv
#print axioms nativeC60EJCumulativeDirectProduct
#print axioms nativeC60EJCumulativeDirectProduct_fst
#print axioms nativeC60EJResidualKernel_not_fg
#print axioms nativeK5EJPhysicalAQ_cumulativeDirectProduct
#print axioms nativeK5EJPhysicalAQ_residualKernel_not_fg

end
end Kuu.F112.Physical
