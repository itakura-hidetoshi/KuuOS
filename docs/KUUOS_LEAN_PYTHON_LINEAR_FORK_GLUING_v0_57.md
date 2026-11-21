# KuuOS Lean→Python v0.57 — 一つの追記専用履歴への分岐貼合障害

**開始時のcanonical main:** `824f8185dbd924836059ee204ba88d5a60f83981`（v0.56正式統合）。  
Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`固定。  
append-only／tighten-only／overwrite-forbidden／same-root。

## 問題と結論の範囲

v0.56は、同一の宣言された祖先の後に二つの後続履歴が現れ、
どちらも祖先を厳密に延長するが互いを延長しない場合を
`declaredForkObstruction`と定義した。

**v0.57はこの障害が単なる検出だけでなく、単一List型の線形追記では
本当に貼合できないことをLeanで証明する。**

二つの旧履歴 (B,C) について、次の局所条件を用いる。

```
commonLinearSuccessor(B,C)
 := exists D, (B is exact prefix of D) and (C is exact prefix of D)
```

このとき、同じ単一Listの前置部分二つは必ず比較可能である。
従って両者が比較不能なforkなら共通後続Dは存在しない。

逆に片方がもう片方の前置なら、長い方のList自身が
共通後続として存在する。
そのため**単一Listの宣言上の共通後続の存在と、局所比較可能性は必要十分**になる。

この不可能性は**単一の全順序List・正確な前置延長というモデルの内側**
に限定する。因果グラフ、分岐を明示的に記録する台帳、
より高次の圏・多重歴史模型における再調停の一般的不可能性ではない。
局所モデルでの不可能性を大域世界へ昇格しない。

## 新規Lean（12宣言公理監査）

既存v0.56 `declaredExtension`、`locallyComparable`、
`declaredForkObstruction`、v0.55および原本PlanOS型を変更せず直接import。

- 共通の線形後続が存在するなら二履歴は比較可能
- 比較不能なら共通の線形後続は存在しない
- 宣言されたforkなら共通後続の存在を否定する
- 任意の未来Listが両方を前置として含む可能性を否定する
- 逆に左右どちらかが長いときは共通後続を構成する
- よって存在と比較可能性の**必要十分条件**を証明する
- 片方の選好や局所的な計算結果だけではforkは消えない
- 原本PlanOSは選択・実行権限を与えない

Leanの定理は抽象的なList構造の証明であり、
実際のSQLite二履歴やPython JSON/SHA-256計算がLeanと同一である
という形式的refinementを証明したものではない。

## Pythonでの分離検査

`audit_local_linear_fork_gluing(ancestor_manifest,left_manifest,right_manifest,
separately_supplied_ancestor_checkpoint_sha256=...,
declared_future_manifest=...)`

既存v0.56で三つの分離snapshotを個別に検査し、
局所fork・比較可能な履歴・祖先障害を区別する。

- forkがあれば、この**単一線形前置モデル**での共通後続なしをobstructionで返す
- 比較可能なら、長い方の宣言履歴が前置関係上の候補であると報告する
- 別途未来manifestを提示された場合、既存v0.54で完全性を再計算し、
  左右両方を厳密な順序で前置として含むか検査する
- 古いcheckpoint値の不一致はforkと同時にも保持する
- 元のVerifyOS・PlanOS・SQLiteを検証器自身が再実行しない
- 実際の二つの履歴を照合するが、本当にどの分岐が発行されたかは
  推定しないし、どちらかを真理や実行権限として選択しない

**局所線形に貼合できる**ことは独立保管者による認証、
外部発行者の真正性、共通因果時計を意味しない。

## 独立認証工程

新規6ファイルのみ。元PlanOS・v0.53〜v0.56・公開107 proof roots・
既存Lake/mathlib pinは変更しない。

1. 固定main親v0.56の独立Strict Lean
2. 新規Leanファイル全文を固定環境でwarning/sorry-fatalビルド
3. 新規12宣言の直接`#print axioms`を標準3公理のみ・`sorryAx`なしで監査
4. 新規Python回帰：六つのnative経路、fork非貼合、比較可能な後続、
   実際に妥当な共通後続、過短の未来、不正な未来、古いcheckpointと
   source pin、秘密の非出力・原本OSの非実行
5. GitHub Governanceの全体Strict Lean・累積Runtime・公開API・
   workflow整合性・Exact-head terminal・提出HEAD／テストマージtree一致
6. main統合前の全ゲートSUCCESS、統合後に新main push CIの別途認証

**未認証を認証としない。** PRはDraft・HOLD MERGEで開始する。
全体KuuOSFormalのSUCCESSは限定CIとは独立の証拠とする。
保護PR #1558はDraft／OPEN／未マージを保持する。

原本PlanOSの未出力三Finset、真正な外部発行者、
独立保管されたチェックポイントと因果時刻、別ホストでのreplay、
暗号学的安全性のLean証明、普遍的Lean↔CPython意味保存、
大域的降下、ホスト実行権限は未証明／NO_DATA。

Preference ⇏ Descent ⇏ Authority。
