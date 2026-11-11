# Qi v5.95 — 真正旧18Dのstrict配置による同指紋衝突の等号反映と添字剛性（Lean4形式認証）

2026年11月11日 JST。canonical正本：\`itakura-hidetoshi/KuuOS\` の \`main\`。対象は元の真正依存型 \`SelectedLocalEighteen W l r J N\`、元raw17D始終端 \`J,N\`、元v5.73非結合内部括弧、v5.89真正unit数、v5.92型付きunit葉全payload履歴、v5.93未解決同指紋衝突命題、v5.94真正strict前置／後置族である。哲学的な「空・縁起・二諦・中道」と形式定理の対応づけは解釈・命名層であり、Lean4が哲学概念自体を証明したわけではない。

## 1．GitHub正本・認証来歴

- 基準main（Qi v5.94三段階統合済み）：\`c927ce23bae7744bb1484faded62f29f1abb7834\`。
- [定理PR #3515](https://github.com/itakura-hidetoshi/KuuOS/pull/3515) **MERGED**。新規Lean4 1ファイル \`formal/KUOS/Architecture/QiWuxingGK5CHP77OriginalStrictPaddingCollisionReflectionV5_95.lean\` 449行追加・既存行削除0。実際の\`#print axioms\`17件。定理source \`ec45ba2d93d1006c9d6520463d67a906f4f97dfc\`、統合main \`691c9291e7cd92346ed1b9054c74a232a2948aa1\`。source／test-merge／squash後main Git treeは **\`8775a5cecff4d3ed3fa8c215fae3949c7798b30c\`一致**。
- [定理exact-source CI #42927426079](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42927426079) **completed／SUCCESS**。Scoped Strict Lean **9,147／9,147**、Governance・独立Kuu Core・整合性SUCCESS。新規17宣言の実ログによる公理監査 **17／17**：公理不要**11宣言**、\`propext\`のみ**2宣言**、\`propext\`／\`Quot.sound\`のみ**4宣言**。新規\`sorryAx\`なし、変更Leanファイルのerror/warning **0／0**。
- [公開import PR #3516](https://github.com/itakura-hidetoshi/KuuOS/pull/3516) **MERGED**。\`formal/KuuOSFormal.lean\`に新規import **1行のみ**追加。公開source \`2d64a25bdbcd4b68eac0765dd8d478e208e31485\`、統合main \`019abaeb870aa276c9b92429421e03b92efbd657\`。source／test-merge／squash後main Git tree **\`b595053cdf3220cfaf6b9fa3b2ca002299d9a66e\`一致**。
- [公開CI #42928104671](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42928104671) **completed／SUCCESS**。公開\`KuuOSFormal\`依存閉包 **10,408／10,408**、Governance **30／30ジョブSUCCESS**。独立Lean実ログで公理監査17／17、新規\`sorryAx\`なし、変更Lean error/warningなし。
- 固定Lean **v4.30.0-rc2**、mathlib **\`5450b53e5ddc75d46418fabb605edbf36bd0beb6\`**、公開root107、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) **Draft／OPEN／未マージ**。既存元17D／18D／19D Type、定理、元旧5／新7比較構成子を変更しない。

## 2．固定した真正J→N fiberでの等号反映

任意の同一真正元raw17D添字をもつ \`M,L : SelectedLocalEighteen W l r J N\` と任意の \`n : Nat\` に対し、元のstrictとchainだけからなるv5.94の \`Prefix(n,-)\`／\`Suffix(n,-)\` を使う。

\`\`\`text
Prefix(n,M)=Prefix(n,L) ↔ M=L
Suffix(n,M)=Suffix(n,L) ↔ M=L

Bracket(Prefix(n,M))=Bracket(Prefix(n,L))
  ↔ Bracket(M)=Bracket(L)
Bracket(Suffix(n,M))=Bracket(Suffix(n,L))
  ↔ Bracket(M)=Bracket(L)
\`\`\`

これらは元旧18D真正raw証拠値の等号と、元v5.73自由非結合括弧の等号を**それぞれ独立に**反映する。証明は元の \`chain\` 構成子と括弧木 \`oldJoined\` の引数に対する帰納的な\`injection\`を用いる。したがって両方を合わせた条件は、前置・後置いずれについても、

\`\`\`text
Bracket(Padding(n,M))=Bracket(Padding(n,L))
  ∧ Padding(n,M)≠Padding(n,L)
↔ Bracket(M)=Bracket(L) ∧ M≠L
\`\`\`

となる。これは**衝突条件の同値な移送**であり、どちらか一方の衝突の実在を無条件に認めるものではない。

## 3．独立したpadding長の履歴一致とstrict原子数障害

本当の型付きunit葉payload履歴は \`Prefix(m,M)\` と \`Prefix(n,L)\` の比較、\`Suffix(m,M)\` と \`Suffix(n,L)\` の比較、さらに前置／後置を混在させた比較について、任意の \`m,n\` で、

\`\`\`text
History(Padding(m,M))=History(Padding(n,L))
  ↔ History(M)=History(L)
\`\`\`

となる。元の \`before/F/G/C/after\` と各unit葉の真の始終端添字は観測から削除しない。ただしstrictの数・括弧の位置はこの履歴だけでは復元できない。

新しい\`selectedV595Prefix_crossIndex_strictBalance\`とSuffix版は、**もし**異なる長さの結果の元内部括弧が一致したなら、

\`\`\`text
m + StrictCount(Bracket(M)) =
n + StrictCount(Bracket(L))
\`\`\`

が必ず成り立つと示す。これは必要条件であり十分条件ではない。

さらに元sourceの \`StrictCount(Bracket(M))=StrictCount(Bracket(L))\` という条件が本当に満たされる場合、前置／後置について次が成り立つ。

\`\`\`text
Bracket(Padding(m,M))=Bracket(Padding(n,L))
  ↔ (m=n ∧ Bracket(M)=Bracket(L))
\`\`\`

元のstrict数一致を仮定しないまま、この剛性を全域の定理へ一般化しない。

## 4．v5.93の1-unit元源衝突命題への厳密な還元

v5.93の \`selectedV593OneUnitSourceCollisionExists l r J N\` は、同じ真正元依存型 \`J→N\` 内に **UnitCount(M)=1・Bracket(M)=Bracket(L)・M≠L** の証拠対が存在するという\`Prop\`であり、証拠対の実際の構成ではない。

v5.95では固定 \`n\` を用いた制限付き\`PrefixOneUnitCollisionExists\`／\`SuffixOneUnitCollisionExists\`を定義し、これらと元v5.93の存在\`Prop\`が**必要十分**であることを証明した。したがって既存のstrict配置だけでv5.93の未解決の存在命題を解消したとはいえず、存在の証明も不可能性の証明も追加していない。

## 5．認証の限界／次段Qi v5.96

**認証済み**：指定された元依存型同一fiber上の固定n strict配置に関する元raw等号反映・元括弧等号反映・同指紋衝突の必要十分条件、任意長での型付きunit履歴一致条件、異なる長さでのstrict数つり合いという必要条件、元strict数一致を条件とした添字剛性、v5.93元1-unit存在Propとの同値還元。

**NO_DATA**：実際に元旧18Dの同一 \`J→N\` fiber内に、同じv5.73内部括弧指紋を持つ**異なる**1-unit raw証拠対が存在するか／不可能か。v5.91のloop unit数≥2の必要下界を十分条件にしない。v5.94の**履歴一致・括弧不一致**の証拠を**括弧一致・raw不一致**に読み替えない。元19D旧5／新7の全域比較同値、異fiber貼合、WORLD／20D降下、制度的行為権限も未認証。

**v5.96研究方向**：元の真正\`unitLeft\`／\`unitRight\`の付加パラメータ、依存型端点と同一括弧木の内部unit位置を合わせ、元1-unit同指紋衝突の存在／不可能性の局所的な判定条件をさらに絞る。未構成の証拠対を仮定なしに発生させない。

append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
