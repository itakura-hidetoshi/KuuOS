import Kuu.F112.PolygonNativeC60AQFullPentagonAlternativeFullFaithfulness

/-!
# F112-P94D3FN — typed old/new AQ comparison, higher non-recovery

FJ proves that the ORIGINAL selected 15D physical whiskering collapses
different original conservative refl and atom proofs, forcing actual
17D context and noncommutative 18D free transport nonfaithfulness for
every nonempty AQ word. FK introduces a SEPARATE constructor-preserving
proof transport on exactly the same physical 14D endpoints, FL proves
faithfulness on every dependent Hom, and FM proves faithfulness on the
new actual 15D Total, 17D raw16D contexts, all original 18D full codes
and the corresponding original NONCOMMUTATIVE free group for every
finite word.

FN makes the comparison precise, rather than identifying two different
relative higher signatures:
* On SAME-boundary 15D proof-bearing Total, OLD = syntax-forget ∘ NEW
  for all singleton contexts, and all NONEMPTY finite contexts.
* The forgetting square is natural for ALL finite words when the input
  is first forgotten. The empty-word case is not falsely asserted to
  factor the identity through a noninjective forgetting function.
* The same genuine original lower 15D refl/atom pair determines SEPARATE
  (not definitionally identified) old and new 17D identity objects.
  Their old images agree at EVERY nonempty physical context; their new
  images remain different for EVERY finite context.
* Transported genuine original 18D reflexive-associator FULL codes
  similarly collide in the old receiver and stay distinct in the
  alternative receiver. Hence there is NO global postprocessor from
  old receiving complete codes to new receiving complete codes
  compatible even with these two selected codes.
* Explicit signed two-letter FreeGroup defects are different typed
  presentations: old nonidentity is killed for every nonempty context,
  new nonidentity survives for every finite context.

None of this asserts a canonical functor between ALL old/new 17D
generator signatures, geometric 19D Type-valued filling, a complete
normal presentation for the old kernel, global strict n-categories or
(∞,3)-hyperdescent. FJ no-go, DS, historical proofs, 107 public roots,
strict Kuu primary and independent Kuu as a presentation survive.
No Gray, new axioms, sorry or admit. Apache-2.0.
Copyright 板倉英俊 / Hidetoshi Itakura.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section OldNewTypedPhysicalComparison

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

/-- Conservative-core syntactic forgetting is idempotent on the
FULL ORIGINAL dependent 15D proof grammar, including exchange and
every signed outer composite. This is not an equality of raw proofs
prior to applying the explicitly defined forgetting function. -/
theorem nativeK5FNForgetCell_idempotent
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeK5AQFifteenCell W R S) :
    nativeK5FKForgetConservativeCell W
      (nativeK5FKForgetConservativeCell W h) =
        nativeK5FKForgetConservativeCell W h := by
  induction h with
  | conservative _ => rfl
  | exchange _ => rfl
  | symm h ih =>
      change NativeFifteenFamilyCell.symm
        (nativeK5FKForgetConservativeCell W
          (nativeK5FKForgetConservativeCell W h)) =
        NativeFifteenFamilyCell.symm
          (nativeK5FKForgetConservativeCell W h)
      rw [ih]
  | trans h j ih ij =>
      change NativeFifteenFamilyCell.trans
        (nativeK5FKForgetConservativeCell W
          (nativeK5FKForgetConservativeCell W h))
        (nativeK5FKForgetConservativeCell W
          (nativeK5FKForgetConservativeCell W j)) =
        NativeFifteenFamilyCell.trans
          (nativeK5FKForgetConservativeCell W h)
          (nativeK5FKForgetConservativeCell W j)
      rw [ih, ij]

/-- The OLD physical AQ whiskering already forgets all internal
conservative constructor histories, so pre-forgetting changes no
old transported 15D proof (for every exact dependent boundary). -/
theorem nativeK5FNOldWhisker_forget_invariant
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeK5AQFifteenCell W R S) :
    nativeK5AQWhiskerCell W side
      (nativeK5FKForgetConservativeCell W h) =
        nativeK5AQWhiskerCell W side h := by
  induction h with
  | conservative _ => rfl
  | exchange _ => rfl
  | symm h ih =>
      change NativeFifteenFamilyCell.symm
        (nativeK5AQWhiskerCell W side
          (nativeK5FKForgetConservativeCell W h)) =
        NativeFifteenFamilyCell.symm (nativeK5AQWhiskerCell W side h)
      rw [ih]
  | trans h j ih ij =>
      change NativeFifteenFamilyCell.trans
        (nativeK5AQWhiskerCell W side
          (nativeK5FKForgetConservativeCell W h))
        (nativeK5AQWhiskerCell W side
          (nativeK5FKForgetConservativeCell W j)) =
        NativeFifteenFamilyCell.trans
          (nativeK5AQWhiskerCell W side h)
          (nativeK5AQWhiskerCell W side j)
      rw [ih, ij]

