import Kuu.F112.PolygonNativeF55P94DK5NaturalitySquare1TypedSeam
import Mathlib.Tactic

/-!
# F112-P94D3Q: real square2 seams and shelling-orientation obstruction

The existing P92B square2 uses assocNaturality in its FIRST
argument. The anchored face is its genuine symm: source has the
actual e15;e13 F54 route and target has e20;e14. We construct
both local and global F54 structural seams, retaining that
inverted actual P92B 3-cell and its exact N-charge -1.

The graph shelling, however, requests path5 -> path1, while the
anchored inverted source is path1 -> path5. We prove an invariant
of EVERY structural seam generator that detects the mismatch.
No word-sign correction, graph inference, old-P92B redefinition,
Gray, sorry/admit, added axiom, C60 replacement or root deletion.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Ordered syntactic depths of real F54 rotation atoms.
Identity chains and depth casts are inert; contexts add one. -/
def KuuNativeF45Tree.DepthRotationRoute.contextDepthTrace
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) : List Nat := by
  induction r with
  | chain path => exact List.replicate path.length 0
  | castDepths _ _ _ => exact []
  | trans _ _ ihLeft ihRight => exact ihLeft ++ ihRight
  | leftContext _ _ ih => exact ih.map Nat.succ
  | rightContext _ _ ih => exact ih.map Nat.succ

/-- Every original F54 structural seam preserves its ordered
context-depth trace. In particular, it never exchanges the two
differently placed associator rotations of square2. -/
theorem NativeF54StructuralSeam.contextDepthTrace_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (w : NativeF54StructuralSeam p r s) :
    r.contextDepthTrace = s.contextDepthTrace := by
  induction w with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | reassoc u v z =>
      change (u.contextDepthTrace ++ v.contextDepthTrace) ++ z.contextDepthTrace =
        u.contextDepthTrace ++ (v.contextDepthTrace ++ z.contextDepthTrace)
      exact List.append_assoc _ _ _
  | leftUnit r => simp [KuuNativeF45Tree.DepthRotationRoute.contextDepthTrace]
  | rightUnit r => simp [KuuNativeF45Tree.DepthRotationRoute.contextDepthTrace]
  | precompose u w ih =>
      change u.contextDepthTrace ++ _ = u.contextDepthTrace ++ _
      exact congrArg (fun xs : List Nat => u.contextDepthTrace ++ xs) ih
  | postcompose w v ih =>
      change _ ++ v.contextDepthTrace = _ ++ v.contextDepthTrace
      exact congrArg (fun xs : List Nat => xs ++ v.contextDepthTrace) ih
  | leftContextTrans u v later =>
      change (u.contextDepthTrace ++ v.contextDepthTrace).map Nat.succ =
        u.contextDepthTrace.map Nat.succ ++ v.contextDepthTrace.map Nat.succ
      simp
  | rightContextTrans earlier u v =>
      change (u.contextDepthTrace ++ v.contextDepthTrace).map Nat.succ =
        u.contextDepthTrace.map Nat.succ ++ v.contextDepthTrace.map Nat.succ
      simp
  | leftContextUnit earlier later => rfl
  | rightContextUnit earlier later => rfl
  | leftContextCongruence w later ih =>
      exact congrArg (fun xs : List Nat => xs.map Nat.succ) ih
  | rightContextCongruence earlier w ih =>
      exact congrArg (fun xs : List Nat => xs.map Nat.succ) ih

section FiveNativeStages
variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- Original reversed P92B square2 source normalizes to e15;e13. -/
def nativeK5NaturalitySquare2LocalSourceSeam :
    NativeF54StructuralSeam p
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.1
      (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e15)
        (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e13)) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let w := KuuNativeF45Tree.DepthRotationRoute.assoc t1 t2 t3
  let h45 := nativeF54P90HorizontalRoute
    (nativeK5RouteUnit t4) (nativeK5RouteUnit t5)
  let h := nativeF54P90HorizontalRoute w h45
  have hh : NativeF54StructuralSeam p h (e .e13) :=
    .trans
      (.precompose (.leftContext w (.node t4 t5))
        (.rightContextCongruence
          (.node t1 (.node t2 t3))
          (nativeF54StructuralHorizontalTwoUnits t4 t5)))
      (nativeF54StructuralHorizontalRightUnit w (.node t4 t5))
  change NativeF54StructuralSeam p
    (.trans (e .e15) h) (.trans (e .e15) (e .e13))
  exact .precompose (e .e15) hh

/-- Original reversed P92B square2 target normalizes to e20;e14. -/
def nativeK5NaturalitySquare2LocalTargetSeam :
    NativeF54StructuralSeam p
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.1
      (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e20)
        (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e14)) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let w := KuuNativeF45Tree.DepthRotationRoute.assoc t1 t2 t3
  let h12 := nativeF54P90HorizontalRoute w (nativeK5RouteUnit t4)
  let h := nativeF54P90HorizontalRoute h12 (nativeK5RouteUnit t5)
  have hh : NativeF54StructuralSeam p h (e .e20) :=
    .trans
      (nativeF54StructuralHorizontalRightUnit h12 t5)
      (.leftContextCongruence
        (nativeF54StructuralHorizontalRightUnit w t4) t5)
  change NativeF54StructuralSeam p
    (.trans h (e .e14)) (.trans (e .e20) (e .e14))
  exact .postcompose hh (e .e14)

