import Kuu.F112.PolygonNativeC60FiniteStrictFunctorComposition

/-!
# F112-P94D3BG — genuine C60 finite-context binary whiskering gates

BF proves a strict endofunctor action by all finite original C60 contexts.
BG does NOT infer or fabricate two-variable horizontal composition from
unary endofunctors. Instead, for independently supplied typed left and
right whiskering candidates, it states EXACT full-arrow equivariance.

The candidate Peiffer square is recorded in the existing no-extra-relations
strict quotient, including BOTH actual C60 endpoints and an entire arrow.
Raw higher comparison evidence is carried separately through its own typed
dependent sigma-bundle: no quotient-by-observation is introduced.

The finite-word equivariance criterion reduces to just the two singleton
C60 frame obligations. Under these explicit obligations, Peiffer square
equalities transport forward and witnessed inequalities pull back.
No unconditional Peiffer interchange, original geometric 16-cell filling,
global strict n-category or hyperdescent is asserted.
No Gray, new axioms, sorry or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- Actual type-valued 16D comparisons, BEFORE the strict Kuu quotient,
retaining both original 15D endpoints. -/
abbrev NativeC60BGRawArrowBundle {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :=
  (nativeC60AXNext L (nativeC60BCClosedSignature S F)).Total

/-- Action on the raw dependent generator grammar; no scalar or
observational quotient is involved. -/
def nativeC60BGRawContext {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) :
    NativeC60BGRawArrowBundle S F → NativeC60BGRawArrowBundle S F
  | ⟨(a, b), f⟩ =>
      ⟨(nativeC60BCContextTotal F word a,
          nativeC60BCContextTotal F word b),
        nativeC60BCMapClosedStep S F word f⟩

theorem nativeC60BGRawContext_nil {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q : NativeC60BGRawArrowBundle S F) :
    nativeC60BGRawContext S F [] q = q := by
  rcases q with ⟨⟨a, b⟩, f⟩
  change (⟨(a, b), nativeC60BCMapClosedStep S F [] f⟩ :
    NativeC60BGRawArrowBundle S F) = ⟨(a, b), f⟩
  rw [nativeC60BEMapClosedStep_nil S F f]

theorem nativeC60BGRawContext_cons {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (side : Bool) (rest : List Bool)
    (q : NativeC60BGRawArrowBundle S F) :
    nativeC60BGRawContext S F (side :: rest) q =
      nativeC60BGRawContext S F [side]
        (nativeC60BGRawContext S F rest q) := by
  rcases q with ⟨⟨a, b⟩, f⟩
  change
    (⟨(nativeC60BCContextTotal F (side :: rest) a,
        nativeC60BCContextTotal F (side :: rest) b),
      nativeC60BCMapClosedStep S F (side :: rest) f⟩ :
        NativeC60BGRawArrowBundle S F) =
    ⟨(nativeC60BCContextTotal F [side] (nativeC60BCContextTotal F rest a),
        nativeC60BCContextTotal F [side] (nativeC60BCContextTotal F rest b)),
      nativeC60BCMapClosedStep S F [side]
        (nativeC60BCMapClosedStep S F rest f)⟩
  rw [nativeC60BEMapClosedStep_cons S F side rest f]
  simp only [nativeC60BCContextTotal]

/-- Exact composition on the whole RAW dependent higher-term bundle.
This stronger statement avoids ill-typed homogeneous comparisons between
terms whose endpoints are only propositionally equal. -/
theorem nativeC60BGRawContext_append {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (outer inner : List Bool) (q : NativeC60BGRawArrowBundle S F) :
    nativeC60BGRawContext S F (outer ++ inner) q =
      nativeC60BGRawContext S F outer
        (nativeC60BGRawContext S F inner q) := by
  induction outer with
  | nil =>
      change nativeC60BGRawContext S F inner q =
        nativeC60BGRawContext S F []
          (nativeC60BGRawContext S F inner q)
      exact (nativeC60BGRawContext_nil S F _).symm
  | cons side rest ih =>
      calc
        nativeC60BGRawContext S F ((side :: rest) ++ inner) q =
          nativeC60BGRawContext S F [side]
            (nativeC60BGRawContext S F (rest ++ inner) q) :=
          nativeC60BGRawContext_cons S F side (rest ++ inner) q
        _ = nativeC60BGRawContext S F [side]
              (nativeC60BGRawContext S F rest
                (nativeC60BGRawContext S F inner q)) :=
          congrArg (nativeC60BGRawContext S F [side]) ih
        _ = nativeC60BGRawContext S F (side :: rest)
              (nativeC60BGRawContext S F inner q) :=
          (nativeC60BGRawContext_cons S F side rest _).symm

/-- The first actual two-variable typed Peiffer route realized in the
strict quotient as a full arrow with BOTH endpoints attached. -/
def nativeC60BGHorizontalRLBundle {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (q r : NativeC60BGRawArrowBundle S F) :
    NativeC60BEStrictArrowBundle S F :=
  ⟨(H.obj q.1.1 r.1.1, H.obj q.1.2 r.1.2),
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BBHorizontalRL H q.2 r.2)⟩

/-- The independent, opposite typed Peiffer route.
The two candidates are not assumed equal. -/
def nativeC60BGHorizontalLRBundle {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (q r : NativeC60BGRawArrowBundle S F) :
    NativeC60BEStrictArrowBundle S F :=
  ⟨(H.obj q.1.1 r.1.1, H.obj q.1.2 r.1.2),
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BBHorizontalLR H q.2 r.2)⟩

/-- Genuine two-sided *conditional* coherence: both binary whiskering
orders commute with unary C60 context transport on ENTIRE strict-arrow
bundles, without discarding dependent endpoints or imposing Peiffer. -/
structure NativeC60BGWhiskeringEquivariant {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (word : List Bool) : Prop where
  rl : ∀ (q r : NativeC60BGRawArrowBundle S F),
    nativeC60BEArrowContext S F word (nativeC60BGHorizontalRLBundle S F H q r) =
      nativeC60BGHorizontalRLBundle S F H
        (nativeC60BGRawContext S F word q) (nativeC60BGRawContext S F word r)
  lr : ∀ (q r : NativeC60BGRawArrowBundle S F),
    nativeC60BEArrowContext S F word (nativeC60BGHorizontalLRBundle S F H q r) =
      nativeC60BGHorizontalLRBundle S F H
        (nativeC60BGRawContext S F word q) (nativeC60BGRawContext S F word r)

/-- Unit compatibility is unconditional, even though nonempty
two-variable whiskering compatibility remains a genuine obstruction. -/
theorem nativeC60BGWhiskeringEquivariant_nil {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F)) :
    NativeC60BGWhiskeringEquivariant S F H [] := by
  constructor
  · intro q r
    simpa only [nativeC60BGRawContext_nil S F] using
      (nativeC60BEArrowContext_nil S F (nativeC60BGHorizontalRLBundle S F H q r))
  · intro q r
    simpa only [nativeC60BGRawContext_nil S F] using
      (nativeC60BEArrowContext_nil S F (nativeC60BGHorizontalLRBundle S F H q r))

/-- If the actual two typed whiskerings are equivariant under each of
two finite words, they remain equivariant under concatenation. -/
theorem nativeC60BGWhiskeringEquivariant_append {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (outer inner : List Bool)
    (ho : NativeC60BGWhiskeringEquivariant S F H outer)
    (hi : NativeC60BGWhiskeringEquivariant S F H inner) :
    NativeC60BGWhiskeringEquivariant S F H (outer ++ inner) := by
  constructor
  · intro q r
    calc
      nativeC60BEArrowContext S F (outer ++ inner)
          (nativeC60BGHorizontalRLBundle S F H q r) =
        nativeC60BEArrowContext S F outer
          (nativeC60BEArrowContext S F inner
            (nativeC60BGHorizontalRLBundle S F H q r)) :=
        nativeC60BEArrowContext_append S F outer inner _
      _ = nativeC60BEArrowContext S F outer
            (nativeC60BGHorizontalRLBundle S F H
              (nativeC60BGRawContext S F inner q)
              (nativeC60BGRawContext S F inner r)) :=
        congrArg (nativeC60BEArrowContext S F outer) (hi.rl q r)
      _ = nativeC60BGHorizontalRLBundle S F H
            (nativeC60BGRawContext S F outer (nativeC60BGRawContext S F inner q))
            (nativeC60BGRawContext S F outer (nativeC60BGRawContext S F inner r)) :=
        ho.rl _ _
      _ = nativeC60BGHorizontalRLBundle S F H
            (nativeC60BGRawContext S F (outer ++ inner) q)
            (nativeC60BGRawContext S F (outer ++ inner) r) := by
        rw [nativeC60BGRawContext_append S F outer inner q,
          nativeC60BGRawContext_append S F outer inner r]
  · intro q r
    calc
      nativeC60BEArrowContext S F (outer ++ inner)
          (nativeC60BGHorizontalLRBundle S F H q r) =
        nativeC60BEArrowContext S F outer
          (nativeC60BEArrowContext S F inner
            (nativeC60BGHorizontalLRBundle S F H q r)) :=
        nativeC60BEArrowContext_append S F outer inner _
      _ = nativeC60BEArrowContext S F outer
            (nativeC60BGHorizontalLRBundle S F H
              (nativeC60BGRawContext S F inner q)
              (nativeC60BGRawContext S F inner r)) :=
        congrArg (nativeC60BEArrowContext S F outer) (hi.lr q r)
      _ = nativeC60BGHorizontalLRBundle S F H
            (nativeC60BGRawContext S F outer (nativeC60BGRawContext S F inner q))
            (nativeC60BGRawContext S F outer (nativeC60BGRawContext S F inner r)) :=
        ho.lr _ _
      _ = nativeC60BGHorizontalLRBundle S F H
            (nativeC60BGRawContext S F (outer ++ inner) q)
            (nativeC60BGRawContext S F (outer ++ inner) r) := by
        rw [nativeC60BGRawContext_append S F outer inner q,
          nativeC60BGRawContext_append S F outer inner r]

/-- All finite genuine C60 contexts are binary-whiskering-equivariant
IFF BOTH original singleton frames individually satisfy the actual
two-sided condition. This reduces INFINITELY many word checks to TWO
nontrivial, proof-relevant one-letter checks. -/
theorem nativeC60BGWhiskeringEquivariant_all_iff_letters
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F)) :
    (∀ word : List Bool, NativeC60BGWhiskeringEquivariant S F H word) ↔
      NativeC60BGWhiskeringEquivariant S F H [false] ∧
        NativeC60BGWhiskeringEquivariant S F H [true] := by
  constructor
  · intro h
    exact ⟨h [false], h [true]⟩
  · intro h word
    induction word with
    | nil => exact nativeC60BGWhiskeringEquivariant_nil S F H
    | cons side rest ih =>
        have hs : NativeC60BGWhiskeringEquivariant S F H [side] := by
          cases side with
          | false => exact h.1
          | true => exact h.2
        exact nativeC60BGWhiskeringEquivariant_append S F H [side] rest hs ih

/-- A selected Peiffer square equality at one actual typed pair
transports forward under the explicit two-sided equivariance gate.
This is a LOCAL witness, not a postulated universal interchange law. -/
theorem nativeC60BGPeifferSquare_transport {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (word : List Bool) (he : NativeC60BGWhiskeringEquivariant S F H word)
    (q r : NativeC60BGRawArrowBundle S F)
    (hp : nativeC60BGHorizontalRLBundle S F H q r =
      nativeC60BGHorizontalLRBundle S F H q r) :
    nativeC60BGHorizontalRLBundle S F H
        (nativeC60BGRawContext S F word q) (nativeC60BGRawContext S F word r) =
      nativeC60BGHorizontalLRBundle S F H
        (nativeC60BGRawContext S F word q) (nativeC60BGRawContext S F word r) := by
  calc
    _ = nativeC60BEArrowContext S F word
          (nativeC60BGHorizontalRLBundle S F H q r) := (he.rl q r).symm
    _ = nativeC60BEArrowContext S F word
          (nativeC60BGHorizontalLRBundle S F H q r) :=
      congrArg (nativeC60BEArrowContext S F word) hp
    _ = _ := he.lr q r

/-- A genuine unequal Peiffer square AFTER context transport obstructs
the corresponding equality BEFORE transport. The converse would require
faithfulness and is NOT claimed here. -/
theorem nativeC60BGPeifferObstruction_pullback {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (word : List Bool) (he : NativeC60BGWhiskeringEquivariant S F H word)
    (q r : NativeC60BGRawArrowBundle S F)
    (hne : nativeC60BGHorizontalRLBundle S F H
        (nativeC60BGRawContext S F word q) (nativeC60BGRawContext S F word r) ≠
      nativeC60BGHorizontalLRBundle S F H
        (nativeC60BGRawContext S F word q) (nativeC60BGRawContext S F word r)) :
    nativeC60BGHorizontalRLBundle S F H q r ≠
      nativeC60BGHorizontalLRBundle S F H q r := by
  intro hp
  exact hne (nativeC60BGPeifferSquare_transport S F H word he q r hp)

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

/-- For the actual original 13-cell physical C60 carrier, the
all-word conditional two-variable whiskering gate is precisely TWO
one-letter gates, not an infinite set of new geometric axioms. -/
theorem nativeK5BGPhysicalWhiskering_iff_letters
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W)) :
    (∀ word : List Bool,
      NativeC60BGWhiskeringEquivariant
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh word) ↔
      NativeC60BGWhiskeringEquivariant
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [false] ∧
      NativeC60BGWhiskeringEquivariant
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [true] :=
  nativeC60BGWhiskeringEquivariant_all_iff_letters
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh

/-- A physical two-sided whiskering candidate meeting the two frame
gates propagates any witnessed original typed Peiffer equality across
all finite contexts. It never asserts such equality unconditionally. -/
theorem nativeK5BGPhysicalPeifferSquare_all
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (hl : NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [false])
    (hr : NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [true])
    (word : List Bool)
    (q r : NativeC60BGRawArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W))
    (hp : nativeC60BGHorizontalRLBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh q r =
        nativeC60BGHorizontalLRBundle
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh q r) :
    nativeC60BGHorizontalRLBundle
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh
        (nativeC60BGRawContext (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word q)
        (nativeC60BGRawContext (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word r) =
      nativeC60BGHorizontalLRBundle
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh
        (nativeC60BGRawContext (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word q)
        (nativeC60BGRawContext (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word r) := by
  have h := (nativeK5BGPhysicalWhiskering_iff_letters W Hh).mpr ⟨hl, hr⟩
  exact nativeC60BGPeifferSquare_transport
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh word (h word) q r hp

end PhysicalC60

#print axioms NativeC60BGRawArrowBundle
#print axioms nativeC60BGRawContext
#print axioms nativeC60BGRawContext_nil
#print axioms nativeC60BGRawContext_cons
#print axioms nativeC60BGRawContext_append
#print axioms nativeC60BGHorizontalRLBundle
#print axioms nativeC60BGHorizontalLRBundle
#print axioms NativeC60BGWhiskeringEquivariant
#print axioms nativeC60BGWhiskeringEquivariant_nil
#print axioms nativeC60BGWhiskeringEquivariant_append
#print axioms nativeC60BGWhiskeringEquivariant_all_iff_letters
#print axioms nativeC60BGPeifferSquare_transport
#print axioms nativeC60BGPeifferObstruction_pullback
#print axioms nativeK5BGPhysicalWhiskering_iff_letters
#print axioms nativeK5BGPhysicalPeifferSquare_all

end
end Kuu.F112.Physical
