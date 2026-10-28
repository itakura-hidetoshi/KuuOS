import Kuu.F112.PolygonNativeC60TypedSeventeenTriangleCertificates

/-!
# F112-P94D3DR — finite C60 17D context transport and dependent 18D associator

DQ constructs an EXPLICITLY RELATIVE, dependent Type-valued 17D triangle
certificate between distinct original 16D proof terms, and proves that
every such certificate preserves the COMPLETE noncommutative BV word.
DO/DP independently prove finite genuine C60 AQ context-tree coherence
in original strict groups and the exact 16D descent obstruction.

DR genuinely lifts the original 14D AQ frames through the 15D source,
the entire raw 16D BC evidence, and the DQ 17D Type-valued grammar:
  * Define the 17D frame on the ACTUAL next AX layer; its onCell is
    the existing typed 16D BC transport, never a Peiffer projection.
  * Form an explicit context-closed 17D signature and construct the
    actual transported dependent 17D path for EVERY finite binary AQ
    tree and EVERY source 17D triangle path.
  * Prove ALL paths in this new context-closed grammar preserve the
    original COMPLETE signed noncommutative BV holonomy, by genuine
    generator/constructor induction and finite-prefix covariance.
    Hence BV mismatch still forbids any contextual 17D path.
  * Prove raw 17D transport is natural under ANY regrouping of equal
    chronological finite AQ context families, with exact dependent
    reindexing, not only after parity or strict quotient.

At the next dimension, construct the TRUE dependent 18D AX layer on
all raw17D paths, not on their strict hom-set quotient. Adjoin ONLY
explicit structural associator generators and their left/right
whiskerings, carrying all original 16D endpoint objects. Build BOTH
genuinely typed 18D routes around the four-input pentagon. Their
starting/ending 17D proof objects are identical but the two raw18D
routes are different syntax. The next 19D pentagon filler is NOT
postulated and no strict 18D pentagon equality is inferred.

The 17D and 18D structural generators are selected PRESENTATION data,
not pre-existing original C60 geometric 17D/18D fillers. The earlier
nonparallel 16D no-go, 14D/15D dependent proof histories, full CN/BV
codes, strict Kuu and independent Kuu presentation distinction, 107
public roots and Gray non-reintroduction are preserved. No new logical
axioms, sorry, admit or proof suppression. Apache-2.0; copyright
Hidetoshi Itakura / 板倉英俊.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Lift EACH physical 14D AQ Boolean singleton frame to the ACTUAL
next layer: objects are original proof-carrying 15D terms and morphisms
are original signed raw16D BC proof paths. No quotient is involved. -/
def nativeC60DRSeventeenFrame
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (side : Bool) :
    NativeC60BCFrame (nativeC60DQSeventeenLayer S F) where
  onObj := nativeC60BCContextTotal F [side]
  onCell := by
    intro a b c
    exact nativeC60BCMapClosedStep S F [side] c

/-- One ACTUAL 17D context step acts on complete original BV holonomy
through the full injective free-group prefix homomorphism. -/
theorem nativeC60DRSeventeenFrame_BV
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (side : Bool)
    (x : (nativeC60DQSeventeenLayer S F).Total) :
    nativeC60DQSeventeenHolonomy S F
        ((nativeC60DRSeventeenFrame S F side).mapTotal x) =
      (nativeC60BWFreePrefix S [side])
        (nativeC60DQSeventeenHolonomy S F x) := by
  rcases x with ⟨⟨a, b⟩, c⟩
  change nativeC60BWFreeHolonomy S F
      (nativeC60BCMapClosedStep S F [side] c) =
    (nativeC60BWFreePrefix S [side]) (nativeC60BWFreeHolonomy S F c)
  exact nativeC60BWFreeHolonomy_frame S F [side] c

