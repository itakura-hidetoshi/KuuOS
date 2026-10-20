import KuuOSFormal.HistoricalF36F40BridgeP40

/-!
# F112-P41 — actual original F42 six-constructor source with native C60 face evidence

This OLD-SIDE-only bridge starts from the ACTUAL preserved
C60F42PresentedFaceCell p q (not the previously adjoined mixed F47
four-boundary formal grammar). It has exactly six proof-relevant
source constructors: ident, physicalFace, symm, trans, whiskerLeft
and whiskerRight. Endpoints are original typed Quiver.Path indices.

For each original physical-face generator f, construct the EXACT
independent Kuu polygon p = polygonEquiv.symm f, with:
  * the genuine 5/6-sided Type-valued PolygonSourcePresentation p
    retaining EVERY fan-sector proof and the full physical disk;
  * the exact original ordered edge-boundary WORD of f transported
    from p, including the historically reversed hexagon orientation;
  * actual native F69 localized disk soundness.

Annotate EVERY original F42 raw proof tree by induction, retaining
the original full dependent 1-path source/target indices and all
independent native witnesses at each genuine physicalFace leaf.
Prove its complete ordered sequence of original faces and original
edge-boundary words is preserved through inverse, vertical
composition and BOTH original left/right whiskering constructors.
Prove the TWO original horizontal-pasting orders carry the
correspondingly ordered (and potentially different) native face
evidence traces, rather than identifying proof trees by their grade.

This is a proven actual-face SOURCE ANNOTATION over historical F42,
not yet a globally defined functor from historical Quiver.Path into
independent F69 Zigzag 1-paths or an equivalence of the two F42 raw
2-cell grammars. Those additional path transport/globularity maps
remain explicitly unproved. No Gray imported into KuuOSStrict,
no original published roots removed, no axioms/sorry/admit.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- The ACTUAL old F42 primitive face f has a REAL independently
constructed Kuu physical polygon, a Type-valued five/six-sector
native fan/disk source, and the ENTIRE exact ordered OLD C60 edge
word. The hexagon's certified reversal is retained by the P4
original boundary transport theorem, not silently quotient-erased. -/
structure HistoricalF42PhysicalFaceSupport
    (f : TruncatedIcosahedralSeedFace) where
  nativeFace : Polygon
  historicalFace : polygonEquiv nativeFace = f
  nativeSource : PolygonSourcePresentation nativeFace
  originalWord :
    orderedBoundaryTransport nativeFace =
      kernelC60FullFaceBoundaryEdges f

/-- For each of the 32 original C60 faces, reconstruct its EXACT
independent native face and FULL typed physical fan/disk evidence,
using actual constructor-level geometry and verified boundary order. -/
def historicalF42CanonicalFaceSupport
    (f : TruncatedIcosahedralSeedFace) :
    HistoricalF42PhysicalFaceSupport f where
  nativeFace := polygonEquiv.symm f
  historicalFace := polygonEquiv.apply_symm_apply f
  nativeSource := canonicalPolygonSource (polygonEquiv.symm f)
  originalWord := by
    simpa only [polygonEquiv.apply_symm_apply] using
      orderedBoundaryTransport_eq_original (polygonEquiv.symm f)

/-- The source disk in every original physical-face certificate
really closes in the independently proved genuine F69 localization
kernel, not merely in a chosen numerical Gray receiver. -/
theorem HistoricalF42PhysicalFaceSupport.disk_sound
    {f : TruncatedIcosahedralSeedFace}
    (w : HistoricalF42PhysicalFaceSupport f) :
    zigzagKernelQ.map (polygonRawLoop w.nativeFace) =
      zigzagKernelQ.map
        (Zigzag.nil
          (Site.vertex (cyclicBoundaryDart w.nativeFace 0))) :=
  w.nativeSource.disk.kernel_sound