/-- Explicit Type-valued forgetting on complete proof-bearing
physical AX Total. It preserves BOTH original 14D endpoints
and only changes the internal conservative 15D proof constructor. -/
def nativeK5FNForgetBaseTotal
    (W : NativeK5StructuralThirteenCell p U V) :
    (nativeK5AXBaseLayer W).Total → (nativeK5AXBaseLayer W).Total :=
  fun z => ⟨z.1, ⟨nativeK5FKForgetConservativeCell W z.2.down⟩⟩

theorem nativeK5FNForgetBaseTotal_pack
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeK5AQFifteenCell W R S) :
    nativeK5FNForgetBaseTotal W (nativeK5AXPack W h) =
      nativeK5AXPack W (nativeK5FKForgetConservativeCell W h) := rfl

theorem nativeK5FNForgetBaseTotal_idempotent
    (W : NativeK5StructuralThirteenCell p U V)
    (z : (nativeK5AXBaseLayer W).Total) :
    nativeK5FNForgetBaseTotal W (nativeK5FNForgetBaseTotal W z) =
      nativeK5FNForgetBaseTotal W z := by
  rcases z with ⟨⟨a, b⟩, h⟩
  change
    (⟨(a, b), ULift.up (nativeK5FKForgetConservativeCell W
      (nativeK5FKForgetConservativeCell W h.down))⟩ :
      (nativeK5AXBaseLayer W).Total) =
    ⟨(a, b), ULift.up (nativeK5FKForgetConservativeCell W h.down)⟩
  exact congrArg (fun v : NativeK5AQFifteenCell W a.down b.down =>
    (⟨(a, b), ULift.up v⟩ : (nativeK5AXBaseLayer W).Total))
      (nativeK5FNForgetCell_idempotent W h.down)

/-- First honest commuting square on full, dependent physical 15D:
the old frame factors through new frame followed by FULL source/target
preserving constructor-history forgetting. This is FK's theorem
lifted to genuine proof-bearing AX Total, not a quotient or observer. -/
theorem nativeK5FNOldFrame_factors_through_new
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool)
    (z : (nativeK5AXBaseLayer W).Total) :
    (nativeK5BCFrame W side).mapTotal z =
      nativeK5FNForgetBaseTotal W
        ((nativeK5FKBCFrame W side).mapTotal z) := by
  rcases z with ⟨⟨a, b⟩, h⟩
  change nativeK5AXPack W
      (nativeK5AQWhiskerCell W side h.down) =
    nativeK5AXPack W
      (nativeK5FKForgetConservativeCell W
        (nativeK5FKWhiskerCell W side h.down))
  exact congrArg (nativeK5AXPack W)
    (nativeK5FKOriginalWhisker_factors_through_alternative W side h.down)

/-- The old full frame does not distinguish an input from its
forgotten conservative history. In particular this is NOT an
assertion that forgetting itself is injective. -/
theorem nativeK5FNOldFrame_forget_invariant
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool)
    (z : (nativeK5AXBaseLayer W).Total) :
    (nativeK5BCFrame W side).mapTotal (nativeK5FNForgetBaseTotal W z) =
      (nativeK5BCFrame W side).mapTotal z := by
  rcases z with ⟨⟨a, b⟩, h⟩
  change nativeK5AXPack W
      (nativeK5AQWhiskerCell W side
        (nativeK5FKForgetConservativeCell W h.down)) =
    nativeK5AXPack W (nativeK5AQWhiskerCell W side h.down)
  exact congrArg (nativeK5AXPack W)
    (nativeK5FNOldWhisker_forget_invariant W side h.down)

/-- ALL one-letter AQ squares commute with forgetting on the SOURCE:
old ∘ forget = forget ∘ new. -/
theorem nativeK5FNFrame_forget_naturality
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool)
    (z : (nativeK5AXBaseLayer W).Total) :
    (nativeK5BCFrame W side).mapTotal (nativeK5FNForgetBaseTotal W z) =
      nativeK5FNForgetBaseTotal W
        ((nativeK5FKBCFrame W side).mapTotal z) := by
  calc
    _ = (nativeK5BCFrame W side).mapTotal z :=
      nativeK5FNOldFrame_forget_invariant W side z
    _ = nativeK5FNForgetBaseTotal W
          ((nativeK5FKBCFrame W side).mapTotal z) :=
      nativeK5FNOldFrame_factors_through_new W side z

