import Kuu.F112.PolygonNativeC60PhysicalPeifferCorrectedNaturality

/-!
# F112-P94D3BN — explicit binary whiskerings and exact physical two-gate obstruction

BB/BG/BI formulate conditional two-variable higher whiskering.
Here we construct an ACTUAL (but degenerate) projection solution of all
their hypotheses, and a genuinely physical NONTRIVIAL one-sided-frame
candidate that provably fails the opposite BG singleton gate.

The positive projection is a mathematical baseline, NOT a genuine
two-variable physical 16D operation: it forgets the second input.
Its coherence cannot establish original geometric horizontal gluing.
The negative result is specific to the genuine AQ raw 14D opposite
frame order. It uses BL's actual free 14D associativity obstruction,
NOT the kernel of an observer or a no-go for arbitrary horizontal
candidates.

No new axioms, sorry, admit, erased boundaries, Gray categories.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- The STRICT realization of the entire raw dependent AX arrow
bundle: actual source, actual target, and the already selected
strict Kuu projection, with no invented geometric generators. -/
def nativeC60BNStrictify {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q : NativeC60BGRawArrowBundle S F) :
    NativeC60BEStrictArrowBundle S F :=
  ⟨q.1, nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) q.2⟩

/-- STRICT realization commutes with every genuine unary context:
this compares full dependent arrow bundles, not observer values. -/
theorem nativeC60BNStrictify_context {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (q : NativeC60BGRawArrowBundle S F) :
    nativeC60BEArrowContext S F word (nativeC60BNStrictify S F q) =
      nativeC60BNStrictify S F (nativeC60BGRawContext S F word q) := by
  rcases q with ⟨⟨a, b⟩, f⟩
  exact nativeC60BEArrowContext_realize S F word f

/-- A real Type-valued BB structure, for ANY signature, obtained
by taking the FIRST argument. This is deliberately DEGENERATE. -/
def nativeC60BNFirstProjection {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L) : NativeC60BBWhiskering T where
  obj a _ := a
  left := by
    intro a x y c
    exact .refl a
  right := by
    intro x y c a
    exact c

/-- First projection RL is the strict realization of the first
raw input. The other independent comparison is truly discarded. -/
theorem nativeC60BNFirstRL {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q r : NativeC60BGRawArrowBundle S F) :
    nativeC60BGHorizontalRLBundle S F
      (nativeC60BNFirstProjection (nativeC60BCClosedSignature S F)) q r =
        nativeC60BNStrictify S F q := by
  rcases q with ⟨⟨a, b⟩, f⟩
  rcases r with ⟨⟨c, d⟩, g⟩
  change (⟨(a, b), nativeC60AZStrictStep
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (.trans f (.refl b))⟩ : NativeC60BEStrictArrowBundle S F) =
    ⟨(a, b), nativeC60AZStrictStep
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) f⟩
  simp only [nativeC60AZStrictStep_comp, nativeC60AZStrictStep_refl,
    Category.comp_id]

/-- First projection LR is the SAME strict arrow, although the
two raw constructor trees remain different. -/
theorem nativeC60BNFirstLR {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q r : NativeC60BGRawArrowBundle S F) :
    nativeC60BGHorizontalLRBundle S F
      (nativeC60BNFirstProjection (nativeC60BCClosedSignature S F)) q r =
        nativeC60BNStrictify S F q := by
  rcases q with ⟨⟨a, b⟩, f⟩
  rcases r with ⟨⟨c, d⟩, g⟩
  change (⟨(a, b), nativeC60AZStrictStep
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (.trans (.refl a) f)⟩ : NativeC60BEStrictArrowBundle S F) =
    ⟨(a, b), nativeC60AZStrictStep
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) f⟩
  simp only [nativeC60AZStrictStep_comp, nativeC60AZStrictStep_refl,
    Category.id_comp]

