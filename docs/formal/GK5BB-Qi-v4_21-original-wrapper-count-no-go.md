# F112-P94D3GK5BB / Qi v4.21 — original-wrapper count と真正高次seam不存在

**2026年11月3日 JST。** Canonical repository: [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS)、theorem branch `main`。独立Kuu→Qi／strict 空 authority／append-only／同一公開root107。元F54双Nat・二圏・Blocks・F55 Type証拠と選択P92B/P93C/P94Aおよび元P89を混同しない。

## 1. 独立GK5BB — exact-source検証とマージ済み正本

- [GK5BB定理PR #3031](https://github.com/itakura-hidetoshi/KuuOS/pull/3031) **MERGED**。
- 最終exact-source HEAD：`ff3dff49c64f5d925d95938ea2f49012c5cbb689`。
- Squash/main commit：`baffe9581e569b78aec0bbdc6d82633c084b9546`。
- [Governance #41615936555](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41615936555)：**Strict Lean 9,260/9,260 SUCCESS、Governance 30/30 SUCCESS**。`#print axioms`21宣言、`sorryAx`なし。主にLean標準の`propext`・`Quot.sound`、実際の北C60型の既存の定義から標準`Classical.choice`が現れる場合を区別し、新規論理公理は追加していない。
- [独立Leanファイル](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BBOriginalWrapperCountObstruction.lean)（424行）は公開`KuuOSFormal`へimport済み。

## 2. 新しい数学的不変量 — 元F55 wrapper数

選択P92Bの**真正Type値付き3-cell証拠**`w`に対し、`N(w) := w.gk5bbOriginalCount : Nat`を定義する。単なる物理shadowでも数値等号でもなく、選択三セル証明構文の`original` wrapperの個数を数える。具体的に

```text
N(P92B.original(f))          = 1
N(P92B.refl(route))          = 0
N(P92B.assocNaturality(...)) = 0
N(P92B.symm(w))              = N(w)
N(P92B.trans(u,v))           = N(u) + N(v)
N(P92B.horizontal(u,v))      = N(u) + N(v)
N(P92B.left/rightContext(w)) = N(w)
N(P92B.pre/postcompose(w))   = N(w)
```

**`NativeF55P93AssocFourCell.gk5bbOriginalCount_sound`**では元P89からのraw埋め込みを含むP93C全16構成子の保存を真正帰納法で証明。**`NativeF55P94UnitFourCell.gk5bbOriginalCount_sound`**ではP94A全19構成子の保存を証明し、P94Aが新規に加えた`horizontalUnit`・`leftContextUnit`・`rightContextUnit`の3ケースまで調べる。以前GK5AMの文脈偶奇はP93Cで保存されても追加P94A contextUnitでは破れるが、この自然数wrapper個数は**P94Aでも保存される**。

## 3. 無条件不存在（構成子別）

真の元F54経路`r`の元F55恒等3-cellには`N(original(ident(r)))=1`、選択側`N(refl(r))=0`。P94A四セルが`N`を保存するため、

```text
¬ Nonempty (P94A(original(F55.ident(r)), P92B.refl(r)))
```

を**任意の元F54依存型経路で無条件にLean証明**。さらに元F55合成可能な証拠`f,g`について、

```text
N(original(F55.trans(f,g)))      = 1
N(P92B.trans(original(f), original(g))) = 2
¬ Nonempty (P94A(original(F55.trans(f,g)),
                   P92B.trans(original(f),original(g))))
```

を証明。これはGK5AZ／GK5BAの`ident`および`trans`局所shellが、単に未構成なのではなく**このP94A証明体系の中では不可能**であることを示す。

## 4. GK5AY／GK5BAの全域seamに関する結論の更新

元F54の**実在する経路rを持つ**依存型source slotでは、GK5AYの一様な`NativeGK5AYOriginalPhiSeam first last`が存在すると`bridge(ident(r))`を与えて3の不存在に矛盾する。ゆえに**`¬ Nonempty GK5AYOriginalPhiSeam`**を無条件に証明。同じ理由で9構成子のstrong `NativeGK5BAConstructorShellKit`も存在しない。これまでのGK5AY・GK5BAで示した条件付き組立て定理は数学的に正しいが、真正に inhabited な元F54経路文脈ではその前提は成立しないという新しい**no-go**を証明した。

これは元P89→P94Aクラス写像の無条件単射性や非単射性を証明するものではない。また、個別に成立する元F55証拠`f`の直接seamすべてを否定しない。**全域seamという統合的条件と、局所高次証拠の存在条件は分離して扱う。**

## 5. 真正北C60での異なる複合例

**元pentagon＋右identity**：実在`nativeGK5AINorthPentagonWithIdentity`のraw全体wrapperから、2個のraw wrapperを持つ`trans(original(p),original(ident))`への分解shellは不可能。しかし最終的な`φ(trans(p,ident))=trans(original(p),refl)`のwrapper数は1であり、raw全体wrapperと同じ。したがって**この不変量だけでは直接raw→φ seam不存在を結論できない**。

**元pentagon＋その逆**：実在`nativeGK5BBNorthPentagonReverseCycle := trans(p,symm(p))`において、再帰φ側は`original(p)`と`symm(original(p))`の**2個**のwrapperを持つ。一方raw全体wrapperは1個であり、**この個別の直接seamも不存在**とLean証明。

**北の全域seam／kit**：正真正銘の`northNativeF45PentagonShort`という元F54経路があるため、`¬ Nonempty (NativeGK5BAConstructorShellKit (.pentagon .north) Site Site)`および`¬ Nonempty (NativeGK5AYOriginalPhiSeam northFirst northLast)`を無条件に証明。

## 6. Qi v4.21 への接続

[Qi v4.21 PR #3032](https://github.com/itakura-hidetoshi/KuuOS/pull/3032) **MERGED**。最終exact-source HEAD `ab1e4afbf391948097568f71f67b7a803f5b1053`、main squash `61b95c4f6c3e55c5fc94e4be5a88693e32395019`。[Governance #41616589679](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41616589679) **Strict Lean 10,187/10,187 SUCCESS、Governance 30/30 SUCCESS**、9宣言公理監査で`sorryAx`なし。[Qi v4.21 Lean source](../../formal/KUOS/Architecture/QiWuxingGK5BBNorthOriginalWrapperObstructionV4_21.lean)（198行）を公開`KuuOSFormal`へimport済み。真正北C60の2つのSiteカテゴリ上で、元identityとtransのP94A不可比較、Kit／global seam／all-local-shells不存在、元右identity複合のcount compatibility、元pentagon＋逆の個別直接seam不存在、物理第五around Dart閉路とe04/e43物理方向の相違を統合する。元P89 class map非単射性は既存の**条件付きiff**のまま保持し、数値五行gaugeから元P89証拠を生成しない。

**Git tree独立一致確認：** GK5BB exact-source HEADとmain squashのtreeはともに `d301bfdb71b81e0c2ac326ec40a0fbc7527a47c3`、Qi v4.21も双方 `062c42c1fe872c40065cc065c4459953cf9fe193`。CIで検証した各ソースとmainに実際にマージされたツリーの内容は一致する。

## 7. 不変条件と次の研究

公開root **107**、保護PR **#1558 Draft/OPEN/未マージ**、Lean **v4.30.0-rc2**、mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**、strict 空／独立Kuu→Qi、append-onlyを維持。新規公理・`sorry`・`admit`・`native_decide`・Gray復元はなし。

**次の研究候補 F112-P94D3GK5BC**：今度はglobal kitの追加仮定を置かず、実際にcountが一致する**元pentagon＋右identityの個別直接seam**をさらに別の高次不変量で判定する。一方、元P89反射障害／P94Aの内部source hole／四セル存在は相互に独立であり、元P89の無条件faithfulness/nonfaithfulnessを先取りしない。