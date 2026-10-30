import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeF55NineCode

/-!
# F112-P94D3GJ2 — entire original nine-constructor F55 Countable

The ORIGINAL free, proof-relevant Type-valued PresentedCell has NINE
genuine constructors. The pinned Mathlib derivation cannot assume
that arbitrary D/E categorical Hom fibers are Countable merely from
Countable objects. We therefore construct a separately Countable
finite syntax of all nine original constructors and a dependent
partial decoder into the ACTUAL original PresentedCell source.

In particular, the decoder checks exact original D/E objects, original
F45 Blocks, original F45 source/target proof terms, both independent
Nat grades, and the entire intermediate F54 proof when composing.
The pentagon and disjointSquare cases retain their ACTUAL typed
F45/LocalRotation primitive evidence. No scalar charge, quotient,
evaluation, shadow model, unproved historical F55 equivalence, or
arbitrary categorical Hom Countable assumption is smuggled in.

The strict original decoder(encoder(c)) = some(original c) left
inverse is a theorem of all nine genuine original proof constructors.
This injects the actual original F55 dependent source total into
the range of a partial decoder of a Countable finite syntax.
Every original exact proof fiber inherits Countable under Countable
input D/E objects and EACH original Hom fiber; genuine physical
C60 Site×Site and all actual polygons discharge these hypotheses.

No unconditional 14D original NativeK5FifteenFourteenFiber Countable,
old FJ exact aleph-null condition removal, 19D filler, Gray import,
global strict n, or hyperdescent is claimed. Append-only, 107 roots,
strict Kuu primary, independent Kuu a distinct presentation.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

/-! ### Strictly dependent original F55 constructor operations -/

/-- Two genuinely parallel raw original F54 proof terms are
composable vertically ONLY when their FULL original F45 boundary
and the exact intermediate F54 route proof are identical. -/
noncomputable def nativeGJ2TransExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGJOriginalPresentedTotal p D E →
    NativeGJOriginalPresentedTotal p D E →
    Option (NativeGJOriginalPresentedTotal p D E)
  | ⟨⟨⟨boundary, r⟩, s⟩, left⟩,
    ⟨⟨⟨boundary', s'⟩, t⟩, right⟩ => by
      classical
      by_cases hb : boundary = boundary'
      · subst boundary'
        by_cases hs : s = s'
        · subst s'
          exact some ⟨⟨⟨boundary, r⟩, t⟩, .trans left right⟩
        · exact none
      · exact none

