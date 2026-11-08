# Qi v5.25 — 型付き文脈閉包・第十二セル欠損面の補完・観測量の選択的保存

## 1. 正本・形式検証・公開範囲

2026年11月8日 JST。Canonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
Qi v5.24までの正本 `ad9ca00bf82a8b55cfc5b3cda2c45f2da17d9591` を継承。

| 項目 | 独立確認した結果 |
|---|---|
| 定理PR | [#3302](https://github.com/itakura-hidetoshi/KuuOS/pull/3302) MERGED |
| source HEAD | `6b8ae410b524ac2c4a56e0b66665d236d136cbee` |
| test-merge HEAD | `94749afe832349b793db0e7fe66cc51081316291` |
| squash / 定理main | `d57d79415abc80397fe8609f5765de088d7188b6` |
| 上記3つのGit tree | `f5adf74193b9d7481bb0e400259d5de5e2983e33` 完全一致 |
| exact-source CI | [#42439861875](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42439861875) completed / SUCCESS |
| Scoped Strict Lean | 対象モジュールと依存先 9,077 / 9,077 SUCCESS |
| Governance | 選択3チェックすべてpassed、欠落receipt・失敗なし |
| 新規宣言の公理依存 | 37 / 37確認、27件公理不要、10件標準公理のみ |
| 使用した標準公理 | 必要な宣言で `propext` / `Quot.sound` のみ |
| `sorryAx` / 変更Lean warning / error | 0 / 0 / 0 |
| 最終定理差分 | 独立新規Leanモジュール441行、削除0 |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保持 | 元6D〜14DのType・仮定・証拠履歴、公開root107、#1558 Draft/OPEN/未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ContextClosedTwelfthV5_25.lean)。

**今回の公開範囲は独立モジュールのmain追加である。**
`formal/KuuOSFormal.lean`へのimport追加とREADME/ROADMAP同期は未実施。
公開集約はcanonical blob `35ed1febcd6cb78b7148910b4876bb37bb43399e` と同一。
9,077という件数は対象限定ビルドの件数であり、以前の公開集約10,337ジョブとの
差を削除や証明喪失と解釈しない。またGovernanceは選択3チェックの成功であり、
30チェックの全再実行とは区別する。

実行コマンド：

```text
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KUOS.Architecture.QiWuxingGK5CHP77ContextClosedTwelfthV5_25
```

完全なLean receiptはreturn_code 0と上記test-merge SHAを記録。
完全ログの末尾は `Build completed successfully (9077 jobs)`。
Governanceの3件はLean、独立Kuu core/retained public proof API、workflow integrity。

## 2. 元の境界と証拠を保つ独立presentation

`ContextFrameEleven W l r c d`は、元第六セル境界 `c,d` を添字として固定し、
元第七〜第十一セル `s,t,q₀,q₁,alpha,beta,xi,zeta,H` をType値のまま保存する。
`contextFramePack`は既存 `FramedEleven` へ包装する。
左右の `contextFrameLeft` / `contextFrameRight` は、境界が合う元第七セル文脈を
元第十一セルの真正whiskeringへ渡す。異なる元fiberをEqで同一視しない。

新しい `ContextClosedFramedTwelve` は、既存のfull framed第十二セル証拠を
`previous`の引数にそのまま保持する。strict/reverse/chainに加え、
**新たな文脈規則は境界適合的なwhiskerLeftとwhiskerRightの二つだけ**である。
旧6D〜14Dの構成子を変更していない。

`contextClosed_previous_injective`は、旧raw第十二セル証拠値の埋込みの単射性を証明する。
これは商類の写像の単射性ではない。
`IsTypedWhiskerCongruence`で旧比較を含む同値関係と同じ左右文脈閉包条件を明示し、
`contextClosed_least`は新しい比較がそのようなすべての関係に含まれることを証明する。
この意味で、指定された型付き文脈規則に関する最小閉包である。

## 3. v5.24の欠けた面を導出する

v5.24の真正三重配置を、構成子の外側からの順序で
`F_LRR`、`F_RLR`、`F_RRL`と書く。
旧presentationには `F_LRR → F_RLR` が存在したが、末尾不変量によって
`F_RLR → F_RRL` は存在しなかった。

新しい `contextClosed_innerFace` は次の証拠を実際に組み立てる：

```text
whiskerRight
  (contextFrameOfRaw (whiskerLeft before (whiskerRight H inner)))
  (contextFrameOfRaw (whiskerRight (whiskerLeft before H) inner))
  (previous (doubleWhisker before H inner))
  outer
```

つまり、**元のdoubleWhisker証拠一つと新しい右文脈閉包一回**から欠損面を得る。
欠損面の存在そのものを特別な生成元として仮定していない。
`contextClosed_fullTriplePath`は旧外側交換面とこの新しい内側交換面を連結する。

`contextClosed_innerFace_strictExtension`が同時に証明する内容は

\[
\boxed{\operatorname{Nonempty}(\mathrm{New12}(F_{RLR},F_{RRL}))
\quad\land\quad
\neg\operatorname{Nonempty}(\mathrm{Old12}(F_{RLR},F_{RRL})).}
\]

旧不存在定理は取り消されない。異なるpresentationの比較能力を分離した結果である。
実在例には元の `exchangeUnit` と反射第七セル文脈を使う。

## 4. 保持されるraw証拠と、新商で失われる区別

旧商から新商への `oldToContextClosedQuotient` を構成する。
`oldToContextClosedQuotient_notInjective`は、上の実在する元exchangeUnit例で
この写像が非単射であることを証明する。

旧raw証拠の埋込みは単射だが、旧商で区別されていた二つのpacket類は新商で一致する。
`contextClosed_noOldReflection`は、新しいすべての比較を旧比較へ戻す解釈を否定する。

v5.24で旧商へ降下した末尾観測
`I(F) = drop 2 (Trace10(F))`についても、
`contextClosed_noTailDescent`が新商への降下を否定する。
元のpacketに保存した履歴が削除されたのではなく、**新しい商だけからは
その履歴を一意に読み出せない**という情報損失である。

## 5. 三つの元観測量と残る障害

`framedContextEventCounts`は元からある三つの計数を組にする：

\[
C(F)=(\mathrm{oldTenthCount}(F),\mathrm{unitTenthCount}(F),\mathrm{tenSymmCount}(F))
\in\mathbb N^3.
\]

`contextClosed_preservesEventCounts`は新しい全構成子で保存を証明し、
`contextClosedEventCounts`は新商からこの三つ組への `Quotient.lift` を構成する。
`contextClosed_retainsTenSymmObstruction`により、元のtenSymm critical loopと反射packetは
新しい比較でも接続されない。今回の補完は、すべてのpacketを無差別に同一視するものではない。
三計数が全比較を完全分類するという逆方向は未証明である。

## 6. 境界ごとの商に降下する左右作用

`contextBoundarySetoid`は、固定した元第六セル境界 `c,d` を持つpacket上で
新しい比較を用いる商を作る。
元第七セル `before:b→c`、`after:d→e`に対し、
`contextClosedLeftAction`と`contextClosedRightAction`が

\[
L_{before}:Q(c,d)\to Q(b,d),\qquad
R_{after}:Q(c,d)\to Q(c,e)
\]

を構成する。旧full商では失敗していた作用の降下を、明示した境界付き新商で実現した。
`contextClosedActions_commute`は元のdoubleWhiskerを使い

\[
\boxed{L_{before}(R_{after}(x))=R_{after}(L_{before}(x))}
\]

を証明する。これは新商上の等式であり、元のraw証拠が同じという主張ではない。
同じ側の文脈合成則・単位則、全packetの正規形、旧13D/14D証拠の自動的拡張は未証明。

## 7. 修正経緯と次の境界

公開集約の全文再送によって意図しないimport差分が生じたため、その編集は
Git blobを再利用して完全に戻した。最終定理PRは新規独立モジュール1件のみであり、
一時的な集約差分はmainへ到達していない。

対象CI #42439346295の実際のLeanエラーは同値定理1件：
`⟨Quotient.exact, Quotient.sound⟩`という未適用関数の組では、独自Setoidが
期待するwrapper越しに推論されなかった。
全文と依存型を照合し、両方向に `intro h` を置いてそれぞれの補題を適用した。
定理文・仮定を変えず、差分はその証明本体だけ。
失敗時の下流 `sorryAx` 表示はこのelaboration失敗の回復項であり、修正後には一切残らない。

次の実装課題は、保持済み公開集約への安全なimport追加と文書索引の同期。
次の研究候補は、同側の文脈合成・反射文脈作用を、保持されるraw履歴長などから調べること。
左右作用が交換するだけで、すべての関手法則や高次整合性が自動的に成立するとはしない。

append-only / tighten-only / overwrite-forbidden / same-root。

---
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
