import Kuu.F112.PolygonNativeC60FiniteWhiskeringContextEquivariance

/-!
# F112-P94D3BH — Peiffer squares are exactly selected replacements

BG constructs a conditionally equivariant context action on the genuine
raw C60 16D comparison bundles and the strict Kuu full-arrow bundles.
BH identifies the exact local condition for Peiffer coherence:

  equality of the two whole dependent strict-arrow bundles
  <=> equality of the actual RL/LR strict morphisms
  <=> a selected Kuu.Replaceable proof for their typed raw words.

No numerical observer or group-valued holonomy defines the quotient.
The global PeifferSound condition is equivalent to equality of EVERY
typed pair's full-arrow Peiffer square. Under BG's explicit two-letter
compatibility, closure under *all* finite C60 contexts holds iff it
holds at the original pair. Non-replaceability after a context is a
sound obstruction to replaceability before context, not conversely.

The supplied typed left/right whiskering remains a separate hypothesis;
there is no unconditional original geometric 16-cell, middle-four law,
global strict 3/n-category or hyperdescent assertion.
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

/-- Equality of entire dependent arrow bundles is EXACTLY equality
of the two selected strict homs at their original shared endpoints.
There is no identification of distinct 15D objects. -/
theorem nativeC60BHPeifferSquare_iff_strict {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (q r : NativeC60BGRawArrowBundle S F) :
    nativeC60BGHorizontalRLBundle S F H q r =
        nativeC60BGHorizontalLRBundle S F H q r ↔
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (nativeC60BBHorizontalRL H q.2 r.2) =
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (nativeC60BBHorizontalLR H q.2 r.2) := by
  constructor
  · intro h
    exact eq_of_heq (Sigma.mk.inj_iff.mp h).2
  · intro h
    exact congrArg
      (fun k : (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
            (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
            ⟨H.obj q.1.1 r.1.1⟩ ⟶
          (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
            (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
            ⟨H.obj q.1.2 r.1.2⟩ =>
        (⟨(H.obj q.1.1 r.1.1, H.obj q.1.2 r.1.2), k⟩ :
          NativeC60BEStrictArrowBundle S F)) h

/-- The local dependent Peiffer square is coherent IF AND ONLY IF
the genuine raw typed RL and LR words lie in the selected Kuu
replacement closure. This is NOT an observational equality. -/
theorem nativeC60BHPeifferSquare_iff_replaceable {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (q r : NativeC60BGRawArrowBundle S F) :
    nativeC60BGHorizontalRLBundle S F H q r =
        nativeC60BGHorizontalLRBundle S F H q r ↔
      Kuu.Replaceable (nativeC60AZStrictRelations
        (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)))
        (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
          (nativeC60BBHorizontalRL H q.2 r.2))
        (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
          (nativeC60BBHorizontalLR H q.2 r.2)) :=
  (nativeC60BHPeifferSquare_iff_strict S F H q r).trans
    (nativeC60AZStrictStep_exact (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BBHorizontalRL H q.2 r.2)
      (nativeC60BBHorizontalLR H q.2 r.2))

/-- The genuinely ALL-hom Peiffer property of BB is EQUIVALENT
to the exact full-bundle Peiffer square at every pair of original
proof-relevant 16D comparisons. A selected strict quotient is used
throughout, not a disjoint union of observer values. -/
theorem nativeC60BHPeifferSound_iff_fullBundles {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F)) :
    NativeC60BBPeifferSound (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) H ↔
      ∀ (q r : NativeC60BGRawArrowBundle S F),
        nativeC60BGHorizontalRLBundle S F H q r =
          nativeC60BGHorizontalLRBundle S F H q r := by
  constructor
  · intro hp q r
    exact (nativeC60BHPeifferSquare_iff_strict S F H q r).mpr (hp q.2 r.2)
  · intro hp a b c d f g
    exact (nativeC60BHPeifferSquare_iff_strict S F H
      (⟨(a, b), f⟩ : NativeC60BGRawArrowBundle S F)
      (⟨(c, d), g⟩ : NativeC60BGRawArrowBundle S F)).mp
        (hp ⟨(a, b), f⟩ ⟨(c, d), g⟩)

/-- A witness to selected Peiffer coherence at a raw pair remains
selected-replaceable AFTER genuine C60 context transport, provided
the explicitly supplied two-sided whiskering equivariance holds. -/
theorem nativeC60BHReplacement_transport {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (word : List Bool)
    (he : NativeC60BGWhiskeringEquivariant S F H word)
    (q r : NativeC60BGRawArrowBundle S F)
    (hp : Kuu.Replaceable
      (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalRL H q.2 r.2))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalLR H q.2 r.2))) :
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
          (nativeC60BGRawContext S F word r).2)) := by
  apply (nativeC60BHPeifferSquare_iff_replaceable S F H
    (nativeC60BGRawContext S F word q)
    (nativeC60BGRawContext S F word r)).mp
  exact nativeC60BGPeifferSquare_transport S F H word he q r
    ((nativeC60BHPeifferSquare_iff_replaceable S F H q r).mpr hp)

