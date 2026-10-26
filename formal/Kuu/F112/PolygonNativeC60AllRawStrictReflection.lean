import Kuu.F112.PolygonNativeC60AllTypedSignedNormalization

/-!
# F112-P94D3CD — full arbitrary raw 16D strict Hom reflection

CC proves ALL genuinely typed finite signed BC paths admit original
15D-boundary-preserving cancellation normal forms, and that equality
of their complete noncommutative free words is equivalent to equality
in the ALREADY SELECTED no-extra-relations strict Kuu quotient under
every finite original AQ context.

CD extends that theorem to EVERY original NativeC60AXStep raw16D term,
including arbitrary nesting of vertical composition, unit comparisons,
and symmetry of composite evidence. No raw constructor is erased by
declaration: instead a typed signed chain is CONSTRUCTED by structural
recursion, using a dependent append and an explicitly reversed chain.
The converter's interpretation in the selected strict quotient is
proved equal to the original raw comparison at every finite AQ context,
using real strict unit, associativity, and inverse laws.

The BW free holonomy is preserved by conversion, and CC then implies
the bidirectional exact equality criterion for ALL parallel RAW16D
comparisons, rather than only already-linear signed chains.

No new axiom, sorry/admit, Gray, geometric all-16-cell coherence,
unconditional horizontal Peiffer, global strict 3/n or hyperdescent
is claimed or introduced. The complete provenance of original 15D
objects and higher generators is retained by the typed converter.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v

/-- Strict arrow of an original positive BC higher generator after
an ACTUAL finite AQ context, before any raw syntax cancellation. -/
def nativeC60CDPosArrow
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :=
  nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    (.atom (nativeC60BCShiftGen S F word g))

/-- Strict arrow of the corresponding formal typed inverse generator. -/
def nativeC60CDNegArrow
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :=
  nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    (.symm (.atom (nativeC60BCShiftGen S F word g)))

/-- Actual dependent concatenation of any two finite signed 16D chains
through their SHARED ORIGINAL 15D proof-bearing boundary. -/
def nativeC60CDAppend
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a b c : L.Total} →
      NativeC60CASignedChain S F a b →
      NativeC60CASignedChain S F b c →
      NativeC60CASignedChain S F a c
  | _, _, _, .nil _, q => q
  | _, _, _, .pos g rest, q =>
      .pos g (nativeC60CDAppend S F rest q)
  | _, _, _, .neg g rest, q =>
      .neg g (nativeC60CDAppend S F rest q)

/-- Reversing an entire genuine typed signed path reverses order
AND each higher generator orientation. Unlike a FreeGroup shadow,
the output retains the EXACT original endpoint types and every
intermediate 15D proof object. -/
def nativeC60CDReverse
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a b : L.Total} →
      NativeC60CASignedChain S F a b →
      NativeC60CASignedChain S F b a
  | _, _, .nil x => .nil x
  | a, _, .pos g rest =>
      nativeC60CDAppend S F (nativeC60CDReverse S F rest)
        (.neg g (.nil a))
  | a, _, .neg g rest =>
      nativeC60CDAppend S F (nativeC60CDReverse S F rest)
        (.pos g (.nil a))

/-- A genuine empty typed chain realizes the categorical identity. -/
theorem nativeC60CDNil_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (a : L.Total) :
    nativeC60CAChainStrictFrame S F word (.nil a) =
      𝟙 ((nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
          ⟨nativeC60BCContextTotal F word a⟩) := by
  change nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (.refl (nativeC60BCContextTotal F word a)) = 𝟙 _
  exact nativeC60AZStrictStep_refl _ _ _

/-- The strictly interpreted positive head is its original arrow
composed with the whole genuine dependent tail. -/
theorem nativeC60CDPos_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b)
    (rest : NativeC60CASignedChain S F b c) :
    nativeC60CAChainStrictFrame S F word (.pos g rest) =
      nativeC60CDPosArrow S F word g ≫
        nativeC60CAChainStrictFrame S F word rest := by
  change nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (.trans (.atom (nativeC60BCShiftGen S F word g))
        (nativeC60BCMapClosedStep S F word (nativeC60CAChainStep S F rest))) =
      nativeC60CDPosArrow S F word g ≫
        nativeC60CAChainStrictFrame S F word rest
  exact nativeC60AZStrictStep_comp _ _ _ _