/-- A TRUE full two-sided BG gate for every finite word. Both
dependent Peiffer routes intertwine with actual strict frame action.
This only exhibits a DEGENERATE binary candidate. -/
theorem nativeC60BNFirst_all_BG {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) :
    NativeC60BGWhiskeringEquivariant S F
      (nativeC60BNFirstProjection (nativeC60BCClosedSignature S F)) word := by
  constructor
  · intro q r
    calc
      nativeC60BEArrowContext S F word
          (nativeC60BGHorizontalRLBundle S F
            (nativeC60BNFirstProjection (nativeC60BCClosedSignature S F)) q r) =
        nativeC60BEArrowContext S F word (nativeC60BNStrictify S F q) :=
          congrArg _ (nativeC60BNFirstRL S F q r)
      _ = nativeC60BNStrictify S F (nativeC60BGRawContext S F word q) :=
        nativeC60BNStrictify_context S F word q
      _ = nativeC60BGHorizontalRLBundle S F
            (nativeC60BNFirstProjection (nativeC60BCClosedSignature S F))
            (nativeC60BGRawContext S F word q)
            (nativeC60BGRawContext S F word r) :=
        (nativeC60BNFirstRL S F _ _).symm
  · intro q r
    calc
      nativeC60BEArrowContext S F word
          (nativeC60BGHorizontalLRBundle S F
            (nativeC60BNFirstProjection (nativeC60BCClosedSignature S F)) q r) =
        nativeC60BEArrowContext S F word (nativeC60BNStrictify S F q) :=
          congrArg _ (nativeC60BNFirstLR S F q r)
      _ = nativeC60BNStrictify S F (nativeC60BGRawContext S F word q) :=
        nativeC60BNStrictify_context S F word q
      _ = nativeC60BGHorizontalLRBundle S F
            (nativeC60BNFirstProjection (nativeC60BCClosedSignature S F))
            (nativeC60BGRawContext S F word q)
            (nativeC60BGRawContext S F word r) :=
        (nativeC60BNFirstLR S F _ _).symm

/-- Projection respects EVERY selected Kuu replacement quotient
because it literally maps one argument by identity, the other by
a genuine reflexivity proof. -/
theorem nativeC60BNFirst_congruent {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L) (R : NativeC60AZParallelRelation T) :
    NativeC60BBWhiskeringCongruent T R (nativeC60BNFirstProjection T) := by
  constructor
  · intro a x y f g hf
    rfl
  · intro x y f g a hf
    exact hf

/-- This projection is strictly functorial in EACH argument,
although the second argument has trivial action. -/
theorem nativeC60BNFirst_functorial {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L) (R : NativeC60AZParallelRelation T) :
    NativeC60BBWhiskeringFunctorial T R (nativeC60BNFirstProjection T) := by
  constructor
  · intro a x
    exact nativeC60AZStrictStep_refl T R a
  · intro x a
    exact nativeC60AZStrictStep_refl T R x
  · intro a x y z f g
    change nativeC60AZStrictStep T R (.refl a) =
      nativeC60AZStrictStep T R (.refl a) ≫
        nativeC60AZStrictStep T R (.refl a)
    simp only [nativeC60AZStrictStep_refl, Category.id_comp]
  · intro x y z f g a
    exact nativeC60AZStrictStep_comp T R f g

/-- Both Peiffer routes AGREE in any strict Kuu quotient, by
the selected unit laws rather than equality of raw 16D syntax. -/
theorem nativeC60BNFirst_peiffer {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L) (R : NativeC60AZParallelRelation T) :
    NativeC60BBPeifferSound T R (nativeC60BNFirstProjection T) := by
  intro a b c d f g
  change nativeC60AZStrictStep T R (.trans f (.refl b)) =
    nativeC60AZStrictStep T R (.trans (.refl a) f)
  simp only [nativeC60AZStrictStep_comp, nativeC60AZStrictStep_refl,
    Category.comp_id, Category.id_comp]

/-- Consequently all finite-context Peiffer replacement conditions
and middle-four hold for this explicitly DEGENERATE baseline.
In particular the BG singleton existence problem alone is solvable. -/
theorem nativeC60BNFirst_all_context_peiffer {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60BIAllContextPeifferReplacement S F
      (nativeC60BNFirstProjection (nativeC60BCClosedSignature S F)) := by
  exact (nativeC60BIAllContext_iff_peiffer S F
    (nativeC60BNFirstProjection (nativeC60BCClosedSignature S F))
    (nativeC60BNFirst_all_BG S F [false])
    (nativeC60BNFirst_all_BG S F [true])).mpr
    (nativeC60BNFirst_peiffer
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)))

