import Kuu.LivingEngi.ScopedGluing

/-!
# Living Engi Cycle LEC-05: typed frame transport and scoped gauge gluing

A family of genuinely dependent fibers F i is supplied with equivalences
e i : F i ≃ A to one declared readout carrier A. Transport is constructed
from these actual frames. Identity, reverse, triangle and quadruple path
coherence follow as theorems, not from an unexplained coherence axiom.

Local sections preserve their original context-dependent fiber types.
Their transported readouts glue to a unique conventional global function
precisely if they agree on overlaps. Independent local gauge changes
preserve readouts, compatibility, and global existence.

This proves neither arbitrary gerbe/stack descent nor original
F55/P77 source witness equality. The chosen frames form a flat,
trivializable model, not a theorem that all connections are flat.
-/

namespace Kuu.LivingEngi

set_option autoImplicit false

universe uX uI uF uA

section FrameTransport

variable {I : Type uI} {F : I → Type uF} {A : Type uA}

/-- Explicit per-context equivalences into one declared common readout type. -/
abbrev Frames (F : I → Type uF) (A : Type uA) :=
  (i : I) → F i ≃ A

/-- Source-to-target transport built from supplied typed equivalences. -/
def frameTransport (e : Frames F A) (i j : I) : F i ≃ F j :=
  (e i).trans (e j).symm

@[simp] theorem frameTransport_apply
    (e : Frames F A) (i j : I) (x : F i) :
    frameTransport e i j x = (e j).symm ((e i) x) := rfl

/-- Transport from a fiber to itself is identity. -/
theorem frameTransport_self
    (e : Frames F A) (i : I) :
    frameTransport e i i = Equiv.refl (F i) := by
  apply Equiv.ext
  intro x
  simp [frameTransport]

/-- Exact triangle cocycle of actual transport equivalences. -/
theorem frameTransport_comp
    (e : Frames F A) (i j k : I) :
    (frameTransport e i j).trans (frameTransport e j k) =
      frameTransport e i k := by
  apply Equiv.ext
  intro x
  simp [frameTransport]

/-- The reverse transport is the inverse equivalence. -/
theorem frameTransport_symm
    (e : Frames F A) (i j : I) :
    (frameTransport e i j).symm = frameTransport e j i := by
  apply Equiv.ext
  intro x
  simp [frameTransport]

/-- Four-context coherence through two certified intermediate steps. -/
theorem frameTransport_four
    (e : Frames F A) (i j k l : I) :
    ((frameTransport e i j).trans (frameTransport e j k)).trans
      (frameTransport e k l) = frameTransport e i l := by
  rw [frameTransport_comp, frameTransport_comp]

/-- Independent presentation changes at every local context. -/
def gaugeFrames (e : Frames F A)
    (g : (i : I) → F i ≃ F i) : Frames F A :=
  fun i => (g i).symm.trans (e i)

/-- Transport is covariant under local gauge changes at both endpoints. -/
theorem gaugeTransport_covariant
    (e : Frames F A) (g : (i : I) → F i ≃ F i)
    (i j : I) (x : F i) :
    frameTransport (gaugeFrames e g) i j ((g i) x) =
      (g j) (frameTransport e i j x) := by
  simp [frameTransport, gaugeFrames]

end FrameTransport

section TypedLocalDescent

variable {X : Type uX} {I : Type uI}
variable {F : I → Type uF} {A : Type uA}

/-- The local values still inhabit their ORIGINAL dependent fibers. -/
abbrev FramedLocalSections (U : I → Set X) (F : I → Type uF) :=
  (i : I) → {x : X // x ∈ U i} → F i

/-- The ordinary function-sheaf readout AFTER explicit frame transport. -/
def framedReadout
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F) : LocalSections U A :=
  fun i x => (e i) (s i x)

/-- Compatibility in the original typed target fiber, not source equality. -/
def TransportCompatible
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F) : Prop :=
  ∀ (i j : I) (x : X) (hi : x ∈ U i) (hj : x ∈ U j),
    frameTransport e i j (s i ⟨x, hi⟩) = s j ⟨x, hj⟩

/-- Global conventional readout only; no assertion of an exact WORLD. -/
def HasFramedGlobal
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F) : Prop :=
  HasGlobal U (framedReadout U e s)

/-- Typed compatibility exactly equals compatibility of true readouts. -/
theorem transportCompatible_iff_readoutCompatible
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F) :
    TransportCompatible U e s ↔ Compatible U (framedReadout U e s) := by
  constructor
  · intro h i j x hi hj
    have ht := congrArg (e j) (h i j x hi hj)
    simpa [frameTransport, framedReadout] using ht
  · intro h i j x hi hj
    have ht := congrArg ((e j).symm) (h i j x hi hj)
    simpa [frameTransport, framedReadout] using ht