/-- Genuine 13-to-0 source seam for the opposite direction 1 -> 5. -/
def nativeK5NaturalitySquare2ReverseGlobalSourceSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .square2) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let tail := KuuNativeF45Tree.DepthRotationRoute.trans (e .e6) (e .e1)
  change NativeF54StructuralSeam p
    (.trans (e .e15) (.trans (e .e13) tail))
    (.trans (.chain (.refl _))
      (.trans (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.1 tail))
  exact .trans
    (.symm (.reassoc (e .e15) (e .e13) tail))
    (.trans
      (.postcompose
        (.symm (nativeK5NaturalitySquare2LocalSourceSeam t1 t2 t3 t4 t5))
        tail)
      (.symm (.leftUnit _)))

/-- Genuine 13-to-0 target seam for the opposite direction 1 -> 5. -/
def nativeK5NaturalitySquare2ReverseGlobalTargetSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .square2) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let tail := KuuNativeF45Tree.DepthRotationRoute.trans (e .e6) (e .e1)
  change NativeF54StructuralSeam p
    (.trans (e .e20) (.trans (e .e14) tail))
    (.trans (.chain (.refl _))
      (.trans (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.1 tail))
  exact .trans
    (.symm (.reassoc (e .e20) (e .e14) tail))
    (.trans
      (.postcompose
        (.symm (nativeK5NaturalitySquare2LocalTargetSeam t1 t2 t3 t4 t5))
        tail)
      (.symm (.leftUnit _)))

/-- A real Type-valued 3-cell in the distinct structural extension.
It has boundary path1 -> path5, not shelling path5 -> path1. -/
def nativeK5NaturalitySquare2ReverseExtendedFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5) :=
  nativeK5StructuralGluedFace t1 t2 t3 t4 t5 .square2 _ _
    (nativeK5NaturalitySquare2ReverseGlobalSourceSeam t1 t2 t3 t4 t5)
    (nativeK5NaturalitySquare2ReverseGlobalTargetSeam t1 t2 t3 t4 t5)

theorem nativeK5NaturalitySquare2ReverseExtendedFace_word :
    (nativeK5NaturalitySquare2ReverseExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord := by
  exact nativeK5StructuralGluedFace_word t1 t2 t3 t4 t5 .square2 _ _ _ _

theorem nativeK5NaturalitySquare2ReverseExtendedFace_NCount_minus_one :
    nativeK5NaturalityCount
      (nativeK5NaturalitySquare2ReverseExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
        -1 := by
  rw [nativeK5NaturalitySquare2ReverseExtendedFace_word]
  change nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square2 = -1
  simpa [nativeK5FaceExpectedNCount] using
    nativeK5AnchoredFaceNCount_exact t1 t2 t3 t4 t5 .square2

/-- Independently computed real source traces differ on the first
two primitive rotations, even though the original suffix agrees. -/
theorem nativeK5NaturalitySquare2ShellingSource_trace :
    (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5).contextDepthTrace =
      [2, 0, 0, 1] := by
  rfl

theorem nativeK5NaturalitySquare2WhiskeredSource_trace :
    (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .square2).contextDepthTrace =
      [0, 1, 0, 1] := by
  rfl

theorem nativeK5NaturalitySquare2ShellingTarget_trace :
    (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1).contextDepthTrace =
      [0, 1, 0, 1] := by
  rfl

theorem nativeK5NaturalitySquare2WhiskeredTarget_trace :
    (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .square2).contextDepthTrace =
      [2, 0, 0, 1] := by
  rfl

/-- No structural-seam proof can invert the real square2 source
without changing the underlying oriented P92B generator. -/
theorem nativeK5NaturalitySquare2NoOutwardSourceSeam :
    ¬ NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .square2) := by
  intro s
  have h := NativeF54StructuralSeam.contextDepthTrace_sound s
  rw [nativeK5NaturalitySquare2ShellingSource_trace,
      nativeK5NaturalitySquare2WhiskeredSource_trace] at h
  exact (by decide : ([2, 0, 0, 1] : List Nat) ≠ [0, 1, 0, 1]) h

theorem nativeK5NaturalitySquare2NoOutwardTargetSeam :
    ¬ NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .square2) := by
  intro s
  have h := NativeF54StructuralSeam.contextDepthTrace_sound s
  rw [nativeK5NaturalitySquare2ShellingTarget_trace,
      nativeK5NaturalitySquare2WhiskeredTarget_trace] at h
  exact (by decide : ([0, 1, 0, 1] : List Nat) ≠ [2, 0, 0, 1]) h

#print axioms KuuNativeF45Tree.DepthRotationRoute.contextDepthTrace
#print axioms NativeF54StructuralSeam.contextDepthTrace_sound
#print axioms nativeK5NaturalitySquare2LocalSourceSeam
#print axioms nativeK5NaturalitySquare2LocalTargetSeam
#print axioms nativeK5NaturalitySquare2ReverseGlobalSourceSeam
#print axioms nativeK5NaturalitySquare2ReverseGlobalTargetSeam
#print axioms nativeK5NaturalitySquare2ReverseExtendedFace_word
#print axioms nativeK5NaturalitySquare2ReverseExtendedFace_NCount_minus_one
#print axioms nativeK5NaturalitySquare2NoOutwardSourceSeam
#print axioms nativeK5NaturalitySquare2NoOutwardTargetSeam

end FiveNativeStages
end
end Kuu.F112.Physical
