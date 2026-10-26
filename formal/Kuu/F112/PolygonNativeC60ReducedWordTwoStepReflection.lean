import Kuu.F112.PolygonNativeC60FreeBridgeAtomicCompleteness
import Mathlib.GroupTheory.FreeGroup.Reduce

/-!
# F112-P94D3BY — reduced signed words and genuine typed two-step completeness

BX constructs a split prefix action and proves strict equality reflection
for individual genuine BC sixteen-dimensional generators. BY extends the
higher free-word calculation in TWO independent directions:

1. For EVERY FINITE signed generator-code word, Mathlib's actual
   FreeGroup reduction (Church-Rosser) yields a unique reduced normal
   form; its equality is exactly free-group equality. A canonical
   reduced trace is attached to EVERY original dependent raw16D term,
   including all inverse and vertical-composition constructors.
2. Arbitrary finite POSITIVE generator-code words have no cancellable
   neighbor; their free-group evaluations are faithful on the entire
   list, without restricting the length to one.
3. Specializing to two independently chosen, genuinely composable
   ORIGINAL typed BC generators g : a => b and h : b => c, equality
   of their transported full strict 16D two-step composite is EXACTLY
   equality of the two original separately supplied generators.
   This is stronger than BX's singleton theorem and applies to
   both genuine false and true AQ frames.

The reduced-word theorem by itself does NOT construct a typed
free-groupoid decoder back to all strict Kuu Hom arrows: such a decoder
has to preserve all original source, target and intermediate 15D
boundaries after signed cancellation. We do NOT infer full typed
faithfulness from mere free-group equality. Mixed signed composites,
original geometric 16-cell coherence, unconditional BG/BH/BI
middle-four and full P92B descent remain open.

No new axiom, sorry, admit, Gray, change of public 107 roots or
alteration of the existing canonical Kuu strict quotient.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Mathlib's Church-Rosser reduction yields UNIQUE fully reduced
representatives of ANY TWO signed words with the SAME free-group
element. No observation is used to redefine Kuu's typed relation. -/
theorem nativeC60BYReducedSignedWord_unique
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (xs ys : List (NativeC60BVGeneratorCode S × Bool))
    (hx : FreeGroup.IsReduced xs) (hy : FreeGroup.IsReduced ys)
    (h : FreeGroup.mk xs = FreeGroup.mk ys) : xs = ys := by
  rcases (FreeGroup.Red.exact).mp h with ⟨z, hxz, hyz⟩
  have h₁ : z = xs := (FreeGroup.IsReduced.red_iff_eq hx).mp hxz
  have h₂ : z = ys := (FreeGroup.IsReduced.red_iff_eq hy).mp hyz
  exact h₁.symm.trans h₂

/-- The signed normal form of the GENUINE whole raw16D evidence,
including all independent typed atoms, reversal and compositions.
Classical decidable equality concerns only normalization of the
original generator-code alphabet, not an axiom of raw equality. -/
noncomputable def nativeC60BYReducedTrace
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    List (NativeC60BVGeneratorCode S × Bool) := by
  classical
  exact (nativeC60BWFreeHolonomy S F c).toWord

/-- Every actual raw16D comparison is mapped to a genuinely REDUCED
signed code word, not a scalar charge, length or Peiffer shadow. -/
theorem nativeC60BYReducedTrace_reduced
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    FreeGroup.IsReduced (nativeC60BYReducedTrace S F c) := by
  classical
  exact FreeGroup.isReduced_toWord

/-- The canonical normal form evaluates back to EXACTLY the original
noncommutative higher-word holonomy, without syntactic inverse
cancellation in the free raw sixteen-dimensional term. -/
theorem nativeC60BYReducedTrace_sound
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    FreeGroup.mk (nativeC60BYReducedTrace S F c) =
      nativeC60BWFreeHolonomy S F c := by
  classical
  exact FreeGroup.mk_toWord

/-- NORMAL-FORM COMPLETENESS at the free GROUP level for arbitrary
genuinely typed signed raw16D comparisons. This does not identify
different strict Hom objects by itself. -/
theorem nativeC60BYReducedTrace_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BYReducedTrace S F c =
        nativeC60BYReducedTrace S F d ↔
      nativeC60BWFreeHolonomy S F c =
        nativeC60BWFreeHolonomy S F d := by
  constructor
  · intro h
    have hh := congrArg FreeGroup.mk h
    rw [nativeC60BYReducedTrace_sound S F c,
      nativeC60BYReducedTrace_sound S F d] at hh
    exact hh
  · intro h
    classical
    exact congrArg FreeGroup.toWord h

