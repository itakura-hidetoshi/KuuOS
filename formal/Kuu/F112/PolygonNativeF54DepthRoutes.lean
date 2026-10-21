import Kuu.F112.PolygonNativeF54Chains

/-!
# F112-E7O / independent old-F54-shaped double-depth rotation routes

The frozen F54/F55 DepthRotationRoute does NOT consist merely of
two F54-type endpoint bracket trees. It stores ACTUAL arbitrary
Type-valued bidirectional RotationChains, BOTH independent original
F19/F28 Nat index equality transports, route concatenation and
genuinely typed left/right binary-tree contexts.

E7L constructs original-shaped two-category F45 Blocks and independent
proof-relevant native AxisTrace histories over REAL C60 sectors.
E7M reconstructs precisely typed, two-Nat-cast root LocalRotation
witnesses. E7N proves their real finite RotationChain operations.

Here we construct the corresponding NEW independent depth-route source,
and BOTH full associahedral 3-vs-2 pentagon raw routes for ANY original-
shaped FOUR consecutively typed C60 F45 stages. Their distinctness is
proved by the number of ACTUAL Type-valued RotationEdge witnesses, not
by assigning phases or collapsing to the E6 quotient.

The generic source is never asserted equivalent to frozen old F54:
historical F19 StrongTrans.Modification and F28 compression-kernel
AxisTrace operations still require constructor-faithful comparison.
No KUOS.*, Gray, F51, F77 imports, axioms, sorry or admits.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Exact Type-valued old-F54-shaped route grammar with FOUR original
depth endpoints. Every chain and explicit equality proof is retained. -/
inductive KuuNativeF45Tree.DepthRotationRoute (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y},
      KuuNativeF45Tree p n m ma pa mb pb →
      KuuNativeF45Tree p n' m' ma pa mb pb →
      Type (max (max uD uE) (max vD vE)) where
  | chain
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first last : KuuNativeF45Tree p n m ma pa mb pb}
      (path : KuuNativeF45Tree.RotationChain p first last) :
      DepthRotationRoute p first last
  | castDepths
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      (hn : n = n') (hm : m = m')
      (tree : KuuNativeF45Tree p n m ma pa mb pb) :
      DepthRotationRoute p tree (KuuNativeF45Tree.castDepths hn hm tree)
  | trans
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (left : DepthRotationRoute p first middle)
      (right : DepthRotationRoute p middle last) :
      DepthRotationRoute p first last
  | leftContext
      {a b : D} {x y : E}
      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {before : KuuNativeF45Tree p n m ma pa mb pb}
      {after : KuuNativeF45Tree p n' m' ma pa mb pb}
      (path : DepthRotationRoute p before after)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      DepthRotationRoute p
        (KuuNativeF45Tree.node before later)
        (KuuNativeF45Tree.node after later)
  | rightContext
      {a b : D} {x y : E}
      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {before : KuuNativeF45Tree p n m mb pb mc pc}
      {after : KuuNativeF45Tree p n' m' mb pb mc pc}
      (path : DepthRotationRoute p before after) :
      DepthRotationRoute p
        (KuuNativeF45Tree.node earlier before)
        (KuuNativeF45Tree.node earlier after)

/-- Only actual primitive F54 local-rotation edges count. Double-Nat
casts, native categorical contexts and proof concatenation introduce
NO fabricated extra physical rotation steps. -/
def KuuNativeF45Tree.DepthRotationRoute.rotationCount
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : Nat := by
  induction route with
  | chain path =>
      exact path.length
  | castDepths _ _ _ =>
      exact 0
  | trans left right ihLeft ihRight =>
      exact ihLeft + ihRight
  | leftContext path later ih =>
      exact ih
  | rightContext earlier path ih =>
      exact ih

