## Kolmogorov-Smirnov test

２標本間をコルモゴルフスルミノフ検定できるpythonモジュールはない。

- p値が0.05以下のとき、帰無仮説を棄却できる
- 帰無仮説は「二つの分布が等しい」である。


import scipy.stats
scipy.stats.ks_2samp(a, b)

## Rのkstestが連続でできない

### エラーメッセージ
p-value will be approximate in the presence of ties

### 原因
The presence of ties always generates a warning, since continuous distributions do not generate them. If the ties arose from rounding the tests may be approximately valid, but even modest amounts of rounding can have a significant effect on the calculated statistic.

### tiesとは
ノンパラメトリックな検定手法では，観察値の順位をつける。観察値のいくつかが全く同じ値を持つ場合，同順位が存在するという。同順位があった場合には平均順位がつけられる。また，検定統計量の求めかたには若干の修正が伴う。
