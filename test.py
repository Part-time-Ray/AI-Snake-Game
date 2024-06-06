from wrapper import environment
from stable_baselines3 import PPO
import os
import time
import pygame
import sys
import random
# set visualization
visualization = True

env = environment(seed=random.randint(0, 1e9), training_mode=not visualization, barrier_mode=False)
path = os.getcwd()
file =  '.\model\model.zip'

# getting the model
model = PPO.load(os.path.join(path, file), env)
delay = 0.01
total_eps = 20
total_snake_len = 0
total_score = 0
for eps in range(total_eps):
    print(f'==============Episode {eps+1}==============')
    obs, _ = env.reset()
    total_reward = 0
    while True:
        action, _ = model.predict(obs)
        obs, reward, done, _, info = env.step(action)
        total_reward += reward
        if visualization:
            env.render()
            if info['eat_food']:
                print('=> eat food!!')
                print(f"\tsnake length: {info['snake_len']}, reward: {reward}, score: {info['score']}")
            else:
                print(f"reward: {reward}, score: {info['score']}")
            time.sleep(delay)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        if done:
            if visualization:
                time.sleep(1)
            break
    total_snake_len += info['snake_len']
    total_score += info['score']
    print(f"===> Snake Length: {info['snake_len']}, Total score: {info['score']}, Total reward: {total_reward}")
print(f"Average Snake Length: {total_snake_len/total_eps:.2f}, Average Score: {total_score/total_eps:.2f}")
env.close()