/-- Compatibility of BV equality with either actual C60 AQ frame.
This is the local input for descent across every finite context word. -/
theorem nativeC60DRSeventeenFrame_BV_congr
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (side : Bool)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (h : nativeC60DQSeventeenHolonomy S F x =
      nativeC60DQSeventeenHolonomy S F y) :
    nativeC60DQSeventeenHolonomy S F
        ((nativeC60DRSeventeenFrame S F side).mapTotal x) =
      nativeC60DQSeventeenHolonomy S F
        ((nativeC60DRSeventeenFrame S F side).mapTotal y) := by
  rw [nativeC60DRSeventeenFrame_BV S F side x,
    nativeC60DRSeventeenFrame_BV S F side y, h]

/-- Any finite AQ Boolean word preserves the EXACT original BV
equality on the genuine 17D boundary, without conflating distinct
raw16D terms. -/
theorem nativeC60DRSeventeenContext_BV_congr
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (h : nativeC60DQSeventeenHolonomy S F x =
      nativeC60DQSeventeenHolonomy S F y) :
    nativeC60DQSeventeenHolonomy S F
        (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
          word x) =
      nativeC60DQSeventeenHolonomy S F
        (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
          word y) := by
  induction word with
  | nil =>
      exact h
  | cons side rest ih =>
      exact nativeC60DRSeventeenFrame_BV_congr S F side ih

/-- Explicitly context-closed RELATIVE 17D triangle presentation,
over ACTUAL original 16D proof objects; no new unframed generator is
obtained merely by forgetting boundary or equality of Peiffer words. -/
def nativeC60DRClosedSeventeenSignature
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AXSignature (nativeC60DQSeventeenLayer S F) :=
  nativeC60BCClosedSignature
    (nativeC60DQTriangleSeventeenSignature S F)
    (nativeC60DRSeventeenFrame S F)

/-- Main 17D soundness theorem: EVERY finite signed composite of
context-closed TRUE TYPE-VALUED 17D structural certificates respects
the complete original noncommutative BV word. -/
theorem nativeC60DRClosedSeventeenPath_BV
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) x y) :
    nativeC60DQSeventeenHolonomy S F x =
      nativeC60DQSeventeenHolonomy S F y := by
  apply NativeC60AXStep.observer_sound
    (nativeC60DQSeventeenHolonomy S F)
  · exact nativeC60BCClosedObserver_sound
      (nativeC60DQTriangleSeventeenSignature S F)
      (nativeC60DRSeventeenFrame S F)
      (nativeC60DQSeventeenHolonomy S F)
      (by
        intro a b g
        exact nativeC60DQSeventeenGenerator_BV S F g)
      (by
        intro word a b h
        exact nativeC60DRSeventeenContext_BV_congr S F word h)
  · exact p

/-- Any BV mismatch is an unconditional Type-valued obstruction to
a 17D path in the SELECTED contextual triangle-only presentation.
No claim about an independently provided alternative geometry. -/
theorem nativeC60DRNoClosedSeventeen_of_BV_mismatch
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (x y : (nativeC60DQSeventeenLayer S F).Total)
    (hne : nativeC60DQSeventeenHolonomy S F x ≠
      nativeC60DQSeventeenHolonomy S F y) :
    ¬ Nonempty (NativeC60AXStep
      (nativeC60DRClosedSeventeenSignature S F) x y) := by
  rintro ⟨p⟩
  exact hne (nativeC60DRClosedSeventeenPath_BV S F p)

/-- Independently constructed proof-relevant 17D transport in the
EXPLICIT closure. Every input 17D triangle path is transported through
the exact chronological AQ word of the supplied finite C60 tree. -/
def nativeC60DRTreeSeventeenTransport
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (tree : NativeK5DOContextTree)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) x y) :
    NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F)
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
        (nativeK5DOTreeWord tree) x)
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
        (nativeK5DOTreeWord tree) y) :=
  nativeC60BCMapOriginalStep
    (nativeC60DQTriangleSeventeenSignature S F)
    (nativeC60DRSeventeenFrame S F)
    (nativeK5DOTreeWord tree) p

