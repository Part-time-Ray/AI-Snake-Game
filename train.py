from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from wrapper import environment
import os
import time
import random

def make_env():
    return environment(seed=random.randint(0, 1e9), training_mode=True)

env = environment()
vec_env = DummyVecEnv([make_env for i in range(32)])

path = 'log'
checkpoint_callback = CheckpointCallback(save_freq=31250, save_path='log', name_prefix="model")
files = os.listdir(path)
if files:
    file = max(files, key=lambda f: os.path.getmtime(os.path.join(path, f)))
    model = PPO.load(os.path.join(path, file), vec_env)
else:
    model = PPO("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=100000000, callback=checkpoint_callback, reset_num_timesteps=False)
model.save("model")