/-- The inverse head is its ACTUAL typed inverse followed by the tail. -/
theorem nativeC60CDNeg_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen b a)
    (rest : NativeC60CASignedChain S F b c) :
    nativeC60CAChainStrictFrame S F word (.neg g rest) =
      nativeC60CDNegArrow S F word g ≫
        nativeC60CAChainStrictFrame S F word rest := by
  change nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (.trans (.symm (.atom (nativeC60BCShiftGen S F word g)))
        (nativeC60BCMapClosedStep S F word (nativeC60CAChainStep S F rest))) =
      nativeC60CDNegArrow S F word g ≫
        nativeC60CAChainStrictFrame S F word rest
  exact nativeC60AZStrictStep_comp _ _ _ _

/-- The one-atom positive path realizes precisely its primitive. -/
theorem nativeC60CDPos_singleton
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60CAChainStrictFrame S F word (.pos g (.nil b)) =
      nativeC60CDPosArrow S F word g := by
  rw [nativeC60CDPos_strict, nativeC60CDNil_strict, Category.comp_id]

/-- The one-atom negative path realizes precisely its strict inverse. -/
theorem nativeC60CDNeg_singleton
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60CAChainStrictFrame S F word (.neg g (.nil a)) =
      nativeC60CDNegArrow S F word g := by
  rw [nativeC60CDNeg_strict, nativeC60CDNil_strict, Category.comp_id]

/-- Dependent concatenation is mapped to REAL strict vertical
composition at ANY genuine finite AQ context, for ALL lengths. -/
theorem nativeC60CDAppend_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b c : L.Total}
    (p : NativeC60CASignedChain S F a b)
    (q : NativeC60CASignedChain S F b c) :
    nativeC60CAChainStrictFrame S F word (nativeC60CDAppend S F p q) =
      nativeC60CAChainStrictFrame S F word p ≫
        nativeC60CAChainStrictFrame S F word q := by
  induction p with
  | nil x =>
      change nativeC60CAChainStrictFrame S F word q =
        nativeC60CAChainStrictFrame S F word (.nil x) ≫
          nativeC60CAChainStrictFrame S F word q
      rw [nativeC60CDNil_strict, Category.id_comp]
  | pos g rest ih =>
      change nativeC60CAChainStrictFrame S F word
          (.pos g (nativeC60CDAppend S F rest q)) =
        nativeC60CAChainStrictFrame S F word (.pos g rest) ≫
          nativeC60CAChainStrictFrame S F word q
      rw [nativeC60CDPos_strict, nativeC60CDPos_strict, ih,
        Category.assoc]
  | neg g rest ih =>
      change nativeC60CAChainStrictFrame S F word
          (.neg g (nativeC60CDAppend S F rest q)) =
        nativeC60CAChainStrictFrame S F word (.neg g rest) ≫
          nativeC60CAChainStrictFrame S F word q
      rw [nativeC60CDNeg_strict, nativeC60CDNeg_strict, ih,
        Category.assoc]

