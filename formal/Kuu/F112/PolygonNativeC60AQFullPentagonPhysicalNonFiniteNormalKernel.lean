import Mathlib.GroupTheory.FinitelyPresentedGroup
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalInfiniteRootSupport

/-!
# F112-P94D3FV — exact finite normal-generation criterion and
# genuine FJ physical infinite normal kernel rank obstruction

FS established an EXACT normal presentation for ANY FreeGroup.map f
using the nontrivial rooted letters a != root_f(a), and proved that
FINITE active support SUFFICES for finite normal generation. FU then
proved that the ACTUAL old FJ physical original 18D DV transport
has INFINITE active support for EVERY nonempty finite AQ context,
via the true arbitrary-depth post-whiskering tower.

FV closes the essential missing converse rigorously, without
confusing infinitely many rooted source letters with independent
normal generators:

1. For EACH original source letter a, use pinned mathlib's actual
   FreeGroup.lift to define a coordinate group homomorphism into
   Multiplicative Int. It detects occurrence of a in the full
   ordered signed noncommutative source group.
2. For EACH arbitrary free-group word z, prove a FINITE set of
   source letters outside which every coordinate hom annihilates z.
   For EACH FINITE set of arbitrary group-word relators R, prove
   a common finite support outside which all R are annihilated.
3. If active-root original source letters are infinite, select an
   active a OUTSIDE that finite support. Its genuine rooted relator
   of a against its actual-image fiber root belongs to ker(FreeGroup.map f),
   but the coordinate hom sends this relator to nonzero integer 1
   while annihilating R and thus their ENTIRE NORMAL closure.
   Therefore NO finite family of arbitrary noncommutative group
   words normally generates the whole kernel.
4. In conjunction with FS, prove the exact general IFF:
     (FreeGroup.map f).ker.IsNormalClosureFG
       <-> (FSActiveLetters f).Finite.
   This is an equivalence for genuine kernels of FREE-GROUP MAPS,
   not for arbitrary general group homomorphisms.
5. Apply to the actual unquotiented OLD FJ 18D physical DV
   source group and the FU infinite active-root theorem, to prove
   that every NONEMPTY genuine finite C60 AQ physical context
   has a kernel that is NOT finitely normally generated.

No assumption of finite signed-word length bound, faithfulness,
commutativity or abelianized quotient. The integer coordinate
detector is a group homomorphism used ONLY to prove a precise
non-membership statement in a noncommutative normal closure:
the ORIGINAL source group/kernel stay noncommutative. We do
NOT claim a minimal independent basis or exact normal rank cardinal,
the single known FJ defect generates the whole kernel, any global
strict higher coherence or a true geometric 19D filler. Preserve
old DS/FJ/FN no-go and distinct FK/FL/FM presentation,
Type-valued 14D–18D history, strict Kuu core/independent Kuu
presentation, 107 public roots, no Gray and pinned Lean/mathlib.
Append-only / no new axioms, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

section FreeGroupFiniteNormalRankObstruction

/-- Original full noncommutative word -> integer coordinate:
the selected source generator a contributes 1, all OTHER
source letters contribute 0. The codomain is written in
multiplicative notation to preserve the Group-hom interface. -/
def nativeC60FVLetterCoordinate
    {A : Type u} (a : A) : FreeGroup A →* Multiplicative ℤ := by
  classical
  exact FreeGroup.lift
    (fun b : A => if b = a then Multiplicative.ofAdd (1 : ℤ) else 1)

