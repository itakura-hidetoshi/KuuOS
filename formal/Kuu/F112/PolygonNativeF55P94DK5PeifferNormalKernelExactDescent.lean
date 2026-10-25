import Kuu.F112.PolygonNativeF55P94DK5GaugeHolonomyUniversalDescent
import Mathlib.GroupTheory.QuotientGroup.Defs
import Mathlib.Tactic

/-!
# F112-P94D3AS — typed C60 contextual Peiffer kernel and exact descent

On the original SOURCE-DEPENDENT fourteen-cell proof fiber, P94D3AR
constructed the normal closure of ALL genuinely whiskered 15-cell
exchange defects.  This file supplies its proof-relevant algebraic
crossed-module structure (normal inclusion N -> F) and a short exact
sequence at F, using the ACTUAL original Type-valued contextual
exchange generators, not scalar equalities or invented higher cells.

Physical 14D right-whiskering implements the group-level Peiffer action
by the inverse of its true free-history frame; left-whiskering acts
trivially on the *ordered defect*.  All group-valued observers of the
original free history descend to the AQ 15D quotient if and only if
they identify the SINGLE ORIGINAL source-typed base exchange.  This
provides an explicit necessary and sufficient gateway for possible
future P92B group receivers, not a claimed unconditional P92B functor.

The normal-inclusion crossed module is an ALGEBRAIC SHADOW.  Its
Peiffer identity is NOT an original geometric 16-cell, and does not
imply coherence, raw fourteen-cell equality, or global strict n-cells.
Only KuuOSFormal is public; no Gray, new axioms, sorry, or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uG
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalFourteenFiber

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

/-- The AR normal kernel is the group-level Peiffer module, with the
same ORIGINAL C60 source-dependent index W. -/
abbrev NativeK5ASPeifferKernel
    (W : NativeK5StructuralThirteenCell p U V) :=
  nativeK5ARHistoryKernel W

/-- The Peiffer boundary is honest inclusion of the exact normal
kernel into the ORIGINAL noncommutative free-history group. -/
def nativeK5ASPeifferBoundary
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5ASPeifferKernel W →* NativeK5FourteenHistoryWord :=
  (nativeK5ARHistoryKernel W).subtype

/-- The proof-relevant conjugation action on the normal kernel.
No equality between raw 14D proofs is used here. -/
def nativeK5ASPeifferAct
    (W : NativeK5StructuralThirteenCell p U V)
    (g : NativeK5FourteenHistoryWord)
    (z : NativeK5ASPeifferKernel W) :
    NativeK5ASPeifferKernel W :=
  ⟨g * (z : NativeK5FourteenHistoryWord) * g⁻¹,
    (inferInstance : (nativeK5ARHistoryKernel W).Normal).conj_mem
      (z : NativeK5FourteenHistoryWord) z.property g⟩

theorem nativeK5ASPeifferAct_one
    (W : NativeK5StructuralThirteenCell p U V)
    (g : NativeK5FourteenHistoryWord) :
    nativeK5ASPeifferAct W g 1 = 1 := by
  apply Subtype.ext
  change g * (1 : NativeK5FourteenHistoryWord) * g⁻¹ = 1
  group

theorem nativeK5ASPeifferAct_mul
    (W : NativeK5StructuralThirteenCell p U V)
    (g : NativeK5FourteenHistoryWord)
    (z t : NativeK5ASPeifferKernel W) :
    nativeK5ASPeifferAct W g (z * t) =
      nativeK5ASPeifferAct W g z *
        nativeK5ASPeifferAct W g t := by
  apply Subtype.ext
  change g * ((z : NativeK5FourteenHistoryWord) *
      (t : NativeK5FourteenHistoryWord)) * g⁻¹ =
    (g * (z : NativeK5FourteenHistoryWord) * g⁻¹) *
      (g * (t : NativeK5FourteenHistoryWord) * g⁻¹)
  group

theorem nativeK5ASPeifferAct_identity
    (W : NativeK5StructuralThirteenCell p U V)
    (z : NativeK5ASPeifferKernel W) :
    nativeK5ASPeifferAct W 1 z = z := by
  apply Subtype.ext
  change (1 : NativeK5FourteenHistoryWord) *
    (z : NativeK5FourteenHistoryWord) * 1⁻¹ =
      (z : NativeK5FourteenHistoryWord)
  group

theorem nativeK5ASPeifferAct_comp
    (W : NativeK5StructuralThirteenCell p U V)
    (g h : NativeK5FourteenHistoryWord)
    (z : NativeK5ASPeifferKernel W) :
    nativeK5ASPeifferAct W (g * h) z =
      nativeK5ASPeifferAct W g
        (nativeK5ASPeifferAct W h z) := by
  apply Subtype.ext
  change (g * h) * (z : NativeK5FourteenHistoryWord) * (g * h)⁻¹ =
    g * (h * (z : NativeK5FourteenHistoryWord) * h⁻¹) * g⁻¹
  group

