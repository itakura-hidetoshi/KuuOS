import Kuu.F112.PolygonNativeF55P94DK5TypedWhiskeredSeams
import Mathlib.Tactic

/-!
# F112-P94D3L: actual F54 structural seams, first pentagon7 face

The original P92B source has NO generator equating reassociations
or identity insertions in the syntax of F54 DepthRotationRoute.
We add a DISTINCT explicitly typed *structural* comparison
presentation for precisely these free-route coherence operations.
Its basic generators preserve the real F54 rotation count and
are assigned zero noncommutative P/N word. This is a presentation,
NOT an inferred historical P92B 3-cell or an F55 filler.

Construct BOTH true 13-to-0 seams of outward pentagon7 (shelling
step 0) by combining the existing original typed F54 edge routes,
proof-relevant parenthesization, and honest structural unit moves.
Then give an actual Type-valued 3-cell in the explicitly EXTENDED
presentation, carrying exactly the original P92B face word.

No claim that this new comparison descends to old P92B, no global
typed K5 nine-face sphere, no universal coherence, no Gray,
no sorry/admit or added logical axiom. The nonzero N-charge
obstruction and all retained public roots remain untouched.
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

/-- Independent source-typed structural seam presentation on original
F54 proof terms. Only associativity, units and congruence of the
original route composition are adjoined; no P92B equation is asserted. -/
inductive NativeF54StructuralSeam (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb},
      KuuNativeF45Tree.DepthRotationRoute p first last →
      KuuNativeF45Tree.DepthRotationRoute p first last →
      Type (max (max uD uE) (max vD vE)) where
  | refl
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
      NativeF54StructuralSeam p r r
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (w : NativeF54StructuralSeam p r s) :
      NativeF54StructuralSeam p s r
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (w : NativeF54StructuralSeam p r s)
      (v : NativeF54StructuralSeam p s t) :
      NativeF54StructuralSeam p r t
  | reassoc
      {a b : D} {x y : E} {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {t₄ : KuuNativeF45Tree p n₄ m₄ ma pa mb pb}
      (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
      (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃)
      (w : KuuNativeF45Tree.DepthRotationRoute p t₃ t₄) :
      NativeF54StructuralSeam p
        (.trans (.trans u v) w) (.trans u (.trans v w))
  | leftUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
      NativeF54StructuralSeam p
        (.trans (.chain (.refl first)) r) r
  | rightUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
      NativeF54StructuralSeam p
        (.trans r (.chain (.refl last))) r
  | precompose
      {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
      {r s : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃}
      (w : NativeF54StructuralSeam p r s) :
      NativeF54StructuralSeam p (.trans u r) (.trans u s)
  | postcompose
      {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂}
      (w : NativeF54StructuralSeam p r s)
      (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
      NativeF54StructuralSeam p (.trans r v) (.trans s v)


  | leftContextTrans
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
      (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF54StructuralSeam p
        (.leftContext (.trans u v) later)
        (.trans (.leftContext u later) (.leftContext v later))
  | rightContextTrans
      {a b : D} {x y : E}
      {k l n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {t₁ : KuuNativeF45Tree p n₁ m₁ mb pb mc pc}
      {t₂ : KuuNativeF45Tree p n₂ m₂ mb pb mc pc}
      {t₃ : KuuNativeF45Tree p n₃ m₃ mb pb mc pc}
      (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
      (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
      NativeF54StructuralSeam p
        (.rightContext earlier (.trans u v))
        (.trans (.rightContext earlier u) (.rightContext earlier v))

/-- Source-level soundness of every structural generator: no
real original F54 primitive rotation is added or removed. -/
theorem NativeF54StructuralSeam.rotationCount_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (w : NativeF54StructuralSeam p r s) :
    r.rotationCount = s.rotationCount := by
  induction w with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | reassoc u v z =>
      change (u.rotationCount + v.rotationCount) + z.rotationCount =
        u.rotationCount + (v.rotationCount + z.rotationCount)
      omega
  | leftUnit r =>
      change 0 + r.rotationCount = r.rotationCount
      omega
  | rightUnit r =>
      change r.rotationCount + 0 = r.rotationCount
      omega
  | precompose u w ih =>
      change u.rotationCount + _ = u.rotationCount + _
      exact congrArg (fun k : Nat => u.rotationCount + k) ih
  | postcompose w v ih =>
      change _ + v.rotationCount = _ + v.rotationCount
      exact congrArg (fun k : Nat => k + v.rotationCount) ih
  | leftContextTrans u v later =>
      change u.rotationCount + v.rotationCount =
        u.rotationCount + v.rotationCount
      rfl
  | rightContextTrans earlier u v =>
      change u.rotationCount + v.rotationCount =
        u.rotationCount + v.rotationCount
      rfl

/-- A separate extension of original Type-valued P92B 3-cells:
a structural seam is explicitly tagged, never coerced to P92B. -/
inductive NativeF55StructuralComparison (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb},
      KuuNativeF45Tree.DepthRotationRoute p first last →
      KuuNativeF45Tree.DepthRotationRoute p first last →
      Type (max (max uD uE) (max vD vE)) where
  | original
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (w : NativeF55P92AssocComparison p r s) :
      NativeF55StructuralComparison p r s
  | structural
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (w : NativeF54StructuralSeam p r s) :
      NativeF55StructuralComparison p r s
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (w : NativeF55StructuralComparison p r s)
      (v : NativeF55StructuralComparison p s t) :
      NativeF55StructuralComparison p r t

/-- The FULL ordered P/N free word is transported from original
P92B constructors, while the separate structural generators have
exactly zero chosen word. This defines a new presentation, not a
claim that arbitrary existing P92B sources have a zero witness. -/
def NativeF55StructuralComparison.p94cGroupWord
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (w : NativeF55StructuralComparison p r s) :
    NativeF55P94CWord :=
  match w with
  | .original c => c.p94cGroupWord
  | .structural _ => 0
  | .trans c d => c.p94cGroupWord + d.p94cGroupWord

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

/-- First REAL outward source seam, for pentagon7 / global path
0:13→8→5→0. The exact F54 redex changes from
 e15;(e11;e2) to unit13;((e15;e11);e2).
The original face supplies the e15;e11 leg; NO graph equality
is used to identify those raw Type-valued F54 terms. -/
def nativeK5FirstSourceStructuralSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .pentagon7) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  change NativeF54StructuralSeam p
    (.trans (e .e15) (.trans (e .e11) (e .e2)))
    (.trans (.chain (.refl _))
      (.trans (.trans (e .e15) (e .e11)) (e .e2)))
  exact .trans
    (.symm (.reassoc (e .e15) (e .e11) (e .e2)))
    (.symm (.leftUnit _))

/-- First REAL outward target seam, for the adjacent global path
3:13→11→6→5→0. It uses two source-level reassociations and
one honest unit insertion, not a group-word shadow comparison. -/
def nativeK5FirstTargetStructuralSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 3)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .pentagon7) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  change NativeF54StructuralSeam p
    (.trans (e .e19) (.trans (e .e12) (.trans (e .e10) (e .e2))))
    (.trans (.chain (.refl _))
      (.trans (.trans (.trans (e .e19) (e .e12)) (e .e10)) (e .e2)))
  exact .trans
    (.symm (.reassoc (e .e19) (e .e12) (.trans (e .e10) (e .e2))))
    (.trans
      (.symm (.reassoc (.trans (e .e19) (e .e12)) (e .e10) (e .e2)))
      (.symm (.leftUnit _)))

/-- ONE outward face is now an unconditional, genuinely Type-valued
3-cell in the explicitly NEW structural extension, between the
canonical independent F54 routes 0 and 3. This is NOT an old P92B
3-cell or a global four-dimensional coherence proof. -/
def nativeK5FirstExtendedTypedFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 3) :=
  .trans
    (.trans
      (.structural (nativeK5FirstSourceStructuralSeam t1 t2 t3 t4 t5))
      (.original (nativeK5WhiskeredGenuineFace t1 t2 t3 t4 t5 .pentagon7)))
    (.structural
      (.symm (nativeK5FirstTargetStructuralSeam t1 t2 t3 t4 t5)))

/-- The newly constructed TRUE typed face loses NONE of the old
ordered noncommutative P92B evidence (no false abelianization). -/
theorem nativeK5FirstExtendedTypedFace_word :
    (nativeK5FirstExtendedTypedFace t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon7).2.2.2.p94cGroupWord := by
  change 0 +
    (nativeK5WhiskeredGenuineFace t1 t2 t3 t4 t5 .pentagon7).p94cGroupWord + 0 =
    (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon7).2.2.2.p94cGroupWord
  simpa using nativeK5WhiskeredGenuineFace_word t1 t2 t3 t4 t5 .pentagon7

theorem nativeK5FirstExtendedTypedFace_NCount :
    nativeK5NaturalityCount
      (nativeK5FirstExtendedTypedFace t1 t2 t3 t4 t5).p94cGroupWord =
        nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon7 := by
  rw [nativeK5FirstExtendedTypedFace_word]
  rfl

#print axioms NativeF54StructuralSeam.rotationCount_sound
#print axioms NativeF55StructuralComparison.p94cGroupWord
#print axioms nativeK5FirstSourceStructuralSeam
#print axioms nativeK5FirstTargetStructuralSeam
#print axioms nativeK5FirstExtendedTypedFace
#print axioms nativeK5FirstExtendedTypedFace_word
#print axioms nativeK5FirstExtendedTypedFace_NCount

end FiveNativeStages
end
end Kuu.F112.Physical
