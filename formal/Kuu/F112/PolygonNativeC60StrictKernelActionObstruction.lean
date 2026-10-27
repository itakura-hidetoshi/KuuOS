import Kuu.F112.PolygonNativeC60StrictIsotropySemidirectProduct
import Mathlib.Tactic.Group

/-!
# F112-P94D3CQ — genuine strict-kernel and conjugation obstructions

CP gives the actual split strict isotropy G = K ⋊ F. CQ does not assume
K = 1 or that its F-conjugation action is trivial. Instead it proves exact
criteria for both assertions, and supplies a witness-transfer theorem
from ORIGINAL dependent signed 15D/16D paths.

A true kernel witness must have full nontrivial BW holonomy while the
different, CN-decoded free-fork coordinate is trivial. The two kernels
are never identified. A trivial action is equivalent to centralization
of each actual kernel element by every embedded fork generator. Only
under that hypothesis does the CP semidirect normal form become a
canonical DIRECT product of groups.

All statements concern the existing proof-bearing strict automorphisms.
Finite AQ context words and original endpoints remain unchanged.
No assertion of unconditional kernel nontriviality or actual higher
geometric coherence is made. No Gray, axioms, sorry/admit, or new roots.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uCQ vCQ u uD vD uE vE

section SplitGroup

variable {G : Type uCQ} {H : Type vCQ} [Group G] [Group H]

/-- A canonical, actual kernel factor is nonidentity exactly when the
original strict loop is outside the chosen split free-factor projector. -/
theorem nativeC60CQGenericKernelPart_ne_one_iff
    (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h) (z : G) :
    nativeC60CPGenericKernelPart r i split z ≠ 1 ↔ z ≠ i (r z) := by
  constructor
  · intro hk hz
    apply hk
    apply Subtype.ext
    change z * (i (r z))⁻¹ = 1
    rw [hz, split (r z)]
    group
  · intro hz hk
    have hv : (nativeC60CPGenericKernelPart r i split z : G) = 1 := by
      simpa only [Subgroup.coe_one] using congrArg Subtype.val hk
    have hfac := nativeC60CPGenericFactor r i split z
    rw [hv, one_mul] at hfac
    exact hz hfac.symm

/-- Exact obstruction to a trivial genuine kernel, with no supposition
that the previously embedded nonabelian free factor is all of isotropy. -/
theorem nativeC60CQGenericKernel_nontrivial_iff
    (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h) :
    (∃ k : r.ker, k ≠ 1) ↔ ∃ z : G, z ≠ i (r z) := by
  constructor
  · rintro ⟨k, hk⟩
    refine ⟨(k : G), ?_⟩
    intro h
    apply hk
    apply Subtype.ext
    have hrk : r (k : G) = 1 := (MonoidHom.mem_ker).mp k.property
    simpa [hrk] using h
  · rintro ⟨z, hz⟩
    exact ⟨nativeC60CPGenericKernelPart r i split z,
      (nativeC60CQGenericKernelPart_ne_one_iff r i split z).mpr hz⟩

/-- The original strict conjugation action is trivial if and only if the
embedded free factor CENTRALIZES every element of the actual kernel. -/
theorem nativeC60CQGenericAction_trivial_iff
    (r : G →* H) (i : H →* G) :
    (∀ x : H, nativeC60CPGenericAction r i x = 1) ↔
      ∀ (x : H) (k : r.ker), i x * (k : G) = (k : G) * i x := by
  constructor
  · intro h x k
    have hact : (nativeC60CPGenericAction r i x) k = k := by
      rw [h x]
      rfl
    have hv := congrArg Subtype.val hact
    rw [nativeC60CPGenericAction_coe] at hv
    calc
      i x * (k : G) = (i x * (k : G) * (i x)⁻¹) * i x := by group
      _ = (k : G) * i x := by rw [hv]
  · intro h x
    apply MulEquiv.ext
    intro k
    apply Subtype.ext
    change ((nativeC60CPGenericAction r i x) k : G) = (k : G)
    rw [nativeC60CPGenericAction_coe, h x k]
    group

