import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK3P92TypedCode

/-!
# F112-P94D3GK3 — original P92B exact dependent partial decoder

All 9 genuine P92B constructors are reconstructed, with two distinct
primitive tags. Type-incompatible original F54 routes, full D/E Blocks,
Nat depths and intermediate F45 trees are rejected. This is NOT the
old F55 PresentedCell, the GK2 F54 structural seam, or a quotient.
Append-only, no Gray, no sorry. Copyright Hidetoshi Itakura.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-! Exact full Type-valued gluing adapted to the DISTINCT P92B source. -/

noncomputable def nativeGK3P92TransExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGKOriginalP92Total p D E →
    NativeGKOriginalP92Total p D E →
    Option (NativeGKOriginalP92Total p D E)
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
noncomputable def nativeGK3P92LeftExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGKOriginalP92Total p D E →
    NativeGHOriginalF45Total p D E →
    Option (NativeGKOriginalP92Total p D E)
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
noncomputable def nativeGK3P92RightExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGHOriginalF45Total p D E →
    NativeGKOriginalP92Total p D E →
    Option (NativeGKOriginalP92Total p D E)
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
noncomputable def nativeGK3P92PreExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIOriginalDepthTotal p D E →
    NativeGKOriginalP92Total p D E →
    Option (NativeGKOriginalP92Total p D E)
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
noncomputable def nativeGK3P92PostExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGKOriginalP92Total p D E →
    NativeGIOriginalDepthTotal p D E →
    Option (NativeGKOriginalP92Total p D E)
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


/-- Exact typed P92B partial interpreter for all nine constructors. -/
noncomputable def nativeGK3P92Decode
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK3P92TypedCode p D E →
    Option (NativeGKOriginalP92Total p D E)
  | .original ⟨⟨⟨boundary, r⟩, s⟩, source⟩ =>
      some ⟨⟨⟨boundary, r⟩, s⟩, .original source⟩
  | .assocNaturality atom =>
      some (nativeGKInterpretP92Naturality atom)
  | .refl ⟨boundary, route⟩ =>
      some ⟨⟨⟨boundary, route⟩, route⟩, .refl route⟩
  | .symm inner =>
      (nativeGK3P92Decode inner).map
        (fun ⟨⟨⟨boundary, r⟩, s⟩, cell⟩ =>
          ⟨⟨⟨boundary, s⟩, r⟩, .symm cell⟩)
  | .trans left right =>
      (nativeGK3P92Decode left).bind (fun rawLeft =>
        (nativeGK3P92Decode right).bind (fun rawRight =>
          nativeGK3P92TransExact rawLeft rawRight))
  | .leftContext inner later =>
      (nativeGK3P92Decode inner).bind (fun raw =>
        nativeGK3P92LeftExact raw later)
  | .rightContext earlier inner =>
      (nativeGK3P92Decode inner).bind (fun raw =>
        nativeGK3P92RightExact earlier raw)
  | .precompose route inner =>
      (nativeGK3P92Decode inner).bind (fun raw =>
        nativeGK3P92PreExact route raw)
  | .postcompose inner route =>
      (nativeGK3P92Decode inner).bind (fun raw =>
        nativeGK3P92PostExact raw route)

end
end Kuu.F112.Physical
