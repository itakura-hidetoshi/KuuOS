import Kuu.F112.PolygonNativeF55P94DK5MoreTypedPentagonSeams
import Mathlib.Tactic

/-!
# F112-P94D3N: original F54 context-transport for K5 pentagon3/8

True F54 route proofs inside left and right *original F45 contexts*
are not judgmentally the same as concatenations of their tagged
edge contexts. Instead, our explicitly distinct Type-valued
structural presentation now contains source-typed context
composition normalization. We prove it conserves the genuine
F54 rotation counts without treating the old F55/P92B source as
if it already contained this extra 3-cell generator.

For original pentagon8 (k=3) and pentagon3 (k=5) we construct both
13→0 F54 seam witnesses, preserving all original F45 Blocks,
Nat indices and context nesting. The exact original P92B face
proof is then used unchanged by the structural extension, whose
noncommutative free word is proved equal to the anchored word.

This reaches SIX of NINE actual K5 faces in the distinct
structural comparison presentation. The remaining three source
associator-naturality squares, original-P92B seam descent and
Peiffer/pentagonator 4-coherence are still open.
No graph-derived coherence, Gray, sorry/admit, axioms, or root loss.
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

/-- k=3 pentagon8 outward source 4→8: original leftContext
pentagon short route, original genuine e19/e17 and a real 9→0
suffix, with one REAL F54 unit at 13. -/
def nativeK5Pentagon8SourceContextSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 4)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .pentagon8) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let a := KuuNativeF45Tree.DepthRotationRoute.assoc (.node t1 t2) t3 t4
  let b := KuuNativeF45Tree.DepthRotationRoute.assoc t1 t2 (.node t3 t4)
  let tail := KuuNativeF45Tree.DepthRotationRoute.trans
    (e .e8) (.trans (e .e3) (e .e0))
  change NativeF54StructuralSeam p
    (.trans (e .e19) (.trans (e .e17) tail))
    (.trans (.chain (.refl _))
      (.trans (.leftContext (.trans a b) t5) tail))
  exact .trans
    (.symm (.reassoc (e .e19) (e .e17) tail))
    (.trans
      (.postcompose (.symm (.leftContextTrans a b t5)) tail)
      (.symm (.leftUnit _)))

/-- k=3 pentagon8 target: the original left-context pentagon long
route, retaining its three truly typed rotations e20/e18/e16.
The context composition theorem is applied TWICE. -/
def nativeK5Pentagon8TargetContextSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 8)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .pentagon8) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let a := KuuNativeF45Tree.DepthRotationRoute.leftContext
    (KuuNativeF45Tree.DepthRotationRoute.assoc t1 t2 t3) t4
  let b := KuuNativeF45Tree.DepthRotationRoute.assoc t1 (.node t2 t3) t4
  let c := KuuNativeF45Tree.DepthRotationRoute.rightContext t1
    (KuuNativeF45Tree.DepthRotationRoute.assoc t2 t3 t4)
  let tail := KuuNativeF45Tree.DepthRotationRoute.trans
    (e .e8) (.trans (e .e3) (e .e0))
  have hc : NativeF54StructuralSeam p
      (.leftContext (.trans (.trans a b) c) t5)
      (.trans (.trans (e .e20) (e .e18)) (e .e16)) :=
    .trans
      (.leftContextTrans (.trans a b) c t5)
      (.postcompose (.leftContextTrans a b t5) (e .e16))
  change NativeF54StructuralSeam p
    (.trans (e .e20) (.trans (e .e18) (.trans (e .e16) tail)))
    (.trans (.chain (.refl _))
      (.trans (.leftContext (.trans (.trans a b) c) t5) tail))
  exact .trans
    (.symm (.reassoc (e .e20) (e .e18) (.trans (e .e16) tail)))
    (.trans
      (.symm (.reassoc (.trans (e .e20) (e .e18)) (e .e16) tail))
      (.trans (.postcompose (.symm hc) tail)
        (.symm (.leftUnit _))))