/-- The independently constructed transported 17D proof has the
ACTUAL dependent raw16D source/target; no Peiffer or parity quotient
was used to invent the boundary. -/
theorem nativeC60DRTreeSeventeenTransport_boundary
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (tree : NativeK5DOContextTree)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) x y) :
    (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
      (nativeK5DOTreeWord tree) x).1 =
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
        (nativeK5DOTreeWord tree) y).1 :=
  (nativeC60DRTreeSeventeenTransport S F tree p).boundary

/-- All finite tree transports preserve original BV holonomy on their
ACTUAL dependent 17D endpoints, not merely after DC parity. -/
theorem nativeC60DRTreeSeventeenTransport_BV
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (tree : NativeK5DOContextTree)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) x y) :
    nativeC60DQSeventeenHolonomy S F
        (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
          (nativeK5DOTreeWord tree) x) =
      nativeC60DQSeventeenHolonomy S F
        (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
          (nativeK5DOTreeWord tree) y) :=
  nativeC60DRClosedSeventeenPath_BV S F
    (nativeC60DRTreeSeventeenTransport S F tree p)

/-- Finite AQ context-tree regrouping is natural on the ORIGINAL
TYPE-VALUED transported 17D path, with dependent target reindexing.
Unlike a free-BV observation, this is actual raw17D proof equality. -/
theorem nativeC60DRTreeSeventeenTransport_refinement
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) x y) :
    (nativeK5DOTreeWord_eq_of_steps_eq hsteps ▸
      nativeC60DRTreeSeventeenTransport S F left p) =
      nativeC60DRTreeSeventeenTransport S F right p := by
  have hdep :
      ∀ {w₁ w₂ : List Bool} (hw : w₁ = w₂),
        (hw ▸ nativeC60BCMapOriginalStep
          (nativeC60DQTriangleSeventeenSignature S F)
          (nativeC60DRSeventeenFrame S F) w₁ p) =
        nativeC60BCMapOriginalStep
          (nativeC60DQTriangleSeventeenSignature S F)
          (nativeC60DRSeventeenFrame S F) w₂ p := by
    intro w₁ w₂ hw
    cases hw
    rfl
  exact hdep (nativeK5DOTreeWord_eq_of_steps_eq hsteps)

/-- For any C60 AQ context tree, AU's ACTUAL physical 16D zigzag
obtains a constructed TYPE-VALUED 17D contextual triangle certificate
in the explicitly extended proof grammar, without declaring that it
exists in the original unextended C60 geometry. -/
theorem nativeC60DRTreeZigzag_contextual_exists
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (tree : NativeK5DOContextTree)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    Nonempty (NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F)
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
        (nativeK5DOTreeWord tree)
        (nativeC60DQPackSixteen S F (nativeC60DQRawZigzag S F g)))
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
        (nativeK5DOTreeWord tree)
        (nativeC60DQPackSixteen S F (.atom g)))) :=
  ⟨nativeC60DRTreeSeventeenTransport S F tree
    (nativeC60DQZigzagSeventeen S F g)⟩

/-- Dimension EIGHTEEN is a genuine NEXT AX layer over original raw
17D Type-valued proofs (not their selected strict equalities). -/
def nativeC60DREighteenLayer
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AXLayer.{u} :=
  nativeC60AXNext (nativeC60DQSeventeenLayer S F)
    (nativeC60DQTriangleSeventeenSignature S F)

/-- Pack a WHOLE raw17D path, retaining its two original raw16D proof
objects (and ultimately the 15D lower dependent source/target). -/
def nativeC60DRPackSeventeen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) x y) :
    (nativeC60DREighteenLayer S F).Total :=
  ⟨(x, y), p⟩

