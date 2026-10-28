import Kuu.F112.PolygonNativeC60AQGaugePentagonDescent

/-!
# F112-P94D3DV — genuine AQ 17D transport of the full typed 18D associator grammar

DR constructs, from EACH actual 17D triangle path and a genuine finite
C60 AQ context word, a TYPE-VALUED 17D path in the independently
declared context-closed 17D signature. DS retains the complete
dependent raw 18D associator, left/right whiskerings and signed paths.

DV transports EVERY ORIGINAL dependent 18D generator through this
actually constructed 17D action, including BOTH dependent endpoints,
into an explicitly distinct context-closed 18D associator grammar:
  * Construct the exact target 18D layer, generator code and signature.
  * Extend the TRUE AQ 17D map by recursion through associator,
    pre-whiskering, post-whiskering and all signed 18D raw paths.
  * Construct the induced universal FreeGroup homomorphism on every
    original complete 18D generator code; prove that interpreting
    original 18D paths into complete free words commutes with transport.
  * Prove preservation of actual 18D associator sources, targets,
    composition, reversal and finite AQ tree refinement.
  * No hidden identification of the two full 18D pentagon routes.

IMPORTANT authority boundary: the source is DT's ORIGINAL 18D
presentation. The target uses the separately constructed context-CLOSED
17D signature, hence is an EXPLICIT RELATIVE target presentation, not
automatically an endomorphism of the original unclosed code alphabet.
Existence of an original geometric C60 19D filler is not asserted.
No new axioms or sorry; keep strict Kuu, independent Kuu as a
presentation, 107 public roots, all no-go and no Gray.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

section ActualAQSeventeenToEighteen

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Unlike DR's original 17D triangle-source signature, the receiving
17D syntax is genuinely closed under ACTUAL finite AQ contexts. -/
def nativeC60DVClosedEighteenLayer : NativeC60AXLayer.{u} :=
  nativeC60AXNext (nativeC60DQSeventeenLayer S F)
    (nativeC60DRClosedSeventeenSignature S F)

/-- Pack an entire target raw 17D path with both dependent endpoints. -/
def nativeC60DVPackClosedSeventeen
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b) :
    (nativeC60DVClosedEighteenLayer S F).Total :=
  ⟨(a, b), p⟩

/-- The target 18D grammar is not an arbitrary graph: every primitive
stores the entire context-closed 17D proof and its original
16D/15D/14D lower boundary data. -/
inductive NativeC60DVClosedEighteenGen :
    (nativeC60DVClosedEighteenLayer S F).Total →
    (nativeC60DVClosedEighteenLayer S F).Total → Type u where
  | assoc {a b c d : (nativeC60DQSeventeenLayer S F).Total}
      (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
      (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
      (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d) :
      NativeC60DVClosedEighteenGen
        (nativeC60DVPackClosedSeventeen S F (.trans (.trans f g) h))
        (nativeC60DVPackClosedSeventeen S F (.trans f (.trans g h)))
  | post {a b c : (nativeC60DQSeventeenLayer S F).Total}
      {p q : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b}
      (r : NativeC60DVClosedEighteenGen
        (nativeC60DVPackClosedSeventeen S F p)
        (nativeC60DVPackClosedSeventeen S F q))
      (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c) :
      NativeC60DVClosedEighteenGen
        (nativeC60DVPackClosedSeventeen S F (.trans p h))
        (nativeC60DVPackClosedSeventeen S F (.trans q h))
  | pre {a b c : (nativeC60DQSeventeenLayer S F).Total}
      (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
      {p q : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c}
      (r : NativeC60DVClosedEighteenGen
        (nativeC60DVPackClosedSeventeen S F p)
        (nativeC60DVPackClosedSeventeen S F q)) :
      NativeC60DVClosedEighteenGen
        (nativeC60DVPackClosedSeventeen S F (.trans h p))
        (nativeC60DVPackClosedSeventeen S F (.trans h q))

/-- A real dependent 18D signature; globular boundaries are proved
by the original stored 17D endpoints, not imposed via a quotient. -/
def nativeC60DVClosedEighteenSignature :
    NativeC60AXSignature (nativeC60DVClosedEighteenLayer S F) where
  Gen := NativeC60DVClosedEighteenGen S F
  boundary := by
    intro x y g
    cases g <;> rfl

/-- The genuine finite-AQ context action on EVERY original 17D path,
but its codomain is deliberately the explicit closed 17D grammar. -/
def nativeC60DVSeventeenWordMap
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) :
    NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F)
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word a)
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word b) :=
  nativeC60BCMapOriginalStep (nativeC60DQTriangleSeventeenSignature S F)
    (nativeC60DRSeventeenFrame S F) word p

