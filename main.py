import pygame
import time
import random

def gamesettings():
    global win_w
    global score
    global win_h
    global win
    global clock
    global font
    global checkpointsound
    global jumpsound
    score = 0
    pygame.init()
    win_w = 1280
    win_h = 720
    win = pygame.display.set_mode((win_w, win_h))
    clock = pygame.time.Clock()
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    checkpointsound = pygame.mixer.Sound('sfx_point.wav')
    jumpsound = pygame.mixer.Sound('sfx_wing.wav')

gamesettings()

def ending():

    text_surface1 = font.render("Game over.", True, (0, 154, 205))
    win.blit(text_surface1, dest=(200, 200))
    text_surface2 = font.render("Score: " + str(score), True, (0, 154, 205))
    win.blit(text_surface2, dest=(200, 240))
    pygame.display.update()
    time.sleep(1)
    text_surface3 = font.render("Press Enter to play again", True, (0, 154, 205))
    win.blit(text_surface3, dest=(300, 320))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gamesettings()
                    game()

class Bird:

    def __init__(self):
        self.x = win_w * 0.2
        self.y = win_h * 0.5
        self.vsp = 0
        self.jumpsp = win_h * 0.015
        self.grv = win_h * 0.00069  # Nice
        self.body = pygame.Rect(self.x, self.y, win_h * 0.05, win_h * 0.05)

    def jump(self):
        self.vsp = -self.jumpsp


    def move(self):

        self.vsp += self.grv
        self.y += self.vsp
        self.body.y = self.y

    def vypis(self):
        text_surface2 = font.render(str(self.y), True, (0, 154, 0))

        text_surface1 = font.render("Score: "+str(score), True, (0, 154, 0))
        win.blit(text_surface2, dest=(0, 0))
        win.blit(text_surface1, dest=(0, 50))

    def checkfordeath(self, obstacles):
        global  game_resumed
        for obstacle in obstacles:
            if bird.body.colliderect(obstacle) or bird.body.colliderect(pygame.Rect(
                    obstacle.x,
                    obstacle.y - win_h * 1.25,
                    obstacle.width,
                    obstacle.height
            )):
                ending()
        if (bird.body.y <= -700 and number_of_obstacles >= 4) or (bird.body.y >= 1000  and number_of_obstacles >= 4):
            ending()


class ObstaclesManager:
    global score
    score = 0

    def __init__(self):
        self.obstacles_list = []

    def generateobstacles(self):
        global score

        global number_of_obstacles

        can_gen = True
        for obstacle in self.obstacles_list:
            if obstacle.x > win_w * 0.7435:
                can_gen = False

        if can_gen:
            self.obstacles_list.append(
                pygame.Rect(
                    win_w,
                    random.randint(win_h * 0.25, win_h * 0.8),
                    win_w * 0.075,
                    win_h
                )

            )
            number_of_obstacles = len(self.obstacles_list)
            if number_of_obstacles >= 4:

                score += 1



    def scrollscene(self):
        for obstacle in self.obstacles_list:
            obstacle.x -= win_w * 0.0025
            if obstacle.x < 0 - obstacle.width:
                self.obstacles_list.remove(obstacle)
                checkpointsound.play()

def game():
    global bird
    global manager
    manager = ObstaclesManager()
    bird = Bird()

    global game_resumed
    game_resumed= False

    while True:
        clock.tick(60)
        win.fill((28, 28, 28))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jumpsound.play()
                    bird.jump()
                    game_resumed = True

        if game_resumed:
            manager.generateobstacles()
            manager.scrollscene()
            bird.move()
            bird.vypis()
            bird.checkfordeath(obstacles=manager.obstacles_list)

        pygame.draw.rect(win, (255, 255, 255), bird.body)
        for obstacle in manager.obstacles_list:
            pygame.draw.rect(win, (0, 154, 205), obstacle)
            pygame.draw.rect(win, (0, 154, 205), pygame.Rect(
                obstacle.x,
                obstacle.y - win_h * 1.25,
                obstacle.width,
                obstacle.height
            ))

        pygame.display.update()

game()