/-- Under an actual covering family, typed compatible local values
glue iff a conventional global readout exists. -/
theorem transportCompatible_iff_hasFramedGlobal
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F)
    (hcover : Covers U) :
    TransportCompatible U e s ↔ HasFramedGlobal U e s := by
  calc
    TransportCompatible U e s ↔ Compatible U (framedReadout U e s) :=
      transportCompatible_iff_readoutCompatible U e s
    _ ↔ HasGlobal U (framedReadout U e s) :=
      compatible_iff_hasGlobal U (framedReadout U e s) hcover

/-- Construct the global readout using the previously certified
ordinary sheaf of functions and the newly proved compatibility bridge. -/
noncomputable def framedGlue
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F)
    (hcover : Covers U) (hcompat : TransportCompatible U e s) : X → A :=
  glue U (framedReadout U e s) hcover
    ((transportCompatible_iff_readoutCompatible U e s).1 hcompat)

/-- Preserve exact values of each original dependent local section. -/
theorem framedGlue_agrees
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F)
    (hcover : Covers U) (hcompat : TransportCompatible U e s)
    (i : I) (x : {y : X // y ∈ U i}) :
    framedGlue U e s hcover hcompat x.1 = (e i) (s i x) := by
  exact glue_agrees U (framedReadout U e s) hcover
    ((transportCompatible_iff_readoutCompatible U e s).1 hcompat) i x

/-- Concrete incompatible typed transport cannot be silently globalized. -/
theorem noFramedGlobal_of_transport_disagreement
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F)
    (hcover : Covers U)
    (hbad : ¬ TransportCompatible U e s) :
    ¬ HasFramedGlobal U e s := by
  intro hglobal
  exact hbad
    ((transportCompatible_iff_hasFramedGlobal U e s hcover).2 hglobal)

/-- Reparameterize each actual source value in its own fiber. -/
def gaugeLocalSections
    (U : I → Set X) (g : (i : I) → F i ≃ F i)
    (s : FramedLocalSections U F) : FramedLocalSections U F :=
  fun i x => (g i) (s i x)

/-- Observable values remain equal after compensating frame changes. -/
theorem gaugeReadout_invariant
    (U : I → Set X) (e : Frames F A)
    (g : (i : I) → F i ≃ F i)
    (s : FramedLocalSections U F) :
    framedReadout U (gaugeFrames e g) (gaugeLocalSections U g s) =
      framedReadout U e s := by
  funext i x
  simp [framedReadout, gaugeFrames, gaugeLocalSections]

/-- Global conventional readout existence is local-frame invariant. -/
theorem gaugeGlobal_iff
    (U : I → Set X) (e : Frames F A)
    (g : (i : I) → F i ≃ F i)
    (s : FramedLocalSections U F) :
    HasFramedGlobal U (gaugeFrames e g) (gaugeLocalSections U g s) ↔
      HasFramedGlobal U e s := by
  change HasGlobal U (framedReadout U (gaugeFrames e g)
      (gaugeLocalSections U g s)) ↔ HasGlobal U (framedReadout U e s)
  rw [gaugeReadout_invariant]

/-- Local compatibility itself is invariant under local presentation change. -/
theorem gaugeCompatible_iff
    (U : I → Set X) (e : Frames F A)
    (g : (i : I) → F i ≃ F i)
    (s : FramedLocalSections U F) :
    TransportCompatible U (gaugeFrames e g) (gaugeLocalSections U g s) ↔
      TransportCompatible U e s := by
  calc
    TransportCompatible U (gaugeFrames e g) (gaugeLocalSections U g s) ↔
        Compatible U (framedReadout U (gaugeFrames e g)
          (gaugeLocalSections U g s)) :=
      transportCompatible_iff_readoutCompatible U _ _
    _ ↔ Compatible U (framedReadout U e s) := by
      rw [gaugeReadout_invariant]
    _ ↔ TransportCompatible U e s :=
      (transportCompatible_iff_readoutCompatible U e s).symm

/-- LEC-04 admission must respect a proved transport incompatibility. -/
theorem transportFailure_blocks_promotion
    (U : I → Set X) (e : Frames F A)
    (s : FramedLocalSections U F) (hcover : Covers U)
    (hbad : ¬ TransportCompatible U e s)
    (ev : PromotionEvidence (HasFramedGlobal U e s)) :
    ¬ Admissible ev := by
  intro hadmit
  exact (noFramedGlobal_of_transport_disagreement U e s hcover hbad)
    (admitted_sound ev hadmit)

end TypedLocalDescent

#print axioms frameTransport_self
#print axioms frameTransport_comp
#print axioms frameTransport_symm
#print axioms frameTransport_four
#print axioms gaugeTransport_covariant
#print axioms transportCompatible_iff_readoutCompatible
#print axioms transportCompatible_iff_hasFramedGlobal
#print axioms framedGlue_agrees
#print axioms noFramedGlobal_of_transport_disagreement
#print axioms gaugeReadout_invariant
#print axioms gaugeGlobal_iff
#print axioms gaugeCompatible_iff
#print axioms transportFailure_blocks_promotion

end Kuu.LivingEngi