theorem nativeC60DVSeventeenWordMap_trans
    (word : List Bool)
    {a b c : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (q : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c) :
    nativeC60DVSeventeenWordMap S F word (.trans p q) =
      .trans (nativeC60DVSeventeenWordMap S F word p)
        (nativeC60DVSeventeenWordMap S F word q) := rfl

theorem nativeC60DVSeventeenWordMap_symm
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) :
    nativeC60DVSeventeenWordMap S F word (.symm p) =
      .symm (nativeC60DVSeventeenWordMap S F word p) := rfl

/-- ACTUAL raw18D object map, preserving the entire source/target
raw17D path syntax under finite original C60 AQ transport. -/
def nativeC60DVTransportEighteenObj (word : List Bool) :
    (nativeC60DREighteenLayer S F).Total →
      (nativeC60DVClosedEighteenLayer S F).Total
  | ⟨(a, b), p⟩ =>
      nativeC60DVPackClosedSeventeen S F
        (nativeC60DVSeventeenWordMap S F word p)

/-- All 18D primitives are mapped by TRUE dependent recursion.
The source is DR's entire genuine associator/whiskering alphabet,
not an arbitrarily selected 18D gauge statistic. -/
def nativeC60DVTransportEighteenGen
    (word : List Bool)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (g : (nativeC60DREighteenAssocSignature S F).Gen x y) :
    (nativeC60DVClosedEighteenSignature S F).Gen
      (nativeC60DVTransportEighteenObj S F word x)
      (nativeC60DVTransportEighteenObj S F word y) := by
  induction g with
  | assoc f g h =>
      exact .assoc
        (nativeC60DVSeventeenWordMap S F word f)
        (nativeC60DVSeventeenWordMap S F word g)
        (nativeC60DVSeventeenWordMap S F word h)
  | post r h ih =>
      exact .post ih (nativeC60DVSeventeenWordMap S F word h)
  | pre h r ih =>
      exact .pre (nativeC60DVSeventeenWordMap S F word h) ih

/-- The COMPLETE signed raw18D path transport induced by the
genuinely constructed 17D AQ map. Every source and target remains
a dependent Type-valued original comparison path. -/
def nativeC60DVTransportEighteenStep
    (word : List Bool)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y) :
    NativeC60AXStep (nativeC60DVClosedEighteenSignature S F)
      (nativeC60DVTransportEighteenObj S F word x)
      (nativeC60DVTransportEighteenObj S F word y) :=
  p.fold
    (K := fun a b => NativeC60AXStep (nativeC60DVClosedEighteenSignature S F)
      (nativeC60DVTransportEighteenObj S F word a)
      (nativeC60DVTransportEighteenObj S F word b))
    (fun {_ _} g => .atom (nativeC60DVTransportEighteenGen S F word g))
    (fun _ => .refl _)
    (fun h => .symm h)
    (fun h k => .trans h k)

theorem nativeC60DVTransportEighteenStep_atom
    (word : List Bool)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (g : (nativeC60DREighteenAssocSignature S F).Gen x y) :
    nativeC60DVTransportEighteenStep S F word (.atom g) =
      .atom (nativeC60DVTransportEighteenGen S F word g) := rfl

