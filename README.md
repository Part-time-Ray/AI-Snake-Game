# AI Playing Snake Game

[繁體中文](README_CHINESE.md) | English | [日本語](README_JAPANESE.md)

Using the **PPO** algorithm combined with the **CNN** architecture, we achieve AI agent control of the Snake game.

The basic structure of the game is located in `game.py`, and `wapper.py` is used to package the environment for model operation.\
The code for training and testing the model is located in `train.py` and `test.py`.\
The final trained model is in the `model/` folder, while models during training are in the `cnn_log/log/` folder.\
`cnn_log/logs/PPO_0/` contains tensorboard logs of the training process.

### Results

On a $12×12$ board:
- After 50 million steps: the average length of the snake reaches 74
- After 100 million steps: the average length of the snake reaches 98

### File Structure

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

### Environment Setup

Developed using Python in an Anaconda environment.

```bash!
conda create --name Snake python=3.10.14
conda activate Snake
```

```bash!
conda install pytorch=2.2.2 torchvision pytorch-cuda -c pytorch -c nvidia
conda install tensorflow
pip install pygame==2.5.2 gym==0.26.2 gymnasium==0.29.1 stable-baselines3==2.3.2 tensorboard==2.9.1
```

or use the packaged environment `snake.yml`
```bash!
conda env create --file snake.yml --name Snake
```

### Acknowledgements
Inspired by this [Video](https://www.youtube.com/watch?v=jTVMxJBtmFs).\
Thanks for the explanation and analysis of many knowledge points.

