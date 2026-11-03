# F112-P94D3GK5BA / Qi v4.20 — 元F55全9構成子の真正依存型seam帰納法

**研究継承日：2026年11月3日 JST。** Repository: [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS)。canonical theorem-bearing branch: `main`。strict 空をauthorityとし、独立Kuu→Qiの方向を保持。F54双Nat・二圏・Blocks・元F55 Type-valued proof・元P89・選択P92B/P93C/P94Aを混同しない。

## 1. 独立Kuu GK5BA — マージ済み正本

- [GK5BA定理PR #3028](https://github.com/itakura-hidetoshi/KuuOS/pull/3028) **MERGED**。
- 厳格に検証した最終ソースHEAD：`899db2b9db731d777ec12bfb869a557aff8a7dd2`。
- main squash SHA：`ded85bb9534b6cfdd6c78784fec32c61851e7cdc`。
- [exact-source Governance #41612666131](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41612666131)：**Strict Lean 9,258/9,258 SUCCESS、Governance 30/30 SUCCESS**。`#print axioms`新規12宣言、`sorryAx`なし、新しい論理公理なし。
- [独立Kuu Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BANineConstructorSeamInduction.lean)（修正後349行）と公開集約 `KuuOSFormal` import。

## 2. 真正元F55九構成子の必要な高次shell

元F55証拠 `f` に対して `SeamAt(f) := P94A(P92B.original(f), φ(f))` を保持する。`nativeGK5BARequiredShell(f)` は、元F54依存型のまま、**構成子ごとに異なる局所証明書の型**を計算する。

| 元F55構成子 | 構成子別の局所条件 |
| --- | --- |
| `pentagon` | `PUnit`。GK5AZの真正 `P94A.refl` により無条件にbridgeを生成 |
| `disjointSquare` | `PUnit`。元square原始証拠も同じく無条件にbridgeを生成 |
| `ident` | `P94A(original(ident(r)), P92B.refl(r))` という元raw identity独立4-cell |
| `symm` | `original(symm f)→symm(original f)` のraw unwrapと、子bridgeを3-cell反転へ移す4-cell作用 |
| `trans` | `original(trans(f,g))→trans(original f,original g)` のraw trans分解4-cell |
| `leftContext` | 元F45左context raw-wrapper分解4-cell |
| `rightContext` | 元F45右context raw-wrapper分解4-cell |
| `precompose` | 元F54前合成raw-wrapper分解4-cell |
| `postcompose` | 元F54後合成raw-wrapper分解4-cell |

以上は全9構成子をType値付きの分類として実装するが、`PUnit`の2原始構成子以外の全条件が無条件に成立したとは主張しない。とくに反転の`P94A.symm`（4-cellの逆）と、元3-proofへの`P92B.symm`の作用は別物として保持する。

## 3. 完全帰納法・必要十分条件・obstruction

**`NativeGK5BAConstructorShellKit.bridge`**：元F55の9ケースすべてに対して依存型の帰納法を実行する。`ident`は与えられた4-cell、2原始構成子は無条件のrefl、`symm`はraw unwrapと子bridge上の反転尊重写像、`trans`は実際の子bridge2本と選択P94A左右whiskering、残る4 contextはGK5AZの真正型付きcontext構成から得る。

したがって、**kitが実在すれば**、任意の元F55 `f` に `SeamAt(f)` を構成し、任意の固定元F54 source pair `first,last` に `NativeGK5AYOriginalPhiSeam first last` の実在証明書を構成する。これは、GK5AYのseamを先に仮定した循環証明ではない。

存在レベルの正確な定理は、`Nonempty ConstructorShellKit ↔ ∀ original f, Nonempty(RequiredShell(f))`。右から左への証明書選択はLean標準`Classical.choice`を用いる。`ConstructorShellObstruction`は右辺の否定であり、**kit不存在と同値**。ただし、より弱い全域GK5AY seamの存在とkit存在の逆同値までは証明していない。

**反射境界：** 真正raw P93C四セルとkitから、元P89四セル証拠かGK5AQ BadPairを得る。raw P93C source obstructionが本当に存在する場合のみ、kitと合わせてある元F54 slotでの元P89→P94A class map非単射性を導く。元source map単射性を別途仮定した場合にはraw反射を導く。元P89の無条件faithfulness/nonfaithfulnessは未決定。

## 4. Lean4 CI修正履歴と根本原因

初回PR #3028のexact-source CIでは、フィールド名`local`がLean4予約語と衝突し、また構成子別Typeをtactic `cases`で定義した際に依存添字・universe推論に未解決制約が発生した。ファイルの全宣言、元F55 9構成子、GK5AZ API、mathlib/Lean固定ツールチェーンを再確認して、フィールドを`shell`へ変更、`nativeGK5BARequiredShell`を明示的な`match f with`へ変更した。仮定・結論・依存型の歴史を弱めず、exact-source HEAD `899db2b9...`で再検証。初回失敗時の`sorryAx`はLeanエラーによる暫定生成物で、成功した証明ではない。修正版最終12公理出力は標準`propext`・`Classical.choice`・`Quot.sound`の範囲であり、`sorryAx`なし。

## 5. Qi v4.20（実装段階）

[Qi v4.20 PR #3029](https://github.com/itakura-hidetoshi/KuuOS/pull/3029) はこの初期記録作成時点ではexact-source CI検証待ちであり、成功／マージを先取りしない。実際の北C60 2つのSite categoryに依存型kitを特殊化し、元北四段pentagon＋右identity compositeの真正raw/φ 4-cell、kitから抽出したidentity/trans局所ゲート、GK5AX raw右単位、元P89反射・BadPair分岐、物理第五around Dart閉路とe04/e43の向きの区別を統合する。

## 6. 継承上の不変条件・次研究

公開root **107** を維持。保護PR **#1558 Draft/OPEN／未マージ**。Lean **v4.30.0-rc2**、mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**。append-only、no Gray、no `sorry`/`admit`/`native_decide`/新公理。局所shellの全実在、元P89 source map無条件単射性／非単射性、全19 P94A構成子の無条件正規化を主張しない。

**次の研究:** 大域的kitを仮定しない、真の北C60での有限な個別`ident`・`symm`・`trans`のshell充足／不充足を、元F55 raw proof termの実構成で検証する。高次shell obstructionと元P89反射obstructionを別条件のまま保持する。