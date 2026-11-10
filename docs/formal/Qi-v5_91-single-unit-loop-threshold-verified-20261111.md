# Qi v5.91 — 真正旧18Dの単一unit非閉路性と同一fiber衝突のunit数下界（Lean4形式証明）

2026年11月11日 JST。canonical正本：`itakura-hidetoshi/KuuOS`の`main`。対象は元の依存型`SelectedLocalEighteen`の真正raw17D端点、既存v5.73内部括弧観測、および元旧5構成子・独立新7構成子の真正選択19D商とそれぞれの型付き比較である。名称上の「空・縁起・二諦・中道」と数学構造の対応は解釈層であり、Lean4によって宗教哲学上の主張が証明されたわけではない。

## 1．Git正本・統合・認証来歴

- 前段v5.90三段階統合後のbase main：`8717e61db7a251b68dc320b725f24585d5a37d9f`。
- [定理PR #3503](https://github.com/itakura-hidetoshi/KuuOS/pull/3503) **MERGED**。新規`formal/KUOS/Architecture/QiWuxingGK5CHP77SingleUnitLoopThresholdV5_91.lean`1ファイル、GitHub差分**392行追加／既存行削除0**。元17D・18D・19Dの型・比較生成子に変更なし。
- 定理認証source `efc96dfa740775b49fbeff23a1e44e2ba4996733`、定理squash後main `8e6b45d20bd26be68097b17ab9a283dd939c79b7`。source／test-merge／squash Git tree **`d94c661920e09db2dbdfcb9087edda135d5741d1`一致**。
- [定理CI #42903132323](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42903132323) **terminal SUCCESS**。Scoped Strict Lean **9,143／9,143**、Governance・独立Kuu Core・workflow integrity SUCCESS。
- [公開import PR #3504](https://github.com/itakura-hidetoshi/KuuOS/pull/3504) **MERGED**。`formal/KuuOSFormal.lean`へ1行import追記のみ。認証source `6b0837c7cece470e631d9cfbd5b320ccba3f23b8`、squash後main `fe04f460fde4334334e439c2dda99c85d7cf0154`。source／test-merge／squash Git tree **`0876f06e669b8044b8df0897edd64452f88e0f6c`一致**。
- [公開CI #42904008712](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42904008712) **terminal SUCCESS**。公開`KuuOSFormal` Strict Lean依存閉包 **10,404件**、Governance30/30ジョブSUCCESS。
- 定理・公開のそれぞれの実`#print axioms`出力は**18/18**。公理不要**6件**、残り**12件**は標準`propext`・`Quot.sound`のみ。新規`sorryAx`なし、変更Lean error／warning 0／0。
- 固定環境：Lean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**、公開root107維持。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。

## 2．元依存型の単一unit証拠はraw閉路になれない

真正旧18D型
`M : SelectedLocalEighteen W l r J N`
の5つの**元の**構成子に対して、v5.89の`selectedV589OriginalUnitCount l r M`を直接適用する。

中核の`selectedV591OneUnitEndpointsDistinct`は

```text
OriginalUnitCount(M) = 1  ->  J ≠ N
```

を型付き帰納法で証明した。各分岐の根拠：

- `strict`：unitCountは0であるため1という前提に矛盾。
- 真正`unitLeft`／`unitRight`：元v5.35で証明済みの**生17D端点非等号** `selectedSeventeenUnitLeft_rawDistinct`／`selectedSeventeenUnitRight_rawDistinct`を直接使用。
- `reverse`：unitCountを保存し、元の真の始終端を反転する。
- `chain A B`：unitCount(A)+unitCount(B)=1なので、片方がzero-unit、もう片方がone-unit。zero-unit脚はv5.89の`selectedV589OriginalFree_exhausted`により**元のraw17D端点が実際に等しい**。この端点等号を接続し、one-unit脚の帰納法の非等号から合成の始終端非等号を得る。

ここでは商クラス等号で生端点を置き換えず、未認証の異fiber gluingを行っていない。

## 3．全真正N→N閉路のunit数ギャップ

元の任意の真正raw17D端点`N`と元旧18D型の閉路`M : SelectedLocalEighteen W l r N N`について、

```text
OriginalUnitCount(M) = 0
  or
2 ≤ OriginalUnitCount(M)
```

を`selectedV591LoopZeroOrAtLeastTwo`で証明した。`selectedV591LoopUnitCount_ne_one`はcount=1から`N ≠ N`が生じる矛盾を形式化する。unitCount正の閉路は必ず2以上（`selectedV591LoopPositiveAtLeastTwo`）。

unitCount=0側の全域性は既にv5.89が証明済みであり、v5.88の忠実な埋込像に一致する。unitCount=2側の全raw証拠が同じ指紋になるとは主張しない。

## 4．下界が鋭いことを示す真正2-unit往復閉路

任意の**本当に供給された**元証拠`A : SelectedLocalEighteen W l r J N`から、元の`chain`／`reverse`だけで

```text
Forward(A)  = chain A (reverse A) : J -> J
Backward(A) = chain (reverse A) A : N -> N
```

を構成した。両者は元の型であり、独立した新しい閉路代理Typeではない。`selectedV591ForwardRoundTrip_unitCount`／`BackwardRoundTrip_unitCount`はどちらもunit数が`2 * OriginalUnitCount(A)`であることを証明。

さらに`selectedV591ForwardRoundTrip_bracket`／`BackwardRoundTrip_bracket`は、元の真正v5.73内部括弧がそれぞれ`joined (bracket A) (reversed (bracket A))`、`joined (reversed (bracket A)) (bracket A)`を保つことを証明。勝手な逆元律・括弧結合律は追加しない。

v5.35の**実際に与えられた**before/F/G/C/after依存データで元の`unitLeft`と`unitRight`を用いる定理`selectedV591ActualLeftUnitTwoRoundTrips`／`selectedV591ActualRightUnitTwoRoundTrips`は、各々の元17D始終端がraw値として異なり、ForwardとBackwardの**それぞれ**がunitCount=2であり、具体的な左右の括弧観測が異なる順序を保つことを検証する。

したがって「unitを含む閉路のunitCountは2以上」という**数値下界は達成可能**である。ただし、二つの往復閉路は一般に**異なるJ→JとN→Nのfiber**に存在する。同じfiberの元証拠対を構成した、あるいは同じ指紋の衝突があるという結果ではない。

## 5．v5.90の同一fiber衝突障害を2原子へ強化

`selectedV591BracketCollision_requiresTwoUnits`は、同一の本当のraw17D N→N fiberにある元証拠M,Lについて

```text
bracket(M) = bracket(L)  and  M ≠ L
  => 2 ≤ OriginalUnitCount(M) and
     2 ≤ OriginalUnitCount(L)
```

を形式証明した。前段v5.90の両側positive証明に、今回認証した「正の閉路unit数は2以上」を厳密に接続する。

別々の元旧5構成子真正selected19商、新7構成子真正selected19商への必要条件（`selectedV591OldClassCollision_requiresTwoUnits`／`NewClassCollision_requiresTwoUnits`）、および**それぞれ真に居住することを仮定した**元の異なる型付き19D比較（`selectedV591OldTypedCollision_requiresTwoUnits`／`NewTypedCollision_requiresTwoUnits`）も独立に検証した。

いずれも「同指紋・異raw対が存在する」ことを主張せず、前件が成立した**場合のみに**2原子必要という条件付き結論を持つ。旧5／新7 Type19の大域同値も主張しない。

## 6．Lean4修正・公理・障害の境界

定理CI #42903132323は**初回sourceのままScoped Strict Lean成功**。新規ファイル全体、元v5.35の依存型生成子・端点非等号、v5.89のzero-unit全域性、v5.90のpositive必要条件と型付き商を照合した。追加された元の仮定・歴史的証明の編集はない。新規18件公理監査は両独立CIで一致。

**NO_DATA**：unitを含む同一真正raw17D exact fiber内の同指紋・異raw旧18D対の実在、count≥2の十分性、元unitパラメータの一意性、旧新19D Type全体の同値、異fibertransport、WORLD／20Dの降下、実行・制度的権限。v5.87の異なるraw17D fiberにまたがる衝突を本定理へ移し替えない。

**次段Qi v5.92候補**：本来の`unitLeft`／`unitRight`源を含む**最小2-unit往復閉路**で、元17D端点を保持したまま、内部括弧と実パラメータ履歴の一致・不一致を比較する。必要なら供給された真正同型fiberの入力条件を別途明記し、局所compatibilityを証明した場合にだけ衝突構成を主張する。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
