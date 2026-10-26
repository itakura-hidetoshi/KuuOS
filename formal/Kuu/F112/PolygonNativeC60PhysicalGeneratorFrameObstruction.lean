import Kuu.F112.PolygonNativeC60ContextualPeifferMiddleFour

/-!
# F112-P94D3BJ — physical singleton-frame gates and nonvanishing Peiffer obstruction

BI reduced genuinely two-variable strict middle-four coherence to
contextual selected replacement under EXPLICIT whiskering hypotheses.
Here the original physical AQ fourteen-cell frames are used directly.

1. Any candidate for original typed binary 16D whiskering must commute
   at the FULL 15D object level with both genuine singleton AQ frames.
   An object-level failure therefore rules out the corresponding BG gate.
2. The original AS noncommutative normal-kernel Peiffer action is faithful
   (conjugation is injective) for EVERY finite AQ context, not just two
   scalar test cases.
3. The actual nontrivial source-dependent Peiffer relator cannot be
   trivialized by ANY finite word in the two original fourteen-cell frames.
   The true left letter fixes it; the false right letter conjugates it
   by the inverse of the actual right-frame history word.
4. Peiffer receiver equality is reflected AND preserved under all actual
   finite contexts. This is a GROUP-level fact, NOT raw 16D equality.
5. Any candidate H failing a physically computed Peiffer-compatibility
   equation fails the corresponding full typed BG singleton gate.