/-- The boundary is genuinely conjugation-equivariant in the original
free group, without imposing commutativity. -/
theorem nativeK5ASPeifferBoundary_equivariant
    (W : NativeK5StructuralThirteenCell p U V)
    (g : NativeK5FourteenHistoryWord)
    (z : NativeK5ASPeifferKernel W) :
    nativeK5ASPeifferBoundary W (nativeK5ASPeifferAct W g z) =
      g * nativeK5ASPeifferBoundary W z * g⁻¹ := rfl

/-- Peiffer identity for the ACTUAL AR normal-inclusion group.
This is only a group-level identity, not a geometric 16-cell. -/
theorem nativeK5ASPeiffer_identity
    (W : NativeK5StructuralThirteenCell p U V)
    (z t : NativeK5ASPeifferKernel W) :
    nativeK5ASPeifferAct W (nativeK5ASPeifferBoundary W z) t =
      z * t * z⁻¹ := by
  apply Subtype.ext
  rfl

/-- Proof-relevant crossed-module laws for the indexed physical
kernel; all operations above were constructed from actual words. -/
structure NativeK5ASCrossedModuleData
    (W : NativeK5StructuralThirteenCell p U V) where
  boundary : NativeK5ASPeifferKernel W →* NativeK5FourteenHistoryWord
  act : NativeK5FourteenHistoryWord →
      NativeK5ASPeifferKernel W → NativeK5ASPeifferKernel W
  act_identity : ∀ z, act 1 z = z
  act_comp : ∀ g h z, act (g * h) z = act g (act h z)
  act_one : ∀ g, act g 1 = 1
  act_mul : ∀ g z t, act g (z * t) = act g z * act g t
  boundary_equivariant :
    ∀ g z, boundary (act g z) = g * boundary z * g⁻¹
  peiffer : ∀ z t, act (boundary z) t = z * t * z⁻¹

def nativeK5ASCrossedModule
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5ASCrossedModuleData W :=
  { boundary := nativeK5ASPeifferBoundary W
    act := nativeK5ASPeifferAct W
    act_identity := nativeK5ASPeifferAct_identity W
    act_comp := nativeK5ASPeifferAct_comp W
    act_one := nativeK5ASPeifferAct_one W
    act_mul := nativeK5ASPeifferAct_mul W
    boundary_equivariant := nativeK5ASPeifferBoundary_equivariant W
    peiffer := nativeK5ASPeiffer_identity W }

/-- A physical, NON-EMPTY, Type-carrying element for EACH genuine
context-indexed 15-cell exchange: the boundary is its raw free-word
defect, not merely equal signed counts. -/
def nativeK5ASPhysicalDefect
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) : NativeK5ASPeifferKernel W :=
  ⟨nativeK5ARWordDefect W
      (nativeK5AQLeft W steps) (nativeK5AQRight W steps),
    nativeK5ARContextDefect_mem W steps⟩

theorem nativeK5ASPhysicalDefect_boundary
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5ASPeifferBoundary W (nativeK5ASPhysicalDefect W steps) =
      nativeK5ARWordDefect W
        (nativeK5AQLeft W steps) (nativeK5AQRight W steps) := rfl

/-- A TRUE source-dependent fourteen-cell left whiskering preserves
the original physical Peiffer boundary. -/
theorem nativeK5ASPhysicalDefect_left
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5ASPeifferBoundary W
      (nativeK5ASPhysicalDefect W (true :: steps)) =
    nativeK5ASPeifferBoundary W (nativeK5ASPhysicalDefect W steps) := by
  change nativeK5ARWordDefect W
      (nativeK5AQWhiskerLeft W (nativeK5AQLeft W steps))
      (nativeK5AQWhiskerLeft W (nativeK5AQRight W steps)) =
    nativeK5ARWordDefect W
      (nativeK5AQLeft W steps) (nativeK5AQRight W steps)
  exact nativeK5ARWordDefect_left W _ _

/-- RIGHT whiskering is exactly the group-level Peiffer action by the
inverse of the ACTUAL right-end fourteen-cell frame; no abelianization. -/
theorem nativeK5ASPhysicalDefect_right
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5ASPeifferBoundary W
      (nativeK5ASPeifferAct W
        (nativeK5AQRightFrame W).historyWord⁻¹
        (nativeK5ASPhysicalDefect W steps)) =
      nativeK5ASPeifferBoundary W
        (nativeK5ASPhysicalDefect W (false :: steps)) := by
  change (nativeK5AQRightFrame W).historyWord⁻¹ *
      nativeK5ARWordDefect W
        (nativeK5AQLeft W steps) (nativeK5AQRight W steps) *
          ((nativeK5AQRightFrame W).historyWord⁻¹)⁻¹ =
    nativeK5ARWordDefect W
      (nativeK5AQWhiskerRight W (nativeK5AQLeft W steps))
      (nativeK5AQWhiskerRight W (nativeK5AQRight W steps))
  rw [inv_inv]
  exact (nativeK5ARWordDefect_right W _ _).symm