/-- Failure of a single true-kernel commutation relation detects a
nontrivial action. This does not manufacture an unproved kernel witness. -/
theorem nativeC60CQGenericAction_nontrivial_of_noncommute
    (r : G →* H) (i : H →* G)
    (x : H) (k : r.ker)
    (hne : i x * (k : G) ≠ (k : G) * i x) :
    nativeC60CPGenericAction r i x ≠ 1 := by
  intro htriv
  have hact : (nativeC60CPGenericAction r i x) k = k := by
    rw [htriv]
    rfl
  have hv := congrArg Subtype.val hact
  rw [nativeC60CPGenericAction_coe] at hv
  apply hne
  calc
    i x * (k : G) = (i x * (k : G) * (i x)⁻¹) * i x := by group
    _ = (k : G) * i x := by rw [hv]

/-- Only after the CENTRALIZATION OBSTRUCTION is discharged does the
canonical semidirect normal form give a genuine direct-product group
isomorphism. Mere bijectivity of CP's underlying sets is insufficient. -/
def nativeC60CQGenericDirectProduct
    (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h)
    (hcomm : ∀ (x : H) (k : r.ker),
      i x * (k : G) = (k : G) * i x) :
    (r.ker × H) ≃* G where
  toFun z := (z.1 : G) * i z.2
  invFun z := (nativeC60CPGenericKernelPart r i split z, r z)
  left_inv z := by
    apply Prod.ext
    · exact nativeC60CPGenericKernelPart_recovery r i split z.1 z.2
    · exact nativeC60CPGenericFreePart_recovery r i split z.1 z.2
  right_inv z := nativeC60CPGenericFactor r i split z
  map_mul' x y := by
    change (((x.1 * y.1 : r.ker) : G) * i (x.2 * y.2)) =
      ((x.1 : G) * i x.2) * ((y.1 : G) * i y.2)
    simp only [Subgroup.coe_mul, map_mul]
    calc
      ((x.1 : G) * (y.1 : G)) * (i x.2 * i y.2) =
          (x.1 : G) * ((y.1 : G) * i x.2) * i y.2 := by group
      _ = (x.1 : G) * (i x.2 * (y.1 : G)) * i y.2 := by
        rw [← hcomm x.2 y.1]
      _ = ((x.1 : G) * i x.2) * ((y.1 : G) * i y.2) := by group

end SplitGroup

section AbstractC60

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- An ORIGINAL dependent strict loop lies in the kernel exactly when
its full BC/BW holonomy has zero CN *decoded* free-fork component. -/
theorem nativeC60CQRawLoop_mem_kernel_iff
    (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a a) :
    nativeC60CORawLoop S F word c ∈ NativeC60CPKernel S F word base ↔
      nativeC60CNRetraction S F base (nativeC60BWFreeHolonomy S F c) = 1 := by
  change nativeC60CNRetraction S F base
      (nativeC60BXFreeUnprefix S word
        (nativeC60COHolonomy S F word a (nativeC60CORawLoop S F word c))) = 1 ↔ _
  rw [nativeC60CORawLoop_holonomy, nativeC60BXFreeUnprefix_prefix]

/-- Nontrivial FULL provenance forces a nonidentity strict automorphism.
It need not force a nonidentity CN decoded coordinate. -/
theorem nativeC60CQRawLoop_ne_one_of_full
    (word : List Bool) {a : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a a)
    (hne : nativeC60BWFreeHolonomy S F c ≠ 1) :
    nativeC60CORawLoop S F word c ≠ 1 := by
  intro hz
  have h := congrArg (nativeC60COHolonomy S F word a) hz
  rw [nativeC60CORawLoop_holonomy, map_one] at h
  have hu := congrArg (nativeC60BXFreeUnprefix S word) h
  rw [nativeC60BXFreeUnprefix_prefix, map_one] at hu
  exact hne hu

