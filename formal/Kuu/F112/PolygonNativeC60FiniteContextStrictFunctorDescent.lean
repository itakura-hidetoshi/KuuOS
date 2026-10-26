import Kuu.F112.PolygonNativeC60FiniteContextClosedHigherComparisons

/-!
# F112-P94D3BD — strict descent of genuine C60 finite-context actions

BC constructs typed 16D context transformations of actual C60 15D proof
evidence. BD connects those transformations to the existing strict Kuu
quotients. A context is a functor on the freely generated comparison category;
its descent through a SELECTED higher strict quotient is equivalent to
congruence on the independently declared higher comparisons.

For the no-extra-relations strict quotient this construction is unconditional,
for arbitrary finite context words. For a NEXT specified higher signature,
descent is exactly the generator-compatibility obligation, not automatic.
The categorical action carries real C60 naturality arrows between distinct
strict objects. BB's middle-four/Peiffer criterion remains a separate
binary-horizontal coherence obligation, not granted by these unary functors.

No scalar-kernel quotient, universal geometric 16-cell, invented whiskering,
Gray, new axioms, sorry/admit or global strict n/hyperdescent claims.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- A genuine BC finite context maps typed AX generators to typed AX
generators. Its image is in the strict Kuu category, not in a discrete
observer that forgets higher comparisons. -/
def nativeC60BDContextPrefunctor {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (steps : List Bool) :
    NativeC60AZStrictObj (nativeC60BCClosedSignature S F) ⥤q
      NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R where
  obj x := (nativeC60AZStrictProject _ R).obj
    ⟨nativeC60BCContextTotal F steps x.val⟩
  map c := nativeC60AZStrictStep _ R
    (nativeC60BCMapClosedStep S F steps c)

def nativeC60BDContextRawFunctor {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (steps : List Bool) :
    Kuu.Raw (NativeC60AZStrictObj (nativeC60BCClosedSignature S F)) ⥤
      NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R :=
  Paths.lift (nativeC60BDContextPrefunctor S F R steps)

theorem nativeC60BDContextRawFunctor_arrow {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (steps : List Bool) {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    (nativeC60BDContextRawFunctor S F R steps).map
      (nativeC60AZRawArrow (nativeC60BCClosedSignature S F) c) =
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
      (nativeC60BCMapClosedStep S F steps c) :=
  Paths.lift_toPath (nativeC60BDContextPrefunctor S F R steps) c

/-- A selected relation is context-stable exactly when a transported
declared higher comparison remains equal in the EXISTING strict quotient. -/
def NativeC60BDContextCongruence {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (steps : List Bool) : Prop :=
  ∀ {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
    R c d →
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
          (nativeC60BCMapClosedStep S F steps c) =
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
          (nativeC60BCMapClosedStep S F steps d)

/-- The structural unit/composition/inverse laws require no new axioms or
identifications. The ONLY new obligation is the selected higher relation. -/
theorem nativeC60BDContextRawFunctor_respects_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (steps : List Bool) :
    Kuu.Respects (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F) R)
      (nativeC60BDContextRawFunctor S F R steps) ↔
      NativeC60BDContextCongruence S F R steps := by
  constructor
  · intro hr a b c d hcd
    have heq := hr _ _ _ _ (NativeC60AZStrictRel.declared hcd)
    simpa only [nativeC60BDContextRawFunctor_arrow] using heq
  · intro h x y f g rel
    let T := nativeC60BCClosedSignature S F
    let P := nativeC60BDContextRawFunctor S F R steps
    cases rel with
    | ident a =>
        calc
          P.map (nativeC60AZRawArrow T (.refl a)) =
              nativeC60AZStrictStep T R
                (nativeC60BCMapClosedStep S F steps (.refl a)) :=
              nativeC60BDContextRawFunctor_arrow S F R steps _
          _ = 𝟙 ((nativeC60AZStrictProject T R).obj
                ⟨nativeC60BCContextTotal F steps a⟩) :=
              nativeC60AZStrictStep_refl T R _
          _ = P.map Quiver.Path.nil := rfl
    | compose c d =>
        calc
          P.map (nativeC60AZRawArrow T (.trans c d)) =
              nativeC60AZStrictStep T R
                (nativeC60BCMapClosedStep S F steps (.trans c d)) :=
              nativeC60BDContextRawFunctor_arrow S F R steps _
          _ = nativeC60AZStrictStep T R
                (nativeC60BCMapClosedStep S F steps c) ≫
              nativeC60AZStrictStep T R
                (nativeC60BCMapClosedStep S F steps d) :=
              nativeC60AZStrictStep_comp T R _ _
          _ = P.map ((nativeC60AZRawArrow T c).comp
                (nativeC60AZRawArrow T d)) := by
              rw [P.map_comp]
              rw [nativeC60BDContextRawFunctor_arrow,
                  nativeC60BDContextRawFunctor_arrow]
    | inverseLeft c =>
        calc
          P.map ((nativeC60AZRawArrow T c).comp
              (nativeC60AZRawArrow T (.symm c))) =
            P.map (nativeC60AZRawArrow T c) ≫
              P.map (nativeC60AZRawArrow T (.symm c)) :=
              P.map_comp _ _
          _ = nativeC60AZStrictStep T R
                (nativeC60BCMapClosedStep S F steps c) ≫
              nativeC60AZStrictStep T R
                (.symm (nativeC60BCMapClosedStep S F steps c)) := by
              rw [nativeC60BDContextRawFunctor_arrow,
                nativeC60BDContextRawFunctor_arrow]
              rfl
          _ = 𝟙 ((nativeC60AZStrictProject T R).obj
                ⟨nativeC60BCContextTotal F steps _⟩) :=
              nativeC60AZStrictStep_inv_left T R _
          _ = P.map Quiver.Path.nil := rfl
    | inverseRight c =>
        calc
          P.map ((nativeC60AZRawArrow T (.symm c)).comp
              (nativeC60AZRawArrow T c)) =
            P.map (nativeC60AZRawArrow T (.symm c)) ≫
              P.map (nativeC60AZRawArrow T c) :=
              P.map_comp _ _
          _ = nativeC60AZStrictStep T R
                (.symm (nativeC60BCMapClosedStep S F steps c)) ≫
              nativeC60AZStrictStep T R
                (nativeC60BCMapClosedStep S F steps c) := by
              rw [nativeC60BDContextRawFunctor_arrow,
                nativeC60BDContextRawFunctor_arrow]
              rfl
          _ = 𝟙 ((nativeC60AZStrictProject T R).obj
                ⟨nativeC60BCContextTotal F steps _⟩) :=
              nativeC60AZStrictStep_inv_right T R _
          _ = P.map Quiver.Path.nil := rfl
    | declared hcd =>
        simpa only [nativeC60BDContextRawFunctor_arrow] using h _ _ hcd

/-- The exact categorical descent criterion; the quotient is defined by
Kuu.Presentation's selected replacement closure, NEVER by an observer. -/
theorem nativeC60BDStrictContext_exists_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (steps : List Bool) :
    (∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R ⥤
        NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R,
      nativeC60AZStrictProject (nativeC60BCClosedSignature S F) R ⋙ G =
        nativeC60BDContextRawFunctor S F R steps) ↔
      NativeC60BDContextCongruence S F R steps :=
  (nativeC60AZStrictObserver_iff (nativeC60BCClosedSignature S F) R
    (nativeC60BDContextRawFunctor S F R steps)).trans
      (nativeC60BDContextRawFunctor_respects_iff S F R steps)

/-- A strict self-functor of the CONSTRUCTED Kuu space at every finite
C60 context for which the independently selected relations are stable. -/
def nativeC60BDStrictContext {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (steps : List Bool) (h : NativeC60BDContextCongruence S F R steps) :
    NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R ⥤
      NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R :=
  Kuu.descend (nativeC60AZStrictRelations _ R)
    (nativeC60BDContextRawFunctor S F R steps)
    ((nativeC60BDContextRawFunctor_respects_iff S F R steps).mpr h)

theorem nativeC60BDStrictContext_obj {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (steps : List Bool) (h : NativeC60BDContextCongruence S F R steps)
    (x : L.Total) :
    (nativeC60BDStrictContext S F R steps h).obj
        ((nativeC60AZStrictProject _ R).obj ⟨x⟩) =
      (nativeC60AZStrictProject _ R).obj
        ⟨nativeC60BCContextTotal F steps x⟩ := rfl

theorem nativeC60BDStrictContext_step {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (steps : List Bool) (h : NativeC60BDContextCongruence S F R steps)
    {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    (nativeC60BDStrictContext S F R steps h).map
        (nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R c) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
        (nativeC60BCMapClosedStep S F steps c) :=
  nativeC60BDContextRawFunctor_arrow S F R steps c

/-- The baseline strict groupoid adds NO extra higher relations. Every
finite proof-relevant BC context therefore induces an actual strict functor,
with its unit and composition preserved by the functor laws. -/
theorem nativeC60BDNoRelations_context {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (steps : List Bool) :
    NativeC60BDContextCongruence S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) steps := by
  intro a b c d hc
  exact False.elim hc

def nativeC60BDNoRelations_strictFunctor {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (steps : List Bool) :
    NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) ⥤
      NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) :=
  nativeC60BDStrictContext S F _ steps (nativeC60BDNoRelations_context S F steps)

/-- When a NEXT higher signature declares comparisons, preserving each
actual new generator is NECESSARY AND SUFFICIENT for strict descent. -/
theorem nativeC60BDHigher_context_iff {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (T : NativeC60AXSignature
      (nativeC60AXNext L (nativeC60BCClosedSignature S F)))
    (steps : List Bool) :
    NativeC60BDContextCongruence S F
      (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T) steps ↔
    ∀ {a b : L.Total}
      (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
      T.Gen ⟨(a, b), c⟩ ⟨(a, b), d⟩ →
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T)
          (nativeC60BCMapClosedStep S F steps c) =
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T)
          (nativeC60BCMapClosedStep S F steps d) := by
  constructor
  · intro hc a b c d gen
    exact hc c d ⟨gen⟩
  · intro hg a b c d hr
    rcases hr with ⟨gen⟩
    exact hg c d gen

/-- Exact factorization criterion for the NEXT declared higher layer. -/
theorem nativeC60BDHigher_strictFunctor_iff {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (T : NativeC60AXSignature
      (nativeC60AXNext L (nativeC60BCClosedSignature S F)))
    (steps : List Bool) :
    (∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
          (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T) ⥤
        NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
          (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T),
      nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T) ⋙ G =
        nativeC60BDContextRawFunctor S F
          (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T) steps) ↔
      ∀ {a b : L.Total}
        (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
        T.Gen ⟨(a, b), c⟩ ⟨(a, b), d⟩ →
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
            (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T)
            (nativeC60BCMapClosedStep S F steps c) =
          nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
            (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T)
            (nativeC60BCMapClosedStep S F steps d) :=
  (nativeC60BDStrictContext_exists_iff S F
    (nativeC60AZHigherRelations (nativeC60BCClosedSignature S F) T) steps).trans
    (nativeC60BDHigher_context_iff S F T steps)

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

/-- A strict functor, NOT a scalar observer, produced for every finite
word of the ACTUAL original fourteen-dimensional C60 whiskerings. -/
def nativeK5BDPhysicalStrictContext
    (W : NativeK5StructuralThirteenCell p U V) (steps : List Bool) :
    NativeC60AZStrictSpace (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W)) ⥤
      NativeC60AZStrictSpace (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W)) :=
  nativeC60BDNoRelations_strictFunctor
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) steps

/-- Physical strict context functors transport each actual AU 16D
naturality arrow to the context-transported Type-valued comparison. -/
theorem nativeK5BDPhysicalStrictContext_arrow
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (nativeK5BDPhysicalStrictContext W outer).map
        (nativeC60AZStrictStep (nativeK5BCSignature W)
          (nativeC60AZNoRelations (nativeK5BCSignature W))
          (nativeK5BCContextualNaturality W inner cell)) =
      nativeC60AZStrictStep (nativeK5BCSignature W)
          (nativeC60AZNoRelations (nativeK5BCSignature W))
          (nativeK5BCClosedContextStep W outer
            (nativeK5BCContextualNaturality W inner cell)) :=
  nativeC60BDStrictContext_step
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeC60AZNoRelations (nativeK5BCSignature W)) outer
    (nativeC60BDNoRelations_context
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer)
    (nativeK5BCContextualNaturality W inner cell)

/-- Even after any finite physical context, the original two AU naturality
proofs remain DISTINCT OBJECTS of the strict Kuu groupoid. The strict arrow
between them therefore cannot be an identity obtained by collapsing objects. -/
theorem nativeK5BDContextualStrictObjects_ne
    (W : NativeK5StructuralThirteenCell p U V) (steps : List Bool) :
    (nativeC60AZStrictProject (nativeK5BCSignature W)
      (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
        ⟨nativeK5BCContext W steps
          (nativeK5AXPack W
            (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))⟩ ≠
    (nativeC60AZStrictProject (nativeK5BCSignature W)
      (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
        ⟨nativeK5BCContext W steps
          (nativeK5AXPack W
            (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])))⟩ := by
  intro h
  exact nativeK5BCContextualPacked_raw_ne W steps
    (nativeC60AZStrictObj_injective
      (nativeK5BCSignature W)
      (nativeC60AZNoRelations (nativeK5BCSignature W)) h)

/-- The object part composes for ALL finite original geometric context
words. Equality of entire functors requires separate higher proof-word
coherence and is NOT inferred from this object equality. -/
theorem nativeK5BDPhysicalStrictContext_obj_append
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool)
    (c : (nativeK5AXBaseLayer W).Total) :
    (nativeK5BDPhysicalStrictContext W outer).obj
        ((nativeK5BDPhysicalStrictContext W inner).obj
          ((nativeC60AZStrictProject (nativeK5BCSignature W)
            (nativeC60AZNoRelations (nativeK5BCSignature W))).obj ⟨c⟩)) =
      (nativeK5BDPhysicalStrictContext W (outer ++ inner)).obj
        ((nativeC60AZStrictProject (nativeK5BCSignature W)
          (nativeC60AZNoRelations (nativeK5BCSignature W))).obj ⟨c⟩) := by
  change (nativeC60AZStrictProject (nativeK5BCSignature W)
      (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
        ⟨nativeK5BCContext W outer (nativeK5BCContext W inner c)⟩ =
      (nativeC60AZStrictProject (nativeK5BCSignature W)
      (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
        ⟨nativeK5BCContext W (outer ++ inner) c⟩
  exact congrArg
    (fun x : (nativeK5AXBaseLayer W).Total =>
      (nativeC60AZStrictProject (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))).obj ⟨x⟩)
    (nativeC60BCContextTotal_append (nativeK5BCFrame W) outer inner c).symm

/-- Next independently selected higher generators still determine the EXACT
remaining descent condition on physical C60 strict arrows. -/
theorem nativeK5BDPhysicalNextContext_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (T : NativeC60AXSignature
      (nativeC60AXNext (nativeK5AXBaseLayer W) (nativeK5BCSignature W)))
    (steps : List Bool) :
    (∃ G : NativeC60AZStrictSpace (nativeK5BCSignature W)
          (nativeC60AZHigherRelations (nativeK5BCSignature W) T) ⥤
        NativeC60AZStrictSpace (nativeK5BCSignature W)
          (nativeC60AZHigherRelations (nativeK5BCSignature W) T),
      nativeC60AZStrictProject (nativeK5BCSignature W)
          (nativeC60AZHigherRelations (nativeK5BCSignature W) T) ⋙ G =
        nativeC60BDContextRawFunctor
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          (nativeC60AZHigherRelations (nativeK5BCSignature W) T) steps) ↔
      ∀ {a b : (nativeK5AXBaseLayer W).Total}
        (c d : NativeC60AXStep (nativeK5BCSignature W) a b),
        T.Gen ⟨(a, b), c⟩ ⟨(a, b), d⟩ →
        nativeC60AZStrictStep (nativeK5BCSignature W)
          (nativeC60AZHigherRelations (nativeK5BCSignature W) T)
          (nativeK5BCClosedContextStep W steps c) =
        nativeC60AZStrictStep (nativeK5BCSignature W)
          (nativeC60AZHigherRelations (nativeK5BCSignature W) T)
          (nativeK5BCClosedContextStep W steps d) :=
  nativeC60BDHigher_strictFunctor_iff
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) T steps

end PhysicalC60

#print axioms nativeC60BDContextPrefunctor
#print axioms nativeC60BDContextRawFunctor
#print axioms nativeC60BDContextRawFunctor_arrow
#print axioms NativeC60BDContextCongruence
#print axioms nativeC60BDContextRawFunctor_respects_iff
#print axioms nativeC60BDStrictContext_exists_iff
#print axioms nativeC60BDStrictContext
#print axioms nativeC60BDStrictContext_obj
#print axioms nativeC60BDStrictContext_step
#print axioms nativeC60BDNoRelations_context
#print axioms nativeC60BDNoRelations_strictFunctor
#print axioms nativeC60BDHigher_context_iff
#print axioms nativeC60BDHigher_strictFunctor_iff
#print axioms nativeK5BDPhysicalStrictContext
#print axioms nativeK5BDPhysicalStrictContext_arrow
#print axioms nativeK5BDContextualStrictObjects_ne
#print axioms nativeK5BDPhysicalStrictContext_obj_append
#print axioms nativeK5BDPhysicalNextContext_iff

end
end Kuu.F112.Physical