/-- The right-whiskering comparison already holds IN the Peiffer
MODULE, not merely after applying the boundary: its inclusion is faithful. -/
theorem nativeK5ASPhysicalDefect_right_in_kernel
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5ASPeifferAct W (nativeK5AQRightFrame W).historyWord⁻¹
      (nativeK5ASPhysicalDefect W steps) =
    nativeK5ASPhysicalDefect W (false :: steps) := by
  apply Subtype.ext
  exact nativeK5ASPhysicalDefect_right W steps

/-- A strict-algebraic Peiffer equation for two DIFFERENT original
indexed physical 15D exchange relators (without a claimed 16D filler). -/
theorem nativeK5ASPhysicalPeiffer
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool) :
    nativeK5ASPeifferAct W
      (nativeK5ASPeifferBoundary W (nativeK5ASPhysicalDefect W xs))
      (nativeK5ASPhysicalDefect W ys) =
    nativeK5ASPhysicalDefect W xs *
      nativeK5ASPhysicalDefect W ys *
        (nativeK5ASPhysicalDefect W xs)⁻¹ :=
  nativeK5ASPeiffer_identity W _ _

/-- Faithful inclusion of the physical Peiffer relation module. -/
theorem nativeK5ASPeifferBoundary_injective
    (W : NativeK5StructuralThirteenCell p U V) :
    Function.Injective (nativeK5ASPeifferBoundary W) := by
  intro z t h
  exact Subtype.ext h

/-- The image of the Peiffer module IS the exact context-generated
normal subgroup, not a conjectural complete geometric higher cell. -/
theorem nativeK5ASPeifferBoundary_range
    (W : NativeK5StructuralThirteenCell p U V) :
    (nativeK5ASPeifferBoundary W).range = nativeK5ARHistoryKernel W := by
  change (nativeK5ARHistoryKernel W).subtype.range =
    nativeK5ARHistoryKernel W
  exact Subgroup.range_subtype _