theorem nativeC60DVTransportEighteenStep_trans
    (word : List Bool)
    {x y z : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y)
    (q : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) y z) :
    nativeC60DVTransportEighteenStep S F word (.trans p q) =
      .trans (nativeC60DVTransportEighteenStep S F word p)
        (nativeC60DVTransportEighteenStep S F word q) := rfl

theorem nativeC60DVTransportEighteenStep_symm
    (word : List Bool)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y) :
    nativeC60DVTransportEighteenStep S F word (.symm p) =
      .symm (nativeC60DVTransportEighteenStep S F word p) := rfl

/-- The target alphabet STILL records full dependent source/target
and the entire 18D generator, now in the separately closed grammar. -/
abbrev NativeC60DVCompleteEighteenCode : Type u :=
  Σ x : (nativeC60DVClosedEighteenLayer S F).Total,
    Σ y : (nativeC60DVClosedEighteenLayer S F).Total,
      (nativeC60DVClosedEighteenSignature S F).Gen x y

/-- Actual map on ALL source complete-code letters, including each
original lower witness; no scalar or parity summary can replace it. -/
def nativeC60DVTransportCompleteCode (word : List Bool)
    (code : NativeC60DSCompleteEighteenCode S F) :
    NativeC60DVCompleteEighteenCode S F :=
  ⟨nativeC60DVTransportEighteenObj S F word code.1,
   nativeC60DVTransportEighteenObj S F word code.2.1,
   nativeC60DVTransportEighteenGen S F word code.2.2⟩

/-- The actual target group retains all signed ordered transported
dependent 18D codes. -/
abbrev NativeC60DVClosedFullFree :=
  FreeGroup (NativeC60DVCompleteEighteenCode S F)

def nativeC60DVClosedFreeWeight :
    ∀ {x y}, (nativeC60DVClosedEighteenSignature S F).Gen x y →
      NativeC60DVClosedFullFree S F :=
  fun {_ _} g => FreeGroup.of ⟨_, _, g⟩

def nativeC60DVClosedFreeWord
    {x y : (nativeC60DVClosedEighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DVClosedEighteenSignature S F) x y) :
    NativeC60DVClosedFullFree S F :=
  nativeC60AZHolonomy (nativeC60DVClosedEighteenSignature S F)
    (nativeC60DVClosedFreeWeight S F) p

/-- The word map is CONSTRUCTED from the entire actual mapped alphabet,
not merely postulated as an endomorphism of the original group. -/
def nativeC60DVFullWordTransport (word : List Bool) :
    NativeC60DTFullFree S F →* NativeC60DVClosedFullFree S F :=
  FreeGroup.lift
    (fun code => FreeGroup.of (nativeC60DVTransportCompleteCode S F word code))

theorem nativeC60DVFullWordTransport_of
    (word : List Bool) (code : NativeC60DSCompleteEighteenCode S F) :
    (nativeC60DVFullWordTransport S F word) (FreeGroup.of code) =
      FreeGroup.of (nativeC60DVTransportCompleteCode S F word code) := by
  simp only [nativeC60DVFullWordTransport, FreeGroup.lift_apply_of]