/-- Every actual old-F54-shaped native double-depth route preserves
the FULL original C60 ordered physical sector source, including all
intermediate block presentations and two independent typed contexts. -/
theorem KuuNativeF45Tree.DepthRotationRoute.sectors_eq
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    first.sectors = last.sectors := by
  induction route with
  | chain path =>
      exact path.sectors_eq
  | castDepths hn hm tree =>
      exact (KuuNativeF45Tree.sectors_castDepths hn hm tree).symm
  | trans left right ihLeft ihRight =>
      exact ihLeft.trans ihRight
  | leftContext path later ih =>
      change _ ++ later.sectors = _ ++ later.sectors
      exact congrArg (fun z => z ++ later.sectors) ih
  | rightContext earlier path ih =>
      change earlier.sectors ++ _ = earlier.sectors ++ _
      exact congrArg (fun z => earlier.sectors ++ z) ih

/-- F54-like double-depth source paths preserve the genuine E7A
physical sector-bracket boundary even when arbitrary index transports
are freely interspersed with forward and backward rotations. -/
theorem KuuNativeF45Tree.DepthRotationRoute.physical_leaves_eq
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    first.erasePhysical.erase.leaves =
      last.erasePhysical.erase.leaves := by
  calc
    first.erasePhysical.erase.leaves = first.sectors :=
      first.erasePhysical_leaves
    _ = last.sectors := route.sectors_eq
    _ = last.erasePhysical.erase.leaves :=
      last.erasePhysical_leaves.symm

/-- A real original-shaped three-subtree F54 associator:
ONE actual Type-valued E7M local-rotation edge with TWO separately
recorded Nat.add_assoc casts of old F19/F28-shaped source depths. -/
def KuuNativeF45Tree.DepthRotationRoute.assoc
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (second : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (third : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    KuuNativeF45Tree.DepthRotationRoute p
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node first second) third)
      (KuuNativeF45Tree.node first
        (KuuNativeF45Tree.node second third)) :=
  .trans
    (.castDepths
      (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node first second) third))
    (.chain (.snoc (.refl _)
      (.forward (.assoc first second third))))

theorem KuuNativeF45Tree.DepthRotationRoute.assoc_rotationCount
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (second : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (third : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc
      first second third).rotationCount = 1 := by
  rfl

section FourNativeStages

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
variable
  (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)

/-- The two genuine four-original-stage source bracket endpoints,
at both EXACT old-F19/F28-style Nat-depth parenthesizations. -/
def KuuNativeF45Tree.pentagon0 :
    KuuNativeF45Tree p
      (((n₁ + n₂) + n₃) + n₄)
      (((m₁ + m₂) + m₃) + m₄)
      p₀ q₀ p₄ q₄ :=
  .node (.node (.node t₁ t₂) t₃) t₄

def KuuNativeF45Tree.pentagon3 :
    KuuNativeF45Tree p
      (n₁ + (n₂ + (n₃ + n₄)))
      (m₁ + (m₂ + (m₃ + m₄)))
      p₀ q₀ p₄ q₄ :=
  .node t₁ (.node t₂ (.node t₃ t₄))

/-- THREE real original-shaped F54 local-rotation chain steps,
each retaining its own two-Nat cast and actual intermediate
two-category Blocks/source proof tree. -/
def KuuNativeF45Tree.DepthRotationRoute.pentagonLong :
    KuuNativeF45Tree.DepthRotationRoute p
      (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄) :=
  .trans
    (.trans
      (.leftContext (.assoc t₁ t₂ t₃) t₄)
      (.assoc t₁ (.node t₂ t₃) t₄))
    (.rightContext t₁ (.assoc t₂ t₃ t₄))

/-- TWO real original-shaped F54 local-rotation chain steps with
identical DEPENDENT four-axis source/target and different raw proof. -/
def KuuNativeF45Tree.DepthRotationRoute.pentagonShort :
    KuuNativeF45Tree.DepthRotationRoute p
      (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄) :=
  .trans
    (.assoc (.node t₁ t₂) t₃ t₄)
    (.assoc t₁ t₂ (.node t₃ t₄))

theorem KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄).rotationCount = 3 := by
  rfl