/-- For any certified original F42 physical face, every native
side actually has the F42 sector Type-valued proof source and is
sound under the genuine independent F69 localization. -/
theorem HistoricalF42PhysicalFaceSupport.sector_sound
    {f : TruncatedIcosahedralSeedFace}
    (w : HistoricalF42PhysicalFaceSupport f)
    (i : Fin 6) (hi : i.val < polygonSideCount w.nativeFace) :
    zigzagToLocalization (polygonRawSide w.nativeFace i hi) =
      zigzagToLocalization (polygonConeRawSide w.nativeFace i hi) :=
  w.nativeSource.sector_localized_sound i hi

/-- A list of ALL actual original physical face-generator labels
occurring in an arbitrary proof-relevant original F42 tree.
Original p,q source path types and BOTH context constructors
remain in the input; an inverse does not pretend to invent a new
physical polygon and vertical composition concatenates ordered
source witnesses. -/
def historicalF42OriginalFaceTrace :
    {a b : IcosahedralDart} → {p q : Quiver.Path a b} →
      C60F42PresentedFaceCell p q →
        List TruncatedIcosahedralSeedFace
  | _, _, .ident _ => []
  | _, _, .physicalFace f => [f]
  | _, _, .symm w => historicalF42OriginalFaceTrace w
  | _, _, .trans w v =>
      historicalF42OriginalFaceTrace w ++ historicalF42OriginalFaceTrace v
  | _, _, .whiskerLeft _ w => historicalF42OriginalFaceTrace w
  | _, _, .whiskerRight w _ => historicalF42OriginalFaceTrace w

/-- Genuine native C60 proof-carrying ANNOTATION of all SIX
constructors of the ACTUAL historical F42 Type-valued raw source.
The original cell is an INDEX, so its original 1-path boundaries,
the inverse, both genuine original whiskerings and vertical raw
composition remain fully proof-relevant; none is collapsed. -/
inductive HistoricalF42NativeAnnotated :
    {a b : IcosahedralDart} →
    {p q : Quiver.Path a b} →
    C60F42PresentedFaceCell p q → Type where
  | ident {a b : IcosahedralDart}
      (p : Quiver.Path a b) :
      HistoricalF42NativeAnnotated (.ident p)
  | physicalFace (f : TruncatedIcosahedralSeedFace)
      (w : HistoricalF42PhysicalFaceSupport f) :
      HistoricalF42NativeAnnotated (.physicalFace f)
  | symm {a b : IcosahedralDart}
      {p q : Quiver.Path a b}
      {cell : C60F42PresentedFaceCell p q}
      (w : HistoricalF42NativeAnnotated cell) :
      HistoricalF42NativeAnnotated (.symm cell)
  | trans {a b : IcosahedralDart}
      {p q r : Quiver.Path a b}
      {left : C60F42PresentedFaceCell p q}
      {right : C60F42PresentedFaceCell q r}
      (w : HistoricalF42NativeAnnotated left)
      (z : HistoricalF42NativeAnnotated right) :
      HistoricalF42NativeAnnotated (.trans left right)
  | whiskerLeft {a b c : IcosahedralDart}
      (prior : Quiver.Path a b)
      {p q : Quiver.Path b c}
      {cell : C60F42PresentedFaceCell p q}
      (w : HistoricalF42NativeAnnotated cell) :
      HistoricalF42NativeAnnotated (.whiskerLeft prior cell)
  | whiskerRight {a b c : IcosahedralDart}
      {p q : Quiver.Path a b}
      {cell : C60F42PresentedFaceCell p q}
      (w : HistoricalF42NativeAnnotated cell)
      (suffix : Quiver.Path b c) :
      HistoricalF42NativeAnnotated (.whiskerRight cell suffix)

/-- SOURCE-TYPED actual original F42 → independent physical Kuu
face-evidence translation, constructor by constructor, preserving
the original COMPLETE old proof term as dependent INDEX. Each
original physical-face leaf obtains the full native fan/disk source,
rather than an integer grade or an erased Prop. -/
def historicalF42Annotate :
    {a b : IcosahedralDart} → {p q : Quiver.Path a b} →
    (cell : C60F42PresentedFaceCell p q) →
      HistoricalF42NativeAnnotated cell
  | _, _, .ident p => .ident p
  | _, _, .physicalFace f => .physicalFace f
      (historicalF42CanonicalFaceSupport f)
  | _, _, .symm w => .symm (historicalF42Annotate w)
  | _, _, .trans w z =>
      .trans (historicalF42Annotate w) (historicalF42Annotate z)
  | _, _, .whiskerLeft prior w =>
      .whiskerLeft prior (historicalF42Annotate w)
  | _, _, .whiskerRight w suffix =>
      .whiskerRight (historicalF42Annotate w) suffix