/-- k=5 pentagon3 outward source 7→6: exactly the original
rightContext pentagon long route in the t1 context, under the
true e20/e18/e9 typed-prefix and a real identity suffix at 0. -/
def nativeK5Pentagon3SourceContextSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 7)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .pentagon3) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let a := KuuNativeF45Tree.DepthRotationRoute.leftContext
    (KuuNativeF45Tree.DepthRotationRoute.assoc t2 t3 t4) t5
  let b := KuuNativeF45Tree.DepthRotationRoute.assoc t2 (.node t3 t4) t5
  let c := KuuNativeF45Tree.DepthRotationRoute.rightContext t2
    (KuuNativeF45Tree.DepthRotationRoute.assoc t3 t4 t5)
  let prefix := KuuNativeF45Tree.DepthRotationRoute.trans
    (e .e20) (.trans (e .e18) (e .e9))
  let tail := KuuNativeF45Tree.DepthRotationRoute.trans
    (e .e7) (.trans (e .e3) (e .e0))
  have hc : NativeF54StructuralSeam p
      (.rightContext t1 (.trans (.trans a b) c))
      (.trans (.trans (e .e7) (e .e3)) (e .e0)) :=
    .trans (.rightContextTrans t1 (.trans a b) c)
      (.postcompose (.rightContextTrans t1 a b) (e .e0))
  change NativeF54StructuralSeam p
    (.trans (e .e20) (.trans (e .e18) (.trans (e .e9) tail)))
    (.trans prefix
      (.trans (.rightContext t1 (.trans (.trans a b) c))
        (.chain (.refl _))))
  exact .trans
    (.precompose (e .e20)
      (.symm (.reassoc (e .e18) (e .e9) tail)))
    (.trans
      (.symm (.reassoc (e .e20) (.trans (e .e18) (e .e9)) tail))
      (.trans
        (.precompose prefix (.symm (.reassoc (e .e7) (e .e3) (e .e0))))
        (.trans
          (.precompose prefix (.symm hc))
          (.precompose prefix (.symm (.rightUnit _))))))

/-- k=5 pentagon3 outward target 6 is its original right-context
pentagon short route. No charge-changing correction is inserted. -/
def nativeK5Pentagon3TargetContextSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 6)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .pentagon3) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let a := KuuNativeF45Tree.DepthRotationRoute.assoc (.node t2 t3) t4 t5
  let b := KuuNativeF45Tree.DepthRotationRoute.assoc t2 t3 (.node t4 t5)
  let prefix := KuuNativeF45Tree.DepthRotationRoute.trans
    (e .e20) (.trans (e .e18) (e .e9))
  let tail := KuuNativeF45Tree.DepthRotationRoute.trans (e .e5) (e .e1)
  change NativeF54StructuralSeam p
    (.trans (e .e20) (.trans (e .e18) (.trans (e .e9) tail)))
    (.trans prefix
      (.trans (.rightContext t1 (.trans a b)) (.chain (.refl _))))
  exact .trans
    (.precompose (e .e20)
      (.symm (.reassoc (e .e18) (e .e9) tail)))
    (.trans
      (.symm (.reassoc (e .e20) (.trans (e .e18) (e .e9)) tail))
      (.trans
        (.precompose prefix (.symm (.rightContextTrans t1 a b)))
        (.precompose prefix (.symm (.rightUnit _)))))

/-- Genuinely Type-valued outward K5 face k=3 in the new source
extension, preserving the source P92B pentagon8 generator. -/
def nativeK5Pentagon8ExtendedContextFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 4)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 8) :=
  nativeK5StructuralGluedFace t1 t2 t3 t4 t5 .pentagon8 _ _
    (nativeK5Pentagon8SourceContextSeam t1 t2 t3 t4 t5)
    (nativeK5Pentagon8TargetContextSeam t1 t2 t3 t4 t5)

/-- Genuinely Type-valued outward K5 face k=5, with the REAL old
P92B right-context pentagon3 cell embedded without alteration. -/
def nativeK5Pentagon3ExtendedContextFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 7)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 6) :=
  nativeK5StructuralGluedFace t1 t2 t3 t4 t5 .pentagon3 _ _
    (nativeK5Pentagon3SourceContextSeam t1 t2 t3 t4 t5)
    (nativeK5Pentagon3TargetContextSeam t1 t2 t3 t4 t5)

theorem nativeK5Pentagon8ExtendedContextFace_word :
    (nativeK5Pentagon8ExtendedContextFace t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon8).2.2.2.p94cGroupWord := by
  exact nativeK5StructuralGluedFace_word t1 t2 t3 t4 t5 .pentagon8 _ _ _ _

theorem nativeK5Pentagon3ExtendedContextFace_word :
    (nativeK5Pentagon3ExtendedContextFace t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon3).2.2.2.p94cGroupWord := by
  exact nativeK5StructuralGluedFace_word t1 t2 t3 t4 t5 .pentagon3 _ _ _ _

#print axioms NativeF54StructuralSeam.rotationCount_sound
#print axioms nativeK5Pentagon8SourceContextSeam
#print axioms nativeK5Pentagon8TargetContextSeam
#print axioms nativeK5Pentagon3SourceContextSeam
#print axioms nativeK5Pentagon3TargetContextSeam
#print axioms nativeK5Pentagon8ExtendedContextFace_word
#print axioms nativeK5Pentagon3ExtendedContextFace_word

end FiveNativeStages
end
end Kuu.F112.Physical