theorem KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄).rotationCount = 2 := by
  rfl

/-- The exact original-shaped 3-vs-2 pentagon path obstruction
is a theorem of raw Type-valued syntax, NOT equality in a shadow
quotient and not a postulated F55 higher exchange relation. -/
theorem KuuNativeF45Tree.DepthRotationRoute.pentagonLong_ne_short :
    KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄ ≠
    KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄ := by
  intro h
  have hc := congrArg KuuNativeF45Tree.DepthRotationRoute.rotationCount h
  rw [KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count,
    KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count] at hc
  exact (by decide : (3 : Nat) ≠ 2) hc

end FourNativeStages

/-- Four ACTUAL successive C60 north-pentagon sector stages,
each with two independently proof-relevant native F19/F28-shaped
original finite-path Blocks histories. -/
def northNativeF45FirstFourth :=
  KuuNativeBlocks.snoc northNativeF45FirstThrice
    (KuuNativePath.nil (Site.face (.pentagon .north)))

def northNativeF45SecondFourth :=
  KuuNativeBlocks.snoc northNativeF45SecondThrice
    (KuuNativePath.nil (Site.face (.pentagon .north)))

def northNativeF45FourthStage :
    KuuNativeF45Tree (.pentagon .north) 1 1
      northNativeF45FirstThrice northNativeF45SecondThrice
      northNativeF45FirstFourth northNativeF45SecondFourth :=
  .leaf (firstFourPolygonSector (.pentagon .north) 3)
    .secondAxisFirst
    (KuuNativeAxisTrace.insertNilOnce _)
    (KuuNativeAxisTrace.insertNilOnce _)

/-- Genuine historical-F54-SHAPED path source on the four original
north C60 sectors 0,1,2,3 with correctly chained two-native-category
block subdivisions and exactly THREE true local rotation steps. -/
def northNativeF45PentagonLong :=
  KuuNativeF45Tree.DepthRotationRoute.pentagonLong
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage

def northNativeF45PentagonShort :=
  KuuNativeF45Tree.DepthRotationRoute.pentagonShort
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage

theorem northNativeF45PentagonLong_ne_short :
    northNativeF45PentagonLong ≠ northNativeF45PentagonShort :=
  KuuNativeF45Tree.DepthRotationRoute.pentagonLong_ne_short
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage

/-- Every C60 sector in the genuine four-original-stage route
survives the full 3-vs-2 original-shaped F54 depth transfer. -/
theorem northNativeF45PentagonLong_physical_sectors :
    ((KuuNativeF45Tree.pentagon0
      northNativeF45FirstStage northNativeF45SecondStage
      northNativeF45ThirdStage northNativeF45FourthStage).erasePhysical.erase).leaves =
    ((KuuNativeF45Tree.pentagon3
      northNativeF45FirstStage northNativeF45SecondStage
      northNativeF45ThirdStage northNativeF45FourthStage).erasePhysical.erase).leaves :=
  northNativeF45PentagonLong.physical_leaves_eq

#print axioms KuuNativeF45Tree.DepthRotationRoute
#print axioms KuuNativeF45Tree.DepthRotationRoute.rotationCount
#print axioms KuuNativeF45Tree.DepthRotationRoute.sectors_eq
#print axioms KuuNativeF45Tree.DepthRotationRoute.physical_leaves_eq
#print axioms KuuNativeF45Tree.DepthRotationRoute.assoc
#print axioms KuuNativeF45Tree.DepthRotationRoute.assoc_rotationCount
#print axioms KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count
#print axioms KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count
#print axioms KuuNativeF45Tree.DepthRotationRoute.pentagonLong_ne_short
#print axioms northNativeF45PentagonLong_ne_short
#print axioms northNativeF45PentagonLong_physical_sectors
end
end Kuu.F112.Physical