/-- Retain every native Type-valued physical-face fan/disk
certificate in a separate dependent List. The old source raw
proof is still retained in the annotation's indexed type. -/
def HistoricalF42NativeAnnotated.supports
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {cell : C60F42PresentedFaceCell p q}
    (w : HistoricalF42NativeAnnotated cell) :
    List (Σ f : TruncatedIcosahedralSeedFace,
      HistoricalF42PhysicalFaceSupport f) :=
  match w with
  | .ident _ => []
  | .physicalFace f s => [⟨f, s⟩]
  | .symm s => s.supports
  | .trans s t => s.supports ++ t.supports
  | .whiskerLeft _ s => s.supports
  | .whiskerRight s _ => s.supports

/-- Every original genuine F42 physical generator is annotated
with exactly ONE corresponding Type-valued native face/disk packet,
not with any artificially adjoined Boolean or rectangular face. -/
theorem historicalF42Annotate_physicalFace
    (f : TruncatedIcosahedralSeedFace) :
    (historicalF42Annotate
      (C60F42PresentedFaceCell.physicalFace f)).supports =
        [⟨f, historicalF42CanonicalFaceSupport f⟩] := rfl

/-- The actual ORIGINAL physical C60 face labels are recovered
exactly from every Type-valued native proof annotation, for
arbitrary old inverse/vertical/left/right contextual proof trees.
No physical face is forgotten, added or swapped. -/
theorem HistoricalF42NativeAnnotated.originalFaceTrace
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {cell : C60F42PresentedFaceCell p q}
    (w : HistoricalF42NativeAnnotated cell) :
    w.supports.map (fun x => x.1) =
      historicalF42OriginalFaceTrace cell := by
  induction w with
  | ident p => rfl
  | physicalFace f s => rfl
  | symm w ih =>
      simpa only [HistoricalF42NativeAnnotated.supports,
        historicalF42OriginalFaceTrace] using ih
  | trans w z ihw ihz =>
      simpa only [HistoricalF42NativeAnnotated.supports,
        historicalF42OriginalFaceTrace, List.map_append,
        ihw, ihz]
  | whiskerLeft prior w ih =>
      simpa only [HistoricalF42NativeAnnotated.supports,
        historicalF42OriginalFaceTrace] using ih
  | whiskerRight w suffix ih =>
      simpa only [HistoricalF42NativeAnnotated.supports,
        historicalF42OriginalFaceTrace] using ih

/-- ALL original physical edge-boundary WORDS, in exact old
pentagon/hexagon order, can be read from any F42 raw proof's
ordered list of genuine native physical fan/disk witnesses.
In particular old hexagon reversed cyclic orientation is retained. -/
def HistoricalF42NativeAnnotated.originalWords
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {cell : C60F42PresentedFaceCell p q}
    (w : HistoricalF42NativeAnnotated cell) :
    List (List TruncatedIcosahedralEdge) :=
  w.supports.map (fun x => orderedBoundaryTransport x.2.nativeFace)