/-- Original left F45 node context, rejecting unrelated D/E
objects and non-equal intermediate BOTH original Blocks sources. -/
noncomputable def nativeGJ2LeftExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGJOriginalPresentedTotal p D E →
    NativeGHOriginalF45Total p D E →
    Option (NativeGJOriginalPresentedTotal p D E)
  | ⟨⟨⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m',
      first, last⟩, r⟩, s⟩, cell⟩,
    ⟨⟨a', b', x', y', k, l, mb', pb', mc, pc⟩, later⟩ => by
      classical
      by_cases ha : a = a'
      · subst a'
        by_cases hb : b = b'
        · subst b'
          by_cases hx : x = x'
          · subst x'
            by_cases hy : y = y'
            · subst y'
              by_cases hmb : mb = mb'
              · subst mb'
                by_cases hpb : pb = pb'
                · subst pb'
                  exact some
                    ⟨⟨⟨⟨a, b, x, y, ma, pa, mc, pc,
                      n + k, n' + k, m + l, m' + l,
                      .node first later, .node last later⟩,
                      .leftContext r later⟩,
                      .leftContext s later⟩,
                      .leftContext cell later⟩
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Original right F45 node context with both original D/E
Blocks and every Nat depth exactly preserved. -/
noncomputable def nativeGJ2RightExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGHOriginalF45Total p D E →
    NativeGJOriginalPresentedTotal p D E →
    Option (NativeGJOriginalPresentedTotal p D E)
  | ⟨⟨a, b, x, y, k, l, ma, pa, mb, pb⟩, earlier⟩,
    ⟨⟨⟨⟨a', b', x', y', mb', pb', mc, pc,
      n, n', m, m', first, last⟩, r⟩, s⟩, cell⟩ => by
      classical
      by_cases ha : a = a'
      · subst a'
        by_cases hb : b = b'
        · subst b'
          by_cases hx : x = x'
          · subst x'
            by_cases hy : y = y'
            · subst y'
              by_cases hmb : mb = mb'
              · subst mb'
                by_cases hpb : pb = pb'
                · subst pb'
                  exact some
                    ⟨⟨⟨⟨a, b, x, y, ma, pa, mc, pc,
                      k + n, k + n', l + m, l + m',
                      .node earlier first, .node earlier last⟩,
                      .rightContext earlier r⟩,
                      .rightContext earlier s⟩,
                      .rightContext earlier cell⟩
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Original *precompose* is accepted only when every D/E category
and Blocks endpoint, BOTH intermediate Nat grades and the ACTUAL
intermediate original F45 tree term coincide exactly. -/
noncomputable def nativeGJ2PreExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIOriginalDepthTotal p D E →
    NativeGJOriginalPresentedTotal p D E →
    Option (NativeGJOriginalPresentedTotal p D E)
  | ⟨⟨a, b, x, y, ma, pa, mb, pb,
      n₁, n₂, m₁, m₂, first, middle⟩, priorRoute⟩,
    ⟨⟨⟨⟨a', b', x', y', ma', pa', mb', pb',
      n₂', n₃, m₂', m₃, middle', last⟩, r⟩, s⟩, cell⟩ => by
      classical
      by_cases ha : a = a'
      · subst a'
        by_cases hb : b = b'
        · subst b'
          by_cases hx : x = x'
          · subst x'
            by_cases hy : y = y'
            · subst y'
              by_cases hma : ma = ma'
              · subst ma'
                by_cases hpa : pa = pa'
                · subst pa'
                  by_cases hmb : mb = mb'
                  · subst mb'
                    by_cases hpb : pb = pb'
                    · subst pb'
                      by_cases hn : n₂ = n₂'
                      · subst n₂'
                        by_cases hm : m₂ = m₂'
                        · subst m₂'
                          by_cases htree : middle = middle'
                          · subst middle'
                            exact some
                              ⟨⟨⟨⟨a, b, x, y, ma, pa, mb, pb,
                                n₁, n₃, m₁, m₃, first, last⟩,
                                .trans priorRoute r⟩,
                                .trans priorRoute s⟩,
                                .precompose priorRoute cell⟩
                          · exact none
                        · exact none
                      · exact none
                    · exact none
                  · exact none
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Original *postcompose* with the same complete intermediate
dependent boundary and exact Type-valued original F45 Tree check. -/
noncomputable def nativeGJ2PostExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGJOriginalPresentedTotal p D E →
    NativeGIOriginalDepthTotal p D E →
    Option (NativeGJOriginalPresentedTotal p D E)
  | ⟨⟨⟨⟨a, b, x, y, ma, pa, mb, pb,
      n₁, n₂, m₁, m₂, first, middle⟩, r⟩, s⟩, cell⟩,
    ⟨⟨a', b', x', y', ma', pa', mb', pb',
      n₂', n₃, m₂', m₃, middle', last⟩, suffix⟩ => by
      classical
      by_cases ha : a = a'
      · subst a'
        by_cases hb : b = b'
        · subst b'
          by_cases hx : x = x'
          · subst x'
            by_cases hy : y = y'
            · subst y'
              by_cases hma : ma = ma'
              · subst ma'
                by_cases hpa : pa = pa'
                · subst pa'
                  by_cases hmb : mb = mb'
                  · subst mb'
                    by_cases hpb : pb = pb'
                    · subst pb'
                      by_cases hn : n₂ = n₂'
                      · subst n₂'
                        by_cases hm : m₂ = m₂'
                        · subst m₂'
                          by_cases htree : middle = middle'
                          · subst middle'
                            exact some
                              ⟨⟨⟨⟨a, b, x, y, ma, pa, mb, pb,
                                n₁, n₃, m₁, m₃, first, last⟩,
                                .trans r suffix⟩,
                                .trans s suffix⟩,
                                .postcompose cell suffix⟩
                          · exact none
                        · exact none
                      · exact none
                    · exact none
                  · exact none
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-! ### Nine-constructor partial original decoder -/