/-- A genuine reversed chain composes to the strict unit in BOTH
orders, with the original proof-bearing 15D endpoints retained. -/
theorem nativeC60CDReverse_strict_inverses
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (p : NativeC60CASignedChain S F a b) :
    (nativeC60CAChainStrictFrame S F word p ≫
        nativeC60CAChainStrictFrame S F word
          (nativeC60CDReverse S F p) =
      𝟙 ((nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
          ⟨nativeC60BCContextTotal F word a⟩)) ∧
    (nativeC60CAChainStrictFrame S F word
          (nativeC60CDReverse S F p) ≫
        nativeC60CAChainStrictFrame S F word p =
      𝟙 ((nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
          ⟨nativeC60BCContextTotal F word b⟩)) := by
  induction p with
  | nil x =>
      constructor <;>
        simp only [nativeC60CDReverse, nativeC60CDNil_strict, Category.id_comp]
  | pos g rest ih =>
      have hpos := nativeC60CDPos_strict S F word g rest
      have hrev : nativeC60CAChainStrictFrame S F word
          (nativeC60CDReverse S F (.pos g rest)) =
        nativeC60CAChainStrictFrame S F word
          (nativeC60CDReverse S F rest) ≫
          nativeC60CDNegArrow S F word g := by
        change nativeC60CAChainStrictFrame S F word
            (nativeC60CDAppend S F (nativeC60CDReverse S F rest)
              (.neg g (.nil _))) = _
        rw [nativeC60CDAppend_strict, nativeC60CDNeg_singleton]
      constructor
      · rw [hpos, hrev]
        calc
          _ = (nativeC60CDPosArrow S F word g ≫
                (nativeC60CAChainStrictFrame S F word rest ≫
                  nativeC60CAChainStrictFrame S F word
                    (nativeC60CDReverse S F rest))) ≫
                nativeC60CDNegArrow S F word g := by
                  simp only [Category.assoc]
          _ = (nativeC60CDPosArrow S F word g ≫ 𝟙 _) ≫
                nativeC60CDNegArrow S F word g := by rw [ih.1]
          _ = nativeC60CDPosArrow S F word g ≫
                nativeC60CDNegArrow S F word g := by
                  simp only [Category.comp_id]
          _ = 𝟙 _ := nativeC60AZStrictStep_inv_left _ _
                (.atom (nativeC60BCShiftGen S F word g))
      · rw [hrev, hpos]
        calc
          _ = (nativeC60CAChainStrictFrame S F word
                (nativeC60CDReverse S F rest) ≫
                (nativeC60CDNegArrow S F word g ≫
                  nativeC60CDPosArrow S F word g)) ≫
                  nativeC60CAChainStrictFrame S F word rest := by
                    simp only [Category.assoc]
          _ = (nativeC60CAChainStrictFrame S F word
                (nativeC60CDReverse S F rest) ≫ 𝟙 _) ≫
                  nativeC60CAChainStrictFrame S F word rest := by
                    rw [nativeC60AZStrictStep_inv_right]
          _ = nativeC60CAChainStrictFrame S F word
                (nativeC60CDReverse S F rest) ≫
                  nativeC60CAChainStrictFrame S F word rest := by
                    simp only [Category.comp_id]
          _ = 𝟙 _ := ih.2
  | neg g rest ih =>
      have hneg := nativeC60CDNeg_strict S F word g rest
      have hrev : nativeC60CAChainStrictFrame S F word
          (nativeC60CDReverse S F (.neg g rest)) =
        nativeC60CAChainStrictFrame S F word
          (nativeC60CDReverse S F rest) ≫
          nativeC60CDPosArrow S F word g := by
        change nativeC60CAChainStrictFrame S F word
            (nativeC60CDAppend S F (nativeC60CDReverse S F rest)
              (.pos g (.nil _))) = _
        rw [nativeC60CDAppend_strict, nativeC60CDPos_singleton]
      constructor
      · rw [hneg, hrev]
        calc
          _ = (nativeC60CDNegArrow S F word g ≫
                (nativeC60CAChainStrictFrame S F word rest ≫
                  nativeC60CAChainStrictFrame S F word
                    (nativeC60CDReverse S F rest))) ≫
                nativeC60CDPosArrow S F word g := by
                  simp only [Category.assoc]
          _ = (nativeC60CDNegArrow S F word g ≫ 𝟙 _) ≫
                nativeC60CDPosArrow S F word g := by rw [ih.1]
          _ = nativeC60CDNegArrow S F word g ≫
                nativeC60CDPosArrow S F word g := by
                  simp only [Category.comp_id]
          _ = 𝟙 _ := nativeC60AZStrictStep_inv_right _ _
                (.atom (nativeC60BCShiftGen S F word g))
      · rw [hrev, hneg]
        calc
          _ = (nativeC60CAChainStrictFrame S F word
                (nativeC60CDReverse S F rest) ≫
                (nativeC60CDPosArrow S F word g ≫
                  nativeC60CDNegArrow S F word g)) ≫
                  nativeC60CAChainStrictFrame S F word rest := by
                    simp only [Category.assoc]
          _ = (nativeC60CAChainStrictFrame S F word
                (nativeC60CDReverse S F rest) ≫ 𝟙 _) ≫
                  nativeC60CAChainStrictFrame S F word rest := by
                    rw [nativeC60AZStrictStep_inv_left]
          _ = nativeC60CAChainStrictFrame S F word
                (nativeC60CDReverse S F rest) ≫
                  nativeC60CAChainStrictFrame S F word rest := by
                    simp only [Category.comp_id]
          _ = 𝟙 _ := ih.2

/-- Categorical uniqueness of a right inverse given a left inverse:
this is STRUCTURAL, not the introduction of a strict higher axiom. -/
theorem nativeC60CDInverse_unique
    {C : Type u} [Category.{v} C] {a b : C}
    (f : a ⟶ b) (g h : b ⟶ a)
    (hfg : f ≫ g = 𝟙 a) (hhf : h ≫ f = 𝟙 b) : g = h := by
  calc
    g = 𝟙 b ≫ g := (Category.id_comp g).symm
    _ = (h ≫ f) ≫ g := by rw [hhf]
    _ = h ≫ (f ≫ g) := Category.assoc _ _ _
    _ = h ≫ 𝟙 a := by rw [hfg]
    _ = h := Category.comp_id _

/-- Convert ANY deeply parenthesized Type-valued AX raw16D comparison
into an actual dependent finite mixed signed 16D chain. The original
15D endpoints are indices; no selected quotient or scalar shadow is
used to define the converter. -/
def nativeC60CDRawToChain
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a b : L.Total} →
      NativeC60AXStep (nativeC60BCClosedSignature S F) a b →
      NativeC60CASignedChain S F a b
  | _, b, .atom g => .pos g (.nil b)
  | _, _, .refl a => .nil a
  | _, _, .symm c =>
      nativeC60CDReverse S F (nativeC60CDRawToChain S F c)
  | _, _, .trans c d =>
      nativeC60CDAppend S F
        (nativeC60CDRawToChain S F c)
        (nativeC60CDRawToChain S F d)

/-- Under EVERY original finite AQ context, interpretation of the
actual recursively constructed typed signed chain is EXACTLY the
chosen strict realization of the unmodified raw16D proof syntax. -/
theorem nativeC60CDRawToChain_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60CAChainStrictFrame S F word
        (nativeC60CDRawToChain S F c) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word c) := by
  induction c with
  | atom g =>
      change nativeC60CAChainStrictFrame S F word (.pos g (.nil _)) =
        nativeC60CDPosArrow S F word g
      exact nativeC60CDPos_singleton S F word g
  | refl x =>
      change nativeC60CAChainStrictFrame S F word (.nil x) =
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (.refl (nativeC60BCContextTotal F word x))
      rw [nativeC60CDNil_strict, nativeC60AZStrictStep_refl]
  | symm c ih =>
      change nativeC60CAChainStrictFrame S F word
          (nativeC60CDReverse S F (nativeC60CDRawToChain S F c)) =
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (.symm (nativeC60BCMapClosedStep S F word c))
      have hleft :
          nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
            (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
            (nativeC60BCMapClosedStep S F word c) ≫
              nativeC60CAChainStrictFrame S F word
                (nativeC60CDReverse S F (nativeC60CDRawToChain S F c)) =
          𝟙 _ := by
        rw [← ih]
        exact (nativeC60CDReverse_strict_inverses S F word
          (nativeC60CDRawToChain S F c)).1
      have hright :
          nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
            (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
            (.symm (nativeC60BCMapClosedStep S F word c)) ≫
          nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
            (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
            (nativeC60BCMapClosedStep S F word c) = 𝟙 _ :=
        nativeC60AZStrictStep_inv_right _ _ _
      exact nativeC60CDInverse_unique
        (nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (nativeC60BCMapClosedStep S F word c))
        (nativeC60CAChainStrictFrame S F word
          (nativeC60CDReverse S F (nativeC60CDRawToChain S F c)))
        (nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (.symm (nativeC60BCMapClosedStep S F word c)))
        hleft hright
  | trans c d ih ik =>
      change nativeC60CAChainStrictFrame S F word
        (nativeC60CDAppend S F
          (nativeC60CDRawToChain S F c) (nativeC60CDRawToChain S F d)) =
          nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
            (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
            (.trans (nativeC60BCMapClosedStep S F word c)
              (nativeC60BCMapClosedStep S F word d))
      calc
        _ = nativeC60CAChainStrictFrame S F word
              (nativeC60CDRawToChain S F c) ≫
            nativeC60CAChainStrictFrame S F word
              (nativeC60CDRawToChain S F d) :=
          nativeC60CDAppend_strict S F word _ _
        _ = nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
              (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
              (nativeC60BCMapClosedStep S F word c) ≫
            nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
              (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
              (nativeC60BCMapClosedStep S F word d) := by rw [ih, ik]
        _ = _ := (nativeC60AZStrictStep_comp _ _ _ _).symm

/-- The conversion preserves the FULL original noncommutative
generator holonomy. This follows from the proved strict realization
and BW's genuine free-holonomy soundness for the selected quotient,
not from equating raw AX proof syntax. -/
theorem nativeC60CDRawToChain_free
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BWFreeHolonomy S F
      (nativeC60CAChainStep S F (nativeC60CDRawToChain S F c)) =
    nativeC60BWFreeHolonomy S F c := by
  have hrel := (nativeC60AZStrictStep_exact
    (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    (nativeC60BCMapClosedStep S F word
      (nativeC60CAChainStep S F (nativeC60CDRawToChain S F c)))
    (nativeC60BCMapClosedStep S F word c)).mp
      (nativeC60CDRawToChain_strict S F word c)
  exact nativeC60BWFreeHolonomy_reflects_contextual_replaceable
    S F word (nativeC60CAChainStep S F (nativeC60CDRawToChain S F c)) c hrel

/-- THE COMPLETE RAW16D STRICT-HOM REFLECTION THEOREM.
For ALL original dependent raw higher comparisons (arbitrary nesting,
formal inverse, unit, vertical composition), including all finite
original AQ contexts, the chosen strict Kuu Hom arrows agree EXACTLY
when their full noncommutative free holonomies agree.

The raw terms themselves are NOT declared equal: only their chosen
strict quotient classes are compared, retaining all original 15D
source/target indices and original sixteen-dimensional generators. -/
theorem nativeC60CDAll_raw_free_eq_iff_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BWFreeHolonomy S F c =
        nativeC60BWFreeHolonomy S F d ↔
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word c) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word d) := by
  constructor
  · intro hfree
    have hc := nativeC60CDRawToChain_free S F word c
    have hd := nativeC60CDRawToChain_free S F word d
    have hchain : FreeGroup.mk
        (nativeC60CAChainSignedCodes S F (nativeC60CDRawToChain S F c)) =
      FreeGroup.mk
        (nativeC60CAChainSignedCodes S F (nativeC60CDRawToChain S F d)) := by
      rw [← nativeC60CAChain_holonomy S F (nativeC60CDRawToChain S F c),
        ← nativeC60CAChain_holonomy S F (nativeC60CDRawToChain S F d),
        hc, hd]
      exact hfree
    have hstrict := (nativeC60CCAll_signed_free_eq_iff_strict S F word
      (nativeC60CDRawToChain S F c)
      (nativeC60CDRawToChain S F d)).mp hchain
    exact (nativeC60CDRawToChain_strict S F word c).symm.trans
      (hstrict.trans (nativeC60CDRawToChain_strict S F word d))
  · intro hstrict
    have hrel := (nativeC60AZStrictStep_exact
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word c)
      (nativeC60BCMapClosedStep S F word d)).mp hstrict
    exact nativeC60BWFreeHolonomy_reflects_contextual_replaceable
      S F word c d hrel

/-- The previously conditional BX strict-free completeness property
is NOW PROVED for every original AX raw16D comparison. The empty
AQ word is ACTUALLY the identity on full Type-valued AX syntax. -/
theorem nativeC60CDFullFreeComplete
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60BXFullFreeComplete S F := by
  intro a b c d hfree
  have hstrict := (nativeC60CDAll_raw_free_eq_iff_strict S F [] c d).mp hfree
  have hraw : nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) c =
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) d := by
    simpa only [nativeC60BEMapClosedStep_nil] using hstrict
  exact (nativeC60AZStrictStep_exact _ _ c d).mp hraw

/-- The EXISTING selected Kuu strict free-holonomy FUNCTOR is fully
faithful on each exact proof-bearing Hom, by BX's representative
surjectivity criterion and the NEW raw16D completeness theorem. -/
theorem nativeC60CDStrictFreeFaithful
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60BXStrictFreeFaithful S F :=
  (nativeC60BXFullFreeComplete_iff_strict_faithful S F).mp
    (nativeC60CDFullFreeComplete S F)

/-- Any finite genuine AQ context is now faithful on these
constructed selected strict Hom arrows, without silently assuming
the previously open reflection gate. -/
theorem nativeC60CDAllContextHomFaithful
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) :
    NativeC60BUContextHomFaithful S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      word (nativeC60BDNoRelations_context S F word) :=
  nativeC60BXComplete_implies_all_context_faithful S F
    (nativeC60CDFullFreeComplete S F) word

#print axioms nativeC60CDAppend_strict
#print axioms nativeC60CDReverse_strict_inverses
#print axioms nativeC60CDInverse_unique
#print axioms nativeC60CDRawToChain_strict
#print axioms nativeC60CDRawToChain_free
#print axioms nativeC60CDAll_raw_free_eq_iff_strict
#print axioms nativeC60CDFullFreeComplete
#print axioms nativeC60CDStrictFreeFaithful
#print axioms nativeC60CDAllContextHomFaithful

end
end Kuu.F112.Physical
