import Kuu.F112.PolygonNativeC60StrictKernelActionObstruction

/-!
# F112-P94D3CR — complete original typed-loop kernel criterion

BA supplies an original raw16D representative for EVERY actual strict Hom;
CD converts every such raw comparison to an ORIGINAL finite dependent
signed chain with identical nonabelian BW holonomy. CR joins these with
CQ's genuine split strict isotropy kernel.

At each original framed 15D object and every genuine finite AQ context,
the TRUE retraction kernel is nontrivial if and only if a COMPLETE typed
signed closed chain has nontrivial full BW holonomy yet zero BX-unprefixed
CN decoded coordinate. This closes the necessity direction missing in CQ.

This equivalence does not assert that such a chain exists physically.
In particular, the kernel of full holonomy is NOT identified with the
kernel of the CN retraction. CN fork chains are separately ruled out as
new kernel witnesses. No Gray, new axiom, sorry/admit or new public root.
The original proof-carrying 15D endpoints and all finite AQ words remain.

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

section AbstractC60

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- An actual strict automorphism at the FULL original outer-framed 15D
object, represented by a genuine source-and-target-typed raw16D loop. -/
def nativeC60CRFramedRawLoop (word : List Bool) (a : L.Total)
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F)
      (nativeC60BCContextTotal F word a)
      (nativeC60BCContextTotal F word a)) :
    NativeC60COIsotropy S F word a :=
  MulOpposite.op {
    hom := nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) c
    inv := nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) (.symm c)
    hom_inv_id := nativeC60AZStrictStep_inv_left _ _ _
    inv_hom_id := nativeC60AZStrictStep_inv_right _ _ _ }

/-- The FULL nonabelian strict holonomy; no redundant AQ prefix. -/
theorem nativeC60CRFramedRawLoop_holonomy
    (word : List Bool) (a : L.Total)
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F)
      (nativeC60BCContextTotal F word a)
      (nativeC60BCContextTotal F word a)) :
    nativeC60COHolonomy S F word a (nativeC60CRFramedRawLoop S F word a c) =
      nativeC60BWFreeHolonomy S F c := by
  change MulOpposite.unop ((nativeC60BWFreeStrictHolonomy S F).map
    (nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) c)) = _
  rw [nativeC60BXFreeStrictHolonomy_step, MulOpposite.unop_op]

/-- EVERY actual strict isotropy loop has an ORIGINAL dependent raw16D
representative at the same precise framed 15D object, by BA. -/
theorem nativeC60CRFramedRawLoop_surjective
    (word : List Bool) (a : L.Total) :
    Function.Surjective (nativeC60CRFramedRawLoop S F word a) := by
  intro z
  obtain ⟨c, hc⟩ := nativeC60BAStep_surjective
    (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    (nativeC60BCContextTotal F word a)
    (nativeC60BCContextTotal F word a) z.unop.hom
  refine ⟨c, ?_⟩
  apply MulOpposite.unop_injective
  apply Aut.ext
  exact hc

/-- Complete BW holonomy detects exact nonidentity of a raw strict loop. -/
theorem nativeC60CRFramedRawLoop_ne_one_iff
    (word : List Bool) (a : L.Total)
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F)
      (nativeC60BCContextTotal F word a)
      (nativeC60BCContextTotal F word a)) :
    nativeC60CRFramedRawLoop S F word a c ≠ 1 ↔
      nativeC60BWFreeHolonomy S F c ≠ 1 := by
  constructor
  · intro hz hfull
    apply hz
    apply nativeC60COHolonomy_injective S F word a
    rw [nativeC60CRFramedRawLoop_holonomy, hfull, map_one]
  · intro hfull hz
    have h := congrArg (nativeC60COHolonomy S F word a) hz
    rw [nativeC60CRFramedRawLoop_holonomy, map_one] at h
    exact hfull h