/-- All finite original/new 15D contexts commute with the lower
constructor forgetful map. At EMPTY context both sides are exactly
forget z, not an artificial assertion forget = identity. -/
theorem nativeK5FNContext_forget_naturality
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (z : (nativeK5AXBaseLayer W).Total) :
    nativeC60BCContextTotal (nativeK5BCFrame W) word
        (nativeK5FNForgetBaseTotal W z) =
      nativeK5FNForgetBaseTotal W
        (nativeC60BCContextTotal (nativeK5FKBCFrame W) word z) := by
  induction word with
  | nil => rfl
  | cons side rest ih =>
      change (nativeK5BCFrame W side).mapTotal
          (nativeC60BCContextTotal (nativeK5BCFrame W) rest
            (nativeK5FNForgetBaseTotal W z)) =
        nativeK5FNForgetBaseTotal W
          ((nativeK5FKBCFrame W side).mapTotal
            (nativeC60BCContextTotal (nativeK5FKBCFrame W) rest z))
      rw [ih]
      exact nativeK5FNFrame_forget_naturality W side _

/-- For EVERY NONEMPTY finite AQ word, the ORIGINAL full 15D
proof-bearing transport factors as forgetting AFTER the alternative
constructor-preserving word transport, with the same original typed
source. This deliberately EXCLUDES empty word, where old=new=id
and forgetting remains noninjective. -/
theorem nativeK5FNOriginalContext_factors_nonempty
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (hne : word ≠ [])
    (z : (nativeK5AXBaseLayer W).Total) :
    nativeC60BCContextTotal (nativeK5BCFrame W) word z =
      nativeK5FNForgetBaseTotal W
        (nativeC60BCContextTotal (nativeK5FKBCFrame W) word z) := by
  revert hne
  induction word with
  | nil =>
      intro hne
      exact (hne rfl).elim
  | cons side rest ih =>
      intro _
      cases rest with
      | nil =>
          change (nativeK5BCFrame W side).mapTotal z =
            nativeK5FNForgetBaseTotal W
              ((nativeK5FKBCFrame W side).mapTotal z)
          exact nativeK5FNOldFrame_factors_through_new W side z
      | cons next tail =>
          change (nativeK5BCFrame W side).mapTotal
              (nativeC60BCContextTotal (nativeK5BCFrame W)
                (next :: tail) z) =
            nativeK5FNForgetBaseTotal W
              ((nativeK5FKBCFrame W side).mapTotal
                (nativeC60BCContextTotal (nativeK5FKBCFrame W)
                  (next :: tail) z))
          rw [ih (by simp)]
          exact nativeK5FNFrame_forget_naturality W side _

/-- The explicitly defined total forgetter is NOT injective,
already on the identical original 14D endpoint and the TWO genuinely
different FJ conservative 15D proof constructors. -/
theorem nativeK5FNForgetBaseTotal_not_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    ¬ Function.Injective (nativeK5FNForgetBaseTotal W) := by
  intro hinj
  apply nativeK5FJBaseRefl_ne_atom W R
  apply hinj
  rfl

/-- Canonical 17D IDENTITY object in the new relative presentation,
over the SAME original 15D refl certificate used by FJ. The raw16D
refl constructor is genuine but the old/new 17D TYPES are distinct. -/
def nativeK5FNNewSeventeenRefl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    (nativeC60DQSeventeenLayer (nativeK5AXKuuSignature W)
      (nativeK5FKBCFrame W)).Total :=
  ⟨(nativeK5FJBaseRefl W R, nativeK5FJBaseRefl W R),
    .refl (nativeK5FJBaseRefl W R)⟩

def nativeK5FNNewSeventeenAtom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    (nativeC60DQSeventeenLayer (nativeK5AXKuuSignature W)
      (nativeK5FKBCFrame W)).Total :=
  ⟨(nativeK5FJBaseAtom W R, nativeK5FJBaseAtom W R),
    .refl (nativeK5FJBaseAtom W R)⟩

/-- Independent newly selected Type-valued 17D identity objects
retain the SAME original distinct lower 15D proof constructors. -/
theorem nativeK5FNNewSeventeenRefl_ne_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5FNNewSeventeenRefl W R ≠
      nativeK5FNNewSeventeenAtom W R := by
  intro heq
  exact nativeK5FJBaseRefl_ne_atom W R
    (congrArg
      (fun t : (nativeC60DQSeventeenLayer (nativeK5AXKuuSignature W)
        (nativeK5FKBCFrame W)).Total => t.1.1) heq)

