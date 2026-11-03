# F112-P94D3GK5BD／Qi v4.23 — 真正P77同値類への局所seam存在性の降下

**2026年11月3日 JST 正式証明記録。** Repository: [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS)。唯一のcanonical theorem-bearing branchは `main`。独立Kuu→Qi、strict 空 authority、元F54双Nat／二圏／Blocks／元F55 Type値証明履歴、公開root107を維持。

## 1. 独立Kuu GK5BD — source-typed P77商への真正局所descent

- [独立GK5BD定理PR #3037](https://github.com/itakura-hidetoshi/KuuOS/pull/3037) **MERGED**、exact-source HEAD `6c9bf8a34a5a0bf1641e81b3d7cdb006511ddf31`、main squash `edce91e2f233c2cbaee4a27333c29d6bd94639a3`。
- [exact-source Strict Lean／Governance #41625437344](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41625437344)：**9,264 / 9,264 Strict Lean SUCCESS、30 / 30 Governance SUCCESS**。新規16宣言の`#print axioms`監査に`sorryAx`なし（標準 `propext`・`Classical.choice`・`Quot.sound`以内）。
- [独立Leanソース](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BDP77ClassLocalSeamDescent.lean)（295行、終端改行を含むsplit表示）。
- 検証対象ソースGit treeとmain squash Git treeは**完全一致**：`666dd0aebe5abae4c3da88acc0025d8879bb81d7`。

元F55証拠 `f : PresentedCell p r s` とその元P77四セル `w : NativeF55RawVerticalFourCell first last f g` を使用する。P77はsourceの`refl/symm/trans/leftWhisker/rightWhisker/leftUnit/rightUnit/assoc`をType値で保持し、元F54端点添字を消さない。

`NativeGK5BDP77Word first last seed target` は有限P77証明語で、`toP77` が真正P77四セルを構成する。逆に任意の元P77四セルは1ステップ語になる。この関係は既存 `NativeF55RawVerticalFourClasses` 商の等式と正確に同値：

```text
Nonempty (NativeGK5BDP77Word first last f g)
  ↔ Nonempty (NativeF55RawVerticalFourCell first last f g)
  ↔ (nativeF55RawVerticalFourClass first last f
       = nativeF55RawVerticalFourClass first last g)
```

GK5BCの元P77四セルに沿う局所seam存在の同値 `Nonempty(SeamAt f) ↔ Nonempty(SeamAt g)` を使い、真正 `_root_.Quotient.lift` によって

```text
nativeGK5BDSeamExistsOnP77Class first last r s :
  NativeF55RawVerticalFourClasses first last r s → Prop
```

を構成。任意の元証拠`f`に対して

```text
nativeGK5BDSeamExistsOnP77Class ... (class f)
  ↔ Nonempty (nativeGK5AZSeamAt f)
```

が成立する。これは**局所seamの存在というPropの代表元非依存性**であり、個々のType値seam証明書を商で同一視するものではない。

この局所正領域は元pentagonからの真正P77有限語で到達する全クラスを含み、元identityのP77クラスはGK5BBのoriginal-wrapper数1対0から全域で負。さらに`phi-count ≠ 1`という数的不一致を持つ元証拠からの全P77有限語にもseamが存在しない。

## 2. Qi v4.23 — 真正北C60の具体的な有限P77語

- [Qi v4.23定理PR #3038](https://github.com/itakura-hidetoshi/KuuOS/pull/3038) **MERGED**、exact-source HEAD `630538b2d61878a469f1e5736cdc7f893492a6c9`、main squash `736fa4b50dfeb300f653e6e2c26dc6f5eafa1a32`。
- [exact-source Strict Lean／Governance #41626316363](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41626316363)：**10,191 / 10,191 Strict Lean SUCCESS、30 / 30 Governance SUCCESS**。新規10宣言の`#print axioms`監査に`sorryAx`なし（標準の`propext`・`Classical.choice`・`Quot.sound`以内）。
- [Qi Leanソース](../../formal/KUOS/Architecture/QiWuxingGK5BDNorthP77LocalSeamDescentV4_23.lean)（199行、終端改行を含むsplit表示）。
- Qi exact-source Git treeとmain squash Git treeは**完全一致**：`a89283bceeda0ce0d69e86b3c8cefb62ce26428d`。

真正北C60の元pentagon原始F55証拠`p`、元短F54経路`s`、元F55右単位を使い、

```text
p -- P77.symm(rightUnit p) --> trans(p, ident s)
  -- P77.symm(rightUnit (trans(p, ident s))) -->
        trans(trans(p, ident s), ident s)
```

という**長さ2のType値P77有限証明語**を構成。二重右単位の元F55証拠がpentagon原始証拠と同じ真正P77商クラスにあり、`nativeGK5BDSeamExistsOnP77Class`を満たすことをLean4で証明した。

同じ真正北F54 slotの元identity商クラスはseam不存在、二重右単位元合成には直接seamが存在してもraw trans split shellが存在せず、全域`NativeGK5AYOriginalPhiSeam`は不存在のまま。さらに真正北top-hexagon `disjointSquare` の左元identity合成にも直接seamが存在するが、そのraw split shellは不存在である。

真正北五行物理gaugeの元P89比較反射は、従来のBadPair obstructionの**条件付きiff**としてのみ保存される。source-image hole、original-wrapper count、元P89反射BadPairは互いに異なる障害であり、統合しない。

## 3. 守るべき数学的・運用的境界

成立したのは**source P77同値類上の局所seam存在性**および真正北C60の明示的正負クラスである。以下は**成立を主張しない**：GK5AY全域seam、GK5BA全構成子shell kit、元F55 `ident`単独seam、元P89の無条件faithfulness/nonfaithfulness、全P94A 19構成子の無条件正規化、P77同値類ごとのType値seam証明書のcanonical同一視、Gray復元、他F54文脈への無条件大域descent。

Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。公開rootは107、保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)はDraft／OPEN／未マージ維持。append-only、旧定理の上書きなし、新規公理・sorry・admit・native_decideなし。

**次の研究 F112-P94D3GK5BE（仮称）**：局所正領域のP77飽和と`phi-count = 1`の必要条件の差を比較し、wrapper数が一致してもseam存在が未決定となるクラスを分類する。obstructionを混同せず、source-typed追加不変量の導入を検討する。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