/-- The exact kernel test, distinguishing the full BW word from the
BX-unprefixed, CN-decoded free-fork coordinate. -/
theorem nativeC60CRFramedRawLoop_mem_kernel_iff
    (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F)
      (nativeC60BCContextTotal F word a)
      (nativeC60BCContextTotal F word a)) :
    nativeC60CRFramedRawLoop S F word a c ∈ NativeC60CPKernel S F word base ↔
      nativeC60CNRetraction S F base
        (nativeC60BXFreeUnprefix S word
          (nativeC60BWFreeHolonomy S F c)) = 1 := by
  change nativeC60CNRetraction S F base
    (nativeC60BXFreeUnprefix S word
      (nativeC60COHolonomy S F word a
        (nativeC60CRFramedRawLoop S F word a c))) = 1 ↔ _
  rw [nativeC60CRFramedRawLoop_holonomy]

/-- The kernel is nontrivial if and only if an ACTUAL original dependent
raw16D based loop has nontrivial complete free holonomy but trivial
decoded free-fork coordinate. No representability assumption is added. -/
theorem nativeC60CRKernel_nontrivial_iff_raw
    (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    (∃ k : NativeC60CPKernel S F word base, k ≠ 1) ↔
      ∃ c : NativeC60AXStep (nativeC60BCClosedSignature S F)
        (nativeC60BCContextTotal F word a)
        (nativeC60BCContextTotal F word a),
        nativeC60CNRetraction S F base
          (nativeC60BXFreeUnprefix S word
            (nativeC60BWFreeHolonomy S F c)) = 1 ∧
          nativeC60BWFreeHolonomy S F c ≠ 1 := by
  constructor
  · rintro ⟨k, hk⟩
    obtain ⟨c, hc⟩ := nativeC60CRFramedRawLoop_surjective
      S F word a (k : NativeC60COIsotropy S F word a)
    refine ⟨c, ?_, ?_⟩
    · apply (nativeC60CRFramedRawLoop_mem_kernel_iff S F word base c).mp
      rw [hc]
      exact k.property
    · apply (nativeC60CRFramedRawLoop_ne_one_iff S F word a c).mp
      rw [hc]
      intro hz
      apply hk
      apply Subtype.ext
      simpa only [Subgroup.coe_one] using hz
  · rintro ⟨c, hdec, hfull⟩
    refine ⟨⟨nativeC60CRFramedRawLoop S F word a c,
      (nativeC60CRFramedRawLoop_mem_kernel_iff S F word base c).mpr hdec⟩, ?_⟩
    intro h
    have hz := congrArg Subtype.val h
    have hnot := (nativeC60CRFramedRawLoop_ne_one_iff
      S F word a c).mpr hfull
    exact hnot (by simpa only [Subgroup.coe_one] using hz)

/-- CD converts ANY raw comparison to a finite signed chain with the
exact same complete BW word, retaining every intermediate 15D Type. -/
theorem nativeC60CRRawToSigned_full_word
    (word : List Bool) (a : L.Total)
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F)
      (nativeC60BCContextTotal F word a)
      (nativeC60BCContextTotal F word a)) :
    FreeGroup.mk (nativeC60CAChainSignedCodes S F
      (nativeC60CDRawToChain S F c)) =
      nativeC60BWFreeHolonomy S F c :=
  (nativeC60CAChain_holonomy S F
    (nativeC60CDRawToChain S F c)).symm.trans
      (nativeC60CDRawToChain_free S F [] c)

