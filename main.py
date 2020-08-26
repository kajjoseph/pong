import pygame as pg
import random as rng
import sys
from config import *
from pygame.locals import *

pg.init()

multi_player = False

BG = BLACK
FG = GREEN
TEXT = BLUE


class Paddle(pg.sprite.Sprite):
    
    def __init__(self, master, x, y, up, down):
        self.master = master
        self.lists = master.all_sprites, master.paddles
        pg.sprite.Sprite.__init__(self, self.lists)
        self.image = pg.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(FG)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.up = up
        self.down = down
        self.score = 0
        self.speed = PADDLE_SPEED
        self.dir = 0
    
    def update(self, input):
        if input[self.up]:
            self.rect.centery -= self.speed
        if input[self.down]:
            self.rect.centery += self.speed
        self.rect.clamp_ip(self.master.display_rect)


class cpuPaddle(Paddle):

    def __init__(self, master, x, y):
        Paddle.__init__(self, master, x, y, None, None)
        self.speed = CPU_PADDLE_SPEED
        self.frame_counter = 0

    def update(self, input):
        ball = self.master.ball
        if self.frame_counter % BALL_CHECK_INTERVAL == 0:
            if ball.rect.bottom < self.rect.top:
                self.dir = -1
            elif ball.rect.top > self.rect.bottom:
                self.dir = 1
        self.rect.centery += self.speed * self.dir
        self.rect.clamp_ip(self.master.display_rect)
        self.frame_counter += 1
        if self.frame_counter > FPS:
            self.frame_counter = 0


class Ball(pg.sprite.Sprite):

    def __init__(self, master):
        self.master = master
        self.lists = master.all_sprites
        pg.sprite.Sprite.__init__(self, self.lists)
        self.image = pg.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(FG)
        self.rect = self.image.get_rect()
        self.rect.center = (BALL_X, BALL_Y)
        self.x_dir = rng.choice([-1, 1])
        self.y_dir = rng.choice([-1, 1])
        self.x_speed = BALL_X_SPEED
        self.y_speed = BALL_Y_SPEED
    
    def check_collision(self):
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            self.y_dir *= -1
        if any(pg.sprite.spritecollide(self, self.master.paddles, False)):
            self.x_dir *= -1
            if rng.choice([True, False]):
                self.y_dir *= -1
                if self.y_speed < BALL_MAX_SPEED:
                    self.y_speed += 1
            if self.x_speed < BALL_MAX_SPEED:
                self.x_speed += 1
    
    def scored(self):
        if self.master.player1.score >= 5 or self.master.player2.score >= 5:
            self.master.reset_screen(True)
        if self.rect.left <= self.master.player1.rect.left:
            self.master.player2.score += 1
            self.master.reset_screen()
        if self.rect.right >= self.master.player2.rect.right:
            self.master.player1.score += 1
            self.master.reset_screen()

    def update(self, input):
        self.check_collision()
        self.scored()
        self.rect.centerx += self.x_speed * self.x_dir
        self.rect.centery += self.y_speed * self.y_dir
        self.rect.clamp_ip(self.master.display_rect)
        

class Game:

    def __init__(self):
        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        self.display_rect = self.display.get_rect()
        self.paddles = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.player1 = Paddle(self, PLAYER1_X, PLAYER1_Y, K_w, K_s)
        if multi_player:
            self.player2 = Paddle(self, PLAYER2_X, PLAYER2_Y, K_UP, K_DOWN)
        else:
            self.player2 = cpuPaddle(self, PLAYER2_X, PLAYER2_Y)
        self.ball = Ball(self)
        self.large_font = pg.font.SysFont(*LARGE_FONT)
        self.small_font = pg.font.SysFont(*SMALL_FONT)
        self.running = True
        self.clock = pg.time.Clock()

    def title_screen(self):
        while True:
            self.display.fill(BG)
            title = self.large_font.render('PONG', False, FG)
            subtitle = self.small_font.render('Press Spacebar to continue.', False, FG)
            self.display.blit(title, (int(WIDTH/3), int(HEIGHT/3)))
            self.display.blit(subtitle, (int(40), int(HEIGHT-100)))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.loop()
            pg.display.update()
            self.clock.tick(FPS)

    def loop(self):
        while self.running:
            self.display.fill(BG)
            keys = pg.key.get_pressed()
            self.all_sprites.update(keys)
            self.all_sprites.draw(self.display)
            p1_score = self.large_font.render(f'{self.player1.score}', False, TEXT)
            p2_score = self.large_font.render(f'{self.player2.score}', False, TEXT)
            self.display.blit(p1_score, (100, 100))
            self.display.blit(p2_score, (WIDTH-100-p2_score.get_width(), 100))
            for event in pg.event.get():
                if event.type == QUIT:
                    self.running = False
                    pg.quit()
                    sys.exit()
                    break
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        self.player1.score = 5
            pg.display.update()
            self.clock.tick(FPS)

    def reset_screen(self, game_over=False):
        delay_counter = 0
        while delay_counter <= RESET_DELAY * FPS:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                    break
            self.all_sprites.draw(self.display)
            pg.display.update()
            delay_counter += 1
            self.clock.tick(FPS)
        self.player1.rect.center = (PLAYER1_X, PLAYER1_Y)
        self.player2.rect.center = (PLAYER2_X, PLAYER2_Y)
        self.ball.rect.center = (BALL_X, BALL_Y)
        self.ball.x_dir = rng.choice([1, -1])
        self.ball.y_dir = rng.choice([1, -1])
        self.ball.y_speed = BALL_Y_SPEED
        self.ball.x_speed = BALL_X_SPEED
        if not game_over:
            self.loop()
        else:
            self.game_over_screen()

    def game_over_screen(self):
        winner = 'Player 1' if self.player1.score > self.player2.score else 'Player 2'
        victory_msg = self.large_font.render(f'{winner} wins!', False, TEXT)
        prompt1 = self.small_font.render('Press spacebar to start again', False, TEXT)
        prompt2 = self.small_font.render('or escape to exit', False, TEXT)
        while True:
            self.display.fill(bg)
            self.display.blit(victory_msg, (25, 125))
            self.display.blit(prompt1, (15, 425))
            self.display.blit(prompt2, (125, 450))
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    elif event.key == K_SPACE:
                        self.player1.score = 0
                        self.player2.score = 0
                        self.loop()
            pg.display.update()
            self.clock.tick(FPS)


game = Game()
game.title_screen()
