# AI Playing Snake Game

[繁體中文](README_CHINESE.md) | [English](README.md) | 日本語

**PPO**アルゴリズムと**CNN**アーキテクチャを組み合わせて、AIエージェントがスネークゲームを操作します。

ゲームの基本構造は`game.py`にあり、`wapper.py`はモデル操作に有利な環境をパッケージ化するために使用されます。\
モデルのトレーニングとテストのコードは`train.py`と`test.py`にあります。\
最終的な訓練モデルは`model/`フォルダにあり、訓練中のモデルは`cnn_log/log/`フォルダにあります。\
`cnn_log/logs/PPO_0/`には訓練プロセスのtensorboardログが含まれています。

### 結果

$12×12$ のボード上で:
- 5000万ステップ後: スネークの平均長さは74に達します
- 1億ステップ後: スネークの平均長さは98に達します

### ファイル構造

```bash
│
├─model
├─cnn_log
│  ├──log
│  └──logs/PPO_0
│ game.py
│ test.py
│ train.py
│ wrapper.py
│ snake.yml
│
```

### 環境セットアップ

Anaconda環境でPythonを使用して開発されました。

```bash!
conda create --name Snake python=3.10.14
conda activate Snake
```

```bash!
conda install pytorch=2.2.2 torchvision pytorch-cuda -c pytorch -c nvidia
conda install tensorflow
pip install pygame==2.5.2 gym==0.26.2 gymnasium==0.29.1 stable-baselines3==2.3.2 tensorboard==2.9.1
```

または、パッケージ化された環境`snake.yml`を使用します:

```bash!
conda env create --file snake.yml --name Snake
```

### 感謝
この[ビデオ](https://www.youtube.com/watch?v=jTVMxJBtmFs)からインスピレーションを受けました。\
多くの知識点の説明と分析に感謝します。