/-- Complete NECESSARY-AND-SUFFICIENT criterion on an ACTUAL finite
dependent signed original 16D chain. The chain is based at the full
framed 15D object, not at an invented graph vertex. -/
theorem nativeC60CRKernel_nontrivial_iff_signed
    (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    (∃ k : NativeC60CPKernel S F word base, k ≠ 1) ↔
      ∃ p : NativeC60CASignedChain S F
        (nativeC60BCContextTotal F word a)
        (nativeC60BCContextTotal F word a),
        nativeC60CNRetraction S F base
          (nativeC60BXFreeUnprefix S word
            (FreeGroup.mk (nativeC60CAChainSignedCodes S F p))) = 1 ∧
          FreeGroup.mk (nativeC60CAChainSignedCodes S F p) ≠ 1 := by
  constructor
  · intro hk
    obtain ⟨c, hdec, hnon⟩ :=
      (nativeC60CRKernel_nontrivial_iff_raw S F word base).mp hk
    refine ⟨nativeC60CDRawToChain S F c, ?_, ?_⟩
    · rw [nativeC60CRRawToSigned_full_word S F word a c]
      exact hdec
    · rw [nativeC60CRRawToSigned_full_word S F word a c]
      exact hnon
  · rintro ⟨p, hdec, hnon⟩
    apply (nativeC60CRKernel_nontrivial_iff_raw S F word base).mpr
    refine ⟨nativeC60CAChainStep S F p, ?_, ?_⟩
    · rw [nativeC60CAChain_holonomy]
      exact hdec
    · rw [nativeC60CAChain_holonomy]
      exact hnon

/-- Entire original CN finite fork words give NO additional nonzero
kernel witness: decoded zero and complete BW zero coincide there. -/
theorem nativeC60CRForkChain_decode_zero_iff_full_zero
    {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (xs : List (NativeC60CNForkAlphabet S F base × Bool)) :
    nativeC60CNRetraction S F base
        (nativeC60BWFreeHolonomy S F
          (nativeC60CAChainStep S F (nativeC60CNWordChain S F base xs))) = 1 ↔
      nativeC60BWFreeHolonomy S F
        (nativeC60CAChainStep S F (nativeC60CNWordChain S F base xs)) = 1 := by
  rw [nativeC60CNWordChain_holonomy,
    nativeC60CNRetraction_left_inverse S F base (FreeGroup.mk xs)]
  constructor
  · intro hx
    rw [hx, map_one]
  · intro hx
    apply nativeC60CNEmbed_injective S F base
    simpa only [map_one] using hx

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

/-- Full PHYSICAL conservative atom, independently chosen original finite
inner/outer AQ context and original Type-valued 15D boundary. A witness
of kernel nontriviality must be found, not postulated by this criterion. -/
theorem nativeK5CRPhysical_kernel_nontrivial_iff_signed
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (inner outer : List Bool) :
    (∃ k : NativeC60CPKernel (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner), k ≠ 1) ↔
    ∃ chain : NativeC60CASignedChain
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (nativeC60BCContextTotal (nativeK5BCFrame W) outer
          (nativeK5CHSource W inner (nativeK5CKConservativeAtom W R)))
        (nativeC60BCContextTotal (nativeK5BCFrame W) outer
          (nativeK5CHSource W inner (nativeK5CKConservativeAtom W R))),
      nativeC60CNRetraction (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          (nativeK5CKAtomGenerator W R inner)
          (nativeC60BXFreeUnprefix (nativeK5AXKuuSignature W) outer
            (FreeGroup.mk (nativeC60CAChainSignedCodes
              (nativeK5AXKuuSignature W) (nativeK5BCFrame W) chain))) = 1 ∧
      FreeGroup.mk (nativeC60CAChainSignedCodes
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) chain) ≠ 1 :=
  nativeC60CRKernel_nontrivial_iff_signed
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    outer (nativeK5CKAtomGenerator W R inner)

end PhysicalC60

#print axioms nativeC60CRFramedRawLoop
#print axioms nativeC60CRFramedRawLoop_holonomy
#print axioms nativeC60CRFramedRawLoop_surjective
#print axioms nativeC60CRFramedRawLoop_ne_one_iff
#print axioms nativeC60CRFramedRawLoop_mem_kernel_iff
#print axioms nativeC60CRKernel_nontrivial_iff_raw
#print axioms nativeC60CRRawToSigned_full_word
#print axioms nativeC60CRKernel_nontrivial_iff_signed
#print axioms nativeC60CRForkChain_decode_zero_iff_full_zero
#print axioms nativeK5CRPhysical_kernel_nontrivial_iff_signed

end
end Kuu.F112.Physical