/-- A full ordered signed FreeGroup word depends on only FINITELY
many source letters: every letter coordinate outside a specific
finite set sends the whole word to the identity. The proof uses
the actual pinned mathlib free-group induction, not an assumption
that words commute, nor a lossy graph projection. -/
theorem nativeC60FVWord_finiteCoordinateSupport
    {A : Type u} (z : FreeGroup A) :
    ∃ s : Finset A, ∀ a : A, a ∉ s →
      (nativeC60FVLetterCoordinate a) z = 1 := by
  classical
  refine FreeGroup.induction_on z ?_ ?_ ?_ ?_
  · refine ⟨∅, ?_⟩
    intro a _
    exact map_one (nativeC60FVLetterCoordinate a)
  · intro b
    refine ⟨{b}, ?_⟩
    intro a ha
    have hba : b ≠ a := by
      intro h
      exact ha (Finset.mem_singleton.mpr h.symm)
    simp only [nativeC60FVLetterCoordinate, FreeGroup.lift_apply_of,
      if_neg hba]
  · intro b hb
    obtain ⟨s, hs⟩ := hb
    refine ⟨s, ?_⟩
    intro a ha
    simpa only [map_inv, inv_one] using
      congrArg Inv.inv (hs a ha)
  · intro x y hx hy
    obtain ⟨sx, hsx⟩ := hx
    obtain ⟨sy, hsy⟩ := hy
    refine ⟨sx ∪ sy, ?_⟩
    intro a ha
    have hax : a ∉ sx := by
      intro hx
      exact ha (Finset.mem_union_left sy hx)
    have hay : a ∉ sy := by
      intro hy
      exact ha (Finset.mem_union_right sx hy)
    simpa only [map_mul, hsx a hax, hsy a hay, one_mul]

/-- Choice of a finite original source-letter support per full
noncommutative free-group word; NOT a chosen support of target
images or a quotient of the original source alphabet. -/
noncomputable def nativeC60FVWordSupport
    {A : Type u} (z : FreeGroup A) : Finset A :=
  Classical.choose (nativeC60FVWord_finiteCoordinateSupport z)

theorem nativeC60FVWordSupport_outside
    {A : Type u} (z : FreeGroup A)
    (a : A) (ha : a ∉ nativeC60FVWordSupport z) :
    (nativeC60FVLetterCoordinate a) z = 1 :=
  Classical.choose_spec (nativeC60FVWord_finiteCoordinateSupport z) a ha

/-- The UNION of the finite source-letter supports of ANY FINITE
family R of arbitrary original free-group words. This construction
does not presuppose that R consists of two-letter rooted defects. -/
noncomputable def nativeC60FVFiniteRelatorsSupport
    {A : Type u} (R : Set (FreeGroup A)) (hR : R.Finite) : Finset A := by
  classical
  exact hR.toFinset.biUnion (fun z => nativeC60FVWordSupport z)

/-- Every original integer coordinate outside the combined
finite source support annihilates EVERY arbitrary relator of R. -/
theorem nativeC60FVFiniteRelatorsSupport_outside
    {A : Type u} (R : Set (FreeGroup A)) (hR : R.Finite)
    (a : A) (ha : a ∉ nativeC60FVFiniteRelatorsSupport R hR)
    (z : FreeGroup A) (hz : z ∈ R) :
    (nativeC60FVLetterCoordinate a) z = 1 := by
  classical
  have hzFin : z ∈ hR.toFinset :=
    (Set.Finite.mem_toFinset hR).mpr hz
  have haWord : a ∉ nativeC60FVWordSupport z := by
    intro hword
    apply ha
    change a ∈ hR.toFinset.biUnion
      (fun x => nativeC60FVWordSupport x)
    exact Finset.mem_biUnion.mpr ⟨z, hzFin, hword⟩
  exact nativeC60FVWordSupport_outside z a haWord

/-- The coordinate detector maps a *NONROOT* original source
letter's actual rooted two-letter free word to integer +1.
Any OTHER original source letter, including its chosen root,
maps to 0. This is a group-hom calculation, not a quotient
identification of distinct source codes. -/
theorem nativeC60FVActiveRoot_coordinate
    {A : Type u} {B : Type v} (f : A → B)
    (a : A) (ha : a ∈ nativeC60FSActiveLetters f) :
    (nativeC60FVLetterCoordinate a)
        (nativeC60FSRootedRelator f a) =
          Multiplicative.ofAdd (1 : ℤ) := by
  have hroot : nativeC60FQLetterRoot f a ≠ a := Ne.symm ha
  simp only [nativeC60FSRootedRelator, map_mul, map_inv,
    nativeC60FVLetterCoordinate, FreeGroup.lift_apply_of,
    if_pos rfl, if_neg hroot, inv_one, mul_one]