/-- A SELECTED, purely structural dependent 18D generator alphabet.
The associator compares two DIFFERENT raw17D bracketings; pre/post
whiskerings preserve every original 16D lower source/target. Such
whiskerings are explicitly constructed here, not claimed as original
C60 geometric horizontal higher composition. -/
inductive NativeC60DREighteenAssocGen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    (nativeC60DREighteenLayer S F).Total →
    (nativeC60DREighteenLayer S F).Total → Type u where
  | assoc {a b c d : (nativeC60DQSeventeenLayer S F).Total}
      (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
      (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
      (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d) :
      NativeC60DREighteenAssocGen S F
        (nativeC60DRPackSeventeen S F (.trans (.trans f g) h))
        (nativeC60DRPackSeventeen S F (.trans f (.trans g h)))
  | post {a b c : (nativeC60DQSeventeenLayer S F).Total}
      {p q : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b}
      (r : NativeC60DREighteenAssocGen S F
        (nativeC60DRPackSeventeen S F p)
        (nativeC60DRPackSeventeen S F q))
      (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c) :
      NativeC60DREighteenAssocGen S F
        (nativeC60DRPackSeventeen S F (.trans p h))
        (nativeC60DRPackSeventeen S F (.trans q h))
  | pre {a b c : (nativeC60DQSeventeenLayer S F).Total}
      (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
      {p q : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c}
      (r : NativeC60DREighteenAssocGen S F
        (nativeC60DRPackSeventeen S F p)
        (nativeC60DRPackSeventeen S F q)) :
      NativeC60DREighteenAssocGen S F
        (nativeC60DRPackSeventeen S F (.trans h p))
        (nativeC60DRPackSeventeen S F (.trans h q))

/-- No endpoint is erased: all three constructors of the explicitly
declared 18D associator/whiskering grammar are actual parallel
raw17D proof comparisons over the original C60 proof history. -/
def nativeC60DREighteenAssocSignature
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AXSignature (nativeC60DREighteenLayer S F) where
  Gen := NativeC60DREighteenAssocGen S F
  boundary := by
    intro x y r
    cases r <;> rfl

/-- Construct one genuine TYPE-VALUED 18D associator between any
three composable raw17D C60 structural comparison certificates. -/
def nativeC60DRAssociatorEighteen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d) :
    NativeC60AXStep (nativeC60DREighteenAssocSignature S F)
      (nativeC60DRPackSeventeen S F (.trans (.trans f g) h))
      (nativeC60DRPackSeventeen S F (.trans f (.trans g h))) :=
  .atom (.assoc f g h)

/-- The 18D associator is a real DEPENDENT proof object: its boundary
is verified from the entire original 17D path, not a scalar shadow. -/
theorem nativeC60DRAssociatorEighteen_boundary
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d) :
    (nativeC60DRPackSeventeen S F (.trans (.trans f g) h)).1 =
      (nativeC60DRPackSeventeen S F (.trans f (.trans g h))).1 :=
  (nativeC60DRAssociatorEighteen S F f g h).boundary

/-- Original raw17D reassociation does NOT become a raw proof identity
just because the selected 18D comparison was explicitly declared. -/
theorem nativeC60DRSeventeen_assoc_raw_ne
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d) :
    NativeC60AXStep.trans (NativeC60AXStep.trans f g) h ≠
      NativeC60AXStep.trans f (NativeC60AXStep.trans g h) := by
  intro eq
  cases eq

/-- The long boundary-typed route in the genuine four-input 18D
pentagon: post-whiskered assoc(f,g,h), assoc(f,g*h,k), then the
pre-whiskered assoc(g,h,k). -/
def nativeC60DRPentagonLong
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    NativeC60AXStep (nativeC60DREighteenAssocSignature S F)
      (nativeC60DRPackSeventeen S F
        (.trans (.trans (.trans f g) h) k))
      (nativeC60DRPackSeventeen S F
        (.trans f (.trans g (.trans h k)))) :=
  .trans
    (.trans
      (.atom (.post (.assoc f g h) k))
      (.atom (.assoc f (.trans g h) k)))
    (.atom (.pre f (.assoc g h k)))

