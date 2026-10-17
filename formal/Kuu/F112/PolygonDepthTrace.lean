import Kuu.F112.PolygonDepthGeneralRoutes

/-!
# F112-E7G / exact physical rotation event traces for ALL dual depths

The arbitrary-depth E7F normalization really contains extra F54
depth-cast paths and unit terms. It would be incorrect to claim
literal equality of these unquotiented E7B/E6A raw proof trees
with the older E6A five/six-sector long, short and square words.

We instead retain an independent, Type-valued event for EACH actual
original C60 sector-bracket rotation: its full physical bracket
source, target and original E6A local rotation certificate.
Finite ordered traces are NOT mere rotation-count or shadow grades.

A trace of a dependent E7B rotation route forgets ONLY two-axis
index casts (zero physical rotations), retaining original contextual
rotation witnesses. We prove its exact agreement with the trace
of the E7B-to-E6A raw erasure, including all identity, composition
and both contextual constructors, and preserve actual step counts.

This is a physical source-sequence semantics, not source proof-tree
equality, historical F55 equivalence, or a global Gray coherence axiom.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
noncomputable section

/-- A fully typed physical rotation event, retaining both original
C60 bracket boundaries AND the proof-relevant elementary generator. -/
structure PolygonRotationEvent (p : Polygon) where
  source : PolygonBracketTree p
  target : PolygonBracketTree p
  generator : PolygonBracketRotation p source target

/-- Actual C60 physical left context of a single rotation event. -/
def PolygonRotationEvent.leftContext {p : Polygon}
    (ev : PolygonRotationEvent p) (c : PolygonBracketTree p) :
    PolygonRotationEvent p :=
  ⟨.node ev.source c, .node ev.target c, .leftContext ev.generator c⟩

/-- Actual right physical context, distinct from left context. -/
def PolygonRotationEvent.rightContext {p : Polygon}
    (a : PolygonBracketTree p) (ev : PolygonRotationEvent p) :
    PolygonRotationEvent p :=
  ⟨.node a ev.source, .node a ev.target, .rightContext a ev.generator⟩

/-- The original E6A source has an exact ordered list of typed
original physical rotation generators, not an integer proxy.
Raw identity has no generator events. -/
def PolygonBracketRoute.physicalTrace {p : Polygon}
    {a b : PolygonBracketTree p} :
    PolygonBracketRoute p a b → List (PolygonRotationEvent p)
  | .ident _ => []
  | .step f => [⟨_, _, f⟩]
  | .trans f g => f.physicalTrace ++ g.physicalTrace
  | .leftContext f c =>
      f.physicalTrace.map (fun ev => ev.leftContext c)
  | .rightContext a f =>
      f.physicalTrace.map (fun ev => ev.rightContext a)