/-- The same nonroot original two-letter relator has NONTRIVIAL
integer coordinate, so it cannot lie in any normal subgroup
annihilated by the corresponding coordinate homomorphism. -/
theorem nativeC60FVActiveRoot_coordinate_ne_one
    {A : Type u} {B : Type v} (f : A → B)
    (a : A) (ha : a ∈ nativeC60FSActiveLetters f) :
    (nativeC60FVLetterCoordinate a)
        (nativeC60FSRootedRelator f a) ≠ 1 := by
  rw [nativeC60FVActiveRoot_coordinate f a ha]
  intro h
  have hz : (1 : ℤ) = 0 := congrArg Multiplicative.toAdd h
  exact one_ne_zero hz

/-- IMPORTANT GENERAL THEOREM: if there are infinitely many
genuinely nonroot image-fiber letters, then the kernel of the
full NONCOMMUTATIVE free-group map is NOT the normal closure of
ANY finite set of arbitrary original group words.

The detector does not merely count listed FQ relations. It
annihilates all finite relators and hence their entire normal
closure, while detecting one actual rooted kernel element
outside their combined original source-letter support. -/
theorem nativeC60FVFreeMap_kernel_not_finitely_normallyGenerated
    {A : Type u} {B : Type v} (f : A → B)
    (hinf : (nativeC60FSActiveLetters f).Infinite) :
    ¬ (FreeGroup.map f).ker.IsNormalClosureFG := by
  classical
  intro hfiniteNormal
  obtain ⟨R, hRfinite, hRclosure⟩ := hfiniteNormal
  let s := nativeC60FVFiniteRelatorsSupport R hRfinite
  obtain ⟨a, ha, haNot⟩ :=
    hinf.exists_notMem_finset s
  have hRcoordinate :
      R ⊆ (nativeC60FVLetterCoordinate a).ker := by
    intro z hz
    apply MonoidHom.mem_ker.mpr
    exact nativeC60FVFiniteRelatorsSupport_outside
      R hRfinite a haNot z hz
  have hnormalCoordinate :
      Subgroup.normalClosure R ≤ (nativeC60FVLetterCoordinate a).ker := by
    apply Subgroup.normalClosure_le_normal
    intro z hz
    exact hRcoordinate hz
  have hrelKer :
      nativeC60FSRootedRelator f a ∈ (FreeGroup.map f).ker := by
    rw [nativeC60FSFreeMap_kernel_eq_active f]
    apply Subgroup.subset_normalClosure
    exact nativeC60FSActiveRelator_mem f a ha
  have hrelClosure :
      nativeC60FSRootedRelator f a ∈ Subgroup.normalClosure R := by
    rw [hRclosure]
    exact hrelKer
  have hrelZero :
      (nativeC60FVLetterCoordinate a)
          (nativeC60FSRootedRelator f a) = 1 :=
    MonoidHom.mem_ker.mp (hnormalCoordinate hrelClosure)
  exact (nativeC60FVActiveRoot_coordinate_ne_one f a ha) hrelZero

/-- EXACT necessary-and-sufficient general group-theoretic
criterion for kernels of FreeGroup.map f:
they are finitely normally generated by SOME arbitrary group words
IFF the actual selected-root ACTIVE source-letter set is finite.

