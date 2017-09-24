# FP-master


## ex01.py

### description
指定した回数予測を行なって、平均を取ったAUC値と、F1値を出力する。
同時に両方の値を求めることはできず、内部のプログラムを変更する必要がある。

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
