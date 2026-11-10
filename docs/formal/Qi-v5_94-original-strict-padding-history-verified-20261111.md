# Qi v5.94 — 真正旧18Dの同一fiber無限strict配置族と型付きunit履歴の非単射（Lean4形式証明）

2026年11月11日 JST。唯一の正本は `itakura-hidetoshi/KuuOS` の `main`。形式対象は**元の真正依存型** `SelectedLocalEighteen W l r J N`、その元raw17D端点 `J,N`、v5.73非結合内部括弧観測、v5.89元unit数、v5.92元の完全な型付きunit葉payload履歴である。「空・縁起・二諦・中道」と形式構造の対応づけは解釈・命名層であり、Lean4が哲学概念を証明したという意味ではない。

## 1．一次正本と独立CIの来歴

- v5.93三段階統合後の基準main：`ea9d130d214711cac13d4e2137fe178cd79cb6a1`。
- [新規Lean4定理PR #3512](https://github.com/itakura-hidetoshi/KuuOS/pull/3512) **MERGED**。新規ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77OriginalStrictPaddingHistoryV5_94.lean` のみ、GitHub差分**422行追加・既存行削除0**。実際の公理監査命令17件。元17D・18D・19D Type・構成子・比較規則、既存定理文を変更しない。
- 修正後の認証source `6dbd51c76a837f1cbef425dffd7036f1abb405ee`。定理squash後main `a14931811cb79f2a86424878fab732d3e7422923`。source／test-merge／squash main Git tree **`62ed6b100ec315042ac147b35c46188bd7e081a4`一致**。
- [定理CI #42919425256](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42919425256) **completed／SUCCESS**。Scoped Strict Lean **9,146／9,146**、独立Kuu Core・選択Governance・workflow整合性すべてSUCCESS。
- [公開import PR #3513](https://github.com/itakura-hidetoshi/KuuOS/pull/3513) **MERGED**。`formal/KuuOSFormal.lean`に新規import**1行のみ**追加。公開source `923a303c7dd04abb0c1d5b8c0b35c3234ce29a51`、squash後main `6cedd684bf3c6ef3c4b884cac1a3f34f971c8c55`。source／test-merge／squash main Git tree **`631df2262b336e4e1e25351947a31bb260113e50`一致**。
- [公開CI #42923231337](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42923231337) **completed／SUCCESS**。公開`KuuOSFormal`依存閉包 **10,407／10,407**、Governance **30／30 SUCCESS**、独立Kuu Core SUCCESS。
- 双方の実ログ：公理監査 **17／17**、**公理不要7宣言**・**`propext`のみ4宣言**・**`propext`と`Quot.sound`のみ6宣言**。新規`sorryAx`なし、対象Lean error/warning **0／0**。
- 固定：Lean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**、公開root107維持。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。

## 2．真正同一raw17D fiberでの自然数族

元の真正旧18D証拠 `M : SelectedLocalEighteen W l r J N` **が本当に与えられた条件下**で、元の構成子`strict`と`chain`だけを使用し、同じ型`J→N`に入る2つの関数を定義した。

```text
Prefix(0,M)   = M
Prefix(n+1,M) = chain (strict J) (Prefix(n,M)) : J→N

Suffix(0,M)   = M
Suffix(n+1,M) = chain (Suffix(n,M)) (strict N) : J→N
```

ここでは元のraw`strict`を何度重ねても`chain`の値を単位律で消さず、元証拠の真正の依存型indexを保持する。帰納法により全てのnについて、`OriginalUnitCount(Prefix(n,M))=OriginalUnitCount(M)`、`OriginalUnitCount(Suffix(n,M))=OriginalUnitCount(M)`を形式証明した。

v5.92の`selectedV592OriginalUnitHistory`は、真のunitLeft/right葉をそれぞれ元の証拠・raw17D始終端・`before/F/G/C/after`全データ付きで保持する。今回、`History(Prefix(n,M))=History(M)=History(Suffix(n,M))`を元の全旧18D Type上で証明。unit数や型付きunit payload履歴が同じだからといって元旧18D証拠が等しいわけではない。

## 3．元の非結合内部括弧での区別と無限単射

新`selectedV594InnerStrictCount`は、**既存v5.73のraw内部括弧構文木**を読む独立の自然数観測である。木の`oldStrict`を1、`oldUnitLeft`／`oldUnitRight`を0、`oldReversed`では再帰的に保存、`oldJoined`では加算する。

元のsource-inner-bracketを`Bracket`と略記すると、

```text
StrictCount(Bracket(Prefix(n,M))) = n + StrictCount(Bracket(M))
StrictCount(Bracket(Suffix(n,M))) = n + StrictCount(Bracket(M))
```

をLean4で帰納法により証明した。これを`congrArg`によって元の真のraw証拠等号に作用させ、`Nat → SelectedLocalEighteen W l r J N`として**Prefix族・Suffix族それぞれの単射性**を証明した。従って、固定Mを与えた同一真正fiberで異なるm≠nなら、元の完全型付きunit履歴は同じだが、内部括弧指紋は**異なり**、元raw証拠は**異なる**。

これは全Mについて同一fiberが無限に多くのraw証拠を含むという**条件付き・構成的定理**である。異なるfiber間の証拠を貼合せず、元19D商での同一性に拡張しない。

## 4．真正unitLeft／unitRight固有の元パラメータを保持した具体例

元v5.35の真正`unitLeft before F G C after : J→N`と独立の`unitRight before F G C after : J'→N'`について、それぞれ元の本当の端点を用いて

```text
A = chain (strict J) U  : J→N
B = chain U (strict N)  : J→N
```

を構成した。`selectedV594ActualLeftOneUnitStrictPlacementGap`／`selectedV594ActualRightOneUnitStrictPlacementGap`は左右を混同せずそれぞれ

```text
History(A) = History(B)
Bracket(A) ≠ Bracket(B)
OriginalUnitCount(A) = 1
OriginalUnitCount(B) = 1
A ≠ B
```

を**元の真正依存型のまま**証明する。例はunitCount=1の同じ`J→N`fiberにおける**履歴衝突と括弧不一致**であり、v5.93が要求した**括弧一致・raw不一致**の実例ではない。

## 5．初回Lean4失敗と構造的修正

[初回CI #42918731813](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42918731813)は、新規v5.94ファイル内の**4件**のLeanエラーでFAILURE。最初の2件（元167・184行）は`rfl`が`0+x=x`を定義的等号とは扱わないことによる帰納法のzero分岐失敗。残る2件（元205・217行）は`congrArg`後の関数適用`(fun n => ... ) m`が未簡約のままで、`rw`パターンに直接一致しなかったことによる。

元v5.35の依存型構成子と添字、v5.73括弧観測、v5.89 unit数、v5.92型付き履歴、v5.93既存証明、**新規Lean全文**を照合。zero分岐は`simpa only [selectedV594StrictPrefix, Nat.zero_add]`／Suffix対応に置き換え、単射証明では`congrArg`後の両側を具体的な型付き式へ`change ... at hc`で明示してから既存の補題で`rw`した。**4件の証明手順だけ**を修正し、仮定・定理文・旧ファイル・Lean/mathlib固定値は不変更。

修正後の両独立CIと公理監査はすべてSUCCESS、新規`sorryAx`なし。未完成の初回CIの公理出力は認証根拠として採用しない。

## 6．障害と次段Qi v5.95

**認証済み**：供給された真正旧18Dの固定fiberにおける元strict配置の自然数単射族、元unit数・真正型付きunit履歴の不変性、元の非結合括弧strict原子数による識別、左右の真正1-unit実例。

**NO_DATA**：同じ真正raw17D `J→N` fiberにあり、**v5.73内部括弧指紋まで等しく、元旧18D証拠が異なる**実例の存在／不可能性。v5.93の元1-unit source collision existenceを今回の履歴一致・括弧不一致で充足させない。count≥2という旧v5.91の必要条件を十分条件へ昇格しない。元unit payloadの一意復元、元旧5／新7の19D Type全域同値、異fiber gluing、WORLD／20D降下、制度的行為権限も未認証。

**次段v5.95研究対象**：v5.93の「1-unit元源同指紋・異raw」Propについて、元`unitLeft`／`unitRight`の依存型端点・パラメータの**同一構文位置での等号反映条件**を検討する。v5.94のstrict配置族が確実に括弧指紋を**変える**ことを前提とし、実際の同指紋衝突の存在・不可能性を未認証（NO_DATA）のまま扱う。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
