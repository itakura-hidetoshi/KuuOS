import Kuu.F112.PolygonNativeC60InnerPrefixFullCNParityNaturality
import Mathlib.GroupTheory.QuotientGroup.Basic

/-!
# F112-P94D3DJ — true strict DC parity quotient transport

DI establishes full naturality of the ORIGINAL DC FreeGroup Bool quotient
under DF's genuine inner AQ strict-group isomorphism, on EVERY original
noncommutative CN generator (including all non-CZ certificates).

DJ takes the categorical and group-theoretic consequence WITHOUT selecting
new 16-cell relations. First it proves, generically, that an isomorphism
commuting with two group-valued quotient maps preserves every genuine kernel
element and every exact quotient fiber. Crucially it carries the ENTIRE
source kernel ONTO the target kernel, not just into it. This makes
QuotientGroup.congr applicable to the two actual normal kernel subgroups.

Then the induced multiplication-preserving equivalence of genuine strict
group quotients is constructed, and its value on every original strict
automorphism is computed. The two surjective DC quotient maps identify
these physical quotients with the SAME noncommutative FreeGroup Bool;
the square with their Noether quotient equivalences commutes exactly.
No assumption of the desired kernel equality or quotient naturality
is introduced into the physical proofs.

Both original dependent 14D and 15D boundaries, the full 16D provenance
and finite C60 AQ inner/outer history are kept through the DI/DF witness
rather than replaced by a graph or by an observer-only category.

The claims concern the chosen no-extra-relations strict Kuu presentation,
not a geometric 16-cell filling. Strict Kuu is retained; independent Kuu
remains another presentation. No Gray and no new axiom/sorry/admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDJ vDJ wDJ uD vD uE vE

section ExactKernelAndQuotientTransport

variable {G : Type uDJ} {H : Type vDJ} {Q : Type wDJ}
variable [Group G] [Group H] [Group Q]

/-- A true strict group isomorphism commuting with the *two original*
quotient homomorphisms reflects as well as preserves membership in the
original kernel. The target kernel is not assumed equal in advance. -/
theorem nativeC60DJKernel_iff
    (q : G →* Q) (r : H →* Q) (e : G ≃* H)
    (h : r.comp e.toMonoidHom = q) (x : G) :
    x ∈ q.ker ↔ e x ∈ r.ker := by
  change q x = 1 ↔ r (e x) = 1
  have hx := DFunLike.congr_fun h x
  change r (e x) = q x at hx
  rw [hx]

/-- In addition the map preserves all exact coarse fibers, not just
whether an individual loop becomes the unit of the chosen quotient. -/
theorem nativeC60DJFiber_iff
    (q : G →* Q) (r : H →* Q) (e : G ≃* H)
    (h : r.comp e.toMonoidHom = q) (x y : G) :
    q x = q y ↔ r (e x) = r (e y) := by
  have hx := DFunLike.congr_fun h x
  have hy := DFunLike.congr_fun h y
  change r (e x) = q x at hx
  change r (e y) = q y at hy
  rw [hx, hy]

/-- Exact kernel IMAGE, as a subgroup equality in the actual target.
The reverse inclusion explicitly uses the inverse of the true strict
group equivalence; a mere forward kernel inclusion would not suffice. -/
theorem nativeC60DJKernel_map
    (q : G →* Q) (r : H →* Q) (e : G ≃* H)
    (h : r.comp e.toMonoidHom = q) :
    Subgroup.map e.toMonoidHom q.ker = r.ker := by
  apply Subgroup.ext
  intro y
  constructor
  · intro hy
    obtain ⟨x, hx, hxy⟩ := (Subgroup.mem_map).mp hy
    rw [← hxy]
    exact (nativeC60DJKernel_iff q r e h x).mp hx
  · intro hy
    apply (Subgroup.mem_map).mpr
    refine ⟨e.symm y, ?_, ?_⟩
    · apply (nativeC60DJKernel_iff q r e h (e.symm y)).mpr
      simpa using hy
    · simp

