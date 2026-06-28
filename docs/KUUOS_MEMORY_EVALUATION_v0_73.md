# KuuOS Memory Evaluation v0.73

## 目的

v0.73は、v0.72の非マルコフMemoryOS接続について、有限個の変形候補を同一条件で評価し、決定的に一件を選択します。

候補生成、候補検証、候補評価、選択証拠を分離します。

## 有限memory family

有限familyは、source memory kernel digestへ束縛された候補集合です。

```text
F = {delta K_1, delta K_2, ..., delta K_n}
```

family内のmember IDは一意でなければなりません。

全memberは同じsource kernel digestへ束縛されなければなりません。
