# FP-master


## ex01.py

### description
指定した回数予測を行なって、平均を取った指標を出力する。
予測結果はバイナリの値で出力され、AUCを求めることはできない

### output
accuracy, recall, precision 

### paramater

| param | value                           | 
|-------|---------------------------------|
| 1     | target_sw                       |
| 2     | iteration number                |
| 3     | predict_type (e.g. rf, svn,...) |


### command example
```
python ex01.py derby 50 rf
```

## ex02.py

### description
変更のないモデルにはプロダクトメトリクスのみを用いたモデルで予測を行い、変更のあるモデルにはプロセスメトリクスを用いたモデルで予測を行った。

### output
F1 value

### paramater

| param | value                           | 
|-------|---------------------------------|
| 1     | target_sw                       |
| 2     | iteration number                |
| 3     | predict_type (e.g. rf, svn,...) |


### command example
```
python ex02.py solr 100 rf
```

## ex01_prob.py

### description
AUCの値を求める

### output
- AUCの面積の試行回数の平均分を集めたSW-rf.csv
- 予測確率を試行回数全ての値を保存したacm-pv.csvがある。