/-- Finite actual AQ context actions preserve AND reflect equality
of the canonical REDUCED SIGNED CODE WORD for any original typed
raw16D comparison, including arbitrary inverse/composite terms. -/
theorem nativeC60BYReducedTrace_frame_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BYReducedTrace S F
        (nativeC60BCMapClosedStep S F word c) =
      nativeC60BYReducedTrace S F
        (nativeC60BCMapClosedStep S F word d) ↔
      nativeC60BYReducedTrace S F c =
        nativeC60BYReducedTrace S F d :=
  (nativeC60BYReducedTrace_eq_iff S F _ _).trans
    ((nativeC60BWFreeHolonomy_frame_eq_iff S F word c d).trans
      (nativeC60BYReducedTrace_eq_iff S F c d).symm)

/-- All finite POSITIVE generator-code words, not only singletons,
are already reduced in the actual signed free-word normal form. -/
def nativeC60BYPositiveSigned
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (xs : List (NativeC60BVGeneratorCode S)) :
    List (NativeC60BVGeneratorCode S × Bool) :=
  xs.map (fun code => (code, true))

theorem nativeC60BYPositiveSigned_reduced
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (xs : List (NativeC60BVGeneratorCode S)) :
    FreeGroup.IsReduced (nativeC60BYPositiveSigned S xs) := by
  induction xs with
  | nil =>
      exact FreeGroup.IsReduced.nil
  | cons x xs ih =>
      cases xs with
      | nil =>
          exact FreeGroup.IsReduced.singleton
      | cons y ys =>
          change FreeGroup.IsReduced
            ((x, true) :: (y, true) :: ys.map (fun code => (code, true)))
          rw [FreeGroup.isReduced_cons_cons]
          refine ⟨?_, ?_⟩
          · intro _
            rfl
          · exact ih

/-- Noncommutative free-group evaluation of any positive ordered
finite code list from the FULL original sixteen-dimensional evidence. -/
def nativeC60BYPositiveFreeWord
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (xs : List (NativeC60BVGeneratorCode S)) :
    FreeGroup (NativeC60BVGeneratorCode S) :=
  FreeGroup.mk (nativeC60BYPositiveSigned S xs)

/-- UNBOUNDED finite positive-word completeness: the ordered free
group value is injective on ALL finite lists of complete original
dependent sixteen-dimensional generator certificates. -/
theorem nativeC60BYPositiveFreeWord_injective
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) :
    Function.Injective (nativeC60BYPositiveFreeWord S) := by
  intro xs ys h
  have hs : nativeC60BYPositiveSigned S xs =
      nativeC60BYPositiveSigned S ys :=
    nativeC60BYReducedSignedWord_unique S
      (nativeC60BYPositiveSigned S xs)
      (nativeC60BYPositiveSigned S ys)
      (nativeC60BYPositiveSigned_reduced S xs)
      (nativeC60BYPositiveSigned_reduced S ys) h
  exact (List.map_injective
    (fun (a b : NativeC60BVGeneratorCode S)
      (h : (a, true) = (b, true)) => (Prod.mk.inj h).1)) hs

/-- The fully typed vertical composite of TWO independent genuine
BC primitive 16D generators evaluates to the exact ordered TWO-LETTER
positive free word. The intermediate ORIGINAL 15D object is shared. -/
theorem nativeC60BYTwoAtomic_holonomy
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b)
    (h : (nativeC60BCClosedSignature S F).Gen b c) :
    nativeC60BWFreeHolonomy S F
        (.trans (.atom g) (.atom h)) =
      nativeC60BYPositiveFreeWord S
        [nativeC60BVGeneratorCode S F g,
          nativeC60BVGeneratorCode S F h] := by
  change
    FreeGroup.mk [(nativeC60BVGeneratorCode S F g, true)] *
      FreeGroup.mk [(nativeC60BVGeneratorCode S F h, true)] =
    FreeGroup.mk
      [(nativeC60BVGeneratorCode S F g, true),
       (nativeC60BVGeneratorCode S F h, true)]
  simp only [FreeGroup.mul_mk, List.singleton_append]

