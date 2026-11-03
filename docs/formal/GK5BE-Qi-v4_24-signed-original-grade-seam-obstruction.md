# F112-P94D3GK5BE／Qi v4.24 — 符号付きoriginal-wrapper不変量と局所seamの逆向き障害

**正式証明記録：2026年11月3日 JST。** Canonical repository: [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS)。唯一のtheorem-bearing branch `main`、strict 空 authority／独立Kuu→Qi／元F54双Nat・二圏・Blocks・Type値証拠履歴保存／公開root107。

## 1. 独立Kuu GK5BE — wrapper総数の十分性を真正に反証

- [独立GK5BE定理PR #3040](https://github.com/itakura-hidetoshi/KuuOS/pull/3040) **MERGED**。exact-source HEAD `82a010fd889129dc6d884e4763249011c3a7ba47`、main squash SHA `ff3f9af868af46537177e7ced2ec5ff569e34dcf`。source/test-merge/squashのGit treeは `82903e19ebc61f4290b97caa964757905d30b074` で一致。
- [Strict Lean／Governance #41628425569](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41628425569)：**9,266/9,266 SUCCESS、30/30 SUCCESS**。新規16宣言を `#print axioms` 監査し `sorryAx` なし、標準 `propext`・`Classical.choice`・`Quot.sound` 以内。変更Leanソースにerror/warningなし。
- [独立GK5BE Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BESignedOriginalGradeObstruction.lean) を公開`KuuOSFormal`に追加済み。

GK5BBの **unsigned** original-wrapper count `N : P92B → Nat` はP92Bの`symm`で保存される。新しい独立 **signed** original grade `S : P92B → Int` は次を満たす：

```text
S(original f)         = +1
S(assocNaturality ...) =  0
S(refl r)             =  0
S(symm u)             = -S(u)
S(trans u v)          =  S(u) + S(v)
S(context u)          =  S(u)
S(horizontal u v)     =  S(u) + S(v)
```

真正P93C全16構成子・P94A全19構成子について `P94A(u,v) → S(u)=S(v)` を元の依存型帰納法で証明。P93Cの元P89埋め込みを旧proof＝元raw `original` の両端として扱い、P94A追加`horizontalUnit`・`leftContextUnit`・`rightContextUnit`についても保存を個別検証した。

任意の元F55 `f` に対し、局所seam `SeamAt(f) := P94A(original(f), φ(f))` が実在すれば

```text
N(φ(f)) = 1  AND  S(φ(f)) = +1
```

が成立する。逆向きの十分性は一般には主張しない。

真正北C60の元F55 pentagon `p := nativeGK5AGNorthOriginalCell` とその元逆証拠 `symm p` を取る。このとき

```text
N(original(symm p)) = N(φ(symm p)) = 1
S(original(symm p)) = +1
S(φ(symm p)) = -1
¬ Nonempty (SeamAt(symm p))
```

が**無条件**のLean4証明で成立。よってGK5BBの `N=1` 条件が必要でも**十分ではないことを真正源の具体的反例で形式化**した。`nativeGK5BEUnsigned_one_not_sufficient` はこの反例を全称命題の否定として証明。さらにGK5BDの真正有限P77 source語で逆pentagonから到達可能な全証拠もseam不存在と証明した。

## 2. Qi v4.24 — 正のpentagon軌道と負の逆pentagon軌道

- [Qi v4.24定理PR #3041](https://github.com/itakura-hidetoshi/KuuOS/pull/3041) **MERGED**。exact-source HEAD `03c0cf3c521740f079409021a63f60af4f23868f`、main squash SHA `ac37cf01c86db07a58717cf087cea3562b0215a0`。source/test-merge/squash Git treeは `6eb78abccb60dd411fe76d3ffc91d7e00fcd294d` で一致。
- [Strict Lean／Governance #41629270434](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41629270434)：**10,193/10,193 SUCCESS、30/30 SUCCESS**。新規10宣言の`#print axioms`監査に`sorryAx`なし。変更Lean error/warningなし。
- [Qi v4.24 Lean](../../formal/KUOS/Architecture/QiWuxingGK5BENorthSignedSeamObstructionV4_24.lean) を公開`KuuOSFormal`に追加済み。

```text
original pentagon p → trans(p, ident(short)) → trans(trans(p, ident(short)), ident(short))
    ↑ 正の同一P77四セル商クラス

original inverse symm p → trans(symm p, ident(long))
    ↑ 負の同一P77四セル商クラス
```

逆証拠の元F55`rightUnit`を反転した真正P77有限語を構成し、元`symm p`と`trans(symm p, ident(long))`のP77商等号を証明。両者は`N(raw)=N(φ)=1`でも負の局所seamクラスに属する。前方pentagonから二重右単位への類は`SeamExists`正である。

前方・逆のsourceは**異なるF54依存型端点**であり、逆向き二つのクラスを同じHom fiberの等号として扱わない。真正北五行物理Dartの第五閉路・元P89反射BadPairの条件付きiffは独立に維持する。数値の正負はここでは新しいP92B`original`証明の**向き付きカウント**であり、物理五行の陰陽や元F55 pentagon電荷と同一視しない。

## 3. 境界と次段階

成立したのは（1）unsigned `N=1`条件より厳密に強い signed `S=1`必要条件、（2）全P94A構成子での保存、（3）真正北逆pentagonによる十分性の反例、（4）P77同値類の正／負の具体的分離。

以下を依然として**主張しない**：同時`N=1,S=1`からの一般局所seamの十分性、各sourceの全判定、GK5AY全域seam、GK5BA shell kit、元F55 identity単独seam、元P89無条件faithfulness/nonfaithfulness、全P94A正規化、Gray復元、Type値seam証明書のcanonical同一視。GK5AT内部source-image hole、GK5AX元P89 BadPair、GK5BB unsigned・GK5BE signed obstructionは別の条件として保持。

**次の研究 F112-P94D3GK5BF（仮称）**：局所seam必要条件`N(φ f)=1 ∧ S(φ f)=1`の元P77同値類上での安定性と、この条件を満たすが存在性が未決定の証拠クラスを区別する。必要なら符号とoriginの二成分または別のP94A保存不変量を新設し、既存の障害を混同せず可能な条件付きdescentを研究する。

Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107。保護PR [#1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558) Draft／OPEN／未マージ。append-only、元Lean定理上書きなし、no Gray/sorry/admit/native_decide/new axioms。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
