import Kuu.F112.PolygonNativeC60PentagonNormalClosureDescent
import Mathlib.Tactic.Group

/-!
# F112-P94D3DU — exact normal-kernel stability and finite C60 AQ gauge descent

DT constructed the minimal NORMAL closure of ALL original, fully dependent
18D pentagon differences. DU addresses a different and necessary question:
which transformations of those ORIGINAL complete free words descend to DT's
explicitly selected relative quotient?

* For an arbitrary group endomorphism, descent through the pair-relation
  quotient is equivalent to preserving its EXACT normal kernel.
* This is equivalent to testing the transformed ORIGINAL pair relations
  modulo precisely that normal closure (no extra equalities).
* Specialize this criterion to ALL genuinely dependent C60 17D pentagon
  inputs, not a scalar/parity/BV observer.
* Produce a concrete finite-AQ-tree-indexed complete free-word defect
  from the physical AU source. It is provably nontrivial BEFORE quotient,
  but becomes the identity IN the selected relative quotient.
* Its genuine inner gauge action therefore descends and is invisible in
  that quotient; equality of different AQ tree descriptions with the
  same original step word respects this construction.

A general C60 contextual whiskering still needs an actual endomorphism of
the COMPLETE 18D generator-code group. Neither DR's 17D closed-context
transport nor this inner action silently manufactures that missing 18D
map, and neither DT nor DU asserts an original geometric 19D Type-valued
filler. The selected algebraic quotient, a DECLARED relative 19D
comparison, and an ORIGINAL C60 19D filler remain distinct.

No Gray, no new axiom, no sorry, no weakening of any existing no-go.
Strict Kuu remains primary; independent Kuu is one presentation.
All original raw 14D–18D witnesses and 107 public roots remain intact.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

section UniversalKernelTransport

variable {G : Type u} [Group G]