/-- ORIGINAL F42 typed source generator WORDS match exactly those
transported from each independent Kuu native face. Proof is by
induction over ALL six old F42 constructors and their native
Type-valued proof annotation, not just at one north hexagon. -/
theorem HistoricalF42NativeAnnotated.originalWords_exact
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {cell : C60F42PresentedFaceCell p q}
    (w : HistoricalF42NativeAnnotated cell) :
    w.originalWords =
      (historicalF42OriginalFaceTrace cell).map
        kernelC60FullFaceBoundaryEdges := by
  induction w with
  | ident p => rfl
  | physicalFace f s =>
      change [orderedBoundaryTransport s.nativeFace] =
        [kernelC60FullFaceBoundaryEdges f]
      exact congrArg (fun z => [z]) s.originalWord
  | symm w ih =>
      simpa only [HistoricalF42NativeAnnotated.originalWords,
        HistoricalF42NativeAnnotated.supports,
        historicalF42OriginalFaceTrace] using ih
  | trans w z ihw ihz =>
      simpa only [HistoricalF42NativeAnnotated.originalWords,
        HistoricalF42NativeAnnotated.supports,
        historicalF42OriginalFaceTrace, List.map_append, ihw, ihz]
  | whiskerLeft prior w ih =>
      simpa only [HistoricalF42NativeAnnotated.originalWords,
        HistoricalF42NativeAnnotated.supports,
        historicalF42OriginalFaceTrace] using ih
  | whiskerRight w suffix ih =>
      simpa only [HistoricalF42NativeAnnotated.originalWords,
        HistoricalF42NativeAnnotated.supports,
        historicalF42OriginalFaceTrace] using ih

/-- EACH physical face appearing in an arbitrarily long original
F42 proof actually carries a Type-valued native disk that is sound
in the original-site F69 kernel. The soundness is not a guessed
prop-level decoder of the old proof term. -/
theorem HistoricalF42NativeAnnotated.allDisks_sound
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {cell : C60F42PresentedFaceCell p q}
    (w : HistoricalF42NativeAnnotated cell)
    (x : Σ f : TruncatedIcosahedralSeedFace,
      HistoricalF42PhysicalFaceSupport f)
    (_hx : x ∈ w.supports) :
    zigzagKernelQ.map (polygonRawLoop x.2.nativeFace) =
      zigzagKernelQ.map
        (Zigzag.nil
          (Site.vertex (cyclicBoundaryDart x.2.nativeFace 0))) :=
  x.2.disk_sound

/-- Left-first HORIZONTAL pasting of the ORIGINAL F42 two-cell
grammar appends evidence in the native order α then β.
No equation between unrelated old 2-cell witnesses is assumed. -/
theorem historicalF42Annotate_horizontalLeftFirst
    {u v w : IcosahedralDart}
    {p q : Quiver.Path u v} {r s : Quiver.Path v w}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    (historicalF42Annotate
      (C60F42PresentedFaceCell.horizontalLeftFirst α β)).supports =
      (historicalF42Annotate α).supports ++
        (historicalF42Annotate β).supports := rfl

/-- Right-first ORIGINAL horizontal pasting has the reverse
evidence order, β before α. The original proof-relevant F42
interchange is NOT silently imposed on native source syntax. -/
theorem historicalF42Annotate_horizontalRightFirst
    {u v w : IcosahedralDart}
    {p q : Quiver.Path u v} {r s : Quiver.Path v w}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    (historicalF42Annotate
      (C60F42PresentedFaceCell.horizontalRightFirst α β)).supports =
      (historicalF42Annotate β).supports ++
        (historicalF42Annotate α).supports := rfl

#print axioms HistoricalF42PhysicalFaceSupport
#print axioms historicalF42CanonicalFaceSupport
#print axioms HistoricalF42PhysicalFaceSupport.disk_sound
#print axioms HistoricalF42PhysicalFaceSupport.sector_sound
#print axioms historicalF42OriginalFaceTrace
#print axioms HistoricalF42NativeAnnotated
#print axioms historicalF42Annotate
#print axioms HistoricalF42NativeAnnotated.supports
#print axioms historicalF42Annotate_physicalFace
#print axioms HistoricalF42NativeAnnotated.originalFaceTrace
#print axioms HistoricalF42NativeAnnotated.originalWords
#print axioms HistoricalF42NativeAnnotated.originalWords_exact
#print axioms HistoricalF42NativeAnnotated.allDisks_sound
#print axioms historicalF42Annotate_horizontalLeftFirst
#print axioms historicalF42Annotate_horizontalRightFirst

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
