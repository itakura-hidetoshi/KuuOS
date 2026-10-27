import Kuu.F112.PolygonNativeC60StrictIsotropyRetract
import Mathlib.GroupTheory.SemidirectProduct
import Mathlib.GroupTheory.GroupAction.ConjAct
import Mathlib.Tactic.Group

/-!
# F112-P94D3CP — the actual strict isotropy semidirect-product theorem

CO gives a split group homomorphism from the existing proof-bearing strict
isotropy onto the noncommutative CN free fork family. CP identifies the
ENTIRE strict isotropy with the semidirect product of the genuine kernel
of that retraction and the same original free fork group.

The free group acts on the kernel by actual conjugation by the CO lift.
Every strict loop z has the UNIQUE normal form

    z = (z * embed(retract z)⁻¹) * embed(retract z).

The first factor belongs to the kernel; the second retains CN's
original dependent 15D chain and full finite AQ context. The action is
not assumed trivial, and no product commutativity is asserted.

The generic split-group algebra below is proved from an explicit left
inverse, then specialized to the original C60 strict automorphism group.
Neither new relations nor geometric 16-cell coherence are introduced.
No Gray, new axioms, sorry/admit, or additional public roots.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uCP vCP u uD vD uE vE

section SplitGroup

variable {G : Type uCP} {H : Type vCP} [Group G] [Group H]

/-- Actual conjugation action on the normal kernel of a group retraction.
The action is not the trivial one, nor an action on mere code observations. -/
def nativeC60CPGenericAction (r : G →* H) (i : H →* G) :
    H →* MulAut r.ker :=
  (MulAut.conjNormal : G →* MulAut r.ker).comp i

/-- The orientation of the genuine semidirect action is left conjugation. -/
theorem nativeC60CPGenericAction_coe (r : G →* H) (i : H →* G)
    (h : H) (k : r.ker) :
    ((nativeC60CPGenericAction r i h) k : G) =
      i h * (k : G) * (i h)⁻¹ :=
  MulAut.conjNormal_apply (i h) k

/-- Homomorphism from the canonical semidirect product to the original group.
It multiplies the true kernel element with the embedded free-group factor. -/
def nativeC60CPGenericForward (r : G →* H) (i : H →* G) :
    r.ker ⋊[nativeC60CPGenericAction r i] H →* G :=
  SemidirectProduct.lift r.ker.subtype i (by
    intro h
    apply MonoidHom.ext
    intro k
    change ((nativeC60CPGenericAction r i h) k : G) =
      i h * (k : G) * (i h)⁻¹
    exact nativeC60CPGenericAction_coe r i h k)

theorem nativeC60CPGenericForward_apply (r : G →* H) (i : H →* G)
    (z : r.ker ⋊[nativeC60CPGenericAction r i] H) :
    nativeC60CPGenericForward r i z = (z.left : G) * i z.right :=
  rfl

/-- The normal-form kernel factor is a genuine element of the kernel;
this uses the existing split equality, not a new quotient. -/
def nativeC60CPGenericKernelPart (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h) (z : G) : r.ker :=
  ⟨z * (i (r z))⁻¹, by
    change r (z * (i (r z))⁻¹) = 1
    rw [map_mul, map_inv, split, mul_inv_cancel]⟩

/-- Canonical factorization of EVERY element of the original group. -/
theorem nativeC60CPGenericFactor (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h) (z : G) :
    (nativeC60CPGenericKernelPart r i split z : G) * i (r z) = z := by
  change (z * (i (r z))⁻¹) * i (r z) = z
  group

/-- The kernel component is recovered exactly, with no cancellation by a
commutative quotient and no loss of the original subgroup witness. -/
theorem nativeC60CPGenericKernelPart_recovery (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h) (k : r.ker) (h : H) :
    nativeC60CPGenericKernelPart r i split ((k : G) * i h) = k := by
  apply Subtype.ext
  change (((k : G) * i h) *
    (i (r ((k : G) * i h)))⁻¹) = (k : G)
  have hk : r (k : G) = 1 := by
    exact (MonoidHom.mem_ker).mp k.property
  rw [map_mul, hk, one_mul, split]
  group

