import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGKSeamTypedCode

/-!
# F112-P94D3GK2 — strict dependent original 14-constructor decoder

All primitive source atoms retain their complete original Type-valued
F54 routes, F45 Trees and independent Nat depths. Recursive operations
accept only equal original D/E, Blocks, depth and genuine middle F54
route/F45 source proof terms. Mismatched boundaries return none.

Unlike a structural shadow, this decoder produces an original free
NativeF54StructuralSeam proof with NO conflation of P92B or F55.
The source left inverse is established separately in the next file.
Append-only. Copyright Hidetoshi Itakura / 板倉英俊.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-! Exact dependent original seam gluing. -/

noncomputable def nativeGK2TransExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK2OriginalSeamTotal p D E →
    NativeGK2OriginalSeamTotal p D E →
    Option (NativeGK2OriginalSeamTotal p D E)
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
noncomputable def nativeGK2LeftExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK2OriginalSeamTotal p D E →
    NativeGHOriginalF45Total p D E →
    Option (NativeGK2OriginalSeamTotal p D E)
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
                      .leftContextCongruence cell later⟩
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Original right F45 node context with both original D/E
Blocks and every Nat depth exactly preserved. -/
noncomputable def nativeGK2RightExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGHOriginalF45Total p D E →
    NativeGK2OriginalSeamTotal p D E →
    Option (NativeGK2OriginalSeamTotal p D E)
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
                      .rightContextCongruence earlier cell⟩
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Original *precompose* is accepted only when every D/E category
and Blocks endpoint, BOTH intermediate Nat grades and the ACTUAL
intermediate original F45 tree term coincide exactly. -/
noncomputable def nativeGK2PreExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIOriginalDepthTotal p D E →
    NativeGK2OriginalSeamTotal p D E →
    Option (NativeGK2OriginalSeamTotal p D E)
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
noncomputable def nativeGK2PostExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK2OriginalSeamTotal p D E →
    NativeGIOriginalDepthTotal p D E →
    Option (NativeGK2OriginalSeamTotal p D E)
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


/-! ### Four honest independent native F54 primitive interpreters -/

def nativeGK2InterpretReassoc
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (atom : NativeGK2ReassocAtom p D E) :
    NativeGK2OriginalSeamTotal p D E := by
  rcases atom with
    ⟨a, b, x, y, ma, pa, mb, pb,
      n₁, n₂, n₃, n₄, m₁, m₂, m₃, m₄,
      t₁, t₂, t₃, t₄, u, v, w⟩
  exact nativeGK2PackSeam (.reassoc u v w)

def nativeGK2InterpretLeftContextTrans
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (atom : NativeGK2LeftContextTransAtom p D E) :
    NativeGK2OriginalSeamTotal p D E := by
  rcases atom with
    ⟨a, b, x, y, ma, pa, mb, pb, mc, pc,
      n₁, n₂, n₃, m₁, m₂, m₃, k, l,
      t₁, t₂, t₃, later, u, v⟩
  exact nativeGK2PackSeam (.leftContextTrans u v later)

def nativeGK2InterpretRightContextTrans
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (atom : NativeGK2RightContextTransAtom p D E) :
    NativeGK2OriginalSeamTotal p D E := by
  rcases atom with
    ⟨a, b, x, y, ma, pa, mb, pb, mc, pc,
      k, l, n₁, n₂, n₃, m₁, m₂, m₃,
      earlier, t₁, t₂, t₃, u, v⟩
  exact nativeGK2PackSeam (.rightContextTrans earlier u v)

def nativeGK2InterpretLeftContextUnit
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (atom : NativeGK2AdjacentTreesAtom p D E) :
    NativeGK2OriginalSeamTotal p D E := by
  rcases atom with
    ⟨a, b, x, y, ma, pa, mb, pb, mc, pc,
      n, m, k, l, earlier, later⟩
  exact nativeGK2PackSeam (.leftContextUnit earlier later)

def nativeGK2InterpretRightContextUnit
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (atom : NativeGK2AdjacentTreesAtom p D E) :
    NativeGK2OriginalSeamTotal p D E := by
  rcases atom with
    ⟨a, b, x, y, ma, pa, mb, pb, mc, pc,
      n, m, k, l, earlier, later⟩
  exact nativeGK2PackSeam (.rightContextUnit earlier later)

/-- Original fourteen-constructor dependent partial interpreter,
rejecting mismatched intermediate raw F54 and F45 proofs. -/
noncomputable def nativeGK2DecodeStructural
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK2StructuralTypedCode p D E →
    Option (NativeGK2OriginalSeamTotal p D E)
  | .refl ⟨boundary, route⟩ =>
      some ⟨⟨⟨boundary, route⟩, route⟩, .refl route⟩
  | .symm prior =>
      (nativeGK2DecodeStructural prior).map
        (fun ⟨⟨⟨boundary, r⟩, s⟩, w⟩ =>
          ⟨⟨⟨boundary, s⟩, r⟩, .symm w⟩)
  | .trans prior later =>
      (nativeGK2DecodeStructural prior).bind (fun first =>
        (nativeGK2DecodeStructural later).bind (fun second =>
          nativeGK2TransExact first second))
  | .reassoc atom => some (nativeGK2InterpretReassoc atom)
  | .leftUnit ⟨boundary, route⟩ =>
      some ⟨⟨⟨boundary, .trans (.chain (.refl _)) route⟩, route⟩,
        .leftUnit route⟩
  | .rightUnit ⟨boundary, route⟩ =>
      some ⟨⟨⟨boundary, .trans route (.chain (.refl _))⟩, route⟩,
        .rightUnit route⟩
  | .precompose route prior =>
      (nativeGK2DecodeStructural prior).bind (fun raw =>
        nativeGK2PreExact route raw)
  | .postcompose prior route =>
      (nativeGK2DecodeStructural prior).bind (fun raw =>
        nativeGK2PostExact raw route)
  | .leftContextTrans atom =>
      some (nativeGK2InterpretLeftContextTrans atom)
  | .rightContextTrans atom =>
      some (nativeGK2InterpretRightContextTrans atom)
  | .leftContextUnit atom =>
      some (nativeGK2InterpretLeftContextUnit atom)
  | .rightContextUnit atom =>
      some (nativeGK2InterpretRightContextUnit atom)
  | .leftContextCongruence prior later =>
      (nativeGK2DecodeStructural prior).bind (fun raw =>
        nativeGK2LeftExact raw later)
  | .rightContextCongruence earlier prior =>
      (nativeGK2DecodeStructural prior).bind (fun raw =>
        nativeGK2RightExact earlier raw)

#print axioms nativeGK2InterpretReassoc
#print axioms nativeGK2InterpretLeftContextTrans
#print axioms nativeGK2InterpretRightContextTrans
#print axioms nativeGK2InterpretLeftContextUnit
#print axioms nativeGK2InterpretRightContextUnit

end
end Kuu.F112.Physical