FS proved the finite->normally-finite half. FV proves the nontrivial
converse using finite ORIGINAL word supports and a concrete
integer-coordinate detecting homomorphism. -/
theorem nativeC60FVFreeMap_kernel_finiteNormal_iff_activeFinite
    {A : Type u} {B : Type v} (f : A → B) :
    (FreeGroup.map f).ker.IsNormalClosureFG ↔
      (nativeC60FSActiveLetters f).Finite := by
  classical
  constructor
  · intro hfinite
    by_contra hinf
    exact (nativeC60FVFreeMap_kernel_not_finitely_normallyGenerated
      f hinf) hfinite
  · intro hfinite
    obtain ⟨R, hR, hker⟩ :=
      nativeC60FSKernel_finitely_normalGenerated_of_active_finite
        f hfinite
    exact ⟨R, hR, hker.symm⟩

end FreeGroupFiniteNormalRankObstruction

section OriginalDependentEighteenKernelObstruction

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- EXACT normal finite-generation criterion for the actual
full dependent 18D DV kernel, relative to its TRUE original
signed free-word alphabet and its separate context-closed target.
An actual finite active-source support is both necessary and
sufficient, not merely sufficient as FS had proved. -/
theorem nativeC60FVFullDV_kernel_finiteNormal_iff_activeFinite
    (word : List Bool) :
    (nativeC60DVFullWordTransport S F word).ker.IsNormalClosureFG ↔
      (nativeC60FSActiveLetters
        (nativeC60DVTransportCompleteCode S F word)).Finite := by
  rw [nativeC60FCTransport_eq_freeMap S F word]
  exact nativeC60FVFreeMap_kernel_finiteNormal_iff_activeFinite
    (nativeC60DVTransportCompleteCode S F word)

end OriginalDependentEighteenKernelObstruction

section GenuinePhysicalNonfiniteNormalKernel

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

/-- ACTUAL ORIGINAL FJ PHYSICAL RESULT: for EVERY nonempty finite
C60 AQ context word, the full original noncommutative 18D DV
transport kernel is NOT finitely NORMALLY generated by ANY
finite family of group words, not merely by finite rooted relations.

The lower FJ 15D distinct physical certificates were transported
through original 17D and all post-whiskering recursion depths in
FU. The genuine infinite active-support input is now discharged. -/
theorem nativeK5FVPhysical_fullDVKernel_not_finitelyNormal
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (hne : word ≠ []) :
    ¬ (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker.IsNormalClosureFG := by
  have hinfinite :
      (nativeC60FSActiveLetters
        (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)).Infinite :=
    Set.infinite_coe_iff.mp
      (nativeK5FUPhysical_activeSource_infinite W R word hne)
  rw [nativeC60FCTransport_eq_freeMap
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word]
  exact nativeC60FVFreeMap_kernel_not_finitely_normallyGenerated
    (nativeC60DVTransportCompleteCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word) hinfinite

/-- No arbitrary physical 14D source fiber is needed:
the canonical genuine inhabited FJ critical-left fiber already
witnesses NONFINITE normal generation for every nonempty real
physical C60 AQ word. -/
theorem nativeK5FVPhysical_canonicalFullDVKernel_not_finitelyNormal
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ []) :
    ¬ (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker.IsNormalClosureFG :=
  nativeK5FVPhysical_fullDVKernel_not_finitelyNormal W
    (nativeK5FifteenCriticalLeft W) word hne

end GenuinePhysicalNonfiniteNormalKernel

#print axioms nativeC60FVWord_finiteCoordinateSupport
#print axioms nativeC60FVWordSupport_outside
#print axioms nativeC60FVFiniteRelatorsSupport_outside
#print axioms nativeC60FVActiveRoot_coordinate
#print axioms nativeC60FVActiveRoot_coordinate_ne_one
#print axioms nativeC60FVFreeMap_kernel_not_finitely_normallyGenerated
#print axioms nativeC60FVFreeMap_kernel_finiteNormal_iff_activeFinite
#print axioms nativeC60FVFullDV_kernel_finiteNormal_iff_activeFinite
#print axioms nativeK5FVPhysical_fullDVKernel_not_finitelyNormal
#print axioms nativeK5FVPhysical_canonicalFullDVKernel_not_finitelyNormal

end
end Kuu.F112.Physical