/-- TRUE two-input genuine vertical-composite completeness:
for any four original typed BC generators with a common actual
15D intermediate object, free-word equality forces equality of BOTH
separate original generators. Neither term is an observer-constructed
replacement. -/
theorem nativeC60BYTwoAtomic_free_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c : L.Total}
    (g g' : (nativeC60BCClosedSignature S F).Gen a b)
    (h h' : (nativeC60BCClosedSignature S F).Gen b c) :
    nativeC60BWFreeHolonomy S F
        (.trans (.atom g) (.atom h)) =
      nativeC60BWFreeHolonomy S F
        (.trans (.atom g') (.atom h')) ↔
      g = g' ∧ h = h' := by
  constructor
  · intro heq
    rw [nativeC60BYTwoAtomic_holonomy S F g h,
      nativeC60BYTwoAtomic_holonomy S F g' h'] at heq
    have hlist := (nativeC60BYPositiveFreeWord_injective S) heq
    injection hlist with hgcode htail
    injection htail with hhcode hnil
    exact ⟨nativeC60BVGeneratorCode_injective S F hgcode,
      nativeC60BVGeneratorCode_injective S F hhcode⟩
  · rintro ⟨rfl, rfl⟩
    rfl

/-- Exact existing strict Kuu equality after ANY finite genuine
AQ context for an original TWO-GENERATOR 16D vertical comparison.
This substantially strengthens BX's singleton gate while avoiding
an unproved general signed groupoid normalization theorem. -/
theorem nativeC60BYTwoAtomic_strict_frame_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b c : L.Total}
    (g g' : (nativeC60BCClosedSignature S F).Gen a b)
    (h h' : (nativeC60BCClosedSignature S F).Gen b c) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (.trans (.atom g) (.atom h))) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (.trans (.atom g') (.atom h'))) ↔
      g = g' ∧ h = h' := by
  constructor
  · intro heq
    have hreplaceable :=
      (nativeC60AZStrictStep_exact
        (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (.trans (.atom g) (.atom h)))
        (nativeC60BCMapClosedStep S F word (.trans (.atom g') (.atom h')))).mp heq
    have hfree := nativeC60BWFreeHolonomy_reflects_contextual_replaceable
      S F word (.trans (.atom g) (.atom h))
        (.trans (.atom g') (.atom h')) hreplaceable
    exact (nativeC60BYTwoAtomic_free_eq_iff S F g g' h h').mp hfree
  · rintro ⟨rfl, rfl⟩
    rfl

/-- Physical AQ false and true generating frames are both included in
this all-finite-context two-step strict reflection theorem. -/
theorem nativeK5BYPhysical_two_atomic_strict_frame_eq_iff
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    {e d : NativeK5StructuralEightCell p h k}
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    {H K : NativeK5StructuralElevenCell p P Q}
    {U V : NativeK5StructuralTwelveCell p H K}
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {a₀ a₁ a₂ : (nativeK5AXBaseLayer W).Total}
    (g₁ g₂ : (nativeK5BCSignature W).Gen a₀ a₁)
    (h₁ h₂ : (nativeK5BCSignature W).Gen a₁ a₂) :
    nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word
          (.trans (.atom g₁) (.atom h₁))) =
      nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word
          (.trans (.atom g₂) (.atom h₂))) ↔
      g₁ = g₂ ∧ h₁ = h₂ :=
  nativeC60BYTwoAtomic_strict_frame_eq_iff
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    word g₁ g₂ h₁ h₂

#print axioms nativeC60BYReducedSignedWord_unique
#print axioms nativeC60BYReducedTrace_reduced
#print axioms nativeC60BYReducedTrace_sound
#print axioms nativeC60BYReducedTrace_eq_iff
#print axioms nativeC60BYReducedTrace_frame_eq_iff
#print axioms nativeC60BYPositiveSigned_reduced
#print axioms nativeC60BYPositiveFreeWord_injective
#print axioms nativeC60BYTwoAtomic_holonomy
#print axioms nativeC60BYTwoAtomic_free_eq_iff
#print axioms nativeC60BYTwoAtomic_strict_frame_eq_iff
#print axioms nativeK5BYPhysical_two_atomic_strict_frame_eq_iff

end
end Kuu.F112.Physical