/-- NO finite context erases this genuinely 17D proof-bearing
alternative pair: the complete contextual 17D object action is
injective by FM, even for nonempty words. -/
theorem nativeK5FNNewSeventeenContext_separates
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame (nativeK5AXKuuSignature W)
        (nativeK5FKBCFrame W)) word
        (nativeK5FNNewSeventeenRefl W R) ≠
    nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame (nativeK5AXKuuSignature W)
        (nativeK5FKBCFrame W)) word
        (nativeK5FNNewSeventeenAtom W R) := by
  intro heq
  exact (nativeK5FNNewSeventeenRefl_ne_atom W R)
    ((nativeK5FMAllSeventeenContexts_injective W word) heq)

/-- 17D selection comparison WITHOUT identifying distinct signatures:
the genuine old typed identity pair COLLIDES for every nonempty word,
but the new typed identity pair, on the same original 15D lower proofs,
remains distinct at every word. -/
theorem nativeK5FNSeventeenOldNew_contrast
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (hne : word ≠ []) :
    (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)) word (nativeK5FJSeventeenRefl W R) =
     nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)) word (nativeK5FJSeventeenAtom W R)) ∧
    (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame (nativeK5AXKuuSignature W)
        (nativeK5FKBCFrame W)) word
        (nativeK5FNNewSeventeenRefl W R) ≠
     nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame (nativeK5AXKuuSignature W)
        (nativeK5FKBCFrame W)) word
        (nativeK5FNNewSeventeenAtom W R)) :=
  ⟨nativeK5FJPhysical_nonempty_context_collision W R word hne,
    nativeK5FNNewSeventeenContext_separates W R word⟩

/-- The SAME selected original lower proof pair gives two distinct
typed 18D assoc-refl code pairs. At each nonempty word the old
receiving COMPLETE CODE identifies its pair, by the real FJ 17D
collision (not an assumed 19D filler). -/
theorem nativeK5FNOldEighteenAssocReflCode_collision
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (hne : word ≠ []) :
    nativeC60DVTransportCompleteCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) (nativeK5FJSeventeenRefl W R)) =
      nativeC60DVTransportCompleteCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) (nativeK5FJSeventeenAtom W R)) :=
  (nativeC60FEAssocReflCode_collision_iff
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word
      (nativeK5FJSeventeenRefl W R) (nativeK5FJSeventeenAtom W R)).mpr
    (nativeK5FJPhysical_nonempty_context_collision W R word hne)

/-- The NEW receiving complete 18D code DOES NOT collapse the
parallel pair, for any finite word. This uses the exact Type-valued
17D context and FI/FE reflection, not scalar or abelian observations. -/
theorem nativeK5FNNewEighteenAssocReflCode_separates
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    nativeC60DVTransportCompleteCode
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5FKBCFrame W) (nativeK5FNNewSeventeenRefl W R)) ≠
      nativeC60DVTransportCompleteCode
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5FKBCFrame W) (nativeK5FNNewSeventeenAtom W R)) := by
  intro heq
  exact nativeK5FNNewSeventeenContext_separates W R word
    ((nativeC60FEAssocReflCode_collision_iff
      (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word
      (nativeK5FNNewSeventeenRefl W R)
      (nativeK5FNNewSeventeenAtom W R)).mp heq)

/-- Even a completely arbitrary function between DIFFERENT old/new
18D receiving code TYPES cannot postprocess the old output to both
selected new outputs at a nonempty context. No claim is made that
every possible higher signature admits such a function. -/
theorem nativeK5FNNoNewEighteenRecovery_from_old
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (hne : word ≠ [])
    (decode : NativeC60DVCompleteEighteenCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) →
      NativeC60DVCompleteEighteenCode
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W)) :
    ¬ (
      (decode (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) (nativeK5FJSeventeenRefl W R))) =
        nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5FKBCFrame W) (nativeK5FNNewSeventeenRefl W R))) ∧
      (decode (nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) (nativeK5FJSeventeenAtom W R))) =
        nativeC60DVTransportCompleteCode
          (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5FKBCFrame W) (nativeK5FNNewSeventeenAtom W R)))) := by
  rintro ⟨hrefl, hatom⟩
  apply nativeK5FNNewEighteenAssocReflCode_separates W R word
  calc
    _ = decode (nativeC60DVTransportCompleteCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) (nativeK5FJSeventeenRefl W R))) := hrefl.symm
    _ = decode (nativeC60DVTransportCompleteCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word
          (nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) (nativeK5FJSeventeenAtom W R))) :=
      congrArg decode (nativeK5FNOldEighteenAssocReflCode_collision
        W R word hne)
    _ = _ := hatom

