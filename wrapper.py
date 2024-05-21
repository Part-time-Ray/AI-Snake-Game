import math
import gymnasium as gym
import numpy as np
from game import Snake

class environment(gym.Env):
    def __init__(self, seed=0, size=12, training_mode=True, barrier_mode=True):
        super().__init__()
        self.game = Snake(seed=seed, size=size, training_mode=training_mode, barrier_mode=barrier_mode)
        self.action_space = gym.spaces.Discrete(4)
        #self.action_masks = self.mask
        # -1: barrier, 0: apple, 1~2, snake
        self.size = size
        self.observation_space = gym.spaces.Box(
            low=0, high=255,
            shape=(60, 60, 3),
            dtype=np.uint8
        )
        self.done = None
        self.step_cnt = 0

    def reset(self, seed=None, **options):
        self.game.reset(seed)
        self.done = False
        obs = self.get_obs()
        return obs, None
    """
    def mask(self):
        # 0: up, 1: left, 2: right, 3: down
        opposite = {'up': 3, 'left': 2, 'right': 1, 'down': 0}
        re = np.array([True] * 4)
        re[opposite[self.game.direction]] = False
        return np.array(list(re))
    """
    def Manhattan_distance(self, posa, posb):
        return abs(posa[0] - posb[0]) + abs(posa[1] - posb[1])

    def step(self, action):
        self.done, info = self.game.step(action)
        obs = self.get_obs()
        reward = 0
        self.step_cnt += 1
        if self.step_cnt >= self.size * self.size * 3:  # too much step
            self.done = True
        if self.done:
            reward += (info["snake_len"] - self.size**2)  # (-141,  0)
            self.step_cnt = 0
        elif info['eat_food']:
            reward += math.exp((self.size**2 - self.step_cnt) / self.size**2) + (info["snake_len"] / self.size**2)  # (0, e)
            self.step_cnt = 0
        else:
            if self.Manhattan_distance(info['now_head'], info['food']) < self.Manhattan_distance(info['prev_head'], info['food']):
                reward += 2 / info['snake_len']
            else:
                reward += -2 / info['snake_len']
        # entropy
        zone = list()
        maze = np.zeros((self.size, self.size))
        for pos in self.game.snake:
            maze[pos] = -1
        if self.game.barrier_mode:
            for pos in self.game.barrier:
                maze[pos] = -1
        for i in range(self.size):
            for j in range(self.size):
                if maze[i, j] != -1:
                    zone.append(self.dfs(i, j, maze))
        reward += -self.entropy(zone) * (info['snake_len'] / self.size**2)
        reward = reward * 0.1
        return obs, reward, self.done, False, info

    def entropy(self, vec):
        s = sum(vec)
        prob = [cnt / s for cnt in vec]
        ent = -np.sum([p * np.log(p) for p in prob if p > 0])
        return ent

    def dfs(self, i, j, maze):
        if i < 0 or i >= self.size or j < 0 or j >= self.size or maze[i, j] == -1:
            return 0
        zone = 1
        maze[i, j] = -1
        zone += self.dfs(i + 1, j, maze)
        zone += self.dfs(i - 1, j, maze)
        zone += self.dfs(i, j + 1, maze)
        zone += self.dfs(i, j - 1, maze)
        return zone

    def get_obs(self):
        re = np.zeros((self.size, self.size, 3), dtype=np.uint8)
        gray = np.linspace(200, 50, len(self.game.snake), dtype=np.uint8)
        for i, pos in enumerate(self.game.snake):
            re[pos[0], pos[1], :] = gray[i]
        re[self.game.snake[0]] = [0, 255, 0]
        if self.game.barrier_mode:
            for i, pos in enumerate(self.game.barrier):
                re[pos[0], pos[1], :] = [255, 0, 0]
        re[self.game.food] = [0, 0, 255]
        re = np.repeat(np.repeat(re, 5, axis=0), 5, axis=1)
        return re

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()

        
if __name__ == '__main__':
    import random
    import pygame
    import sys
    import time
    env = environment(seed=random.randint(0,1e9), training_mode=False, barrier_mode=False)
    update_interval = 0.1
    for eps in range(10):
        print(f'==============Episode {eps+1}==============')
        env.reset()
        start_time = time.time()
        done = False
        action = 0
        total_reward = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        action = 0
                    elif event.key == pygame.K_DOWN:
                        action = 3
                    elif event.key == pygame.K_LEFT:
                        action = 1
                    elif event.key == pygame.K_RIGHT:
                        action = 2
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if time.time() - start_time >= update_interval:
                obs, reward, done, _, info = env.step(action)
                total_reward += reward
                if info['eat_food']:
                    print('=> eat food!!')
                    print(f"\tsnake length: {info['snake_len']}, reward: {reward}, score: {info['score']}")
                else:
                    print(f"reward: {reward}, score: {info['score']}")
                env.render()
                start_time = time.time()
            if done==True:
                print(f"===> Total score: {info['score']}, Total reward: {total_reward}")
                pygame.time.wait(1000)
                break
    env.close()