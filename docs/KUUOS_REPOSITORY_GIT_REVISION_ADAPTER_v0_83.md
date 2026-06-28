# KuuOS Repository Git Revision Adapter v0.83

## 目的

v0.83は、v0.82 certificate chainのrevision入力を、ローカルGit object databaseの観測結果へ接続します。

```text
Git parent tree
→ Git current tree
→ 実changed paths
→ explicit inventory snapshot
→ v0.82 certificate record
```

外部承認は要求しません。

## read-only観測

adapterは次のGitコマンドだけを使用します。

- `rev-parse`
- `show`
- `diff`
- `cat-file`

branch、index、working treeを書き換えません。

snapshotの内容はworking treeではなく、指定commitのtree objectから取得します。

未commit変更は観測結果へ入りません。

## 単一親

v0.83のadvanceは、current commitが指定parent commitを唯一の親として持つ場合だけ成立します。

merge commitは拒否します。

複数親の統合certificateは別versionで扱います。

## changed paths

changed pathsは次から取得します。

```text
git diff --no-renames --name-only -z parent current
```

path集合は辞書順、重複なしへ正規化します。

changed pathが明示inventory外にある場合は拒否します。

これにより、観測対象外の変更を無視したcertificate生成を防ぎます。

## snapshot

inventory内の各pathについて、指定commitのblobを`git cat-file`で読みます。

存在しないpathはsnapshotから除外します。

UTF-8でないblobはpath集合へ残しますが、構造textとしては解釈しません。

## v0.82との接続

adapterは次をv0.82へ渡します。

- object databaseから解決したparent SHA
- object databaseから解決したcurrent SHA
- Git diffから取得したchanged paths
- parent tree snapshot
- current tree snapshot

v0.82はさらに、chain ID、直前record digest、直前snapshot、commit replay、chain lengthを検証します。

## 検証

一時Git repositoryを生成し、次を検査します。

- genesis snapshot
- 無関係commitでのscope再利用
- contract固有commitの局所再検証
- dirty working treeの非参照
- inventory外変更の拒否
- 誤ったparentの拒否
- merge commitの拒否
- path削除の観測
- 不正inventory pathの拒否
- 非Git directoryの拒否

## 非主張

v0.83は次を主張しません。

- remote hosting上の履歴完全性
- 署名付きcommitの真正性
- merge commitの統合証明
- Git repositoryへの書込み
- score 0と真理の同一視
