import Kuu.F112.PolygonNativeC60FinitePeifferReplacementCriterion

/-!
# F112-P94D3BI — finite-context Peiffer criterion for middle-four

BG proves that the finite-word equivariance gate for two independently
supplied, genuinely typed 16D C60 whiskerings reduces to the two original
one-letter frames. BH identifies exact Peiffer bundle equality with Kuu's
SELECTED compositional replacement relation.

BI now proves, under the explicit two original frame gates, that:
* universal typed PeifferSound is equivalent to selected replaceability
  for EVERY raw dependent pair at EVERY finite C60 context;
* exact all-hom strict interchange is equivalent to that same finite
  criterion, provided the horizontal operations separately descend;
* with genuine left/right functoriality, true middle-four is equivalent
  to that finite criterion;
* one witnessed failure of selected replacement at a finite context
  obstructs the full strict interchange, and a distinguished group-valued
  holonomy gives a sufficient obstruction.

All hypotheses remain honest mathematical obligations. No conclusion
asserts unconditional horizontal composition, the original geometric
16-cell, full P92B descent, global strict n-category or hyperdescent.
No Gray, new axioms, sorry, admit or observer-defined quotient.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- Finite C60 contexts of all *actual typed* source/target pairs obey
the selected strict Kuu Peiffer replacement. This is a proposition
about the existing quotient's declared compositional closure, not
about equality under any chosen numerical or group-valued observer. -/
def NativeC60BIAllContextPeifferReplacement {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F)) : Prop :=
  ∀ (q r : NativeC60BGRawArrowBundle S F) (word : List Bool),
    Kuu.Replaceable
      (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalRL H
          (nativeC60BGRawContext S F word q).2
          (nativeC60BGRawContext S F word r).2))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalLR H
          (nativeC60BGRawContext S F word q).2
          (nativeC60BGRawContext S F word r).2))