/-- A transport of COMPLETE free evidence may descend only if every
declared relation remains true AFTER transport, in the SAME quotient.
The target is an endomorphism of the selected relative presentation. -/
theorem nativeC60DURelationTransport_factor_iff
    (R : Set (G × G)) (τ : G →* G) :
    (∃ induced : NativeC60DTQuotient R →* NativeC60DTQuotient R,
      induced.comp (QuotientGroup.mk' (nativeC60DTNormalClosure R)) =
        (QuotientGroup.mk' (nativeC60DTNormalClosure R)).comp τ) ↔
      ∀ p : G × G, p ∈ R →
        (QuotientGroup.mk' (nativeC60DTNormalClosure R)) (τ p.1) =
          (QuotientGroup.mk' (nativeC60DTNormalClosure R)) (τ p.2) := by
  exact nativeC60DTQuotient_factor_iff R
    ((QuotientGroup.mk' (nativeC60DTNormalClosure R)).comp τ)

/-- Exact preservation of the original MINIMAL NORMAL KERNEL is
equivalent to the existence of the induced transport on the quotient.
The reverse implication uses the exact DT kernel theorem, not a
faithfulness assumption about the quotient. -/
theorem nativeC60DUNormalKernel_preservation_iff
    (R : Set (G × G)) (τ : G →* G) :
    (∀ x : G, x ∈ nativeC60DTNormalClosure R →
      τ x ∈ nativeC60DTNormalClosure R) ↔
    (∃ induced : NativeC60DTQuotient R →* NativeC60DTQuotient R,
      induced.comp (QuotientGroup.mk' (nativeC60DTNormalClosure R)) =
        (QuotientGroup.mk' (nativeC60DTNormalClosure R)).comp τ) := by
  let q : G →* NativeC60DTQuotient R :=
    QuotientGroup.mk' (nativeC60DTNormalClosure R)
  constructor
  · intro stable
    apply (nativeC60DTQuotient_factor_iff R (q.comp τ)).mpr
    intro p hp
    apply (QuotientGroup.eq_iff_div_mem).mpr
    rw [div_eq_mul_inv]
    have hmem : τ (p.1 * p.2⁻¹) ∈ nativeC60DTNormalClosure R :=
      stable _ (nativeC60DTPairDefect_mem R p hp)
    simpa only [map_mul, map_inv] using hmem
  · rintro ⟨induced, hcomp⟩ x hx
    have hxq : q x = 1 := by
      apply MonoidHom.mem_ker.mp
      change x ∈ (QuotientGroup.mk' (nativeC60DTNormalClosure R)).ker
      rw [nativeC60DTQuotient_kernel R]
      exact hx
    have hyq : q (τ x) = 1 := by
      calc
        q (τ x) = induced (q x) :=
          (DFunLike.congr_fun hcomp x).symm
        _ = 1 := by rw [hxq]; exact map_one induced
    have hker : τ x ∈ (QuotientGroup.mk'
        (nativeC60DTNormalClosure R)).ker :=
      MonoidHom.mem_ker.mpr hyq
    rw [nativeC60DTQuotient_kernel R] at hker
    exact hker

/-- Necessary AND sufficient test on precisely the selected original
pairs. It detects every obstruction to quotient descent for ANY
proposed complete-evidence transport. -/
theorem nativeC60DUNormalKernel_criterion
    (R : Set (G × G)) (τ : G →* G) :
    (∀ x : G, x ∈ nativeC60DTNormalClosure R →
      τ x ∈ nativeC60DTNormalClosure R) ↔
      ∀ p : G × G, p ∈ R →
        (QuotientGroup.mk' (nativeC60DTNormalClosure R)) (τ p.1) =
          (QuotientGroup.mk' (nativeC60DTNormalClosure R)) (τ p.2) :=
  (nativeC60DUNormalKernel_preservation_iff R τ).trans
    (nativeC60DURelationTransport_factor_iff R τ)

/-- Gauge conjugation of a COMPLETE noncommutative evidence group.
No generator is forgotten and no new 19D identification is made. -/
def nativeC60DUConjugation (c : G) : G →* G where
  toFun := fun x => c * x * c⁻¹
  map_one' := by group
  map_mul' x y := by group

/-- Any group receiver intertwines conjugation with conjugation
by the received gauge element. -/
theorem nativeC60DUConjugation_natural
    {H : Type v} [Group H] (ρ : G →* H) (c : G) :
    (nativeC60DUConjugation (ρ c)).comp ρ =
      ρ.comp (nativeC60DUConjugation c) := by
  apply MonoidHom.ext
  intro x
  change ρ c * ρ x * (ρ c)⁻¹ = ρ (c * x * c⁻¹)
  simp only [map_mul, map_inv]

/-- In particular all inner gauge actions descend to ANY exact
normal-closure quotient. This is genuine normal-subgroup covariance;
the quotient itself remains an explicitly chosen presentation. -/
theorem nativeC60DUConjugation_descends
    (R : Set (G × G)) (c : G) :
    ∃ induced : NativeC60DTQuotient R →* NativeC60DTQuotient R,
      induced.comp (QuotientGroup.mk' (nativeC60DTNormalClosure R)) =
        (QuotientGroup.mk' (nativeC60DTNormalClosure R)).comp
          (nativeC60DUConjugation c) :=
  ⟨nativeC60DUConjugation
      ((QuotientGroup.mk' (nativeC60DTNormalClosure R)) c),
    nativeC60DUConjugation_natural
      (QuotientGroup.mk' (nativeC60DTNormalClosure R)) c⟩

end UniversalKernelTransport

section ActualC60KernelDescent

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The necessary-and-sufficient finite C60 condition is tested
against EVERY ORIGINAL 17D-dependent four-path pentagon; there is no
substitution of a count, graph edge, parity, or chosen fake generator. -/
theorem nativeC60DUPentagonTransport_criterion
    (τ : NativeC60DTFullFree S F →* NativeC60DTFullFree S F) :
    (∀ x : NativeC60DTFullFree S F,
      x ∈ nativeC60DTPentagonNormalClosure S F →
        τ x ∈ nativeC60DTPentagonNormalClosure S F) ↔
      ∀ {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
        (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
        (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
        (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
        (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e),
        (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F))
          (τ (nativeC60DSFreeWord S F
            (nativeC60DRPentagonLong S F f g h k))) =
        (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F))
          (τ (nativeC60DSFreeWord S F
            (nativeC60DRPentagonShort S F f g h k))) := by
  refine (nativeC60DUNormalKernel_criterion
    (nativeC60DTPentagonPairs S F) τ).trans ?_
  constructor
  · intro hall a b c d e f g h k
    exact hall _ (nativeC60DTPentagon_pair_mem S F f g h k)
  · intro hall pair hp
    rcases hp with ⟨a, b, c, d, e, f, g, h, k, rfl⟩
    exact hall f g h k

/-- A transformed genuine pentagon with different quotient images is
an explicit obstruction to a purported global 18D transport descent. -/
theorem nativeC60DUPentagonTransport_obstructed
    (τ : NativeC60DTFullFree S F →* NativeC60DTFullFree S F)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (bad : (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F))
        (τ (nativeC60DSFreeWord S F
          (nativeC60DRPentagonLong S F f g h k))) ≠
      (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F))
        (τ (nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k)))) :
    ¬ ∃ induced : NativeC60DTPentagonQuotient S F →*
        NativeC60DTPentagonQuotient S F,
      induced.comp (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F)) =
        (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F)).comp τ := by
  intro hfactor
  have hall := (nativeC60DURelationTransport_factor_iff
    (nativeC60DTPentagonPairs S F) τ).mp hfactor
  exact bad (hall _ (nativeC60DTPentagon_pair_mem S F f g h k))

end ActualC60KernelDescent

section PhysicalAQInnerGauge

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

/-- TRUE complete free-group defect associated to a physical C60 AU
source in a finite AQ context tree. Source and target are actual
17D-dependent routes, and all complete 18D generator codes survive. -/
def nativeK5DUPhysicalAQDefect
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    NativeC60DTFullFree (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  let S := nativeK5AXKuuSignature W
  let F := nativeK5BCFrame W
  let gen := nativeC60BCShiftGen S F (nativeK5DOTreeWord tree)
    (nativeK5CEPhysicalAUGenerator W)
  let route := nativeC60DQSeventeenRoundtrip S F gen
  nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F
    route route route route) *
    (nativeC60DSFreeWord S F
      (nativeC60DRPentagonShort S F route route route route))⁻¹

/-- The physically constructed defect belongs to DT's minimal normal
kernel; it does NOT thereby become a geometric 19D comparison. -/
theorem nativeK5DUPhysicalAQDefect_mem
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    nativeK5DUPhysicalAQDefect W tree ∈
      nativeC60DTPentagonNormalClosure
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) := by
  unfold nativeK5DUPhysicalAQDefect
  exact nativeC60DTPentagon_defect_mem
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) _ _ _ _

/-- This is not a vacuous chosen relation: the same COMPLETE physical
18D difference is nonidentity in the ORIGINAL free evidence group. -/
theorem nativeK5DUPhysicalAQDefect_ne_one
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    nativeK5DUPhysicalAQDefect W tree ≠ 1 := by
  unfold nativeK5DUPhysicalAQDefect
  intro hone
  exact nativeC60DSPentagon_free_ne
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) _ _ _ _
    (eq_of_mul_inv_eq_one hone)

/-- The actual nontrivial full-evidence defect becomes 1 ONLY in
the explicitly selected algebraic pentagon quotient. -/
theorem nativeK5DUPhysicalAQDefect_quotient_one
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)))
      (nativeK5DUPhysicalAQDefect W tree) = 1 := by
  apply MonoidHom.mem_ker.mp
  rw [nativeC60DTPentagon_kernel_exact]
  exact nativeK5DUPhysicalAQDefect_mem W tree

/-- A concrete finite-AQ-tree-indexed INNER gauge transformation of
the original complete 18D group. It is induced by an actual original
AU pentagon word, not claimed to equal all 17D-context whiskerings. -/
def nativeK5DUPhysicalAQInnerTransport
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    NativeC60DTFullFree (nativeK5AXKuuSignature W) (nativeK5BCFrame W) →*
      NativeC60DTFullFree (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  nativeC60DUConjugation (nativeK5DUPhysicalAQDefect W tree)

/-- The finite-AQ physical inner gauge action survives quotienting;
in fact the nontrivial kernel defect becomes invisible, so the induced
action is the IDENTITY. This is algebraic gauge covariance, not a
new assertion of original geometric 19D filling. -/
theorem nativeK5DUPhysicalAQInnerTransport_quotient_identity
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W))).comp
        (nativeK5DUPhysicalAQInnerTransport W tree) =
    QuotientGroup.mk' (nativeC60DTPentagonNormalClosure
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) := by
  have hdef := nativeK5DUPhysicalAQDefect_quotient_one W tree
  apply MonoidHom.ext
  intro x
  change (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)))
      (nativeK5DUPhysicalAQDefect W tree * x *
        (nativeK5DUPhysicalAQDefect W tree)⁻¹) =
      (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W))) x
  simp only [map_mul, map_inv, hdef, one_mul, inv_one, mul_one]

/-- This explicit identity action supplies the actual quotient factor
without asserting that the unreduced COMPLETE evidence was equal. -/
theorem nativeK5DUPhysicalAQInnerTransport_factors
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    ∃ induced : NativeC60DTPentagonQuotient
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) →*
          NativeC60DTPentagonQuotient
            (nativeK5AXKuuSignature W) (nativeK5BCFrame W),
      induced.comp (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W))) =
        (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W))).comp
            (nativeK5DUPhysicalAQInnerTransport W tree) :=
  ⟨MonoidHom.id _, (nativeK5DUPhysicalAQInnerTransport_quotient_identity W tree).symm⟩