This is a genuine nonvanishing/no-trivialization result in the physical
nonabelian crossed-module receiver. It does NOT by itself forbid
geometric 16-cell fillers or prove/disprove full Peiffer interchange.
No Gray, invented binary whiskering, observer-kernel quotient,
new axioms, sorry or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- The full dependent strict-arrow BG gate forces compatibility of
the binary source object with each finite unary C60 context.
Identity raw comparisons provide actual typed source/target witnesses. -/
theorem nativeC60BJObjectGate_of_equivariant {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (word : List Bool)
    (he : NativeC60BGWhiskeringEquivariant S F H word)
    (a c : L.Total) :
    nativeC60BCContextTotal F word (H.obj a c) =
      H.obj (nativeC60BCContextTotal F word a)
        (nativeC60BCContextTotal F word c) := by
  have h := he.rl
    (⟨(a, a), NativeC60AXStep.refl a⟩ : NativeC60BGRawArrowBundle S F)
    (⟨(c, c), NativeC60AXStep.refl c⟩ : NativeC60BGRawArrowBundle S F)
  exact congrArg (fun z : NativeC60BEStrictArrowBundle S F => z.1.1) h

/-- Failure of source-object compatibility at even ONE actual pair
obstructs the full two-sided whiskering gate for that frame. -/
theorem nativeC60BJObjectMismatch_no_gate {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (word : List Bool) (a c : L.Total)
    (hne : nativeC60BCContextTotal F word (H.obj a c) ≠
      H.obj (nativeC60BCContextTotal F word a)
        (nativeC60BCContextTotal F word c)) :
    ¬ NativeC60BGWhiskeringEquivariant S F H word := by
  intro he
  exact hne (nativeC60BJObjectGate_of_equivariant S F H word he a c)

section OriginalPhysicalC60

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

/-- Actual AS Peiffer conjugation is an injective map of the original
noncommutative normal kernel for any genuine frame history word.
This reflects equality, not merely preserving it. -/
theorem nativeK5BJPeifferAct_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (g : NativeK5FourteenHistoryWord) :
    Function.Injective (nativeK5ASPeifferAct W g) := by
  intro z t h
  apply Subtype.ext
  have hw : g * (z : NativeK5FourteenHistoryWord) * g⁻¹ =
      g * (t : NativeK5FourteenHistoryWord) * g⁻¹ :=
    congrArg (nativeK5ASPeifferBoundary W) h
  exact mul_left_cancel (mul_right_cancel hw)

/-- Conjugating a nontrivial physical Peiffer-kernel value cannot
make it the neutral element, for any original frame word. -/
theorem nativeK5BJPeifferAct_ne_one
    (W : NativeK5StructuralThirteenCell p U V)
    (g : NativeK5FourteenHistoryWord)
    (z : NativeK5ASPeifferKernel W) (hz : z ≠ 1) :
    nativeK5ASPeifferAct W g z ≠ 1 := by
  intro h
  apply hz
  apply nativeK5BJPeifferAct_injective W g
  exact h.trans (nativeK5ASPeifferAct_one W g).symm

/-- In the ACTUAL original C60 fourteen-cell geometry, a true/left
singleton fixes the full physical Peiffer element, not only its charge. -/
theorem nativeK5BJPhysicalDefect_left
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5ASPhysicalDefect W [true] =
      nativeK5ASPhysicalDefect W [] := by
  apply nativeK5ASPeifferBoundary_injective W
  exact nativeK5ASPhysicalDefect_left W []

/-- A false/right singleton conjugates the full physical Peiffer
element by the inverse right boundary history, with order preserved. -/
theorem nativeK5BJPhysicalDefect_right
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5ASPhysicalDefect W [false] =
      nativeK5ASPeifferAct W (nativeK5AQRightFrame W).historyWord⁻¹
        (nativeK5ASPhysicalDefect W []) :=
  (nativeK5ASPhysicalDefect_right_in_kernel W []).symm

/-- FULL finite-context nonvanishing, not just nonvanishing after
either of the two elementary original fourteen-cell whiskerings.
This is the exact physical crossed-module-level no-trivialization. -/
theorem nativeK5BJPhysicalDefect_context_ne_one
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    nativeK5ASPhysicalDefect W word ≠ 1 := by
  rw [nativeK5ATPhysicalDefect_context W word]
  exact nativeK5BJPeifferAct_ne_one W
    (nativeK5ATGaugeWord W word)
    (nativeK5ASPhysicalDefect W [])
    (nativeK5ASPhysicalDefect_base_ne_one W)

/-- Both physically supplied singleton frames carry a nontrivial
Peiffer relator. No cancellation is inferred from scalar equality. -/
theorem nativeK5BJPhysicalDefect_two_frames_ne_one
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) :
    nativeK5ASPhysicalDefect W [side] ≠ 1 := by
  exact nativeK5BJPhysicalDefect_context_ne_one W [side]

/-- None of the original physical finite context words erases the
noncommutative crossed-module relator. -/
theorem nativeK5BJPhysicalDefect_no_trivializing_word
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ ∃ word : List Bool, nativeK5ASPhysicalDefect W word = 1 := by
  rintro ⟨word, h⟩
  exact (nativeK5BJPhysicalDefect_context_ne_one W word) h

/-- ACTUAL Peiffer equality is reflected by any finite source-dependent
whiskering word. It must not be confused with reflection of equality
between raw 15D or 16D comparison terms. -/
theorem nativeK5BJPhysicalPeiffer_context_eq_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (a b : (nativeK5AXBaseLayer W).Total) :
    nativeK5AXPeiffer W (nativeK5BCContext W word a) =
      nativeK5AXPeiffer W (nativeK5BCContext W word b) ↔
    nativeK5AXPeiffer W a = nativeK5AXPeiffer W b := by
  rw [nativeK5BCContext_peiffer W word a,
      nativeK5BCContext_peiffer W word b]
  constructor
  · exact nativeK5BJPeifferAct_injective W (nativeK5ATGaugeWord W word)
  · intro h
    exact congrArg (nativeK5ASPeifferAct W (nativeK5ATGaugeWord W word)) h

/-- Any new two-variable strict-whiskering candidate satisfying the
full BG frame gate MUST satisfy this equation in the ACTUAL original
noncommutative physical Peiffer kernel.  This is a necessary filter,
not a construction of a geometric sixteen-cell. -/
theorem nativeK5BJPhysicalPeifferGate_necessary
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (side : Bool)
    (he : NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [side])
    (a c : (nativeK5AXBaseLayer W).Total) :
    nativeK5ASPeifferAct W (nativeK5ATGaugeWord W [side])
        (nativeK5AXPeiffer W (Hh.obj a c)) =
      nativeK5AXPeiffer W
        (Hh.obj (nativeK5BCContext W [side] a)
          (nativeK5BCContext W [side] c)) := by
  calc
    nativeK5ASPeifferAct W (nativeK5ATGaugeWord W [side])
        (nativeK5AXPeiffer W (Hh.obj a c)) =
      nativeK5AXPeiffer W
        (nativeK5BCContext W [side] (Hh.obj a c)) :=
      (nativeK5BCContext_peiffer W [side] (Hh.obj a c)).symm
    _ = nativeK5AXPeiffer W
        (Hh.obj (nativeK5BCContext W [side] a)
          (nativeK5BCContext W [side] c)) :=
      congrArg (nativeK5AXPeiffer W)
        (nativeC60BJObjectGate_of_equivariant
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          Hh [side] he a c)

/-- An actual Peiffer-kernel mismatch at a specified original left/right
singleton is sufficient to rule out BG's full two-sided gate for that
candidate H. No inequality witness is silently assumed. -/
theorem nativeK5BJPhysicalPeifferMismatch_no_frame
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (side : Bool)
    (a c : (nativeK5AXBaseLayer W).Total)
    (hne : nativeK5ASPeifferAct W (nativeK5ATGaugeWord W [side])
        (nativeK5AXPeiffer W (Hh.obj a c)) ≠
      nativeK5AXPeiffer W
        (Hh.obj (nativeK5BCContext W [side] a)
          (nativeK5BCContext W [side] c))) :
    ¬ NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [side] := by
  intro he
  exact hne (nativeK5BJPhysicalPeifferGate_necessary W Hh side he a c)

/-- Scalar/group Peiffer equality of the ACTUAL AU naturality endpoints
survives every AQ context, but their TYPE-VALUED 15D proof terms
remain distinct. Therefore this nonvanishing result is not falsely
promoted to a geometric 16-cell coherence conclusion. -/
theorem nativeK5BJPhysicalNaturality_samePeiffer_distinctRaw
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    nativeK5AXPeiffer W
      (nativeK5BCContext W word
        (nativeK5AXPack W
          (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))) =
      nativeK5AXPeiffer W
        (nativeK5BCContext W word
          (nativeK5AXPack W
            (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])))) ∧
    nativeK5BCContext W word
        (nativeK5AXPack W
          (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W []))) ≠
      nativeK5BCContext W word
        (nativeK5AXPack W
          (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))) := by
  constructor
  · exact nativeK5BCContextualNaturality_peiffer W word
      (nativeK5AQExchange W [])
  · exact nativeK5BCContextualPacked_raw_ne W word

end OriginalPhysicalC60

#print axioms nativeC60BJObjectGate_of_equivariant
#print axioms nativeC60BJObjectMismatch_no_gate
#print axioms nativeK5BJPeifferAct_injective
#print axioms nativeK5BJPeifferAct_ne_one
#print axioms nativeK5BJPhysicalDefect_left
#print axioms nativeK5BJPhysicalDefect_right
#print axioms nativeK5BJPhysicalDefect_context_ne_one
#print axioms nativeK5BJPhysicalDefect_two_frames_ne_one
#print axioms nativeK5BJPhysicalDefect_no_trivializing_word
#print axioms nativeK5BJPhysicalPeiffer_context_eq_iff
#print axioms nativeK5BJPhysicalPeifferGate_necessary
#print axioms nativeK5BJPhysicalPeifferMismatch_no_frame
#print axioms nativeK5BJPhysicalNaturality_samePeiffer_distinctRaw

end
end Kuu.F112.Physical