/-- A failure of Kuu's selected-replacement relation AFTER a context
is an obstruction already at its original source. Faithfulness is
needed for the reverse implication, and is not assumed. -/
theorem nativeC60BHReplacement_obstruction_pullback {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (word : List Bool)
    (he : NativeC60BGWhiskeringEquivariant S F H word)
    (q r : NativeC60BGRawArrowBundle S F)
    (hne : ¬ Kuu.Replaceable
      (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalRL H
          (nativeC60BGRawContext S F word q).2
          (nativeC60BGRawContext S F word r).2))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalLR H
          (nativeC60BGRawContext S F word q).2
          (nativeC60BGRawContext S F word r).2))) :
    ¬ Kuu.Replaceable
      (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalRL H q.2 r.2))
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
        (nativeC60BBHorizontalLR H q.2 r.2)) := by
  intro hp
  exact hne (nativeC60BHReplacement_transport S F H word he q r hp)

/-- With all finite-word binary equivariance, the selected Peiffer
square is replaceable at EVERY contextual image IF AND ONLY IF it is
replaceable at the unshifted source. The reverse follows by the
empty context, not by a falsely assumed faithful nonempty action. -/
theorem nativeC60BHReplacement_all_iff_base {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (he : ∀ word, NativeC60BGWhiskeringEquivariant S F H word)
    (q r : NativeC60BGRawArrowBundle S F) :
    (∀ word : List Bool,
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
            (nativeC60BGRawContext S F word r).2))) ↔
      Kuu.Replaceable
        (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)))
        (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
          (nativeC60BBHorizontalRL H q.2 r.2))
        (nativeC60AZRawArrow (nativeC60BCClosedSignature S F)
          (nativeC60BBHorizontalLR H q.2 r.2)) := by
  constructor
  · intro h
    simpa only [nativeC60BGRawContext_nil S F] using h []
  · intro h word
    exact nativeC60BHReplacement_transport S F H word (he word) q r h

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

/-- For the original physical C60, unconditional all-hom Peiffer
coherence is exactly a universal full-dependent-bundle equality,
not automatically supplied by finite strict functors. -/
theorem nativeK5BHPhysicalPeifferSound_iff_fullBundles
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W)) :
    NativeC60BBPeifferSound (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W)) Hh ↔
      ∀ (q r : NativeC60BGRawArrowBundle
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
        nativeC60BGHorizontalRLBundle
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh q r =
        nativeC60BGHorizontalLRBundle
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh q r :=
  nativeC60BHPeifferSound_iff_fullBundles
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh

end PhysicalC60

#print axioms nativeC60BHPeifferSquare_iff_strict
#print axioms nativeC60BHPeifferSquare_iff_replaceable
#print axioms nativeC60BHPeifferSound_iff_fullBundles
#print axioms nativeC60BHReplacement_transport
#print axioms nativeC60BHReplacement_obstruction_pullback
#print axioms nativeC60BHReplacement_all_iff_base
#print axioms nativeK5BHPhysicalPeifferSound_iff_fullBundles

end
end Kuu.F112.Physical