/-- AQ tree regrouping with the same ACTUAL finite context word
preserves the physical defect, not merely its BV or parity shadow. -/
theorem nativeK5DUPhysicalAQDefect_refinement
    (W : NativeK5StructuralThirteenCell p U V)
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    nativeK5DUPhysicalAQDefect W left =
      nativeK5DUPhysicalAQDefect W right := by
  have hword := nativeK5DOTreeWord_eq_of_steps_eq hsteps
  unfold nativeK5DUPhysicalAQDefect
  rw [hword]

/-- The induced complete-code gauge endomorphisms agree for finite
AQ refinements with equal original flattened step words. -/
theorem nativeK5DUPhysicalAQInnerTransport_refinement
    (W : NativeK5StructuralThirteenCell p U V)
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    nativeK5DUPhysicalAQInnerTransport W left =
      nativeK5DUPhysicalAQInnerTransport W right := by
  unfold nativeK5DUPhysicalAQInnerTransport
  rw [nativeK5DUPhysicalAQDefect_refinement W hsteps]

end PhysicalAQInnerGauge

#print axioms nativeC60DURelationTransport_factor_iff
#print axioms nativeC60DUNormalKernel_preservation_iff
#print axioms nativeC60DUNormalKernel_criterion
#print axioms nativeC60DUConjugation
#print axioms nativeC60DUConjugation_natural
#print axioms nativeC60DUConjugation_descends
#print axioms nativeC60DUPentagonTransport_criterion
#print axioms nativeC60DUPentagonTransport_obstructed
#print axioms nativeK5DUPhysicalAQDefect
#print axioms nativeK5DUPhysicalAQDefect_mem
#print axioms nativeK5DUPhysicalAQDefect_ne_one
#print axioms nativeK5DUPhysicalAQDefect_quotient_one
#print axioms nativeK5DUPhysicalAQInnerTransport
#print axioms nativeK5DUPhysicalAQInnerTransport_quotient_identity
#print axioms nativeK5DUPhysicalAQInnerTransport_factors
#print axioms nativeK5DUPhysicalAQDefect_refinement
#print axioms nativeK5DUPhysicalAQInnerTransport_refinement

end
end Kuu.F112.Physical
