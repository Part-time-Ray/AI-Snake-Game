import pygame, sys
import random
import time
class Snake:
    def __init__(self, seed=0, size=12, screen_width=760, screen_height=820, margin=20, training_mode=False, barrier_mode=True):
        self.training_mode = training_mode
        self.barrier_mode = barrier_mode
        if not self.training_mode:
            pygame.init()
            pygame.display.set_caption("Snake")
            self.width = screen_width
            self.height = screen_height
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.font = pygame.font.Font('freesansbold.ttf', 32)
            self.margin = margin
            self.rect_size = 60
        random.seed(seed)
        self.size = size
        if self.barrier_mode:
            self.barrier = list()
        self.snake = None
        self.food = None
        self.score = None
        self.score_text = None
    def reset(self, seed=None):
        if seed:
            random.seed(seed)
        self.snake = [(self.size//2, self.size//2+i) for i in range(3)]
        self.space = set([(i,j) for i in range(self.size) for j in range(self.size) if (i,j) not in self.snake])
        if self.barrier_mode:
            self.barrier = self.renew_barrier()
        self.direction = 'up'
        self.food = self.make_food()
        self.score = 0
        if not self.training_mode:
            pygame.time.wait(1000)
            pygame.display.update()
    def pos_to_rect_pos(self, pos):
        return (self.margin  + pos[0]*self.rect_size, self.margin  + pos[1]*self.rect_size, self.rect_size, self.rect_size)
    def make_food(self):
        return random.sample(self.space, 1)[0] if len(self.space) else None
    def _filter_function(self, pos):
        a, b = pos
        return self.snake[0] not in [(a+1,b), (a-1,b), (a,b+1), (a,b+1)] and (a,b) not in self.snake
    def renew_barrier(self):
        for pos in self.barrier:
            self.space.add(pos)
        if len(self.snake)>=self.size**2/3:
            new_barrier = list()
        else:
            new_barrier = list(filter(self._filter_function, random.sample([(a,b) for a in range(self.size) for b in range(self.size)], random.randint(0, 3))))
        for pos in new_barrier:
            self.space.remove(pos)
        return new_barrier
    def update_direction(self, act):
        # 0: up, 1: left, 2: right, 3: down
        match act:
            case 0:           #up
                 if self.direction!='down':
                     self.direction='up'
            case 1:           #left
                 if self.direction!='right':
                     self.direction='left'
            case 2:           #right
                 if self.direction!='left':
                     self.direction='right'
            case 3:           #down
                if self.direction!='up':
                    self.direction='down'
    def step(self, act):
        a, b = self.snake[0]
        self.update_direction(act)
        match self.direction:
            case 'up':
                b-=1
            case 'right':
                a+=1
            case 'left':
                a-=1
            case 'down':
                b+=1
        eat_food = None
        done = None
        if a<0 or a>=self.size or b<0 or b>=self.size or (a,b) in self.snake or (self.barrier_mode and (a,b) in self.barrier):
            done = True
        else:
            if (a,b)==self.food:
                self.snake.insert(0, (a,b))
                self.space.remove((a,b))
                if self.barrier_mode:
                    self.barrier = self.renew_barrier()
                self.food = self.make_food()
                self.score += 1+len(self.snake)
                eat_food = True
            else:
                self.snake.insert(0, (a,b))
                self.space.remove((a,b))
                self.space.add((self.snake[-1]))
                self.snake.pop()
                eat_food = False   
        done = done or len(self.snake) == self.size**2
        info = {
            'snake_len': len(self.snake),
            'prev_head': self.snake[1],
            'now_head': self.snake[0],
            'score': self.score,
            'food': self.food,
            'eat_food': eat_food,
            'done': done    
        }
        return done, info
                
    def render(self):
        #background
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.margin - 2, self.margin - 2, self.rect_size*self.size + 4, self.rect_size*self.size + 4), 2)
        
        #draw snake
        for index, pos in enumerate(self.snake):
            pygame.draw.rect(self.screen, (0, 150+(105/144*index), 255-(255/144*index)) if index!=0 else (134, 231, 70), self.pos_to_rect_pos(pos), 0, 10)
        
        #draw food
        pygame.draw.rect(self.screen, (255, 15, 15), self.pos_to_rect_pos(self.food), 0, 10)
            
        #draw barrier
        if self.barrier_mode:
            for index, pos in enumerate(self.barrier):
                pygame.draw.rect(self.screen, (255,255,255), self.pos_to_rect_pos(pos), 5, 10)
            
        #draw score
        self.score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(self.score_text, (50, self.margin + 20 + self.size*self.rect_size))
        
        pygame.display.flip()
    def close(self):
        pygame.quit()
        sys.exit()
    def run(self):
        self.reset()
        action = 0
        start_time = time.time()
        update_interval = 0.08
        done = False
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
                done, _ = game.step(action)
                game.render()
                start_time = time.time()
            if done==True:
                self.reset()
                action = 0
                pygame.time.wait(1000)
            
                
            
if __name__ == '__main__':
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    game = Snake(barrier_mode=False)
    game.run()
    