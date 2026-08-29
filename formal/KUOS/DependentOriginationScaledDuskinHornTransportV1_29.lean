import KUOS.DependentOriginationNormalizationChoiceInvariantV1_28

namespace KUOS.DependentOriginationScaledDuskinHornTransportV1_29

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Simplicial
open Opposite
open scoped Bicategory
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27

universe u v w

/-!
# Scaled Duskin horn transport v1.29

This layer separates three claims that should not be conflated.

1. A scaled simplicial map sends any scaled horn-extension problem forward.
2. A scaled filler for the source problem sends forward to a scaled filler of
   the transported target problem.
3. A strictly-unitary model equivalence between models in the same universe
   triple already supplies the underlying simplicial map of global Duskin nerves
   and preserves nondegenerate thin triangles. Full thinness preservation,
   including degenerate triangles, is therefore isolated as an explicit
   certificate until the corresponding simplicial degeneracy calculation is
   promoted to a theorem.

The same-universe condition in the global Duskin specialization is exactly the
boundary of `normalizedDuskinNerveMap` from v1.27. Degreewise Duskin simplex
transport remains universe-polymorphic there, but a single bundled simplicial
map is only constructed for one universe triple.

No target-side fibrancy theorem is claimed from a one-way map alone: a filler
for every source admissible horn yields fillers only for the transported image
of those horns in the target.
-/

/-- Push a scaled horn-extension problem forward along a scaled simplicial map. -/
def mapScaledHornProblem
    {X Y : SSet}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y}
    (hf : IsScaledMap sX sY f)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    ScaledHornExtensionProblem Y sY n i where
  hornScaling := P.hornScaling
  simplexScaling := P.simplexScaling
  inclusion_scaled := P.inclusion_scaled
  hornMap := P.hornMap ≫ f
  hornMap_scaled := P.hornMap_scaled.comp hf

/-- A source scaled filler pushes forward to a filler of the transported horn problem. -/
def mapScaledHornFiller
    {X Y : SSet}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y}
    (hf : IsScaledMap sX sY f)
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem X sX n i}
    (Q : ScaledHornFiller P) :
    ScaledHornFiller (mapScaledHornProblem hf P) where
  simplexMap := Q.simplexMap ≫ f
  extends_horn := by
    rw [Category.assoc, ← Q.extends_horn]
  simplexMap_scaled := Q.simplexMap_scaled.comp hf

/-- Nonempty source filler data therefore transports forward. -/
theorem mapScaledHornFiller_nonempty
    {X Y : SSet}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y}
    (hf : IsScaledMap sX sY f)
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem X sX n i}
    (hP : Nonempty (ScaledHornFiller P)) :
    Nonempty (ScaledHornFiller (mapScaledHornProblem hf P)) := by
  rcases hP with ⟨Q⟩
  exact ⟨mapScaledHornFiller hf Q⟩

/-- Compatibility of chosen admissible horn families with a scaled map. -/
structure ScaledHornFamilyMap
    {X Y : SSet}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y}
    (hf : IsScaledMap sX sY f)
    (FX : ScaledHornFamily X sX)
    (FY : ScaledHornFamily Y sY) : Prop where
  admissible_preserved :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      FX.admissible P → FY.admissible (mapScaledHornProblem hf P)

/-- A scaled horn filler theorem pushes forward for every admissible source problem. -/
theorem admissibleFiller_forward
    {X Y : SSet}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y}
    (hf : IsScaledMap sX sY f)
    (FX : ScaledHornFamily X sX)
    (FY : ScaledHornFamily Y sY)
    (Hfam : ScaledHornFamilyMap hf FX FY)
    [HX : HasScaledHornFillers X sX FX]
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i)
    (hP : FX.admissible P)
    (h0 : 0 < i) (hn : i < Fin.last n) :
    FY.admissible (mapScaledHornProblem hf P) ∧
      Nonempty (ScaledHornFiller (mapScaledHornProblem hf P)) := by
  constructor
  · exact Hfam.admissible_preserved P hP
  · exact mapScaledHornFiller_nonempty hf (HX.fill P hP h0 hn)

/-! ## Global Duskin specialization -/

/--
The remaining datum needed to regard the normalized global Duskin map as a
full scaled map. Version 1.27 constructs this simplicial map for source and
target models in one universe triple, and v1.29 keeps exactly that boundary.
-/
structure FullScaledDuskinMapCertificate
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C) : Prop where
  map_scaled :
    IsScaledMap (duskinScaling B) (duskinScaling C)
      (normalizedDuskinNerveMap E)

/-- Re-export the scaled map from the full certificate. -/
def normalizedDuskinScaledMap
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {E : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (H : FullScaledDuskinMapCertificate E) :
    IsScaledMap (duskinScaling B) (duskinScaling C)
      (normalizedDuskinNerveMap E) :=
  H.map_scaled

/-- The nondegenerate portion of full scaling preservation is already theorem-level. -/
theorem normalizedDuskin_nonDegenerateThin_preserved
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 2)
    (hnd : ¬ IsDegenerateDuskinTwoSimplex σ)
    (hthin : (duskinScaling B).thin σ) :
    (duskinScaling C).thin
      ((normalizedDuskinNerveMap E).app (op ⦋2⦌) σ) := by
  simpa using nondegenerateThin_transport_isThin E σ hnd hthin

/-- A full scaled Duskin map transports every scaled horn problem forward. -/
def transportGlobalDuskinHornProblem
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {E : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (H : FullScaledDuskinMapCertificate E)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem
      (duskinNerve B) (duskinScaling B) n i) :
    ScaledHornExtensionProblem
      (duskinNerve C) (duskinScaling C) n i :=
  mapScaledHornProblem H.map_scaled P

/-- Every scaled filler of a source global Duskin horn transports to the target image horn. -/
def transportGlobalDuskinHornFiller
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {E : StrictlyUnitaryBicategoricalModelEquivalence B C}
    (H : FullScaledDuskinMapCertificate E)
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem
      (duskinNerve B) (duskinScaling B) n i}
    (Q : ScaledHornFiller P) :
    ScaledHornFiller (transportGlobalDuskinHornProblem H P) :=
  mapScaledHornFiller H.map_scaled Q

/-!
The exact v1.29 boundary is therefore:

```text
scaled simplicial map
  -> scaled horn problem forward transport
  -> scaled filler forward transport

same-universe strictly-unitary model equivalence
  -> normalized Duskin simplicial map                 -- v1.27
  -> nondegenerate thin preservation                  -- v1.27/v1.29
  + FullScaledDuskinMapCertificate                    -- explicit remaining boundary
  -> all scaled horn/filler data transport forward    -- v1.29
```

A one-way scaled map does not imply all target horns are images of source horns,
so target fibrancy is not inferred without an inverse/essential-surjectivity
statement at the scaled horn-presentation level.
-/

end KUOS.DependentOriginationScaledDuskinHornTransportV1_29