/-- Each correctly typed finite nine-constructor F55 code is decoded
to the ACTUAL complete original Type-valued PresentedCell source.
Every erroneous original D/E object, Blocks, F45 tree, grade,
or intermediate raw F54 route is rejected, never quotiented. -/
noncomputable def nativeGJ2DecodePresented
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGJ2FullNineCode p D E →
    Option (NativeGJOriginalPresentedTotal p D E)
  | .ident ⟨boundary, route⟩ =>
      some ⟨⟨⟨boundary, route⟩, route⟩, .ident route⟩
  | .pentagon source =>
      some (nativeGJInterpretPentagon source)
  | .disjointSquare source =>
      some (nativeGJInterpretSquare source)
  | .symm prior =>
      (nativeGJ2DecodePresented prior).map
        (fun ⟨⟨⟨boundary, r⟩, s⟩, cell⟩ =>
          ⟨⟨⟨boundary, s⟩, r⟩, .symm cell⟩)
  | .trans left right =>
      (nativeGJ2DecodePresented left).bind (fun rawLeft =>
        (nativeGJ2DecodePresented right).bind (fun rawRight =>
          nativeGJ2TransExact rawLeft rawRight))
  | .leftContext prior later =>
      (nativeGJ2DecodePresented prior).bind (fun raw =>
        nativeGJ2LeftExact raw later)
  | .rightContext earlier prior =>
      (nativeGJ2DecodePresented prior).bind (fun raw =>
        nativeGJ2RightExact earlier raw)
  | .precompose route prior =>
      (nativeGJ2DecodePresented prior).bind (fun raw =>
        nativeGJ2PreExact route raw)
  | .postcompose prior route =>
      (nativeGJ2DecodePresented prior).bind (fun raw =>
        nativeGJ2PostExact raw route)

/-! ### Strict source reconstruction under genuinely matching indices -/

theorem nativeGJ2TransExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (right : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t) :
    nativeGJ2TransExact
      (nativeGJPackPresented left : NativeGJOriginalPresentedTotal p D E)
      (nativeGJPackPresented right : NativeGJOriginalPresentedTotal p D E) =
    some (nativeGJPackPresented (.trans left right) :
      NativeGJOriginalPresentedTotal p D E) := by
  simp [nativeGJ2TransExact, nativeGJPackPresented]