/-- A commuting square of ENTIRE ORIGINAL noncommutative 18D free
evidence, not merely length or Peiffer shadows. It is a naturality
statement between the two EXPLICITLY DECLARED Type-valued grammars. -/
theorem nativeC60DVFullWordTransport_natural
    (word : List Bool)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y) :
    (nativeC60DVFullWordTransport S F word)
        (nativeC60DSFreeWord S F p) =
      nativeC60DVClosedFreeWord S F
        (nativeC60DVTransportEighteenStep S F word p) := by
  induction p with
  | atom g =>
      change (nativeC60DVFullWordTransport S F word)
        (FreeGroup.of (nativeC60DSCode S F g)) =
        FreeGroup.of (nativeC60DVTransportCompleteCode S F word
          (nativeC60DSCode S F g))
      exact nativeC60DVFullWordTransport_of S F word _
  | refl a =>
      change (nativeC60DVFullWordTransport S F word) 1 = 1
      exact map_one _
  | symm p ih =>
      change (nativeC60DVFullWordTransport S F word)
          (nativeC60DSFreeWord S F p)⁻¹ =
        (nativeC60DVClosedFreeWord S F
          (nativeC60DVTransportEighteenStep S F word p))⁻¹
      simpa only [map_inv] using congrArg Inv.inv ih
  | trans p q ihp ihq =>
      change (nativeC60DVFullWordTransport S F word)
          (nativeC60DSFreeWord S F p * nativeC60DSFreeWord S F q) =
        nativeC60DVClosedFreeWord S F
          (nativeC60DVTransportEighteenStep S F word p) *
        nativeC60DVClosedFreeWord S F
          (nativeC60DVTransportEighteenStep S F word q)
      rw [map_mul, ihp, ihq]

/-- The physical finite AQ tree supplies the chronological word; its
transport of a source complete raw18D path is the above genuine map. -/
theorem nativeC60DVActualTree_full_naturality
    (tree : NativeK5DOContextTree)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y) :
    (nativeC60DVFullWordTransport S F (nativeK5DOTreeWord tree))
        (nativeC60DSFreeWord S F p) =
      nativeC60DVClosedFreeWord S F
        (nativeC60DVTransportEighteenStep S F
          (nativeK5DOTreeWord tree) p) :=
  nativeC60DVFullWordTransport_natural S F (nativeK5DOTreeWord tree) p

/-- Every original chronological AQ family has the SAME exact map
after changing only the binary pasting parentheses of its tree. -/
theorem nativeC60DVActualTree_word_refinement
    {left right : NativeK5DOContextTree}
    (h : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    nativeC60DVFullWordTransport S F (nativeK5DOTreeWord left) =
      nativeC60DVFullWordTransport S F (nativeK5DOTreeWord right) :=
  congrArg (nativeC60DVFullWordTransport S F)
    (nativeK5DOTreeWord_eq_of_steps_eq h)

/-- Same refinement principle for ORIGINAL full 18D raw Type-valued
paths in the explicit contextual target; no source data is replaced. -/
theorem nativeC60DVActualTree_step_refinement
    {left right : NativeK5DOContextTree}
    (h : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y) :
    (nativeK5DOTreeWord_eq_of_steps_eq h ▸
      nativeC60DVTransportEighteenStep S F
        (nativeK5DOTreeWord left) p) =
      nativeC60DVTransportEighteenStep S F
        (nativeK5DOTreeWord right) p := by
  have hdep :
      ∀ {w₁ w₂ : List Bool} (hw : w₁ = w₂),
        (hw ▸ nativeC60DVTransportEighteenStep S F w₁ p) =
          nativeC60DVTransportEighteenStep S F w₂ p := by
    intro w₁ w₂ hw
    cases hw
    rfl
  exact hdep (nativeK5DOTreeWord_eq_of_steps_eq h)

end ActualAQSeventeenToEighteen

#print axioms nativeC60DVClosedEighteenLayer
#print axioms NativeC60DVClosedEighteenGen
#print axioms nativeC60DVClosedEighteenSignature
#print axioms nativeC60DVTransportEighteenObj
#print axioms nativeC60DVTransportEighteenGen
#print axioms nativeC60DVTransportEighteenStep
#print axioms nativeC60DVTransportCompleteCode
#print axioms nativeC60DVFullWordTransport
#print axioms nativeC60DVFullWordTransport_natural
#print axioms nativeC60DVActualTree_full_naturality
#print axioms nativeC60DVActualTree_word_refinement
#print axioms nativeC60DVActualTree_step_refinement

end
end Kuu.F112.Physical