/-- A sufficient, entirely typed construction of a nonidentity actual
kernel element. Its two independent premises are intentionally not
identified: decoding vanishes, but complete holonomy does not. -/
theorem nativeC60CQTypedKernel_witness
    (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (p : NativeC60CASignedChain S F a a)
    (hdecode : nativeC60CNRetraction S F base
      (FreeGroup.mk (nativeC60CAChainSignedCodes S F p)) = 1)
    (hfull : FreeGroup.mk (nativeC60CAChainSignedCodes S F p) ≠ 1) :
    ∃ k : NativeC60CPKernel S F word base, k ≠ 1 := by
  have hmem : nativeC60CORawLoop S F word
      (nativeC60CAChainStep S F p) ∈ NativeC60CPKernel S F word base := by
    apply (nativeC60CQRawLoop_mem_kernel_iff S F word base
      (nativeC60CAChainStep S F p)).mpr
    rw [nativeC60CAChain_holonomy]
    exact hdecode
  have hne : nativeC60CORawLoop S F word
      (nativeC60CAChainStep S F p) ≠ 1 := by
    apply nativeC60CQRawLoop_ne_one_of_full S F word
    rw [nativeC60CAChain_holonomy]
    exact hfull
  refine ⟨⟨nativeC60CORawLoop S F word
    (nativeC60CAChainStep S F p), hmem⟩, ?_⟩
  intro hk
  apply hne
  simpa only [Subgroup.coe_one] using congrArg Subtype.val hk

/-- On actual C60, the obstruction to a trivial action can be checked
on each ORIGINAL BC fork letter, rather than on abstract free words.
No unproved commutativity of letters is used. -/
theorem nativeC60CQAction_trivial_iff_letters
    (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    (∀ x : FreeGroup (NativeC60CNForkAlphabet S F base),
      nativeC60CPAction S F word base x = 1) ↔
    ∀ (j : NativeC60CNForkAlphabet S F base)
      (k : NativeC60CPKernel S F word base),
      nativeC60COEmbed S F word base (FreeGroup.of j) *
          (k : NativeC60COIsotropy S F word a) =
        (k : NativeC60COIsotropy S F word a) *
          nativeC60COEmbed S F word base (FreeGroup.of j) := by
  constructor
  · intro h j k
    exact (nativeC60CQGenericAction_trivial_iff
      (nativeC60CORetraction S F word base)
      (nativeC60COEmbed S F word base)).mp h (FreeGroup.of j) k
  · intro h
    have hhom : nativeC60CPAction S F word base =
        (1 : FreeGroup (NativeC60CNForkAlphabet S F base) →*
          MulAut (NativeC60CPKernel S F word base)) := by
      apply FreeGroup.ext_hom
      intro j
      apply MulEquiv.ext
      intro k
      apply Subtype.ext
      change ((nativeC60CPAction S F word base (FreeGroup.of j)) k :
        NativeC60COIsotropy S F word a) =
        (k : NativeC60COIsotropy S F word a)
      rw [nativeC60CPAction_coe, h j k]
      group
    intro x
    have hx := DFunLike.congr_fun hhom x
    simpa using hx

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

/-- The exact kernel-existence obstruction in the original physical C60
conservative atom, for independent inner and outer finite AQ contexts. -/
theorem nativeK5CQPhysical_kernel_nontrivial_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    (∃ k : NativeC60CPKernel (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner), k ≠ 1) ↔
    ∃ z : NativeC60COIsotropy (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
       outer (nativeK5CHSource W inner (nativeK5CKConservativeAtom W R)),
      z ≠ nativeC60COEmbed (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CKAtomGenerator W R inner)
        (nativeC60CORetraction (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          outer (nativeK5CKAtomGenerator W R inner) z) :=
  nativeC60CQGenericKernel_nontrivial_iff
    (nativeC60CORetraction (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner))
    (nativeC60COEmbed (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner))
    (nativeC60CORetraction_embed (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner))

end PhysicalC60

#print axioms nativeC60CQGenericKernelPart_ne_one_iff
#print axioms nativeC60CQGenericKernel_nontrivial_iff
#print axioms nativeC60CQGenericAction_trivial_iff
#print axioms nativeC60CQGenericAction_nontrivial_of_noncommute
#print axioms nativeC60CQGenericDirectProduct
#print axioms nativeC60CQRawLoop_mem_kernel_iff
#print axioms nativeC60CQRawLoop_ne_one_of_full
#print axioms nativeC60CQTypedKernel_witness
#print axioms nativeC60CQAction_trivial_iff_letters
#print axioms nativeK5CQPhysical_kernel_nontrivial_iff

end
end Kuu.F112.Physical
