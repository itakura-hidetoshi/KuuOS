# Qi v5.69 — 全祖先塔＋全連続反転数塔でも残る順序付き反転ラン障害（Lean4形式証明・公理監査）

2026年11月10日 JST。**数学的定理の対象は、真正の元依存型18D raw証拠と、独立した新7構成子の19D Type値比較から構成する真正商の同一fiberである。** KuuOSの「空」「縁起」との対応は命名・解釈の層であり、形式定理自体がその哲学的同一性を証明するわけではない。

## 唯一の正本・証明と検証の来歴

- Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。開始時のQi v5.68正式統合済みHEAD `1746603cd48b91d84bf8681d81dd31f58e6d46fd`。
- [定理PR #3437](https://github.com/itakura-hidetoshi/KuuOS/pull/3437) **MERGED**。新規Leanモジュール `formal/KUOS/Architecture/QiWuxingGK5CHP77FullDoubleInfiniteOrderedRunResidualV5_69.lean` 1件のみ、最終676行追加・既存ファイル削除0。認証source HEAD `cbeef40ae9a0b43d31b0bceec058e06d5743d7fb`、squash merge `e1d20e678a458a1f6dc92986aa2f5bf87001a8b8`。
- 定理[exact-source CI #42688363378](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42688363378) **completed SUCCESS**：Scoped Strict Lean **9,121/9,121**、Governance **5/5**、40新規宣言の実公理監査、変更Lean error/warning **0/0**、exact-head受領書2件SUCCESS。source／test-merge／squash Git tree `13be132a025ad5177dbc04ba5c2619a3f5f09327` 完全一致。
- [公開import PR #3438](https://github.com/itakura-hidetoshi/KuuOS/pull/3438) **MERGED**。`formal/KuuOSFormal.lean`にimport1行のみ追加、旧ソースや公開importsの削除0。認証source HEAD `ac0f62de0e3461cce7a3483a0e2a9b8537ec5735`、squash merge `cadb784fa72706529468b74ed69eb8dab18c0e14`。
- 公開[exact-source CI #42689402624](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42689402624) **completed SUCCESS**：KuuOSFormal Strict Lean **10,382/10,382**、Governance **30/30**、同じ40宣言の公理監査、変更Lean error/warning **0/0**、exact-head受領書2件SUCCESS。source／test-merge／squash Git tree `89c5f7c28b5f73592a696093cf90e60fd5c3caaf` 完全一致。
- 固定：Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root **107**。保護[PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ維持。

## v5.68からの新しい数学的条件：全二重無限観測

v5.68では、元18D raw reverseの長さ別出現数`RunCount_d`（長さ`d+1`の連続反転部分列数）が、旧selected19の5構成子と新7構成子のすべてで保存され、新・旧商へそれぞれ`Quotient.lift`で降下することを証明済みだった。しかしv5.68の証拠対は、未観測の次次数`RunCount_(n+3)`で区別できるため、**全次数のRunCountを同時に観測する反例ではなかった**。

今回は真の新7構成子商の観測を

```text
Obs_double(q) =
  (selectedRawCongruentNineFullTowerObservation(q),
   (d : Nat) ↦ selectedRawCongruentRunCountOnQuotient(d, q))

型：Quotient →
  (selectedRawNineObservationValue × (Nat → Nat)) × (Nat → Nat)
```

と定義。ここで第1の`Nat→Nat`は**全次数の祖先塔**、第2の`Nat→Nat`は**全次数の直接連続反転数塔**である。有限prefixや有限サンプルには切り詰めない。

## 真正18Dにおける順序付き反転ランの新しい独立不変量

新規`selectedContextEighteenOrderedRunList`は、元`SelectedContextualEighteen`の構造再帰により**直接連続するraw reverseの長さを生の出現順で`List Nat`として保持**する。`strict`と`inherited`は空列、whiskeringは内部履歴を保持、chainは左右列を連結する。reverseはその子の`TopRunLength=0`なら新たな先頭runを1として加え、正なら子の先頭runを1延長する。元18D Type値の代わりに任意の代理構文を導入して比較を増やすことはない。

保存性は独立に確認した。

1. 元の`SelectedLocalNineteen` 5構成子：unitPrepend／unitAppendを含めて順序付き列を保存。
2. 新しい`SelectedRawCongruentNineteen` 7構成子：rawReverseでは新規ordered listの帰納仮定に加えv5.68で保存済みの`TopRunLength`を使い、rawChainLeft／Rightではordered listの連結に対する合同性を証明。
3. 旧・新商それぞれに対し真正`Quotient.lift`で同じ元Type値から順序付きラン列を降下。既存`selectedRawCongruentProject`での旧→新射影とも因子化。

これは旧selected19商と新7構成子商を同一視する主張ではなく、**それぞれ異なる比較presentation上で共通する元不変量が保存される**という形式的構成である。

## 全祖先塔と全連続反転数塔が一致する真正証拠対

真正17D端点`N`に対して`S=strict N`、`gap(X)=chain X S`、`R^k`を元raw reverseの`Nat.rec`反復として、

```text
A = R^3 (gap (R^2 S))    -- 順序付きrun [3,2]
B = R^2 (gap (R^3 S))    -- 順序付きrun [2,3]
```

を、実在する同一N→Nの元18D依存Type値として構成。次をLean4で証明した。

```text
∀ k : Nat, AncestorCount_k(A) = AncestorCount_k(B)
∀ d : Nat, RunCount_d(A) = RunCount_d(B)
Trace(A) = Trace(B)
TopReverseFlag(A) = TopReverseFlag(B)
AdjacentReverseCount(A) = AdjacentReverseCount(B)
NineObservation(A) = NineObservation(B)

OrderedRunList(A) = [3,2]
OrderedRunList(B) = [2,3]
OrderedRunList(A) ≠ OrderedRunList(B)
```

任意の二ブロック長`p,q`に対し、`RunCount_d(R^p(gap(R^q S)))=(p-d)+(q-d)`（自然数の切断減算）という真正raw計数式を定理化した。この値は`p,q`の交換に不変なので、**全てのdを同時に一致**させる。

祖先塔についても、strict-chain gapを除いても各次数の計数が不変である既証明を、反転反復の全次数保存と合成し、`p+q=q+p`によって**全てのkを同時に一致**させる。v5.60のC₁〜C₅橋渡し、完全ordered trace、top reverseと既存Adjacencyの一致から元八観測、さらにC₆で第九観測まで一致を確認した。

一方、`[3,2]≠[2,3]`は新商へ独立に降下済みのordered list不変量で区別できる。したがって、**真正新商クラスは不一致**であり、両者を比較する新19D Type値証拠も存在しない。

## 元の同一fiberへの輸送・非単射性・decoder障害

`M : SelectedContextualEighteen W l r J N`という**元の真正証拠が実際に供給された場合に限り**、`chain M A`と`chain M B`を元と同一J→N dependent fiberに構成した。全無限祖先塔、全無限run-count塔、元九観測は右連結で一致したまま、順序付きrun listは共通の`OrderedRunList(M)`を前置した二列になる。一般の`List Nat`の左連結消去（prefix cancellation）を証明し、元の`[3,2]≠[2,3]`の差がこの同一fiber内でも消えないことを認証した。

この結果から、実在する任意のMを持つ同一fiberの真の新商で：

- `Obs_double : Quotient → (Nine × AncestorTower) × RunTower`は**非単射**。
- `Obs_double`から全域でordered raw-run listを復元するdecoderは存在しない。
- 同観測から全ての新商クラスを復元するdecoderも存在しない。
- 指定された元17D端点Jについて、元の`strict J`を用いたJ→Jの真正例が存在する。

異端点fiberの任意の非空性、異fiberの比較や貼合は一切仮定していない。

## Lean4エラー修正と40宣言公理監査

- 初回[CI #42687580117](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42687580117)では、補助定理`selectedOrderedRunList_prefixCancel`の引数名`prefix`がLean4の**予約語**であるため構文解析に失敗。後段に未知の定理名と未解決ゴールが連鎖したが、数学的な保存性・証拠対の定理本体には独立の型エラーは検出されなかった。
- 変更ファイル全677行、importするv5.68、旧新19D比較の構成子および失敗ログ全体を照合して、補助定理内の引数名を`pre`へ変更しただけで復旧。仮定・定理文・元Type値・商の定義・旧証拠は不変。
- 修正後[CI #42688363378](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42688363378)と公開[CI #42689402624](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42689402624)で新規40宣言すべて`#print axioms`の実ログ確認：**公理不要11・標準公理のみ29**（`propext`、`Quot.sound`、`Classical.choice`）、新規`sorryAx`0、変更Lean error/warning0/0。exact-head受領書2件ずつSUCCESS。これは当該ソース・固定依存閉包の機械的認証である。

## 未認証境界・次段Qi v5.70

今回認証されたのは、**全祖先塔と全run-count塔を同時に持つ商観測が非単射であること**であり、順序付きラン列を追加した次の観測が完全分類子になるという主張ではない。順序付きラン列が一致する別の真正元18D証拠対の探索、または限定された構文クラス／exact fiber上での条件付き忠実性が次段の候補となる。

全無限順序付き履歴を加えた後の単射性、任意異端点fiberの非空性、異fiber whiskering、20D gluing、全WORLDへの貼合、全商の完全分類および制度的権限は未認証（NO_DATA）とする。元18D依存Type値、旧selected19／新独立7構成子比較の分離、公開root107、Lean/mathlib固定pin、保護#1558 Draft／OPEN／未マージを維持。append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
