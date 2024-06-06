# AI Playing Snake Game

繁體中文 | [English](README.md) | [日本語](README_JAPANESE.md)

使用**PPO**算法搭配**CNN**架構，實現由人工智慧代理貪吃蛇遊戲的操作。

遊戲的基本架構位於`game.py`，`wapper.py`用於包裝成有利於模型操作的環境。\
訓練和測試模型的程式碼位於`train.py`和`test.py`當中。\
`model/`中含有最終的訓練模型，對於訓練過程當中的模型位於資料夾`cnn_log/log/`當中，\
`cnn_log/logs/PPO_0/`有包含訓練過程的tensorboard日誌。

### 成果

在 $12\times12$ 的棋盤上
訓練5000萬步後: 平均每局貪吃蛇的長度到達74
訓練1億步後: 平均每局貪吃蛇的長度到達98

### 文件結構

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


### 環境設置

使用python在Anaconda環境下撰寫

```bash
conda create --name Snake python=3.10.14
conda activate Snake
```

```bash
conda install pytorch=2.2.2 torchvision pytorch-cuda -c pytorch -c nvidia
conda install tensorflow
pip install pygame==2.5.2 gym==0.26.2 gymnasium==0.29.1 stable-baselines3==2.3.2 tensorboard==2.9.1
```

或者使用打包好的環境`snake.yml`
```bash!
conda env create --file snake.yml --name Snake
```

### 查看tensorboard日誌

```bash
tensorboard --logdir="cnn_log/logs/"
```

### 感謝

本項目靈感來源[Video](https://www.youtube.com/watch?v=jTVMxJBtmFs)\
感謝其對許多知識論點的解釋分析