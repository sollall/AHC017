# AHC_template

## 使い方
以下のコマンドを参考に、AHC提出用のスクリプトを引数で指定してdebug.pyを実行することで各テストケースを実行することができる。

``` bash
python debug.py --module_name scripts.sample --test_id 0 --epsilon 0.1 cooling_rate 0.1 epoch 100
```
- あるハイパーパラメータを設定して各テストケースでソルバーを実行する
- 出力ログを残したい場合は上記のコマンドを使用

``` bash
python optimizer.py
```
- configで指定したscriptsのハイパーパラメータ探索を行う
- 出力ログは残らない

### 留意点
- scriptには自作したsolve()を含む必要がある、main()はdebug.pyが使用する用なので基本変更する必要はない
- scriptごとに適したconfig.yamlをconf内に作成してもらう
    - cfg.optimizerを自作solverに与える


## 機能

### debug.py


### optimzer.py
- 複数のテストケースを自動で並列に実行
- optunaでのパラメータ最適化
- mlflowで実験記録、スコアの可視化を保存(予定)