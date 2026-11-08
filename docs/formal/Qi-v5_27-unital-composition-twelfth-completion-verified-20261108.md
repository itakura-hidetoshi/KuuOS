# Qi v5.27 — 型付き第十二セルの選択的単位・同側合成補完と観測の降下

2026-11-08 JST。Repository: `itakura-hidetoshi/KuuOS`。唯一のcanonical branch: `main`。

## 1. 厳密な正本と検証

| 項目 | exact-sourceで確認した状態 |
|---|---|
| 継承元main | `4dadac90313a3068bc60cd1088ef07c74eeedca3`（Qi v5.26まで） |
| 新規定理PR | [#3309](https://github.com/itakura-hidetoshi/KuuOS/pull/3309) **MERGED** |
| 定理source HEAD | `61ed5dac3ecabbe3fa578937357db5ff599cbaa8` |
| 定理test-merge HEAD | `216f94d482107f87c9d931de374de7749ffd1c96` |
| 定理squash main HEAD | `25e5c08d896175531cac24814efbd5cf29d7938a` |
| 上記3 commitのGit tree | **`be30d59fc2219a63ed682ef8772ab334a59a72f3` 完全一致** |
| 新規定理exact-source CI | [#42444566108](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42444566108) **completed / SUCCESS** |
| Scoped Lean | **9,079 / 9,079 SUCCESS** |
| Governance | **選択5ジョブ / 5ジョブ SUCCESS** |
| 新規宣言の公理監査 | **26 / 26**（12件公理不要、14件標準公理のみ） |
| 使用した標準公理 | `propext`・`Quot.sound`、新規公理なし |
| `sorryAx`・変更Leanエラー/警告 | **なし・0/0** |
| 定理差分 | 新規独立Leanファイル1件、457行追加／削除0 |
| 公開集約PR | [#3310](https://github.com/itakura-hidetoshi/KuuOS/pull/3310) **MERGED** |
| 公開集約exact-source CI | [#42444916420](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42444916420) **completed / SUCCESS** |
| KuuOSFormal Strict Lean | **10,340 / 10,340 SUCCESS** |
| 公開集約Governance | **30 / 30 SUCCESS** |
| 公開集約source/test-merge/squash Git tree | **`c50f7b8c1ff3c91dd0132530b34b9d828b62c34f` 完全一致** |
| 公開集約squash main | `077b37f1a1cfd3acac32aa0073b8d31b0f32a3b7` |
| 固定toolchain | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護対象 | 公開root107、PR #1558 Draft／OPEN／未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77UnitalCompositionCompletionV5_27.lean)。

対象限定CIの9,079ジョブと公開集約CIの10,340ジョブは**別の検証**である。新定理PRのsource/test-merge/squash tree一致、公開import追加PRのsource/test-merge/squash tree一致をそれぞれ独立に確認した。過去の全てのLean証明が公理不要だとは主張しない。

## 2. 最小の選択的文脈補完

新たな独立Type `SelectedUnitalCompositionTwelve W l r F G` は、v5.25の`ContextClosedFramedTwelve`の真正生証拠を`previous`へそのまま格納する。既存構文の変更は一切ない。

`strict/reverse/chain`、元第七セルの境界適合的`whiskerLeft/whiskerRight`は新presentation側でも保持する。そのうえで、型付き第十二セル比較生成元は**次の4種類だけ**を新設した：

- `unitLeft`：元第七セル`refl c`で左whiskeringした元packetと元packetとの比較。
- `unitRight`：元第七セル`refl d`で右whiskeringした元packetと元packetとの比較。
- `compLeft`：左文脈を2回逐次適用したpacketと、元`SevenRewrite.trans`で合成した文脈を1回適用したpacketとの比較。
- `compRight`：右文脈の逐次適用と、元`SevenRewrite.trans`合成文脈の適用との比較。

いずれも元第六セル境界`c,d`と真の元第七〜第十一セルType値を添字として保持する。既存の第六〜第十四セルの構成子に単位・合成法則を密かに追加したのではなく、**新たに選択した比較presentationのみ**に法則を導入した。

`IsSelectedUnitalCongruence`と`selectedUnital_least`は、元v5.25比較とこの4種類の局所生成元を含む同値関係・左右文脈閉包に関して、新比較が**最小の関係**であると証明する。最小性は指定した生成規則に関するもので、任意の外部coherenceまで含む万能的最小性ではない。

## 3. 新しい境界付き商における厳密な単位則と合成則

元第六セルの正確な境界`c,d`ごとに`selectedUnitalBoundarySetoid`を構成し、商を`Q_{27}(c,d)`と表す。元第七セルの文脈`u:b→c`、`v:d→e`に対して、元の真のwhiskeringを使った

\[
L_u:Q_{27}(c,d)\to Q_{27}(b,d),\qquad
R_v:Q_{27}(c,d)\to Q_{27}(c,e)
\]

が新比較に関してwell-definedであることを`Quotient.lift`で証明した。

`selectedUnitalLeft_unit`・`selectedUnitalRight_unit`はすべての商の点`x`について

\[
\boxed{L_{\mathrm{refl}}(x)=x,\qquad R_{\mathrm{refl}}(x)=x.}
\]

`selectedUnitalLeft_comp`・`selectedUnitalRight_comp`は型付きの合成可能な二つの元第七セル文脈について

\[
\boxed{L_u(L_v(x))=L_{u\cdot v}(x),\qquad
R_v(R_u(x))=R_{u\cdot v}(x).}
\]

を証明した。さらに`selectedUnital_actions_commute`は、v5.18の元`doubleWhisker`から来る真正旧比較証拠を二重に包含し、**左右反対側の作用の交換則**を維持する。

これらは選択商上の等式であり、元の生`FramedEleven`値のEqではない。

## 4. 元証拠の保存と、従来の履歴長の非降下

`selectedUnital_previous_injective`は旧v5.25の**生の十二セル証拠値**の新Typeへの埋込みが単射であることを証明する。一方、`contextToSelectedUnital`は旧v5.25商から新v5.27商への自然な写像を構成するが、この商写像は単射ではない。

実在する元`MixedExchangeUnitElevenCell.exchangeUnit`から`ContextFrameEleven`証拠を作り、反射左文脈の前後で元raw第十セルのwhisker総履歴長が1増えることを用いると、

\[
\operatorname{contextClosedClass}(L_{\mathrm{refl}} F)
\ne\operatorname{contextClosedClass}(F)
\quad\text{but}\quad
\operatorname{selectedUnitalClass}(L_{\mathrm{refl}}F)
=\operatorname{selectedUnitalClass}(F).
\]

したがって、新商から全raw packetの旧長さ`contextTraceLength`を再構成する観測写像は存在しない：

\[
\boxed{\neg\exists\, O:Q_{27}\to\mathbb N\;\;
\forall F,\ O([F])=|\mathrm{Trace}_{10}(F)|.}
\]

`selectedUnital_contextQuotient_notInjective`と`selectedUnital_noLengthDescent`でそれぞれ証明した。
元の生packetの履歴は削除されず、**選択商からの読み出しに関してのみ区別が失われる**。

## 5. 三つの元観測量は保存され、tenSymm障害は残る

従来の真正元第十セル関連三計数

\[
C(F)=
(\mathrm{oldTenthCount}(F),
\mathrm{unitTenthCount}(F),
\mathrm{tenSymmCount}(F))\in\mathbb N^3
\]

に対し、`selectedUnital_preservesCounts`は新第十二セルの**全10構成子**を帰納して保存を証明する。`selectedUnitalEventCounts`は新商からこの三つ組への実際の`Quotient.lift`を構成する。

`selectedUnital_retainsTenSymmObstruction`は元v5.18のtenSymm critical loopとその反射packetの間に新比較が存在しないと証明した。これにより補完は全packetを無条件に同一視しない。ただし三計数が全新比較を完全分類するという逆方向は未証明。

## 6. authority境界・次の課題

本結果は、元第七セル・第十一セル証拠から導いた**独立の選択第十二セルpresentation**における定理である。元F55/P77/GK5CGの同一視、既存6D〜14Dのraw Eq、v5.22/23の選択13D/14Dとの全面的自然性、任意高次cubeのcoherence、汎用的な完全正規化は主張していない。

次のQi v5.28では、新商上で同側合成法則が複数の括弧付け・三連文脈の貼り合わせと整合するか、旧13D/14Dの選択比較へ移送できる条件は何か、さらに一段上の証拠履歴を保持しながら調べる。

append-only／tighten-only／overwrite-forbidden／same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
