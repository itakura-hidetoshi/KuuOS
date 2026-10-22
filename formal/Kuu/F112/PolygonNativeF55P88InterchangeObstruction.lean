import Kuu.F112.PolygonNativeF55P88InterchangeWordInvariant

/-!
# F112-P88B — exact source 4-cell obstruction to strict interchange

P87 gives an internally closed genuine four-cell quotient with
original source F55 horizontal and vertical binary operations.
The P87 proof of equal FULL numeric interchange shadows does NOT
manufacture a source 4-cell between the two interchange pastings.

P88A builds a separate NONCOMMUTATIVE original-source word
invariant and checks soundness for EVERY old P77/P80/P85/P86/P87
Type-valued 4-cell constructor. The original horizontal operation
has source word:
  map (constant false) (left word) ++
  map (constant true)  (right word).

For the original interchange pastings, the two source words are
  L(f1) ++ L(f2) ++ R(g1) ++ R(g2)
  L(f1) ++ R(g1) ++ L(f2) ++ R(g2).
If both middle factors f2 and g1 have NONEMPTY original source
primitive words, these two noncommutative words cannot be equal:
after their common prefix, one starts with FALSE and one TRUE.

Therefore there is NO genuine Type-valued P87 four-cell comparing
these original terms, and the exact source-witness P87 quotient
classes differ. This is a strict-interchange NO-GO for the
chosen current P87 presentation on EVERY genuinely typed
configuration satisfying the explicit nonempty-source hypotheses.
It is NOT a general impossibility theorem for strict 3-categories
or a no-go outside P87, and it leaves the P66 original C60 square
and all pre-C60 dependent-origination theory unchanged.

The expected next direction is to decide whether adding a source
interchange four-cell can be done in a DISTINCT presentation while
faithfully handling the underlying F54 route objects and nontrivial
odd exchange phase. Do not assert interchange from shadow equality.
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

/-- Pure FREE-WORD fact: two nonempty blocks of FALSE and TRUE
letters cannot commute past each other even after the same
surrounding prefix and suffix are appended. This statement
uses ORIGINAL source order, not numeric F55 charges. -/
private theorem p88_false_true_blocks_do_not_commute
    (prefix leftMiddle rightMiddle suffix : List Bool)
    (hl : leftMiddle ≠ [])
    (hr : rightMiddle ≠ []) :
    prefix ++ leftMiddle.map (fun _ => false) ++
        rightMiddle.map (fun _ => true) ++ suffix ≠
      prefix ++ rightMiddle.map (fun _ => true) ++
        leftMiddle.map (fun _ => false) ++ suffix := by
  induction prefix with
  | nil =>
      intro h
      cases leftMiddle with
      | nil => exact hl rfl
      | cons x xs =>
          cases rightMiddle with
          | nil => exact hr rfl
          | cons y ys =>
              simp at h
  | cons a rest ih =>
      intro h
      apply ih
      exact (List.cons.inj h).2

/-- The ACTUAL original F55 interchange source terms have
different NONCOMMUTATIVE trace words whenever the left second
step and right first step both contain actual source primitives.
No assumption on selected numerical shadow equality is used. -/
theorem nativeF55P88_raw_interchange_word_ne
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₀ u₁)
    (f₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₁ u₂)
    (g₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₀ v₁)
    (g₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₁ v₂)
    (hLeft : f₂.p88InterchangeWord ≠ [])
    (hRight : g₁.p88InterchangeWord ≠ []) :
    ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂)).p88InterchangeWord ≠
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
      (f₁.horizontal g₁) (f₂.horizontal g₂)).p88InterchangeWord := by
  intro heq
  have hword :
      f₁.p88InterchangeWord.map (fun _ => false) ++
        f₂.p88InterchangeWord.map (fun _ => false) ++
        g₁.p88InterchangeWord.map (fun _ => true) ++
        g₂.p88InterchangeWord.map (fun _ => true) =
      f₁.p88InterchangeWord.map (fun _ => false) ++
        g₁.p88InterchangeWord.map (fun _ => true) ++
        f₂.p88InterchangeWord.map (fun _ => false) ++
        g₂.p88InterchangeWord.map (fun _ => true) := by
    simpa only [
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88_horizontal_word,
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p88InterchangeWord,
      List.map_append, List.append_assoc] using heq
  exact (p88_false_true_blocks_do_not_commute
    (f₁.p88InterchangeWord.map (fun _ => false))
    f₂.p88InterchangeWord g₁.p88InterchangeWord
    (g₂.p88InterchangeWord.map (fun _ => true)) hLeft hRight)
    (by simpa only [List.append_assoc] using hword)

/-- P87 genuinely has a total original horizontal binary operation,
but the original interchange pair cannot be compared by P87's
chosen freely generated Type-valued four-cells in the stated
(nonempty source-middle-factor) situation. This is an exact
NEGATION OF CERTIFICATE EXISTENCE, not lack of an implementation. -/
theorem nativeF55P88_raw_interchange_noFourCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₀ u₁)
    (f₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₁ u₂)
    (g₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₀ v₁)
    (g₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₁ v₂)
    (hLeft : f₂.p88InterchangeWord ≠ [])
    (hRight : g₁.p88InterchangeWord ≠ []) :
    ¬ Nonempty (NativeF55P87ClosedFourCell
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂))
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
      (f₁.horizontal g₁) (f₂.horizontal g₂))) := by
  rintro ⟨certificate⟩
  exact (nativeF55P88_raw_interchange_word_ne
    f₁ f₂ g₁ g₂ hLeft hRight)
    certificate.p88_word_sound

/-- The exact P87 source-witness quotient likewise cannot
identify those genuine original interchange histories. This
holds IN THE SAME P87 strict local vertical Category that
already supports a total P87×P87→P87 binary horizontal operation. -/
theorem nativeF55P88_interchange_quotient_ne
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₀ u₁)
    (f₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₁ u₂)
    (g₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₀ v₁)
    (g₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₁ v₂)
    (hLeft : f₂.p88InterchangeWord ≠ [])
    (hRight : g₁.p88InterchangeWord ≠ []) :
    nativeF55P87FourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂)) ≠
    nativeF55P87FourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
      (f₁.horizontal g₁) (f₂.horizontal g₂)) := by
  intro heq
  exact (nativeF55P88_raw_interchange_noFourCell
    f₁ f₂ g₁ g₂ hLeft hRight)
    ((nativeF55P87FourClass_eq_iff _ _ _ _).mp heq)

#print axioms p88_false_true_blocks_do_not_commute
#print axioms nativeF55P88_raw_interchange_word_ne
#print axioms nativeF55P88_raw_interchange_noFourCell
#print axioms nativeF55P88_interchange_quotient_ne

end
end Kuu.F112.Physical
