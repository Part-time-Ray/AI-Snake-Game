from wrapper import environment
import os
import time
import pygame
import sys
import random
from stable_baselines3 import PPO
env = environment(seed=random.randint(0, 1e9), training_mode=False)
path = "model"
model = PPO.load(os.path.join(path, 'lazy_snake'), env)
delay = 0.1
for eps in range(20):
    print(f'==============Episode {eps+1}==============')
    obs = env.reset()
    total_reward = 0
    while True:
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        env.render()
        if info['eat_food']:
            print(f"snake length: {info['snake_len']}, reward: {reward}, score: {info['score']}")
        total_reward += reward
        time.sleep(delay)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if done:
            time.sleep(1)
            break
    print(f"===> Total score: {info['score']}, Total reward: {total_reward}")
env.close()