/-- NEW ORIGINAL free-group signed two-letter defect between the
corresponding two fully dependent alternative 18D assoc-refl codes.
This is a different well-typed source FreeGroup from FJ's old one;
it is not an arbitrary transport of the old defect. -/
def nativeK5FNNewUniversalDefect
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeC60DTFullFree (nativeK5AXKuuSignature W)
      (nativeK5FKBCFrame W) :=
  nativeC60FCCodeFiberDefect
    (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W)
    (nativeC60FDAssocReflCode
      (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W)
      (nativeK5FNNewSeventeenRefl W R))
    (nativeC60FDAssocReflCode
      (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W)
      (nativeK5FNNewSeventeenAtom W R))

/-- A genuinely NONTRIVIAL new signed two-letter source word,
but its image is NONTRIVIAL under EVERY finite new noncommutative
DV transport, including both nonempty and empty contexts. -/
theorem nativeK5FNNewUniversalDefect_all_survive
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5FNNewUniversalDefect W R ≠ 1 ∧
      ∀ word : List Bool,
        (nativeC60DVFullWordTransport (nativeK5AXKuuSignature W)
            (nativeK5FKBCFrame W) word)
          (nativeK5FNNewUniversalDefect W R) ≠ 1 := by
  have hcodes :
      nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
        (nativeK5FKBCFrame W) (nativeK5FNNewSeventeenRefl W R) ≠
      nativeC60FDAssocReflCode (nativeK5AXKuuSignature W)
        (nativeK5FKBCFrame W) (nativeK5FNNewSeventeenAtom W R) := by
    intro h
    exact nativeK5FNNewSeventeenRefl_ne_atom W R
      (nativeC60FDAssocReflCode_injective
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) h)
  have hne : nativeK5FNNewUniversalDefect W R ≠ 1 :=
    nativeC60FCCodeFiberDefect_ne_one
      (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) hcodes
  constructor
  · exact hne
  · intro word himg
    exact hne (nativeK5FMFullFree_kernel_trivial W word
      (nativeK5FNNewUniversalDefect W R) himg)

/-- Exact old/new NONCOMMUTATIVE defect contrast for each nonempty
genuine physical AQ word. Both source elements are nonidentity;
old maps its element to one, the new map retains its independent
nonidentity element. Their ambient original free groups are NOT
definitionally the same. No normal-kernel classification is inferred. -/
theorem nativeK5FNOldNewUniversalDefect_contrast
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (hne : word ≠ []) :
    nativeK5FJPhysicalUniversalDefect W R ≠ 1 ∧
      (nativeC60DVFullWordTransport (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) word)
          (nativeK5FJPhysicalUniversalDefect W R) = 1 ∧
      nativeK5FNNewUniversalDefect W R ≠ 1 ∧
      (nativeC60DVFullWordTransport (nativeK5AXKuuSignature W)
        (nativeK5FKBCFrame W) word)
          (nativeK5FNNewUniversalDefect W R) ≠ 1 := by
  obtain ⟨hold, hkill⟩ :=
    nativeK5FJPhysicalUniversalDefect_all_nonempty W R
  obtain ⟨hnew, hsurvive⟩ :=
    nativeK5FNNewUniversalDefect_all_survive W R
  exact ⟨hold, hkill word hne, hnew, hsurvive word⟩

end OldNewTypedPhysicalComparison

#print axioms nativeK5FNForgetCell_idempotent
#print axioms nativeK5FNOldWhisker_forget_invariant
#print axioms nativeK5FNForgetBaseTotal
#print axioms nativeK5FNForgetBaseTotal_idempotent
#print axioms nativeK5FNOldFrame_factors_through_new
#print axioms nativeK5FNOldFrame_forget_invariant
#print axioms nativeK5FNContext_forget_naturality
#print axioms nativeK5FNOriginalContext_factors_nonempty
#print axioms nativeK5FNForgetBaseTotal_not_injective
#print axioms nativeK5FNNewSeventeenRefl_ne_atom
#print axioms nativeK5FNNewSeventeenContext_separates
#print axioms nativeK5FNSeventeenOldNew_contrast
#print axioms nativeK5FNOldEighteenAssocReflCode_collision
#print axioms nativeK5FNNewEighteenAssocReflCode_separates
#print axioms nativeK5FNNoNewEighteenRecovery_from_old
#print axioms nativeK5FNNewUniversalDefect_all_survive
#print axioms nativeK5FNOldNewUniversalDefect_contrast

end
end Kuu.F112.Physical