/-- Main finite-context Peiffer criterion. BOTH physical singleton
C60 gates are explicit hypotheses; BE/BF unary strict action does
not magically establish two-variable whiskering equivariance. -/
theorem nativeC60BIAllContext_iff_peiffer {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (hl : NativeC60BGWhiskeringEquivariant S F H [false])
    (hr : NativeC60BGWhiskeringEquivariant S F H [true]) :
    NativeC60BIAllContextPeifferReplacement S F H ↔
      NativeC60BBPeifferSound (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H := by
  have he : ∀ word, NativeC60BGWhiskeringEquivariant S F H word :=
    (nativeC60BGWhiskeringEquivariant_all_iff_letters S F H).mpr ⟨hl, hr⟩
  constructor
  · intro hp
    apply (nativeC60BHPeifferSound_iff_fullBundles S F H).mpr
    intro q r
    apply (nativeC60BHPeifferSquare_iff_replaceable S F H q r).mpr
    exact (nativeC60BHReplacement_all_iff_base S F H he q r).mp (hp q r)
  · intro hp q r word
    have hbase :
        nativeC60BGHorizontalRLBundle S F H q r =
          nativeC60BGHorizontalLRBundle S F H q r :=
      (nativeC60BHPeifferSound_iff_fullBundles S F H).mp hp q r
    exact nativeC60BHReplacement_transport S F H word (he word) q r
      ((nativeC60BHPeifferSquare_iff_replaceable S F H q r).mp hbase)

/-- Universal equality of strict horizontal morphisms is *exactly*
the all-finite-context selected replacement condition, if the given
two whiskerings separately descend to the already selected quotient.
No new binary operation is postulated by this theorem. -/
theorem nativeC60BIStrictInterchange_iff_context {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (hc : NativeC60BBWhiskeringCongruent (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H)
    (hl : NativeC60BGWhiskeringEquivariant S F H [false])
    (hr : NativeC60BGWhiskeringEquivariant S F H [true]) :
    (∀ {a b c d : L.Total}
      (f : (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨a⟩ ⟶
        (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨b⟩)
      (g : (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨c⟩ ⟶
        (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨d⟩),
      nativeC60BBStrictHorizontalRL (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H hc f g =
        nativeC60BBStrictHorizontalLR (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H hc f g) ↔
      NativeC60BIAllContextPeifferReplacement S F H :=
  (nativeC60BBStrictInterchange_iff (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H hc).trans
      (nativeC60BIAllContext_iff_peiffer S F H hl hr).symm

/-- A genuine full middle-four interchange (horizontal with vertical
strict composition) is equivalent to the contextwise selected relation,
under separate left/right whiskering functoriality. This is stronger
than a claim about object action or observed Peiffer numbers. -/
theorem nativeC60BIMiddleFour_iff_context {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (hf : NativeC60BBWhiskeringFunctorial (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H)
    (hl : NativeC60BGWhiskeringEquivariant S F H [false])
    (hr : NativeC60BGWhiskeringEquivariant S F H [true]) :
    (∀ {a b e c d k : L.Total}
      (f : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
      (f' : NativeC60AXStep (nativeC60BCClosedSignature S F) b e)
      (g : NativeC60AXStep (nativeC60BCClosedSignature S F) c d)
      (g' : NativeC60AXStep (nativeC60BCClosedSignature S F) d k),
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (nativeC60BBHorizontalRL H (.trans f f') (.trans g g')) =
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
            (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
            (nativeC60BBHorizontalRL H f g) ≫
          nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
            (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
            (nativeC60BBHorizontalRL H f' g')) ↔
      NativeC60BIAllContextPeifferReplacement S F H :=
  (nativeC60BBHorizontal_middleFour_iff (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H hf).trans
      (nativeC60BIAllContext_iff_peiffer S F H hl hr).symm

/-- An explicit contextual witness of failure of the already selected
Kuu replacement closure. A witness is not manufactured here. -/
def NativeC60BIContextPeifferFailure {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (word : List Bool) (q r : NativeC60BGRawArrowBundle S F) : Prop :=
  ¬ Kuu.Replaceable
      (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalRL H
          (nativeC60BGRawContext S F word q).2
          (nativeC60BGRawContext S F word r).2))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalLR H
          (nativeC60BGRawContext S F word q).2
          (nativeC60BGRawContext S F word r).2))

/-- A SINGLE contextual Peiffer failure blocks universal all-hom
strict interchange. No observer or unproved faithfulness is needed. -/
theorem nativeC60BIContextFailure_no_interchange {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (hc : NativeC60BBWhiskeringCongruent (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H)
    (hl : NativeC60BGWhiskeringEquivariant S F H [false])
    (hr : NativeC60BGWhiskeringEquivariant S F H [true])
    (word : List Bool) (q r : NativeC60BGRawArrowBundle S F)
    (hne : NativeC60BIContextPeifferFailure S F H word q r) :
    ¬ (∀ {a b c d : L.Total}
      (f : (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨a⟩ ⟶
        (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨b⟩)
      (g : (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨c⟩ ⟶
        (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨d⟩),
      nativeC60BBStrictHorizontalRL (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H hc f g =
        nativeC60BBStrictHorizontalLR (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H hc f g) := by
  intro h
  have hh := (nativeC60BIStrictInterchange_iff_context S F H hc hl hr).mp h
  exact hne (hh q r word)

/-- If a group-valued holonomy, respecting the independently selected
Kuu replacement relations, distinguishes a pair of *contextual* Peiffer
routes, global selected Peiffer coherence is impossible. Holonomy is a
one-way detector, NEVER the definition of replacement equality. -/
theorem nativeC60BIHolonomy_context_obstruction {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (hl : NativeC60BGWhiskeringEquivariant S F H [false])
    (hr : NativeC60BGWhiskeringEquivariant S F H [true])
    {G : Type v} [Group G]
    (weight : ∀ {x y}, (nativeC60BCClosedSignature S F).Gen x y → G)
    (hw : NativeC60AZWeightsRespect (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) weight)
    (word : List Bool) (q r : NativeC60BGRawArrowBundle S F)
    (hne :
      nativeC60AZHolonomy (nativeC60BCClosedSignature S F) weight
        (nativeC60BBHorizontalRL H
          (nativeC60BGRawContext S F word q).2
          (nativeC60BGRawContext S F word r).2) ≠
      nativeC60AZHolonomy (nativeC60BCClosedSignature S F) weight
        (nativeC60BBHorizontalLR H
          (nativeC60BGRawContext S F word q).2
          (nativeC60BGRawContext S F word r).2)) :
    ¬ NativeC60BIAllContextPeifferReplacement S F H := by
  intro hall
  have hp : NativeC60BBPeifferSound (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H :=
    (nativeC60BIAllContext_iff_peiffer S F H hl hr).mp hall
  exact (nativeC60BBPeiffer_holonomy_obstruction
    (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    H weight hw
    (nativeC60BGRawContext S F word q).2
    (nativeC60BGRawContext S F word r).2 hne) hp

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

/-- The actual original thirteen-cell C60 carrier specializes the
finite context replacement/Peiffer equivalence, with BOTH independent
singleton gates still explicit. -/
theorem nativeK5BIPhysical_allContext_iff_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (hl : NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [false])
    (hr : NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [true]) :
    NativeC60BIAllContextPeifferReplacement
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh ↔
      NativeC60BBPeifferSound (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W)) Hh :=
  nativeC60BIAllContext_iff_peiffer
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh hl hr

end PhysicalC60

#print axioms NativeC60BIAllContextPeifferReplacement
#print axioms nativeC60BIAllContext_iff_peiffer
#print axioms nativeC60BIStrictInterchange_iff_context
#print axioms nativeC60BIMiddleFour_iff_context
#print axioms NativeC60BIContextPeifferFailure
#print axioms nativeC60BIContextFailure_no_interchange
#print axioms nativeC60BIHolonomy_context_obstruction
#print axioms nativeK5BIPhysical_allContext_iff_peiffer

end
end Kuu.F112.Physical
