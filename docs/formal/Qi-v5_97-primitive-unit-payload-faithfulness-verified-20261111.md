# Qi v5.97 — 真正旧18Dの単独unit葉における元依存型payload履歴の忠実性（Lean4形式認証）

2026年11月11日 JST。唯一のcanonical正本は `itakura-hidetoshi/KuuOS` の `main`。形式的な対象は**既存の真正依存型** `SelectedLocalEighteen W l r J N`、元v5.73非結合括弧観測、v5.89元unit数、v5.92完全な型付きSigma unit葉payload履歴、v5.94–v5.96真正strict配置・衝突条件である。空・縁起・二諦・中道との対応づけは命名・解釈層であって、形式定理が思想的概念そのものを証明したわけではない。

## 1．GitHub正本とLean4検証来歴

- 基準main（Qi v5.96の三段階統合完了）：`e988b5c24aa18b8c53545f1d97a28079929a22eb`。
- [新規Lean4定理PR #3521](https://github.com/itakura-hidetoshi/KuuOS/pull/3521) **MERGED**。新規ファイル `formal/KUOS/Architecture/QiWuxingGK5CHP77PrimitiveUnitPayloadFaithfulnessV5_97.lean` のみ、GitHub差分**374行追加／既存行削除0**、実`#print axioms` **15件**。元17D/18D/19D Type・旧5／新7比較を変更せず、新たな大域等号や比較構成子を加えない。
- 定理の最終source HEAD `8054d3772df55397d1ed903fe6c2397c9f66644d`。[修正後exact-source CI #42965793931](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42965793931) **completed／SUCCESS**、Scoped Strict Lean **9,149／9,149**、Governance／独立Kuu Core／workflow整合性SUCCESS。
- 定理squash後main `99db06b2b8d8445781a2afb1be23e0f36b5e8f58`。認証source／test-merge／squash後main Git tree **`6ad999e4de2e013c9419255e496292716bd063e9`一致**。
- [公開import PR #3524](https://github.com/itakura-hidetoshi/KuuOS/pull/3524) **MERGED**。`formal/KuuOSFormal.lean`に **1行のみ**新importを追加。公開source `ae43b8a0f8e7211182cbfde4994117ab0ff35c65`。[公開CI #42966346026](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42966346026) **completed／SUCCESS**：公開 `KuuOSFormal` のStrict Lean依存閉包 **10,410／10,410**、Governance **30／30 SUCCESS**、独立Core SUCCESS。
- 公開squash後main `14b6a02c56ada60297af69d054a93df56ebee8c2`。公開source／test-merge／squash後main Git tree **`f054d6a4678026b29d1c2c6e1842e11fbc297a49`一致**。
- 定理・公開の両独立実ログの公理監査 **15／15**：**公理不要4宣言**、**`propext`のみ10宣言**、**`propext`／`Quot.sound`のみ1宣言**。新規`sorryAx` **なし**、変更Lean warning／error **0／0**。
- Lean **v4.30.0-rc2**、mathlib **`5450b53e5ddc75d46418fabb605edbf36bd0beb6`**、公開root **107維持**。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) はDraft／OPEN／未マージのまま。append-only／tighten-only／overwrite-forbidden／same-root。

## 2．本当の原始unit葉と条件を限定した理由

v5.97は既存の元依存型`SelectedLocalEighteen`の値について、元v5.73の内部括弧が**厳密に`oldUnitLeft`または`oldUnitRight`**であるという`selectedV597OriginalPrimitiveUnit`を定義した。これは元unitLeft／unitRight生成子単独の条件であり、元のreverseや非結合chainを外側に持つ1-unit証拠は含まない。新しい18D生成子や全域商は導入しない。

この条件が満たされる本当の元証拠`M:J→N`は、真正元unit数が厳密に1であり、元v5.92の完全型付き履歴が

```text
History(M) = [⟨J, ⟨N, M⟩⟩]
```

と**その証拠自身を含む**ことをLean4で証明。ここで元の`before/F/G/C/after`は単なるタグに置換されず、Sigmaの最内層に格納された元の実証拠値の一部として保存される。型付きの真のraw17D始終端`J,N`を勝手に識別・移送しない。

## 3．二重Sigmaの等号反映と局所忠実性

同じ本当の`J→N`依存型を固定したうえで、

```text
M : SelectedLocalEighteen W l r J N
Atom(M) := ⟨J, ⟨N, M⟩⟩
```

とすると、`Atom`の単射性を本当の二重Sigma構成子の等号から証明。Lean4では外側`Sigma.mk.inj_iff`による依存等号`HEq`を同一型へ戻し、内側Sigmaについて再び同様に元の真正旧18D証拠等号を回収した。

その結果、`M,L`がともに単独unit葉で**同じ真正J→N fiber**に属する場合、

```text
History(M) = History(L) ↔ M = L
(Bracket(M) = Bracket(L) ∧ History(M) = History(L))
  ↔ M = L
```

を形式証明した。さらに`M ≠ L`なら元の完全型付き履歴も異なる。**これはprimitive単独unit葉に限った忠実性**であり、すべての一個unitの元証拠へ無条件に拡張していない。

## 4．strict配置族への条件付き移送

真正元のstrict前置`Prefix(m,M)`・後置`Suffix(n,L)`では、任意のm,nでも元v5.92の完全型付きunit履歴は保存される。v5.95の履歴等号反映を既証明のprimitive局所忠実性につなぎ、

```text
History(Prefix(m,M)) = History(Prefix(n,L)) ↔ M = L
History(Suffix(m,M)) = History(Suffix(n,L)) ↔ M = L
History(Prefix(m,M)) = History(Suffix(n,L)) ↔ M = L
```

を証明。これは**元のsourceのraw等号**を復元するのであって、異なるstrict追加数・配置の**padding後raw証拠の等号**を推論するものではない。同じnで同方向のpaddingを用いた場合に限り、元等号からpadding後raw等号が成立することを別途確認した。

元の内部括弧まで一致し、かつ元primitive型付き履歴が一致している場合には、v5.96の正unit数・mixed orientationの定理を使い、padding後の括弧一致と異raw値が同時成立しないことを形式証明した。

## 5．限定された不存在命題とNO_DATA

新しい存在`Prop`は**双方がprimitive unit単独葉**であること、**元の完全型付き履歴が一致する**こと、元内部括弧も一致すること、かつ元raw値が異なることを要求する。

この指定された限定`Prop`は**不可能と形式証明された**。ただしv5.93の`selectedV593OneUnitSourceCollisionExists`は単独葉や履歴一致を仮定しない。元のreverse／chainでunit葉が包まれる場合、またはtyped payload履歴が異なる場合の同指紋・異raw元源の存在・不可能性は引き続き **NO_DATA** である。primitive局所結果を元依存型全域へ昇格させず、異fiber gluing、旧新19D商全域同値、WORLD／20D降下・権限も未認証。

## 6．Lean4失敗の構造的理由と修正

- [初回CI #42964616845](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42964616845) FAILURE：二重Sigma単射の`sigma_mk_injective`に暗黙の端点引数を明示して型不一致2件。primitive葉以外の元構成子に対する大域的`simp`で、深い依存型正規化の`whnf`がタイムアウト3件。
- [第2回CI #42965203188](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42965203188) FAILURE：暗黙引数を省いた`sigma_mk_injective`でもSigmaの型族が異なる形に推論され、残り1件の型不一致。leaf以外の`change`／構成子`cases`による局所的no-confusionはこの時点でSUCCESS。
- [最終CI #42965793931](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42965793931) SUCCESS：外・内の二重`Sigma.mk.inj_iff`から`HEq`を得て`eq_of_heq`する、明示型付き証明へ修正。**新規Leanファイルの証明手順だけ**修正し、元17D／18D／19D Type、すべての新定理文、元unit payload定義、比較規則、Lean/mathlib固定を変更せず、公理追加・sorryによる回避もなし。失敗CIの公理出力は認証根拠としない。

## 7．次段Qi v5.98候補

厳密に限定したprimitive unit葉の局所忠実性から出発し、元の`reverse`・`chain`で構成する1-unit断片で、元の型付きpayload履歴と内部括弧指紋から元raw証拠を復元するための**依存型中間端点に関する補助条件**を明示する。条件が成立しない枝はobstructionとして残す。元v5.93の無条件同指紋・異raw source存在または全域不可能性を証明したと主張しない。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
