# KuuOS Repository Structure Alignment v0.79

v0.79は、v0.78の観測、診断、有限候補、shadow比較、再観測をrepository構造へ接続します。

入力は明示的な`RepositorySnapshot`です。

`repository_autorepair_contract`を持つmanifestだけを診断対象とします。

診断対象は次です。

- manifest参照path
- 累積runtime rootのvalidator登録
- lakefileのstrict root登録
- aggregate Lean rootのimport登録
- manual workflowの重複PR trigger

候補catalogは次の四種類に限定します。

```text
REGISTER_RUNTIME_VALIDATOR
REGISTER_LAKE_ROOT
REGISTER_AGGREGATE_IMPORT
REMOVE_DUPLICATE_PR_TRIGGER
```

候補はsource snapshot digestと対象fileのbefore digestへ束縛されます。

shadow snapshot上でweighted defect scoreが厳密に減少した候補だけを採用します。

一cycleは一patchだけを返します。

外部承認は要求しません。

自由なコード生成、保護pathの変更、stale patchの適用は行いません。

複数cycleは最大回数を持つ上位runnerから接続します。