/-- The true E7B dependent route has the SAME physical generators.
A two-axis cast changes only the depth indices and contributes
NO physical rotation event. -/
def PolygonDepthRoute.physicalTrace {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'} :
    PolygonDepthRoute p a b → List (PolygonRotationEvent p)
  | .ident _ => []
  | .assoc a b c =>
      [⟨.node (.node a.erase b.erase) c.erase,
        .node a.erase (.node b.erase c.erase),
        .assoc a.erase b.erase c.erase⟩]
  | .castDepths _ _ _ => []
  | .trans f g => f.physicalTrace ++ g.physicalTrace
  | .leftContext f c =>
      f.physicalTrace.map (fun ev => ev.leftContext c.erase)
  | .rightContext a f =>
      f.physicalTrace.map (fun ev => ev.rightContext a.erase)

/-- Even before forgetting depth indices, the event-list length
is EXACTLY the original E6A raw rotation count. -/
theorem PolygonBracketRoute.physicalTrace_length {p : Polygon}
    {a b : PolygonBracketTree p} (r : PolygonBracketRoute p a b) :
    r.physicalTrace.length = r.rotationCount := by
  induction r with
  | ident a => rfl
  | step f => rfl
  | trans f g ihf ihg =>
      change (f.physicalTrace ++ g.physicalTrace).length =
        f.rotationCount + g.rotationCount
      rw [List.length_append, ihf, ihg]
  | leftContext f c ih =>
      change (f.physicalTrace.map (fun ev => ev.leftContext c)).length =
        f.rotationCount
      rw [List.length_map, ih]
  | rightContext a f ih =>
      change (f.physicalTrace.map (fun ev => ev.rightContext a)).length =
        f.rotationCount
      rw [List.length_map, ih]

theorem PolygonDepthRoute.physicalTrace_length {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    (r : PolygonDepthRoute p a b) :
    r.physicalTrace.length = r.rotationCount := by
  induction r with
  | ident a => rfl
  | assoc a b c => rfl
  | castDepths hn hm a => rfl
  | trans f g ihf ihg =>
      change (f.physicalTrace ++ g.physicalTrace).length =
        f.rotationCount + g.rotationCount
      rw [List.length_append, ihf, ihg]
  | leftContext f c ih =>
      change (f.physicalTrace.map (fun ev => ev.leftContext c.erase)).length =
        f.rotationCount
      rw [List.length_map, ih]
  | rightContext a f ih =>
      change (f.physicalTrace.map (fun ev => ev.rightContext a.erase)).length =
        f.rotationCount
      rw [List.length_map, ih]

/-- A target cast does not insert any extra E6 original physical
rotation generator into its source sequence. -/
theorem polygonBracketRouteCastTarget_physicalTrace
    {p : Polygon} {a b c : PolygonBracketTree p}
    (h : b = c) (r : PolygonBracketRoute p a b) :
    (polygonBracketRouteCastTarget h r).physicalTrace =
      r.physicalTrace := by
  cases h
  rfl

theorem PolygonDepthRoute.castTarget_physicalTrace
    {p : Polygon} {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b c : PolygonDepthTree p n' m'}
    (h : b = c) (r : PolygonDepthRoute p a b) :
    (r.castTarget h).physicalTrace = r.physicalTrace := by
  cases h
  rfl

/-- CORE E7G: EVERY arbitrary-double-depth E7B route has EXACTLY
the physical rotation-event list of its already proved E6A
source erasure. Both original bracket boundaries and original
rotation witnesses are preserved in each event of the list;
only explicitly marked Nat-depth transports disappear. -/
theorem PolygonDepthRoute.physicalTrace_eq_erasure
    {p : Polygon} {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    (r : PolygonDepthRoute p a b) :
    r.physicalTrace = r.toBracketRoute.physicalTrace := by
  induction r with
  | ident a =>
      rfl
  | assoc a b c =>
      change
        ([⟨.node (.node a.erase b.erase) c.erase,
          .node a.erase (.node b.erase c.erase),
          .assoc a.erase b.erase c.erase⟩] :
          List (PolygonRotationEvent p)) =
        (polygonBracketRouteCastTarget
          (polygonDepthAssoc_erase a b c).symm
          (PolygonBracketRoute.step
            (PolygonBracketRotation.assoc a.erase b.erase c.erase))).physicalTrace
      rw [polygonBracketRouteCastTarget_physicalTrace]
      rfl
  | castDepths hn hm a =>
      change ([] : List (PolygonRotationEvent p)) =
        (polygonBracketRouteCastTarget
          (PolygonDepthTree.erase_cast hn hm a).symm
          (PolygonBracketRoute.ident a.erase)).physicalTrace
      rw [polygonBracketRouteCastTarget_physicalTrace]
      rfl
  | trans f g ihf ihg =>
      change
        f.physicalTrace ++ g.physicalTrace =
        f.toBracketRoute.physicalTrace ++ g.toBracketRoute.physicalTrace
      rw [ihf, ihg]
  | leftContext f c ih =>
      change
        f.physicalTrace.map (fun ev => ev.leftContext c.erase) =
        f.toBracketRoute.physicalTrace.map
          (fun ev => ev.leftContext c.erase)
      rw [ih]
  | rightContext a f ih =>
      change
        f.physicalTrace.map (fun ev => ev.rightContext a.erase) =
        f.toBracketRoute.physicalTrace.map
          (fun ev => ev.rightContext a.erase)
      rw [ih]

/-- In particular, arbitrary Nat-depth associativity normalization
contains precisely ONE genuine physical rotation event. Its
two independent casts and proof-level target reindexing have
not fabricated any extra geometric generator. -/
theorem polygonDepthAssocNormalized_physicalTrace
    {p : Polygon} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    (a : PolygonDepthTree p n₁ m₁)
    (b : PolygonDepthTree p n₂ m₂)
    (c : PolygonDepthTree p n₃ m₃) :
    (polygonDepthAssocNormalized a b c).physicalTrace =
      [⟨.node (.node a.erase b.erase) c.erase,
        .node a.erase (.node b.erase c.erase),
        .assoc a.erase b.erase c.erase⟩] := by
  unfold polygonDepthAssocNormalized
  rw [PolygonDepthRoute.castTarget_physicalTrace]
  rfl

#print axioms PolygonBracketRoute.physicalTrace_length
#print axioms PolygonDepthRoute.physicalTrace_length
#print axioms polygonBracketRouteCastTarget_physicalTrace
#print axioms PolygonDepthRoute.castTarget_physicalTrace
#print axioms PolygonDepthRoute.physicalTrace_eq_erasure
#print axioms polygonDepthAssocNormalized_physicalTrace
end
end Kuu.F112.Physical
