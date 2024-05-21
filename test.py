from wrapper import environment
import os
import time
import pygame
import sys
import random
from sb3_contrib import MaskablePPO
from stable_baselines3 import PPO
env = environment(seed=random.randint(0, 1e9), training_mode=False, barrier_mode=False)
path = os.path.join('cnn_log', "log")
files = os.listdir(path)
file = max(files, key=lambda f: os.path.getmtime(os.path.join(path, f)))
print(file)
model = PPO.load(os.path.join(path, file), env)
delay = 0.05
for eps in range(50):
    print(f'==============Episode {eps+1}==============')
    obs, _ = env.reset()
    total_reward = 0
    while True:
        action, _ = model.predict(obs)
        obs, reward, done, _, info = env.step(action)
        env.render()
        if info['eat_food']:
            print('=> eat food!!')
            print(f"\tsnake length: {info['snake_len']}, reward: {reward}, score: {info['score']}")
        else:
            print(f"reward: {reward}, score: {info['score']}")
        total_reward += reward
        time.sleep(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if done:
            time.sleep(1)
            break
    print(f"===> Snake Length: {info['snake_len']}, Total score: {info['score']}, Total reward: {total_reward}")
env.close()
