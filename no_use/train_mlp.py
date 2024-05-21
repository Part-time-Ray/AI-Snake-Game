from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from wrapper_mlp import environment
import os
import time
import random

if __name__ == '__main__':
    def make_env(seed):
        def f():
            env = environment(seed, training_mode=True)
            return env
        return f
    
    vec_env = SubprocVecEnv([make_env(random.randint(0,1e9)) for i in range(32)])
    path = os.path.join('mlp_log', 'log')
    os.makedirs(path, exist_ok=True)
    checkpoint_callback = CheckpointCallback(save_freq=312500, save_path='log', name_prefix="subproc")
    
    LOG_DIR = os.path.join('mlp_log', 'logs')
    os.makedirs(LOG_DIR, exist_ok=True)
    
    files = os.listdir(path)
    if files:
        file = max(files, key=lambda f: os.path.getmtime(os.path.join(path, f)))
        model = PPO.load(os.path.join(path, file), vec_env, verbose=1, tensorboard_log=LOG_DIR)
    else:
        model = PPO("MlpPolicy", vec_env, verbose=1, tensorboard_log=LOG_DIR)
    model.learn(total_timesteps=100000000, callback=checkpoint_callback, reset_num_timesteps=False)
    model.save("model")