theorem nativeGJ2LeftExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {n n' m m' k l : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    nativeGJ2LeftExact
      (nativeGJPackPresented cell : NativeGJOriginalPresentedTotal p D E)
      (nativeGIPackTree later) =
    some (nativeGJPackPresented (.leftContext cell later) :
      NativeGJOriginalPresentedTotal p D E) := by
  simp [nativeGJ2LeftExact, nativeGJPackPresented, nativeGIPackTree]

theorem nativeGJ2RightExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {n n' m m' k l : Nat}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGJ2RightExact
      (nativeGIPackTree earlier)
      (nativeGJPackPresented cell : NativeGJOriginalPresentedTotal p D E) =
    some (nativeGJPackPresented (.rightContext earlier cell) :
      NativeGJOriginalPresentedTotal p D E) := by
  simp [nativeGJ2RightExact, nativeGJPackPresented, nativeGIPackTree]

theorem nativeGJ2PreExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (priorRoute : KuuNativeF45Tree.DepthRotationRoute p first middle)
    {r s : KuuNativeF45Tree.DepthRotationRoute p middle last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGJ2PreExact
      (nativeGJ2PackRoute priorRoute)
      (nativeGJPackPresented cell : NativeGJOriginalPresentedTotal p D E) =
    some (nativeGJPackPresented (.precompose priorRoute cell) :
      NativeGJOriginalPresentedTotal p D E) := by
  simp [nativeGJ2PreExact, nativeGJ2PackRoute, nativeGJPackPresented]

theorem nativeGJ2PostExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    nativeGJ2PostExact
      (nativeGJPackPresented cell : NativeGJOriginalPresentedTotal p D E)
      (nativeGJ2PackRoute suffix) =
    some (nativeGJPackPresented (.postcompose cell suffix) :
      NativeGJOriginalPresentedTotal p D E) := by
  simp [nativeGJ2PostExact, nativeGJ2PackRoute, nativeGJPackPresented]

/-- Faithful primitive pentagon code evaluates to the ACTUAL
original four-F45-tree primitive 3-cell, including both F54 paths. -/
theorem nativeGJ2Pentagon_decode_pack
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    nativeGJInterpretPentagon
      (nativeGJ2PackPentagon t₁ t₂ t₃ t₄) =
      (nativeGJPackPresented (.pentagon t₁ t₂ t₃ t₄) :
        NativeGJOriginalPresentedTotal p D E) := by
  rfl

theorem nativeGJ2Square_decode_pack
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore leftAfter : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : KuuNativeF45Tree p n' m' p₁ q₁ p₂ q₂}
    (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
    (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter) :
    nativeGJInterpretSquare
      (nativeGJ2PackSquare left right) =
      (nativeGJPackPresented (.disjointSquare left right) :
        NativeGJOriginalPresentedTotal p D E) := by
  rfl

/-- STRICT left inverse on EVERY ACTUAL original nine-constructor
F55 Type-valued raw 3-cell, not only on primitive pentagon/square
cells or observer data. All nested Type-valued witnesses survive. -/
theorem nativeGJ2Decode_encodePresented
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGJ2DecodePresented (nativeGJ2EncodePresented cell) =
      some (nativeGJPackPresented cell :
        NativeGJOriginalPresentedTotal p D E) := by
  induction cell with
  | ident route =>
      simp [nativeGJ2EncodePresented, nativeGJ2DecodePresented,
        nativeGJ2PackRoute, nativeGJPackPresented]
  | pentagon t₁ t₂ t₃ t₄ =>
      simpa only [nativeGJ2EncodePresented, nativeGJ2DecodePresented]
        using congrArg some (nativeGJ2Pentagon_decode_pack t₁ t₂ t₃ t₄)
  | disjointSquare left right =>
      simpa only [nativeGJ2EncodePresented, nativeGJ2DecodePresented]
        using congrArg some (nativeGJ2Square_decode_pack left right)
  | symm prior ih =>
      simp [nativeGJ2EncodePresented, nativeGJ2DecodePresented,
        ih, nativeGJPackPresented]
  | trans left right ihLeft ihRight =>
      simp [nativeGJ2EncodePresented, nativeGJ2DecodePresented,
        ihLeft, ihRight]
      exact nativeGJ2TransExact_eq left right
  | leftContext prior later ih =>
      simp [nativeGJ2EncodePresented, nativeGJ2DecodePresented, ih]
      exact nativeGJ2LeftExact_eq prior later
  | rightContext earlier prior ih =>
      simp [nativeGJ2EncodePresented, nativeGJ2DecodePresented, ih]
      exact nativeGJ2RightExact_eq earlier prior
  | precompose route prior ih =>
      simp [nativeGJ2EncodePresented, nativeGJ2DecodePresented, ih]
      exact nativeGJ2PreExact_eq route prior
  | postcompose prior route ih =>
      simp [nativeGJ2EncodePresented, nativeGJ2DecodePresented, ih]
      exact nativeGJ2PostExact_eq prior route

/-- The entire ORIGINAL F55 proof-bearing 3-cell total is genuinely
Countable: the complete original proof embeds into the image of a
dependent partial decoder of a Countable all-nine-constructor code.
No original constructors or proof histories are identified. -/
theorem nativeGJ2OriginalPresentedTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGJOriginalPresentedTotal p D E) := by
  letI : Countable (NativeGJ2FullNineCode p D E) :=
    nativeGJ2FullNineCode_countable hobjD hhomD hobjE hhomE
  have hrange :
      (Set.range (nativeGJ2DecodePresented (p := p) (D := D) (E := E))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeGJ2DecodePresented (p := p) (D := D) (E := E))) :=
    hrange.to_subtype
  let embedding : NativeGJOriginalPresentedTotal p D E →
      Set.range (nativeGJ2DecodePresented (p := p) (D := D) (E := E)) :=
    fun raw => ⟨some raw, by
      rcases raw with ⟨⟨⟨boundary, r⟩, s⟩, cell⟩
      rcases boundary with
        ⟨a, b, x, y, ma, pa, mb, pb,
          n, n', m, m', first, last⟩
      exact ⟨nativeGJ2EncodePresented cell,
        nativeGJ2Decode_encodePresented cell⟩⟩
  have hinj : Function.Injective embedding := by
    intro left right h
    have hs : (some left : Option (NativeGJOriginalPresentedTotal p D E)) =
        some right := congrArg
          (fun t : Set.range
            (nativeGJ2DecodePresented (p := p) (D := D) (E := E)) => t.1) h
    exact Option.some.inj hs
  exact hinj.countable