/-- Actual strict quotient-group equivalence by the ORIGINAL kernels.
This is not an extra quotient of the underlying Type-valued 16D
certificates: only the already selected DC parity group observable
induces the two normal subgroups. -/
def nativeC60DJQuotientTransport
    (q : G →* Q) (r : H →* Q) (e : G ≃* H)
    (h : r.comp e.toMonoidHom = q) :
    (G ⧸ q.ker) ≃* (H ⧸ r.ker) :=
  QuotientGroup.congr q.ker r.ker e
    (nativeC60DJKernel_map q r e h)

/-- Exact representative formula, including every original strict
automorphism, not just the selected CZ n-generated subfamily. -/
theorem nativeC60DJQuotientTransport_mk
    (q : G →* Q) (r : H →* Q) (e : G ≃* H)
    (h : r.comp e.toMonoidHom = q) (x : G) :
    nativeC60DJQuotientTransport q r e h
        ((QuotientGroup.mk' q.ker) x) =
      (QuotientGroup.mk' r.ker) (e x) :=
  QuotientGroup.congr_mk' q.ker r.ker e
    (nativeC60DJKernel_map q r e h) x

/-- The two genuine surjective quotient maps have exactly the same
gauge class value once their normal-kernel quotients are transported.
This uses the first isomorphism theorem on the actual kernel quotient. -/
theorem nativeC60DJQuotientParity_mk
    (q : G →* Q) (r : H →* Q) (e : G ≃* H)
    (h : r.comp e.toMonoidHom = q)
    (hq : Function.Surjective q) (hr : Function.Surjective r)
    (x : G) :
    (QuotientGroup.quotientKerEquivOfSurjective hr)
        (nativeC60DJQuotientTransport q r e h
          ((QuotientGroup.mk' q.ker) x)) =
      (QuotientGroup.quotientKerEquivOfSurjective hq)
        ((QuotientGroup.mk' q.ker) x) := by
  rw [nativeC60DJQuotientTransport_mk]
  change (QuotientGroup.kerLift r)
      ((QuotientGroup.mk' r.ker) (e x)) =
    (QuotientGroup.kerLift q) ((QuotientGroup.mk' q.ker) x)
  rw [QuotientGroup.kerLift_mk, QuotientGroup.kerLift_mk]
  exact DFunLike.congr_fun h x

/-- Strong descent: the induced quotient equivalence becomes IDENTICAL
on the canonical common Q receiver, as an equality of true MulEquivs,
not an equality only of particular observed generator values. -/
theorem nativeC60DJQuotientParity_equiv
    (q : G →* Q) (r : H →* Q) (e : G ≃* H)
    (h : r.comp e.toMonoidHom = q)
    (hq : Function.Surjective q) (hr : Function.Surjective r) :
    (nativeC60DJQuotientTransport q r e h).trans
        (QuotientGroup.quotientKerEquivOfSurjective hr) =
      QuotientGroup.quotientKerEquivOfSurjective hq := by
  apply MulEquiv.ext
  intro x
  obtain ⟨z, rfl⟩ := QuotientGroup.mk'_surjective q.ker x
  exact nativeC60DJQuotientParity_mk q r e h hq hr z

end ExactKernelAndQuotientTransport

section GenuineC60StrictParity

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

/-- DI's exact whole-CN strict naturality implies a TWO-SIDED
kernel transport statement, with no kernel hypothesis on its RHS. -/
theorem nativeK5DJInnerPrefix_kernel_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    z ∈ (nativeK5DCParityQuotient W R inner outer).ker ↔
      nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z ∈
        (nativeK5DCParityQuotient W R (shift ++ inner) outer).ker :=
  nativeC60DJKernel_iff
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient W R (shift ++ inner) outer)
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift)
    (nativeK5DIInnerPrefix_full_parity W R inner outer shift) z

/-- All strict loops with the same original parity stay in the same
parity fiber after physical inner-prefix transport, AND conversely. -/
theorem nativeK5DJInnerPrefix_fiber_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool)
    (z z' : nativeK5DBIsotropy W R inner outer) :
    nativeK5DCParityQuotient W R inner outer z =
        nativeK5DCParityQuotient W R inner outer z' ↔
      nativeK5DCParityQuotient W R (shift ++ inner) outer
          (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z) =
        nativeK5DCParityQuotient W R (shift ++ inner) outer
          (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z') :=
  nativeC60DJFiber_iff
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient W R (shift ++ inner) outer)
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift)
    (nativeK5DIInnerPrefix_full_parity W R inner outer shift) z z'

/-- Strong kernel IMAGE equality of ACTUAL DF strict automorphisms,
not merely DG's original kernel inclusion. -/
theorem nativeK5DJInnerPrefix_kernel_map
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    Subgroup.map
        (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).toMonoidHom
        (nativeK5DCParityQuotient W R inner outer).ker =
      (nativeK5DCParityQuotient W R (shift ++ inner) outer).ker :=
  nativeC60DJKernel_map
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient W R (shift ++ inner) outer)
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift)
    (nativeK5DIInnerPrefix_full_parity W R inner outer shift)

/-- The original physical strict isotropy, quotient by its selected
DC kernel, transports as a TRUE group equivalence to the target
physical strict quotient under arbitrary finite inner AQ framing. -/
def nativeK5DJInnerPrefix_quotientEquiv
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    (nativeK5DBIsotropy W R inner outer ⧸
        (nativeK5DCParityQuotient W R inner outer).ker) ≃*
      (nativeK5DBIsotropy W R (shift ++ inner) outer ⧸
        (nativeK5DCParityQuotient W R (shift ++ inner) outer).ker) :=
  nativeC60DJQuotientTransport
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient W R (shift ++ inner) outer)
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift)
    (nativeK5DIInnerPrefix_full_parity W R inner outer shift)

/-- Every original STRICT group element has its exact image in the
target quotient; the formula does not discard original CN/BW witnesses. -/
theorem nativeK5DJInnerPrefix_quotientEquiv_mk
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DJInnerPrefix_quotientEquiv W R inner outer shift
        ((QuotientGroup.mk'
          (nativeK5DCParityQuotient W R inner outer).ker) z) =
      (QuotientGroup.mk'
        (nativeK5DCParityQuotient W R (shift ++ inner) outer).ker)
        (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z) :=
  nativeC60DJQuotientTransport_mk
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient W R (shift ++ inner) outer)
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift)
    (nativeK5DIInnerPrefix_full_parity W R inner outer shift) z

/-- True first-isomorphism equivalence of each original strict
quotient with the ORIGINAL noncommutative DC FreeGroup Bool. -/
def nativeK5DJParityQuotientEquiv
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    (nativeK5DBIsotropy W R inner outer ⧸
        (nativeK5DCParityQuotient W R inner outer).ker) ≃*
      FreeGroup Bool :=
  QuotientGroup.quotientKerEquivOfSurjective
    (nativeK5DCParityQuotient_surjective W R inner outer)

/-- Final genuine strict quotient descent: quotient transport followed
by the true target Noether isomorphism equals the original source
Noether isomorphism, as an equality of MUL EQUIVALENCES. -/
theorem nativeK5DJInnerPrefix_quotient_parity_naturality
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    (nativeK5DJInnerPrefix_quotientEquiv W R inner outer shift).trans
        (nativeK5DJParityQuotientEquiv W R (shift ++ inner) outer) =
      nativeK5DJParityQuotientEquiv W R inner outer :=
  nativeC60DJQuotientParity_equiv
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient W R (shift ++ inner) outer)
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift)
    (nativeK5DIInnerPrefix_full_parity W R inner outer shift)
    (nativeK5DCParityQuotient_surjective W R inner outer)
    (nativeK5DCParityQuotient_surjective W R (shift ++ inner) outer)

end GenuineC60StrictParity

#print axioms nativeC60DJKernel_iff
#print axioms nativeC60DJFiber_iff
#print axioms nativeC60DJKernel_map
#print axioms nativeC60DJQuotientTransport
#print axioms nativeC60DJQuotientTransport_mk
#print axioms nativeC60DJQuotientParity_mk
#print axioms nativeC60DJQuotientParity_equiv
#print axioms nativeK5DJInnerPrefix_kernel_iff
#print axioms nativeK5DJInnerPrefix_fiber_iff
#print axioms nativeK5DJInnerPrefix_kernel_map
#print axioms nativeK5DJInnerPrefix_quotientEquiv
#print axioms nativeK5DJInnerPrefix_quotientEquiv_mk
#print axioms nativeK5DJParityQuotientEquiv
#print axioms nativeK5DJInnerPrefix_quotient_parity_naturality

end
end Kuu.F112.Physical