/-- The quotient coordinate is recovered exactly from the actual kernel. -/
theorem nativeC60CPGenericFreePart_recovery (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h) (k : r.ker) (h : H) :
    r ((k : G) * i h) = h := by
  have hk : r (k : G) = 1 := (MonoidHom.mem_ker).mp k.property
  rw [map_mul, hk, split, one_mul]

/-- A concrete multiplicative equivalence, not merely an equality of
cardinalities or a pair of set-theoretic inverse functions. -/
def nativeC60CPGenericMulEquiv (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h) :
    r.ker ⋊[nativeC60CPGenericAction r i] H ≃* G where
  toFun := nativeC60CPGenericForward r i
  invFun z := ⟨nativeC60CPGenericKernelPart r i split z, r z⟩
  left_inv z := by
    apply SemidirectProduct.ext
    · change nativeC60CPGenericKernelPart r i split
        ((z.left : G) * i z.right) = z.left
      exact nativeC60CPGenericKernelPart_recovery r i split z.left z.right
    · change r ((z.left : G) * i z.right) = z.right
      exact nativeC60CPGenericFreePart_recovery r i split z.left z.right
  right_inv z := by
    change (nativeC60CPGenericKernelPart r i split z : G) *
      i (r z) = z
    exact nativeC60CPGenericFactor r i split z
  map_mul' x y := (nativeC60CPGenericForward r i).map_mul x y

/-- The retraction is precisely the semidirect second-coordinate
projection, not just a split epimorphism with unspecified factor. -/
theorem nativeC60CPGenericRight_projection (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h)
    (z : r.ker ⋊[nativeC60CPGenericAction r i] H) :
    r (nativeC60CPGenericMulEquiv r i split z) = z.right := by
  change r ((z.left : G) * i z.right) = z.right
  exact nativeC60CPGenericFreePart_recovery r i split z.left z.right

/-- No nonidentity element of the embedded free factor is in the kernel.
Thus the semidirect decomposition does not collapse its CN provenance. -/
theorem nativeC60CPGenericSplit_disjoint (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h)
    (h : H) (hker : i h ∈ r.ker) : h = 1 := by
  have hh : r (i h) = 1 := (MonoidHom.mem_ker).mp hker
  rw [split] at hh
  exact hh

end SplitGroup

