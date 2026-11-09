# Qi v5.68 — 全無限祖先塔に加え任意有限長の連続反転観測でも残る障害（Lean4形式証明・公理監査）

2026年11月10日 JST。**形式命題は真正の依存型18D raw証拠および、それを新7構成子の19D Type値比較で商にした同一fiberの局所的識別限界に限定される。**「空」「縁起」との対応は命名・解釈の層であり、Lean4で証明される数学的定理の意味に含めない。

## 正本・形式成果物・認証の来歴

- Repository: `itakura-hidetoshi/KuuOS`、canonical branch `main`。出発点はQi v5.67正式統合HEAD `f1f5fb16dc359e8dcf744f2e4650f3a6a046be85`。
- [定理PR #3434](https://github.com/itakura-hidetoshi/KuuOS/pull/3434) **MERGED**。新規Leanモジュール `formal/KUOS/Architecture/QiWuxingGK5CHP77UniformConsecutiveRunTowerObstructionV5_68.lean` **1件867行追加・既存Lean削除0**。認証済みsource HEAD `4788cc911b0a34766d254058f04cb81a48bcc26d`、squash merge `888be633ed71deaf2858e995f37797c70dd21b24`。
- 定理[exact-source CI #42638793890](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42638793890) **completed SUCCESS**：Scoped Strict Lean **9,120/9,120**、Governance **5/5**、新規47宣言全件公理監査、変更Lean error/warning **0/0**、exact-head受領書2件SUCCESS。source／test-merge／squash Git tree `03c4750a5cc2bcad1de8231f02721970e1077654` が一致。
- [公開import PR #3435](https://github.com/itakura-hidetoshi/KuuOS/pull/3435) **MERGED**。`formal/KuuOSFormal.lean` に**import1行だけ**追加し、旧importsは全て保持。認証済みsource HEAD `aa99afc37a3773e23270a8162c9df59a6470cc41`、squash merge `7139c708b2e5b8802b06da5a2037add3ca598057`。
- 公開[exact-source CI #42640128599](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42640128599) **completed SUCCESS**：KuuOSFormal Strict Lean **10,381/10,381**、Governance **30/30**、新規47宣言の公理監査は定理側と一致、変更Lean error/warning **0/0**、exact-head受領書2件SUCCESS。source／test-merge／squash Git tree `d6a2a2587c6d4814a00c60a90ff47891271027c3` が一致。
- 固定：Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root **107**。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージを維持。

## 全次数連続反転数：元依存Typeへの定義と商への保存

新定義 `selectedContextEighteenTopRunLength` は、生の外側に**連続して現れるraw reverseの長さ**を再帰的に数える。外側がchain・strict・inherited・whiskerの場合は0である。

`selectedContextEighteenConsecutiveRunCount l r d A` は、**長さ`d+1`の直接連続したraw reverse部分列の出現数**を元18D証拠`A`で構造再帰により数える。`reverse A`のとき、内側の計数に `if d ≤ topRunLength(A) then 1 else 0` を加える。chainは左右計数の和、whiskerは内側の計数を保存し、元のType値と証明履歴を失わない。

この`Nat`全次数の計数について、それぞれ別個の機械的構造帰納法で：

1. 元`SelectedLocalNineteen`の**5構成子**すべてに対するtop-run lengthとrun-countの保存、
2. 新`SelectedRawCongruentNineteen`の**7構成子**すべてに対する保存（rawReverseで帰納仮定とtop-run length保存を併用）、
3. 旧selected19商と新7構成子商の**別々の`Quotient.lift`**および旧→新projectionとの因子化、

を証明した。旧19D Type比較と新19D Type比較は別のpresentationのままであり、片方をもう一方と同一視していない。

さらに`d=1`では、今回のrun-countが既存v5.53の`AdjacentReverseCount`と元18D Type値上で**完全一致**することを構造帰納法で検証した。低次数と既存の真正観測の対応を、単なる命名だけではなく明示的な証明にしている。

## 具体的な全n反例族：全祖先塔の一致と次連続長の障害

任意の`n : Nat`と真正17D端点`N`に対し、元の`SelectedContextualEighteen W l r N N`上で`Nat.rec`によりraw reverse反復`R^p`を構成し、`S = strict N`、`gap(X) = chain X S`として、

```text
A_n = R^(n+4) (gap (R^(n+2) S))    -- 連続ラン [n+4,n+2]
B_n = R^(n+3) (gap (R^(n+3) S))    -- 連続ラン [n+3,n+3]
```

を真正Type値として定義した。定理では、次の等式を**全自然数nと全次数d**について個別に証明している。

```text
∀ k : Nat, C_k(A_n) = C_k(B_n)      -- 全無限祖先塔（Nat → Nat）
Trace(A_n) = Trace(B_n)
TopReverseFlag(A_n) = TopReverseFlag(B_n)
AdjacentReverseCount(A_n) = AdjacentReverseCount(B_n)
RunCount_d(A_n) = RunCount_d(B_n)    (d ≤ n+2)
RunCount_(n+3)(A_n) = RunCount_(n+3)(B_n) + 1
```

両方のrun-countの明示式は、`(n+4-d)+(n+2-d)`と`(n+3-d)+(n+3-d)`（`Nat`の切断減算）。`d≤n+2`で一致し、`d=n+3`で左1・右0となる。run-countの添字`d`が長さ`d+1`を表すため、**長さ`n+3`以下では一致し、長さ`n+4`で初めて相違**する。

全塔一致は、strict chainの挿入が真正祖先塔の各座標を変えないこと、raw reverseを同じ回数だけ反復した証拠間の全座標一致を保存すること、合計反転回数`(n+2)+(n+4)=(n+3)+(n+3)`という証明を接続している。有限サンプリングから無限への帰納的飛躍はない。v5.60の橋渡しで旧八観測を、さらに`C_6`によって九番目を一致させる。

違いは新商に独立に降下済みの`RunCount_(n+3)`が証明するため、`selectedRawCongruentClass`の不一致および元証拠対に対する真正新19D Type比較の不存在を導いた。

## exact fiberへの輸送と非単射定理の範囲

任意の異端点fiberの非空性を仮定で追加する代わりに、**実在する元証拠`M : SelectedContextualEighteen W l r J N`が供給された場合のみ**、`chain M A_n`／`chain M B_n`を同じJ→N fiber内へ構成した。九変量・全祖先塔・短い連続ラン計数の等式、および次の計数の差1が保存されることを明示証明している。

真正新商上の結合観測は

```text
Obs_n(q) : (selectedRawNineObservationValue × (Nat → Nat))
           × (Fin (n+3) → Nat)
Obs_n(q) := (NineFullTower(q), i ↦ RunCount_i(q))
```

であり、既存九成分と**全自然数祖先塔**、および短い連続ラン数を同時に読む。与えられた実在Mの同一fiberで、この`Obs_n`は**非単射**、次計数`RunCount_(n+3)`の全域decoderおよび商クラス全復元decoderは存在しない。指定された任意のJ→Jでは本来の`strict J`から具体的な同一fiber反例を得る。

これは、**任意の有限個の連続長計数＋全無限祖先塔**を加えても、この形の真正商観測では完全識別できないという一様な結果である。一方、**全自然数dのrun-countを同時に観測した場合の単射性**については、今回の証拠対では次の計数で区別できるため、結論を出さない。

## 修正・公理監査・検証境界

- 初回定理CI [#42637934249](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42637934249) は、真正fiberでの次計数差の証明`selectedUniformRunWitnessFiber_nextCountGap`において、`rw`後の加法結合順序 `a+(b+1)=(a+b)+1` が残りFAILURE。失敗ログの未解決ゴールを追跡し、新規Lean全文・依存するv5.67・関連signatureを照合したうえで、**`omega`1行だけ追加**した。元証拠、定理文、仮定、既存比較に変更はない。
- 初回の下流`sorryAx`診断6件は未解決ゴールの伝播であり、**認証済みとは扱わない**。修正版CI #42638793890 と公開CI #42640128599の全47宣言実出力では**公理不要9、標準公理のみ38**（`propext`、`Quot.sound`、`Classical.choice`）、**新規`sorryAx`0**、変更Lean error/warning **0/0**。
- CI SUCCESSは、このsourceとその固定依存閉包に関する機械的認証である。命名層の「空」「縁起」の哲学的同一性、外部への行為権限、将来の全更新までの自動的な保証ではない。

## 未認証境界と次段Qi v5.69

**全run-count塔`(Nat → Nat)`と全祖先塔`(Nat → Nat)`を同時に持つ真の結合観測が、真正新商を完全識別するか**は未認証（NO_DATA）。今回の`[n+4,n+2]`対`[n+3,n+3]`はそれぞれ`n+3`次数のrun-countが異なるため、全run-count塔の反例に転用してはならない。次段は、全run-count塔の非単射性を示す新しい真正証拠対の探索、または限定されたfiber／構文クラス上での条件付き忠実性を調べるのが正確である。

任意異端点fiberの非空性、異fiber whiskering、20D gluing、全WORLD大域貼合、全商分類および制度的権限も依然NO_DATA。元18D依存Type値、独立する旧selected19／新7構成子19D Type比較、公開root107、固定Lean/mathlib、保護#1558 Draft／OPEN／未マージを維持する。append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
