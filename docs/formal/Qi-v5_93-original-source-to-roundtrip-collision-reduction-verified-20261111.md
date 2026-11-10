# Qi v5.93 — 真正元旧18Dの1-unit源衝突と2-unit双方向閉路衝突の同値条件（Lean4形式証明）

2026年11月11日 JST。canonical正本：`itakura-hidetoshi/KuuOS`／`main`。本記録が対象とするのは、元の依存型`SelectedLocalEighteen W l r J N`、真正raw17Dの添字`J,N`、v5.73非結合的内部括弧観測、v5.89元unit数、v5.91往復閉路、およびv5.92元パラメータ履歴である。「空・縁起・二諦・中道」との対応は解釈・命名の層であり、Lean4の定理が仏教哲学の全域的真理を機械証明したという意味ではない。

## 1．GitHub正本と認証来歴

- Qi v5.92三段階統合後の基準main `68ede48e6227154b05a83118e82a0fa1e76a0d0b`。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージ。
- [Lean4定理PR #3509](https://github.com/itakura-hidetoshi/KuuOS/pull/3509) **MERGED**。新規`formal/KUOS/Architecture/QiWuxingGK5CHP77OriginalRoundTripCollisionReductionV5_93.lean`1ファイル、GitHub差分386行追加／既存行削除0、実際の`#print axioms`16件。
- 最終定理認証source `9282dd1e2575a9d0d81b1d211144f96475604aa9`、定理squash後main `fa897f7c077b680004a1df2f4672e82f84d5d39f`。認証source／test-merge／squash後main Git tree `79a2a63f3d9c00f45cd4e129efa43ee5fba6aab4`一致。
- [修正後定理CI #42914930248](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42914930248) **completed／SUCCESS**。Scoped Strict Lean **9,145／9,145**、選択Governance・独立Kuu Core・workflow integrity成功。
- [公開import PR #3510](https://github.com/itakura-hidetoshi/KuuOS/pull/3510) **MERGED**。`formal/KuuOSFormal.lean`へ新規import1行のみ追加。公開source `bfd8dba4ec24a3f925ce3c1ad069d652e7e2f202`、squash後main `65fcdbb38230f792051524e4e1b7dc83f895f75f`。source／test-merge／squash Git tree `1431a8fcdd06b0e2ad4c106e7a580385491efa0a`一致。
- [公開CI #42915783805](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42915783805) **completed／SUCCESS**。公開`KuuOSFormal`のStrict Lean依存閉包 **10,406／10,406**、Governance30/30 SUCCESS。独立した両ログで新規公理監査16/16：**公理不要13**、残り**3は標準`propext`・`Quot.sound`のみ**。新規`sorryAx`なし、対象Lean error/warning 0/0。
- 固定Lean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**、公開root107を維持。元の17D／18D／19Dの型と比較規則は無改変。

## 2．真正18Dの前後往復閉路が元raw等号を反映

元の**同一の依存型**に本当に属する証拠`M,L : SelectedLocalEighteen W l r J N`に対して、元の5構成子のうち`chain`と`reverse`のみを用い、

```text
F(M) := chain M (reverse M) : J→J
B(M) := chain (reverse M) M : N→N
```

を考える。v5.93は`selectedV593ForwardRoundTrip_rawEq_iff`と`...Backward...rawEq_iff`で、

```text
F(M) = F(L)  ↔  M = L
B(M) = B(L)  ↔  M = L
```

を**元の真正old18D Type値の等号**として証明。証明は、固定添字上で元の`chain`構成子の引数に対する`injection`を使用する。`reverse`が逆元律を満たすことは仮定していない。

## 3．元v5.73内部括弧指紋の等号も反映

元観測`Bracket(M)=selectedLocalEighteenInnerBracket l r M`を用いると、

```text
Bracket(F(M)) = joined (Bracket(M)) (reversed (Bracket(M)))
Bracket(B(M)) = joined (reversed (Bracket(M))) (Bracket(M))
```

が定義から従う。元の非結合構文木`oldJoined`の`injection`／`congrArg`を使い、

```text
Bracket(F(M)) = Bracket(F(L)) ↔ Bracket(M) = Bracket(L)
Bracket(B(M)) = Bracket(B(L)) ↔ Bracket(M) = Bracket(L)
```

を各方向で独立に形式証明。これは**raw証拠が等しい**という無条件の主張ではなく、観測等号の反映に関する定理である。

従って、前方向／後方向のそれぞれで「**同じ内部括弧指紋かつ異なるraw証拠**」という条件は、元の同じ`J→N`fiberでの対応するsource条件と**必要十分**になる（`selectedV593ForwardRoundTrip_collision_iff`／`Backward...`）。

## 4．1-unitの元源が本当に衝突した場合に限る2-unit衝突構成

本当に元の同じ`J→N`依存型にいる`M,L`について、

```text
OriginalUnitCount(M) = 1
Bracket(M) = Bracket(L)
M ≠ L
```

を**前提として与えた場合に限り**、v5.90のcount一致で`OriginalUnitCount(L)=1`、v5.91で真正`J≠N`が得られる。そのうえで認証済み`selectedV593OneUnitSourceAmbiguity_givesDualTwoUnitCollisions`は、`F(M),F(L):J→J`と`B(M),B(L):N→N`のそれぞれについて

```text
Bracket(F(M)) = Bracket(F(L))   and   F(M) ≠ F(L)
Bracket(B(M)) = Bracket(B(L))   and   B(M) ≠ B(L)
all four roundtrips have actual original UnitCount = 2
```

を構成する。**前後2つのfiberはJ≠Nにより異なる**。各々の内部で有効な等号を維持し、両fiber間の元証拠等号や19D比較を捏造しない。

`selectedV593OneUnitSourceCollisionExists`は元の証拠対の**存在を表すPropであり、存在証明ではない**。`selectedV593ForwardTwoUnitCollisionExists`／`BackwardTwoUnitCollisionExists`も元の1-unit証拠から作る往復閉路**像の中だけ**を量化する。それらの存在の同値と前後相互の同値をLean4で証明したが、どの存在Propにも無条件のinhabitantは構成していない。

## 5．Lean4初回失敗・修正の構造理由

初回source `62fbb2d4f02bf5e936b453af7c473b5e20966779`の[CI #42914363288](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42914363288)は新規ファイルの**8件**のLeanエラーでFAILURE。変更Lean全文、元v5.35の5構成子と依存型index、v5.73非結合括弧観測、v5.89 count、v5.90・v5.91・v5.92補題、固定Lean環境とともに照合した。

主因は、元`chain`／`oldJoined`構成子の`injection`がすでに等号目標を解消しているのに余分な`exact`を続けたこと（4件）、まだ定義を展開していない`Bracket(Forward/Backward(...))`に直接`rw`を当てたこと（2件）、数値計算済みのゴールへ余分な`norm_num`を続けたこと（2件）。

修正版では、過剰な行のみ削除し、元の非結合構文木の具体形を`change`で固定して`congrArg`を適用。元の定理文、対象範囲、物理・数学的仮定、元17D／18D／19D定義、Lean/mathlib固定値は一切変更せず、修正後CIで16宣言すべて形式認証された。これは`sorry`・追加公理・比較規則の弱化による修正ではない。

## 6．残余障害と次段Qi v5.94

**形式認証済み**：元raw17D添字を保存する前後往復閉路の元raw等号反映／v5.73指紋等号反映、同指紋・異raw条件の元源への同値還元、元unit数1の**条件付き**双方向2-unit閉路衝突構成、およびrestricted roundtrip-imageでの存在Propの同値。

**NO_DATA**：同一真正raw17D `J→N`fiberの元unitCount=1証拠に同じ内部括弧指紋・異rawの対が本当に存在するか。その存在も不可能性も未認証。従って、同一真正`J→J`／`N→N`fiberの同指紋衝突が無条件で存在すること、2-unit数値下界が十分であること、sourceパラメータ履歴の復元可能性、元旧5／新7選択19D Type間の大域同値、異fiber gluing、WORLD／20D降下・制度的行為権限は依然として未認証。v5.92の**履歴一致・括弧不一致**の実例を本来の**括弧一致・raw不一致**の証明に転用しない。

**次段Qi v5.94候補**：元unitCount=1証拠の`unitLeft`／`unitRight`の**真正before/F/G/C/afterと型付き端点履歴**を、同一括弧指紋の固定構文木の下で比較し、元源の衝突が内部unit葉のパラメータ曖昧性に還元できる条件を検証する。実際の元パラメータ差の存在はNO_DATA保持。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