/-- The short boundary-typed route in the genuine four-input 18D
pentagon: assoc(f*g,h,k), then assoc(f,g,h*k). The two raw routes
are independent presentations of a higher pentagon compatibility
problem, not silently declared equal. -/
def nativeC60DRPentagonShort
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    NativeC60AXStep (nativeC60DREighteenAssocSignature S F)
      (nativeC60DRPackSeventeen S F
        (.trans (.trans (.trans f g) h) k))
      (nativeC60DRPackSeventeen S F
        (.trans f (.trans g (.trans h k)))) :=
  .trans
    (.atom (.assoc (.trans f g) h k))
    (.atom (.assoc f g (.trans h k)))

/-- Both pasting routes exist as actual Type-valued 18D comparisons
between the SAME original raw17D endpoints, without adding a single
geometric 19-cell. This is the EXACT next coherence BOUNDARY. -/
theorem nativeC60DRPentagon_two_typed_routes
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    Nonempty (NativeC60AXStep (nativeC60DREighteenAssocSignature S F)
      (nativeC60DRPackSeventeen S F
        (.trans (.trans (.trans f g) h) k))
      (nativeC60DRPackSeventeen S F
        (.trans f (.trans g (.trans h k))))) :=
  ⟨nativeC60DRPentagonLong S F f g h k⟩

/-- The LONG and SHORT 18D pentagon paths are distinct ORIGINAL
raw Type-valued 18D proof terms. Their common lower 17D boundaries
do NOT supply a 19D filler nor an equality in the 18D strict quotient. -/
theorem nativeC60DRPentagon_raw_routes_ne
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    nativeC60DRPentagonLong S F f g h k ≠
      nativeC60DRPentagonShort S F f g h k := by
  intro eq
  cases eq

/-- Instantiate the 18D pentagon with FOUR independently constructed
original C60 17D AU zigzag roundtrips, at ANY genuine finite AQ tree.
This is a positive physical example, not a generic empty higher model. -/
def nativeC60DRPhysicalPentagonLong
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
    (tree : NativeK5DOContextTree) :=
  let S := nativeK5AXKuuSignature W
  let F := nativeK5BCFrame W
  let gen := nativeC60BCShiftGen S F (nativeK5DOTreeWord tree)
    (nativeK5CEPhysicalAUGenerator W)
  let route := nativeC60DQSeventeenRoundtrip S F gen
  nativeC60DRPentagonLong S F route route route route

#print axioms nativeC60DRSeventeenFrame
#print axioms nativeC60DRSeventeenFrame_BV
#print axioms nativeC60DRSeventeenFrame_BV_congr
#print axioms nativeC60DRSeventeenContext_BV_congr
#print axioms nativeC60DRClosedSeventeenSignature
#print axioms nativeC60DRClosedSeventeenPath_BV
#print axioms nativeC60DRNoClosedSeventeen_of_BV_mismatch
#print axioms nativeC60DRTreeSeventeenTransport
#print axioms nativeC60DRTreeSeventeenTransport_boundary
#print axioms nativeC60DRTreeSeventeenTransport_BV
#print axioms nativeC60DRTreeSeventeenTransport_refinement
#print axioms nativeC60DRTreeZigzag_contextual_exists
#print axioms nativeC60DREighteenLayer
#print axioms nativeC60DRPackSeventeen
#print axioms NativeC60DREighteenAssocGen
#print axioms nativeC60DREighteenAssocSignature
#print axioms nativeC60DRAssociatorEighteen
#print axioms nativeC60DRAssociatorEighteen_boundary
#print axioms nativeC60DRSeventeen_assoc_raw_ne
#print axioms nativeC60DRPentagonLong
#print axioms nativeC60DRPentagonShort
#print axioms nativeC60DRPentagon_two_typed_routes
#print axioms nativeC60DRPentagon_raw_routes_ne
#print axioms nativeC60DRPhysicalPentagonLong

end
end Kuu.F112.Physical