section AbstractC60

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The actual normal kernel in the strict automorphism group, after a
genuine finite AQ context, with a fixed original BC certificate. -/
abbrev NativeC60CPKernel (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    Subgroup (NativeC60COIsotropy S F word a) :=
  (nativeC60CORetraction S F word base).ker

/-- The free fork family acts by genuine conjugation in strict isotropy,
not by a presumed trivial/abelian action. -/
def nativeC60CPAction (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    FreeGroup (NativeC60CNForkAlphabet S F base) →*
      MulAut (NativeC60CPKernel S F word base) :=
  nativeC60CPGenericAction (nativeC60CORetraction S F word base)
    (nativeC60COEmbed S F word base)

/-- A completely explicit isomorphism of the full strict isotropy group
with the semidirect product of its true kernel and CN's free fork group. -/
def nativeC60CPSemidirectEquiv (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    (NativeC60CPKernel S F word base ⋊[nativeC60CPAction S F word base]
      FreeGroup (NativeC60CNForkAlphabet S F base)) ≃*
      NativeC60COIsotropy S F word a :=
  nativeC60CPGenericMulEquiv
    (nativeC60CORetraction S F word base)
    (nativeC60COEmbed S F word base)
    (nativeC60CORetraction_embed S F word base)

/-- The second semidirect coordinate is exactly CO's proven decoder. -/
theorem nativeC60CPSemidirect_retraction (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (z : NativeC60CPKernel S F word base ⋊[nativeC60CPAction S F word base]
      FreeGroup (NativeC60CNForkAlphabet S F base)) :
    nativeC60CORetraction S F word base
        (nativeC60CPSemidirectEquiv S F word base z) = z.right :=
  nativeC60CPGenericRight_projection
    (nativeC60CORetraction S F word base)
    (nativeC60COEmbed S F word base)
    (nativeC60CORetraction_embed S F word base) z

/-- Every strict isotropy loop is a unique kernel element multiplied by
an original CN free loop, and the witness is explicitly computable via r. -/
theorem nativeC60CPSemidirect_normal_form (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (z : NativeC60COIsotropy S F word a) :
    (nativeC60CPGenericKernelPart
        (nativeC60CORetraction S F word base)
        (nativeC60COEmbed S F word base)
        (nativeC60CORetraction_embed S F word base) z :
      NativeC60COIsotropy S F word a) *
      nativeC60COEmbed S F word base (nativeC60CORetraction S F word base z) = z :=
  nativeC60CPGenericFactor
    (nativeC60CORetraction S F word base)
    (nativeC60COEmbed S F word base)
    (nativeC60CORetraction_embed S F word base) z

/-- Any free factor lying in the actual kernel is necessarily identity. -/
theorem nativeC60CPFree_factor_disjoint_kernel (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (x : FreeGroup (NativeC60CNForkAlphabet S F base))
    (hx : nativeC60COEmbed S F word base x ∈
        NativeC60CPKernel S F word base) : x = 1 :=
  nativeC60CPGenericSplit_disjoint
    (nativeC60CORetraction S F word base)
    (nativeC60COEmbed S F word base)
    (nativeC60CORetraction_embed S F word base) x hx

/-- The precise noncommutative kernel action retains the original
traversal order in (Aut X)ᵐᵒᵖ. -/
theorem nativeC60CPAction_coe (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (x : FreeGroup (NativeC60CNForkAlphabet S F base))
    (k : NativeC60CPKernel S F word base) :
    ((nativeC60CPAction S F word base x) k :
      NativeC60COIsotropy S F word a) =
        nativeC60COEmbed S F word base x * (k : NativeC60COIsotropy S F word a) *
          (nativeC60COEmbed S F word base x)⁻¹ :=
  nativeC60CPGenericAction_coe
    (nativeC60CORetraction S F word base)
    (nativeC60COEmbed S F word base) x k

end AbstractC60

section PhysicalC60

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

/-- The actual physical C60 conservative atom, with independent inner and
outer finite AQ contexts, now admits the genuine kernel semidirect split. -/
def nativeK5CPPhysicalSemidirect
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    (NativeC60CPKernel (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CKAtomGenerator W R inner) ⋊[
      nativeC60CPAction (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CKAtomGenerator W R inner)]
        FreeGroup (NativeC60CNForkAlphabet
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          (nativeK5CKAtomGenerator W R inner))) ≃*
      NativeC60COIsotropy (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CHSource W inner (nativeK5CKConservativeAtom W R)) :=
  nativeC60CPSemidirectEquiv
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    outer (nativeK5CKAtomGenerator W R inner)

end PhysicalC60

#print axioms nativeC60CPGenericAction
#print axioms nativeC60CPGenericAction_coe
#print axioms nativeC60CPGenericForward
#print axioms nativeC60CPGenericKernelPart
#print axioms nativeC60CPGenericFactor
#print axioms nativeC60CPGenericKernelPart_recovery
#print axioms nativeC60CPGenericFreePart_recovery
#print axioms nativeC60CPGenericMulEquiv
#print axioms nativeC60CPGenericRight_projection
#print axioms nativeC60CPGenericSplit_disjoint
#print axioms nativeC60CPSemidirectEquiv
#print axioms nativeC60CPSemidirect_retraction
#print axioms nativeC60CPSemidirect_normal_form
#print axioms nativeC60CPFree_factor_disjoint_kernel
#print axioms nativeC60CPAction_coe
#print axioms nativeK5CPPhysicalSemidirect

end
end Kuu.F112.Physical