/-- Every original F55 dependent proof fiber is Countable at its
actual fully parallel F54 Type-valued source and target. -/
theorem nativeGJ2OriginalPresentedFiber_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y))
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Countable (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) := by
  letI : Countable (NativeGJOriginalPresentedTotal p D E) :=
    nativeGJ2OriginalPresentedTotal_countable hobjD hhomD hobjE hhomE
  have hinj : Function.Injective
      (fun cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s =>
        (nativeGJPackPresented cell : NativeGJOriginalPresentedTotal p D E)) := by
    intro left right h
    exact eq_of_heq (Sigma.mk.inj h).2
  exact hinj.countable

/-- The ACTUAL original raw F55 total on true physical C60 Site
axes is unconditionally Countable, retaining the complete proof. -/
theorem nativeGJ2PhysicalPresentedTotal_countable (p : Polygon) :
    Countable (NativeGJOriginalPresentedTotal p Site Site) :=
  nativeGJ2OriginalPresentedTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

/-- Each actual parallel C60 F54 raw route pair has a Countable
original F55 nine-constructor proof fiber, without quotienting. -/
theorem nativeGJ2PhysicalPresentedFiber_countable
    (p : Polygon)
    {a b x y : Site}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Countable (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :=
  nativeGJ2OriginalPresentedFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable r s

/-- All true physical C60 polygons carry Countable original F55
proof totals with full independent two-axis history. -/
theorem nativeGJ2PhysicalAllPolygonPresented_countable :
    Countable (Σ p : Polygon,
      NativeGJOriginalPresentedTotal p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon,
      Countable (NativeGJOriginalPresentedTotal p Site Site) :=
    nativeGJ2PhysicalPresentedTotal_countable
  infer_instance

#print axioms nativeGJ2TransExact_eq
#print axioms nativeGJ2LeftExact_eq
#print axioms nativeGJ2RightExact_eq
#print axioms nativeGJ2PreExact_eq
#print axioms nativeGJ2PostExact_eq
#print axioms nativeGJ2Pentagon_decode_pack
#print axioms nativeGJ2Square_decode_pack
#print axioms nativeGJ2Decode_encodePresented
#print axioms nativeGJ2OriginalPresentedTotal_countable
#print axioms nativeGJ2OriginalPresentedFiber_countable
#print axioms nativeGJ2PhysicalPresentedTotal_countable
#print axioms nativeGJ2PhysicalPresentedFiber_countable
#print axioms nativeGJ2PhysicalAllPolygonPresented_countable

end
end Kuu.F112.Physical