/-- Honest BB candidate that applies an ACTUAL finite unary frame
to the first input. The second input is still discarded.
It need not be BG-equivariant for frames in the opposite order. -/
def nativeC60BNPrefixedFirst {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (fixed : List Bool) :
    NativeC60BBWhiskering (nativeC60BCClosedSignature S F) where
  obj a _ := nativeC60BCContextTotal F fixed a
  left := by
    intro a x y c
    exact .refl _
  right := by
    intro x y c a
    exact nativeC60BCMapClosedStep S F fixed c

section Physical

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

def nativeK5BNPrefixedFirst
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) : NativeC60BBWhiskering (nativeK5BCSignature W) :=
  nativeC60BNPrefixedFirst (nativeK5AXKuuSignature W)
    (nativeK5BCFrame W) [side]

/-- This NONCOMMUTATION is at the actual ORIGINAL 14D boundary
of ANY packed physical 15D proof, not merely at an observer.
It is the physical BL associativity obstruction. -/
theorem nativeK5BNFrames_swap_raw_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (a : (nativeK5AXBaseLayer W).Total) :
    nativeK5BCContext W [false] (nativeK5BCContext W [true] a) ≠
      nativeK5BCContext W [true] (nativeK5BCContext W [false] a) := by
  rcases a with ⟨⟨⟨R⟩, ⟨S⟩⟩, ⟨c⟩⟩
  intro h
  have heq := congrArg
    (fun z : (nativeK5AXBaseLayer W).Total => z.1.1.down) h
  change nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W R) =
    nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W R) at heq
  exact (nativeK5BLPhysicalFrames_raw_ne W R) heq.symm

/-- A GENUINELY PHYSICAL BB whiskering candidate that prefixes the
first input by the original AQ LEFT frame violates the opposite
RIGHT singleton BG gate, for EVERY original physical C60 carrier.
This is unconditional for this explicit candidate, NOT a global no-go. -/
theorem nativeK5BNLeftPrefixed_no_right_gate
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BNPrefixedFirst W true) [false] := by
  let a := nativeK5AXPack W (nativeK5AQExchange W [])
  apply nativeC60BJObjectMismatch_no_gate
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5BNPrefixedFirst W true) [false] a a
  change nativeK5BCContext W [false] (nativeK5BCContext W [true] a) ≠
    nativeK5BCContext W [true] (nativeK5BCContext W [false] a)
  exact nativeK5BNFrames_swap_raw_ne W a

/-- Conversely, an original AQ RIGHT-prefixed first projection
fails the actual LEFT singleton BG gate. -/
theorem nativeK5BNRightPrefixed_no_left_gate
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BNPrefixedFirst W false) [true] := by
  let a := nativeK5AXPack W (nativeK5AQExchange W [])
  apply nativeC60BJObjectMismatch_no_gate
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5BNPrefixedFirst W false) [true] a a
  change nativeK5BCContext W [true] (nativeK5BCContext W [false] a) ≠
    nativeK5BCContext W [false] (nativeK5BCContext W [true] a)
  exact (nativeK5BNFrames_swap_raw_ne W a).symm

/-- The one-sided frame obstruction rules out EVERY finite-context
BG equivariance for either prefixed physical candidate, since each
already fails ONE of BG's TWO actual generating tests. -/
theorem nativeK5BNPrefixed_not_all_BG
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) :
    ¬ ∀ word : List Bool, NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BNPrefixedFirst W side) word := by
  intro hall
  cases side with
  | false => exact nativeK5BNRightPrefixed_no_left_gate W (hall [true])
  | true => exact nativeK5BNLeftPrefixed_no_right_gate W (hall [false])

end Physical

#print axioms nativeC60BNStrictify
#print axioms nativeC60BNStrictify_context
#print axioms nativeC60BNFirstProjection
#print axioms nativeC60BNFirstRL
#print axioms nativeC60BNFirstLR
#print axioms nativeC60BNFirst_all_BG
#print axioms nativeC60BNFirst_congruent
#print axioms nativeC60BNFirst_functorial
#print axioms nativeC60BNFirst_peiffer
#print axioms nativeC60BNFirst_all_context_peiffer
#print axioms nativeC60BNPrefixedFirst
#print axioms nativeK5BNPrefixedFirst
#print axioms nativeK5BNFrames_swap_raw_ne
#print axioms nativeK5BNLeftPrefixed_no_right_gate
#print axioms nativeK5BNRightPrefixed_no_left_gate
#print axioms nativeK5BNPrefixed_not_all_BG

end
end Kuu.F112.Physical