/-- Exactness at the original NONCOMMUTATIVE free history group:
the quotient kills precisely the image of the physical normal kernel. -/
theorem nativeK5AS_exact_at_history
    (W : NativeK5StructuralThirteenCell p U V) :
    (nativeK5ASPeifferBoundary W).range =
      (nativeK5ARWordClass W).ker := by
  rw [nativeK5ASPeifferBoundary_range]
  exact (QuotientGroup.ker_mk' (nativeK5ARHistoryKernel W)).symm

/-- The quotient map onto the corrected gauge group is surjective,
providing a short exact sequence of groups at the purely algebraic
shadow, not a strict n-category statement. -/
theorem nativeK5AS_quoti_surjective
    (W : NativeK5StructuralThirteenCell p U V) :
    Function.Surjective (nativeK5ARWordClass W) :=
  QuotientGroup.mk'_surjective _

/-- The physical base Peiffer relation is genuinely nontrivial
BEFORE quotienting, because its original free-history words differ. -/
theorem nativeK5ASPhysicalDefect_base_ne_one
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5ASPhysicalDefect W [] ≠ 1 := by
  intro heq
  have hword :
      (nativeK5FifteenCriticalLeft W).historyWord⁻¹ *
        (nativeK5FifteenCriticalRight W).historyWord = 1 := by
    have h := congrArg (nativeK5ASPeifferBoundary W) heq
    simpa only [nativeK5ASPhysicalDefect_boundary,
      nativeK5ASPhysicalDefect, nativeK5ASPeifferBoundary,
      nativeK5ARWordDefect] using h
  have heqWord :
      (nativeK5FifteenCriticalLeft W).historyWord =
        (nativeK5FifteenCriticalRight W).historyWord := by
    calc
      (nativeK5FifteenCriticalLeft W).historyWord =
          (nativeK5FifteenCriticalLeft W).historyWord *
            ((nativeK5FifteenCriticalLeft W).historyWord⁻¹ *
              (nativeK5FifteenCriticalRight W).historyWord) := by
                rw [hword, mul_one]
      _ = (nativeK5FifteenCriticalRight W).historyWord := by group
  exact nativeK5FourteenSquareExchange_pastingWord_ne W heqWord

/-- The minimal normal context kernel is precisely the obstruction
for an arbitrary GROUP-VALUED history receiver. The original C60
critical pair is sufficient; no need to assume infinitely many
independent scalar equalities. -/
theorem nativeK5ASGroupHistoryDescent_iff
    (W : NativeK5StructuralThirteenCell p U V)
    {G : Type uG} [Group G]
    (f : NativeK5FourteenHistoryWord →* G) :
    (∃ F : NativeK5AQClasses W → G,
      ∀ R : NativeK5FifteenFourteenFiber W,
        F (nativeK5AQClass W R) = f R.historyWord) ↔
      f (nativeK5FifteenCriticalLeft W).historyWord =
        f (nativeK5FifteenCriticalRight W).historyWord := by
  constructor
  · rintro ⟨F, hf⟩
    calc
      f (nativeK5FifteenCriticalLeft W).historyWord =
          F (nativeK5AQClass W (nativeK5FifteenCriticalLeft W)) :=
            (hf _).symm
      _ = F (nativeK5AQClass W (nativeK5FifteenCriticalRight W)) :=
        congrArg F (nativeK5AQ_exchange_eq W [])
      _ = f (nativeK5FifteenCriticalRight W).historyWord := hf _
  · intro hbase
    have hk : nativeK5ARHistoryKernel W ≤ f.ker := by
      rw [nativeK5ARHistoryKernel_eq_base W]
      unfold nativeK5ARBaseKernel
      apply Subgroup.normalClosure_le_normal
      intro z hz
      have heq : z =
          nativeK5ARWordDefect W
            (nativeK5FifteenCriticalLeft W)
            (nativeK5FifteenCriticalRight W) := by
        simpa [nativeK5ARBaseRelators] using hz
      rw [heq]
      change f ((nativeK5FifteenCriticalLeft W).historyWord⁻¹ *
        (nativeK5FifteenCriticalRight W).historyWord) = 1
      rw [map_mul, map_inv, hbase, inv_mul_cancel]
    let lift : NativeK5ARHistoryQuotient W →* G :=
      QuotientGroup.lift (nativeK5ARHistoryKernel W) f hk
    refine ⟨fun q => lift (nativeK5ARGaugeHistory W q), ?_⟩
    intro R
    change lift (nativeK5ARWordClass W R.historyWord) = f R.historyWord
    exact QuotientGroup.lift_mk' (nativeK5ARHistoryKernel W) hk R.historyWord

/-- The strongest exact conditional P92B-style receiver criterion
available without an ACTUAL old-P92B-to-new-15D typed functor:
for group-valued history observers, nonidentification of the
TRUE raw critical pair is an obstruction to any AQ descent. -/
theorem nativeK5ASGroupHistory_noDescent
    (W : NativeK5StructuralThirteenCell p U V)
    {G : Type uG} [Group G]
    (f : NativeK5FourteenHistoryWord →* G)
    (hsep : f (nativeK5FifteenCriticalLeft W).historyWord ≠
      f (nativeK5FifteenCriticalRight W).historyWord) :
    ¬ ∃ F : NativeK5AQClasses W → G,
      ∀ R : NativeK5FifteenFourteenFiber W,
        F (nativeK5AQClass W R) = f R.historyWord := by
  intro h
  exact hsep ((nativeK5ASGroupHistoryDescent_iff W f).mp h)

end OriginalFourteenFiber

#print axioms NativeK5ASPeifferKernel
#print axioms nativeK5ASPeifferBoundary
#print axioms nativeK5ASPeifferAct
#print axioms nativeK5ASPeifferAct_one
#print axioms nativeK5ASPeifferAct_mul
#print axioms nativeK5ASPeifferAct_identity
#print axioms nativeK5ASPeifferAct_comp
#print axioms nativeK5ASPeifferBoundary_equivariant
#print axioms nativeK5ASPeiffer_identity
#print axioms NativeK5ASCrossedModuleData
#print axioms nativeK5ASCrossedModule
#print axioms nativeK5ASPhysicalDefect
#print axioms nativeK5ASPhysicalDefect_boundary
#print axioms nativeK5ASPhysicalDefect_left
#print axioms nativeK5ASPhysicalDefect_right
#print axioms nativeK5ASPhysicalDefect_right_in_kernel
#print axioms nativeK5ASPhysicalPeiffer
#print axioms nativeK5ASPeifferBoundary_injective
#print axioms nativeK5ASPeifferBoundary_range
#print axioms nativeK5AS_exact_at_history
#print axioms nativeK5AS_quoti_surjective
#print axioms nativeK5ASPhysicalDefect_base_ne_one
#print axioms nativeK5ASGroupHistoryDescent_iff
#print axioms nativeK5ASGroupHistory_noDescent

end
end Kuu.F112.Physical
